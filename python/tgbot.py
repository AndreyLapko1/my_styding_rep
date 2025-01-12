import telebot
from telebot import types
import app

bot = telebot.TeleBot('7855375894:AAE8jf5q-RgYlhIZRGDqwapMZiNinjpqAP0')



@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Поиск по году')
    markup.row(btn1)
    btn2 = types.KeyboardButton('Поиск по категории')
    btn3 = types.KeyboardButton('Поиск по имени актера')
    markup.row(btn2, btn3)
    bot.send_message(message.chat.id, 'Welcome to movie search', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)

def on_click(message):
    if message.text == 'Поиск по году':
        bot.send_message(message.chat.id, 'Введите год: ')
        bot.register_next_step_handler(message, get_year)


def get_year(message):
    try:
        year = int(message.text)
        main_.App.search_year(year)
        bot.send_message(message.chat.id, f"Вы ввели год: {year}")
    except ValueError:
        bot.send_message(message.chat.id, "Это не похоже на год. Попробуйте снова.")
        bot.register_next_step_handler(message, get_year)




@bot.message_handler(content_types=['photo'])
def get(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Put', url='https://google.com'))
    markup.add(types.InlineKeyboardButton('Edit text', callback_data='edit'))
    bot.reply_to(message, 'aaa', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_message(callback):
    if callback.data == 'edit':
        bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)

bot.polling(none_stop=True)
