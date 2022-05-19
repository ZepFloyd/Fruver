from django.urls import path
from . import views

urlpatterns = [
    path('', views.reportes, name='fruver-reportes'), #Página para seleccionar los reportes a generar
    path('elegirfecha/<tipo_reporte>', views.elegirfecha, name='fruver-elegirfecha'), #Página para seleccionar la fecha de los reportes a generar
    path('reporteventas/<periodo>', views.reporteventas, name='fruver-reporteventas'), #Genera reporte de ventas para un período
    path('reportegastos/<periodo>', views.reportegastos, name='fruver-reportegastos'), #Genera reporte de gastos para un período
    path('reportecliente/<periodo>', views.reportecliente, name='fruver-reportecliente'), #Genera reporte de ventas por cliente
    path('pdfreporte/<tipo_reporte>', views.pdfreporte, name='fruver-pdfreporte'), #Genera documento .pdf con un informe de ventas, ventas por cliente, o gastos
]