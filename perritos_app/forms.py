from django import forms

from .models import Perro, PerroFotos

class PerrosForm(forms.ModelForm):
    class Meta:
        model = Perro
        fields = [
            'nombre',
            'genero',
            'edad',
            'historia',
            'talla',
            'status',
        ]

#class PerroFotosForm(forms.Form):
#    imagen = forms.FileField(
#        label='Image',
#        widget=forms.ClearableFileInput(attrs={"multiple": True}),
#    )

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

class PerroFotosForm(forms.Form):
    file_field = MultipleFileField()