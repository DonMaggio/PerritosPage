from django.db import models

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
    edad=models.DecimalField(max_digits= 4, decimal_places=2, help_text='Ingresar la edad en años y meses')
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
    imagen = models.ImageField(upload_to='perritos_app/images')

    def __str__(self):
        return f'Foto de {self.perro.nombre}'