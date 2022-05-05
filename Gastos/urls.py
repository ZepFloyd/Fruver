from django.urls import path
from . import views

urlpatterns = [
    path('', views.gastos, name='fruver-gastos'), #Listado de gastos de la empresa
    path('ingresarotrosgastos/<id_gasto>', views.ingresarotrosgastos, name='fruver-ingresarotrosgastos'), #Ingresa otros gastos
]

