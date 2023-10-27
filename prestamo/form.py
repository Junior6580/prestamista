from django import forms
from .models import Abono, Prestamo

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = '__all__'


class AbonoForm(forms.ModelForm):
    class Meta:
        model = Abono
        fields = ['cliente', 'abono', 'fecha_abono']
        



