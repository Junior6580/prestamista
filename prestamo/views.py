from django.shortcuts import render
from .models import Prestamo

def inicio(request):
    return render(request, 'paginas/inicio.html')
def nosotros(request):
    return render(request, 'paginas/nosotros.html')
def prestamos(request):
    prestamos = Prestamo.objects.all()
    return render(request, 'registros/index.html', {'prestamos': prestamos})



    


