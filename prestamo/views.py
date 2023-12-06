from datetime import date, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Abono
from .models import Prestamo
from .models import Cliente
from .form import AbonoForm, ClienteForm, PrestamoForm
from django.contrib import messages
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


@login_required
def dashboard(request):
    return render(request, 'paginas/inicio.html', {'section': 'inicio'})


def inicio(request):
    return render(request, 'paginas/inicio.html', {'section': 'inicio'})


def clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/index.html', {'clientes': clientes})


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


def generate_pdf_cliente(request):
    # Create a buffer to receive PDF data.
    buffer = HttpResponse(content_type='application/pdf')
    buffer['Content-Disposition'] = 'attachment; filename="clientes.pdf"'

    # Create the PDF object, using the buffer as its "file."
    p = SimpleDocTemplate(buffer, pagesize=letter)

    # Create a list to store table data.
    data = [['ID', 'Nombre', 'Documento', 'Dirección', 'Correo']]

    # Query the data from the database
    clientes = Cliente.objects.all()

    for cliente in clientes:
        data.append([cliente.id, cliente.nombre, cliente.documento,
                    cliente.direccion, cliente.correo])

    # Create the table and style it.
    table = Table(data)
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    table.setStyle(style)

    # Add the table to the PDF document.
    elements = [table]

    # Build the PDF document and return it.
    p.build(elements)
    return buffer


def generate_pdf_prestamo(request):
    # Create a buffer to receive PDF data.
    buffer = HttpResponse(content_type='application/pdf')
    buffer['Content-Disposition'] = 'attachment; filename="Prestamos.pdf"'

    # Create the PDF object, using the buffer as its "file."
    p = SimpleDocTemplate(buffer, pagesize=letter)

    # Create a list to store table data.
    data = [['ID', 'Cliente ID', 'Fecha Prestamo', 'Fecha Cuota', 'Valor',
             'Cantidad cuotas', 'Frecuencia pago', 'Tasa Interes', 'Cuota', 'Debe', 'Pagado', 'Estado']]

    # Query the data from the database
    prestamos = Prestamo.objects.all()

    for prestamo in prestamos:
        data.append([prestamo.id, prestamo.cliente, prestamo.fecha_prestamo,
                    prestamo.fecha_cuota, prestamo.prestamo, prestamo.cantidad_cuotas, prestamo.frecuencia_pago,
                    prestamo.tasa_interes, prestamo.valor_cuota, prestamo.debe, prestamo.pagado, prestamo.estado])

    # Transpose the data to display the table horizontally
    data_transposed = list(map(list, zip(*data)))

    # Create the table and style it.
    table = Table(data_transposed)
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    table.setStyle(style)

    # Add the table to the PDF document.
    elements = [table]

    # Build the PDF document and return it.
    p.build(elements)
    return buffer
