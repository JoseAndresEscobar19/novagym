from django.contrib.auth.models import User
from django.db import models

from almacenamiento.models import AlmacenamientoGlobal, AlmacenamientoUsuario
from seguridad.models import UserDetails


import os

def usuario_detalle(usuario):
    detalle = UserDetails.objects.get(usuario=usuario)
    data = { "nombre": detalle.nombres, "apellido": detalle.apellidos,
            "foto_perfil": detalle.imagen.url if detalle.imagen else None }
    return data

def aumentar_almacenamiento_usuario(usuario, almacenamiento_utilizado):
    almacenamiento = AlmacenamientoUsuario.objects.get(usuario=usuario)
    almacenamiento.usado += almacenamiento_utilizado
    almacenamiento.save()
    
def aumentar_almacenamiento_global(almacenamiento_utilizado):
    almacenamiento = AlmacenamientoGlobal.objects.get(id=1)
    almacenamiento.total_usado += almacenamiento_utilizado
    almacenamiento.save()

def reducir_almacenamiento_usuario(usuario, almacenamiento_utilizado):
    almacenamiento = AlmacenamientoUsuario.objects.get(usuario=usuario)
    actual = almacenamiento.usado - almacenamiento_utilizado
    if actual > 0:
        almacenamiento.usado = actual
    else:
        almacenamiento.usado = 0
    almacenamiento.save()

def reducir_almacenamiento_global(almacenamiento_utilizado):
    almacenamiento = AlmacenamientoGlobal.objects.get(id=1)
    actual = almacenamiento.total_usado - almacenamiento_utilizado
    if actual > 0:
        almacenamiento.total_usado = actual
    else:
        almacenamiento.total_usado = 0
    almacenamiento.save()


class Biografia(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    foto_perfil = models.ImageField(upload_to='perfil/', default='avatar.png')
    foto_portada = models.ImageField(
        upload_to='portada/', default='portada.jpg')
    descripcion = models.TextField(default='Sin descripción ...')
    seguidores = models.IntegerField(default=0)
    seguidos = models.IntegerField(default=0)

    def __str__(self):
        return str(self.usuario)

    @property
    def usuario_info(self):
        return usuario_detalle(self.usuario)

    def incrementar_seguidores(self):
        self.seguidores += 1
        self.save()

    def incrementar_seguidos(self):
        self.seguidos += 1
        self.save()

    def decrementar_seguidores(self):
        if self.seguidores > 0:
            self.seguidores -= 1
        self.save()

    def decrementar_seguidos(self):
        if self.seguidos > 0:
            self.seguidos -= 1
        self.save()


class Seguidor(models.Model):
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='seguido')
    seguidor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='seguidor')
    
    def __str__(self):
        return f'{str(self.usuario)} - {str(self.seguidor)}'

    @property
    def seguidos_info(self):
        return usuario_detalle(self.usuario)

    @property
    def seguidor_info(self):
        return usuario_detalle(self.seguidor)
    
    @property
    def siguiendo(self):
        try:
            Seguidor.objects.get(usuario=self.seguidor, seguidor=self.usuario)
            return True
        except Seguidor.DoesNotExist:
            return False
        


class Publicacion(models.Model):

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField(blank=True, default="")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    num_likes = models.IntegerField(default=0)
    visible = models.BooleanField(default=True)
    motivo = models.TextField(blank=True, default="")

    def __str__(self):
        return f'{str(self.usuario)}: {self.pk}'

    @property
    def usuario_info(self):
        return usuario_detalle(self.usuario)

    @property
    def num_comentarios(self):
        return self.comentario.all().count()

    @property
    def comentarios(self):
        from .serializers import ComentarioSerializer
        all_comentarios = self.comentario.filter(comentario_padre=None).all()
        return ComentarioSerializer(all_comentarios, many=True).data

    @property
    def archivos_publicacion(self):
        return self.archivos.filter(publicacion=self).all()
        
    

