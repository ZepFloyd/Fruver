from django.urls import path
from . import views

urlpatterns = [
    path('', views.clientes, name='fruver-clientes'), #Módulo de Clientes
    path('editarcliente/<usuario_id>', views.editarcliente, name='fruver-editarcliente'), #editar datos de clientes
    path('eliminarcliente/<usuario_id>', views.eliminarcliente, name='fruver-eliminarcliente'), #elimina un cliente
    path('perfilcliente/', views.perfilcliente, name='fruver-perfilcliente'), #perfil de cliente
    path('actualizardatos/', views.actualizardatos, name='fruver-actualizardatos'), #actualiza datos del cliente actual
    path('mispedidos/', views.mispedidos, name='fruver-mispedidos'), #muestra los pedidos del cliente actual
    path('mipedido/<pedido_id>', views.mipedido, name='fruver-mipedido'), #muestra el detalle de un pedido seleccionado
]