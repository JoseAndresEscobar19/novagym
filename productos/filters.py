import django_filters
from .models import Producto,Categoria

class ProductoFilter(django_filters.FilterSet):
    class Producto:
        model = Producto
        fields = ['id',
                  'codigo',
                  'nombre',
                  'descripcion',
                  'precio_referencial',
                  'categoria',
                  "valor_presentacion",
                  'talla',
                  "unidad_presentacion",
                  ]

class CategoriaFilter(django_filters.FilterSet):
    class Meta:
        model = Categoria
        fields = ['id',
                  'nombre'
                  ]