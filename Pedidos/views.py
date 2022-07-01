from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from Productos.models import Producto
from Pedidos.carrito import Carrito
from Home.models import CuentaBancaria
from datetime import datetime, timedelta



#ver frutas a la venta
def frutas(request):
    #Generamos un dataset con todas las ocurrencias de la tabla Producto, para iterar sobre ellas en el template html
    #El query contiene 2 filtros: los objetos deben ser frutas, y deben estar activos (disponibles para la venta)
    frutas = Producto.objects.filter(tipo_producto='Fruta', is_active=True)
    context = {'frutas': frutas}
    return render(request, 'Pedidos/frutas.html', context)



#Muestra las frutas filtradas según el criterio seleccionado por el usuario
def filtrarfrutas(request):
    #Obtenemos desde el combobox el orden que el usuario desea visualizar para los productos
    orden = request.POST.get('ordenar')
    #Reordenamos los productos en función del orden requerido, mediante el método order_by()
    frutas = Producto.objects.filter(tipo_producto='Fruta', is_active=True).order_by(orden)
    context = {'frutas': frutas}
    return render(request, 'Pedidos/frutas.html', context)



#ver verduras a la venta
def verduras(request):
    #Generamos un dataset con todas las ocurrencias de la tabla Producto, para iterar sobre ellas en el template html
    #El query contiene 2 filtros: los objetos deben ser verduras, y deben estar activos (disponibles para la venta)
    verduras = Producto.objects.filter(tipo_producto='Verdura', is_active=True)
    context = {'verduras': verduras}
    return render(request, 'Pedidos/verduras.html', context)



#Muestra las verduras filtradas según el criterio seleccionado por el usuario
def filtrarverduras(request):
    #Obtenemos desde el combobox el orden que el usuario desea visualizar para los productos
    orden = request.POST.get('ordenar')
    #Reordenamos los productos en función del orden requerido, mediante el método order_by()
    verduras = Producto.objects.filter(tipo_producto='Verdura', is_active=True).order_by(orden)
    context = {'verduras': verduras}
    return render(request, 'Pedidos/verduras.html', context)



#Agregar productos al carrito de compras
@login_required(login_url='fruver-acceso')
def agregarproducto(request, producto_id):
    #Instanciamos un objeto de la clase Carrito para ir guardando en él los productos a comprar
    carrito = Carrito(request)
    #Instanciamos el objeto de la clase Producto cuyo id corresponda al argumento producto_id recibido por esta función
    producto = Producto.objects.get(id=producto_id)
    #Obtenemos la cantidad requerida del producto desde el number input del html
    cantidad = int(request.POST.get('cantidad'))
    #Restamos la cantidad al stock del producto, y guardamos con el método save()
    producto.stock_producto -= cantidad
    producto.save()
    #Dado que el carrito está vinculado a la sesión de usuario, se guarda en RAM, y no en la base de datos (no existe una tabla carrito)
    #Por ello, es necesario pasar la imagen del producto agregado al carrito directamente en el método agregar() de la clase Carrito
    #Así, es posible acceder a la imagen del producto en la página de vista previa del pedido del cliente
    #Asignamos la imagen del producto a una variable, y luego pasamos como argumento el producto, la cantidad, y la imagen, en el método agregar()
    #Con esto, el carrito guarda el id, la cantidad y la imagen para cada producto agregado por el usuario
    imagen = request.POST.get('image')
    carrito.agregar(producto, cantidad, imagen)
    messages.success(request,'¡Producto agregado al carrito!')
    if producto.tipo_producto == 'Fruta':
        return redirect('fruver-frutas')
    elif producto.tipo_producto == 'Verdura':
        return redirect('fruver-verduras')



#Eliminar productos del carrito de compras
@login_required(login_url='fruver-acceso')
def eliminarproducto(request, producto_id):
    #Obtenemos el carrito vinculado a la sesión del usuario actual
    carrito = Carrito(request)
    #Obtenemos el producto cuyo id corresponda al argumento producto_id recibido por esta función
    producto = Producto.objects.get(id=producto_id)
    #Obtenemos la cantidad de productos que están guardados en el carrito (por ejemplo, 5 manzanas) desde el html
    cantidad = int(request.POST.get('cantidad'))
    #Dado que estamos eliminando el producto del carrito, reponemos el stock para que vuelva a estar disponible para la venta (lo guardamos en la base de datos)
    producto.stock_producto += cantidad
    producto.save()
    #Eliminamos el producto del carrito, llamando al método eliminar() de la clase Carrito, y le pasamos el producto como argumento
    carrito.eliminar(producto)
    return redirect('fruver-carrito')



