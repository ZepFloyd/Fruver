from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
#from .forms import *
from .models import *
from Productos.models import Producto
from Pedidos.carrito import Carrito


#ver frutas a la venta
def frutas(request):
    #Hacemos query sobre todas las ocurrencias de la tabla Producto, para iterar sobre ellas en el template
    frutas = Producto.objects.filter(tipo_producto='Fruta')
    context = {'frutas': frutas}
    return render(request, 'Pedidos/frutas.html', context)

#ver verduras a la venta
def verduras(request):
    #Hacemos query sobre todas las ocurrencias de la tabla Producto, para iterar sobre ellas en el template
    verduras = Producto.objects.filter(tipo_producto='Verdura')
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
    #Instanciamos al usuario actual para crear el pedido, y también para acceder a sus atributos desde el template, lo pasamos al return en el context
    current_user = request.user
    
    if request.method == 'POST':  
        #Recogemos el medio de pago, el monto y el estado del pedido desde el POST y los asignamos a avriables
        pago = request.POST.get('mediopago')
        monto = int(request.POST.get('totalpedido'))
        estado = request.POST.get('estadopedido')
        #creamos un pedido pasando los argumentos de monto, medio de pago, estado y id del cliente
        order = Pedido.objects.create(monto_pedido=monto, medio_pago=pago, estado_pedido=estado, cliente=current_user)
        cart = request.session.get("carrito")
        for value in cart:
            producto = value.producto_id
            cantidad = value.cantidad
            modoventa = value.modo_venta
            subtotal = value.subtotal
            precio = subtotal / cantidad
            detalle = DetallePedido.objects.create(precio_producto=precio, modo_venta=modoventa, cantidad_producto=cantidad, subtotal=subtotal, pedido_id=order.id, producto_id=producto)


        #limpiamos el carrito
        carrito = Carrito(request)
        carrito.limpiar()
        #informamos al usuario que su pedido ha sido confirmado y redirigimos a página principal
        messages.success(request,'¡Su pedido ha sido confirmado!')
        return redirect('fruver-home')
    
    context = {'current_user': current_user} 
    return render(request, 'Pedidos/hacerpedido.html', context)





#Accede a la lista de pedidos activos de los clientes
@login_required(login_url='fruver-acceso')
def pedidos(request):
    #Hacemos query sobre todas las ocurrencias de la tabla Pedido, para iterar sobre ellas en el template
    pedidos = Pedido.objects.all()
    #Hacemos query sobre el objeto vinculado con la llave foránea de tabla Pedido, en este caso, su atributo cliente se corresponde con tabla Usuario,
    # por lo que será posible acceder al nombre y resto de datos del cliente que hizo el pedido  
    clientes = Pedido.objects.select_related()  
    context = {'pedidos': pedidos, 'clientes': clientes}
    return render(request, 'Pedidos/pedidos.html', context)