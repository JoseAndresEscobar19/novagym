from django.db import models

from seguridad.models import UserDetails

# Create your models here.


class Beneficio(models.Model):
    nombre = models.CharField(max_length=255)
    texto = models.TextField()

    def __str__(self):
        return self.nombre


class Membresia(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    meses_duracion = models.IntegerField()
    beneficios = models.ManyToManyField(Beneficio, related_name='membresia')
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre


class Descuento(models.Model):
    membresia = models.ForeignKey(
        Membresia, on_delete=models.SET_NULL, null=True)
    porcentaje_descuento = models.PositiveIntegerField()
    fecha_hora_desde = models.DateTimeField()
    fecha_hora_hasta = models.DateTimeField()
    activo = models.BooleanField(default=False)
    
    def __str__(self):
        return self.membresia.nombre + ' - %' + str(self.porcentaje_descuento)


class Historial(models.Model):
    usuario = models.ForeignKey(
        UserDetails, on_delete=models.SET_NULL, null=True, related_name='historial_membresia')
    membresia = models.ForeignKey(
        Membresia, on_delete=models.SET_NULL, null=True)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    costo = models.DecimalField(max_digits=12, decimal_places=2)
    activa = models.BooleanField(default=False)
    
    def __str__(self):
        return self.usuario.nombres + ' - ' + self.membresia.nombre