# Generated by Django 4.2.3 on 2023-11-22 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prestamo', '0007_alter_prestamo_fecha_cuota_pago'),
    ]

    operations = [
        migrations.AddField(
            model_name='prestamo',
            name='estado',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='prestamo',
            name='fecha_cuota',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='prestamo',
            name='frecuencia_pago',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.DeleteModel(
            name='Pago',
        ),
    ]
