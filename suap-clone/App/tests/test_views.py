
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Card, Chamado 
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

class AdminViewsTestCase(BaseTestCase):
    """ Testes para as views de administração (dashboard, etc.) """

    def setUp(self):
        super().setUp()
        Chamado.objects.create(criado_por=self.user, assunto='Aberto 1', status='aberto')
        Chamado.objects.create(criado_por=self.user, assunto='Resolvido 1', status='resolvido')

    def test_dashboard_admin_access_by_staff(self):
        self.client.login(username='staffuser', password='password123')
        response = self.client.get(reverse('dashboard_admin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'App/pages/dashboard_admin.html')
        
        # Testa o contexto
        self.assertEqual(response.context['total_chamados'], 3)
        self.assertEqual(response.context['chamados_abertos'], 2)
        self.assertEqual(response.context['chamados_resolvidos'], 1)

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