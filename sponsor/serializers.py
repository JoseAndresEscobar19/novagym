from django.contrib.auth.models import User
from .models import *
from rest_framework import serializers


class SponsorSerializer(serializers.ModelSerializer):
    nombre=serializers.CharField(max_length=24)
    descripcion = serializers.CharField(max_length=255)
    telefono = serializers.CharField(max_length=12)
    nombre_contacto = serializers.CharField(max_length=24)
    url = serializers.CharField(max_length=255)
    imagen = serializers.CharField(max_length=255)
    class Meta:
        model = Sponsor
        fields = ('id', 'nombre', 'descripcion', 'telefono', 'nombre_contacto', 'url','imagen')