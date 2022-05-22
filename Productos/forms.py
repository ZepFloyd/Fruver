from django.contrib.auth.forms import UserCreationForm
from django import forms
#from django.contrib.auth.models import User
from .models import Producto

# Create your forms here.

#formulario para guardar los datos de cuenta bancaria del vendedor, que después se muestra al cliente para que pague pedido con transferencia
class FormularioProducto(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'nombre_producto',
            'tipo_producto',
            'precio_producto',
            'modo_venta',
            'stock_producto',
            'descripcion_producto',
            'imagen_producto'
        ]

        TIPO_PRODUCTO_CHOICES = (('Fruta', 'Fruta'), ('Verdura', 'Verdura'))

        MODO_VENTA_CHOICES = (('Unidad', 'Unidad'), ('Kg', 'Kg'))

        widgets = {
            'tipo_producto': forms.Select(choices=TIPO_PRODUCTO_CHOICES, attrs={'class': 'form-control'}),
            'modo_venta': forms.RadioSelect(choices=MODO_VENTA_CHOICES, attrs={'class': 'form-control'})
        }

        
