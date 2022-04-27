from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, nombre_usuario, apellido_usuario, email_usuario, password, telefono_usuario, domicilio_usuario, comuna, **other_fields):
        
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('superuser debe ser asignado is_staff=True')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('superuser debe ser asignado is_superuser=True')

        return self.create_user(nombre_usuario, apellido_usuario, email_usuario, password, telefono_usuario, domicilio_usuario, comuna, **other_fields)


    def create_user(self, nombre_usuario, apellido_usuario, email_usuario, password, telefono_usuario, domicilio_usuario, comuna, **other_fields):

        if not email_usuario:
            raise ValueError(_('Debe ingresar un e-mail válido'))
        email_usuario = self.normalize_email(email_usuario)
        user = self.model(
            nombre_usuario=nombre_usuario,
            apellido_usuario=apellido_usuario,
            email_usuario=email_usuario,
            password=password,
            telefono_usuario=telefono_usuario,
            domicilio_usuario=domicilio_usuario,
            comuna=comuna,
            **other_fields
        )
        user.set_password(password)
        user.save()
        return user


class Usuario(AbstractBaseUser, PermissionsMixin):
    nombre_usuario = models.CharField(max_length=30)
    apellido_usuario = models.CharField(max_length=30)
    email_usuario = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=18)
    telefono_usuario = models.CharField(max_length=12)
    domicilio_usuario = models.CharField(max_length=50)
    comuna = models.CharField(max_length=40)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email_usuario'
    REQUIRED_FIELDS = ['nombre_usuario', 'apellido_usuario', 'password', 'telefono_usuario', 'domicilio_usuario', 'comuna']

    def __str__(self):
        return self.nombre_usuario


class CuentaBancaria(models.Model):
    titular = models.CharField(max_length=40)
    rut = models.CharField(max_length=12)
    banco = models.CharField(max_length=30)
    tipo_cuenta = models.CharField(max_length=20)
    numero_cuenta = models.CharField(max_length=40)
    email = models.CharField(max_length=50)

    def __str__(self):
        return 'Cuenta N° '+self.numero_cuenta+' de '+self.titular




#class Comuna(models.Model):
#    nombre_comuna = models.CharField(primary_key=True, max_length=40)


