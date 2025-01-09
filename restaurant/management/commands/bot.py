# bot.py
import telebot
from telebot import types
from decouple import config
from django.db.utils import IntegrityError
from restaurant.models import *
from user_auth.models import *
from user_auth.serializers import *
from restaurant.serializers import *
import pytz

bot = telebot.TeleBot(config('TOKEN'))
user_states = {}

def bot_handler():
    bot.enable_save_next_step_handlers(delay=2)
    bot.load_next_step_handlers()

    @bot.message_handler(commands=['start'])
    def start_bot(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Покажи забронированные столики')
        item2 = types.KeyboardButton('Мой аккаунт')
        item3 = types.KeyboardButton('Привязать мой аккаунт')
        item4 = types.KeyboardButton('Отвязать этот аккаунт')
        markup.add(item1, item2, item3, item4)
        bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.first_name}! Я бот для финального проекта команды "Лигма".', reply_markup=markup)

    @bot.message_handler(func=lambda message: message.text == 'Привязать мой аккаунт')
    def bind_account(message):
        bot.send_message(message.chat.id, 'Напишите пожалуйста код, который указан в вашем профиле на сайте')
        user_states[message.chat.id] = 'waiting_for_code'

    @bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'waiting_for_code')
    def code_input(message):
        try:
            code = int(message.text)
            person = Person.objects.filter(tg_code=code).first()
            if person:
                try:
                    person.tg_id = message.chat.id
                    person.save()
                    bot.send_message(message.chat.id, 'Аккаунт успешно привязан')
                except IntegrityError:
                    bot.send_message(message.chat.id, 'У вас уже привязан этот телеграм аккаунт')
            else:
                bot.send_message(message.chat.id, 'Такого пользователя не существует')
            user_states[message.chat.id] = None
        except ValueError:
            bot.send_message(message.chat.id, 'Пожалуйста, введите число')

    @bot.message_handler(content_types=['text'])
    def main(message):
        if message.chat.type == 'private':

            if message.text == 'Мой аккаунт':
                person = Person.objects.filter(tg_id=message.chat.id).first()
                if person:
                    serializer = PersonSerializer(person)
                    name = serializer.data.get('name', 'Не указано')
                    email = serializer.data.get('email', 'Не указано')
                    number = serializer.data.get('number', 'Не указано')
                    bot.send_message(message.chat.id, f'Ваше имя: {name}\nВаш email: {email}\nВаш номер: {number}')
                else:
                    bot.send_message(message.chat.id, 'Пользователь не найден')

            if message.text == 'Покажи забронированные столики':
                person = Person.objects.filter(tg_id=message.chat.id).first()
                if person:
                    reservations = Reservation.objects.filter(reserved_by=person)
                    if reservations:
                        local_timezone = pytz.timezone("Asia/Bishkek")

                        for reservation in reservations:
                            table = reservation.table
                            restaurant = table.restaurant
                            
                            start_time_local = reservation.start_time.astimezone(local_timezone)
                            end_time_local = reservation.end_time.astimezone(local_timezone)

                            bot.send_message(
                                message.chat.id,
                                f'Ресторан: {restaurant.name}\nНомер столика: {table.number}\nВремя брони: {start_time_local.strftime("%d-%m-%Y %H:%M")} до {end_time_local.strftime("%d-%m-%Y %H:%M")}'
                            )
                    else:
                        bot.send_message(message.chat.id, 'У вас нет забронированных столиков')
                else:
                    bot.send_message(message.chat.id, 'Пользователь не найден')

            if message.text == 'Отвязать этот аккаунт':
                person = Person.objects.filter(tg_id=message.chat.id).first()
                if person:
                    person.tg_id = None
                    person.save()
                    bot.send_message(message.chat.id, 'Аккаунт успешно отвязан')
                else:
                    bot.send_message(message.chat.id, 'Аккаунт не привязан')
    bot.infinity_polling()
