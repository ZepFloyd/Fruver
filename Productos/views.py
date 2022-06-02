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

# Create your views here.

#Accede al módulo de Productos
@login_required(login_url='fruver-acceso')
def productos(request):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')
    return render(request, 'Productos/productos.html')



#Accede a la lista de productos a la venta
@login_required(login_url='fruver-acceso')
def adminproductos(request, tipo_producto):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')

    if tipo_producto == 'Fruta':
        productos = Producto.objects.filter(tipo_producto='Fruta').order_by('nombre_producto')
    elif tipo_producto == 'Verdura':
        productos = Producto.objects.filter(tipo_producto='Verdura').order_by('nombre_producto')

    context = {'productos': productos, 'tipo_producto': tipo_producto}
    return render(request, 'Productos/adminproductos.html', context)



#Crea nuevos Productos
@login_required(login_url='fruver-acceso')
def crearproducto(request, tipo_producto):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')

    form = FormularioProducto()
    if request.method == 'POST':
        form = FormularioProducto(request.POST, request.FILES)
        tipo_producto = request.POST.get('tipo_producto')
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

    producto = Producto.objects.get(pk=id_producto)
    form = FormularioProducto(request.POST or None, request.FILES or None, instance=producto)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, '¡Los cambios fueron guardados con éxito!')
            return redirect('/productos/editarproducto/'+id_producto)
    
    context = {'form': form, 'producto': producto}
    return render(request, 'Productos/editarproducto.html', context)



#Edita datos de Productos
@login_required(login_url='fruver-acceso')
def suprimirproducto(request, id_producto, tipo_producto):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')

    #Obtenemos el productp a eliminar haciendo un query con la id del producto
    producto = Producto.objects.get(pk=id_producto)
    #Verificamos si el producto está incluido en algún pedido, haciendo query en la tabla DetallePedido, 
    # en donde la columna "producto" tenga ocurrencias del producto que queremos eliminar
    detalle = DetallePedido.objects.filter(producto=id_producto)
    #Si hay ocurrencias, es decir, si el producto está contenido en alguno de los pedidos hechos por clientes, no eliminamos e informamos al usuario de ello
    if detalle:
        messages.warning(request, 'Acción de Riesgo')
        return redirect('/productos/adminproductos/'+tipo_producto)
    #Si el producto no está en ningún pedido, eliminamos
    else:
        producto.delete()
        messages.success(request, 'El producto ha sido eliminado correctamente.')
        return redirect('/productos/adminproductos/'+tipo_producto)



#Muestra estadísticas de los productos
@login_required(login_url='fruver-acceso')
def estadisticaproducto(request):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')

    locale.setlocale(locale.LC_TIME, 'es_ES') #Seteamos el formato de fecha para mostrarse en idioma español
    mes = datetime.now() #Obtenemos la fecha actual
    mes = mes.strftime('%B de %Y') #Damos formato a la fecha para mostrar solo el nombre del mes

    frutas = {}
    verduras = {}
    queryset = DetallePedido.objects.all().order_by('producto')

    for registro in queryset:
        #Si el tipo de producto es una fruta
        if registro.producto.tipo_producto == 'Fruta':
            #Si la fruta no se encuentra aún incluida en nuestro diccionario, la incluimos usando el id como llave, y una lista de 2 items: cantidades y montos vendidos
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
            #Si la verdura no se encuentra aún incluida en nuestro diccionario, la incluimos usando el id como llave, y una lista de 2 items: cantidades y montos vendidos
            if registro.producto.nombre_producto not in verduras.keys():
                cantidad = 0
                monto = 0
                verduras[registro.producto.nombre_producto] = [cantidad + registro.cantidad_producto, monto + registro.subtotal]
            #Si la verdura ya se encuentra en el diccionario, sólo actualizamos la cantidad y el monto
            elif registro.producto.nombre_producto in verduras.keys():
                cantidad = verduras[registro.producto.nombre_producto][0]
                monto = verduras[registro.producto.nombre_producto][1]
                verduras[registro.producto.nombre_producto] = [cantidad + registro.cantidad_producto, monto + registro.subtotal]
    
    frutadata = []
    frutalabels = []
    for name, quantity in frutas.items():
        frutalabels.append(name)
        frutadata.append(quantity[0])
    frutamax = max(frutadata)
    for key, value in frutas.items():
        for elemento in value:
            if elemento == frutamax:
                nom = key
                quantite = elemento
                somme = frutas[nom][1]


    verduradata = []
    verduralabels = []
    for name, quantity in verduras.items():
        verduralabels.append(name)
        verduradata.append(quantity[0])
    verdumax = max(verduradata)
    for key, value in verduras.items():
        for elemento in value:
            if elemento == verdumax:
                namae = key
                ryou = elemento
                goukei = verduras[namae][1]

    context = {'mes': mes, 'frutadata': frutadata, 'frutalabels': frutalabels, 'verduradata': verduradata, 'verduralabels': verduralabels, 
    'nom':nom, 'quantite':quantite, 'somme': somme, 'namae':namae, 'ryou':ryou, 'goukei':goukei}    
    return render(request, 'Productos/estadisticaproducto.html', context)