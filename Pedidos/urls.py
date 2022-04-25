from django.urls import path
from . import views

urlpatterns = [
    path('', views.pedidos, name='fruver-pedidos'), #Listado de pedidos activos hechos por clientes
    path('frutas/', views.frutas, name='fruver-frutas'), #Sección de frutas a la venta
    path('verduras/', views.verduras, name='fruver-verduras'), #Sección de verduras a la venta
    path('carrito/', views.carrito, name='fruver-carrito'), #Productos en el carrito de compras
    path('hacerpedido/', views.hacerpedido, name='fruver-hacerpedido'), #Muestra página para la confirmación y realización del pedido
    path('agregarproducto/<producto_id>', views.agregarproducto, name='fruver-agregarproducto'), #Agrega productos al carrito de compras
    path('eliminarproducto/<producto_id>', views.eliminarproducto, name='fruver-eliminarproducto'), #elimina productos del carrito de compras
    path('restarproducto/<producto_id>', views.restarproducto, name='fruver-restarproducto'), #quita 1 Kg/unidad del carrito de compras
    path('sumarproducto/<producto_id>', views.sumarproducto, name='fruver-sumarproducto'), #suma 1 Kg/unidad del carrito de compras
    path('limpiarcarrito/', views.limpiarcarrito, name='fruver-limpiarcarrito'), #limpia el carrito de compras
    #path('mainmenu/', views.mainmenu, name='fruver-mainmenu'), #Menú principal para vendedor
]