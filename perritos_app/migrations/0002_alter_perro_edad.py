# Generated by Django 5.1.2 on 2024-10-10 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perritos_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perro',
            name='edad',
            field=models.DecimalField(decimal_places=2, help_text='Ingresar la edad en años y meses', max_digits=4),
        ),
    ]
