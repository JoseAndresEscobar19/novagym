from .models import AlmacenamientoUsuario, AlmacenamientoGlobal
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created:
        almacenamiento = AlmacenamientoGlobal.objects.get(id=1)
        AlmacenamientoUsuario.objects.create(usuario=instance, asignado=almacenamiento.capacidad_max)