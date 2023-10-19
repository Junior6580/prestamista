from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    documento = models.CharField(max_length=20, unique=True)
    direccion = models.TextField()
    correo = models.EmailField(unique=True)

    def __str__(self):
        return self.nombre

class Prestamo(models.Model):
    fecha_prestamo = models.DateField()
    fecha_fin = models.DateField()
    prestamo = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_cuotas = models.PositiveIntegerField()
    tasa_interes = models.DecimalField(max_digits=5, decimal_places=2)
    debe = models.DecimalField(max_digits=10, decimal_places=2)
    pagado = models.DecimalField(max_digits=10, decimal_places=2)
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)

    def __str__(self):
        return f'Préstamo de {self.cliente.nombre}'

@receiver(post_migrate)
def create_initial_data(sender, **kwargs):
    if sender.name == 'prestamo':  # Reemplaza 'your_app_name' por el nombre de tu aplicación
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
            fecha_fin="2023-12-18",
            prestamo=1000.00,
            cantidad_cuotas=12,
            tasa_interes=0.05,
            debe=1000.00,
            pagado=0.00,
            cliente=cliente
        )

# Asegúrate de reemplazar 'your_app_name' con el nombre real de tu aplicación
