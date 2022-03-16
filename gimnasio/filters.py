import django_filters
from .models import Gimnasio
class GimnasioFilter(django_filters.FilterSet):
    class Meta:
        model = Gimnasio
        fields = ['id',
                  'tipo',
                  'nombre',
                  'telefono',
                  'ubicacion',
                  "horario_inicio",
                  'horario_fin',
                  'estado',
                  'ciudad',
                  'aforo',
                  ]