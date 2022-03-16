from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from calendario.views import *
from .apps import CalendarioConfig

app_name = CalendarioConfig.name


urlpatterns = [
    path('listar',ShowCalendario.as_view(),name="listar"),
    path('crear/',CrearCalendario.as_view(),name="crear"),
    path('editar/<int:pk>',UpdateCalendario.as_view(),name="editar"),
    path('eliminar/<int:id>',deleteCalendario,name="eliminar"),
    path('getHorarios/',getHorarios,name="getHorarios"),
]