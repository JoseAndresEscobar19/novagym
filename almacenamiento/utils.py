from decimal import Decimal
from .models import *

def tamanio_archivos(archivos):
   tamanio = 0
   for archivo in archivos:
      tamanio += archivo['almacenamiento_utilizado']
   return tamanio

def almacenamiento_disponible_user(user, archivos):
   almacenamiento_global = AlmacenamientoGlobal.objects.get(id=1)
   if almacenamiento_global.sin_limite:
      return True

   almacenamiento = AlmacenamientoUsuario.objects.get(usuario=user)
   tamanio = tamanio_archivos(archivos)   
   if (Decimal(tamanio) + almacenamiento.usado) > (almacenamiento.asignado + almacenamiento.comprado):
      return False
   return True

def almacenamiento_disponible_servidor(archivos):
   almacenamiento = AlmacenamientoGlobal.objects.get(id=1)
   if almacenamiento.sin_limite:
      return True
   tamanio = tamanio_archivos(archivos)
   almacenamiento_actual = Decimal(tamanio) + almacenamiento.total_usado
   if almacenamiento_actual > almacenamiento.servidor:
      return False
   elif Decimal(tamanio) > almacenamiento.capacidad_max:
      return False
   return True

def peso_archivo_permitido(user, peso_archivo):
   almacenamiento = AlmacenamientoUsuario.objects.get(usuario=user)
   if Decimal(peso_archivo) > almacenamiento.peso_archivo_asignado:
      return False
   return True


   
