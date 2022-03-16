from django.urls import path
from .views import *
from .apps import ComunidadConfig

app_name = ComunidadConfig.name

urlpatterns = [
     path('publicacion_reportada/', ListaPublicacionReportada.as_view(), name='publicacion_reportada'),
     path('aceptar-publicacion/<int:pk>/', aceptar_publicacion, name='aceptar-publicacion'),
     path('bloquear-publicacion/<int:pk>/', bloquear_publicacion, name='bloquear-publicacion'),

     path('publicacion_novagym/', ListaPublicacionNovagym.as_view(), name='publicacion_novagym'),
     path('crear-publicacion/', CrearPublicacion.as_view(), name='crear-publicacion'),
     path('editar-publicacion/<int:pk>/', EditarPublicacion.as_view(), name='editar-publicacion'),
     path('eliminar-publicacion/<int:pk>/', eliminar_publicacion, name='eliminar-publicacion'),
]
