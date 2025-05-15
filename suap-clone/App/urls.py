from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', login_required(views.home), name='home'), 
    path('cards/novo/', views.criar_card, name='criar_card'),
    path('cards/editar/<int:id>/', views.editar_card, name='editar_card'),
    path('cards/deletar/<int:id>/', views.deletar_card, name='deletar_card'),
    path('chamados/', views.chamados, name='chamados'),
]