from django.contrib.auth.forms import UserCreationForm
from django import forms
#from django.contrib.auth.models import User
from .models import Pedido

# Create your forms here.

#formulario para seleccionar medio de pago antes de confirmar un pedido
class FormularioOrdenarProductos(forms.Form):
    class Meta:
        fields = forms.ChoiceField(choices=(
            ('precio_producto', 'Precio menor a mayor'),
            ('precio_producto', 'Precio mayor a menor'),
            ('nombre_producto', 'Orden alfabético'),
            ('stock_producto', 'Stock disponible'),
            ))

        widgets = forms.Select(attrs={'onchange': 'submit();'})