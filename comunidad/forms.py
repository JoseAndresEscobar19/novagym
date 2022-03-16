from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row

from django import forms
from django.forms.widgets import FileInput
from django.forms.models import inlineformset_factory

from .models import Publicacion, ArchivoPublicacion


class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = ['texto']
        labels = {
            'texto': 'Contenido de la publicación'
        }
        widgets = {
            'texto': forms.Textarea(attrs={'rows':4, 'cols':15})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['texto'].required = True
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('texto', css_class='col-8'),
            ),
        )
    

class ArchivoPublicacionForm(forms.ModelForm):
    class Meta:
        model = ArchivoPublicacion
        fields = ['archivo']
        widgets = {
            'archivo': forms.FileInput(attrs={'multiple': True, 'accept': 'image/*, audio/*, video/*'}),
        }

    
        


ArchivoFormSet = inlineformset_factory(Publicacion, ArchivoPublicacion, form=ArchivoPublicacionForm, fields=('archivo',), extra=1, can_delete=False)