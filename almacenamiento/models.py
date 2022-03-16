from django.contrib.auth.models import User
from django.db import models

from seguridad.models import UserDetails


class AlmacenamientoUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    asignado = models.DecimalField(max_digits=10, decimal_places=2 ,default=0)
    usado = models.DecimalField(max_digits=10, decimal_places=2 ,default=0)
    comprado = models.DecimalField(max_digits=10, decimal_places=2 ,default=0)
    peso_archivo_asignado = models.DecimalField(max_digits=10, decimal_places=2 ,default=0)
    es_excepcion = models.BooleanField(default=False)

    @property
    def usuario_detalle(self):
        detalle = UserDetails.objects.get(usuario=self.usuario)
        return f'{detalle.nombres} {detalle.apellidos}'

    @property
    def usuario_info(self):
        detalle = UserDetails.objects.get(usuario=self.usuario)
        return {
            "nombres": f'{detalle.nombres} {detalle.apellidos}',
            "cedula": detalle.cedula,
            'foto_perfil': detalle.imagen,
            'codigo': detalle.codigo
        }


class AlmacenamientoGlobal(models.Model):
    servidor = models.DecimalField(max_digits=10, decimal_places=2 ,default=0)
    capacidad_max = models.DecimalField(max_digits=10, decimal_places=2 ,default=0)#lo max que puede tener un usuario de almacenamiento
    peso_archivo_max = models.DecimalField(max_digits=10, decimal_places=2 ,default=0)
    total_usado = models.DecimalField(max_digits=10, decimal_places=2 ,default=0)
    sin_limite = models.BooleanField(default=True)