class ArchivoPublicacion(models.Model):
    class MediaType(models.TextChoices):
        IMAGE = 'IMG', 'Imagen'
        VIDEO = 'VID', 'Video'
        AUDIO = 'AUD', 'Audio'

    publicacion = models.ForeignKey(
        Publicacion, related_name='archivos', on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='publicacion/')
    tipo = models.CharField(max_length=3, choices=MediaType.choices)
    almacenamiento_utilizado = models.DecimalField(max_digits=10, decimal_places=2 ,default=0)

    def delete(self, *args, **kwargs):
        if self.archivo and os.path.isfile(self.archivo.path):
            os.remove(self.archivo.path)
        super(ArchivoPublicacion, self).delete(*args, **kwargs)
    
    def aumentar_almacenamiento(self, usuario):
        aumentar_almacenamiento_usuario(usuario, self.almacenamiento_utilizado)
        aumentar_almacenamiento_global(self.almacenamiento_utilizado)
    
    def reducir_almacenamiento(self, usuario):
        reducir_almacenamiento_usuario(usuario, self.almacenamiento_utilizado)
        reducir_almacenamiento_global(self.almacenamiento_utilizado)


class Like(models.Model):
    publicacion = models.ForeignKey(
        Publicacion, on_delete=models.CASCADE)
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE)

    def incrementar_publicacion_likes(self):
        publicacion = Publicacion.objects.get(id=self.publicacion.id)
        publicacion.num_likes += 1
        publicacion.save()

    def decrementar_publicacion_likes(self):
        publicacion = Publicacion.objects.get(id=self.publicacion.id)
        if publicacion.num_likes > 0:
            publicacion.num_likes -= 1
        publicacion.save()

class Comentario(models.Model):

    class Meta:
        ordering = ['-fecha_creacion']

    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE)
    publicacion = models.ForeignKey(
        Publicacion, on_delete=models.CASCADE, related_name='comentario')
    texto = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='comentario/', blank=True, null=True)
    comentario_padre = models.ForeignKey('self', on_delete=models.CASCADE,
        blank=True, null=True, related_name='padre')
    almacenamiento_utilizado = models.DecimalField(max_digits=10, decimal_places=2 ,default=0)
    
    def __str__(self):
        return f'{str(self.usuario)}: {self.pk}'
    
    def delete(self, *args, **kwargs):
        if self.imagen and os.path.isfile(self.imagen.path):
            os.remove(self.imagen.path)
        super(Comentario, self).delete(*args, **kwargs)
    
    def aumentar_almacenamiento(self):
        aumentar_almacenamiento_usuario(self.usuario, self.almacenamiento_utilizado)
        aumentar_almacenamiento_global(self.almacenamiento_utilizado)
    
    def reducir_almacenamiento(self):
        reducir_almacenamiento_usuario(self.usuario, self.almacenamiento_utilizado)
        reducir_almacenamiento_global(self.almacenamiento_utilizado)

    def count_comentarios_hijos(self):
        return Comentario.objects.filter(comentario_padre=self).all().count()
   
    @property
    def usuario_info(self):
        return usuario_detalle(self.usuario)

    @property
    def comentarios_hijo(self):
        from .serializers import ComentarioSerializer
        comentarios = Comentario.objects.filter(comentario_padre=self).all()
        return ComentarioSerializer(comentarios, many=True).data
    
    @property
    def es_padre(self):
        if self.count_comentarios_hijos() > 0:
            return True
        return False
    
    @property
    def nivel_comentario(self):
        nivel = 0
        padre = self.comentario_padre
        while padre != None:
            nivel += 1
            padre = padre.comentario_padre
        return nivel


class Historia(models.Model):

    class Meta:
        ordering = ['-fecha_creacion']

    class MediaType(models.TextChoices):
        IMAGE = 'IMG', 'Imagen'
        VIDEO = 'VID', 'Video'
        AUDIO = 'AUD', 'Audio'

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField(blank=True, default="")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    archivo = models.FileField(upload_to='historias/', blank=True, null=True)
    tipo_archivo = models.CharField(max_length=3, choices=MediaType.choices, default="")
    almacenamiento_utilizado = models.DecimalField(max_digits=10, decimal_places=2 ,default=0)

    def delete(self, *args, **kwargs):
        if self.archivo and os.path.isfile(self.archivo.path):
            os.remove(self.archivo.path)
        super(Historia, self).delete(*args, **kwargs)
    
    def aumentar_almacenamiento(self):
        aumentar_almacenamiento_usuario(self.usuario, self.almacenamiento_utilizado)
        aumentar_almacenamiento_global(self.almacenamiento_utilizado)
    
    def reducir_almacenamiento(self):
        reducir_almacenamiento_usuario(self.usuario, self.almacenamiento_utilizado)
        reducir_almacenamiento_global(self.almacenamiento_utilizado)