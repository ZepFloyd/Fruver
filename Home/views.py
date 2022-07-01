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
from datetime import datetime, timedelta



#Página principal de Fruver
def home(request):
    return render(request, 'Home/index.html')



#Registro de cuenta de usuario cliente
def registro(request):
    #Si el usuario ya está autenticado, no aplica el registro. Se lo redirige a página home
    if request.user.is_authenticated:
        messages.warning(request,'Usted ya está registrado')
        return redirect('fruver-home')
    else:
        #Si usuario no está autenticado, se instancia el formulario para crear un nuevo usuario    
        form = FormularioCrearUsuario()
        if request.method == 'POST':
            form = FormularioCrearUsuario(request.POST)
            #Al recibir el POST desde el formulario, se comprueba la validez de este y se crea la cuenta de usuario
            if form.is_valid():
                form.save()
                messages.success(request,'¡Su cuenta ha sido creada con éxito!')
                return redirect('fruver-acceso')
        #Pasamos el objeto formulario, dentro del diccionario context, para renderizarlo junto a la plantilla html
        context = {'form': form}
        return render(request, 'Home/registro.html', context)



#Login del sitio para clientes y vendedores
def acceso(request):
    #Si el usuario ya ha iniciado sesión, se le redirige a la página principal
    if request.user.is_authenticated:
        messages.warning(request,'Usted ya inició sesión')
        return redirect('fruver-home')
    #Si usuario no ha inciado sesión, se procede al proceso de autenticación
    else:
        if request.method == 'POST':
            #Se recibe el nombre de usuario (e-mail) y contraseña, y se validan llamando al método authenticate()
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            #Si la credenciales son correctas, el usuario queda autenticado
            if user is not None:
                login(request, user)
                name = user.nombre_usuario
                # Validamos si el usuario es cliente o vendedor mediante el atributo is_staff, y lo redirigimos al menú de vendedor o a la página home según corresponda
                if user.is_staff is True:
                    messages.success(request,'¡Hola ' + name + '!')
                    return redirect('fruver-mainmenu')
                else:
                    messages.success(request,'¡Hola ' + name + '!')
                    return redirect('fruver-home')
            #Si las credenciales de acceso son incorrectas, se informa de ello al usuario
            else:
                messages.error(request, 'E-mail o contraseña incorrectos')
                return redirect('fruver-acceso')
        return render(request, 'Home/acceso.html')



#Cerrar sesión
def salir(request):
    #Cerramos la sesión de usuario llamando al método logout de Django, y enviamos un mensaje al usuario para informarle el cierre de sesión correcto
    logout(request)
    messages.info(request, 'Ha cerrado sesión correctamente')
    return redirect('fruver-home')



#Menú principal para usuario vendedor
@login_required(login_url='fruver-acceso')
def mainmenu(request):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')
    return render(request, 'Home/mainmenu.html')



#Ingresar o actualizar datos de cuenta bancaria
@login_required(login_url='fruver-acceso')
def datosbanco(request):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')
    #Asignamos el usuario actual a una variable current_user y obtenemos la fecha y la hora, para dejar registrado quién hizo la última modificación
    current_user = request.user
    date = datetime.now()
    fecha = date.strftime('%d-%m-%Y')
    hora = date.strftime('%H:%M')
    #Instanciamos un objeto de la clase CuentaBancaria
    cuenta = CuentaBancaria.objects.first()
    account = CuentaBancaria.objects.filter(pk=1)
    #Generamos un formulario para los datos de la cuenta bancaria. Si ya existen, los mostramos al usuario
    form = FormularioCuentaBancaria(request.POST or None, instance=cuenta)
    #Si los datos del formulario son válidos, guardamos los cambios y dejamos registrado quién los realizó
    if form.is_valid():
        form.save()
        account.update(vendedor=current_user)
        messages.success(request,'Los datos de la cuenta se han guardado con éxito')
        return redirect('fruver-datosbanco')
    context = {'cuenta': cuenta, 'form': form, 'fecha': fecha, 'hora': hora,}
    return render(request, 'Home/datosbanco.html', context)



#Muestra el listado de vendedores, desde donde se puede acceder a las funciones para crear nuevo vendedor, editar vendedor, o eliminar vendedor
@login_required(login_url='fruver-acceso')
def gestionarvendedor(request):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')
    #Query hace filtro para obtener a los usuarios cuyo atributo is_staff es True, se muestran en el listado de vendedores del html
    vendedores = Usuario.objects.filter(is_staff=True)
    #Generamos el formulario para crear un nuevo vendedor
    form = FormularioCrearUsuario()
    if request.method == 'POST':
        form = FormularioCrearUsuario(request.POST)
        #Si los datos ingresados al formulario son válidos, se crea un nuevo vendedor
        if form.is_valid():
            form.instance.is_staff = True  #Fija en verdadero el atributo is_staff para crear usuario perfil vendedor
            form.save()
            user = form.cleaned_data.get('nombre_usuario')
            messages.success(request,'¡La cuenta de vendedor ' + user + ' ha sido creada con éxito!')
            return redirect('fruver-gestionarvendedor')
    #Pasamos el formulario y el dataset de los vendedores, para renderizarlos junto al html
    context = {'form': form, 'vendedores': vendedores}
    return render(request, 'Home/gestionarvendedor.html', context)



#Editar datos de vendedor
@login_required(login_url='fruver-acceso')
def editarvendedor(request, usuario_id):
    #instanciamos al usuario actual y verificamos que sea staff, si no lo es, se le redirige a la página principal
    current_user = request.user
    if current_user.is_staff != 1:
        return redirect('fruver-home')
    #Instanciamos el vendedor cuyo id corresponda al argumento usuario_id recibido al comienzo de esta función
    usuario = Usuario.objects.get(pk=usuario_id)
    #Generamos un formulario para modificar los datos, y mostramos los ya existentes
    form = FormularioEditarVendedor(request.POST or None, instance=usuario)
    #Si los datos ingresados son válidos, guardamos los cambios y redirigimos al listado de vendedores 
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
    #Instanciamos el vendedor cuyo id corresponda al argumento usuario_id recibido al comienzo de esta función, y lo eliminamos mediante el método delete()
    usuario = Usuario.objects.get(pk=usuario_id)
    usuario.delete()
    messages.success(request,'El usuario ha sido eliminado correctamente.')
    return redirect('fruver-gestionarvendedor')