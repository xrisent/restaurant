from django.core.management.base import BaseCommand
from django.conf import settings
from decouple import config
import telebot
from telebot import types
from restaurant.models import Table
from user_auth.models import Person
from user_auth.serializers import PersonSerializer
from restaurant.serializers import TableSerializer


bot = telebot.TeleBot(config('TOKEN'))


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
    markup.add(item1, item2)
    bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.first_name}! Я бот для финального проекта команды "Лигма".', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def whoamibot(message):
    if message.chat.type == 'private':
        if message.text == 'Мой аккаунт':
            person = Person.objects.filter(tg_id=message.chat.id).first()
            if person:
                serializer = PersonSerializer(person)
                name = serializer.data.get('name', 'Не указано')
                email = serializer.data.get('email', 'Не указано')
                number = serializer.data.get('number', 'Не указано')
                bot.send_message(message.chat.id, f'Ваше имя: {name}\nВаш email: {email}\nВаш номер: {number}')
                table = Table.objects.filter(reserved_by=serializer.data.get('id')).first()
                table_serializer = TableSerializer(table)
                reserved_time = table_serializer.data.get('reserved_time')
                table_number = table_serializer.data.get('number')
                restaurant = table_serializer.data.get('restaurant')
                bot.send_message(message.chat.id, f'Ресторан: {restaurant}\nНомер: {table_number}\nВремя брони: {reserved_time}')

            else:
                bot.send_message(message.chat.id, 'Пользователь не найден')


# @bot.message_handler(content_types=['text'])
# def reservedbot(message):
#     if message.chat.type == 'private':
#         if message.text == 'Покажи забронированные столики':
#             person = Person.objects.filter(tg_id=message.chat.id).first()
#             if person:
#                 serializer_person = PersonSerializer(person)
#                 table = Table.objects.filter(reserved_by=serializer_person.data.get('id')).first()
#                 serializer = TableSerializer(table)
#                 reserved_time = serializer.data.get('reserved_time', 'Не указано')
#                 restaurant = serializer.data.get('restaurant', 'Не указано')
#                 number = serializer.data.get('number', 'Не указано')
#                 bot.send_message(message.chat.id, f'Ресторан: {restaurant}\nНомер столика: {number}\nВремя брони: {reserved_time}')
#             else:
#                 bot.send_message(message.chat.id, 'Пользователь не найден')