from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from django_filters.views import FilterView
from novagym.utils import calculate_pages_to_render
from rest_framework import status
from seguridad.views import UsuarioPermissionRequieredMixin

from membresia.filters import MembresiaFilter
from membresia.forms import BeneficioForm, MembresiaForm
from membresia.models import Beneficio, Membresia

# Create your views here.


class ListarMembresia(LoginRequiredMixin, UsuarioPermissionRequieredMixin, FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = Membresia
    context_object_name = 'usuarios'
    template_name = "lista_membresia.html"
    permission_required = 'seguridad.view_userdetails'
    filterset_class = MembresiaFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Membresías"
        page_obj = context["page_obj"]
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        return context


class CrearMembresia(LoginRequiredMixin, UsuarioPermissionRequieredMixin, CreateView):
    model = Membresia
    form_class = MembresiaForm
    template_name = 'crear_membresia.html'
    success_url = reverse_lazy('membresia:listar')
    permission_required = 'seguridad.add_userdetails'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Agregar Membresía"
        return context


class EditarMembresia(LoginRequiredMixin, UsuarioPermissionRequieredMixin, UpdateView):
    model = Membresia
    form_class = MembresiaForm
    template_name = 'crear_membresia.html'
    success_url = reverse_lazy('membresia:listar')
    permission_required = 'seguridad.add_userdetails'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Editar Membresía"
        return context


@login_required
@permission_required('seguridad.delete_userdetails')
def membresia_confirmar_eliminacion(request, pk):
    membresia = Membresia.objects.get(id=pk)
    if request.POST:
        membresia.estado = False
        membresia.save()
        messages.info(request, "Membresía deshabilitada con éxito.")
        return redirect(reverse_lazy('membresia:listar'))
    return render(request, 'ajax/membresia_confirmar_elminar.html', {'membresia': membresia})


@login_required
@permission_required('seguridad.delete_userdetails')
def membresia_confirmar_activar(request, pk):
    membresia = Membresia.objects.get(id=pk)
    if request.POST:
        membresia.estado = True
        membresia.save()
        messages.success(request, "Membresía habilitada con éxito.")
        return redirect(reverse_lazy('membresia:listar'))
    return render(request, 'ajax/membresia_confirmar_activar.html', {'membresia': membresia})


class ListarBeneficio(LoginRequiredMixin, UsuarioPermissionRequieredMixin, ListView):
    model = Beneficio
    context_object_name = 'usuarios'
    template_name = "lista_beneficio.html"
    permission_required = 'seguridad.view_userdetails'
    filterset_class = MembresiaFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Beneficios"
        return context


class CrearBeneficio(LoginRequiredMixin, UsuarioPermissionRequieredMixin, CreateView):
    model = Beneficio
    form_class = BeneficioForm
    template_name = 'crear_beneficio.html'
    success_url = reverse_lazy('membresia:listar_beneficio')
    permission_required = 'seguridad.add_userdetails'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Agregar beneficio"
        context['url'] = reverse_lazy('membresia:agregar_beneficio')
        return context


class EditarBeneficio(LoginRequiredMixin, UsuarioPermissionRequieredMixin, UpdateView):
    model = Beneficio
    form_class = BeneficioForm
    template_name = 'crear_beneficio.html'
    success_url = reverse_lazy('membresia:listar_beneficio')
    permission_required = 'seguridad.add_userdetails'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Editar beneficio"
        context['url'] = reverse_lazy('membresia:editar_beneficio', kwargs={
                                      'pk': self.get_object().pk})
        return context
