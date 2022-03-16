from dataclasses import fields
from rest_framework import serializers
from decimal import Decimal
from almacenamiento.models import *
from .models import *


class BiografiaSerializer(serializers.ModelSerializer):
    usuario_info = serializers.ReadOnlyField()

    class Meta:
        model = Biografia
        fields = ['id', 'usuario', 'foto_perfil', 'foto_portada',
                 'descripcion', 'seguidores', 'usuario_info']


class ArchivoPublicacionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArchivoPublicacion
        fields = ('id', 'archivo', 'tipo', 'almacenamiento_utilizado')
        

class PublicacionSerializer(serializers.ModelSerializer):
    usuario_info = serializers.ReadOnlyField()
    comentarios = serializers.ReadOnlyField()
    archivos = ArchivoPublicacionSerializer(many=True)

    class Meta:
        model = Publicacion
        fields = ['id', 'usuario', 'usuario_info', 'texto', 
                'fecha_creacion', 'num_likes', 'archivos', 'comentarios']

    def create(self, validated_data):
        archivos = validated_data.pop('archivos')
        publicacion = Publicacion.objects.create(**validated_data)
        for archivo in archivos:
            archivo_publicacion = ArchivoPublicacion.objects.create(publicacion=publicacion, **archivo)
            archivo_publicacion.aumentar_almacenamiento(publicacion.usuario)

        return publicacion
    
    def update(self, instance, validated_data):
        archivos = validated_data.pop('archivos')
        if 'texto' in validated_data:
            instance.texto = validated_data.get('texto', instance.texto)
        instance.save()
        for archivo in archivos:
            archivo_publicacion = ArchivoPublicacion.objects.create(publicacion=instance, **archivo)
            archivo_publicacion.aumentar_almacenamiento(instance.usuario)
        return instance


class ComentarioSerializer(serializers.ModelSerializer):
    usuario_info = serializers.ReadOnlyField()
    comentarios_hijo = serializers.ReadOnlyField()
    es_padre = serializers.ReadOnlyField()
    nivel_comentario = serializers.ReadOnlyField()

    class Meta:
        model = Comentario
        fields = ['id', 'texto', 'publicacion', 'usuario', 
                'usuario_info', 'fecha_creacion', 'imagen',
                'almacenamiento_utilizado', 'nivel_comentario', 
                'comentario_padre', 'es_padre', 'comentarios_hijo']
    
    def create(self, validated_data):
        comentario = Comentario.objects.create(**validated_data)
        if comentario.imagen:
            comentario.aumentar_almacenamiento()
        return comentario
    
    def update(self, instance, validated_data):
        if 'texto' in validated_data:
            instance.texto = validated_data.get('texto', instance.texto)
        if 'imagen' in validated_data:
            instance.imagen = validated_data.get('imagen', instance.imagen)
            instance.almacenamiento_utilizado = validated_data.get('almacenamiento_utilizado', instance.almacenamiento_utilizado)
            instance.aumentar_almacenamiento()
        instance.save()
        return instance


class SeguidorSerializer(serializers.ModelSerializer):
    seguidor_info = serializers.ReadOnlyField()
    siguiendo = serializers.ReadOnlyField()

    class Meta:
        model = Seguidor
        fields = ['usuario', 'seguidor', 'seguidor_info', 'siguiendo']
        extra_kwargs = {"usuario": {"write_only": True, 'required': True}}

    def create(self, validated_data):
        seguidor = Seguidor.objects.create(**validated_data)
        return seguidor

class SeguidosSerializer(serializers.ModelSerializer):
    seguidos_info = serializers.ReadOnlyField()

    class Meta:
        model = Seguidor
        fields = ['usuario', 'seguidos_info']


class HistoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historia
        fields = ['id', 'usuario', 'texto', 'fecha_creacion', 
                'archivo', 'tipo_archivo', 'almacenamiento_utilizado']
        extra_kwargs = {"usuario": {"write_only": True, 'required': True}}

    def create(self, validated_data):
        historia = Historia.objects.create(**validated_data)
        if historia.archivo:
            historia.aumentar_almacenamiento()
        return historia