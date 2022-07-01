from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import *
from datetime import datetime, timedelta
import calendar



#Módulo de Gastos, muestra un listado con los gastos de la empresa
@login_required(login_url='fruver-acceso')
def gastos(request):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')
    #Generamos un dataset con todos los registros de la tabla GastoProductos, y los ordenamos por fecha
    gastos = GastoProductos.objects.all().order_by('fecha_gasto')
    #También generamos un dataset con todos los registros de la tabla OtroGasto
    otros_gastos = OtroGasto.objects.all()
    #Instanciamos un formulario para ingresar gastos de productos, y otro formulario para ingresar otros gastos asociados
    form = FormularioGastoProductos()
    form2 = FormularioOtroGasto()
    #Al recibir el método POST, se recogen desde el template html los datos para generar un registro de gastos de productos en la base de datos
    if request.method == 'POST':
        form = FormularioGastoProductos(request.POST)
        frutas = int(request.POST.get('monto_frutas'))
        verduras = int(request.POST.get('monto_verduras'))
        bolsas = int(request.POST.get('monto_bolsas'))
        fecha = request.POST.get('fecha')
        #Si los datos del formulario son válidos, se guarda el registro de gastos y se informa de ello al usuario
        if form.is_valid():
            form.instance.fecha_gasto = fecha
            form.instance.total_gastoproductos = frutas + verduras + bolsas
            form.instance.total_dia = frutas + verduras + bolsas
            form.instance.vendedor = current_user
            form.save()
            messages.success(request, '¡Los gastos fueron registrados con éxito!')
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
    #Instanciamos el gasto cuyo id corresponda al argumento id_gasto recibido por esta función
    gasto = GastoProductos.objects.get(pk=id_gasto)
    #Obtenemos el valor de otros gastos asociados al gasto principal, para sumarlos al total del día
    otros_gastos = gasto.total_otrosgastos
    #Generamos un formulario para editar los gastos de productos, mostrando los datos del registro al usuario
    form = FormularioGastoProductos(request.POST or None, instance=gasto)
    #Al recibir el método POST, los gastos de productos son asignados a variables para obtener los totales de gastos en productos y gastos del día, y luego se guardan los cambios
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
    


#Elimina un registro de gastos de productos
@login_required(login_url='fruver-acceso')
def eliminargasto(request, id_gasto):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')
    #Instanciamos el gasto de productos cuyo id corresponda al argumento id_gasto recibido por esta función 
    gasto = GastoProductos.objects.get(pk=id_gasto)
    #Obtenemos los otros gastos asociados al gasto de productos, ya que para mantener la integridad referencial en la base de datos, también deben eliminarse 
    otros_gastos = OtroGasto.objects.filter(main_gasto=id_gasto)
    #Mediante un ciclo for, eliminamos cada uno de los otros gastos asociados, y por último, eliminamos el gasto de productos llamando al método delete()
    for expense in otros_gastos:
        expense.delete()
    gasto.delete()
    messages.success(request,'El registro de gasto de productos, y sus otros gastos asociados han sido eliminados')
    return redirect('fruver-gastos')



#Registra otros gastos asociados a una fecha, esto es, asociados a un registro de gastos de productos
@login_required(login_url='fruver-acceso')
def ingresarotrosgastos(request, id_gasto):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')
    #Instanciamos el gastos de productos cuyo id corresponda al argumento id_gasto recibido por esta función
    main_expense = GastoProductos.objects.get(pk=id_gasto)
    #Obtenemos desde el template html los datos del otro gasto que se quiere registrar
    nombre = request.POST.get('nombre_otrogasto')
    monto = int(request.POST.get('monto_otrogasto'))
    descripcion = request.POST.get('descripcion_otrogasto')
    #Creamos el nuevo registro de otros gastos llamando al método create() y asignando los valores correspondientes
    otro_gasto = OtroGasto.objects.create(vendedor=current_user, main_gasto=main_expense, nombre_otrogasto=nombre, monto_otrogasto=monto, descripcion_otrogasto=descripcion)
    #Por último, actualizamos los valores dentro del gasto principal de la tabla de GastoProductos, para que tenga coherencia con el nuevo otro gasto recién creado
    main_expense.otros_gastos += 1 #Aumentamos en 1 la cantidad de otros gastos asociados
    main_expense.total_otrosgastos += monto #Sumamos el valor del otro gasto recién creado al total de otros gastos asociados a este gasto principal
    main_expense.total_dia += monto #Sumamos el valor del otro gasto recién creado al total del día
    main_expense.save()
    messages.success(request, '¡El gasto ha sido registrado con éxito!')
    return redirect('fruver-gastos')



