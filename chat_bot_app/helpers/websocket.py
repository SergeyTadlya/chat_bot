import json
from channels.generic.websocket import AsyncWebsocketConsumer
from chat_bot_app.helpers.messages import Messages


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # self.roomGroupName = "chat_with_manager"
        self.room_name = self.scope['url_route']['kwargs']['grpname']
        self.roomGroupName = 'chat_%s' % self.room_name
        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_layer
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        sender = text_data_json["sender"]
        if sender == "client":
            message_block = Messages.user(message)
        else:
            message_block = Messages.other(message)
        await self.channel_layer.group_send(
            self.roomGroupName, {
                "type": "sendMessage",
                "message": message,
                "username": username,
                "sender": sender,
                "message_block": message_block,
            })

    async def sendMessage(self, event):
        message = event["message"]
        username = event["username"]
        sender = event["sender"]
        message_block = event["message_block"]
        await self.send(text_data=json.dumps({
            "message": message,
            "username": username,
            "sender": sender,
            "message_block": message_block,
        }))