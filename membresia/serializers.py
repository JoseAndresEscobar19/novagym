from rest_framework import serializers

from membresia.models import Beneficio, Descuento, Historial, Membresia


class BeneficioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beneficio
        fields = '__all__'


class DescuentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Descuento
        fields = ['url', 'porcentaje_descuento', 'fecha_hora_desde', 'fecha_hora_hasta',
                  'activo', ]


class HistorialSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(source='membresia.nombre')
    descripcion = serializers.CharField(source='membresia.descripcion')

    class Meta:
        model = Historial
        fields = ['fecha_inicio', 'fecha_fin',
                  'costo', 'activa', 'nombre', 'descripcion']


class MembresiaSerializer(serializers.HyperlinkedModelSerializer):
    beneficios = BeneficioSerializer(many=True)
    descuento = serializers.SerializerMethodField()

    class Meta:
        model = Membresia
        fields = ['url', 'beneficios', 'nombre', 'descripcion',
                  'precio', 'meses_duracion', 'estado', 'descuento']

    def get_descuento(self, object):
        try:
            descuento = object.descuentos.get(activo=True)
            return DescuentoSerializer(descuento, context={'request': self.context['request']}).data
        except:
            return None
