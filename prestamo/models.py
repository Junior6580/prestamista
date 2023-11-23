from datetime import timedelta
from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from dateutil.relativedelta import relativedelta


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    documento = models.CharField(max_length=20, unique=True)
    direccion = models.TextField()
    correo = models.EmailField(unique=True)

    def __str__(self):
        return self.nombre


class Abono(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    abono = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_abono = models.DateField()

    def __str__(self):
        return f'Abono de {self.cliente.nombre} - {self.fecha_abono}'

    def actualizar_deuda_y_pagado(self):
        # Actualizar la cantidad pagada
        prestamos = self.cliente.prestamo_set.all()
        prestamos.update(pagado=models.F('pagado') + self.abono)

        # Calcular la deuda restante y actualizar la fecha de la próxima cuota
        for prestamo in prestamos:
            prestamo.debe = prestamo.prestamo - prestamo.pagado
            prestamo.actualizar_fecha_proxima_cuota()

            # Check if the debt is zero or negative
            if prestamo.debe <= 0:
                prestamo.estado = 'Pagado'  # Update the state to 'Pagado'

        # Guardar el cliente y los préstamos actualizados
        self.cliente.save()

class Prestamo(models.Model):
    fecha_prestamo = models.DateField()
    fecha_cuota = models.DateField(null=True, blank=True)
    frecuencia_pago = models.CharField(max_length=20, null=True, blank=True)
    estado = models.CharField(max_length=10, default='Debe')
    prestamo = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_cuotas = models.PositiveIntegerField()
    tasa_interes = models.TextField()
    valor_cuota = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    debe = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pagado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)

    def __str__(self):
        return f'Préstamo de {self.cliente.nombre}'
    def actualizar_fecha_proxima_cuota(self):
        if self.fecha_cuota:
            # Calcula la próxima fecha de cuota basándose en la frecuencia de pago
            if self.frecuencia_pago == 'diario':
                delta = relativedelta(days=1)
            elif self.frecuencia_pago == 'ocho_dias':
                delta = relativedelta(days=8)
            elif self.frecuencia_pago == 'quince_dias':
                delta = relativedelta(days=15)
            elif self.frecuencia_pago == 'mensual':
                delta = relativedelta(months=1)
            else:
                return None

            # Calcula la próxima fecha de cuota sumando el delta a la última fecha de cuota
            self.fecha_cuota += delta
            self.save()


@receiver(post_migrate)
def create_initial_data(sender, **kwargs):
    if sender.name == 'prestamo':
        # Crea un cliente
        cliente = Cliente.objects.create(
            nombre="Junior Medina",
            documento="1079173785",
            direccion="Parcela 12 ",
            correo="jsmedina@gmail.com"
        )

        # Crea un préstamo relacionado con el cliente
        prestamo = Prestamo.objects.create(
            fecha_prestamo="2023-10-18",
            fecha_cuota="2023-12-18",
            prestamo=1000.00,
            cantidad_cuotas=12,
            tasa_interes=0.05,
            valor_cuota=85.5,
            debe=1027.32,
            pagado=0.00,
            cliente=cliente
        )

# Asegúrate de reemplazar 'your_app_name' con el nombre real de tu aplicación
