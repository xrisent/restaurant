import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Table

class TableUpdateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'table_updates'  # Имя группы для обновлений
        # Добавляем клиент в группу
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Убираем клиент из группы при отключении
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Обрабатываем сообщения, полученные от клиента WebSocket
        pass

    @database_sync_to_async
    def get_table_updates(self):
        # Получаем обновления для всех таблиц
        tables = Table.objects.all()  # Можно фильтровать, если нужно
        return list(tables.values())  # Возвращаем как список словарей

    # Этот метод вызывается для отправки обновлений клиентам
    async def send_table_update(self, event):
        table_updates = await self.get_table_updates()
        print("Sending table updates:", table_updates)  # Логируем обновления
        # Отправляем данные клиенту через WebSocket
        await self.send(text_data=json.dumps({
            'type': 'table_update',
            'data': table_updates
        }))
