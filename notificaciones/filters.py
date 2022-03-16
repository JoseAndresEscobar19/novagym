import django_filters
from .models import Notificacion

class NotificacionFilter(django_filters.FilterSet):
    class Meta:
        model = Notificacion
        fields = ['id',
                  'titulo',
                  'cuerpo',
                  'fecha_hora_inicio',
                  'fecha_hora_fin',
                  "frecuencia",
                  'activo',
                  "created_at",
                  ]