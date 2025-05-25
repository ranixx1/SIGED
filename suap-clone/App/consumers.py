import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async # Importe esta função
from .models import ChatMessage # Importe seu novo modelo ChatMessage

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Obtém o nome da sala da URL WebSocket
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Adiciona o usuário ao grupo da sala
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Remove o usuário do grupo da sala
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        user = self.scope["user"] # Obtém o usuário logado via AuthMiddlewareStack

        # Salvar a mensagem no banco de dados de forma assíncrona
        await self.save_message(user, self.room_name, message)

        # Envia a mensagem para o grupo da sala (para todos os conectados)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message', # Nome do método que receberá a mensagem
                'message': message,
                'username': user.username, # Envia o username junto com a mensagem
            }
        )

    # Função para receber a mensagem do grupo da sala e enviar para o WebSocket do cliente
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Envia a mensagem de volta para o WebSocket do cliente
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))

    # Função para salvar a mensagem no banco de dados (executado de forma síncrona)
    @sync_to_async
    def save_message(self, user, room_name, message):
        ChatMessage.objects.create(
            user=user,
            room_name=room_name,
            message=message
        )