from django.contrib import admin
from .models import Cliente, Abono, Prestamo  # Asegúrate de importar tus modelos

admin.site.register(Cliente)
admin.site.register(Abono)
admin.site.register(Prestamo)
