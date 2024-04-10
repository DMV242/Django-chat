import base64
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chat.models import Message, Room
from django.core.files.base import ContentFile


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message")

        user = self.scope.get("user")
        room = self.scope["url_route"]["kwargs"]["room_name"]
        current_room = await database_sync_to_async(self.get_room)(room)

        if message is not None:

            saved_message = await database_sync_to_async(self.save_message)(
                content=message, user=user, room=current_room
            )
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat.message",
                    "message": message,
                    "user": saved_message.author.username,
                    "time": saved_message.sended_date.strftime("%H:%M:%S"),
                },
            )
        else:

            image_data = text_data_json["image"].split(";")[1].split(",")[1]
            image_name = text_data_json["name"]
            image_binary = base64.b64decode(image_data)

            saved_message = await database_sync_to_async(self.save_message)(
                user=user, room=current_room
            )
            await database_sync_to_async(saved_message.image.save)(
                image_name, ContentFile(image_binary)
            )

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat.image",
                    "image": saved_message.image.url,
                    "user": saved_message.author.username,
                    "time": saved_message.sended_date.strftime("%H:%M:%S"),
                },
            )

    async def chat_message(self, event):
        message = event["message"]
        user = event["user"]
        time = event["time"]
        type = event["type"]
        await self.send(
            text_data=json.dumps(
                {"message": message, "user": user, "time": time, "type": type}
            )
        )

    async def chat_image(self, event):
        imageUrl = event["image"]
        user = event["user"]
        time = event["time"]
        type = event["type"]
        await self.send(
            text_data=json.dumps(
                {"image": imageUrl, "user": user, "time": time, "type": type}
            )
        )

    def get_room(self, room):
        return Room.objects.filter(name=room).get()

    def save_message(self, content=None, user=None, room=None, file=None):
        message = Message.objects.create(
            content=content, author=user, room=room, image=file
        )
        return message
