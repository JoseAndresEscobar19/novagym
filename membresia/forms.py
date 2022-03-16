from crispy_forms.bootstrap import PrependedText, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Field, Layout, Row
from django import forms

from membresia.models import Beneficio, Membresia


class MembresiaFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('nombre',
                       css_class='col-12 col-sm-6 col-md-4 col-lg-3'),
                Column(
                    'estado', css_class='col-12 col-sm-6 col-md-4 col-lg-3'),
            ),
            Row(
                Column(
                    StrictButton("Buscar", type='submit',
                                 css_class='btn btn-primary mt-1'),
                    css_class='col-12'
                )
            ),
        )


class MembresiaForm(forms.ModelForm):
    class Meta:
        model = Membresia
        exclude = ('estado',)
        labels = {
            'descripcion': 'Descripción',
            'meses_duracion': 'Duración (meses)'
        }
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('nombre', css_class='col-12 col-md-6'),
            ),
            Row(
                Column('descripcion', css_class='col-12 col-md-6'),
            ),
            Row(
                Column(PrependedText('precio', '$'),
                       css_class='col-6 col-md-3'),
                Column('meses_duracion', css_class='col-6 col-md-3'),
            ),
            Row(
                Column(Field('beneficios', multiple="true",
                       css_class="select2"), css_class="col-12 col-md-6"),
                Column(
                    HTML("""
                        <a href="#" data-url="{% url 'membresia:listar_beneficio' %}" 
                            data-toggle='modal' data-target="#mainModal" class="btn btn-primary use-modal mr-2" >
                            <i class="fas fa-list"></i>
                        </a>
                       """), css_class='col-auto align-self-end py-2')
            ),
            Row(
                Column('imagen', css_class='col-12 col-md-7')
            ),
        )


class BeneficioForm(forms.ModelForm):
    class Meta:
        model = Beneficio
        fields = '__all__'
        labels = {
            'texto': 'Descripción'
        }
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 2}),
        }
