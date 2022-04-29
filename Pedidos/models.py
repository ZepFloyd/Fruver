from django.db import models
#from Home.models import *

#Tabla que almacena los pedidos de clientes. Tiene una llave foránea hacia tabla de usuario (cliente),
# y una relación N es a N (detalle_pedido) con la tabla Productos
class Pedido(models.Model):
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    monto_pedido = models.IntegerField(default=0)
    medio_pago = models.CharField(max_length=30, null=True)
    estado_pedido = models.CharField(max_length=20, null=True)
    cliente = models.ForeignKey('Home.Usuario', null=True, on_delete=models.SET_NULL)
    detalle_pedido = models.ManyToManyField('Productos.Producto', through='DetallePedido')

    def __str__(self):
        return 'Pedido de ' + str(self.cliente) + ' del ' + str(self.fecha_pedido.strftime('%d-%m-%Y')) + ' a las ' + str(self.fecha_pedido.strftime('%H:%M:%S')) + ' hrs.'


#Tabla auxiliar intermedia entre Pedido y Productos para manejar la relación N:N
class DetallePedido(models.Model):
    pedido = models.ForeignKey('Pedido', on_delete=models.DO_NOTHING)
    producto = models.ForeignKey('Productos.Producto', on_delete=models.DO_NOTHING)
    precio_producto = models.IntegerField(default=0)
    modo_venta = models.CharField(max_length=30, null=True)
    cantidad_producto = models.IntegerField(default=0)
    subtotal = models.IntegerField(default=0)

    def __str__(self):
        return str(self.pedido) + ' Item: ' + str(self.producto) + ' ' + str(self.cantidad_producto) + ' ' + self.modo_venta
