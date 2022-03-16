from django import template

from comunidad.utils import tipo_archivo

register = template.Library()


@register.filter(name="mime_type")
def mime_type(url):
    ext = url.split(".")[1]
    for key, value in tipo_archivo.items():
        if ext == value:
            return key
    return ext
