# Generated by Django 5.1.2 on 2024-10-15 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perritos_app', '0003_remove_perro_fotos_alter_perro_status_perrofotos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perro',
            name='talla',
            field=models.CharField(choices=[('p', 'Pequeño'), ('m', 'Mediano'), ('g', 'Grande')], default='m', help_text='Ingresar la talla del perro', max_length=1),
        ),
    ]