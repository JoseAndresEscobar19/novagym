from django.urls import path

from .apps import MembresiaConfig
from .views import *

app_name = MembresiaConfig.name
urlpatterns = [
    path('membresias/', ListarMembresia.as_view(), name='listar'),
    path('membresias/agregar/', CrearMembresia.as_view(), name='agregar'),
    path('membresias/editar/<int:pk>/', EditarMembresia.as_view(), name='editar'),
    path('membresias/eliminar/<int:pk>/', membresia_confirmar_eliminacion,
         name='eliminar'),
    path('membresias/activar/<int:pk>/', membresia_confirmar_activar,
         name='activar'),
    path('membresias/beneficios/', ListarBeneficio.as_view(), name='listar_beneficio'),
    path('membresias/beneficios/agregar/', CrearBeneficio.as_view(), name='agregar_beneficio'),
    path('membresias/beneficios/editar/<int:pk>/', EditarBeneficio.as_view(), name='editar_beneficio'),
]
