from rest_framework import routers
from .viewsets import *

almacenamiento = routers.DefaultRouter()

almacenamiento.register(r'almacenamientoUsuario', AlmacenamientoUsuarioView, 'almacenamientoUsuario')
almacenamiento.register(r'almacenamientoGlobal', AlmacenamientoGlobalView, 'almacenamientoGlobal')

almacenamiento_api = almacenamiento.urls