from datetime import datetime, timedelta
import pytz
import time
import schedule
import telebot
from decouple import config
from restaurant.models import *
from user_auth.models import *

bot = telebot.TeleBot(config('TOKEN'))
local_timezone = pytz.timezone("Asia/Bishkek")

def reserved_tables():
    current_time = datetime.now(local_timezone)
    reservations = Reservation.objects.filter(start_time__gte=current_time)
    
    for reservation in reservations:
        time_difference = reservation.start_time - current_time
        minutes_difference = time_difference.total_seconds() / 60
        
        if int(minutes_difference) == 30:
            person = reservation.reserved_by
            table = reservation.table
            restaurant = table.restaurant

            start_time_local = reservation.start_time.astimezone(local_timezone)

            bot.send_message(
                person.tg_id,
                f'Напоминаю! Вы забронировали стол номер {table.number} в ресторане {restaurant.name} на {start_time_local.strftime("%d-%m-%Y %H:%M")}'
            )

def start_reserved_tables_bot():
    schedule.every().minute.do(reserved_tables)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
