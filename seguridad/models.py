from django.contrib.auth.models import Group, User
from django.db import models

# Create your models here.


class UserDetails(models.Model):
    class Meta:
        ordering = ['-id']

    class Sex(models.TextChoices):
        MAN = 'H', 'Hombre'
        WOMEN = 'M', 'Mujer'
        NON = 'N', 'No especificar'

    class Tipo(models.TextChoices):
        CLI = 'C', 'Cliente'
        EMP = 'E', 'Empleado'

    usuario = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="detalles")
    codigo = models.CharField(max_length=255, blank=True)
    cedula = models.CharField(max_length=13)
    nombres = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    imagen = models.ImageField(upload_to='usuario/', null=True, blank=True)
    telefono = models.CharField(max_length=12)
    sexo = models.CharField(max_length=2, choices=Sex.choices)
    tipo = models.CharField(max_length=2, choices=Tipo.choices, default='E')
    fecha_nacimiento = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cedula + ' - ' + self.apellidos + ' - ' + self.tipo
