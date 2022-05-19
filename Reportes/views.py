from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime, timedelta
from .models import *
from Home.models import *
from Pedidos.models import *
from Gastos.models import *
import calendar
#Módulos para exportar a .pdf
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas


#Módulo de Reportes
@login_required(login_url='fruver-acceso')
def reportes(request):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')

    context = {}
    return render(request, 'Reportes/reportes.html', context)



#Página para seleccionar la fecha requerida para el reporte
@login_required(login_url='fruver-acceso')
def elegirfecha(request, tipo_reporte):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')

    clientes = Usuario.objects.filter(is_staff=0).order_by('nombre_usuario')
    context = {'tipo_reporte': tipo_reporte, 'clientes': clientes}
    return render(request, 'Reportes/elegirfecha.html', context)



#Genera reporte de ventas
@login_required(login_url='fruver-acceso')
def reporteventas(request, periodo):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')

    #filtramos los registros en función del período: semana, mes o rango de fechas
    if periodo=='semana':
        year_week = request.POST.get("week") #recibe un string con el formato '2022-W11' desde el input week del html
        semana = year_week.rsplit("-W") #separamos el string year_week, generando una lista con 2 items tipo string: el año y el número de la semana
        #pasamos el año y el número de semana para generar un formato de fecha válido para el lunes y el domingo de la semana requerida
        inicio = datetime.strptime(semana[0]+"-"+semana[1]+'-1', "%Y-%W-%w")
        fin = datetime.strptime(semana[0]+"-"+semana[1]+'-0', "%Y-%W-%w")
        #hacemos query sobre los registros cuya fecha esté en el rango lunes - domingo de la semana requerida y ordenamos el dataset según fecha
        ventas = Pedido.objects.filter(fecha_pedido__range=[inicio, fin]).order_by('fecha_pedido')
    elif periodo=='mes':
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
        #hacemos query sobre los registros cuya fecha esté en el rango inicio y fin de del mes requerido y ordenamos el dataset según fecha
        ventas = Pedido.objects.filter(fecha_pedido__range=[inicio, fin]).order_by('fecha_pedido')
    elif periodo=='rangofecha':
        start = request.POST.get("start") #recibe un string con el formato '2022-01-01' desde el input start del html
        end = request.POST.get("end") #recibe un string con el formato '2022-01-01' desde el input end del html
        #hacemos query sobre los registros cuya fecha esté en el rango inicio - fin y ordenamos el dataset según fecha
        ventas = Pedido.objects.filter(fecha_pedido__range=[start, end]).order_by('fecha_pedido')
        inicio = datetime.strptime(start, '%Y-%m-%d')
        fin = datetime.strptime(end, '%Y-%m-%d')

    #Validamos que existan registros para el período consultado
    #Si no hay registros, enviamos un mensaje para informar al usuario y redirijimos a la selección de fecha
    if not ventas:
        messages.warning(request, 'No existen ventas registradas para el período consultado.')
        return redirect('/reportes/elegirfecha/'+'ventas')
    #Si hay registros realizamos los cálculos para generar el reporte
    else:    
        #calculamos el total de ventas
        total_ventas = 0
        cantidad_ventas = 0
        for venta in ventas:
            total_ventas = total_ventas + venta.monto_pedido
            cantidad_ventas = cantidad_ventas + 1
        #calculamos cantidad y porcentaje de pagos hechos en efectivo, con transferencias, y con tarjetas
        total_efectivo = 0
        cantidad_efectivo = 0
        porcentaje_efectivo = 0.0
        total_transferencias = 0
        cantidad_transferencias = 0
        porcentaje_transferencias = 0.0
        total_tarjetas = 0
        cantidad_tarjetas = 0
        porcentaje_tarjetas = 0.0
        for venta in ventas:
            if venta.medio_pago == 'Efectivo':
                total_efectivo = total_efectivo + venta.monto_pedido
                cantidad_efectivo = cantidad_efectivo + 1
                porcentaje_efectivo = "{:.2f}".format((cantidad_efectivo*100)/cantidad_ventas)
            elif venta.medio_pago == 'Transferencia':
                total_transferencias = total_transferencias + venta.monto_pedido
                cantidad_transferencias = cantidad_transferencias + 1
                porcentaje_transferencias = "{:.2f}".format((cantidad_transferencias*100)/cantidad_ventas)
            elif venta.medio_pago == 'Tarjeta Crédito/Débito':
                total_tarjetas = total_tarjetas + venta.monto_pedido
                cantidad_tarjetas = cantidad_tarjetas + 1
                porcentaje_tarjetas = "{:.2f}".format((cantidad_tarjetas*100)/cantidad_ventas)

        inicio = inicio.strftime("%d-%m-%Y")
        fin = fin.strftime("%d-%m-%Y")
        context = {'inicio': inicio, 'fin': fin, 'ventas': ventas, 'total_ventas': total_ventas, 'cantidad_ventas':cantidad_ventas,
                    'total_efectivo':total_efectivo, 'cantidad_efectivo':cantidad_efectivo, 'porcentaje_efectivo': porcentaje_efectivo,
                    'total_transferencias':total_transferencias, 'cantidad_transferencias': cantidad_transferencias, 'porcentaje_transferencias': porcentaje_transferencias,
                    'total_tarjetas':total_tarjetas, 'cantidad_tarjetas': cantidad_tarjetas, 'porcentaje_tarjetas': porcentaje_tarjetas}
        return render(request, 'Reportes/reporteventas.html', context)



