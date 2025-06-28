from channels.testing import WebsocketCommunicator
from django.test import TransactionTestCase
from django.contrib.auth import get_user_model
from suap_clone.core.asgi import application  # Corrected import path

User = get_user_model()

class ChatConsumerTestCase(TransactionTestCase):
    async def asyncSetUp(self):
        # Create a user for testing. It's generally better to use a more secure password
        # or manage test passwords properly. For a test, this is fine.
        self.user = await User.objects.acreate(username='chatuser', password='senha123')

    async def test_send_chat_message(self):  # Renamed for clarity
        # Ensure the path matches your routing configuration in asgi.py
        communicator = WebsocketCommunicator(application, "/ws/chat/geral/")
        
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)
        
        # Optionally, you might want to authenticate the user here if your consumer
        # requires an authenticated user. For example:
        # await communicator.send_json_to({"command": "authenticate", "user_id": self.user.id})
        # await communicator.receive_json_from() # Await confirmation of authentication
        
        test_message = "Olá, chat!"
        await communicator.send_json_to({"message": test_message})
        
        response = await communicator.receive_json_from()
        # Verify the received message. This assumes your consumer echoes the message.
        self.assertEqual(response.get('message'), test_message) 
        
        await communicator.disconnect()

    async def asyncTearDown(self):
        # Clean up the created user after the test
        await self.user.adelete()