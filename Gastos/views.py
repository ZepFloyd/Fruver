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

    gastos = GastoProductos.objects.all().order_by('fecha_gasto')
    otros_gastos = OtroGasto.objects.all()

    form = FormularioGastoProductos()
    form2 = FormularioOtroGasto()
    if request.method == 'POST':
        form = FormularioGastoProductos(request.POST)
        frutas = int(request.POST.get('monto_frutas'))
        verduras = int(request.POST.get('monto_verduras'))
        bolsas = int(request.POST.get('monto_bolsas'))
        fecha = request.POST.get('fecha')
        if form.is_valid():
            form.instance.fecha_gasto = fecha
            form.instance.total_gastoproductos = frutas + verduras + bolsas
            form.instance.total_dia = frutas + verduras + bolsas
            form.instance.vendedor = current_user
            form.save()
            messages.success(request, '¡Los gastos del día '+fecha+' han sido registrados con éxito!')
            return redirect('fruver-gastos')
    context = {'form': form, 'form2': form2, 'gastos': gastos, 'otros_gastos': otros_gastos}
    return render(request, 'Gastos/gastos.html', context)



#Editar gasto de productos
@login_required(login_url='fruver-acceso')
def editargasto(request, id_gasto):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')
    gasto = GastoProductos.objects.get(pk=id_gasto)
    otros_gastos = gasto.total_otrosgastos
    form = FormularioGastoProductos(request.POST or None, instance=gasto)
    if request.method == 'POST':
        frutas = int(request.POST.get('monto_frutas'))
        verduras = int(request.POST.get('monto_verduras'))
        bolsas = int(request.POST.get('monto_bolsas'))
        if form.is_valid():
            form.instance.total_gastoproductos = frutas + verduras + bolsas
            form.instance.total_dia = frutas + verduras + bolsas + otros_gastos
            form.instance.vendedor = current_user
            form.save()
            messages.success(request, '¡Gastos actualizados con éxito!')
            return redirect('fruver-gastos')
    context = {'gasto': gasto, 'form': form}
    return render(request, 'Gastos/editargasto.html', context)
    


#Editar gasto de productos
@login_required(login_url='fruver-acceso')
def eliminargasto(request, id_gasto):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')
    
    gasto = GastoProductos.objects.get(pk=id_gasto)
    otros_gastos = OtroGasto.objects.filter(main_gasto=id_gasto)
    for expense in otros_gastos:
        expense.delete()
    gasto.delete()
    messages.success(request,'El registro de gasto de productos, y sus otros gastos asociados han sido eliminados')
    return redirect('fruver-gastos')



#Registrar otros de Gastos
@login_required(login_url='fruver-acceso')
def ingresarotrosgastos(request, id_gasto):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')
    
    main_expense = GastoProductos.objects.get(pk=id_gasto)
    nombre = request.POST.get('nombre_otrogasto')
    monto = int(request.POST.get('monto_otrogasto'))
    descripcion = request.POST.get('descripcion_otrogasto')
    otro_gasto = OtroGasto.objects.create(vendedor=current_user, main_gasto=main_expense, nombre_otrogasto=nombre, monto_otrogasto=monto, descripcion_otrogasto=descripcion)
    main_expense.otros_gastos += 1
    main_expense.total_otrosgastos += monto
    main_expense.total_dia += monto
    main_expense.save()
    messages.success(request, '¡El gasto ha sido registrado con éxito!')
    return redirect('fruver-gastos')



#Ver detalle de otros gastos vinculados a un gasto
@login_required(login_url='fruver-acceso')
def detalleotrosgastos(request, id_gastoproductos):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')

    gasto_productos = GastoProductos.objects.filter(pk=id_gastoproductos)
    product_expenses = GastoProductos.objects.get(pk=id_gastoproductos)
    otros_gastos = OtroGasto.objects.filter(main_gasto=product_expenses.id)    
    context = {'gasto_productos': gasto_productos, 'otros_gastos': otros_gastos}
    return render(request, 'Gastos/detalleotrosgastos.html', context)