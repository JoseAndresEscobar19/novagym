from decimal import Decimal
from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from django_filters.views import FilterView
from django.conf import settings
from django.core.files.base import File
from almacenamiento.models import AlmacenamientoUsuario

from novagym.utils import calculate_pages_to_render
from comunidad.utils import enum_media

from .models import ArchivoPublicacion, Publicacion
from .forms import PublicacionForm, ArchivoFormSet

import os


class ListaPublicacionNovagym(FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = Publicacion
    queryset = Publicacion.objects.filter(usuario__is_superuser=1).order_by('-fecha_creacion')
    context_object_name = 'publicacion_novagym'
    template_name = "lista_publicacion.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipo'] = "novagym"
        page_obj = context["page_obj"]
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CrearPublicacion(CreateView):
    form_class = PublicacionForm
    template_name = 'nueva_publicacion.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['crear'] = True
        if self.request.POST:
            data['archivos'] = ArchivoFormSet(self.request.POST, self.request.FILES)
        else:
            data['archivos'] = ArchivoFormSet()
            data['peso_archivo_asignado'] = AlmacenamientoUsuario.objects.get(usuario=self.request.user).peso_archivo_asignado
        return data
    
    def form_valid(self, form):
        context = self.get_context_data()
        archivos = self.request.FILES.getlist('archivos-0-archivo')
        formset = context['archivos']
        if form.is_valid() and formset.is_valid():
            form.instance.usuario = self.request.user
            self.object = form.save()
            for file in archivos:
                tamanio = round(file.size/1000, 2)
                tipo = file.content_type.split("/")
                if tipo[0] not in enum_media:
                    messages.error(self.request, "Error al subir los archivos. Solo se puede subir imagenes, videos o audios.")
                    return redirect('comunidad:publicacion_novagym')
                archivo = ArchivoPublicacion.objects.create(publicacion=self.object, archivo=file,
                    tipo=enum_media[tipo[0]], almacenamiento_utilizado=Decimal(str(tamanio))) 
                archivo.aumentar_almacenamiento(self.request.user)
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("comunidad:publicacion_novagym")


class EditarPublicacion(UpdateView):
    model = Publicacion
    form_class = PublicacionForm
    template_name = 'nueva_publicacion.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['editar'] = True
        data['publicacion'] = self.object.pk
        if self.request.POST:
            data['archivos'] = ArchivoFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['archivos'] = ArchivoFormSet()
            data['peso_archivo_asignado'] = AlmacenamientoUsuario.objects.get(usuario=self.request.user).peso_archivo_asignado
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        
        archivos = ArchivoPublicacion.objects.filter(publicacion=context['publicacion'])
        for archivo in archivos:
            archivo.reducir_almacenamiento(self.request.user)
            archivo.delete()

        nuevos_archivos = self.request.FILES.getlist('archivos-0-archivo')
        if form.is_valid():
            form.instance.usuario = self.request.user
            self.object = form.save()
            for file in nuevos_archivos:
                tamanio = round(file.size/1000, 2)
                tipo = file.content_type.split("/")
                if tipo[0] not in enum_media:
                    messages.error(self.request, "Error al subir los archivos. Solo se puede subir imagenes, videos o audios.")
                    return redirect('comunidad:publicacion_novagym')
                archivo = ArchivoPublicacion.objects.create(publicacion=self.object, archivo=file,
                    tipo=enum_media[tipo[0]], almacenamiento_utilizado=Decimal(str(tamanio))) 
                archivo.aumentar_almacenamiento(self.request.user)
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("comunidad:publicacion_novagym")


def eliminar_publicacion(request, pk):
    if request.POST:
        try:
            publicacion = Publicacion.objects.get(pk=pk)
            archivos = ArchivoPublicacion.objects.filter(publicacion=publicacion)
            for archivo in archivos:
                archivo.reducir_almacenamiento(publicacion.usuario)
                archivo.delete()
            publicacion.delete()
            messages.success(request, "La publicación ha sido eliminada.")
        except:
            messages.error(request, "No se ha encontrado la publicación.")
        return redirect('comunidad:publicacion_novagym')
    return render(request, 'ajax/eliminar_publicacion.html', {'publicacion': pk})



class ListaPublicacionReportada(FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = Publicacion
    queryset = Publicacion.objects.filter(visible=False).all()
    context_object_name = 'publicacion_reportada'
    template_name = "lista_publicacion.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Publicaciones Reportadas"
        context['tipo'] = "reporte"
        page_obj = context["page_obj"]
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


def aceptar_publicacion(request, pk):
    if request.POST:
        try:
            publicacion = Publicacion.objects.get(pk=pk)
            publicacion.visible = True
            publicacion.motivo = ""
            publicacion.save()
            messages.success(request, 'Operacion realizada con exito.')
        except Publicacion.DoesNotExist:
            messages.error(request, "No se ha encontrado la publicación.")
        return redirect('comunidad:publicacion_reportada')
    return render(request, 'ajax/aceptar_publicacion.html', {'publicacion': pk})

def bloquear_publicacion(request, pk):
    if request.POST:
        try:
            publicacion = Publicacion.objects.get(pk=pk)
            publicacion.visible = True
            publicacion.texto = ""
            publicacion.motivo = ""

            archivos = ArchivoPublicacion.objects.filter(publicacion=publicacion)
            for archivo in archivos:
                archivo.reducir_almacenamiento(publicacion.usuario)
                archivo.delete()

            archivo = ArchivoPublicacion()
            ruta = f'{settings.MEDIA_ROOT}/publicacion/publicacion_reportada.jpg'
            with open(ruta, 'rb') as f:
                file = File(f)
                archivo.publicacion = publicacion
                archivo.tipo = "IMG"
                archivo.almacenamiento_utilizado = Decimal(str(round(os.path.getsize(ruta) * 0.001, 2)))
                archivo.archivo.save(f'reportado_{publicacion.id}_{publicacion.usuario.id}.jpg', file)
                archivo.save()
                archivo.aumentar_almacenamiento(publicacion.usuario)

            publicacion.save()
            messages.success(request, 'Operacion realizada con exito.')
        except Publicacion.DoesNotExist:
            messages.error(request, "No se ha encontrado la publicación.")
        return redirect('comunidad:publicacion_reportada')
    return render(request, 'ajax/bloquear_publicacion.html', {'publicacion': pk})