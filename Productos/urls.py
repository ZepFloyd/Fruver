from django.urls import path
from . import views

urlpatterns = [
    path('', views.productos, name='fruver-productos'), #Productos en el carrito de compras
    #path('mainmenu/', views.mainmenu, name='fruver-mainmenu'), #Menú principal para vendedor
]