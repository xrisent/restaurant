
import threading
from django.core.management.base import BaseCommand
from .reserve import start_reserved_tables_bot
from .bot import bot_handler


class Command(BaseCommand):
    help = 'Запускает ботов для проверки резервов и общения с пользователями'

    def handle(self, *args, **kwargs):
        # Создаем два потока
        thread1 = threading.Thread(target=start_reserved_tables_bot)
        thread2 = threading.Thread(target=bot_handler)

        # Запускаем потоки
        thread1.start()
        thread2.start()

        # Ожидаем завершения работы обоих потоков
        thread1.join()
        thread2.join()
