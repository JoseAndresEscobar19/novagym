import django_filters
from .models import Buzon

class BuzonFilter(django_filters.FilterSet):
    class Meta:
        model = Buzon
        fields = ['id',
                  'sender',
                  'titulo',
                  'descripcion',
                  'fecha',
                  "leido",
                  ]