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
from novagym.utils import calculate_pages_to_render
from .models import *
from django.contrib import messages
import json
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView
from .filters import SponsorFilter
# Create your views here.
#SPONSOR

@api_view(["GET"])
def sponsorList(request):
    sponsors= Sponsor.objects.all()
    serializer=SponsorSerializer(sponsors,many=True)
    return Response(serializer.data)

@api_view(["GET"])
def sponsorDetail(request,id):
    sponsors= Sponsor.objects.get(id=id)
    serializer=SponsorSerializer(sponsors,many=False)
    return Response(serializer.data)

@api_view(["POST"])
def sponsorCreate(request):
    serializer=SponsorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def sponsorUpdate(request,id):
    sponsor= Sponsor.objects.get(id=id)
    serializer=SponsorSerializer(instance=sponsor,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["DELETE"])
def sponsorDelete(request,id):
    sponsor= Sponsor.objects.get(id=id)
    try:
        sponsor.delete()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def createSponsor(request):
    if request.method=='POST':
        form = SponsorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("sponsor:createSponsor")
    else:
        form=SponsorForm()
    return render(request,'createSponsor.html',{'form':form})

class ListarSponsors(FilterView):
    paginate_by = 10
    max_pages_render = 10
    model = Sponsor
    context_object_name = 'sponsor'
    template_name = "lista_sponsor.html"
    permission_required = 'novagym.view_empleado'
    filterset_class=SponsorFilter
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "ANUNCIANTES"
        page_obj = context["page_obj"]
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

@login_required()
def deleteSponsor(request,id):
    query = Sponsor.objects.get(id=id)
    if request.POST:
        query.delete()
        messages.success(request, "Anunciante eliminado con éxito.")
        return redirect('sponsor:listar')
    return render(request, "ajax/sponsor_confirmar_elminar.html", {"sponsor": query})

class CrearSponsor(CreateView):
    form_class =SponsorForm
    model=Sponsor
    template_name = 'sponsor_nuevo.html'
    title = "CREAR SPONSOR"
    success_url = reverse_lazy('sponsor:listar')

class UpdateSponsor(UpdateView):
    form_class =SponsorForm
    model=Sponsor
    title = "ACTUALIZAR SPONSOR"
    template_name = 'sponsor_nuevo.html'
    success_url = reverse_lazy('sponsor:listar')

def ChangeState(request,pk):
    query = Sponsor.objects.get(id=pk)
    print(query.activo)
    if query.activo==0:
        query.activo=1
        messages.success(request, "Anunciante "+query.nombre +" habilitado.")
    elif query.activo==1:
        query.activo=0
        messages.success(request, "Anunciante "+query.nombre +" deshabilitado.")
    query.save()
    return redirect('sponsor:listar')

def getAllSponsors(request):
    urls={}
    sponsors=Sponsor.objects.all()
    for sponsor in sponsors:
        urls[sponsor.nombre]={
                            "codigo":sponsor.codigo,
                            "descripcion":sponsor.descripcion,
                            "imagen":request.build_absolute_uri('/media/')+str(sponsor.imagen),
                            "fechaInicio":str(sponsor.fecha_inicio),
                            "fechaFin":str(sponsor.fecha_fin),
                            "url":sponsor.url,
                            "activo":sponsor.activo
                            }
    return HttpResponse(json.dumps(urls))