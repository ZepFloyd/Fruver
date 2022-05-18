from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import *
#from Productos.models import Producto
from datetime import datetime, timedelta
import calendar


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



#Filtra gastos por semana
@login_required(login_url='fruver-acceso')
def filtrarsemana(request):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')
    if request.method == 'POST' and request.POST.get('week') != None:
        year_week = request.POST.get("week") #recibe un string con el formato '2022-W11' desde el input week del html
        semana = year_week.rsplit("-W") #separamos el string year_week, generando una lista con 2 items tipo string: el año y el número de la semana
        #pasamos el año y el número de semana para generar un formato de fecha válido para el lunes y el domingo de la semana requerida
        lunes = datetime.strptime(semana[0]+"-"+semana[1]+'-1', "%Y-%W-%w")
        domingo = datetime.strptime(semana[0]+"-"+semana[1]+'-0', "%Y-%W-%w")
        #hacemos query sobre los registros cuya fecha esté en el rango lunes - domingo de la semana requerida y ordenamos el dataset según fecha
        gastos = GastoProductos.objects.filter(fecha_gasto__range=[lunes, domingo]).order_by('fecha_gasto')
    otros_gastos = OtroGasto.objects.all()
    form = FormularioGastoProductos()
    form2 = FormularioOtroGasto()
    if request.method == 'POST' and request.POST.get('monto_frutas') != None:
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



#Filtra gastos por mes
@login_required(login_url='fruver-acceso')
def filtrarmes(request):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')
    if request.method == 'POST' and request.POST.get('month') != None:
        year_month = request.POST.get("month") #recibe un string con el formato '2022-05' desde el input month del html
        mes = year_month.rsplit("-") #separamos el string year_month, generando una lista con 2 items tipo string: el año y el número del mes
        #pasamos el año y el número del mes para generar 2 formatos de fecha válidos, inicio y fin de mes, para usarlos en el rango del query.
        #también nos aseguramos de que el fin de mes corresponda al último día del mes, según el mes requerido
        inicio = datetime.strptime(mes[0]+"-"+mes[1]+'-01', "%Y-%m-%d")
        if mes[1] == '01' or mes[1] == '03' or mes[1] == '05' or mes[1] == '07' or mes[1] == '08' or mes[1] == '10' or mes[1] == '12':
            fin = datetime.strptime(mes[0]+"-"+mes[1]+'-31', "%Y-%m-%d")
        elif mes[1] == '04' or mes[1] == '06' or mes[1] == '09' or mes[1] == '11':
            fin = datetime.strptime(mes[0]+"-"+mes[1]+'-30', "%Y-%m-%d")
        elif mes[1] == '02':
            #verificamos si el año es bisiesto o no con el módulo calendar de python, y fijamos el día en 28 o 29 según corresponda
            if calendar.is_leap(int(mes[0])) == False:
                fin = datetime.strptime(mes[0]+"-"+mes[1]+'-28', "%Y-%m-%d")
            elif calendar.is_leap(int(mes[0])) == True:
                fin = datetime.strptime(mes[0]+"-"+mes[1]+'-29', "%Y-%m-%d")    
        #hacemos query sobre los registros cuya fecha esté en el rango inicio y fin de del mes requerido y ordenamos el dataset según fecha
        gastos = GastoProductos.objects.filter(fecha_gasto__range=[inicio, fin]).order_by('fecha_gasto')
    otros_gastos = OtroGasto.objects.all()
    form = FormularioGastoProductos()
    form2 = FormularioOtroGasto()
    if request.method == 'POST' and request.POST.get('monto_frutas') != None:
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



#Filtra gastos por rango personalizado de fecha
@login_required(login_url='fruver-acceso')
def filtrarfechas(request):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')
    if request.method == 'POST' and request.POST.get('start') != None and request.POST.get('end') != None:
        inicio = request.POST.get("start") #recibe un string con el formato '2022-01-01' desde el input start del html
        fin = request.POST.get("end") #recibe un string con el formato '2022-01-01' desde el input end del html
        #hacemos query sobre los registros cuya fecha esté en el rango inicio - fin y ordenamos el dataset según fecha
        gastos = GastoProductos.objects.filter(fecha_gasto__range=[inicio, fin]).order_by('fecha_gasto')
    otros_gastos = OtroGasto.objects.all()
    form = FormularioGastoProductos()
    form2 = FormularioOtroGasto()
    if request.method == 'POST' and request.POST.get('monto_frutas') != None:
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
