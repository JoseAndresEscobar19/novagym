from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from novagym.utils import calculate_pages_to_render
from push_notifications.models import APNSDevice, GCMDevice
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
    permission_required = 'novagym.view_empleado'
    permission_required = 'notificacion.view_notificacion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Notificaciones"
        page_obj = context["page_obj"]
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        return context


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

    def post(self, request, *args, **kwargs):
        messages.success(request, "Notificación creada con éxito.")
        return super().post(request, *args, **kwargs)


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

    def post(self, request, *args, **kwargs):
        messages.success(request, "Notificación editada con éxito.")
        return super().post(request, *args, **kwargs)


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


#TODO: Enviar por batches, no uno por uno
def enviarNotificacionGlobal(request, id_notificacion):
    notificacion = Notificacion.objects.get(id=id_notificacion)
    dispositivos = GCMDevice.objects.all()
    for dispositivo in dispositivos:
        dispositivo.send_message(notificacion.cuerpo, extra={
                                 "title": notificacion.titulo, "image": notificacion.imagen})
    messages.success(request, "Notificación enviada a todos los usuarios.")
    return redirect('notificaciones:listar')


def enviarNotificacionIndividual(request, id_notificacion, usuario):
    notificacion = Notificacion.objects.get(id=id_notificacion)
    dispositivos = GCMDevice.objects.filter(user=usuario).send_message(
        notificacion.cuerpo, extra={"title": notificacion.titulo, "image": notificacion.imagen})
    messages.success(request, "Notificación enviada al usuario "+usuario+".")
    return redirect('notificaciones:listar')
