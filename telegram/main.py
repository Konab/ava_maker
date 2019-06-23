import os
import telebot
import requests

from dotenv import load_dotenv
from pathlib import Path

from libs.face_detected.detecters import create_mask_nake
from libs.face_detected.detecters import create_face_shape
from libs.face_detected.detecters import create_current_mask

# env_path = os.Path('../')/'.env'
env_path = os.getcwd()+'/.env'
load_dotenv(dotenv_path=env_path)

TOKEN = os.getenv('TG_TOKEN')
bot = telebot.TeleBot(TOKEN)


def download_image(file_path, save=False):
	'''Download image
	Скачивает изображение и передает его в битах
	
	Arguments:
		file_path {str} -- путь к файлу
	
	Returns:
		<requests> -- объект Requests
	'''
	url = 'https://api.telegram.org/file/bot{token}/{file_path}'
	curr_file = requests.get(url.format(token=TOKEN, file_path=file_path))
	if save:
		with open('data/download/'+file_path.split('/')[-1], 'wb') as f:
			f.write(curr_file.content)
	return curr_file


@bot.message_handler(commands=['start'])
def start_handler(message):
	print(f'--> Started by user: {message.chat.id}')

	bot.send_message(message.chat.id, f'Hello')


@bot.message_handler(content_types=['photo', 'document'])
def photo_handler(message):
	print(f'Start photo handler by {message.chat.id}')
	file_id = message.photo[-1].file_id
	file = bot.get_file(file_id)
	img = download_image(file.file_path, save=True)

	# img = create_mask_nake('data/download/'+file.file_path.split('/')[-1], save=True)
	img = create_current_mask('data/download/'+file.file_path.split('/')[-1], save=True)

	bot.send_photo(message.chat.id, open(img, 'rb'))

	# name = file.file_path.split('/')[-1].split('.')[0] + '.png'
	# bot.send_photo(message.chat.id, open('data/hand/'+name, 'rb'))

	# bot.send_photo(message.chat.id, img.content)
	# with open('down_data/'+file.file_path.split('/')[-1], 'rb') as f:
	# 	bot.send_photo(message.chat.id, f)
	# bot.send_message(message.chat.id, open('down_data/'+file.file_path.split('/')[-1], 'rb'))


def start_bot():
	print('--> Запускаю бот')
	bot.polling(True)


if __name__ == '__main__':
	start_bot()