#Restar unidades/Kg de un producto determinado al carrito de compras
@login_required(login_url='fruver-acceso')
def restarproducto(request, producto_id):
    #Obtenemos el carrito vinculado a la sesión del usuario actual
    carrito = Carrito(request)
    #Obtenemos el producto cuyo id corresponda al argumento producto_id recibido por esta función
    producto = Producto.objects.get(id=producto_id)
    #Ya que estamos restando 1 unidad/Kg de un producto desde el carrito, debemos reponer el stock del producto, sumándole 1 al stock_producto en la base de datos
    producto.stock_producto += 1
    producto.save()
    #Para restar la unidad/Kg del producto, lo pasamos como argumento al método restar() de la clase Carrito
    carrito.restar(producto)
    return redirect('fruver-carrito')



#Suma unidades/Kg de un producto determinado al carrito de compras
@login_required(login_url='fruver-acceso')
def sumarproducto(request, producto_id):
    #Obtenemos el carrito vinculado a la sesión del usuario actual
    carrito = Carrito(request)
    #Obtenemos el producto cuyo id corresponda al argumento producto_id recibido por esta función
    producto = Producto.objects.get(id=producto_id)
    #Si el usuario intenta agregar al carrito unidades/Kg de un producto del cual ya no queda stock, se le informa de ello y no se agrega nada al carrito
    if producto.stock_producto == 0:
        messages.error(request, 'Lo sentimos')
    #Si aún queda stock del producto, restamos 1 al stock_producto en la base de datos,
    #y agregamos 1 unidad/Kg al carrito, pasando el producto como argumento al método sumar() de la clase Carrito
    elif producto.stock_producto > 0:
        producto.stock_producto -= 1
        producto.save()
        carrito.sumar(producto)
    return redirect('fruver-carrito')



#Limpiar carrito de compras, quita todos los productos que han sido agregados al carrito, dejándolo vacío
@login_required(login_url='fruver-acceso')
def limpiarcarrito(request):
    #Obtenemos el carrito vinculado a la sesión del usuario actual
    carrito = Carrito(request)
    #Llamamos al método limpiar() de la clase Carrito y redirigimos al usuario a la página del carrito
    carrito.limpiar()
    return redirect('fruver-carrito')



#Muestra la página del carrito de compras, incluyendo los productos y cantidades que han sido agregados por el usuario, si los hay
@login_required(login_url='fruver-acceso')
def carrito(request):
    return render(request, 'Pedidos/carrito.html')



