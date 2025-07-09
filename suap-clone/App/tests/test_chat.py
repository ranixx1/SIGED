# App/tests/test_chat.py

import pytest
from django.contrib.auth import get_user_model
from django.test import TransactionTestCase
from django.contrib.sessions.models import Session
from django.contrib.auth import SESSION_KEY
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async

from core.asgi import application
from ..models import ChatMessage

User = get_user_model()

pytestmark = pytest.mark.django_db(transaction=True)


class ChatConsumerTestCase(TransactionTestCase):
    """
    Classe de teste para o ChatConsumer.
    """
    room_name = "geral"

    @classmethod
    def setUpClass(cls):
        """
        Cria os usuários e suas sessões uma vez para toda a classe de teste.
        Isso garante que a transação seja confirmada e os dados estejam
        visíveis para o processo do consumer.
        """
        super().setUpClass()
        cls.user1 = User.objects.create_user(username='user1', password='password123')
        cls.user2 = User.objects.create_user(username='user2', password='password123')

        # Cria as sessões de forma síncrona, pois setUpClass não é async
        from django.contrib.sessions.backends.db import SessionStore
        
        session1 = SessionStore()
        session1[SESSION_KEY] = cls.user1.pk
        session1.create()
        cls.session_key1 = session1.session_key

        session2 = SessionStore()
        session2[SESSION_KEY] = cls.user2.pk
        session2.create()
        cls.session_key2 = session2.session_key

    @classmethod
    def tearDownClass(cls):
        """
        Limpa os dados criados para a classe.
        """
        Session.objects.all().delete()
        User.objects.all().delete()
        super().tearDownClass()


    async def test_authenticated_user_can_connect(self):
        """
        Testa se um usuário autenticado consegue se conectar ao WebSocket.
        """
        communicator = WebsocketCommunicator(
            application,
            f"/ws/chat/{self.room_name}/",
            headers=[(b"cookie", f"sessionid={self.session_key1}".encode("ascii"))]
        )
        
        connected, subprotocol = await communicator.connect(timeout=5)
        self.assertTrue(connected, "Usuário autenticado deveria conseguir se conectar.")
        
        await communicator.disconnect()

    async def test_send_message_is_saved_and_broadcasted(self):
        """
        Testa o cenário principal: envio, salvamento e broadcast da mensagem.
        """
        communicator1 = WebsocketCommunicator(
            application,
            f"/ws/chat/{self.room_name}/",
            headers=[(b"cookie", f"sessionid={self.session_key1}".encode("ascii"))]
        )
        await communicator1.connect(timeout=5)

        communicator2 = WebsocketCommunicator(
            application,
            f"/ws/chat/{self.room_name}/",
            headers=[(b"cookie", f"sessionid={self.session_key2}".encode("ascii"))]
        )
        await communicator2.connect(timeout=5)

        test_message = "Olá, mundo do Channels!"
        await communicator1.send_json_to({
            "message": test_message
        })

        response1 = await communicator1.receive_json_from(timeout=5)
        response2 = await communicator2.receive_json_from(timeout=5)

        self.assertEqual(response1['message'], test_message)
        self.assertEqual(response1['username'], self.user1.username)
        self.assertEqual(response2, response1, "Usuário 2 deveria receber a mesma mensagem que o Usuário 1.")

        # A verificação no banco de dados agora deve funcionar corretamente
        message_exists = await database_sync_to_async(ChatMessage.objects.filter(
            user_id=self.user1.pk,
            message=test_message,
            room_name=self.room_name
        ).exists)()
        
        self.assertTrue(message_exists, "A mensagem enviada não foi salva no banco de dados.")

        await communicator1.disconnect()
        await communicator2.disconnect()
