from django.db import models



class GastoProductos(models.Model):
    fecha_gasto = models.DateField(auto_now_add=False)
    monto_frutas = models.IntegerField(default=0)
    monto_verduras = models.IntegerField(default=0)
    monto_bolsas = models.IntegerField(default=0)
    total_gastoproductos = models.IntegerField(default=0)
    otros_gastos = models.IntegerField(default=0)
    total_otrosgastos = models.IntegerField(default=0)
    total_dia = models.IntegerField(default=0)
    vendedor = models.ForeignKey('Home.Usuario', null=True, on_delete=models.SET_NULL)


class OtroGasto(models.Model):
    fecha_otrogasto = models.DateField(auto_now_add=True)
    nombre_otrogasto = models.CharField(max_length=50)
    monto_otrogasto = models.IntegerField(default=0)
    descripcion_otrogasto = models.TextField(max_length=350)
    main_gasto = models.ForeignKey('GastoProductos', null=True, on_delete=models.SET_NULL)
    vendedor = models.ForeignKey('Home.Usuario', null=True, on_delete=models.SET_NULL)

