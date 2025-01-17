from django.contrib.auth.models import User
from .models import *
from rest_framework import serializers




class InventarioSerializer(serializers.ModelSerializer):
    precio = serializers.DecimalField(max_digits=4, decimal_places=2)
    stock = serializers.IntegerField()
    producto_id=serializers.IntegerField()
    class Meta:
        model = Inventario
        fields = ('id','precio','producto_id', 'stock')

class CategoriaSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(max_length=24)
    imagen = serializers.FileField(required=False)
    class Meta:
        model = Categoria
        fields = ('id','nombre','imagen')

class ProductoSerializer(serializers.ModelSerializer):
    codigo = serializers.CharField(max_length=255)
    nombre = serializers.CharField(max_length=24)
    descripcion = serializers.CharField(max_length=255)
    imagen = serializers.FileField(required=True)
    categoria_id=serializers.IntegerField()
    talla = serializers.CharField(max_length=3)
    usaNovacoins=serializers.BooleanField()
    class Meta:
        model = Producto
        fields = ('id','codigo','nombre', 'descripcion','precio_referencial','imagen','categoria_id', 'valor_presentacion','talla','unidad_presentacion','usaNovacoins','envio')



class ProductoDescuentoSerializer(serializers.ModelSerializer):
    porcentaje_descuento=serializers.DecimalField(max_digits=3,decimal_places=2)
    fecha_hora_desde=serializers.DateTimeField()
    fecha_hora_hasta=serializers.DateTimeField()
    estado=serializers.CharField()
    producto_id=serializers.IntegerField()
    class Meta:
        model = ProductoDescuento
        fields = ('id','porcentaje_descuento','producto_id','fecha_hora_desde','fecha_hora_hasta','estado')