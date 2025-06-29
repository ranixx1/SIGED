
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Card, Chamado, ChatMessage 
from ..forms import CardForm, ChamadoForm      


class BaseTestCase(TestCase):
    """
    Configuração base para os testes, criando usuários e o cliente de teste.
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.staff_user = User.objects.create_user(username='staffuser', password='password123', is_staff=True)
        self.card = Card.objects.create(titulo='Card Teste', descricao='Descricao do card')

class CardViewsTestCase(BaseTestCase):
    """ Testes para as views relacionadas a 'Card' """

    def test_home_view(self):
        self.client.login(username='testuser', password='password123')

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200) 
        self.assertTemplateUsed(response, 'App/home.html')
        self.assertIn(self.card, response.context['cards'])

    def test_criar_card_get_request_as_staff(self):
        self.client.login(username='staffuser', password='password123')
        response = self.client.get(reverse('criar_card'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], CardForm)

    def test_criar_card_redirects_if_not_staff(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('criar_card'))
        self.assertEqual(response.status_code, 302) # Redireciona para a página de login
        self.assertIn('/admin/login/', response.url) 

    def test_criar_card_post_request_success(self):
        self.client.login(username='staffuser', password='password123')
        card_count_before = Card.objects.count()
        response = self.client.post(reverse('criar_card'), {'titulo': 'Novo Card', 'descricao': 'Nova Descricao'})
        self.assertEqual(response.status_code, 302) # Redireciona para 'home'
        self.assertEqual(Card.objects.count(), card_count_before + 1)
        self.assertTrue(Card.objects.filter(titulo='Novo Card').exists())

    def test_criar_card_post_ajax_success(self):
        self.client.login(username='staffuser', password='password123')
        response = self.client.post(
            reverse('criar_card'),
            {'titulo': 'Card via AJAX', 'descricao': 'Descricao'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('html', data)
        self.assertTrue(Card.objects.filter(titulo='Card via AJAX').exists())

    def test_deletar_card_as_staff(self):
        self.client.login(username='staffuser', password='password123')
        card_to_delete = Card.objects.create(titulo='Para Deletar', descricao='...')
        card_count_before = Card.objects.count()
        
        response = self.client.post(reverse('deletar_card', args=[card_to_delete.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Card.objects.count(), card_count_before - 1)
        
    def test_deletar_card_get_not_allowed(self):
        self.client.login(username='staffuser', password='password123')
        response = self.client.get(reverse('deletar_card', args=[self.card.id]))
        self.assertEqual(response.status_code, 405) # Method Not Allowed


class ChamadoViewsTestCase(BaseTestCase):
    """ Testes para as views relacionadas a 'Chamado' """

    def setUp(self):
        # Chama o setUp da classe pai para criar usuários
        super().setUp()
        # Cria chamados específicos para estes testes
        self.chamado_user1 = Chamado.objects.create(
            criado_por=self.user,
            assunto='Problema User 1',
            descricao='Detalhes do problema 1'
        )
        self.user2 = User.objects.create_user(username='testuser2', password='password123')
        self.chamado_user2 = Chamado.objects.create(
            criado_por=self.user2,
            assunto='Problema User 2',
            descricao='Detalhes do problema 2'
        )

    def test_criar_chamado_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('criar_chamado'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/usuarios/login/', response.url)

    def test_criar_chamado_post_ajax_success(self):
        self.client.login(username='testuser', password='password123')
        chamado_count_before = Chamado.objects.count()

        form_data = {
            'assunto': 'Novo Chamado via AJAX',
            'descricao': 'Esta é uma descrição com mais de vinte caracteres para o teste.',
            'setor': 'ti', # Exemplo
            'urgencia': 'media' # Exemplo
        }

        response = self.client.post(
            reverse('criar_chamado'),
            form_data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )


        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(Chamado.objects.count(), chamado_count_before + 1)

        novo_chamado = Chamado.objects.latest('data_criacao')
        self.assertEqual(novo_chamado.criado_por, self.user)
        self.assertEqual(novo_chamado.assunto, 'Novo Chamado via AJAX')

    def test_criar_chamado_post_ajax_invalid_form(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(
            reverse('criar_chamado'),
            {'assunto': '', 'descricao': ''}, # Dados inválidos
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data['success'])
        self.assertIn('errors', data)

    def test_ver_chamados_shows_only_own_chamados(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('ver_chamados'))
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.chamado_user1, response.context['chamados'])
        self.assertNotIn(self.chamado_user2, response.context['chamados'])


class ChatViewsTestCase(BaseTestCase):
    """ Testes para as views relacionadas ao Chat """

    def test_iniciar_chat_suporte_creates_new_ticket_and_redirects(self):
        self.client.login(username='testuser', password='password123')
        chamado_count_before = Chamado.objects.count()

        response = self.client.get(reverse('iniciar_chat_suporte'))
        
        self.assertEqual(Chamado.objects.count(), chamado_count_before + 1)
        new_chamado = Chamado.objects.latest('data_criacao')
        
        self.assertEqual(new_chamado.criado_por, self.user)
        self.assertIsNotNone(new_chamado.chat_room_name)
        
        expected_redirect_url = reverse('chat_room', args=[new_chamado.chat_room_name])
        self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)

    def test_iniciar_chat_suporte_uses_existing_ticket(self):
        self.client.login(username='testuser', password='password123')
        # Cria um chamado de chat pré-existente e ativo para o usuário
        existing_chat = Chamado.objects.create(
            criado_por=self.user,
            assunto='Chat antigo',
            descricao='...',
            status='aberto',
            chat_room_name='chat_suporte_999'
        )
        chamado_count_before = Chamado.objects.count()
        
        response = self.client.get(reverse('iniciar_chat_suporte'))
        
        # Garante que nenhum chamado novo foi criado
        self.assertEqual(Chamado.objects.count(), chamado_count_before)
        
        # Garante que o redirecionamento foi para a sala existente
        expected_redirect_url = reverse('chat_room', args=[existing_chat.chat_room_name])
        self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)

    def test_chat_room_view(self):
        self.client.login(username='testuser', password='password123')
        room_name = 'chat_suporte_123'
        chamado = Chamado.objects.create(criado_por=self.user, id=123, chat_room_name=room_name)
        msg = ChatMessage.objects.create(room_name=room_name, user=self.user, message='Olá, mundo')

        response = self.client.get(reverse('chat_room', args=[room_name]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'App/pages/chat/chat_room.html')
        self.assertEqual(response.context['room_name'], room_name)
        self.assertEqual(response.context['chamado_associado'], chamado)
        self.assertIn(msg, response.context['messages'])


class AdminViewsTestCase(BaseTestCase):
    """ Testes para as views de administração (dashboard, etc.) """

    def setUp(self):
        super().setUp()
        Chamado.objects.create(criado_por=self.user, assunto='Aberto 1', status='aberto')
        Chamado.objects.create(criado_por=self.user, assunto='Resolvido 1', status='resolvido')
        Chamado.objects.create(criado_por=self.user, assunto='Chat 1', chat_room_name='chat_1', status='aberto')

    def test_dashboard_admin_access_by_staff(self):
        self.client.login(username='staffuser', password='password123')
        response = self.client.get(reverse('dashboard_admin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'App/pages/dashboard_admin.html')
        
        # Testa o contexto
        self.assertEqual(response.context['total_chamados'], 3)
        self.assertEqual(response.context['chamados_abertos'], 2)
        self.assertEqual(response.context['chamados_resolvidos'], 1)
        self.assertEqual(response.context['tickets_chat_pendentes'], 1)

    def test_dashboard_admin_redirects_non_staff(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('dashboard_admin'))
        self.assertEqual(response.status_code, 302)

    def test_ver_chamados_admin_view(self):
        self.client.login(username='staffuser', password='password123')
        response = self.client.get(reverse('ver_chamados_admin'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['chamados']), 3)

    def test_ver_chamados_admin_filter_by_status(self):
        self.client.login(username='staffuser', password='password123')
        response = self.client.get(reverse('ver_chamados_admin'), {'status': 'resolvido'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['chamados']), 1)
        self.assertEqual(response.context['chamados'][0].status, 'resolvido')
        
    def test_ver_chamados_admin_filter_by_search(self):
        self.client.login(username='staffuser', password='password123')
        response = self.client.get(reverse('ver_chamados_admin'), {'search': 'Aberto 1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['chamados']), 1)
        self.assertEqual(response.context['chamados'][0].assunto, 'Aberto 1')

    def test_ver_chamados_admin_filter_by_chat_ticket(self):
        self.client.login(username='staffuser', password='password123')
        response = self.client.get(reverse('ver_chamados_admin'), {'chat_ticket': 'true'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['chamados']), 1)
        self.assertIsNotNone(response.context['chamados'][0].chat_room_name)