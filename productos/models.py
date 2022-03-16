from enum import unique
from django.db import models
from django.core.validators import MinValueValidator
# Create your models here.

class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=24)
    imagen=models.ImageField(upload_to="categoriasProductos/", null=True, blank=True,default="images/no_image.png")

    def __str__(self):
        return self.nombre



class Producto(models.Model):
    class Talla(models.TextChoices):
        NA = 'NA', 'No aplica'
        EXTRA_SMALL = 'LS', 'Extra Small'
        SMALL = 'S', 'Small'
        MEDIUM = 'M', 'Medium'
        LARGE = 'L', 'Large'
        EXTRA_LARE = 'XL', 'Extra Large'
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=255,unique=True)
    nombre = models.CharField(max_length=24,unique=True)
    descripcion = models.CharField(max_length=255)
    precio_referencial = models.DecimalField(max_digits=4, decimal_places=2,validators=[MinValueValidator(0)])
    imagen=models.ImageField(upload_to="productos/", null=True, blank=True,default="images/no_image.png")
    categoria=models.ForeignKey(Categoria, on_delete=models.CASCADE)
    valor_presentacion=models.DecimalField(max_digits=4, decimal_places=2,validators=[MinValueValidator(0)])
    talla = models.CharField(max_length=3, choices=Talla.choices)
    unidad_presentacion = models.PositiveIntegerField()

    def __str__(self):
        return self.codigo + ' - ' + self.nombre

class Inventario(models.Model):
    id = models.AutoField(primary_key=True)
    producto=models.ForeignKey(Producto, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=4, decimal_places=2,default=0)
    stock = models.PositiveIntegerField()
    novacoins=models.PositiveIntegerField(default=0)
    usaNovacoins=models.BooleanField()
    def __str__(self):
        return self.nombre

class ProductoDescuento(models.Model):
    id = models.AutoField(primary_key=True)
    producto=models.ForeignKey(Producto, on_delete=models.CASCADE)
    porcentaje_descuento=models.PositiveIntegerField()
    fecha_hora_desde=models.DateTimeField()
    fecha_hora_hasta=models.DateTimeField()
    estado=models.BooleanField(default=True)
    def __str__(self):
        return str(self.producto) +"-"+str(self.porcentaje_descuento)+"-"+ self.estado



