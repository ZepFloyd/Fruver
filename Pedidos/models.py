from django.db import models
#from Home.models import *


class Pedido(models.Model):
    fecha_pedido = models.DateField(auto_now_add=True)
    monto_pedido = models.IntegerField(default=0)
    medio_pago = models.CharField(max_length=30)
    estado_pedido = models.CharField(max_length=20)
    cliente = models.ForeignKey('Home.Usuario', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.estado_pedido
