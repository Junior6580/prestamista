from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Prestamo
from .models import Cliente
from .form import PrestamoForm
from django.contrib import messages


def inicio(request):
    return render(request, 'paginas/inicio.html')
def clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/index.html', {'clientes': clientes})
def prestamos(request):
    clientes = Cliente.objects.all()
    prestamos = Prestamo.objects.all()
    return render(request, 'registros/index.html', {'prestamos': prestamos, 'clientes': clientes})



def nuevo_prestamo(request):
    fecha_prestamo = request.POST['fecha_prestamo']
    fecha_fin = request.POST['fecha_fin']
    prestamo = request.POST['prestamo']
    cantidad_cuotas = request.POST['cantidad_cuotas']
    tasa_interes = request.POST['tasa_interes']
    debe = request.POST['debe']
    cliente_id = request.POST['cliente']  # Get the client ID from the form

    # Retrieve the Cliente instance using the ID
    cliente = Cliente.objects.get(id=cliente_id)

    prestamos = Prestamo.objects.create(
        fecha_prestamo=fecha_prestamo, fecha_fin=fecha_fin, prestamo=prestamo, 
        cantidad_cuotas=cantidad_cuotas, tasa_interes=tasa_interes, debe=debe, 
        cliente=cliente)  # Assign the Cliente instance
    messages.success(request, 'Prestamo registrado!')
    return redirect('prestamos')



def cuotas(request):
    return render(request, 'paginas/cuotas.html')





    


