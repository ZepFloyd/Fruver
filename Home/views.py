from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'Home/index.html')

def login(request):
    return render(request, 'Home/login.html')

def registro(request):
    return render(request, 'Home/registro.html')

def frutas(request):
    return render(request, 'Home/frutas.html')

def verduras(request):
    return render(request, 'Home/verduras.html')

def carrito(request):
    return render(request, 'Home/carrito.html')