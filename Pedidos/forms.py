from django.contrib.auth.forms import UserCreationForm
from django import forms
#from django.contrib.auth.models import User
from .models import Pedido

# Create your forms here.

#formulario para seleccionar medio de pago antes de confirmar un pedido
class FormularioCrearPedido(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = [
            'medio_pago',
            'estado_pedido',
            'cliente',
            'monto_pedido'
        ]

        MEDIO_PAGO_CHOICES = (
            ('Efectivo', 'Efectivo'),
            ('Transferencia', 'Transferencia'),
            ('Tarjeta Crédito/Débito', 'Tarjeta Crédito/Débito')
            )

        widgets = {
            'medio_pago': forms.Select(choices=MEDIO_PAGO_CHOICES, attrs={'class': 'form-control'})
        }