from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', login_required(views.home), name='home'), 
    path('cards/novo/', views.criar_card, name='criar_card'),
    path('cards/editar/<int:id>/', views.editar_card, name='editar_card'),
    path('cards/deletar/<int:id>/', views.deletar_card, name='deletar_card'),
    path('chamados/', views.chamados, name='chamados'),
    path('chamado/criar/', views.criar_chamado, name='criar_chamado'),
    path('meus-chamados/', views.ver_chamados, name='ver_chamados'),
    path('meus-chamados/<int:id>/', views.detalhe_chamado, name='detalhe_chamado'),
    


]