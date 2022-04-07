from django.forms import PasswordInput
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import messages

# Create your views here.

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('fruver-home')
    else:    
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request,'¡Muy bien ' + user + ', su cuenta ha sido creada con éxtio!')
                return redirect('fruver-acceso')

        context = {'form': form}
        return render(request, 'Home/registerPage.html', context)

def home(request):
    return render(request, 'Home/index.html')

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
                return redirect('fruver-mainmenu')
            else:
                return messages.info(request, 'Nombre de usuario o contraseña incorrectos')
        return render(request, 'Home/acceso.html')

def salir(request):
    logout(request)
    return redirect('fruver-home')

def registro(request):
    return render(request, 'Home/registro.html')

def frutas(request):
    return render(request, 'Home/frutas.html')

def verduras(request):
    return render(request, 'Home/verduras.html')

def carrito(request):
    return render(request, 'Home/carrito.html')

@login_required(login_url='fruver-acceso')
def mainmenu(request):
    return render(request, 'Home/mainmenu.html')

@login_required(login_url='fruver-acceso')
def datosbanco(request):
    return render(request, 'Home/datosbanco.html')
