from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Div, Field, Layout, Row
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from seguridad.models import *


class UsuarioForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", 'email', 'groups']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['username'].help_text = None
        self.fields['groups'].help_text = 'Use Ctrl para quitar o agregar al usuario a varios grupos.'
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='col-4'),
                Column('email', css_class='col-8'),
                Column('groups', css_class='col-6'),
            ),
            Row(
                Column('password1', css_class='col-6'),
                Column('password2', css_class='col-6'),
            ),
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            self.save_m2m()
        return user


class UsuarioEditarForm(UserChangeForm):
    class Meta:
        model = User
        fields = ["username", 'email', 'groups']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['username'].help_text = None
        self.fields['groups'].help_text = 'Use Ctrl para quitar o agregar al usuario a varios grupos.'
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='col-4'),
                Column('email', css_class='col-8'),
                Column('groups', css_class='col-6'),
            ),
        )


class UsuarioDetallesForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        labels = {
            'cedula': "Cédula",
            'nombres': "Nombres",
            'apellidos': "Apellidos",
            'telefono': "Teléfono",
            'telefono2': "Teléfono secundario",
            'direccion': "Dirección",
            'sexo': "Sexo",
        }
        fields = ['cedula',
                  'nombres',
                  'apellidos',
                  'telefono',
                  'telefono2',
                  'direccion',
                  'sexo', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('cedula', css_class='col-6 col-xl-4'),
                Column('nombres', css_class='col-6 col-xl-4'),
                Column('apellidos', css_class='col-6 col-xl-4'),
                Column('sexo', css_class='col-6 col-xl-4'),
                Column('telefono', css_class='col-6 col-xl-4'),
                Column('telefono2', css_class='col-6 col-xl-4'),
                Column('direccion', css_class='col-12 col-lg-8'),
            ),
        )


class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        exclude = ('usuario', 'detalles',)
        labels = {
            "imagen": "Foto de perfil"
        }
        widgets = {
            "codigo": forms.HiddenInput(),
            "estado": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False


class EmpleadoEditarForm(forms.ModelForm):
    class Meta:
        model = Empleado
        exclude = ('usuario', 'detalles',)
        labels = {
            "imagen": "Foto de perfil"
        }
        widgets = {
            "codigo": forms.HiddenInput(),
            "imagen": forms.ClearableFileInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                'codigo',
                Column('estado', css_class='col-4'),
                Column('imagen', css_class='col-8'),
            ),
        )


class EmpleadoFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.fields['orden_fechas'].label = "Fechas de ventas"
        self.fields['orden_monto'].label = "Monto de ventas"
        self.fields['detalles__sexo'].label = "Sexo del empleado"
        self.fields['created_at'].label = "Fecha de ingreso"
        self.fields['rol'].label = "Rol del empleado"
        self.helper.layout = Layout(
            Row(
                Column(
                    Field('created_at', template="forms/fields/range-filter.html",
                          css_class="form-control"), css_class='col-12 col-lg-6'
                ),
                Column('detalles__sexo', css_class='col-6 col-lg-3'),
                Column('estado', css_class='col-6 col-lg-3'),
                Column(
                    Field('orden_fechas',
                          template="forms/fields/range-filter.html", css_class="form-control"),
                    css_class='col-12 col-lg-6'
                ),
                Column(
                    Field('orden_monto',
                          template="forms/fields/range-filter.html", css_class="form-control", placeholder="$"),
                    css_class='col-12 col-lg-3'
                ),
                Column('rol', css_class="'col-6 col-lg-3"),
                Column(
                    StrictButton("Buscar", type='submit',
                                 css_class='btn btn-primary mt-1'),
                    css_class='col-12'
                )
            ),
        )
