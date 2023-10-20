from django.shortcuts import render
from .models import Prestamo
from .models import Cliente

def inicio(request):
    return render(request, 'paginas/inicio.html')
def clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/index.html', {'clientes': clientes})
def prestamos(request):
    prestamos = Prestamo.objects.all()
    return render(request, 'registros/index.html', {'prestamos': prestamos})
def cuotas(request):
    return render(request, 'paginas/cuotas.html')



    


