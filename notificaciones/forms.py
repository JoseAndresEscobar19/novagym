from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Div, Field, Layout, Row
from django import forms

from .models import *


class NotificacionForm(forms.ModelForm):
    class Meta:
        model = Notificacion
        fields = ('titulo', 'cuerpo', 'imagen', "fecha_inicio",
                  "fecha_fin", "frecuencia")
        labels = {
            'titulo': 'Título',
            'fecha_inicio': 'Fecha de inicio',
            'fecha_fin': 'Fecha de fin'
        }
        widgets = {
            "cuerpo": forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    Row(
                        Column('titulo', css_class='col-12'),
                        Column('cuerpo', css_class='col-12'),
                        Column('imagen', css_class='col-12'),
                    ), css_class='col-12 col-lg-6'),
                Column(
                    Row(
                        Column('fecha_inicio', css_class='col-6'),
                        Column('fecha_fin', css_class='col-6'),
                        Column('frecuencia', css_class='col-12'),
                    ), css_class='col-12 col-lg-6'),
            ),
        )
