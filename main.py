import telebot
from config import keys, TOKEN
from error import APIException, CryptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    text = f'Welcome, {message.chat.username}\nЧтобы я начал работать, введите команду боту в следующем формате:\n' \
           f'<Имя валюты> <В какую перевести> <Количество переводимой валюты>\n' \
           f'Вводя команду "/values" можно вывести все доступные валюты с какими можно работать'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты: "
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values1 = message.text.lower()
        values = values1.split(' ')

        if len(values) != 3:
            raise APIException('Слишком много параметров')

        iz, w, sk = values
        total_base = CryptoConverter.convert(iz, w, sk)
    except APIException as e:
        bot.reply_to(message, f'Ошибка! \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n"{e}"')
    else:
        result = float(sk)*total_base
        text = f'Цена {sk} {iz} в {w} - {result}'
        bot.send_message(message.chat.id, text)


bot.polling()
