# Mural/urls.py
from django.urls import path
from . import views

app_name = 'Mural'  # Define o namespace para as URLs deste app

urlpatterns = [
    path('cards/novo/', views.criar_card, name='criar_card'),
    path('cards/editar/<int:id>/', views.editar_card, name='editar_card'),
    path('cards/deletar/<int:id>/', views.deletar_card, name='deletar_card'),
]