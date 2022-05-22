from django.urls import path
from . import views

urlpatterns = [
    path('', views.productos, name='fruver-productos'), #Módulo de Productos
    path('adminproductos/<tipo_producto>', views.adminproductos, name='fruver-adminproductos'), #Página para administrar Productos
    path('agregarproducto/<tipo_producto>', views.agregarproducto, name='fruver-agregarproducto'), #Página para agregar nuevos Productos
    path('editarproducto/<id_producto>', views.editarproducto, name='fruver-editarproducto'), #Página para editar datos de Productos
    path('eliminarproducto/<id_producto>', views.eliminarproducto, name='fruver-eliminarproducto'), #Elimina Productos
    #path('mainmenu/', views.mainmenu, name='fruver-mainmenu'), #Menú principal para vendedor
]