from django.contrib import admin
from .models import Card

# Register your models here.
@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'descricao')
    search_fields = ('titulo', 'descricao')