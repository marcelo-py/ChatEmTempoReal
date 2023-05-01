import json
from .models import Sala, Mensagem
from django.contrib.auth.models import User


from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"] # vem la da URL ver ela qual quer coisa
        self.room_group_name = "chat_%s" % self.room_name
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    # Essa parte em mais a ver com a pessoa conectada mandando a mensagem
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_json = text_data_json["message"]

        outro_usuario = self.scope['query_string'].decode().split('=')[1]

        # Criando a sala caso ela não exista
        if not await database_sync_to_async(Sala.objects.filter(sala=self.room_name).exists)():
            objt_outro_usuario = await database_sync_to_async(User.objects.get)(id=int(outro_usuario))
            criar_sala = Sala(sala=self.room_name)
            await database_sync_to_async(criar_sala.save)()
            await database_sync_to_async(criar_sala.usuarios_permitidos.add)(self.scope['user'], objt_outro_usuario)
        
        sala_obj = await database_sync_to_async(list)(Sala.objects.filter(sala=self.room_name))
        print('isso que o obj sala retorna >>>>', sala_obj)
        mensagem = Mensagem(mensagem=message_json, remetente=self.scope['user'], sala=sala_obj[0])
        await database_sync_to_async(mensagem.save)()

        #usuario_de_la_obj = User.objects.get(id=outro_usuario)

        #print('Sobre o outro usuario>>>>>>>>', usuario_de_la_obj)
        # type = evento
        # com isso eu posso passar id objetos de user e etc para capturar
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message_json, 'remetente': self.scope['user'].username}
        )

    # Receive message from room group
    # relacionado ao rceive. Ele manda achave type para event junto com a messagem
    # Essa parte tem mais a ver com a pessoa do outra lado,
    # pois é aqui que a mensagem chega pra ela tem tempo real
    async def chat_message(self, event):
        message = event['message'] # pegando somente a mensagem em vez do type
        remetente = event['remetente']
        # recebe a mensagem para poder enviar de volta para todos os os usuarios em tempo real
        await self.send(text_data=json.dumps({"message": message, 'remetente': remetente}))
