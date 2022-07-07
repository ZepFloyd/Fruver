from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
import locale
from django.db.models import Count
from .forms import *
from .models import *
from Pedidos.models import *



#Accede al módulo de Productos
@login_required(login_url='fruver-acceso')
def productos(request):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')
    return render(request, 'Productos/productos.html')



#Accede a la lista de productos registrados en el sistema
@login_required(login_url='fruver-acceso')
def adminproductos(request, tipo_producto):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')
    #Mediante el argumento tipo_producto recibido por esta función, filtramos los productos para mostrar ya sea la lista de frutas o de verduras
    if tipo_producto == 'Fruta':
        productos = Producto.objects.filter(tipo_producto='Fruta').order_by('nombre_producto')
    elif tipo_producto == 'Verdura':
        productos = Producto.objects.filter(tipo_producto='Verdura').order_by('nombre_producto')
    #Luego pasamos los productos al return de la función para acceder a ellos desde el template html
    #También pasamos el tipo_producto para poder hacer las operaciones deseadas con los productos, y volver a la página previa de forma coherente
    context = {'productos': productos, 'tipo_producto': tipo_producto}
    return render(request, 'Productos/adminproductos.html', context)



#Crea nuevos Productos
@login_required(login_url='fruver-acceso')
def crearproducto(request, tipo_producto):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')
    #Generamos un formulario para ingresar los datos del producto a crear
    form = FormularioProducto()
    #Al recibir el método POST, asignamos los datos y el archivo de imagen a los campos del formulario
    #También obtenemos el tipo_producto para volver a la página previa que corresponda, frutas o verduras
    if request.method == 'POST':
        form = FormularioProducto(request.POST, request.FILES)
        tipo_producto = request.POST.get('tipo_producto')
        #Si los datos del formulario son válidos, guardamos el producto e informamos al usuario de ello, redirigiendo a la lista de frutas o verduras según corresponda
        if form.is_valid():
            form.save()
            messages.success(request, '¡Producto registrado con éxito!')
            return redirect('/productos/adminproductos/'+tipo_producto)
    context = {'form': form, 'tipo_producto': tipo_producto}
    return render(request, 'Productos/crearproducto.html', context)



#Edita datos de Productos
@login_required(login_url='fruver-acceso')
def editarproducto(request, id_producto):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')
    #Instanciamos el producto cuyo id corresponda al argumento id_producto recibido por esta función
    producto = Producto.objects.get(pk=id_producto)
    #Generamos un formulario para ingresar los datos que se requiera cambiar, mostrando también los datos actuales del producto en cada campo
    form = FormularioProducto(request.POST or None, request.FILES or None, instance=producto)
    #Al recibir el método POST, validamos los datos ingresados, y guardamos los cambios
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, '¡Los cambios fueron guardados con éxito!')
            return redirect('/productos/editarproducto/'+id_producto)
    context = {'form': form, 'producto': producto}
    return render(request, 'Productos/editarproducto.html', context)



#Elimina productos de la base de datos. Esta acción sólo se lleva a cabo si el producto no está incluido en ningún pedido, para mantener la integridad referencial 
@login_required(login_url='fruver-acceso')
def suprimirproducto(request, id_producto, tipo_producto):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')
    #Obtenemos el producto a eliminar haciendo un query con la id del producto
    producto = Producto.objects.get(pk=id_producto)
    #Verificamos si el producto está incluido en algún pedido, haciendo query en la tabla DetallePedido, 
    # en donde la columna "producto" tenga ocurrencias del producto que queremos eliminar
    detalle = DetallePedido.objects.filter(producto=id_producto)
    #Si hay ocurrencias, es decir, si el producto está contenido en alguno de los pedidos hechos por clientes, no eliminamos e informamos al usuario de ello
    if detalle:
        #En el cuadro de diálogo emergente se indica al usuario que puede cambiar el estado del producto a inactivo, para que no se muestre en la sección de ventas
        messages.warning(request, 'Acción de Riesgo')
        return redirect('/productos/adminproductos/'+tipo_producto)
    #Si el producto no está en ningún pedido, eliminamos
    else:
        producto.delete()
        messages.success(request, 'El producto ha sido eliminado correctamente')
        return redirect('/productos/adminproductos/'+tipo_producto)



