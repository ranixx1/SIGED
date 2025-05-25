from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.template.loader import render_to_string
from .models import Card, Chamado, ChatMessage 
from .forms import CardForm, ChamadoForm


def home(request):
    cards = Card.objects.all().order_by('-id')
    return render(request, 'App/home.html', {'cards': cards})

@login_required
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

@login_required
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

@login_required
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
    chamados = Chamado.objects.filter(criado_por=request.user).order_by('-data_criacao')
    return render(request, 'App/pages/central/ver_chamados.html', {'chamados': chamados})


@login_required
def detalhe_chamado(request, id):
    chamado = get_object_or_404(Chamado, id=id)  
    return render(request, 'App/pages/central/detalhe_chamado.html', {
        'chamado': chamado,

    })

# VIEW PARA O CHAT
@login_required
def chat_room(request, room_name):
    # Carrega as últimas 50 mensagens para a sala específica
    messages = ChatMessage.objects.filter(room_name=room_name).order_by('timestamp')[:50]
    return render(request, 'App/pages/chat/chat_room.html', {
        'room_name': room_name,
        'messages': messages,
    })