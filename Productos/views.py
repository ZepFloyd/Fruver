from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *

# Create your views here.

#Accede a la lista de productos a la venta
@login_required(login_url='fruver-acceso')
def productos(request):
    return render(request, 'Productos/productos.html')


