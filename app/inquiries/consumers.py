import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import Inquiry, InquiryMessage


class InquiryConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.inquiry_id = self.scope["url_route"]["kwargs"]["inquiry_id"]

        self.room_name = f"inquiry_{self.inquiry_id}"

        user = self.scope["user"]

        # User must be logged in
        if user.is_anonymous:
            await self.close()
            return

        # Check that user belongs to this inquiry
        allowed = await self.user_can_access_inquiry()

        if not allowed:
            await self.close()
            return

        # Add this connection to the inquiry room
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name,
        )

        await self.accept()


    async def disconnect(self, close_code):
        # Remove connection from inquiry room
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name,
        )


    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return

        message_text = data.get("message")

        if not message_text:
            return

        message_text = message_text.strip()

        if not message_text:
            return

        # Save message
        message = await self.save_message(message_text)

        # Send message to everyone in the inquiry room
        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "chat_message",

                "message_id": message["id"],
                "message": message["message"],
                "sender_id": message["sender_id"],
                "sender_name": message["sender_name"],
                "created_at": message["created_at"],
            },
        )


    async def chat_message(self, event):

        await self.send(
            text_data=json.dumps({
                "type": "message",

                "message_id": event["message_id"],
                "message": event["message"],
                "sender_id": event["sender_id"],
                "sender_name": event["sender_name"],
                "created_at": event["created_at"],
            })
        )


    @database_sync_to_async
    def user_can_access_inquiry(self):

        try:
            inquiry = Inquiry.objects.select_related(
                "customer",
                "profile__userId",
            ).get(id=self.inquiry_id)
        except Inquiry.DoesNotExist:
            return False

        user = self.scope["user"]

        # Customer
        if inquiry.customer_id == user.id:
            return True

        # Property owner / agent
        if inquiry.profile and inquiry.profile.userId_id == user.id:
            return True

        return False


    @database_sync_to_async
    def save_message(self, message_text):

        inquiry = Inquiry.objects.get(id=self.inquiry_id)

        user = self.scope["user"]

        message = InquiryMessage.objects.create(
            inquiry=inquiry,
            sender=user,
            message=message_text,
        ).save()

        return {
            "id": str(message.id),
            "message": message.message,
            "sender_id": str(user.id),
            "sender_name": user.name,
            "created_at": message.created_at.isoformat(),
        }