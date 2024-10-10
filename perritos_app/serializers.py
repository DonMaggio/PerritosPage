from rest_framework import serializers
from .models import Perro, PerroFotos

class PerroFotoSerizalizer(serializers.ModelSerializer):
    class Meta:
        model = PerroFotos
        fields = ['imagen']


class PerroSerizalizer(serializers.ModelSerializer):
    fotos = PerroFotoSerizalizer(many=True, read_only=True)

    class Meta:
        model = Perro
        fields = '__all__'

