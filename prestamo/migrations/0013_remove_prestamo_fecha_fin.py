# Generated by Django 4.2.3 on 2023-11-23 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prestamo', '0012_alter_prestamo_frecuencia_pago'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prestamo',
            name='fecha_fin',
        ),
    ]
