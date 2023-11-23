from django import forms
from .models import Abono, Cliente, Prestamo


class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = ['fecha_prestamo', 'fecha_cuota', 'frecuencia_pago', 'estado',
                  'prestamo', 'cantidad_cuotas', 'tasa_interes', 'valor_cuota', 'debe', 'pagado', 'cliente']


class AbonoForm(forms.ModelForm):
    class Meta:
        model = Abono
        fields = ['cliente', 'abono', 'fecha_abono']


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'documento', 'direccion', 'correo']
