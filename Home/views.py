from ssl import AlertDescription
from django.forms import PasswordInput
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import *

# Página principal de Fruver
def home(request):
    return render(request, 'Home/index.html')


#Registro de cuenta de usuario cliente
def registro(request):
    if request.user.is_authenticated:
        return redirect('fruver-home')
    else:    
        form = FormularioCrearUsuario()
        if request.method == 'POST':
            form = FormularioCrearUsuario(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'¡Su cuenta ha sido creada con éxito!')
                return redirect('fruver-acceso')

        context = {'form': form}
        return render(request, 'Home/registro.html', context)


#Login del sitio
def acceso(request):
    if request.user.is_authenticated:
        return redirect('fruver-home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                name = user.nombre_usuario
                # Valida si el usuario es cliente o vendedor, y lo redirige a la página que corresponda
                if user.is_staff is True:
                    messages.success(request,'¡Hola ' + name + '!')
                    return redirect('fruver-mainmenu')
                else:
                    messages.success(request,'¡Hola ' + name + '!')
                    return redirect('fruver-home')
            else:
                messages.error(request, 'E-mail o contraseña incorrectos')
                return redirect('fruver-acceso')
        return render(request, 'Home/acceso.html')


#Cerrar sesión
def salir(request):
    logout(request)
    messages.info(request, 'Ha cerrado sesión correctamente')
    return redirect('fruver-home')


#ver frutas a la venta
def frutas(request):
    return render(request, 'Home/frutas.html')


#ver verduras a la venta
def verduras(request):
    return render(request, 'Home/verduras.html')


#Ver carrito de compras
def carrito(request):
    return render(request, 'Home/carrito.html')


#Menú principal para vendedor
@login_required(login_url='fruver-acceso')
def mainmenu(request):
    return render(request, 'Home/mainmenu.html')


#Ingresar o actualizar datos de cuenta bancaria
@login_required(login_url='fruver-acceso')
def datosbanco(request):

    cuenta = CuentaBancaria.objects.first()
    form = FormularioCuentaBancaria(request.POST or None, instance=cuenta)
    if form.is_valid():
        form.save()
        messages.success(request,'Los datos de la cuenta se han guardado con éxito')
        return redirect('fruver-datosbanco')
    context = {'cuenta': cuenta, 'form': form}
    return render(request, 'Home/datosbanco.html', context)



#Gestionar a los vendedores, crear nuevo vendedor, actualizar, eliminar
@login_required(login_url='fruver-acceso')
def gestionarvendedor(request):

    #query hace filtro para obtener a los usuarios cuyo atributo is_staff es True, se muestran en el listado de vendedores del html
    vendedores = Usuario.objects.filter(is_staff=True)
    form = FormularioCrearUsuario()
    if request.method == 'POST':
        form = FormularioCrearUsuario(request.POST)
        if form.is_valid():
            form.instance.is_staff = True  #setea verdadero el atributo is_staff para crear usuario perfil vendedor
            form.save()
            user = form.cleaned_data.get('nombre_usuario')
            messages.success(request,'¡La cuenta de vendedor ' + user + ' ha sido creada con éxito!')
            return redirect('fruver-gestionarvendedor')

    context = {'form': form, 'vendedores': vendedores}
    return render(request, 'Home/gestionarvendedor.html', context)



#Actualizar datos de vendedor
@login_required(login_url='fruver-acceso')
def editarvendedor(request, usuario_id):

    usuario = Usuario.objects.get(pk=usuario_id)
    form = FormularioEditarVendedor(request.POST or None, instance=usuario)
    if form.is_valid():
        form.save()
        user = form.cleaned_data.get('nombre_usuario')
        messages.success(request,'¡Los datos del vendedor ' + user + ' han sido actualizados con éxito!')
        return redirect('fruver-gestionarvendedor')
    context = {'usuario': usuario, 'form': form}
    return render(request, 'Home/editarvendedor.html', context)



#Eliminar vendedor
@login_required(login_url='fruver-acceso')
def eliminarvendedor(request, usuario_id):

    usuario = Usuario.objects.get(pk=usuario_id)
    usuario.delete()
    messages.success(request,'El usuario ha sido eliminado')
    return redirect('fruver-gestionarvendedor')
