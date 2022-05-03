from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import *
#from Productos.models import Producto
from datetime import datetime, timedelta


#Módulo de Gastos
@login_required(login_url='fruver-acceso')
def gastos(request):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')

    gastos = GastoProductos.objects.all()
    otros_gastos = OtroGasto.objects.all()
    form = FormularioGastoProductos()
    if request.method == 'POST':
        form = FormularioGastoProductos(request.POST)
        frutas = form.instance.monto_frutas
        verduras = form.instance.monto_verduras
        bolsas = form.instance.monto_bolsas
        if form.is_valid():
            form.instance.total_gasto = frutas + verduras + bolsas
            form.instance.vendedor = current_user
            form.save()
            messages.success(request, '¡Los gastos del día han sido registrados con éxito!')
            return redirect('fruver-gastos')
    context = {'form': form, 'gastos': gastos, 'otros_gastos': otros_gastos}
    return render(request, 'Gastos/gastos.html', context)