#Muestra un resumen de los productos a comprar, y las opciones para elegir medio de pago y hacer el pedido
@login_required(login_url='fruver-acceso')
def hacerpedido(request):
    #Instanciamos el carrito y verificamos que contenga items, si no hay, se redirige al usuario a la página del carrito
    #Así evitamos que un usuario intente hacer un pedido con el carrito vacío, ingresando mediante la URL de hacerpedido
    cart = request.session.get('carrito')
    if len(cart) == 0:
        return redirect('fruver-carrito')
    #Instanciamos al usuario actual para crear el pedido, y también para acceder a sus atributos desde el template, lo pasamos al return dentro del diccionario 'context'
    current_user = request.user
    #Instanciamos el objeto de cuenta bancaria para mostrar los datos al cliente, en caso de que desee pagar vía transferencia
    banco = CuentaBancaria.objects.filter(id=1)
    #Mediante la librería datetime de python asignamos la fecha de hoy a la variable ahora, y definimos una variable dias_entrega
    #para informar la fecha estimada de entrega del pedido (2 días a partir de la fecha actual)
    ahora = datetime.now()
    dias_entrega = datetime.now()+timedelta(days=2)
    #Damos formato a la fecha, para pasarla luego al return en el diccionario context
    fecha_pedido = ahora.strftime("%d-%m-%Y %H:%M")
    fecha_estimada = dias_entrega.strftime("%d-%m-%Y")
    if request.method == 'POST':  
        #Recogemos el medio de pago, el monto y el estado del pedido desde el POST y los asignamos a variables
        pago = request.POST.get('mediopago')
        monto = int(request.POST.get('totalpedido'))
        estado = request.POST.get('estadopedido')
        #Creamos un pedido mediante el método create(), y pasamos los argumentos de monto, medio de pago, estado y id del cliente para guardar el pedido en la base de datos
        order = Pedido.objects.create(monto_pedido=monto, medio_pago=pago, estado_pedido=estado, cliente=current_user)
        #Recorremos los valores del diccionario 'carrito' con un ciclo for, accediendo así a cada producto en el carrito,
        #Y obtenemos sus atributos para crear los registros en la tabla DetallePedido de la base de datos, que vinculen a los productos en el carrito con el pedido recién creado
        for value in request.session['carrito'].values():
            producto = value['producto_id']
            cantidad = value['cantidad']
            modoventa = value['modo_venta']
            subtotal = value['subtotal']
            precio = subtotal / cantidad
            #Creamos el registro en la tabla DetallePedido que vincula los productos, sus cantidades y precios al pedido recién creado
            detalle = DetallePedido.objects.create(precio_producto=precio, modo_venta=modoventa, cantidad_producto=cantidad, subtotal=subtotal, pedido_id=order.id, producto_id=producto)
        #Limpiamos el carrito luego de crear los registros de las tablas Pedido y DetallePedido en la base de datos
        carrito = Carrito(request)
        carrito.limpiar()
        #Informamos al usuario que su pedido ha sido confirmado y redirigimos a la página del carrito
        messages.success(request,'¡Su pedido ha sido confirmado!')
        return redirect('fruver-carrito')
    context = {'current_user': current_user, 'banco': banco, 'fecha_estimada': fecha_estimada, 'fecha_pedido': fecha_pedido} 
    return render(request, 'Pedidos/hacerpedido.html', context)



#Accede a la lista de pedidos de los clientes
@login_required(login_url='fruver-acceso')
def pedidos(request):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')
    #Hacemos query sobre todas las ocurrencias de la tabla Pedido, para iterar sobre ellas en el template
    pedidos = Pedido.objects.all().order_by('-fecha_pedido')
    #Hacemos query sobre el objeto vinculado con la llave foránea de tabla Pedido, en este caso, su atributo cliente se corresponde con tabla Usuario,
    #por lo que será posible acceder al nombre y resto de datos del cliente que hizo el pedido  
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
    #Obtenemos un dataset con todos los pedidos cuyo estado_pedido corresponda al argumento estado recibido por esta función
    pedidos = Pedido.objects.filter(estado_pedido=estado)
    #Obtenemos un dataset con todos los clientes vinculados a los pedidos filtrados
    clientes = Pedido.objects.select_related()
    #Si no hay pedidos del estado requerido, se informa de ello al usuario con un mensaje
    if not pedidos:
        messages.warning(request, 'No hay pedidos '+estado+'s en este momento')
    context = {'pedidos': pedidos, 'clientes': clientes}  
    return render(request, 'Pedidos/pedidos.html', context)



#Actualiza el estado de los pedidos
@login_required(login_url='fruver-acceso')
def actualizarpedido(request, pedido_id, estado):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')
    #Instanciamos el pedido cuyo id corresponda al argumento pedido_id recibido por esta función
    pedido = Pedido.objects.filter(pk=pedido_id)
    #Mediante el método update(), actualizamos el atributo estado_pedido, asignándole el argumento estado recibido por esta función, e informamos al usuario con un mensaje 
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
    #Instanciamos el pedido cuyo id corresponda al argumento pedido_id recibido por esta función 
    pedidos = Pedido.objects.filter(pk=pedido_id)
    #Instanciamos al cliente vinculado al pedido
    clientes = Pedido.objects.select_related()
    #Obtenemos el objeto Pedido, lo que nos permitirá acceder a los productos vinculados a él a través de la clase (tabla en la BD) intermediaria DetallePedido
    order = Pedido.objects.get(pk=pedido_id)
    #Hacemos consultas sobre los registros de la tabla DetallePedido que estén vinculados al pedido actual, mediante un filtro con la id del pedido
    detalles = DetallePedido.objects.filter(pedido=order.id)
    context = {'pedidos': pedidos, 'clientes': clientes, 'detalles': detalles}
    return render(request, 'Pedidos/detallepedido.html', context)