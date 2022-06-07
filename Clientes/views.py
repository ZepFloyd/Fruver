from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Home.models import *
from Pedidos.models import *
from .forms import *
from .models import *
from datetime import datetime, timedelta



#Gestionar a los clientes, crear nuevo, actualizar, eliminar
@login_required(login_url='fruver-acceso')
def clientes(request):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')

    #query hace filtro para obtener a los usuarios cuyo atributo is_staff es False, se muestran en el listado de clientes del html
    clientes = Usuario.objects.filter(is_staff=False)
    
    context = {'clientes': clientes,}
    return render(request, 'Clientes/clientes.html', context)



#Actualizar datos de cliente
@login_required(login_url='fruver-acceso')
def editarcliente(request, usuario_id):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')
    usuario = Usuario.objects.get(pk=usuario_id)
    form = FormularioEditarCliente(request.POST or None, instance=usuario)
    if form.is_valid():
        form.save()
        user = form.cleaned_data.get('nombre_usuario')
        messages.success(request,'¡Los datos del cliente ' + user + ' han sido actualizados con éxito!')
        return redirect('fruver-clientes')
    context = {'usuario': usuario, 'form': form}
    return render(request, 'Clientes/editarcliente.html', context)



#Eliminar cliente
@login_required(login_url='fruver-acceso')
def eliminarcliente(request, usuario_id):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')
    #obtenemos al usuario que se reuiqre eliminar
    usuario = Usuario.objects.get(pk=usuario_id)
    #Verificamos si el usuario ha realizado algún pedido.
    #Filtramos todos los pedidos en donde la columna cliente posea el id del cliente que se desea eliminar
    pedido = Pedido.objects.filter(cliente=usuario_id)
    #Si pedido existe, es decir, si hay pedidos que hayan sido realizados por el cliente en cuestión, no eliminamos e informamos de ello al usuario
    if pedido:
        messages.warning(request, 'Acción de Riesgo')
        return redirect('fruver-clientes')
    #Si el cliente no posee ningún pedido, eliminamos
    else:
        usuario.delete()
        messages.success(request,'El usuario ha sido eliminado correctamente.')
        return redirect('fruver-clientes')



#Perfil de usuario cliente
@login_required(login_url='fruver-acceso')
def perfilcliente(request):
    usuario = request.user
    pedidos = Pedido.objects.filter(cliente=usuario)
    cantidad = 0
    for pedido in pedidos:
        cantidad = cantidad + 1
    context = {'usuario': usuario, 'cantidad': cantidad}
    return render(request, 'Clientes/perfilcliente.html', context)



#Actualizar datos personales
@login_required(login_url='fruver-acceso')
def actualizardatos(request):
    #Obtenemos el usuario actual
    usuario = request.user
    #generamos el formulario para modificar los datos que se requieran
    form = FormularioEditarCliente(request.POST or None, instance=usuario)
    if form.is_valid():
        form.instance.is_active = True
        form.save()
        messages.success(request,'¡Sus datos fueron actualizados con éxito!')
        return redirect('fruver-perfilcliente')
    context = {'usuario': usuario, 'form': form}
    return render(request, 'Clientes/actualizardatos.html', context)



#Pedidos del cliente
@login_required(login_url='fruver-acceso')
def mispedidos(request):
    usuario = request.user
    pedidos = Pedido.objects.filter(cliente=usuario).order_by('fecha_pedido')
    context = {'usuario': usuario, 'pedidos': pedidos}
    return render(request, 'Clientes/mispedidos.html', context)



#Accede al detalle de un pedido
@login_required(login_url='fruver-acceso')
def mipedido(request, pedido_id):
    pedido = Pedido.objects.get(pk=pedido_id)
    if pedido.cliente != request.user:
        return redirect('fruver-mispedidos')
    else:
        #Obtenemos un queryset del Pedido, lo que nos permitirá iterar sobre sus atributos
        pedidos = Pedido.objects.filter(pk=pedido_id)
        clientes = Pedido.objects.select_related()
        #Obtenemos el objeto Pedido, lo que nos permitirá acceder a los productos vinculados a él a través de la clase intermediaria DetallePedido
        order = Pedido.objects.get(pk=pedido_id)
        #Hacemos query sobre los registros de la tabla DetallePedido que estén vinculados al pedido actual
        detalles = DetallePedido.objects.filter(pedido=order.id)
        context = {'pedidos': pedidos, 'clientes': clientes, 'detalles': detalles}
        return render(request, 'Clientes/mipedido.html', context)