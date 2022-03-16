from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions

from .serializers import *
from .models import Publicacion

from almacenamiento.utils import almacenamiento_disponible_user, almacenamiento_disponible_servidor, peso_archivo_permitido
from .utils import fileb64decode, eliminar_archivo
import random
from django.utils import timezone
import datetime

class BiografiaView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, usuario):
        biografia, created = Biografia.objects.get_or_create(usuario=usuario)
        return biografia
    
    def list(self, request):
        biografia = self.get_object(request.user)
        serializer = BiografiaSerializer(biografia)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        data = request.data
        biografia = self.get_object(request.user)

        if data['foto_perfil'] != None:
            resultado = fileb64decode(data['foto_perfil'], request.user.id)
            if "message" in resultado:
                return Response(resultado, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
            data['foto_perfil'] = resultado[1]
            eliminar_archivo(biografia.foto_perfil)
        else:
            data.pop('foto_perfil')
        if data['foto_portada'] != None:
            resultado = fileb64decode(data['foto_portada'], request.user.id)
            if "message" in resultado:
                return Response(resultado, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
            data['foto_portada'] = resultado[1]
            eliminar_archivo(biografia.foto_portada)
        else:
            data.pop('foto_portada')

        serializer = BiografiaSerializer(biografia, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PublicacionView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, pk):
        try:
            publicacion = Publicacion.objects.get(pk=pk)
            return Response(PublicacionSerializer(publicacion).data, status=status.HTTP_200_OK)
        except Publicacion.DoesNotExist:
            return Response({"message": "Publicación no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        start = timezone.now().replace(hour=0, minute=0, second=0)
        end = timezone.now().replace(hour=23, minute=59, second=59)
        publicaciones_admin = Publicacion.objects.filter(usuario__is_superuser=1, fecha_creacion__gte=start, fecha_creacion__lte=end).order_by('-fecha_creacion')
        publicaciones = Publicacion.objects.filter(visible=True).order_by('-fecha_creacion')
        data = []
        if len(publicaciones_admin) > 0:
            data = list(publicaciones_admin) + list(publicaciones.exclude(usuario__is_superuser=1, fecha_creacion__gte=start, fecha_creacion__lte=end))
        else:
            data = publicaciones

        paginator = PageNumberPagination()
        paginator.page_size = 10
        result = paginator.paginate_queryset(data, request)

        serializer = PublicacionSerializer(result, many=True)
        paginated_response = paginator.get_paginated_response(serializer.data)

        return Response(paginated_response.data, status=status.HTTP_200_OK)

    def create(self, request):
        data = request.data
        if not data:
            return Response({"message": "Publicación sin contenido."}, status=status.HTTP_400_BAD_REQUEST)
        archivos = data['archivos'] if 'archivos' in data else []
        for i in range(len(archivos)):
            resultado = fileb64decode(archivos[i]['archivo'], request.user.id)
            if "message" in resultado:
                return Response(resultado, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
            archivos[i]['tipo'] = resultado[0]
            archivos[i]['archivo'] = resultado[1]
            archivos[i]['almacenamiento_utilizado'] = round(archivos[i]['almacenamiento_utilizado'], 2)

            if not peso_archivo_permitido(request.user, archivos[i]['almacenamiento_utilizado']):
                return Response({"message": "El archivo supera el limite de peso establecido."}, status=status.HTTP_400_BAD_REQUEST)

        data['archivos'] = archivos
        data['usuario'] = request.user.id

        if not almacenamiento_disponible_user(request.user, data['archivos']):
            return Response({"message": "Publicación supera la capacidad maxima de almacenamiento."}, status=status.HTTP_400_BAD_REQUEST)
        if not almacenamiento_disponible_servidor(data['archivos']):
            return Response({"message": "Almacenamiento superado"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PublicacionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk):
        data = request.data
        try:
            publicacion = Publicacion.objects.get(pk=pk)
            if publicacion.usuario == request.user:
                archivos = data['archivos'] if 'archivos' in data else []
                nuevos_archivos = []
                for i, archivo in enumerate(archivos):
                    if 'id' in archivo:
                        archivo_db = ArchivoPublicacion.objects.get(id=archivo['id'])
                        if archivo['archivo'] == None:
                            archivo_db.reducir_almacenamiento(publicacion.usuario)
                            archivo_db.delete()
                    else:
                        resultado = fileb64decode(archivo['archivo'], request.user.id)
                        if "message" in resultado:
                            return Response(resultado, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
                        archivos[i]['tipo'] = resultado[0]
                        archivos[i]['archivo'] = resultado[1]
                        archivos[i]['almacenamiento_utilizado'] = round(archivos[i]['almacenamiento_utilizado'], 2)

                        if not peso_archivo_permitido(request.user, archivos[i]['almacenamiento_utilizado']):
                            return Response({"message": "El archivo supera el limite de peso establecido."}, status=status.HTTP_400_BAD_REQUEST)

                        nuevos_archivos.append(archivos[i])
                data['archivos'] = nuevos_archivos
                
                if not almacenamiento_disponible_user(request.user, data['archivos']):
                    return Response({"message": "Publicación supera la capacidad máxima de almacenamiento."}, status=status.HTTP_400_BAD_REQUEST)
                if not almacenamiento_disponible_servidor(data['archivos']):
                    return Response({"message": "Almacenamiento superado"}, status=status.HTTP_400_BAD_REQUEST)

                serializer = PublicacionSerializer(publicacion, data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "No tienes permisos para editar esta publicación."} , status=status.HTTP_403_FORBIDDEN)
        except Publicacion.DoesNotExist:
            return Response({"message": "Publicación no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk):
        try:
            publicacion = Publicacion.objects.get(pk=pk)
            if publicacion.usuario == request.user:
                archivos = ArchivoPublicacion.objects.filter(publicacion=publicacion)
                for archivo in archivos:
                    archivo.reducir_almacenamiento(publicacion.usuario)
                    archivo.delete()
                publicacion.delete()
                return Response(status=status.HTTP_200_OK)
            return Response({"message": "No tienes permisos para eliminar esta publicación."} , status=status.HTTP_403_FORBIDDEN)
        except Publicacion.DoesNotExist:
            return Response({"message": "Publicación no encontrada"}, status=status.HTTP_404_NOT_FOUND)


class PublicacionUsuarioView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request):
        publicaciones = Publicacion.objects.filter(usuario=request.user.id)
        
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result = paginator.paginate_queryset(publicaciones, request)

        serializer = PublicacionSerializer(result, many=True)
        paginated_response = paginator.get_paginated_response(serializer.data)

        return Response(paginated_response.data, status=status.HTTP_200_OK)


class ReportarPublicacionView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def partial_update(self, request, pk):
        data = request.data
        try:
            publicacion = Publicacion.objects.get(pk=pk)
            if 'motivo' not in data:
                return Response(status=status.HTTP_400_BAD_REQUEST) 
            data['visible'] = False
            publicacion.motivo = data['motivo']
            publicacion.visible = False
            publicacion.save()
            return Response(status=status.HTTP_200_OK)
        except Publicacion.DoesNotExist:
            return Response({"message": "Publicación no encontrada"}, status=status.HTTP_404_NOT_FOUND)


class ComentarioView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request):
        data = request.data
        if 'imagen' in data and data['imagen'] is not None:
            resultado = fileb64decode(data['imagen'], request.user.id)
            if "message" in resultado:
                return Response(resultado, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
            data['imagen'] = resultado[1]
            data['almacenamiento_utilizado'] = round(data['almacenamiento_utilizado'], 2)

            if not peso_archivo_permitido(request.user, data['almacenamiento_utilizado']):
                return Response({"message": "El archivo supera el limite de peso establecido."}, status=status.HTTP_400_BAD_REQUEST)
            if not almacenamiento_disponible_user(request.user, [data]):
                return Response({"message": "El comentario supera la capacidad máxima de almacenamiento."}, status=status.HTTP_400_BAD_REQUEST)
            if not almacenamiento_disponible_servidor([data]):
                return Response({"message": "Almacenamiento superado"}, status=status.HTTP_400_BAD_REQUEST)

        data['usuario'] = request.user.id

        serializer = ComentarioSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            publicacion = Publicacion.objects.get(id=data['publicacion'])
            comentarios = publicacion.comentario.filter(comentario_padre=None).all()

            return Response(ComentarioSerializer(comentarios, many=True).data ,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk):
        data = request.data
        try:
            comentario = Comentario.objects.get(pk=pk)
            if comentario.usuario == request.user:
                if 'imagen' not in data:
                    comentario.reducir_almacenamiento()
                    eliminar_archivo(comentario.imagen)
                    comentario.imagen = None
                    comentario.almacenamiento_utilizado = 0.00
                else:
                    if ';base64,' in data['imagen']:
                        resultado = fileb64decode(data['imagen'], request.user.id)
                        if "message" in resultado:
                            return Response(resultado, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
                        data['imagen'] = resultado[1]
                        data['almacenamiento_utilizado'] = round(data['almacenamiento_utilizado'], 2)

                        if not peso_archivo_permitido(request.user, data['almacenamiento_utilizado']):
                            return Response({"message": "El archivo supera el limite de peso establecido."}, status=status.HTTP_400_BAD_REQUEST)
                        if not almacenamiento_disponible_user(request.user, [data]):
                            return Response({"message": "El comentario supera la capacidad máxima de almacenamiento."}, status=status.HTTP_400_BAD_REQUEST)
                        if not almacenamiento_disponible_servidor([data]):
                            return Response({"message": "Almacenamiento superado"}, status=status.HTTP_400_BAD_REQUEST)

                        if comentario.imagen:
                            comentario.reducir_almacenamiento()
                            eliminar_archivo(comentario.imagen)
                    else:
                        data.pop('imagen')
                        if 'almacenamiento_utilizado' in data:
                            data.pop('almacenamiento_utilizado')

                serializer = ComentarioSerializer(comentario, data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "No tienes permisos para editar esta comentario."} , status=status.HTTP_403_FORBIDDEN)
        except Comentario.DoesNotExist:
            return Response({"message": "Comentario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
    def destroy(self, request, pk):
        try:
            comentario = Comentario.objects.get(pk=pk)
            if comentario.usuario == request.user:
                comentarios_hijos = Comentario.objects.filter(comentario_padre=comentario.id).all()
                for c_hijo in comentarios_hijos:
                    if c_hijo.imagen:
                        c_hijo.reducir_almacenamiento()
                        eliminar_archivo(c_hijo.imagen)
                comentario.reducir_almacenamiento()
                comentario.delete()
                return Response(status=status.HTTP_200_OK)
            else:
              return Response(data={"message": "No tienes permisos para editar esta comentario."} , status=status.HTTP_403_FORBIDDEN)  
        except Comentario.DoesNotExist:
            return Response({"message": "Comentario no encontrado"}, status=status.HTTP_404_NOT_FOUND)


class LikeView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request):
        publicacion_id = request.data['publicacion']
        usuario = request.user
        try:
            Like.objects.get(publicacion=publicacion_id, usuario=usuario)
            return Response({"message": "Ya se ha dado like a esa publicación."}, status=status.HTTP_400_BAD_REQUEST)
        except Like.DoesNotExist:
            publicacion = Publicacion.objects.get(id=publicacion_id)
            if publicacion.usuario == usuario:
                return Response({"message": "No puede dar like a su publicación."}, status=status.HTTP_400_BAD_REQUEST)
            like = Like.objects.create(publicacion=publicacion, usuario=usuario)
            like.incrementar_publicacion_likes()
            return Response(status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk):
        publicacion_id = pk
        usuario = request.user
        try:
            like = Like.objects.get(publicacion=publicacion_id, usuario=usuario)
            like.decrementar_publicacion_likes()
            like.delete()
            return Response(status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class SeguidorView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    
    def list(self, request):
        seguidores = Seguidor.objects.filter(usuario=request.user)
        seguidos = Seguidor.objects.filter(seguidor=request.user)

        seguidores_serializer = SeguidorSerializer(seguidores, many=True)
        seguidos_serializer = SeguidosSerializer(seguidos, many=True)

        data = { "seguidores": seguidores_serializer.data, "seguidos": seguidos_serializer.data }
        return Response(data, status=status.HTTP_200_OK)

    def create(self, request):
        data = request.data
        data['seguidor'] = request.user.id
        try:
            Seguidor.objects.get(seguidor=request.user.id, usuario=data['usuario'])
            return Response({"message": "Ya sigues a este usuario"}, status=status.HTTP_400_BAD_REQUEST)
        except Seguidor.DoesNotExist:
            serializer = SeguidorSerializer(data=data)
            if serializer.is_valid():
                biografia_seguidor = Biografia.objects.get(usuario=request.user.id)
                biografia_seguido = Biografia.objects.get(usuario=data['usuario'])

                biografia_seguidor.incrementar_seguidos()
                biografia_seguido.incrementar_seguidores()

                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        try:
            seguidor = Seguidor.objects.get(seguidor=request.user.id, usuario=pk)

            biografia_seguidor = Biografia.objects.get(usuario=seguidor.seguidor)
            biografia_seguido = Biografia.objects.get(usuario=seguidor.usuario)

            biografia_seguidor.decrementar_seguidos()
            biografia_seguido.decrementar_seguidores()

            seguidor.delete()
            return Response(status=status.HTTP_200_OK)
        except Seguidor.DoesNotExist:
            return Response({"message": "Parece que ya no sigues a este usuario"}, status=status.HTTP_404_NOT_FOUND)


class RecomendacionAmigoView(viewsets.ReadOnlyModelViewSet):
    serializer_class = BiografiaSerializer

    def get_queryset(self):
        q = self.request.GET.get('amigo')
        biografias = Biografia.objects.all().exclude(usuario=self.request.user.id)
        seguidos = Seguidor.objects.filter(seguidor=self.request.user.id)

        biografia_seguidos = []
        for s in seguidos:
            biografia_seguidos.append(Biografia.objects.get(usuario=s.usuario.id))

        disponibles = []
        for b in biografias:
            if b not in biografia_seguidos:
                disponibles.append(b)

        if q:
            user_details = UserDetails.objects.filter(nombres__icontains=q).exclude(usuario=self.request.user.id)
            disponibles.clear()
            for detalle in user_details:
                disponibles.append(Biografia.objects.get(usuario=detalle.usuario))
        else:
            random.shuffle(disponibles)
            disponibles = disponibles[:10]
        return disponibles

    
class HistoriaView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def usuario_detalle(self, usuario):
        detalle = UserDetails.objects.get(usuario=usuario)
        return {
            "usuario": usuario,
            "nombres": detalle.nombres,
            "apellidos": detalle.apellidos,
            "foto_perfil": detalle.imagen.url if detalle.imagen else None,
        }

    def list(self, request):
        historias = []
        historias_usuario = Historia.objects.filter(usuario=request.user)
        historias_usuario = HistoriaSerializer(historias_usuario, many=True).data
        data =  self.usuario_detalle(request.user.id)
        data.update({"historias": historias_usuario})
        historias.append(data)

        seguidos = Seguidor.objects.filter(seguidor=request.user)
        for seguido in seguidos:
            historias_seguido = Historia.objects.filter(usuario=seguido.usuario)
            if len(historias_seguido) > 0:
                historias_seguido = HistoriaSerializer(historias_seguido, many=True).data
                data = self.usuario_detalle(seguido.usuario.id)
                data.update({"historias": historias_seguido})
                historias.append(data)

        return Response(historias, status=status.HTTP_200_OK)

    def create(self, request):
        data = request.data
        if not data:
            return Response({"message": "Historia sin contenido."}, status=status.HTTP_400_BAD_REQUEST)
        if 'archivo' in data and data['archivo'] is not None:
            resultado = fileb64decode(data['archivo'], request.user.id)
            if "message" in resultado:
                return Response(resultado, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
            data['tipo_archivo'] = resultado[0]
            data['archivo'] = resultado[1]
            data['almacenamiento_utilizado'] = round(data['almacenamiento_utilizado'], 2)

            if not peso_archivo_permitido(request.user, data['almacenamiento_utilizado']):
                return Response({"message": "El archivo supera el limite de peso establecido."}, status=status.HTTP_400_BAD_REQUEST)
            if not almacenamiento_disponible_user(request.user, [data]):
                return Response({"message": "La historia supera la capacidad máxima de almacenamiento."}, status=status.HTTP_400_BAD_REQUEST)
            if not almacenamiento_disponible_servidor([data]):
                return Response({"message": "Almacenamiento superado"}, status=status.HTTP_400_BAD_REQUEST)

        data['usuario'] = request.user.id
        
        serializer = HistoriaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk): 
        try:
            historia = Historia.objects.get(pk=pk)
            if historia.usuario == request.user:
                historia.reducir_almacenamiento()
                historia.delete()
                return Response(status=status.HTTP_200_OK)
            else:
              return Response(data={"message": "No tienes permisos para eliminar esta historia."} , status=status.HTTP_403_FORBIDDEN)  
        except Comentario.DoesNotExist:
            return Response({"message": "Historia no encontrada"}, status=status.HTTP_404_NOT_FOUND)