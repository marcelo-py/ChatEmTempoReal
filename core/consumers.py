import json
from .models import Sala, Mensagem
from django.contrib.auth.models import User


from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs
from django.shortcuts import get_object_or_404


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
        message = text_data_json["message"]

        user = self.scope['query_string'].decode().split('=')[1]
        print('O suaurio da URL é >>>>>>', user)

        # type = evento
        # com isso eu posso passar id objetos de user e etc para capturar
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    # relacionado ao rceive. ele manda achave type para event junto com a messagem
    # Essa parte tem mais a ver com a pessoa do outra lado,
    # pois é aqui que a mensagem chega pra ela tem tempo real
    async def chat_message(self, event):
        message = event['message'] # pegando somente a mensagem em vez do type
        print('>>>>>msg   :', message)
        
        # recebe a mensagem para poder enviar de volta para todos os os usuarios em tempo real
        await self.send(text_data=json.dumps({"message": message}))
