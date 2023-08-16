import telebot
from currency_converter import CurrencyConverter
from telebot import types

bot = telebot.TeleBot('6688383886:AAE_t8r_jK3ZgcpOvFAWaH5uOdHMezTaWXs')

currency = CurrencyConverter()
amount = 0

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Greetings. Enter the required amount")
    bot.register_next_step_handler(message, summa)

def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
        if amount > 0:
            markup = types.InlineKeyboardMarkup(row_width=2)
            btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
            btn2 = types.InlineKeyboardButton('USD/GBP', callback_data='usd/gbp')
            btn3 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
            btn4 = types.InlineKeyboardButton('Other pair', callback_data='else')
            markup.add(btn1, btn2, btn3, btn4)
            bot.send_message(message.chat.id, 'Choose a pair of currencies', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "The number must be more than 0")
    except ValueError:
        bot.send_message(message.chat.id, "Wrong format. Write the amount in numerical form. Example: 32, 4, 102")
        bot.register_next_step_handler(message, start)

@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f"Result: {round(res, 2)}. You can re-enter the amount")
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, "Enter a value pair using a slash. Example: USD/EUR")
        bot.register_next_step_handler(call.message, my_currency)

def my_currency(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f"Result: {round(res, 2)}. You can re-enter the amount")
        bot.register_next_step_handler(message, summa)
    except ValueError:
        bot.send_message(message.chat.id, "Invalid input format. Please enter the value again")
        bot.register_next_step_handler(message, my_currency)

bot.polling(none_stop=True)