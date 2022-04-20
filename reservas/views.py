import datetime
from django.shortcuts import render
from django.urls import reverse_lazy
from calendario.filters import MaquinaFilter
from calendario.forms import MaquinaForm
from calendario.models import Maquina,MaquinaReserva,PosicionMaquina,Horario,HorarioReserva,Posicion
from django_filters.views import FilterView
from novagym.utils import calculate_pages_to_render
from django.views.generic import CreateView, UpdateView
# Create your views here.

class ListarMaquinas(FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = Maquina
    context_object_name = 'maquina'
    template_name = "templates/lista_maquina.html"
    permission_required = 'novagym.view_empleado'
    filterset_class=MaquinaFilter
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "MÁQUINAS"
        page_obj = context["page_obj"]
        context['type'] = "m"
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class CrearMaquina(CreateView):
    form_class =MaquinaForm
    model=Maquina
    template_name = 'templates/calendario_nuevo.html'
    success_url = reverse_lazy('reservas:listarMaquina')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "CREAR MÁQUINA"
        return context

class UpdateMaquina(UpdateView):
    form_class =MaquinaForm
    model=Maquina
    title = "ACTUALIZAR MÁQUINA"
    template_name = 'templates/calendario_nuevo.html'
    success_url = reverse_lazy('reservas:listarMaquina')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Editar Máquina"
        return context

class ListarReservasMaquinas(FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = MaquinaReserva
    context_object_name = 'maquinaReserva'
    template_name = "templates/lista_maquinaReserva.html"
    permission_required = 'novagym.view_empleado'
    #filterset_class=MaquinaFilter
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "RESERVAS DE MÁQUINAS"
        page_obj = context["page_obj"]
        context['type'] = "m"
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ListarReservasHorarios(FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = HorarioReserva
    context_object_name = 'horarioReserva'
    template_name = "templates/lista_horarioReserva.html"
    permission_required = 'novagym.view_empleado'
    #filterset_class=MaquinaFilter
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "RESERVAS DE CLASES"
        page_obj = context["page_obj"]
        context['type'] = "c"
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)