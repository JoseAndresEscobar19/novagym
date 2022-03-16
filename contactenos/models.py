from django.db import models
from seguridad.models import UserDetails
# Create your models here.

class Buzon(models.Model):
    id=models.AutoField(primary_key=True)
    sender=models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    titulo=models.CharField(max_length=255)
    descripcion=models.CharField(max_length=255)
    fecha=models.DateTimeField(auto_now_add=True)
    imagen=models.ImageField(upload_to="mail/", null=True, blank=True)
    leido=models.BooleanField(default=False)
    def __str__(self):
        return self.titulo