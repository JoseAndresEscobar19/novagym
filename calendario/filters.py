import django_filters
from calendario.forms import MaquinaFilterForm

from gimnasio.models import Gimnasio
from .models import Horario,Maquina, MaquinaReserva, Zona
class CalendarioFilter(django_filters.FilterSet):
    class Meta:
        model = Horario
        fields = ['gimnasio',
                  ]

class MaquinaFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr="icontains", label='Nombre')
    categoria = django_filters.ChoiceFilter(choices=Maquina.Categoria.choices)
    reservable = django_filters.ChoiceFilter(choices=(('1', 'Reservable'), ('0', 'No reservable')))
    activo = django_filters.ChoiceFilter(choices=(('1', 'Activo'), ('0', 'Inactivo')))
    gimnasio = django_filters.ModelChoiceFilter(queryset=Gimnasio.objects.all())
    zona = django_filters.ModelChoiceFilter(queryset=Zona.objects.all().filter(tipo="maquinas"))
    class Meta:
        model = Maquina
        fields = ['nombre',
                  'categoria',
                    'reservable',
                    'activo',
                  'gimnasio',
                  'zona'
                  ]
        form = MaquinaFilterForm

class MaquinaReservaFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr="icontains", label='Nombre')
    categoria = django_filters.ChoiceFilter(choices=Maquina.Categoria.choices)
    reservable = django_filters.ChoiceFilter(choices=(('1', 'Reservable'), ('0', 'No reservable')))
    activo = django_filters.ChoiceFilter(choices=(('1', 'Activo'), ('0', 'Inactivo')))
    gimnasio = django_filters.ModelChoiceFilter(queryset=Gimnasio.objects.all())
    zona = django_filters.ModelChoiceFilter(queryset=Zona.objects.all().filter(tipo="maquinas"))
    class Meta:
        model = MaquinaReserva
        fields = ['nombre',
                  'categoria',
                    'reservable',
                    'activo',
                  'gimnasio',
                  'zona'
                  ]
        form = MaquinaFilterForm