#Muestra estadísticas de los productos: productos más vendidos y cantidades
@login_required(login_url='fruver-acceso')
def estadisticaproducto(request):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')
    #Mediante la librería de Python locale, seteamos el formato de fecha para mostrarse en idioma español
    locale.setlocale(locale.LC_TIME, 'es_ES')
    #Obtenemos la fecha actual mediante la librería datetime
    mes = datetime.now()
    #Damos formato a la fecha para mostrar solo el nombre del mes. Esto servirá para mostrarse en la página a renderizar
    mes = mes.strftime('%B de %Y')
    #Declaramos un diccionario para almacenar las frutas, y otro para las verduras. Esto servirá de base para generar los gráficos
    frutas = {}
    verduras = {}
    #Obtenemos un dataset con todos los productos incluidos en los pedidos registrados. Con esto sabremos qué productos se han vendido
    queryset = DetallePedido.objects.all().order_by('producto')
    #Si no hay registros de ventas, informamos al usuario
    if not queryset.exists():
        messages.warning(request, 'No existen registros de ventas disponibles para generar estadísticas')
        return redirect('fruver-productos')
    #Luego recorremos el dataset con un ciclo for para separar frutas y verduras
    for registro in queryset:
        #Si el tipo de producto es una fruta
        if registro.producto.tipo_producto == 'Fruta':
            #Si la fruta no se encuentra aún incluida en nuestro diccionario, la incluimos usando el nombre como llave, y una lista de 2 items como valor: cantidades y montos vendidos
            if registro.producto.nombre_producto not in frutas.keys():
                cantidad = 0
                monto = 0
                frutas[registro.producto.nombre_producto] = [cantidad + registro.cantidad_producto, monto + registro.subtotal]
            #Si la fruta ya se encuentra en el diccionario, sólo actualizamos la cantidad y el monto
            elif registro.producto.nombre_producto in frutas.keys():
                cantidad = frutas[registro.producto.nombre_producto][0]
                monto = frutas[registro.producto.nombre_producto][1]
                frutas[registro.producto.nombre_producto] = [cantidad + registro.cantidad_producto, monto + registro.subtotal]
        #Si el tipo de producto es una verdura
        elif registro.producto.tipo_producto == 'Verdura':
            #Si la verdura no se encuentra aún incluida en nuestro diccionario, la incluimos usando el nombre como llave, y una lista de 2 items como valor: cantidades y montos vendidos
            if registro.producto.nombre_producto not in verduras.keys():
                cantidad = 0
                monto = 0
                verduras[registro.producto.nombre_producto] = [cantidad + registro.cantidad_producto, monto + registro.subtotal]
            #Si la verdura ya se encuentra en el diccionario, sólo actualizamos la cantidad y el monto
            elif registro.producto.nombre_producto in verduras.keys():
                cantidad = verduras[registro.producto.nombre_producto][0]
                monto = verduras[registro.producto.nombre_producto][1]
                verduras[registro.producto.nombre_producto] = [cantidad + registro.cantidad_producto, monto + registro.subtotal]
    #Luego, declaramos 3 listas, una para cantidades, una para montos y otra para etiquetas de los productos, las que utilizaremos para generar los gráficos con Chart.js
    #Primero, las frutas
    frutadata = []
    frutaventas = []
    frutalabels = []
    #Con un ciclo for, recorremos el diccionario y añadimos el nombre del producto a la lista de etiquetas, la cantidad vendida a la lista de datos y los montos a frutaventas
    #También convertimos los montos de miles (pesos) a unidades, para poder mostrarlos correctamente en conjunto con las cantidades dentro del mismo gráfico
    for name, quantity in frutas.items():
        frutalabels.append(name)
        frutadata.append(quantity[0])
        frutaventas.append(round(quantity[1]*0.001, 2))
    #Con el método max() de Python, buscamos el valor más grande en la lista de datos. La mayor cantidad equivale al producto más vendido
    frutamax = max(frutadata)
    #Conociendo la fruta más vendida, recorremos el diccionario con un ciclo for para obtener su nombre y el monto vendido
    for key, value in frutas.items():
        for elemento in value:
            if elemento == frutamax:
                #Al hallar la fruta más vendida dentro del diccionario, asignamos a variables su nombre, cantidad y monto vendidos, para mostrarlo en el template html
                nom = key
                quantite = elemento
                somme = frutas[nom][1]
    #Luego, realizamos las mismas operaciones para las verduras
    #Declaramos una lista para los datos, una para los montos y otra para las etiquetas
    verduradata = []
    verduraventas = []
    verduralabels = []
    #Con un ciclo for, recorremos el diccionario y añadimos el nombre del producto a la lista de etiquetas, la cantidad vendida a la lista de datos y los montos a verduraventas
    #También convertimos los montos de miles (pesos) a unidades, para poder mostrarlos correctamente en conjunto con las cantidades dentro del mismo gráfico
    for name, quantity in verduras.items():
        verduralabels.append(name)
        verduradata.append(quantity[0])
        verduraventas.append(round(quantity[1]*0.001, 2))
    #Con el método max() de Python, buscamos el valor más grande en la lista de datos. La mayor cantidad equivale al producto más vendido
    verdumax = max(verduradata)
    #Conociendo la verdura más vendida, recorremos el diccionario con un ciclo for para obtener su nombre y el monto vendido
    for key, value in verduras.items():
        for elemento in value:
            if elemento == verdumax:
                #Al hallar la verdura más vendida dentro del diccionario, asignamos a variables su nombre, cantidad y monto vendidos, para mostrarlo en el template html
                namae = key
                ryou = elemento
                goukei = verduras[namae][1]
    #Por último, mediante el diccionario context, pasamos al return todas las variables y objetos necesarios para mostrar los datos y gráficos en la plantilla html
    context = {'mes': mes, 'frutadata': frutadata, 'frutaventas': frutaventas, 'frutalabels': frutalabels,
    'verduradata': verduradata, 'verduraventas': verduraventas, 'verduralabels': verduralabels, 
    'nom':nom, 'quantite':quantite, 'somme': somme, 'namae':namae, 'ryou':ryou, 'goukei':goukei}    
    return render(request, 'Productos/estadisticaproducto.html', context)