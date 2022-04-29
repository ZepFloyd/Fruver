from django.contrib.auth.forms import UserCreationForm
from django import forms
#from django.contrib.auth.models import User
from .models import Usuario, CuentaBancaria

# Create your forms here.

#formulario para registrar usuario cliente y crear vendedores
class FormularioCrearUsuario(UserCreationForm):
    class Meta:
        model = Usuario
        fields = [
            'nombre_usuario',
            'apellido_usuario',
            'email_usuario',
            'password1',
            'password2',
            'telefono_usuario',
            'domicilio_usuario',
            'comuna',
            'is_staff'  #por defecto seteado False. No se muestra en la plantilla .html, solo sirve para setearlo True al crear un vendedor
        ]
        
        COMUNA_CHOICES = (
            ('Cerrillos', 'Cerrillos'),
            ('Cerro Navia', 'Cerro Navia'),
            ('Conchalí', 'Conchalí'),
            ('El Bosque', 'El Bosque'),
            ('Estación Central', 'Estación Central'),
            ('Huechuraba', 'Huechuraba'),
            ('Independencia', 'Independencia'),
            ('La Cisterna', 'La Cisterna'),
            ('La Florida', 'La Florida'),
            ('La Granja', 'La Granja'),
            ('La Pintana', 'La Pintana'),
            ('La Reina', 'La Reina'),
            ('Las Condes', 'Las Condes'),
            ('Lo Barnechea', 'Lo Barnechea'),
            ('Lo Espejo', 'Lo Espejo'),
            ('Lo Prado', 'Lo Prado'),
            ('Macul', 'Macul'),
            ('Maipú', 'Maipú'),
            ('Ñuñoa', 'Ñuñoa'),
            ('Padre Hurtado', 'Padre Hurtado'),
            ('Pedro Aguirre Cerda', 'Pedro Aguirre Cerda'),
            ('Peñalolén', 'Peñalolén'),
            ('Providencia', 'Providencia'),
            ('Pudahuel', 'Pudahuel'),
            ('Puente Alto', 'Puente Alto'),
            ('Quilicura', 'Quilicura'),
            ('Quinta Normal', 'Quinta Normal'),
            ('Recoleta', 'Recoleta'),
            ('Renca', 'Renca'),
            ('San Bernardo', 'San Bernardo'),
            ('San Joaquín', 'San Joaquín'),
            ('San Miguel', 'San Miguel'),
            ('San Ramón', 'San Ramón'),
            ('Santiago', 'Santiago'),
            ('Vitacura', 'Vitacura')
            )

        widgets = {
            'comuna': forms.Select(choices=COMUNA_CHOICES, attrs={'class': 'form-control'})
        }

        #fields = ['username', 'email', 'password1', 'password2']

#formulario para actualizar datos de vendedor
class FormularioEditarVendedor(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'nombre_usuario',
            'apellido_usuario',
            'email_usuario',
            'telefono_usuario',
            'domicilio_usuario',
            'comuna'
        ]
        
        COMUNA_CHOICES = (
            ('Cerrillos', 'Cerrillos'),
            ('Cerro Navia', 'Cerro Navia'),
            ('Conchalí', 'Conchalí'),
            ('El Bosque', 'El Bosque'),
            ('Estación Central', 'Estación Central'),
            ('Huechuraba', 'Huechuraba'),
            ('Independencia', 'Independencia'),
            ('La Cisterna', 'La Cisterna'),
            ('La Florida', 'La Florida'),
            ('La Granja', 'La Granja'),
            ('La Pintana', 'La Pintana'),
            ('La Reina', 'La Reina'),
            ('Las Condes', 'Las Condes'),
            ('Lo Barnechea', 'Lo Barnechea'),
            ('Lo Espejo', 'Lo Espejo'),
            ('Lo Prado', 'Lo Prado'),
            ('Macul', 'Macul'),
            ('Maipú', 'Maipú'),
            ('Ñuñoa', 'Ñuñoa'),
            ('Padre Hurtado', 'Padre Hurtado'),
            ('Pedro Aguirre Cerda', 'Pedro Aguirre Cerda'),
            ('Peñalolén', 'Peñalolén'),
            ('Providencia', 'Providencia'),
            ('Pudahuel', 'Pudahuel'),
            ('Puente Alto', 'Puente Alto'),
            ('Quilicura', 'Quilicura'),
            ('Quinta Normal', 'Quinta Normal'),
            ('Recoleta', 'Recoleta'),
            ('Renca', 'Renca'),
            ('San Bernardo', 'San Bernardo'),
            ('San Joaquín', 'San Joaquín'),
            ('San Miguel', 'San Miguel'),
            ('San Ramón', 'San Ramón'),
            ('Santiago', 'Santiago'),
            ('Vitacura', 'Vitacura')
            )

        widgets = {
            'comuna': forms.Select(choices=COMUNA_CHOICES, attrs={'class': 'form-control'})
        }


#formulario para guardar los datos de cuenta bancaria del vendedor, que después se muestra al cliente para que pague pedido con transferencia
class FormularioCuentaBancaria(forms.ModelForm):
    class Meta:
        model = CuentaBancaria
        fields = [
            'titular',
            'rut',
            'banco',
            'tipo_cuenta',
            'numero_cuenta',
            'email'
        ]

