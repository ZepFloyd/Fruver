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
    path('mainmenu/', views.mainmenu, name='fruver-mainmenu'), #Menú principal para vendedor
    path('mainmenu/datosbanco/', views.datosbanco, name='fruver-datosbanco'), #Ingresar datos bancarios del vendedor
    path('mainmenu/gestionarvendedor', views.gestionarvendedor, name='fruver-gestionarvendedor'), #Gestionar CRUD de vendedores
    path('mainmenu/gestionarvendedor/editarvendedor/<usuario_id>', views.editarvendedor, name='fruver-editarvendedor'), #editar datos de vendedores
    path('mainmenu/gestionarvendedor/eliminarvendedor/<usuario_id>', views.eliminarvendedor, name='fruver-eliminarvendedor'), #elimina un vendedor de la base de datos
]