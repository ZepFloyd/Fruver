from django import forms
from . models import GastoProductos, OtroGasto



#formulario para crear registro de gastos del día (la fecha se genera automáticamente)
class FormularioGastoProductos(forms.ModelForm):
    class Meta:
        model = GastoProductos
        fields = [
            'monto_frutas',
            'monto_verduras',
            'monto_bolsas',
            'total_gasto',
            'vendedor'
        ]
