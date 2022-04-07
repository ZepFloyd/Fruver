from django.db import models

# Create your models here.

class Comuna(models.Model):
    nombre_comuna = models.CharField(primary_key=True, max_length=30 )

class Usuario(models.Model):
    nombre_usuario = models.CharField(max_length=20)
    apellido_usuario = models.CharField(max_length=20)
    email_usuario = models.EmailField(max_length=30)
    password_usuario = models.CharField(max_length=12)
    telefono_usuario = models.CharField(max_length=12)
    domicilio_usuario = models.CharField(max_length=40)
    comuna = models.ForeignKey(Comuna, on_delete=models.DO_NOTHING)
    PERFIL_CHOICES = (
        ("Cliente", "Cliente"),
        ("Vendedor", "Vendedor"),
    )
    perfil_usuario = models.CharField(max_length=10, choices=PERFIL_CHOICES, default='Cliente')
