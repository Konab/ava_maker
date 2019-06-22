import os
import telebot


from dotenv import load_dotenv
from pathlib import Path


# env_path = os.Path('../')/'.env'
env_path = os.getcwd()+'/.env'
load_dotenv(dotenv_path=env_path)

TOKEN = os.getenv('TG_TOKEN')
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_handler(message):
	print(f'--> Started by user: {message.chat.id}')

	bot.send_message(message.chat.id, f'Hello')


if __name__ == '__main__':
	print('--> Запускаю бот')
	bot.polling(True)
