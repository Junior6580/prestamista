from django.urls import path
from . import views


urlpatterns = [
    path('',views.inicio, name='inicio'),
    path('clientes',views.clientes, name='clientes'),
    path('nuevo_cliente/',views.nuevo_cliente, name='nuevo_cliente'),
    path('prestamos',views.prestamos, name='prestamos'),
    path('nuevo_prestamo/',views.nuevo_prestamo, name='nuevo_prestamo'),
    path('cuota del dia',views.cuotas, name='cuotas'),
    path('registrar_abono/', views.registrar_abono, name='registrar_abono')
    
] 