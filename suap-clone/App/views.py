# App/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.template.loader import render_to_string
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
from django.db.models import Q 

from .models import Card, Chamado 
from .forms import CardForm, ChamadoForm
from django.contrib.admin.views.decorators import staff_member_required

def home(request):
    cards = Card.objects.all().order_by('-id')
    return render(request, 'App/home.html', {'cards': cards})

@staff_member_required
def criar_card(request):
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                cards = Card.objects.all().order_by('-id')
                html = render_to_string('App/partials/card_list.html', {'cards': cards})
                return JsonResponse({'html': html})
            return redirect('home')
        elif request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = CardForm()

    return render(request, 'App/criar_card.html', {'form': form})

@staff_member_required
@require_http_methods(["GET", "POST"])
def editar_card(request, id):
    card = get_object_or_404(Card, id=id)
    if request.method == 'POST':
        form = CardForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('home')
        elif request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = CardForm(instance=card)

    return render(request, 'App/editar_card.html', {'form': form, 'card': card})

@staff_member_required
@require_http_methods(["POST"])
def deletar_card(request, id):
    card = get_object_or_404(Card, id=id)
    card.delete()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    return redirect('home')

@login_required
def chamados(request):
    return render(request, 'App/pages/central/chamado.html')

@login_required
def criar_chamado(request):
    if request.method == 'POST':
        form = ChamadoForm(request.POST)
        if form.is_valid():
            chamado = form.save(commit=False)
            chamado.criado_por = request.user
            chamado.save()

            return JsonResponse({
                'success': True,
                'message': 'Chamado criado com sucesso!'
            })

        # Se o formulário for inválido
        return JsonResponse({
            'success': False,
            'errors': form.errors
        }, status=400)

    # GET request - renderiza o template normalmente
    return render(request, 'App/pages/central/chamado.html')

@login_required
def ver_chamados(request):
    # Esta view é para o USUÁRIO ver SOMENTE SEUS chamados
    chamados = Chamado.objects.filter(criado_por=request.user).order_by('-data_criacao')
    return render(request, 'App/pages/central/ver_chamados.html', {'chamados': chamados})

@login_required
def detalhe_chamado(request, id):
    chamado = get_object_or_404(Chamado, id=id)
    return render(request, 'App/pages/central/detalhe_chamado.html', {
        'chamado': chamado,
    })


@staff_member_required # Apenas usuários com is_staff=True podem acessar
def dashboard_admin(request):
    total_chamados = Chamado.objects.count()
    chamados_abertos = Chamado.objects.filter(status='aberto').count()
    chamados_em_analise = Chamado.objects.filter(status='em_analise').count()
    chamados_resolvidos = Chamado.objects.filter(status='resolvido').count()

@staff_member_required # Apenas staff pode ver todos os chamados
def ver_chamados_admin(request):
    chamados_list = Chamado.objects.all().order_by('-data_criacao')

    # Filtrar por status
    status_filter = request.GET.get('status')
    if status_filter:
        statuses = status_filter.split(',')
        chamados_list = chamados_list.filter(status__in=statuses)
        

    # Filtrar por termo de busca (assunto, descrição ou username do criador)
    search_query = request.GET.get('search')
    if search_query:
        chamados_list = chamados_list.filter(
            Q(assunto__icontains=search_query) |
            Q(descricao__icontains=search_query) |
            Q(criado_por__username__icontains=search_query)
        )
    # Paginação
    paginator = Paginator(chamados_list, 10) # 10 chamados por página
    page_number = request.GET.get('page')

    try:
        chamados = paginator.page(page_number)
    except PageNotAnInteger:
        chamados = paginator.page(1)
    except EmptyPage:
        chamados = paginator.page(paginator.num_pages)

    # Adiciona as escolhas de status do Chamado para o template de filtro
    chamado_status_choices = Chamado.STATUS_CHOICES

    return render(request, 'App/pages/central/ver_chamados_admin.html', {
        'chamados': chamados,
        'status_filter': status_filter,
        'search_query': search_query,
        'chamado_status_choices': chamado_status_choices, 
    })