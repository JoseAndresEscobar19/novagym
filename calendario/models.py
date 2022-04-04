import random
from django.db import models
from seguridad.models import UserDetails
from gimnasio.models import Gimnasio

# Create your models here.

def generarCodigo():
    not_unique = True
    while not_unique:
        unique_code = random.randint(0, 999999)
        codeString=str(unique_code).zfill(6)
        if not MaquinaReserva.objects.filter(codigo=codeString):
            not_unique = False
            return codeString

def generarCodigoMaquina():
    not_unique = True
    while not_unique:
        unique_code = "MCN-"+str(random.randint(1000, 9999))
        if not MaquinaReserva.objects.filter(codigo=unique_code):
            not_unique = False
            return "MCN-"+str(unique_code)

class Horario(models.Model):
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
    gimnasio=models.ForeignKey(Gimnasio, on_delete=models.PROTECT)
    capacidad=models.PositiveIntegerField(max_length=2)
    asistentes=models.PositiveIntegerField(max_length=2,default=0)
    activo=models.BooleanField(default=True)
    class Meta:
        ordering=('horario_inicio',)
    def __str__(self):
        return self.nombre



class Maquina(models.Model):
    class Categoria(models.TextChoices):
        CORRER = 'Cintas de correr', 'Cintas de correr'
        BICICLETAS = 'Bicicletas', 'Bicicletas'
        ELIPTICAS = 'Elipticas', 'Elipticas'
        REMO = 'Remo', 'Remo'
        FUERZA = 'Fuerza', 'Fuerza'
        HERRAMIENTAS = 'Herramientas', 'Herramientas'
    codigo=codigo=models.CharField(max_length=20, unique=True, default=generarCodigoMaquina, editable=False)
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=24)
    descripcion = models.CharField(max_length=255)
    imagen=models.ImageField(upload_to="maquinas/", null=False, blank=False,default="images/no_image.png")
    categoria=models.CharField(max_length=20, choices=Categoria.choices)  
    cantidad=models.PositiveIntegerField(max_length=2)


class Zona(models.Model):
    id=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=24)
    espacios=models.PositiveIntegerField(max_length=2)


class Posicion(models.Model):
    id=models.AutoField(primary_key=True)
    fila=models.CharField(max_length=1)
    columna=models.PositiveIntegerField(max_length=2)
    maquina=models.ForeignKey(Maquina, on_delete=models.PROTECT)
    zona=models.ForeignKey(Zona, on_delete=models.PROTECT)

class MaquinaReserva(models.Model):
    id=models.AutoField(primary_key=True)
    codigo=models.CharField(max_length=20, unique=True, default=generarCodigo, editable=False)
    maquina=models.ForeignKey(Maquina,on_delete=models.PROTECT)
    horario=models.DateTimeField()
    posicion=models.ForeignKey(Posicion, on_delete=models.PROTECT)
    usuario=models.ForeignKey(UserDetails,on_delete=models.PROTECT)

class HorarioReserva(models.Model):
    id = models.AutoField(primary_key=True)
    codigo=models.CharField(max_length=20, unique=True, default=generarCodigo, editable=False)
    horario=models.ForeignKey(Horario,on_delete=models.PROTECT)
    usuario=models.ForeignKey(UserDetails,on_delete=models.PROTECT)
