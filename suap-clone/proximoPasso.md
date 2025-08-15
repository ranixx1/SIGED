
# Guia de Refatoração: De Monolítico para Apps Dedicados

Este guia detalha o processo de refatoração de um projeto Django, movendo a lógica de um único `App` monolítico para múltiplos apps focados em funcionalidades específicas (`mural` e `chamados`). Seguir estes passos garantirá uma arquitetura de projeto mais organizada, manutenível e escalável.

## Passo 1: A Nova Estrutura de Apps

O primeiro passo é criar os novos apps que irão abrigar as funcionalidades. No terminal, na raiz do seu projeto (onde o `manage.py` está localizado), execute os seguintes comandos:

```bash
python manage.py startapp mural
python manage.py startapp chamados
```
## Passo 2: Mover os Models
Vamos mover as classes dos models do antigo App/models.py para os seus novos lares.

1. mural/models.py
Mova a classe Card para este ficheiro.

```python

# mural/models.py
from django.db import models

class Card(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()

    def __str__(self):
        return self.titulo
2. chamados/models.py
Mova as classes Chamado e AtualizacaoChamado para este ficheiro.

Python

# chamados/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Chamado(models.Model):
    STATUS_CHOICES = [
        ('aberto', 'Aberto'),
        ('em_analise', 'Em Análise'),
        ('resolvido', 'Resolvido'),
        ('fechado', 'Fechado'),
    ]
    URGENCIA_CHOICES = [
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta'),
    ]
    SETOR_CHOICES = [
        ('ti', 'TI'),
        ('rh', 'RH'),
        ('financeiro', 'Financeiro'),
        ('manutencao', 'Manutenção'),
        ('limpeza', 'Limpeza'),
        ('outros', 'Outros'),
    ]

    criado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    assunto = models.CharField(max_length=200)
    descricao = models.TextField()
    setor = models.CharField(max_length=20, choices=SETOR_CHOICES)
    urgencia = models.CharField(max_length=10, choices=URGENCIA_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberto')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Chamado #{self.id} - {self.assunto}"

class AtualizacaoChamado(models.Model):
    chamado = models.ForeignKey(Chamado, on_delete=models.CASCADE)
    responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status_anterior = models.CharField(max_length=20)
    status_novo = models.CharField(max_length=20)
    mensagem = models.TextField(blank=True)
    data_atualizacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Atualização #{self.id}"

```

## 3. Limpe App/models.py
Após a movimentação, o ficheiro App/models.py deve ficar vazio.

Passo 3: Atualizar settings.py
Adicione os novos apps à lista INSTALLED_APPS no ficheiro core/settings.py.

```python
# core/settings.py

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'usuarios',
    'App',
    'mural',      # <-- Adicionar
    'chamados',   # <-- Adicionar
    'channels',
]
```

## Passo 4: Gerir as Migrações (Passo Crucial)
Para evitar a recriação de tabelas, informaremos ao Django sobre a mudança de localização dos modelos.

1. Especifique as Tabelas Existentes
Adicione uma classe Meta a cada um dos seus modelos movidos, especificando o nome da tabela antiga (applabel_modelname).

Em mural/models.py:

```python

# mural/models.py
class Card(models.Model):
    # ... seus campos ...
    class Meta:
        db_table = 'App_card' # <-- Informa ao Django qual tabela usar
```

Em chamados/models.py:

```python

# chamados/models.py
class Chamado(models.Model):
    # ... seus campos ...
    class Meta:
        db_table = 'App_chamado' # <-- Informa ao Django qual tabela usar

class AtualizacaoChamado(models.Model):
    # ... seus campos ...
    class Meta:
        db_table = 'App_atualizacaochamado' # <-- Informa ao Django qual tabela usar
```
2. Gere as Novas Migrações
Execute o comando para criar os ficheiros de migração para os novos apps.

```bash

python manage.py makemigrations mural
python manage.py makemigrations chamados

```

## 3. Aplique as Migrações "Falsas"
Este comando atualiza o estado das migrações no Django sem alterar a estrutura do banco de dados.

```bash

python manage.py migrate --fake-initial

```
## Passo 5: Mover Views e URLs
1. Crie os Ficheiros de URL
mural/urls.py

chamados/urls.py

2. Mova as URLs de App/urls.py
Para mural/urls.py:

```python

# mural/urls.py
from django.urls import path
from . import views

app_name = 'mural'

urlpatterns = [
    path('cards/novo/', views.criar_card, name='criar_card'),
    path('cards/editar/<int:id>/', views.editar_card, name='editar_card'),
    path('cards/deletar/<int:id>/', views.deletar_card, name='deletar_card'),
]
```

Para chamados/urls.py:

```python

# chamados/urls.py
from django.urls import path
from . import views

app_name = 'chamados'

urlpatterns = [
    path('', views.chamados, name='chamados'),
    path('criar/', views.criar_chamado, name='criar_chamado'),
    path('meus/', views.ver_chamados, name='ver_chamados'),
    path('meus/<int:id>/', views.detalhe_chamado, name='detalhe_chamado'),
    path('admin/', views.ver_chamados_admin, name='ver_chamados_admin'),
]
```
## 3. Mova as Views de App/views.py
Mova as views criar_card, editar_card, deletar_card para mural/views.py.

Mova as views chamados, criar_chamado, ver_chamados, detalhe_chamado, ver_chamados_admin para chamados/views.py.

As views home e dashboard_admin devem permanecer em App/views.py.

## 4. Atualize a Configuração de URLs Principal

core/urls.py:

```python

# core/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),
    path('home/', include('App.urls')),
    path('mural/', include('mural.urls')),
    path('chamados/', include('chamados.urls')),
]

```
App/urls.py (versão limpa):

```python
# App/urls.py
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', login_required(views.home), name='home'),
    path('dashboard-admin/', views.dashboard_admin, name='dashboard_admin'),
]
```

## Passo 6: Mover Templates e Atualizar Referências
1. Crie Novas Pastas de Templates
mural/templates/mural/

chamados/templates/chamados/

2. Mova os Ficheiros
Mova criar_card.html, editar_card.html, deletar_card.html para mural/templates/mural/.

Mova chamado.html, ver_chamados.html, detalhe_chamado.html, ver_chamados_admin.html para chamados/templates/chamados/.

3. Atualize as Referências de URL nos Templates
Use o app_name definido nos ficheiros urls.py para referenciar as rotas corretamente.

```html
{% url 'criar_card' %} torna-se {% url 'mural:criar_card' %}

{% url 'criar_chamado' %} torna-se {% url 'chamados:criar_chamado' %}
```

Passo 7: Mover Forms e Admin
Finalmente, organize os ficheiros restantes:

Crie mural/forms.py e chamados/forms.py e mova as classes CardForm e ChamadoForm para os respetivos ficheiros.

Crie mural/admin.py e chamados/admin.py e mova os registros do Django Admin (admin.site.register) para os apps correspondentes.