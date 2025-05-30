# App/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.template.loader import render_to_string
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # Corrigido aqui: PageNotAnInteger
from django.db.models import Q # Importe Q para queries complexas

from .models import Card, Chamado, ChatMessage # Importe seus modelos
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

@login_required
def iniciar_chat_suporte(request):
    """
    Inicia ou retoma um chat de suporte para o usuário, gerando um ticket (Chamado).
    """
    user = request.user

    # Tentamos encontrar um chamado de chat de suporte aberto para este usuário
    try:
        chat_ticket = Chamado.objects.filter(
            criado_por=user,
            chat_room_name__isnull=False # Garante que é um chamado de chat
        ).exclude(status__in=['resolvido', 'fechado']).first()

    except Chamado.DoesNotExist:
        chat_ticket = None

    if chat_ticket:
        # Se o usuário já tem um ticket de chat ativo, redireciona para a sala existente
        room_name = chat_ticket.chat_room_name
        messages.info(request, "Você já possui um chat de suporte ativo.")
    else:
        # Se não houver ticket ativo, cria um novo Chamado
        try:
            with transaction.atomic(): # Garante que a operação seja atômica
                # Crie o Chamado primeiro para obter o ID
                new_chamado = Chamado.objects.create(
                    criado_por=user,
                    assunto=f"Suporte via Chat - Usuário {user.username}",
                    descricao=f"Chamado de suporte iniciado via chat pelo usuário {user.username}.",
                    setor='ti', # Ou 'suporte_chat' se você adicionou em models.py
                    urgencia='media', # Defina uma urgência padrão para chats
                    status='aberto',
                )

                # Defina o room_name baseado no ID do Chamado
                room_name = f'chat_suporte_{new_chamado.id}'
                new_chamado.chat_room_name = room_name # Vincula o room_name ao chamado
                new_chamado.save()

                messages.success(request, f"Seu chamado de suporte #{new_chamado.id} foi criado. Iniciando chat.")
        except Exception as e:
            messages.error(request, f"Não foi possível iniciar o chat de suporte: {e}")
            return redirect('home')

    return redirect('chat_room', room_name=room_name)

# VIEW PARA O CHAT
@login_required
def chat_room(request, room_name):
    # Carrega as últimas 50 mensagens para a sala específica
    messages_in_room = ChatMessage.objects.filter(room_name=room_name).order_by('timestamp')[:50]

    # Opcional: Para passar o objeto Chamado associado ao template do chat
    chamado_associado = None
    if room_name.startswith('chat_suporte_'):
        try:
            # Tenta encontrar o chamado pelo chat_room_name
            chamado_id = room_name.split('_')[-1]
            chamado_associado = Chamado.objects.get(id=chamado_id, chat_room_name=room_name)
        except (Chamado.DoesNotExist, ValueError):
            messages.warning(request, "Chamado associado a este chat não encontrado.")
            # Você pode querer redirecionar ou lidar com isso de outra forma
            pass

    return render(request, 'App/pages/chat/chat_room.html', {
        'room_name': room_name,
        'messages': messages_in_room, # Use 'messages_in_room' para evitar conflito com 'messages' do Django.
        'chamado_associado': chamado_associado, # Passa o chamado associado, se existir
    })

@staff_member_required # Apenas usuários com is_staff=True podem acessar
def dashboard_admin(request):
    total_chamados = Chamado.objects.count()
    chamados_abertos = Chamado.objects.filter(status='aberto').count()
    chamados_em_analise = Chamado.objects.filter(status='em_analise').count()
    chamados_resolvidos = Chamado.objects.filter(status='resolvido').count()


    # Tickets de chat (Chamados que são do tipo 'chat_suporte')
    tickets_chat_pendentes = Chamado.objects.filter(
        chat_room_name__isnull=False
    ).exclude(status__in=['resolvido', 'fechado']).count()

    tickets_chat_resolvidos = Chamado.objects.filter(
        chat_room_name__isnull=False,
        status='resolvido'
    ).count()

    context = {
        'total_chamados': total_chamados,
        'chamados_abertos': chamados_abertos,
        'chamados_em_analise': chamados_em_analise,
        'chamados_resolvidos': chamados_resolvidos,
        'tickets_chat_pendentes': tickets_chat_pendentes,
        'tickets_chat_resolvidos': tickets_chat_resolvidos,
    }
    return render(request, 'App/pages/dashboard_admin.html', context)

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

    # Filtrar apenas tickets de chat, se o parâmetro 'chat_ticket' estiver presente
    chat_ticket_filter = request.GET.get('chat_ticket')
    if chat_ticket_filter == 'true':
        chamados_list = chamados_list.filter(chat_room_name__isnull=False)

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
        'chat_ticket_filter': chat_ticket_filter == 'true',
        'chamado_status_choices': chamado_status_choices, # Passa as escolhas para o template
    })