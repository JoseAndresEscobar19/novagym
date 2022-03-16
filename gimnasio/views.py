from django.forms import BooleanField
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.shortcuts import render
from django.urls import reverse_lazy
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django_filters.views import FilterView
from backend.settings import BASE_DIR, MEDIA_ROOT, MEDIA_URL

from gimnasio.filters import GimnasioFilter
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
#Gimnasio - Contacto

@api_view(["GET"])
def gimnasioList(request):
    gimnasio= Gimnasio.objects.all()
    serializer=GimnasioSerializer(gimnasio,many=True)
    return Response(serializer.data)

@api_view(["GET"])
def gimnasioDetail(request,id):
    gimnasio= Gimnasio.objects.get(id=id)
    serializer=GimnasioSerializer(gimnasio,many=False)
    return Response(serializer.data)

@api_view(["POST"])
def gimnasioCreate(request):
    serializer=GimnasioSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def gimnasioUpdate(request,id):
    gimnasio= Gimnasio.objects.get(id=id)
    serializer=GimnasioSerializer(instance=gimnasio,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["DELETE"])
def gimnasioDelete(request,id):
    gimnasio= Gimnasio.objects.get(id=id)
    try:
        gimnasio.delete()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ListarGimnasio(FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = Gimnasio
    context_object_name = 'gimnasio'
    template_name = "lista_gimnasio.html"
    permission_required = 'novagym.view_empleado'
    filterset_class=GimnasioFilter
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "GIMNASIOS"
        page_obj = context["page_obj"]
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class CrearGimnasio(CreateView):
    form_class =GimnasioForm
    model=Gimnasio
    template_name = 'gimnasio_nuevo.html'
    title = "CREAR SPONSOR"
    success_url = reverse_lazy('gimnasio:listar')

class UpdateGimnasio(UpdateView):
    form_class =GimnasioForm
    model=Gimnasio
    title = "ACTUALIZAR GIMNASIO"
    template_name = 'gimnasio_nuevo.html'
    success_url = reverse_lazy('gimnasio:listar')

def deleteGimnasio(request,id):
    query = Gimnasio.objects.get(id=id)
    if request.POST:
        query.delete()
        messages.success(request, "Gimnasio eliminado con éxito.")
        return redirect('gimnasio:listar')
    return render(request, "ajax/gimnasio_confirmar_elminar.html", {"gimnasio": query})

def changeState(request,pk):
    gimnasio=Gimnasio.objects.get(id=pk)
    if gimnasio.estado:
        gimnasio.estado=False
    else:
        gimnasio.estado=True
    gimnasio.save()
    return redirect('gimnasio:listar')

def changeAforo(request):
    gimnasios=Gimnasio.objects.all()
    aforoGlobal = request.GET.get('aforo')
    if aforoGlobal:
        for gimnasio in gimnasios:
            gimnasio.aforo=aforoGlobal
            gimnasio.save()
    return redirect('gimnasio:listar')

def getGimnasios(request):
    urls={}
    gimnasios=Gimnasio.objects.all()
    for gimnasio in gimnasios:
        urls[gimnasio.nombre]={
                            "imagen":request.build_absolute_uri('/media/')+str(gimnasio.imagen),
                            "horaApertura":str(gimnasio.horario_inicio),
                            "horaCierre":str(gimnasio.horario_fin),
                            "telefono":gimnasio.telefono,
                            "ubicacion":gimnasio.ubicacion,
                            "activo":gimnasio.estado,
                            "ciudad":gimnasio.ciudad,
                            "aforo":gimnasio.aforo,
                            "coordenadas":[float(gimnasio.latitud),float(gimnasio.longitud)]
                            }
    return HttpResponse(json.dumps(urls))