#Genera reporte de ventas por cliente
@login_required(login_url='fruver-acceso')
def reportecliente(request, periodo):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')

    id = int(request.POST.get('customer'))
    customer = Usuario.objects.get(pk=id)

    #filtramos los registros en función del período: semana, mes o rango de fechas
    if periodo=='semana':
        year_week = request.POST.get("week") #recibe un string con el formato '2022-W11' desde el input week del html
        semana = year_week.rsplit("-W") #separamos el string year_week, generando una lista con 2 items tipo string: el año y el número de la semana
        #pasamos el año y el número de semana para generar un formato de fecha válido para el lunes y el domingo de la semana requerida
        inicio = datetime.strptime(semana[0]+"-"+semana[1]+'-1', "%Y-%W-%w")
        fin = datetime.strptime(semana[0]+"-"+semana[1]+'-0', "%Y-%W-%w")
        #hacemos query sobre los registros cuya fecha esté en el rango lunes - domingo de la semana requerida y ordenamos el dataset según fecha
        ventas = Pedido.objects.filter(cliente=id, fecha_pedido__range=[inicio, fin]).order_by('fecha_pedido')
    elif periodo=='mes':
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
        #hacemos query sobre los registros cuya fecha esté en el rango inicio y fin de del mes requerido y ordenamos el dataset según fecha
        ventas = Pedido.objects.filter(cliente=id, fecha_pedido__range=[inicio, fin]).order_by('fecha_pedido')
    elif periodo=='rangofecha':
        start = request.POST.get("start") #recibe un string con el formato '2022-01-01' desde el input start del html
        end = request.POST.get("end") #recibe un string con el formato '2022-01-01' desde el input end del html
        #hacemos query sobre los registros cuya fecha esté en el rango inicio - fin y ordenamos el dataset según fecha
        ventas = Pedido.objects.filter(cliente=id, fecha_pedido__range=[start, end]).order_by('fecha_pedido')
        inicio = datetime.strptime(start, '%Y-%m-%d')
        fin = datetime.strptime(end, '%Y-%m-%d')
    
    #Validamos que existan registros para el período consultado
    #Si no hay registros, enviamos un mensaje para informar al usuario y redirijimos a la selección de fecha
    if not ventas:
        messages.warning(request, 'El cliente no registra ventas para el período consultado.')
        return redirect('/reportes/elegirfecha/'+'cliente')
    #Si hay registros realizamos los cálculos para generar el reporte
    else:  
        #calculamos el total de ventas
        total_ventas = 0
        cantidad_ventas = 0
        for venta in ventas:
            total_ventas = total_ventas + venta.monto_pedido
            cantidad_ventas = cantidad_ventas + 1
        #calculamos cantidad y porcentaje de pagos hechos en efectivo, con transferencias, y con tarjetas
        total_efectivo = 0
        cantidad_efectivo = 0
        porcentaje_efectivo = 0.0
        total_transferencias = 0
        cantidad_transferencias = 0
        porcentaje_transferencias = 0.0
        total_tarjetas = 0
        cantidad_tarjetas = 0
        porcentaje_tarjetas = 0.0
        for venta in ventas:
            if venta.medio_pago == 'Efectivo':
                total_efectivo = total_efectivo + venta.monto_pedido
                cantidad_efectivo = cantidad_efectivo + 1
                porcentaje_efectivo = "{:.2f}".format((cantidad_efectivo*100)/cantidad_ventas)
            elif venta.medio_pago == 'Transferencia':
                total_transferencias = total_transferencias + venta.monto_pedido
                cantidad_transferencias = cantidad_transferencias + 1
                porcentaje_transferencias = "{:.2f}".format((cantidad_transferencias*100)/cantidad_ventas)
            elif venta.medio_pago == 'Tarjeta Crédito/Débito':
                total_tarjetas = total_tarjetas + venta.monto_pedido
                cantidad_tarjetas = cantidad_tarjetas + 1
                porcentaje_tarjetas = "{:.2f}".format((cantidad_tarjetas*100)/cantidad_ventas)

        inicio = inicio.strftime("%d-%m-%Y")
        fin = fin.strftime("%d-%m-%Y")
        context = {'customer': customer, 'inicio': inicio, 'fin': fin, 'ventas': ventas, 'total_ventas': total_ventas, 'cantidad_ventas':cantidad_ventas,
                    'total_efectivo':total_efectivo, 'cantidad_efectivo':cantidad_efectivo, 'porcentaje_efectivo': porcentaje_efectivo,
                    'total_transferencias':total_transferencias, 'cantidad_transferencias': cantidad_transferencias, 'porcentaje_transferencias': porcentaje_transferencias,
                    'total_tarjetas':total_tarjetas, 'cantidad_tarjetas': cantidad_tarjetas, 'porcentaje_tarjetas': porcentaje_tarjetas}
        return render(request, 'Reportes/reportecliente.html', context)



