from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Inventario)
admin.site.register(ProductoDescuento)