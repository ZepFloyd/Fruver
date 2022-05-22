from django.db import models


class Producto(models.Model):
    nombre_producto = models.CharField(max_length=30)
    tipo_producto = models.CharField(max_length=20)
    precio_producto = models.PositiveIntegerField(default=0)
    modo_venta = models.CharField(max_length=30)
    stock_producto = models.PositiveIntegerField(default=0)
    descripcion_producto = models.TextField(max_length=350)
    imagen_producto = models.ImageField(null=False, blank=False)

    def __str__(self):
        return self.nombre_producto

