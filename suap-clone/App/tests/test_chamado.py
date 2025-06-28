from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

# Certifique-se de que App.models e App.forms estão corretos
# se o seu app não se chamar 'App', ajuste aqui!
from App.models import Chamado
from App.forms import ChamadoForm

User = get_user_model()

class ChamadoModelTest(TestCase):
    """Testes para o modelo Chamado."""

    def setUp(self):
        """Configurações iniciais para os testes de modelo."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        # CRIAÇÃO DO CHAMADO AJUSTADA PARA O SEU MODELO REAL
        self.chamado = Chamado.objects.create(
            criado_por=self.user,
            assunto='Problema com acesso ao sistema', # Seu campo 'assunto'
            descricao='Não consigo logar no sistema. O erro é 401.', # Seu campo 'descricao'
            setor='ti', # Um dos SETOR_CHOICES válidos
            urgencia='alta', # Um dos URGENCIA_CHOICES válidos
            status='aberto' # O status padrão já é 'aberto', mas especificando para clareza
        )

    def test_chamado_creation(self):
        """Verifica se um chamado é criado corretamente."""
        self.assertEqual(Chamado.objects.count(), 1)
        self.assertEqual(self.chamado.assunto, 'Problema com acesso ao sistema')
        self.assertEqual(self.chamado.criado_por, self.user)
        self.assertEqual(self.chamado.status, 'aberto') # Verifica o status inicial
        self.assertEqual(self.chamado.setor, 'ti')
        self.assertEqual(self.chamado.urgencia, 'alta')

    def test_chamado_str_representation(self):
        """Verifica a representação de string do modelo Chamado."""
        self.assertEqual(str(self.chamado), f"Chamado #{self.chamado.id} - Problema com acesso ao sistema")

    def test_chamado_status_default(self):
        """Verifica se o campo 'status' é 'aberto' por padrão."""
        novo_chamado = Chamado.objects.create(
            criado_por=self.user,
            assunto='Novo chamado de teste padrão',
            descricao='Esta é uma descrição de teste com mais de 20 caracteres.',
            setor='outros',
            urgencia='baixa'
        )
        self.assertEqual(novo_chamado.status, 'aberto')

class ChamadoFormTest(TestCase):
    """Testes para o formulário ChamadoForm."""

    def test_valid_chamado_form(self):
        """Verifica se o formulário é válido com dados corretos e completos."""
        data = {
            'assunto': 'Assunto do chamado com mais de 10 caracteres', # Min 10 caracteres
            'descricao': 'Esta é uma descrição detalhada com mais de 20 caracteres.', # Min 20 caracteres
            'setor': 'ti', # Escolha válida do modelo
            'urgencia': 'media' # Escolha válida do modelo
        }
        form = ChamadoForm(data=data)
        self.assertTrue(form.is_valid(), f"Formulário inválido com erros: {form.errors}")

    def test_invalid_chamado_form_short_assunto(self):
        """Verifica se o formulário é inválido com assunto muito curto."""
        data = {
            'assunto': 'Curto', # Menos de 10 caracteres
            'descricao': 'Esta é uma descrição detalhada com mais de 20 caracteres.',
            'setor': 'ti',
            'urgencia': 'media'
        }
        form = ChamadoForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('assunto', form.errors)
        self.assertIn("O assunto deve ter pelo menos 10 caracteres.", form.errors['assunto'])

    def test_invalid_chamado_form_short_descricao(self):
        """Verifica se o formulário é inválido com descrição muito curta."""
        data = {
            'assunto': 'Assunto do chamado com mais de 10 caracteres',
            'descricao': 'Curta.', # Menos de 20 caracteres
            'setor': 'ti',
            'urgencia': 'media'
        }
        form = ChamadoForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('descricao', form.errors)
        self.assertIn("A descrição deve ter pelo menos 20 caracteres.", form.errors['descricao'])

    def test_invalid_chamado_form_missing_required_fields(self):
        """Verifica se o formulário é inválido sem campos obrigatórios."""
        # Dados vazios ou incompletos
        form = ChamadoForm(data={})
        self.assertFalse(form.is_valid())
        # Espera erros para todos os campos obrigatórios: assunto, descricao, setor, urgencia
        self.assertEqual(len(form.errors), 4) # Agora esperando 4 erros

    def test_invalid_chamado_form_invalid_choice_setor(self):
        """Verifica se o formulário é inválido com escolha de setor inválida."""
        data = {
            'assunto': 'Assunto válido do chamado',
            'descricao': 'Esta é uma descrição detalhada com mais de 20 caracteres.',
            'setor': 'setor_invalido', # Escolha inválida
            'urgencia': 'media'
        }
        form = ChamadoForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('setor', form.errors)
        # >>> CORRIGIDO AQUI: Mensagem de erro do Django em Português
        self.assertIn("Faça uma escolha válida. 'setor_invalido' não é uma das escolhas disponíveis.", str(form.errors['setor']))


class ChamadoViewTest(TestCase):
    """Testes para as views de Chamado."""

    def setUp(self):
        """Configurações iniciais para os testes de view."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        # CRIAÇÃO DO CHAMADO AJUSTADA PARA O SEU MODELO REAL
        self.chamado = Chamado.objects.create(
            criado_por=self.user,
            assunto='Problema de Acesso ao APP',
            descricao='Não consigo logar no sistema, erro desconhecido persistente.',
            setor='ti',
            urgencia='alta'
        )
        # Loga o usuário para acessar views protegidas
        self.client.login(username='testuser', password='testpassword')

    def test_ver_chamados_view_authenticated(self):
        """Verifica se a view ver_chamados funciona para usuário autenticado."""
        response = self.client.get(reverse('ver_chamados'))
        self.assertEqual(response.status_code, 200) # HTTP 200 OK
        # >>> CORRIGIDO AQUI: Nome do template real
        self.assertTemplateUsed(response, 'App/pages/central/ver_chamados.html')
        self.assertContains(response, self.chamado.assunto) # Verifica se o assunto do chamado aparece na página

    def test_ver_chamados_view_unauthenticated(self):
        """Verifica redirecionamento para login se usuário não estiver autenticado."""
        self.client.logout() # Desloga o usuário
        response = self.client.get(reverse('ver_chamados'))
        self.assertEqual(response.status_code, 302) # HTTP 302 Found (redirecionamento)
        # Esta linha já foi corrigida para usar reverse('login') anteriormente.
        # O ERROR neste teste se deve a problemas com staticfiles na página de login.
        # Isso precisa ser resolvido na configuração de staticfiles do Django para testes,
        # ou garantindo que o 'logo.png' esteja acessível via 'collectstatic' ou 'STATICFILES_DIRS'.
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('ver_chamados')}")

    def test_criar_chamado_view_get(self):
        """Verifica se a view criar_chamado exibe o formulário corretamente via GET."""
        response = self.client.get(reverse('criar_chamado'))
        self.assertEqual(response.status_code, 200)
        # >>> CORRIGIDO AQUI: Nome do template real
        self.assertTemplateUsed(response, 'App/pages/central/chamado.html')
        self.assertIsInstance(response.context['form'], ChamadoForm) # Verifica se o formulário está no contexto

    def test_criar_chamado_view_post_valid_data(self):
        """Verifica se a view criar_chamado cria um novo chamado com dados válidos via POST."""
        initial_chamado_count = Chamado.objects.count()
        data = {
            'assunto': 'Novo Chamado de Teste Válido',
            'descricao': 'Esta é uma descrição de teste para o novo chamado com mais de 20 caracteres.',
            'setor': 'financeiro',
            'urgencia': 'baixa'
        }
        response = self.client.post(reverse('criar_chamado'), data)
        # >>> CORRIGIDO AQUI: Espera 302 (redirecionamento) se a view redirecionar corretamente.
        # SE A SUA VIEW NÃO ESTIVER REDIRECIONANDO APÓS O SUCESSO, ELA ESTÁ COM UM BUG.
        # A view DEVE retornar um redirect após a criação bem-sucedida.
        self.assertEqual(response.status_code, 302) # HTTP 302 Found (redirecionamento após sucesso)
        self.assertRedirects(response, reverse('ver_chamados')) # Redireciona para a lista
        self.assertEqual(Chamado.objects.count(), initial_chamado_count + 1) # Verifica se um novo chamado foi criado
        novo_chamado = Chamado.objects.latest('data_criacao')
        self.assertEqual(novo_chamado.assunto, 'Novo Chamado de Teste Válido')
        self.assertEqual(novo_chamado.criado_por, self.user)
        self.assertEqual(novo_chamado.setor, 'financeiro')
        self.assertEqual(novo_chamado.urgencia, 'baixa')

    def test_criar_chamado_view_post_invalid_data(self):
        """Verifica se a view criar_chamado não cria um chamado com dados inválidos."""
        initial_chamado_count = Chamado.objects.count()
        data = {
            'assunto': 'Curto', # Inválido: menos de 10 caracteres
            'descricao': 'Desc válida com mais de 20 caracteres.',
            'setor': 'ti',
            'urgencia': 'media' # >>> CORRIGIDO AQUI: removido '' extra antes de 'urgencia'
        }
        response = self.client.post(reverse('criar_chamado'), data)
        # >>> CORRIGIDO AQUI: Espera 400 se a view retornar HttpResponseBadRequest.
        self.assertEqual(response.status_code, 400) # Se sua view retorna HttpResponseBadRequest
        self.assertTemplateUsed(response, 'App/pages/central/chamado.html') # >>> CORRIGIDO AQUI: Nome do template real
        self.assertIn('form', response.context)
        self.assertFalse(response.context['form'].is_valid()) # Verifica que o formulário é inválido
        self.assertEqual(Chamado.objects.count(), initial_chamado_count) # Nenhum novo chamado criado
        self.assertIn('assunto', response.context['form'].errors) # Espera erro no campo 'assunto'
