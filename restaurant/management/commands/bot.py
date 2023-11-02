from django.core.management.base import BaseCommand
from django.conf import settings
from decouple import config
import telebot
from telebot import types
from datetime import datetime
from django.db.utils import IntegrityError


from restaurant.models import *
from user_auth.models import *
from user_auth.serializers import *
from restaurant.serializers import *


bot = telebot.TeleBot(config('TOKEN'))
user_states = {}


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        bot.infinity_polling()


@bot.message_handler(commands=['start'])
def start_bot(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Покажи забронированные столики')
    item2 = types.KeyboardButton('Мой аккаунт')
    item3 = types.KeyboardButton('Привязать мой аккаунт')
    markup.add(item1, item2, item3)
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
                person.tg_id=message.chat.id
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
                person_serializer = PersonSerializer(person)
                tables = Table.objects.filter(reserved_by=person_serializer.data.get('id'))
                if tables:
                    for table in tables:
                        table_serializer = TableSerializer(table)

                        restaurant = Restaurant.objects.filter(id=table_serializer.data.get('restaurant')).first()
                        restaurant_serializer = RestaurantSerializerView(restaurant)

                        reserved_time = table_serializer.data.get('reserved_time')
                        table_number = table_serializer.data.get('number')
                        send_restaurant = restaurant_serializer.data.get('name')
                        
                        bot.send_message(message.chat.id, f'Ресторан: {send_restaurant}\nНомер: {table_number}\nВремя брони: {datetime.fromisoformat(reserved_time).strftime("%Y-%m-%d %H:%M:%S")}')
                else:
                    bot.send_message(message.chat.id, 'У вас не забронированы столики')
            else:
                bot.send_message(message.chat.id, 'Пользователь не найден')

