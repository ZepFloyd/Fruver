from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='fruver-home'), # HomePage www.fruver.com/
]