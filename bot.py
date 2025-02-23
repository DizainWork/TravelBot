import telebot
from telebot import types
import os
from dotenv import load_dotenv
from datetime import datetime
import json
from currency_api import get_currency_rates, update_currency_rate, get_stored_rates
from database import Database
from excel_manager import ExcelManager

# Загружаем переменные окружения
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')

print(f"BOT_TOKEN: {BOT_TOKEN}")
print(f"ADMIN_CHAT_ID: {ADMIN_CHAT_ID}")

bot = telebot.TeleBot(BOT_TOKEN)
db = Database()
excel_mgr = ExcelManager(db)

def create_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        '✈️ Авиабилеты', '🏝 Туры',
        '🏠 Отели', '🚗 Аренда авто',
        '🌍 Визы', '🛡 Страховка',
        '🎫 Экскурсии', '🛄 Консьерж-сервис',
        '💳 Бонусы и акции', '💱 Обмен валют',
        '📞 Связаться с агентом'
    ]
    markup.add(*[types.KeyboardButton(button) for button in buttons])
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = (
        "👋 Добро пожаловать в Travel in New Life!\n\n"
        "Я помогу вам забронировать туры, билеты и отели, "
        "а также предоставлю информацию о других наших услугах."
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=create_main_menu())

@bot.message_handler(func=lambda message: message.text == '🌍 Визы')
def visas_menu(message):
    # Получаем кастомный текст для раздела виз
    custom_text = db.get_text_block('🌍 Визы')
    if custom_text:
        bot.send_message(message.chat.id, custom_text, parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, "Информация о визах временно недоступна. Пожалуйста, обратитесь к менеджеру.")

# ... (остальной код без изменений)
