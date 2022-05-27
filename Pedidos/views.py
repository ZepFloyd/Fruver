from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
#from .forms import *
from .models import *
from Productos.models import Producto
from Pedidos.carrito import Carrito
from Home.models import CuentaBancaria
from datetime import datetime, timedelta

#ver frutas a la venta
def frutas(request):
    #Hacemos query sobre todas las ocurrencias de la tabla Producto, para iterar sobre ellas en el template
    frutas = Producto.objects.filter(tipo_producto='Fruta', stock_producto__gt=0) #__gt filtra por stock greater than 0
    context = {'frutas': frutas}
    return render(request, 'Pedidos/frutas.html', context)

#Muestra las frutas filtradas según el criterio seleccionado
def filtrarfrutas(request):
    orden = request.POST.get('ordenar')
    frutas = Producto.objects.filter(tipo_producto='Fruta', stock_producto__gt=0).order_by(orden)
    context = {'frutas': frutas}
    return render(request, 'Pedidos/frutas.html', context)

#ver verduras a la venta
def verduras(request):
    #Hacemos query sobre todas las ocurrencias de la tabla Producto, para iterar sobre ellas en el template
    verduras = Producto.objects.filter(tipo_producto='Verdura', stock_producto__gt=0) #__gt filtra por stock greater than 0
    context = {'verduras': verduras}
    return render(request, 'Pedidos/verduras.html', context)

#Muestra las verduras filtradas según el criterio seleccionado
def filtrarverduras(request):
    orden = request.POST.get('ordenar')
    verduras = Producto.objects.filter(tipo_producto='Verdura', stock_producto__gt=0).order_by(orden)
    context = {'verduras': verduras}
    return render(request, 'Pedidos/verduras.html', context)


#Agregar productos al carrito de compras
@login_required(login_url='fruver-acceso')
def agregarproducto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    cantidad = int(request.POST.get('cantidad'))
    producto.stock_producto -= cantidad
    producto.save()
    imagen = request.POST.get('image')
    carrito.agregar(producto, cantidad, imagen)
    messages.success(request,'¡Producto agregado al carrito!')
    if producto.tipo_producto == 'Fruta':
        return redirect('fruver-frutas')
    elif producto.tipo_producto == 'Verdura':
        return redirect('fruver-verduras')

#Eliminar productos al carrito de compras
@login_required(login_url='fruver-acceso')
def eliminarproducto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    cantidad = int(request.POST.get('cantidad'))
    producto.stock_producto += cantidad
    producto.save()
    carrito.eliminar(producto)
    return redirect('fruver-carrito')

#Restar unidades/Kg de productos al carrito de compras
@login_required(login_url='fruver-acceso')
def restarproducto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    producto.stock_producto += 1
    producto.save()
    carrito.restar(producto)
    return redirect('fruver-carrito')

#Suma unidades/Kg de productos al carrito de compras
@login_required(login_url='fruver-acceso')
def sumarproducto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)
    if producto.stock_producto == 0:
        messages.error(request, 'Lo sentimos')
    elif producto.stock_producto > 0:
        producto.stock_producto -= 1
        producto.save()
        carrito.sumar(producto)
    return redirect('fruver-carrito')

#Limpiar carrito de compras
@login_required(login_url='fruver-acceso')
def limpiarcarrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect('fruver-carrito')

#ver carrito de compras
@login_required(login_url='fruver-acceso')
def carrito(request):
    return render(request, 'Pedidos/carrito.html')




