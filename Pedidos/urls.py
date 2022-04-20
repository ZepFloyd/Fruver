from django.urls import path
from . import views

urlpatterns = [
    path('carrito/', views.carrito, name='fruver-carrito'), #Productos en el carrito de compras
    path('', views.pedidos, name='fruver-pedidos'), #Listado de pedidos activos hechos por clientes
    #path('mainmenu/', views.mainmenu, name='fruver-mainmenu'), #Menú principal para vendedor
]