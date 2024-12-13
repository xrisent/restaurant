from datetime import datetime, timedelta
import time
import schedule
from decouple import config
import telebot

from restaurant.models import Table
from user_auth.models import Person

bot = telebot.TeleBot(config('TOKEN'))

def reserved_tables():
    tables = Table.objects.filter(is_reserved=True)
    for table in tables:
        persons = Person.objects.filter(id=table.reserved_by.id)
        for person in persons:
            if datetime.now().replace(second=0, microsecond=0) == table.reserved_time.replace(second=0, tzinfo=None) + timedelta(minutes=1):
                bot.send_message(person.tg_id, f'Напоминаю! Вы забронировали стол номер {table.number} в ресторане {table.restaurant.name} на {table.reserved_time.strftime("%Y-%m-%d %H:%M")}.')
        

schedule.every().minute.do(reserved_tables)

while True:
    schedule.run_pending()
    time.sleep(1)