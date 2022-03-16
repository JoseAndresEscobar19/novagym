from django.db import models

from gimnasio.models import Gimnasio

# Create your models here.

class Calendario(models.Model):
    id = models.AutoField(primary_key=True)
    class Dia(models.TextChoices):
        LUNES = 'LUNES', 'LUNES'
        MARTES = 'MARTES', 'MARTES'
        MIERCOLES = 'MIERCOLES', 'MIERCOLES'
        JUEVES = 'JUEVES', 'JUEVES'
        VIERNES = 'VIERNES', 'VIERNES'
        SABADO = 'SABADO', 'SABADO'
        DOMINGO = 'DOMINGO', 'DOMINGO'
    dia=models.CharField(max_length=10, choices=Dia.choices)
    nombre = models.CharField(max_length=24)
    descripcion = models.CharField(max_length=255)
    horario_inicio = models.TimeField(blank=False)
    horario_fin = models.TimeField(blank=False)
    gimnasio=models.ForeignKey(Gimnasio, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre