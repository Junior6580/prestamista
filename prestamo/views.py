from datetime import date, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Abono
from .models import Prestamo
from .models import Cliente
from .form import AbonoForm, ClienteForm, PrestamoForm
from django.contrib import messages
from django.contrib.auth.models import User


@login_required
def dashboard(request):
    return render(request, 'paginas/inicio.html', {'section': 'inicio'})


def inicio(request):
    return render(request, 'paginas/inicio.html', {'section': 'inicio'})


def clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/index.html', {'clientes': clientes})


def usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'registros/users.html', {'usuarios': usuarios})


def prestamos(request):
    clientes = Prestamo.objects.all()
    prestamos = Prestamo.objects.all()
    return render(request, 'registros/index.html', {'prestamos': prestamos, 'clientes': clientes})


def nuevo_prestamo(request):
    clients_with_debe_loans = Prestamo.objects.filter(
        estado='debe').values_list('cliente_id', flat=True).distinct()
    clientes = Cliente.objects.exclude(id__in=clients_with_debe_loans)

    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Prestamo registrado')
            return redirect('prestamos')
    else:
        form = PrestamoForm()

    return render(request, 'registros/nuevo_prestamo.html', {'form': form, 'clientes': clientes})


def nuevo_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente registrado')
            return redirect('clientes')
    else:
        form = ClienteForm()


def registrar_abono(request):
    prestamos = Prestamo.objects.filter(estado='debe')
    clientes = Cliente.objects.filter(prestamo__in=prestamos).distinct()
    abonos = Abono.objects.all()

    if request.method == 'POST':
        form = AbonoForm(request.POST)
        if form.is_valid():
            # No guardes el abono en la base de datos aún
            abono = form.save(commit=False)
            
            # Obtén la deuda actual del cliente
            cliente = abono.cliente
            deuda_actual = sum(
                prestamo.debe for prestamo in cliente.prestamo_set.all())

            # Verifica si el abono es mayor que la deuda actual
            if abono.abono > deuda_actual:
                messages.error(
                    request, 'El abono no puede ser mayor que la deuda actual.')
                return redirect('registrar_abono')

            # Guarda el abono y actualiza la deuda
            abono.save()
            abono.actualizar_deuda_y_pagado()

            messages.success(request, 'Abono registrado y deuda actualizada.')
            return redirect('prestamos')
    else:
        form = AbonoForm()

    return render(request, 'paginas/cuotas.html', {'prestamos': prestamos, 'form': form, 'clientes': clientes, 'abonos': abonos})
