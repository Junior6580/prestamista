# Generated by Django 4.2.3 on 2023-11-22 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prestamo', '0008_prestamo_estado_alter_prestamo_fecha_cuota_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prestamo',
            name='estado',
            field=models.CharField(choices=[('DEBE', 'Debe'), ('PAGADO', 'Pagado')], default='DEBE', max_length=10),
        ),
    ]
