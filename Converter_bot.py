
import telebot
from currency_converter import CurrencyConverter #импорт класса CurrencyConverter
from telebot import types
import os
from dotenv import load_dotenv #импорта библиотеки
load_dotenv() #поиска файла .env и загрузки из него переменных среды

Token = os.getenv("TOKEN")
bot = telebot.TeleBot(Token)
#создание объекта класса CurrencyConverter
currency = CurrencyConverter()

#глобальная переменная
amount = 0

#должны отслеживать команду start
@bot.message_handler(commands=['start'])
#ввод функции которая срабатывает при вводе команды start
def start(message):
    #пользователю будем выводить некоторое сообщение
    bot.send_message(message.chat.id, 'Привет, введите сумму')
    bot.register_next_step_handler(message,summa)


def summa(message): #функция как только пользователь вводит сумму
    #объявление глобальной переменной
    global amount
    #пропишем обработчик исключения
    try:
        amount = int(message.text.strip()) #конвертировать от пользователю текст и конвертировать его в число
    except ValueError:
        #отправлять пользователю некоторое сообщение
        bot.send_message(message.chat.id, "Неверный формат. Впишите сумму")
        bot.register_next_step_handler(message,summa)
        return
    #кнопки
    if amount>0:
        markup = types.InlineKeyboardMarkup(row_width=2) #объект markup
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('USD/GBP', callback_data='usd/gbp')
        btn4 = types.InlineKeyboardButton('Другое значение', callback_data='else') #возможность пользователю выбирать свою конвертацию
        markup.add(btn1,btn2,btn3,btn4)
        #пользователю выводить сообщение
        bot.send_message(message.chat.id, "Выберите пару валют", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Число должно быть больше чем 0. Впишите сумму.")
        bot.register_next_step_handler(message, summa)


#методы
@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    if call.data !="else":
        values = call.data.upper().split("/")
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f"Получается: {round(res,2)}. Можете заново вписать сумму")
        bot.register_next_step_handler(call.message,summa)
    else:
        bot.send_message(call.message.chat.id, "Введите пару значений через слеш")
        bot.register_next_step_handler(call.message, my_currency)
def my_currency(message):
    #добавляем обработчик исключений
    try:
        values = message.text.upper().split("/")
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f"Получается: {round(res, 2)}. Можете заново вписать сумму")
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, f"Что-то не так впишите значение заново")
        bot.register_next_step_handler(message, my_currency)


bot.polling(none_stop=True)