# App/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# Importações corrigidas dos novos apps
from Mural.models import Card
from Chamados.models import Chamado

@login_required
def home(request):
    cards = Card.objects.all().order_by('-id')
    return render(request, 'App/home.html', {'cards': cards})

@staff_member_required
def dashboard_admin(request):
    total_chamados = Chamado.objects.count()
    chamados_abertos = Chamado.objects.filter(status='aberto').count()
    chamados_em_analise = Chamado.objects.filter(status='em_analise').count()
    chamados_resolvidos = Chamado.objects.filter(status='resolvido').count()
    chamados_recentes = Chamado.objects.order_by('-data_criacao')[:5]

    context = {
        'total_chamados': total_chamados,
        'chamados_abertos': chamados_abertos,
        'chamados_em_analise': chamados_em_analise,
        'chamados_resolvidos': chamados_resolvidos,
        'chamados_recentes': chamados_recentes,
    }
    return render(request, 'App/dashboard_admin.html', context)