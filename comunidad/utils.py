from django.core.files.base import ContentFile
import base64
import os


EXTENSIONES_PERMITIDAS = ['gif', 'png', 'jpeg', 'jpg', 'jfif',
                          'mp4', 'avi', 'wmv', 'flv',
                          'mp3', 'wav', 'opus', 'wma']

tipo_archivo = {
    'ogg': 'opus',
    'x-ms-wma': "wma",
    'mpeg': 'mp3',
    'x-wav': 'wav',
    'x-msvideo': 'avi',
    'x-ms-wmv': 'wmv',
    'x-flv': 'flv',
    'mp4': 'mp4'
}

enum_media = {
    'image': 'IMG',
    'audio': 'AUD',
    'video': 'VID'
}


def obtener_extension(formato):
    if formato in tipo_archivo:
        return tipo_archivo[formato]
    return formato


def fileb64decode(archivo, id_user):
    try:
        info, contenido = archivo.split(";base64,")
        mime_type, ext = info.split('/')
        media = mime_type.split(':')[-1]

        ext = obtener_extension(ext)
        if not (ext in EXTENSIONES_PERMITIDAS):
            return {"message": "Formato de archivo no permitido."}

        return [enum_media[media], ContentFile(base64.b64decode(contenido), name=f"{media}_{id_user}." + ext)]
    except:
        return {"message": "Error al subir el archivo."}


def eliminar_archivo(archivo):
    if archivo and os.path.exists(archivo.path):
        if archivo.name != 'avatar.png' and archivo.name != 'portada.jpg':
            os.remove(archivo.path)