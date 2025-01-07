import telebot
import main

bot = telebot.TeleBot('7855375894:AAE8jf5q-RgYlhIZRGDqwapMZiNinjpqAP0')


@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, main.a())


@bot.message_handler()
def info(message):
    if message.text.lower() == 'hello':
        bot.send_message(message.chat.id, 'asdasd')



bot.polling(none_stop=True)
