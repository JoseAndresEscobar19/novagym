import json
from django.shortcuts import render
from django.shortcuts import render, redirect
from django_filters.views import FilterView
from contactenos.models import Buzon
from contactenos.filters import BuzonFilter
from novagym.utils import calculate_pages_to_render
from .forms import *
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from backend.settings import env
from django.contrib import messages
from seguridad.models import UserDetails
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .serializers import BuzonSerializer
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
# Create your views here.


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Dudas y sugerencias"
            body = {
            'nombre': form.cleaned_data['nombre'],
            'apellido': form.cleaned_data['apellido'],
            'email': form.cleaned_data['email'],
            'mensaje': form.cleaned_data['mensaje'],
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject, message, 'admin@example.com',
                          ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect("seguridad:login_admin")

    form = ContactForm()
    return render(request, "contacto.html", {'form': form})


@api_view(['POST'])
def sendEmail(request):
    if request.method == 'POST':
        data = request.data
        titulo=data["titulo"]
        mensaje=data["mensaje"]
        imagen=data["imagen"]
        id=data["id"]
        email=data["email"]
        details=UserDetails.objects.get(id=int(id))
        buzon_data = Buzon.objects.create(sender_id=details,titulo=titulo,descripcion=mensaje,imagen=imagen)
        try:
            send_mail(titulo, mensaje, env("E_MAIL"),env("E_MAIL"), fail_silently = False)
            return Response(status=status.HTTP_200_OK)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        except:
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
        

class SendMail(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        file_serializer = BuzonSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ShowBuzon(FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = Buzon
    exclude = ['imagen']
    context_object_name = 'mail'
    template_name = "buzon.html"
    permission_required = 'seguridad.view_userdetails'
    filterset_class = BuzonFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "BUZÓN"
        page_obj = context["page_obj"]
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ShowBuzonNoLeidos(FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = Buzon
    exclude = ['imagen']
    context_object_name = 'mail'
    template_name = "buzonFilter.html"
    permission_required = 'seguridad.view_userdetails'
    filterset_class = BuzonFilter
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "BUZÓN"
        page_obj = context["page_obj"]
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        context['theMail'] = Buzon.objects.filter(leido=0)
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ShowBuzonLeidos(FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = Buzon
    exclude = ['imagen']
    context_object_name = 'mail'
    template_name = "buzonFilter.html"
    permission_required = 'seguridad.view_userdetails'
    filterset_class = BuzonFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "BUZÓN"
        
        page_obj = context["page_obj"]
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        context['theMail'] = Buzon.objects.filter(leido=1)
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

def deleteMail(request,id):
    query = Buzon.objects.get(id=id)
    if request.POST:
        query.delete()
        messages.success(request, "Correo eliminado con éxito.")
        return redirect('contactenos:buzon')
    return render(request, "ajax/mail_confirmar_elminar.html", {"mail": query})

def readMail(request,id):
    query = Buzon.objects.get(id=id)
    markAsRead(request,id)
    return render(request, "ajax/mail_leer.html", {"mail": query})

def markAsRead(request,id):
    mail=Buzon.objects.get(id=id)
    mail.leido=True
    mail.save()
    return redirect('contactenos:buzon')