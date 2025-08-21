import calendar
from django.shortcuts import render
from django.utils import timezone
from collections import defaultdict
from .models import Evento

def calendario_view(request):
    agora = timezone.now()
    ano = agora.year
    mes = agora.month

    cal = calendar.Calendar()
    # Pega uma lista de semanas, onde cada semana é uma lista de objetos 'date'
    dias_do_mes_datas = cal.monthdatescalendar(ano, mes)
    
    eventos = Evento.objects.filter(data_evento__year=ano, data_evento__month=mes)
    
    # Agrupa os eventos por dia em um dicionário
    eventos_por_dia = defaultdict(list)
    for evento in eventos:
        eventos_por_dia[evento.data_evento].append(evento)

    # CORREÇÃO PRINCIPAL: Cria uma nova estrutura de dados
    # que combina a data com sua lista de eventos correspondente.
    calendario_com_eventos = []
    for semana in dias_do_mes_datas:
        semana_com_eventos = []
        for dia in semana:
            # Para cada dia, adicionamos uma tupla: (objeto_date, lista_de_eventos)
            semana_com_eventos.append((dia, eventos_por_dia[dia]))
        calendario_com_eventos.append(semana_com_eventos)

    context = {
        # Passa a nova estrutura para o template
        'calendario_semanas': calendario_com_eventos, 
        'mes_atual': timezone.datetime(ano, mes, 1),
        'eventos_lista': eventos,
        'today': agora.date(),
        'week_days': ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sab"],
    }
    return render(request, 'Calendario/calendario.html', context)