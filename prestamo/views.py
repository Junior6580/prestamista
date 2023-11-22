from datetime import date, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Abono
from .models import Prestamo
from .models import Cliente
from .form import AbonoForm, ClienteForm, PrestamoForm
from django.contrib import messages

@login_required 
def dashboard(request):
    return render(request, 'paginas/inicio.html', {'section': 'inicio'})


def inicio(request):
    return render(request, 'paginas/inicio.html', {'section': 'inicio'})


def clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/index.html', {'clientes': clientes})


def prestamos(request):
    clientes = Cliente.objects.all()
    prestamos = Prestamo.objects.all()
    return render(request, 'registros/index.html', {'prestamos': prestamos, 'clientes': clientes})


def nuevo_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente registrado')
            return redirect('clientes')
    else:
        form = ClienteForm()


def nuevo_prestamo(request):
    fecha_prestamo = request.POST['fecha_prestamo']
    fecha_fin = request.POST['fecha_fin']
    fecha_cuota = request.POST['fecha_cuota']
    prestamo = request.POST['prestamo']
    cantidad_cuotas = request.POST['cantidad_cuotas']
    tasa_interes = request.POST['tasa_interes']
    valor_cuota = request.POST['valor_cuota']
    debe = request.POST['debe']
    cliente_id = request.POST['cliente']  # Get the client ID from the form

    # Retrieve the Cliente instance using the ID
    cliente = Cliente.objects.get(id=cliente_id)

    prestamos = Prestamo.objects.create(
        fecha_prestamo=fecha_prestamo, fecha_fin=fecha_fin, prestamo=prestamo,
        cantidad_cuotas=cantidad_cuotas, tasa_interes=tasa_interes, valor_cuota=valor_cuota, debe=debe, fecha_cuota=fecha_cuota,
        cliente=cliente)  # Assign the Cliente instance
    messages.success(request, 'Prestamo registrado!')
    return redirect('prestamos')

def registrar_abono(request):
    clientes = Cliente.objects.all()
    abonos = Abono.objects.all()
    prestamos = Prestamo.objects.all()
    
    if request.method == 'POST':
        form = AbonoForm(request.POST)
        if form.is_valid():
            abono = form.save()
            abono.actualizar_deuda_y_pagado()
            messages.success(request, 'Abono registrado y deuda actualizada.')
            return redirect('prestamos')
    else:
        form = AbonoForm()

    return render(request, 'paginas/cuotas.html', {'prestamos': prestamos, 'form': form, 'clientes': clientes, 'abonos': abonos})


