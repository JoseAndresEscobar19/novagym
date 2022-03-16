from django.db import models
from datetime import date

# Create your models here.

class Sponsor(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=10)
    nombre = models.CharField(max_length=24)
    descripcion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=12)
    nombre_contacto = models.CharField(max_length=24)
    url = models.CharField(max_length=255)
    imagen = models.ImageField(upload_to="anunciantes/", null=True, blank=True,default="images/no_image.png")
    fecha_inicio=models.DateField()
    fecha_fin=models.DateField()
    activo=models.BooleanField(default=True)
    def __str__(self):
        return str(self.sender_id) +"-"+ str(self.receiver_id)

    @property
    def compararFechas(self):
        if ((self.fecha_inicio <= date.today() <= self.fecha_fin) and (self.fecha_inicio <= self.fecha_fin)) or date.today() < self.fecha_fin:
            return True
        else:
            return False

"""     @property
    def isActive(self):
        if date.today() > self.fecha_fin:
            self._activo=True
            return True
        else:
            self._activo=False
            return False """