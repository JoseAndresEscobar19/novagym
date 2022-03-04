from django.forms import BooleanField
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.shortcuts import render
from django.urls import reverse_lazy
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django_filters.views import FilterView
from .forms import *
from .serializers import *
from django.core.mail import send_mail
from novagym.utils import calculate_pages_to_render
from datetime import date
from .models import *
from django.contrib import messages
import json
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView
from push_notifications.models import APNSDevice, GCMDevice
# Create your views here.
#SPONSOR

@api_view(["GET"])
def notificacionList(request):
    sponsors= Notificacion.objects.all()
    serializer=NotificacionSerializer(sponsors,many=True)
    return Response(serializer.data)

@api_view(["GET"])
def notificacionDetail(request,id):
    sponsors= Notificacion.objects.get(id=id)
    serializer=NotificacionSerializer(sponsors,many=False)
    return Response(serializer.data)

@api_view(["POST"])
def notificacionCreate(request):
    serializer=NotificacionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def notificacionUpdate(request,id):
    sponsor= Notificacion.objects.get(id=id)
    serializer=NotificacionSerializer(instance=sponsor,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["DELETE"])
def notificacionDelete(request,id):
    sponsor= Notificacion.objects.get(id=id)
    try:
        sponsor.delete()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ListarNotificacion(FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = Notificacion
    context_object_name = 'notificacion'
    template_name = "lista_notificaciones.html"
    permission_required = 'novagym.view_empleado'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Notificaciones"
        page_obj = context["page_obj"]
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

def deleteNotificacion(request,id):
    query = Notificacion.objects.get(id=id)
    if request.POST:
        query.delete()
        messages.success(request, "Notificacion eliminada con éxito.")
        return redirect('notificaciones:listar')
    return render(request, "ajax/notificacion_confirmar_elminar.html", {"notificacion": query})

class CrearNotificacion(CreateView):
    form_class =NotificacionForm
    model=Notificacion
    template_name = 'notificacion_nueva.html'
    title = "CREAR NOTIFICACION"
    success_url = reverse_lazy('notificaciones:listar')

class UpdateNotificacion(UpdateView):
    form_class =NotificacionForm
    model=Notificacion
    title = "ACTUALIZAR NOTIFICACION"
    template_name = 'notificacion_nueva.html'
    success_url = reverse_lazy('notificaciones:listar')

def ChangeState(request,pk):
    query = Notificacion.objects.get(id=pk)
    print(query.activo)
    if query.activo==0:
        query.activo=1
        messages.success(request, "Notificación habilitada.")
    elif query.activo==1:
        query.activo=0
        messages.success(request, "Notificación deshabilitada.")
    query.save()
    return redirect('notificaciones:listar')

def registrarDispositivo(id_registro,usuario):
    try:
        dispositivo = GCMDevice.objects.get(registration_id=id_registro)
        dispositivo.user = usuario
        dispositivo.save()
    except:
        dispositivo=GCMDevice.objects.create(registration_id=id_registro, cloud_message_type="FCM",user=usuario, active=True)

def enviarNotificacionGlobal(request,id_notificacion):
    notificacion=Notificacion.objects.get(id=id_notificacion)
    dispositivos=GCMDevice.objects.all()
    for dispositivo in dispositivos:
        dispositivo.send_message(notificacion.cuerpo,extra={"title" : notificacion.titulo,"image":notificacion.imagen})
    messages.success(request, "Notificación enviada a todos los usuarios.")
    return redirect('notificaciones:listar')

def enviarNotificacionIndividual(request,id_notificacion,usuario):
    notificacion=Notificacion.objects.get(id=id_notificacion)
    dispositivos=GCMDevice.objects.filter(user=usuario).send_message(notificacion.cuerpo,extra={"title" : notificacion.titulo,"image":notificacion.imagen})
    messages.success(request, "Notificación enviada al usuario "+usuario+".")
    return redirect('notificaciones:listar')