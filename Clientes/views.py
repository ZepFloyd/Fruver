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



#Muestra lista de clientes para ser gestionados: actualizar, eliminar
@login_required(login_url='fruver-acceso')
def clientes(request):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')
    #Query hace filtro para obtener a los usuarios cuyo atributo is_staff es False, se muestran en el listado de clientes del html
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
    #Instanciamos al cliente cuyo id corresponda al argumento usuario_id recibido por esta función
    usuario = Usuario.objects.get(pk=usuario_id)
    #Generamos el formulario para ingresar los datos que se requiera cambiar. También mostramos los datos actuales del cliente, asignando la variable usuario al instance
    form = FormularioEditarCliente(request.POST or None, instance=usuario)
    #Si el formulario es válido, guardamos los cambios e informamos al usuario
    if form.is_valid():
        form.save()
        user = form.cleaned_data.get('nombre_usuario')
        messages.success(request,'¡Los datos del cliente ' + user + ' han sido actualizados con éxito!')
        return redirect('fruver-clientes')
    context = {'usuario': usuario, 'form': form}
    return render(request, 'Clientes/editarcliente.html', context)



#Elimina un cliente. Esta acción se lleva a cabo sólo cuando no posea pedidos, para mantener la integridad referencial en la base de datos
@login_required(login_url='fruver-acceso')
def eliminarcliente(request, usuario_id):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')
    #obtenemos al usuario que se requiere eliminar
    usuario = Usuario.objects.get(pk=usuario_id)
    #Verificamos si el usuario ha realizado algún pedido.
    #Filtramos todos los pedidos en donde la columna cliente posea el id del cliente que se desea eliminar
    pedido = Pedido.objects.filter(cliente=usuario_id)
    #Si pedido existe, es decir, si hay pedidos que hayan sido realizados por el cliente en cuestión, no eliminamos e informamos de ello al usuario
    #En el cuadro de diálogo emergente (ver html) se informa al usuario que el cliente posee pedidos, por lo que se recomienda sólo bloquear la cuenta 
    if pedido:
        messages.warning(request, 'Acción de Riesgo')
        return redirect('fruver-clientes')
    #Si el cliente no posee ningún pedido, eliminamos
    else:
        usuario.delete()
        messages.success(request,'El usuario ha sido eliminado correctamente.')
        return redirect('fruver-clientes')



#Muestra el perfil de usuario cliente, con la posibilidad de acceder a la edición de datos personales y consultar estado de pedidos
@login_required(login_url='fruver-acceso')
def perfilcliente(request):
    #Instanciamos al usuario actual mediante el request de la sesión activa
    usuario = request.user
    #Obtenemos un dataset con todos los pedidos que el cliente ha realizado. Con esto podremos saber la cantidad de pedidos
    pedidos = Pedido.objects.filter(cliente=usuario)
    #Declaramos la variable cantidad para almacenar la cantidad de pedidos del cliente, y contamos mediante un ciclo for sobre el dataset de pedidos
    cantidad = 0
    for pedido in pedidos:
        cantidad = cantidad + 1
    #Por último, pasamos al usuario y la cantidad al return mediante el diccionario context, así podremos acceder a ellos desde el template html
    context = {'usuario': usuario, 'cantidad': cantidad}
    return render(request, 'Clientes/perfilcliente.html', context)



#Actualizar datos personales del perfil de cliente
@login_required(login_url='fruver-acceso')
def actualizardatos(request):
    #Obtenemos el usuario actual
    usuario = request.user
    #generamos el formulario para modificar los datos que se requieran, y mostramos los datos actuales del cliente
    form = FormularioEditarCliente(request.POST or None, instance=usuario)
    #Si los datos ingresados al formulario son válidos, guardamos los cambios y nos aseguramos de que la cuenta permanezca activa
    if form.is_valid():
        form.instance.is_active = True
        form.save()
        messages.success(request,'¡Sus datos fueron actualizados con éxito!')
        return redirect('fruver-perfilcliente')
    #Mediante el diccionario context, pasamos el usuario y el formulario al return de la función, para ser renderizados junto con el template html
    context = {'usuario': usuario, 'form': form}
    return render(request, 'Clientes/actualizardatos.html', context)



#Muestra una lista con los pedidos del cliente actual
@login_required(login_url='fruver-acceso')
def mispedidos(request):
    #Instanciamos al usuario actual mediante el request de la sesión activa
    usuario = request.user
    #Obtenemos un dataset con todos los pedidos que el cliente ha realizado y los ordenamos por fecha
    pedidos = Pedido.objects.filter(cliente=usuario).order_by('fecha_pedido')
    #Por último, pasamos al usuario y los pedidos al return de la función para acceder a ellos desde la plantilla html
    context = {'usuario': usuario, 'pedidos': pedidos}
    return render(request, 'Clientes/mispedidos.html', context)



#Muestra el detalle de un pedido del cliente actual
@login_required(login_url='fruver-acceso')
def mipedido(request, pedido_id):
    #Instanciamos el pedido cuyo id corresponda al argumento pedido_id recibido por esta función
    pedido = Pedido.objects.get(pk=pedido_id)
    #Validamos que el usuario actual sólo pueda acceder a sus propios pedidos, comparando el cliente registrado en el pedido, con el id del usuario actual
    #Esto es necesario ya que, un usuario podría haber accedido a otros pedidos no propios cambiando el número de id en la barra de direcciones del navegador web
    if pedido.cliente != request.user:
        return redirect('fruver-mispedidos')
    else:
        #Obtenemos un queryset del Pedido, lo que nos permitirá acceder sus atributos (o columnas en la BD)
        pedidos = Pedido.objects.filter(pk=pedido_id)
        clientes = Pedido.objects.select_related()
        #Obtenemos el objeto Pedido, lo que nos permitirá acceder a los productos vinculados a él a través de la clase intermediaria DetallePedido
        order = Pedido.objects.get(pk=pedido_id)
        #Hacemos query sobre los registros de la tabla DetallePedido que estén vinculados al pedido actual
        detalles = DetallePedido.objects.filter(pedido=order.id)
        #Por último, pasamos el pedido, el cliente y los artículos incluidos en el pedido (detalles) al return para acceder a ellos desde el template html
        context = {'pedidos': pedidos, 'clientes': clientes, 'detalles': detalles}
        return render(request, 'Clientes/mipedido.html', context)