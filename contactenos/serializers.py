from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.serializers import Serializer, FileField, CharField, PrimaryKeyRelatedField

from seguridad.models import UserDetails
from .models import Buzon

class BuzonSerializer(Serializer):
    sender=PrimaryKeyRelatedField(queryset=UserDetails.objects.all())
    titulo=CharField()
    descripcion=CharField()
    imagen=FileField(required=False)
    class Meta:
        fields = ['sender','titulo','descripcion','imagen']
    def create(self, validated_data):
            return Buzon.objects.create(**validated_data)