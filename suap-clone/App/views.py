from django.shortcuts import render, redirect, get_object_or_404
from .models import Card
from .forms import CardForm
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

def home(request):
    if not request.user.is_authenticated:
        return redirect('usuarios/login')
    cards = Card.objects.all().order_by('-id')  # Ordena do mais novo para o mais antigo
    return render(request, 'App/home.html', {'cards': cards})

@login_required
def criar_card(request):
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CardForm()
    
    return render(request, 'App/criar_card.html', {'form': form})

@login_required
def editar_card(request, id):
    card = get_object_or_404(Card, id=id)
    if request.method == 'POST':
        form = CardForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CardForm(instance=card)
    
    return render(request, 'App/editar_card.html', {'form': form, 'card': card})

@login_required
def deletar_card(request, id):
    card = get_object_or_404(Card, id=id)
    if request.method == 'POST':
        card.delete()
        return redirect('home')
    
    return render(request, 'App/deletar_card.html', {'card': card})