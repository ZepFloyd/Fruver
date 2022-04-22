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
    return render(request, 'Pedidos/verduras.html')


#Agregar productos al carrito de compras
@login_required(login_url='fruver-acceso')
def agregarproducto(request, producto_id):

    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)

    carrito.agregar(producto)
    messages.success(request,'¡Producto agregado al carrito!')
    return redirect('fruver-frutas')


'''    if request.POST:
        producto = Producto.objects.get(pk=producto_id)
        cantidad = request.POST.get('cantidad')
        print(cantidad)
        messages.success(request,'¡Producto añadido al carrito!')
        return redirect('fruver-frutas')

    return render(request, 'Pedidos/.html')'''

'''#Eliminar productos al carrito de compras
@login_required(login_url='fruver-acceso')
def eliminarproducto(request, producto_id):

    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)

    carrito.eliminar(producto)
    return redirect('fruver-frutas')
'''
#Restar productos al carrito de compras
@login_required(login_url='fruver-acceso')
def restarproducto(request, producto_id):

    carrito = Carrito(request)
    producto = Producto.objects.get(id=producto_id)

    carrito.restar(producto)
    return redirect('fruver-frutas')

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