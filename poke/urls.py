from django.urls import path
from . import views

app_name = 'poke'

urlpatterns = [
    path('pokemon/', views.pokepost, name='pokepost'),
    path('pokemon/<int:pk>/', views.PokeDetailView.as_view(), name='index'),
    path('pokemon/pokepost/<int:pk>/', views.pokepost, name='pokepost'),
    
    path('moves/', views.movepost, name='movepost'),
    path('moves/<int:pk>', views.MoveDetailView.as_view(), name='moves'),
    path('moves/movepost/<int:pk>/', views.movepost, name='movepost'),

    path('pokemon/pgl/', views.pgl, name='pgl'),
]