# Generated by Django 4.2.3 on 2023-10-27 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prestamo', '0003_prestamo_valor_cuota_alter_prestamo_debe_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prestamo',
            name='tasa_interes',
            field=models.TextField(),
        ),
    ]
