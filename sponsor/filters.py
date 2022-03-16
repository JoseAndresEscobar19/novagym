import django_filters
from .models import Sponsor
class SponsorFilter(django_filters.FilterSet):
    class Meta:
        model = Sponsor
        fields = ['id',
                  'codigo',
                  'nombre',
                  'descripcion',
                  'telefono',
                  "nombre_contacto",
                  'url',
                  'fecha_inicio',
                  'fecha_fin',
                  'activo',
                  ]