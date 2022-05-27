from django.urls import path
from . import views

urlpatterns = [
    path('', views.productos, name='fruver-productos'), #Módulo de Productos
    path('adminproductos/<tipo_producto>', views.adminproductos, name='fruver-adminproductos'), #Página para administrar Productos
    path('crearproducto/<tipo_producto>', views.crearproducto, name='fruver-crearproducto'), #Página para crear nuevos Productos
    path('editarproducto/<id_producto>', views.editarproducto, name='fruver-editarproducto'), #Página para editar datos de Productos
    path('suprimirproducto/<id_producto>/<tipo_producto>', views.suprimirproducto, name='fruver-suprimirproducto'), #Elimina Productos de la base de datos
    #path('mainmenu/', views.mainmenu, name='fruver-mainmenu'), #Menú principal para vendedor
]