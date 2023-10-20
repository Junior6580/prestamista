from django.urls import path
from . import views


urlpatterns = [
    path('',views.inicio, name='inicio'),
    path('clientes',views.clientes, name='clientes'),
    path('prestamos',views.prestamos, name='prestamos'),
    path('cuota del dia',views.cuotas, name='cuotas')
] 