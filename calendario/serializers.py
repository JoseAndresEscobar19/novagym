from django.contrib.auth.models import User
from .models import Calendario
from rest_framework import serializers

class CalendarioSerializer(serializers.ModelSerializer):
    dia = serializers.CharField(max_length=10)
    nombre = serializers.CharField(max_length=24)
    descripcion = serializers.CharField(max_length=255)
    horario_inicio = serializers.TimeField()
    horario_fin = serializers.TimeField()

    class Meta:
        model = Calendario
        fields = ('id','dia','nombre', 'descripcion','horario_inicio', 'horario_fin','gimnasio')