import telebot
from telebot import types
import main_

bot = telebot.TeleBot('7855375894:AAE8jf5q-RgYlhIZRGDqwapMZiNinjpqAP0')



@bot.message_handler(commands=['start'])
def stat(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Search by year')
    markup.row(btn1)
    btn2 = types.KeyboardButton('Search by category')
    btn3 = types.KeyboardButton('Search by actor name')
    markup.row(btn2, btn3)
    bot.send_message(message.chat.id, 'Welcome to movie search', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)

def on_click(message):
    if message.text == 'Search by year':
        bot.send_message(message.chat.id, main_.App.search_year(self=message))




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
