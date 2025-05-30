# App/admin.py

from django.contrib import admin
from .models import Card, Chamado, AtualizacaoChamado, ChatMessage

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'descricao')
    search_fields = ('titulo', 'descricao')

class AtualizacaoInline(admin.TabularInline):
    model = AtualizacaoChamado
    extra = 0
    readonly_fields = ('data_atualizacao', 'responsavel', 'status_anterior')
    
    def has_add_permission(self, request, obj=None):
        return False

@admin.register(Chamado)
class ChamadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'assunto', 'criado_por', 'setor', 'status', 'urgencia', 'data_criacao', 'chat_room_name') # <--- NOVO CAMPO AQUI
    list_filter = ('status', 'urgencia', 'setor', 'chat_room_name') # Adicione chat_room_name ao filtro
    search_fields = ('assunto', 'descricao', 'criado_por__username', 'chat_room_name') # Adicione à busca
    readonly_fields = ('data_criacao', 'chat_room_name',) # chat_room_name deve ser somente leitura aqui
    inlines = [AtualizacaoInline]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(criado_por=request.user)
    
    def save_model(self, request, obj, form, change):
        if change and 'status' in form.changed_data:
            AtualizacaoChamado.objects.create(
                chamado=obj,
                responsavel=request.user,
                status_anterior=form.initial['status'],
                status_novo=obj.status,
                mensagem="Status alterado pelo admin"
            )
        super().save_model(request, obj, form, change)

@admin.register(AtualizacaoChamado)
class AtualizacaoChamadoAdmin(admin.ModelAdmin):
    list_display = ('chamado', 'status_anterior', 'status_novo', 'responsavel', 'data_atualizacao')
    list_filter = ('status_novo',)
    search_fields = ('chamado__assunto', 'mensagem')
    readonly_fields = ('chamado', 'responsavel', 'status_anterior', 'status_novo', 'data_atualizacao')

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('room_name', 'user', 'message', 'timestamp')
    list_filter = ('room_name', 'timestamp')
    search_fields = ('user__username', 'message')
    readonly_fields = ('room_name', 'user', 'message', 'timestamp')