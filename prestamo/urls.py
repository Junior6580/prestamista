from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.contrib.staticfiles.urls import static


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('',views.inicio, name='inicio'),
    path('clientes', views.clientes, name='clientes'),
    path('nuevo_cliente/', views.nuevo_cliente, name='nuevo_cliente'),
    path('prestamos', views.prestamos, name='prestamos'),
    path('nuevo_prestamo/', views.nuevo_prestamo, name='nuevo_prestamo'),
    path('registrar_abono/', views.registrar_abono, name='registrar_abono'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
