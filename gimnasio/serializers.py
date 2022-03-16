from django.contrib.auth.models import User
from .models import *
from rest_framework import serializers
class GimnasioSerializer(serializers.ModelSerializer):
    tipo = serializers.CharField(max_length=24)
    nombre = serializers.CharField(max_length=24)
    imagen = serializers.FileField(required=False)
    telefono = serializers.CharField(max_length=24)
    ubicacion = serializers.CharField(max_length=24)
    horario_inicio = serializers.TimeField()
    horario_fin = serializers.TimeField()
    estado = serializers.CharField(max_length=24)
    ciudad = serializers.CharField(max_length=24)
    class Meta:
        model = Gimnasio
        fields = ('id','tipo','nombre', 'imagen','telefono','ubicacion','horario_inicio', 'horario_fin','estado','ciudad')