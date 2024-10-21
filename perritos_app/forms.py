from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Perro, PerroFotos

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


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

    def clean_file_field(self):
        files = self.files.getlist('file_field')
        if not files or len(files) == 0:
            raise forms.ValidationError("Debes subir al menos una imagen.")
        return files