#Genera reporte de gastos
@login_required(login_url='fruver-acceso')
def reportegastos(request, periodo):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')

    #filtramos los registros en función del período: semana, mes o rango de fechas
    if periodo=='semana':
        year_week = request.POST.get("week") #recibe un string con el formato '2022-W11' desde el input week del html
        semana = year_week.rsplit("-W") #separamos el string year_week, generando una lista con 2 items tipo string: el año y el número de la semana
        #pasamos el año y el número de semana para generar un formato de fecha válido para el lunes y el domingo de la semana requerida
        inicio = datetime.strptime(semana[0]+"-"+semana[1]+'-1', "%Y-%W-%w")
        fin = datetime.strptime(semana[0]+"-"+semana[1]+'-0', "%Y-%W-%w")
        #hacemos query sobre los registros cuya fecha esté en el rango lunes - domingo de la semana requerida y ordenamos el dataset según fecha
        gastos = GastoProductos.objects.filter(fecha_gasto__range=[inicio, fin]).order_by('fecha_gasto')
    elif periodo=='mes':
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
        #hacemos query sobre los registros cuya fecha esté en el rango inicio y fin de del mes requerido y ordenamos el dataset según fecha
        gastos = GastoProductos.objects.filter(fecha_gasto__range=[inicio, fin]).order_by('fecha_gasto')
    elif periodo=='rangofecha':
        start = request.POST.get("start") #recibe un string con el formato '2022-01-01' desde el input start del html
        end = request.POST.get("end") #recibe un string con el formato '2022-01-01' desde el input end del html
        #hacemos query sobre los registros cuya fecha esté en el rango inicio - fin y ordenamos el dataset según fecha
        gastos = GastoProductos.objects.filter(fecha_gasto__range=[start, end]).order_by('fecha_gasto')
        inicio = datetime.strptime(start, '%Y-%m-%d')
        fin = datetime.strptime(end, '%Y-%m-%d')

    #Validamos que existan registros para el período consultado
    #Si no hay registros, enviamos un mensaje para informar al usuario y redirijimos a la selección de fecha
    if not gastos:
        messages.warning(request, 'No existen gastos registrados para el período consultado.')
        return redirect('/reportes/elegirfecha/'+'gastos')
    #Si hay registros realizamos los cálculos para generar el reporte
    else:  
        #calculamos el total de gastos
        total_frutas = 0
        total_verduras = 0
        total_bolsas = 0
        total_gastoproductos = 0
        total_otrosgastos = 0
        total_gastos = 0
        for gasto in gastos:
            total_frutas = total_frutas + gasto.monto_frutas
            total_verduras = total_verduras + gasto.monto_verduras
            total_bolsas = total_bolsas + gasto.monto_bolsas
            total_gastoproductos = total_gastoproductos + gasto.total_gastoproductos
            total_otrosgastos = total_otrosgastos + gasto.total_otrosgastos
            total_gastos = total_gastos + gasto.total_dia

        inicio = inicio.strftime("%d-%m-%Y")
        fin = fin.strftime("%d-%m-%Y")
        context = {'inicio': inicio, 'fin': fin, 'gastos': gastos,
                'total_frutas': total_frutas, 'total_verduras': total_verduras, 'total_bolsas': total_bolsas, 'total_gastoproductos':total_gastoproductos,
                'total_otrosgastos':total_otrosgastos, 'total_gastos': total_gastos,}
        return render(request, 'Reportes/reportegastos.html', context)



