# Chamados/views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Chamado
from .forms import ChamadoForm 

@login_required
def chamados(request):
    return render(request, 'Chamados/chamado.html')

@login_required
def criar_chamado(request):
    if request.method == 'POST':
        form = ChamadoForm(request.POST)
        if form.is_valid():
            chamado = form.save(commit=False)
            chamado.criado_por = request.user
            chamado.save()
            return JsonResponse({'success': True, 'message': 'Chamado criado com sucesso!'})
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return render(request, 'Chamados/chamado.html')

@login_required
def ver_chamados(request):
    chamados_list = Chamado.objects.filter(criado_por=request.user).order_by('-data_criacao')
    return render(request, 'Chamados/ver_chamados.html', {'chamados': chamados_list})

@login_required
def detalhe_chamado(request, id):
    chamado = get_object_or_404(Chamado, id=id, criado_por=request.user) # Garante que o user só veja os seus
    return render(request, 'Chamados/detalhe_chamado.html', {'chamado': chamado})

@staff_member_required
def ver_chamados_admin(request):
    chamados_list = Chamado.objects.all().order_by('-data_criacao')
    # ... (lógica de filtro e paginação que estava em App/views.py)
    status_filter = request.GET.get('status')
    if status_filter:
        chamados_list = chamados_list.filter(status=status_filter)
    search_query = request.GET.get('search')
    if search_query:
        chamados_list = chamados_list.filter(
            Q(assunto__icontains=search_query) |
            Q(descricao__icontains=search_query) |
            Q(criado_por__username__icontains=search_query)
        )
    paginator = Paginator(chamados_list, 10)
    page_number = request.GET.get('page')
    try:
        chamados = paginator.page(page_number)
    except PageNotAnInteger:
        chamados = paginator.page(1)
    except EmptyPage:
        chamados = paginator.page(paginator.num_pages)

    context = {
        'chamados': chamados,
        'status_filter': status_filter,
        'search_query': search_query,
        'chamado_status_choices': Chamado.STATUS_CHOICES,
    }
    return render(request, 'Chamados/ver_chamados_admin.html', context)