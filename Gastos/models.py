from django.db import models



class GastoProductos(models.Model):
    fecha_gasto = models.DateField(auto_now_add=True)
    monto_frutas = models.IntegerField(default=0)
    monto_verduras = models.IntegerField(default=0)
    monto_bolsas = models.IntegerField(default=0)
    total_gasto = models.IntegerField(default=0)
    vendedor = models.ForeignKey('Home.Usuario', null=True, on_delete=models.SET_NULL)


class OtroGasto(models.Model):
    fecha_gasto = models.DateField(auto_now_add=True)
    nombre_gasto = models.CharField(max_length=50)
    monto_gasto = models.IntegerField(default=0)
    descripcion_gasto = models.TextField(max_length=350)
    vendedor = models.ForeignKey('Home.Usuario', null=True, on_delete=models.SET_NULL)

