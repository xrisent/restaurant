import json
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Reservation


class ReservationUpdateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'reservation_updates'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        pass

    @database_sync_to_async
    def get_reservation_updates(self):
        reservations = Reservation.objects.all()
        return [
            {
                **reservation,
                'start_time': reservation['start_time'].isoformat() if 'start_time' in reservation else None,
                'end_time': reservation['end_time'].isoformat() if 'end_time' in reservation else None,
            }
            for reservation in reservations.values()
        ]

    async def send_reservation_update(self, event):
        reservation_updates = await self.get_reservation_updates()
        print("Sending reservation updates:", reservation_updates)
        await self.send(text_data=json.dumps({
            'type': 'reservation_update',
            'data': reservation_updates
        }))