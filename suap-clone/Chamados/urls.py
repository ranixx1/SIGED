# Chamados/urls.py
from django.urls import path
from . import views

app_name = 'Chamados' 

urlpatterns = [
    path('', views.chamados, name='chamados'),
    path('criar/', views.criar_chamado, name='criar_chamado'),
    path('meus/', views.ver_chamados, name='ver_chamados'),
    path('meus/<int:id>/', views.detalhe_chamado, name='detalhe_chamado'),
    path('admin/', views.ver_chamados_admin, name='ver_chamados_admin'),
]