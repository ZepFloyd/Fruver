from django.contrib.auth.forms import UserCreationForm
from django import forms
#from django.contrib.auth.models import User
from Home.models import Usuario



#formulario para actualizar datos de cliente
class FormularioEditarCliente(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'nombre_usuario',
            'apellido_usuario',
            'email_usuario',
            'telefono_usuario',
            'domicilio_usuario',
            'comuna',
            'is_active',
        ]

        IS_ACTIVE_CHOICES = ((True, 'Activo'), (False, 'Inactivo'))
        
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
            'comuna': forms.Select(choices=COMUNA_CHOICES, attrs={'class': 'form-control'}),
            'is_active': forms.RadioSelect(choices=IS_ACTIVE_CHOICES, attrs={'class': 'form-control'}),
        }


