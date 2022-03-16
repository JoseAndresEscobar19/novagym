from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Div, Field, Layout, Row
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from seguridad.models import *
from django.contrib.auth.models import Group


class UsuarioForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'groups']
        labels = {
            'groups': 'Rol',
            'username': 'Correo electrónico',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['groups'].required = False
        self.fields['username'].help_text = None
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='col-4'),
            ),
            Row(
                Column('password1', css_class='col-4'),
                Column('password2', css_class='col-4'),
            ),
        )


class UsuarioEditarForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'groups']
        labels = {
            'groups': 'Rol',
            'username': 'Correo electrónico',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['groups'].required = False
        self.fields['username'].help_text = None
        self.fields['groups'].help_text = None
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='col-6'),
            ),
        )


class UsuarioDetallesForm(forms.ModelForm):
    class Meta:
        model = UserDetails
        exclude = ('usuario',)
        labels = {
            'cedula': "Cédula",
            'nombres': "Nombres",
            'apellidos': "Apellidos",
            'telefono': "Teléfono",
            'telefono2': "Teléfono secundario",
            'direccion': "Dirección",
            'sexo': "Sexo",
            "imagen": "Foto de perfil",
            "fecha_nacimiento": "Fecha de nacimento",
        }
        fields = '__all__'
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
            'codigo',
            Row(
                Column('imagen', css_class='col-6'),
            ),
            Row(
                Column('cedula', css_class='col-6 col-xl-4'),
                Column('nombres', css_class='col-6 col-xl-4'),
                Column('apellidos', css_class='col-6 col-xl-4'),
                Column('fecha_nacimiento', css_class='col-6 col-xl-4'),
                Column('telefono', css_class='col-6 col-xl-4'),
                Column('sexo', css_class='col-6 col-xl-4'),
            ),
        )


class UsuarioFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.fields['usuario__email'].label = "Email del usuario"
        self.fields['cedula'].label = "Cédula"
        self.fields['nombres'].label = "Nombres"
        self.fields['apellidos'].label = "Apellidos"
        self.fields['sexo'].label = "Sexo"
        self.fields['created_at'].label = "Fecha de ingreso"
        self.fields['rol'].label = "Rol del usuario"
        self.helper.layout = Layout(
            Row(
                Column('usuario__email',
                       css_class='col-12 col-sm-6 col-md-4 col-lg-3'),
                Column(
                    'cedula', css_class='col-12 col-sm-6 col-md-4 col-lg-3'),
                Column('apellidos', css_class='col-12 col-sm-6 col-md-4 col-lg-3'),
                Column(
                    'nombres', css_class='col-12 col-sm-6 col-md-4 col-lg-3'),
            ),
            Row(
                Column('rol', css_class="col-12 col-sm-6 col-md-4 col-lg-3"),
                Column('sexo', css_class='col-12 col-sm-6 col-md-4 col-lg-3'),
                Column(
                    Field('created_at', template="forms/fields/range-filter.html",
                          css_class="form-control"), css_class='col-12 col-md-6 col-lg-3'
                ),
                Column(
                    StrictButton("Buscar", type='submit',
                                 css_class='btn btn-primary mt-1'),
                    css_class='col-12'
                )
            ),
        )

class ClienteFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.fields['usuario__email'].label = "Email del usuario"
        self.fields['cedula'].label = "Cédula"
        self.fields['nombres'].label = "Nombres"
        self.fields['apellidos'].label = "Apellidos"
        self.fields['sexo'].label = "Sexo"
        self.fields['created_at'].label = "Fecha de ingreso"
        self.helper.layout = Layout(
            Row(
                Column('usuario__email',
                       css_class='col-12 col-sm-6 col-md-4 col-lg-3'),
                Column(
                    'cedula', css_class='col-12 col-sm-6 col-md-4 col-lg-3'),
                Column('apellidos', css_class='col-12 col-sm-6 col-md-4 col-lg-3'),
                Column(
                    'nombres', css_class='col-12 col-sm-6 col-md-4 col-lg-3'),
            ),
            Row(
                Column(
                    Field('created_at', template="forms/fields/range-filter.html",
                          css_class="form-control"), css_class='col-12 col-md-6 col-lg-3'
                ),
                Column('sexo', css_class='col-12 col-sm-6 col-md-4 col-lg-3'),
                Column(
                    StrictButton("Buscar", type='submit',
                                 css_class='btn btn-primary mt-1'),
                    css_class='col-12'
                )
            ),
        )

class RolUsuarioForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name',)
        label = {
            'name': 'Nombre del rol'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-12 col-md-4'),
            ),
        )
