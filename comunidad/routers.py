from rest_framework import routers
from .viewsets import *

comunidad = routers.DefaultRouter()

comunidad.register(r'biografia', BiografiaView, 'biografia')
comunidad.register(r'publicacion', PublicacionView, 'publicacion')
comunidad.register(r'publicacionUsuario', PublicacionUsuarioView, 'publicacionUsuario')
comunidad.register(r'reportarPublicacion', ReportarPublicacionView, 'reportarPublicacion')
comunidad.register(r'publicacionLike', LikeView, 'publicacionLike')
comunidad.register(r'comentario', ComentarioView, 'comentario')
comunidad.register(r'seguidor', SeguidorView, 'seguidor')
comunidad.register(r'recomendacionAmigo', RecomendacionAmigoView, 'recomendacionAmigo')
comunidad.register(r'historia', HistoriaView, 'historia')

comunidad_api = comunidad.urls