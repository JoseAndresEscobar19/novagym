from rest_framework import serializers
from .models import *



class AlmacenamientoUsuarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = AlmacenamientoUsuario
        fields = ['usuario', 'asignado', 'usado',
                 'comprado', 'peso_archivo_asignado']


class AlmacenamientoGlobalSerializer(serializers.ModelSerializer):

    class Meta:
        model = AlmacenamientoGlobal
        fields = ['servidor', 'total_usado', 'sin_limite']