from django.db import models
import os
from cloudinary.models import CloudinaryField
from cloudinary.uploader import destroy


from web_perritos import settings

GENERO_CHOICES = (
    (1, 'Macho'),
    (2, 'Hembra')
)

TALLA_CHOISES = (
    ('p', 'Pequeño'),
    ('m', 'Mediano'),
    ('g', 'Grande'),
)

# Create your models here.
class Perro(models.Model):
    nombre=models.CharField(max_length=100, help_text='Nombre completo del perrito')
    genero=models.PositiveSmallIntegerField(choices=GENERO_CHOICES, default='1', help_text='1-Macho, 2-Hembra')
    edad=models.DecimalField(max_digits= 2, decimal_places=0, help_text='Ingresar la edad en años')
    historia=models.TextField(max_length=1000, help_text='Ingrese una breve descripcion del perrito y su historia')
    talla=models.CharField(max_length=1, choices=TALLA_CHOISES, default='m', help_text='Ingresar la talla del perro')
    status = models.BooleanField(default=1, help_text='Habilitar si el perro está disponible para adoptar')

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Perro'
        verbose_name_plural = 'Perros'

class PerroFotos(models.Model):
    perro = models.ForeignKey(Perro, related_name='fotos', on_delete=models.CASCADE)
    #imagen = models.ImageField(upload_to='imagen')
    imagen = CloudinaryField('imagen', resource_type='image', blank=True, null=True)

    def __str__(self):
        return f'Foto de {self.perro.nombre}'
    
    def delete(self, *args, **kwargs):
        # Elimina el archivo del sistema de archivos antes de eliminar la instancia
        if self.imagen:
            public_id = self.imagen.public_id
            destroy(public_id)
            #file_path = os.path.join(settings.MEDIA_ROOT, self.imagen.name)
            #if os.path.exists(file_path):
            #    os.remove(file_path)
        super().delete(*args, **kwargs)