# App/urls.py

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
    path('meus-chamados/', views.ver_chamados, name='ver_chamados'), # Esta linha está correta
    path('meus-chamados/<int:id>/', views.detalhe_chamado, name='detalhe_chamado'),

    # Rota para iniciar o chat de suporte
    path('chat/suporte/', login_required(views.iniciar_chat_suporte), name='iniciar_chat_suporte'),

    path('chat/<str:room_name>/', login_required(views.chat_room), name='chat_room'),
    path('dashboard-admin/', views.dashboard_admin, name='dashboard_admin'),
    path('admin/chamados/', views.ver_chamados_admin, name='ver_chamados_admin'), # Nova rota para admin
]