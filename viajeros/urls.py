
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Página principal
    path('ver_destino/', views.ver_destino, name='ver_destino'),
    path('ver_pais/', views.ver_pais, name='ver_pais'),
    path('agregar_pasajero/', views.agregar_pasajero, name='agregar_pasajero'),
    path('agregar_ciudad/', views.agregar_ciudad, name='agregar_ciudad'),
]

