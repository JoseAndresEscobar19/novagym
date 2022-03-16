from rest_framework import permissions, viewsets

from membresia.models import Beneficio, Descuento, Historial, Membresia
from membresia.serializers import BeneficioSerializer, DescuentoSerializer, MembresiaSerializer


class MembresiaViewSet(viewsets.ModelViewSet):
    queryset = Membresia.objects.all().prefetch_related('beneficios', 'descuentos')
    serializer_class = MembresiaSerializer


class BeneficioViewSet(viewsets.ModelViewSet):
    queryset = Beneficio.objects.all().order_by('id')
    serializer_class = BeneficioSerializer


class DescuentoViewSet(viewsets.ModelViewSet):
    queryset = Descuento.objects.all().order_by('-activo')
    serializer_class = DescuentoSerializer
