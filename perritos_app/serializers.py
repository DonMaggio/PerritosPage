from rest_framework import serializers
from .models import Perro, PerroFotos

class PerroFotoSerizalizer(serializers.ModelSerializer):
    imagen = serializers.ImageField()

    class Meta:
        model = PerroFotos
        fields = '__all__'


class PerroListSerizalizer(serializers.ModelSerializer):
    primera_foto = serializers.SerializerMethodField()

    class Meta:
        model = Perro
        fields = '__all__'

    def get_primera_foto(self, obj):
        primera_foto = obj.fotos.first()
        if primera_foto:
            return {
                'id': primera_foto.id,
                'imagen': primera_foto.imagen.url
            }
        return None

class PerroDetailSerizalizer(serializers.ModelSerializer):
    fotos = PerroFotoSerizalizer(many=True, read_only=True)

    class Meta:
        model = Perro
        fields = '__all__'

