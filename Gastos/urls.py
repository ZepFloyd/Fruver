from django.urls import path
from . import views

urlpatterns = [
    path('', views.gastos, name='fruver-gastos'), #Listado de gastos de la empresa
]