#Muestra el detalle de otros gastos vinculados a un gasto de productos
@login_required(login_url='fruver-acceso')
def detalleotrosgastos(request, id_gastoproductos):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')
    #Instanciamos el gasto de productos cuyo id corresponda al argumento id_gastoproductos recibido por esta función
    gasto_productos = GastoProductos.objects.filter(pk=id_gastoproductos)
    product_expenses = GastoProductos.objects.get(pk=id_gastoproductos)
    #Obtenemos un dataset con todos los otros gastos asociados al gasto de productos recién instanciado
    otros_gastos = OtroGasto.objects.filter(main_gasto=product_expenses.id)
    #Si no hay ningún registro de otros gastos asociados al gasto de productos principal, informamos de ello al usuario y lo redirigimos al listado de gastos
    if not otros_gastos :
        messages.warning(request, 'No existen otros gastos asociados a esta fecha')
        return redirect('fruver-gastos')
    #Si hay registros de otros gastos asociados, los mostramos al usuario renderizando el template correspondiente
    else:   
        context = {'gasto_productos': gasto_productos, 'otros_gastos': otros_gastos}
        return render(request, 'Gastos/detalleotrosgastos.html', context)



#Elimina otros gastos asociados a una fecha, es decir, asociados a un registro de gastos de productos
@login_required(login_url='fruver-acceso')
def eliminarotrogasto(request, id_otrogasto):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')
    #Instanciamos el otro gasto que se requiere eliminar, usando el argumento id_otrogasto recibido por esta función
    otrogasto = OtroGasto.objects.get(pk=id_otrogasto)
    #Instanciamos el gasto de productos al que el otro gasto se encuentra asociado
    gasto = GastoProductos.objects.get(pk=otrogasto.main_gasto.id)
    #Quitamos el otro gasto que se quiere eliminar del registro del gasto principal, restando -1 a la cantidad de otros gastos,
    # y restando el valor del gasto a eliminar del total de otros gastos y del total del día
    gasto.otros_gastos -= 1
    gasto.total_otrosgastos -= otrogasto.monto_otrogasto
    gasto.total_dia -= otrogasto.monto_otrogasto
    gasto.save()
    #Por último, eliminamos el registro de otros gastos con el método delete() e informamos al usuario de ello
    otrogasto.delete()
    messages.success(request,'El registro del otro gasto asociado ha sido eliminado')
    return redirect('fruver-gastos')



#Filtra gastos por semana, mes o por un rango de fechas
@login_required(login_url='fruver-acceso')
def filtrargastos(request):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')
    #validamos si el POST pide un filtro de gastos por semana
    if request.method == 'POST' and request.POST.get('week') != None:
        year_week = request.POST.get("week") #recibe un string con el formato '2022-W11' desde el input week del html
        semana = year_week.rsplit("-W") #separamos el string year_week, generando una lista con 2 items tipo string: el año y el número de la semana
        #pasamos el año y el número de semana para generar un formato de fecha válido para el lunes y el domingo de la semana requerida
        lunes = datetime.strptime(semana[0]+"-"+semana[1]+'-1', "%Y-%W-%w")
        domingo = datetime.strptime(semana[0]+"-"+semana[1]+'-0', "%Y-%W-%w")
        #hacemos query sobre los registros cuya fecha esté en el rango lunes - domingo de la semana requerida y ordenamos el dataset según fecha
        gastos = GastoProductos.objects.filter(fecha_gasto__range=[lunes, domingo]).order_by('fecha_gasto')
        #si no hay gastos, enviamos un mensaje al usuario informando que no existen registros, y redirigimos a la página de todos los gastos
        if not gastos:
            messages.warning(request, 'No existen registros para el período consultado')
            return redirect('fruver-gastos')
    #validamos si el POST pide un filtro de gastos por mes
    elif request.method == 'POST' and request.POST.get('month') != None:
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
            if calendar.isleap(int(mes[0])) == False:
                fin = datetime.strptime(mes[0]+"-"+mes[1]+'-28', "%Y-%m-%d")
            elif calendar.isleap(int(mes[0])) == True:
                fin = datetime.strptime(mes[0]+"-"+mes[1]+'-29', "%Y-%m-%d")    
        #hacemos query sobre los registros cuya fecha esté en el rango inicio y fin del mes requerido y ordenamos el dataset según fecha
        gastos = GastoProductos.objects.filter(fecha_gasto__range=[inicio, fin]).order_by('fecha_gasto')
        #si no hay gastos, enviamos un mensaje al usuario informando que no existen registros, y redirigimos a la página de todos los gastos
        if not gastos:
            messages.warning(request, 'No existen registros para el período consultado')
            return redirect('fruver-gastos')
    #validamos si acaso el POST pide un filtro de gastos por rango de fechas
    elif request.method == 'POST' and request.POST.get('start') != None and request.POST.get('end') != None:
        inicio = request.POST.get("start") #recibe un string con el formato '2022-01-01' desde el input start del html
        fin = request.POST.get("end") #recibe un string con el formato '2022-01-01' desde el input end del html
        #hacemos query sobre los registros cuya fecha esté en el rango inicio - fin y ordenamos el dataset según fecha
        gastos = GastoProductos.objects.filter(fecha_gasto__range=[inicio, fin]).order_by('fecha_gasto')
        #si no hay gastos, enviamos un mensaje al usuario informando que no existen registros, y redirigimos a la página de todos los gastos
        if not gastos:
            messages.warning(request, 'No existen registros para el período consultado')
            return redirect('fruver-gastos')
    #luego de ejecutar el filtro solicitado por el usuario, instanciamos otros gastos y formularios para operar el resto de funcionalidades del módulo si así se requiere
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