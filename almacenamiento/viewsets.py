from rest_framework.response import Response
from rest_framework import status, viewsets, permissions

from .serializers import *

class AlmacenamientoUsuarioView(viewsets.ViewSet):
    serializer_class = AlmacenamientoUsuarioSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request):
        almacenamiento_usuario = AlmacenamientoUsuario.objects.get(usuario=request.user)
        serializer = AlmacenamientoUsuarioSerializer(almacenamiento_usuario)
        return Response(serializer.data)


class AlmacenamientoGlobalView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request):
        almacenamiento_global = AlmacenamientoGlobal.objects.get(pk=1)
        serializer = AlmacenamientoGlobalSerializer(almacenamiento_global)
        return Response(serializer.data)