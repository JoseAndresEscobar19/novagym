from django.contrib.auth.models import User
from .models import *
from rest_framework import serializers



class NotificacionSerializer(serializers.ModelSerializer):
    titulo = serializers.CharField(max_length=24)
    cuerpo = serializers.CharField(max_length=255)
    imagen = serializers.FileField(required=False)
    created_at = serializers.DateTimeField()
    class Meta:
        model = Notificacion
        fields = ('id', 'titulo', 'cuerpo', 'imagen', 'created_at')

class NotificacionUsuarioSerializer(serializers.ModelSerializer):
    sender_id = serializers.IntegerField()
    receiver_id = serializers.IntegerField()
    class Meta:
        model = NotificacionUsuario
        fields = ('id','sender_id', 'receiver_id')