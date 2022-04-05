from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='fruver-home'), # HomePage www.fruver.com/
    path('home/', views.home, name='fruver-home'), # HomePage www.fruver.com/
    path('login/', views.login, name='fruver-login'), #Acceso al sitio
    path('registro/', views.registro, name='fruver-registro'), #Registro de usuario
    path('frutas/', views.frutas, name='fruver-frutas'), #Sección de frutas a la venta
    path('verduras/', views.verduras, name='fruver-verduras'), #Sección de verduras a la venta
    path('carrito/', views.carrito, name='fruver-carrito'), #Productos en el carrito de compras
]