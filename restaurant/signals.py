import asyncio
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Table
from .consumers import TableUpdateConsumer
from channels.layers import get_channel_layer

@receiver(post_save, sender=Table)
def send_table_update(sender, instance, created, **kwargs):
    # Логируем обновление
    print(f"Sending update for table {instance.number}")

    # Создаем сообщение
    message = f"Table {instance.number} updated."

    # Запускаем асинхронную задачу для отправки обновления
    asyncio.run(send_update_to_group_async(message))

async def send_update_to_group_async(message):
    # Get the channel layer
    channel_layer = get_channel_layer()
    
    # Send the update to the 'table_updates' group
    await channel_layer.group_send(
        'table_updates',  # Имя группы
        {
            'type': 'send_table_update',  # Тип события
            'message': message  # Сообщение (обновление)
        }
    )
