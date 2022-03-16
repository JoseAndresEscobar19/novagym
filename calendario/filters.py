import django_filters
from .models import Calendario
class CalendarioFilter(django_filters.FilterSet):
    class Meta:
        model = Calendario
        fields = ['gimnasio',
                  ]