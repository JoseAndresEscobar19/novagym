from django.shortcuts import render
from django.forms import BooleanField
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.shortcuts import render
from django.urls import reverse_lazy
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django_filters.views import FilterView

from calendario.filters import CalendarioFilter
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
# Create your views here.

@api_view(["GET"])
def calendarioList(request):
    calendario= Calendario.objects.all()
    serializer=CalendarioSerializer(calendario,many=True)
    return Response(serializer.data)

@api_view(["GET"])
def calendarioDetail(request,id):
    calendario= Calendario.objects.get(id=id)
    serializer=CalendarioSerializer(calendario,many=False)
    return Response(serializer.data)

class ShowCalendario(FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = Calendario
    context_object_name = 'calendario'
    template_name = "templates/lista_calendario.html"
    permission_required = 'novagym.view_empleado'
    filterset_class=CalendarioFilter

    def get_filterset_class(self):
        return self.filterset_class

    def filtering(self, request, *args, **kwargs):
        if request.GET.get('sucursales'):
            data=request.GET.get('sucursales')
            return data

    def get_queryset(self):
        return self.model.objects.filter(gimnasio=self.filtering(self.request))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "CALENDARIO"
        gimnasios=Gimnasio.objects.all()
        context["gimnasios"]=gimnasios
        #page_obj = context["page_obj"]
        #context['num_pages'] = calculate_pages_to_render(self, page_obj)
        return context

    

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class CrearCalendario(CreateView):
    form_class =CalendarioForm
    model=Calendario
    template_name = 'templates/calendario_nuevo.html'
    title = "AGREGAR ACTIVIDAD"
    success_url = reverse_lazy('calendario:listar')

class UpdateCalendario(UpdateView):
    form_class =CalendarioForm
    model=Calendario
    title = "ACTUALIZAR ACTIVIDAD"
    template_name = 'templates/calendario_nuevo.html'
    success_url = reverse_lazy('calendario:listar')

def deleteCalendario(request,id):
    query = Calendario.objects.get(id=id)
    if request.POST:
        query.delete()
        messages.success(request, "Actividad eliminada con éxito.")
        return redirect('calendario:listar')
    return render(request, "templates/ajax/calendario_confirmar_elminar.html", {"calendario": query})

def getHorarios(request):
    urls={}
    horarios=Calendario.objects.all()
    for horario in horarios:
        if horario.gimnasio.nombre not in urls.keys():
            urls[horario.gimnasio.nombre]={
                "lunes":{},
                "martes":{},
                "miercoles":{},
                "jueves":{},
                "viernes":{},
                "sabado":{},
                "domingo":{}
                }
        urls[horario.gimnasio.nombre][str(horario.dia).lower()][horario.nombre]={
                "descripcion":horario.descripcion,
                "horaInicio":str(horario.horario_inicio),
                "horaFin":str(horario.horario_fin)
            }
    return HttpResponse(json.dumps(urls))