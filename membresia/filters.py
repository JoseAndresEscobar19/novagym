import django_filters

from membresia.forms import MembresiaFilterForm
from membresia.models import Membresia


class MembresiaFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr="icontains", label='Nombre')
    estado = django_filters.ChoiceFilter(label='Estado', choices=(('1', 'Habilitado'), ('0', 'Deshabilitado'),))

    class Meta:
        model = Membresia
        fields = ['nombre', 'estado', ]
        form = MembresiaFilterForm
