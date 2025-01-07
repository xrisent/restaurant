from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Reservation
from .consumers import ReservationUpdateConsumer
from channels.layers import get_channel_layer
import asyncio

# Signal for when a reservation is created or updated
@receiver(post_save, sender=Reservation)
def send_reservation_update(sender, instance, created, **kwargs):
    # Логируем обновление
    print(f"Sending update for reservation {instance.id}")

    # Создаем сообщение
    message = f"Reservation for table {instance.table.number} updated."

    # Запускаем асинхронную задачу для отправки обновления
    asyncio.run(send_update_to_group_async(message))

# Signal for when a reservation is deleted
@receiver(post_delete, sender=Reservation)
def send_reservation_delete(sender, instance, **kwargs):
    # Логируем удаление
    print(f"Sending delete for reservation {instance.id}")

    # Создаем сообщение о удалении
    message = f"Reservation for table {instance.table.number} deleted."

    # Запускаем асинхронную задачу для отправки обновления
    asyncio.run(send_update_to_group_async(message))

async def send_update_to_group_async(message):
    # Get the channel layer
    channel_layer = get_channel_layer()
    
    # Send the update to the 'reservation_updates' group
    await channel_layer.group_send(
        'reservation_updates',  # Group name
        {
            'type': 'send_reservation_update',  # Event type
            'message': message  # The update message
        }
    )
