from django.urls import path
from . import views

urlpatterns = [
    path('', views.gastos, name='fruver-gastos'), #Listado de gastos de la empresa
    path('filtrarsemana/', views.filtrarsemana, name='fruver-filtrarsemana'), #Filtra gastos por semana
    path('filtrarmes/', views.filtrarmes, name='fruver-filtrarmes'), #Filtra gastos por mes
    path('filtrarfechas/', views.filtrarfechas, name='fruver-filtrarfechas'), #Filtra gastos por rango de fecha personalizado
    path('editargasto/<id_gasto>', views.editargasto, name='fruver-editargasto'), #Edita un registro de gasto de productos
    path('eliminargasto/<id_gasto>', views.eliminargasto, name='fruver-eliminargasto'), #Elimina un registro de gasto de productos
    path('ingresarotrosgastos/<id_gasto>', views.ingresarotrosgastos, name='fruver-ingresarotrosgastos'), #Ingresa otros gastos
    path('detalleotrosgastos/<id_gastoproductos>', views.detalleotrosgastos, name='fruver-detalleotrosgastos'), #Muestra el detalle de otros gastos asociados a una fecha
]