#Confirmar preoductos, medio de pago y hacer el pedido
@login_required(login_url='fruver-acceso')
def hacerpedido(request):
    #instanciamos el carrito y verificamos que contenga items, si no hay, se redirige al usuario a la página del carrito
    #así evitamos que un usuario intente hacer un pedido con el carrito vacío, ingresando mediante la URL de hacerpedido
    cart = request.session.get('carrito')
    if len(cart) == 0:
        return redirect('fruver-carrito')
    #Instanciamos al usuario actual para crear el pedido, y también para acceder a sus atributos desde el template, lo pasamos al return dentro de la variable context
    current_user = request.user
    #Instanciamos el objeto de cuenta bancaria para mostrar los datos al cliente
    #en caso de que desee pagar vía transferencia
    banco = CuentaBancaria.objects.filter(id=1)
    #Mediante la librería datetime de python asignamos la fecha de hoy a la variable ahora, y definimos una variable dias_entrega
    #para informar la fecha estimada de entrega del pedido
    ahora = datetime.now()
    dias_entrega = datetime.now()+timedelta(days=2)
    #damos formato a la fecha, para pasarla luego al return en el diccionario context
    fecha_pedido = ahora.strftime("%d-%m-%Y %H:%M")
    fecha_estimada = dias_entrega.strftime("%d-%m-%Y")
    if request.method == 'POST':  
        #Recogemos el medio de pago, el monto y el estado del pedido desde el POST y los asignamos a variables
        pago = request.POST.get('mediopago')
        monto = int(request.POST.get('totalpedido'))
        estado = request.POST.get('estadopedido')
        #creamos un pedido pasando los argumentos de monto, medio de pago, estado y id del cliente
        order = Pedido.objects.create(monto_pedido=monto, medio_pago=pago, estado_pedido=estado, cliente=current_user)
        #Recorremos los valores del diccionario 'carrito' con un ciclo for,  accediendo así a cada producto en el carrito, y obtenemos sus atributos
        #para crear los registros en la tabla DetallePedido, que vinculen a los productos en el carrito con el pedido recién creado
        for value in request.session['carrito'].values():
            producto = value['producto_id']
            cantidad = value['cantidad']
            modoventa = value['modo_venta']
            subtotal = value['subtotal']
            precio = subtotal / cantidad
            detalle = DetallePedido.objects.create(precio_producto=precio, modo_venta=modoventa, cantidad_producto=cantidad, subtotal=subtotal, pedido_id=order.id, producto_id=producto)
        #limpiamos el carrito luego de crear los registros de las tablas Pedido y DetallePedido en la base de datos
        carrito = Carrito(request)
        carrito.limpiar()
        #informamos al usuario que su pedido ha sido confirmado y redirigimos a la página del carrito
        messages.success(request,'¡Su pedido ha sido confirmado!')
        return redirect('fruver-carrito')
    context = {'current_user': current_user, 'banco': banco, 'fecha_estimada': fecha_estimada, 'fecha_pedido': fecha_pedido} 
    return render(request, 'Pedidos/hacerpedido.html', context)



#Accede a la lista de pedidos activos de los clientes
@login_required(login_url='fruver-acceso')
def pedidos(request):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')
    #Hacemos query sobre todas las ocurrencias de la tabla Pedido, para iterar sobre ellas en el template
    pedidos = Pedido.objects.all().order_by('-fecha_pedido')
    #Hacemos query sobre el objeto vinculado con la llave foránea de tabla Pedido, en este caso, su atributo cliente se corresponde con tabla Usuario,
    # por lo que será posible acceder al nombre y resto de datos del cliente que hizo el pedido  
    clientes = Pedido.objects.select_related()  
    context = {'pedidos': pedidos, 'clientes': clientes}
    return render(request, 'Pedidos/pedidos.html', context)



#Filtra y muestra los pedidos según su estado
@login_required(login_url='fruver-acceso')
def filtrarpedidos(request, estado):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')
    pedidos = Pedido.objects.filter(estado_pedido=estado)
    clientes = Pedido.objects.select_related()
    if not pedidos:
        messages.warning(request, 'No hay pedidos '+estado+'s en este momento')
    context = {'pedidos': pedidos, 'clientes': clientes}  
    return render(request, 'Pedidos/pedidos.html', context)



#Actualiza el estado de los pedidos
@login_required(login_url='fruver-acceso')
def actualizarpedido(request, pedido_id, estado):
    pedido = Pedido.objects.filter(pk=pedido_id)
    pedido.update(estado_pedido=estado)
    messages.success(request,'¡Estado cambiado con éxito!')
    return redirect('fruver-pedidos')



#Accede al detalle de un pedido
@login_required(login_url='fruver-acceso')
def detallepedido(request, pedido_id):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')
    #Obtenemos un queryset del Pedido, lo que nos permitirá iterar sobre sus atributos
    pedidos = Pedido.objects.filter(pk=pedido_id)
    clientes = Pedido.objects.select_related()
    #Obtenemos el objeto Pedido, lo que nos permitirá acceder a los productos vinculados a él a través de la clase intermediaria DetallePedido
    order = Pedido.objects.get(pk=pedido_id)
    #Hacemos query sobre los registros de la tabla DetallePedido que estén vinculados al pedido actual
    detalles = DetallePedido.objects.filter(pedido=order.id)
    context = {'pedidos': pedidos, 'clientes': clientes, 'detalles': detalles}
    return render(request, 'Pedidos/detallepedido.html', context)