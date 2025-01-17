from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from novagym.utils import calculate_pages_to_render
from push_notifications.models import GCMDevice
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from seguridad.views import UsuarioPermissionRequieredMixin

from notificaciones.forms import NotificacionForm

from .models import *
from .serializers import *

# Create your views here.


@api_view(["GET"])
def notificacionList(request):
    sponsors = Notificacion.objects.all()
    serializer = NotificacionSerializer(sponsors, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def notificacionDetail(request, id):
    sponsors = Notificacion.objects.get(id=id)
    serializer = NotificacionSerializer(sponsors, many=False)
    return Response(serializer.data)


@api_view(["POST"])
def notificacionCreate(request):
    serializer = NotificacionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def notificacionUpdate(request, id):
    sponsor = Notificacion.objects.get(id=id)
    serializer = NotificacionSerializer(instance=sponsor, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["DELETE"])
def notificacionDelete(request, id):
    sponsor = Notificacion.objects.get(id=id)
    try:
        sponsor.delete()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListarNotificacion(LoginRequiredMixin, UsuarioPermissionRequieredMixin, ListView):
    paginate_by = 20
    max_pages_render = 10
    model = Notificacion
    context_object_name = 'notificacion'
    template_name = "lista_notificaciones.html"
    permission_required = 'notificacion.view_notificacion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Notificaciones"
        page_obj = context["page_obj"]
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        return context

    def get_queryset(self):
        return self.model.objects.filter(tipo=Notificacion.Tipo.Admin)


class CrearNotificacion(LoginRequiredMixin, UsuarioPermissionRequieredMixin, CreateView):
    form_class = NotificacionForm
    model = Notificacion
    template_name = 'notificacion_nueva.html'
    title = "Agregar notificación"
    success_url = reverse_lazy('notificaciones:listar')
    permission_required = 'notificacion.add_notificacion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def form_valid(self, form):
        messages.success(self.request, "Notificación creada con éxito.")
        return super().form_valid(form)


class UpdateNotificacion(LoginRequiredMixin, UsuarioPermissionRequieredMixin, UpdateView):
    form_class = NotificacionForm
    model = Notificacion
    title = "Editar notificación"
    template_name = 'notificacion_nueva.html'
    success_url = reverse_lazy('notificaciones:listar')
    permission_required = 'notificacion.change_notificacion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def form_valid(self, form):
        messages.success(self.request, "Notificación editada con éxito.")
        return super().form_valid(form)


def deleteNotificacion(request, id):
    query = Notificacion.objects.get(id=id)
    if request.POST:
        query.delete()
        messages.success(request, "Notificacion eliminada con éxito.")
        return redirect('notificaciones:listar')
    return render(request, "ajax/notificacion_confirmar_elminar.html", {"notificacion": query})


@login_required
@permission_required('notificacion.delete_notificacion')
def changeState(request, pk):
    notificacion = Notificacion.objects.get(id=pk)
    if request.POST:
        notificacion.activo = not notificacion.activo
        if notificacion.activo:
            messages.success(request, "Notificación habilitada con éxito.")
        else:
            messages.info(request, "Notificación deshabilitada con éxito.")
        notificacion.save()
        return redirect('notificaciones:listar')
    if notificacion.activo:
        return render(request, "ajax/notificacion_confirmar_elminar.html", {"notificacion": notificacion})
    return render(request, "ajax/notificacion_confirmar_activar.html", {"notificacion": notificacion})


@login_required
@permission_required('notificacion.delete_notificacion')
def notificacion_confirmar_eliminar(request, pk):
    notificacion = Notificacion.objects.get(id=pk)
    if request.POST:
        messages.info(request, "Notificación eliminada.")
        notificacion.delete()
        return redirect('notificaciones:listar')
    return render(request, "ajax/notificacion_confirmar_elminar_perma.html", {"notificacion": notificacion})


# Ref: https://github.com/jazzband/django-push-notifications#sending-messages-in-bulk
def enviarNotificacionGlobal(request, id_notificacion):
    notificacion = Notificacion.objects.get(id=id_notificacion)
    imagen = request.build_absolute_uri('/')+notificacion.imagen.url[1:]
    GCMDevice.objects.all().send_message(notificacion.cuerpo, extra={
        "title": notificacion.titulo, "image": imagen})
    report = NotificacionUsuario(notificacion=notificacion,
                                 sender=request.user, grupo_usuarios=Group.objects.get(name='Todos'))
    report.save()
    messages.success(request, "Notificación enviada a todos los usuarios.")
    return redirect('notificaciones:listar')


def enviarNotificacionIndividual(request, id_notificacion, usuario):
    notificacion = Notificacion.objects.get(id=id_notificacion)
    imagen = request.build_absolute_uri('/')+notificacion.imagen.url[1:]
    GCMDevice.objects.filter(user=usuario).send_message(
        notificacion.cuerpo, extra={"title": notificacion.titulo, "image": imagen})
    messages.success(request, "Notificación enviada al usuario "+usuario+".")
    return redirect('notificaciones:listar')
