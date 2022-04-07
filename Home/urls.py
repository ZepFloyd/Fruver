from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='fruver-home'), # HomePage www.fruver.com/
   #path('home/', views.home, name='fruver-home'), # HomePage www.fruver.com/
    path('acceso/', views.acceso, name='fruver-acceso'), #Acceso al sitio
    path('salir/', views.salir, name='fruver-salir'), #Acceso al sitio
    path('registro/', views.registro, name='fruver-registro'), #Registro de usuario
    path('frutas/', views.frutas, name='fruver-frutas'), #Sección de frutas a la venta
    path('verduras/', views.verduras, name='fruver-verduras'), #Sección de verduras a la venta
    path('carrito/', views.carrito, name='fruver-carrito'), #Productos en el carrito de compras
    path('mainmenu/', views.mainmenu, name='fruver-mainmenu'), #Menú principal para vendedor
    path('registerPage/', views.registerPage, name='fruver-registerPage'),
    path('mainmenu/datosbanco', views.datosbanco, name='fruver-datosbanco'), #Ingresar datos bancarios del vendedor 
]