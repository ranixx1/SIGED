# Mural/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_http_methods
from .models import Card
from .forms import CardForm

@staff_member_required
def criar_card(request):
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('App:home')
    else:
        form = CardForm()
    return render(request, 'criar_card.html', {'form': form})

@staff_member_required
@require_http_methods(["GET", "POST"])
def editar_card(request, id):
    card = get_object_or_404(Card, id=id)
    if request.method == 'POST':
        form = CardForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            return redirect('App:home')
    else:
        form = CardForm(instance=card)
    return render(request, 'editar_card.html', {'form': form, 'card': card})

@staff_member_required
@require_http_methods(["POST"])
def deletar_card(request, id):
    card = get_object_or_404(Card, id=id)
    card.delete()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    return redirect('App:home')