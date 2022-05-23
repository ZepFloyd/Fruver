from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import *

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



#Agrega nuevos Productos
@login_required(login_url='fruver-acceso')
def agregarproducto(request, tipo_producto):
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
    return render(request, 'Productos/agregarproducto.html', context)



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
def eliminarproducto(request, id_producto, tipo_producto):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')

    producto = Producto.objects.get(pk=id_producto)
    producto.delete()
    messages.success(request, 'El producto ha sido eliminado correctamente.')
    return redirect('/productos/adminproductos/'+tipo_producto)