#Genera documento reporteventas.pdf
@login_required(login_url='fruver-acceso')
def pdfreporte(request, tipo_reporte):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')
    
    #instrucciones obtenidas desde la documentación de Django en: https://docs.djangoproject.com/en/3.2/howto/outputting-pdf/
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    # Create the PDF object, using the buffer as its "file."
    reporte = canvas.Canvas(buffer)

    if tipo_reporte == 'ventas' or tipo_reporte == 'cliente':
        #obtenemos los datos para el reporte a través del POST recibido desde reporteventas.html 
        titulo = request.POST.get('title')
        if tipo_reporte == 'cliente':
            cliente = request.POST.get('customer')
        subtitulo = request.POST.get('subtitle')
        efectivo_titulo = request.POST.get('cash-title')
        efectivo_cantidad = request.POST.get('cash-quantity')
        efectivo_monto = request.POST.get('cash-amount')
        efectivo_porcentaje = request.POST.get('cash-percentage')
        transferencia_titulo = request.POST.get('transfer-title')
        transferencia_cantidad = request.POST.get('transfer-quantity')
        transferencia_monto = request.POST.get('transfer-amount')
        transferencia_porcentaje = request.POST.get('transfer-percentage')
        tarjeta_titulo = request.POST.get('card-title')
        tarjeta_cantidad = request.POST.get('card-quantity')
        tarjeta_monto = request.POST.get('card-amount')
        tarjeta_porcentaje = request.POST.get('card-percentage')
        periodo_transacciones = request.POST.get('period-transactions')
        periodo_total = request.POST.get('period-total')
        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        #Una hoja A4 está constituida por 595.2 puntos de ancho (width) y 841.8 puntos de alto (height)
        if tipo_reporte == 'ventas':
            reporte.drawString(238.08, 820, titulo)
        elif tipo_reporte == 'cliente':
            reporte.drawString(198.4, 820, titulo)
        reporte.drawString(148.8, 800, subtitulo)
        if tipo_reporte == 'cliente':
            reporte.drawString(20, 790, cliente)
        reporte.drawString(20, 780, '------------------------------------------------------------------------------------------------------------------------------------------')
        reporte.drawString(20, 760, efectivo_titulo)
        reporte.drawString(20, 740, '------------------------------------------------------------------------------------------------------------------------------------------')
        reporte.drawString(20, 720, efectivo_cantidad)
        reporte.drawString(20, 700, efectivo_monto)
        reporte.drawString(20, 680, efectivo_porcentaje)
        reporte.drawString(20, 660, '------------------------------------------------------------------------------------------------------------------------------------------')
        reporte.drawString(20, 640, transferencia_titulo)
        reporte.drawString(20, 620, '------------------------------------------------------------------------------------------------------------------------------------------')
        reporte.drawString(20, 600, transferencia_cantidad)
        reporte.drawString(20, 580, transferencia_monto)
        reporte.drawString(20, 560, transferencia_porcentaje)
        reporte.drawString(20, 540, '------------------------------------------------------------------------------------------------------------------------------------------')
        reporte.drawString(20, 520, tarjeta_titulo)
        reporte.drawString(20, 500, '------------------------------------------------------------------------------------------------------------------------------------------')
        reporte.drawString(20, 480, tarjeta_cantidad)
        reporte.drawString(20, 460, tarjeta_monto)
        reporte.drawString(20, 440, tarjeta_porcentaje)
        reporte.drawString(20, 420, '------------------------------------------------------------------------------------------------------------------------------------------')
        reporte.drawString(20, 400, periodo_transacciones)
        reporte.drawString(20, 380, periodo_total)
    elif tipo_reporte == 'gastos':
        #obtenemos los datos para el reporte a través del POST recibido desde reporteventas.html 
        titulo = request.POST.get('title')
        subtitulo = request.POST.get('subtitle')
        frutas = request.POST.get('fruits')
        verduras = request.POST.get('vegetables')
        bolsas = request.POST.get('bags')
        gasto_productos = request.POST.get('products-expenses')
        otros_gastos = request.POST.get('other-expenses')
        periodo_total = request.POST.get('period-total')
        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        #Una hoja A4 está constituida por 595.2 puntos de ancho (width) y 841.8 puntos de alto (height)
        reporte.drawString(238.08, 820, titulo)
        reporte.drawString(148.8, 800, subtitulo)
        reporte.drawString(20, 780, '------------------------------------------------------------------------------------------------------------------------------------------')
        reporte.drawString(20, 760, frutas)
        reporte.drawString(20, 740, verduras)
        reporte.drawString(20, 720, bolsas)
        reporte.drawString(20, 700, gasto_productos)
        reporte.drawString(20, 680, '------------------------------------------------------------------------------------------------------------------------------------------')
        reporte.drawString(20, 660, otros_gastos)
        reporte.drawString(20, 640, '------------------------------------------------------------------------------------------------------------------------------------------')
        reporte.drawString(20, 620, periodo_total)
    
    # Close the PDF object cleanly, and we're done.
    reporte.showPage()
    reporte.save()
    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    #asignamos un nombre al reporte dependiendo del tipo de datos que contenga
    if tipo_reporte == 'ventas':
        nombrepdf = 'Reporte Ventas.pdf'
    elif tipo_reporte == 'cliente':
        nombrepdf = 'Reporte Ventas por Cliente.pdf'
    elif tipo_reporte == 'gastos':
        nombrepdf = 'Reporte Gastos.pdf'
    return FileResponse(buffer, as_attachment=True, filename=nombrepdf)