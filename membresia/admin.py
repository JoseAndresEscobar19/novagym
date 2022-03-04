from django.contrib import admin

from membresia.models import Beneficio, Descuento, Historial, Membresia

# Register your models here.
admin.site.register(Membresia)
admin.site.register(Beneficio)
admin.site.register(Descuento)
admin.site.register(Historial)
