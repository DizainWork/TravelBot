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

# Инициализация базы данных
db = Database()

# Создаем экземпляр менеджера Excel
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

@bot.message_handler(func=lambda message: message.text == '💱 Обмен валют')
def currency_exchange(message):
    markup = types.InlineKeyboardMarkup(row_width=3)
    currencies = ['USD', 'EUR', 'GBP', 'TRY']
    buttons = [types.InlineKeyboardButton(curr, callback_data=f'currency_{curr}') for curr in currencies]
    markup.add(*buttons)
    markup.add(types.InlineKeyboardButton('🔙 В главное меню', callback_data='back_to_main'))
    
    bot.send_message(
        message.chat.id,
        "Выберите интересующую вас валюту:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('currency_'))
def handle_currency(call):
    currency = call.data.split('_')[1]
    rates = get_stored_rates()
    
    if currency in rates:
        rate_info = rates[currency]
        response = (
            f"Курс {currency} на {rate_info['date']}:\n"
            f"1 {currency} = {rate_info['rate']} RUB\n\n"
            f"Последнее обновление: {rate_info['updated_at']}"
        )
    else:
        response = f"Извините, курс для {currency} временно недоступен"

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('🔄 Обновить курс', callback_data=f'update_{currency}'))
    markup.add(types.InlineKeyboardButton('🔔 Подписаться на обновления', callback_data=f'subscribe_{currency}'))
    markup.add(types.InlineKeyboardButton('🔙 Назад к списку валют', callback_data='back_to_currencies'))

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=response,
        reply_markup=markup
    )

# Админские команды
@bot.message_handler(commands=['update_currency'])
def update_currency(message):
    if str(message.chat.id) != ADMIN_CHAT_ID:
        return
    
    try:
        _, currency, rate = message.text.split()
        rate = float(rate)
        update_currency_rate(currency, rate)
        bot.reply_to(message, f"Курс {currency} успешно обновлен")
    except ValueError:
        bot.reply_to(message, "Неверный формат. Используйте: /update_currency USD 92.5")

@bot.message_handler(commands=['show_currency'])
def show_currency(message):
    if str(message.chat.id) != ADMIN_CHAT_ID:
        return
    
    rates = get_stored_rates()
    response = "Текущие курсы валют:\n\n"
    for currency, info in rates.items():
        response += f"{currency}: {info['rate']} RUB (обновлено: {info['updated_at']})\n"
    
    bot.reply_to(message, response)

@bot.message_handler(func=lambda message: message.text == '✈️ Авиабилеты')
def flights_menu(message):
    flights = db.get_flights()
    if not flights:
        bot.reply_to(message, "К сожалению, сейчас нет доступных рейсов")
        return

    markup = types.InlineKeyboardMarkup(row_width=1)
    for flight in flights:
        button_text = f"{flight[1]} ➡️ {flight[2]} ({flight[3]}) - {flight[4]}₽"
        markup.add(types.InlineKeyboardButton(
            button_text, 
            callback_data=f'flight_{flight[0]}'
        ))
    markup.add(types.InlineKeyboardButton('🔙 В главное меню', callback_data='back_to_main'))
    
    bot.send_message(
        message.chat.id,
        "Доступные рейсы:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == '🏝 Туры')
def tours_menu(message):
    tours = db.get_tours()
    if not tours:
        bot.reply_to(message, "К сожалению, сейчас нет доступных туров")
        return

    markup = types.InlineKeyboardMarkup(row_width=1)
    for tour in tours:
        button_text = f"{tour[1]} - {tour[2]} ({tour[3]} дней) - {tour[4]}₽"
        markup.add(types.InlineKeyboardButton(
            button_text, 
            callback_data=f'tour_{tour[0]}'
        ))
    markup.add(types.InlineKeyboardButton('🔙 В главное меню', callback_data='back_to_main'))
    
    bot.send_message(
        message.chat.id,
        "Доступные туры:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == '🏠 Отели')
def hotels_menu(message):
    hotels = db.get_hotels()
    if not hotels:
        bot.reply_to(message, "К сожалению, сейчас нет доступных отелей")
        return

    markup = types.InlineKeyboardMarkup(row_width=1)
    for hotel in hotels:
        button_text = f"{hotel[1]} ({hotel[2]}) - {hotel[3]}⭐ - {hotel[4]}₽/ночь"
        markup.add(types.InlineKeyboardButton(
            button_text, 
            callback_data=f'hotel_{hotel[0]}'
        ))
    markup.add(types.InlineKeyboardButton('🔙 В главное меню', callback_data='back_to_main'))
    
    bot.send_message(
        message.chat.id,
        "Доступные отели:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == '🌍 Визы')
def visas_menu(message):
    # Получаем кастомный текст для раздела виз
    custom_text = db.get_text_block('🌍 Визы')
    if custom_text:
        bot.send_message(message.chat.id, custom_text, parse_mode='HTML')
    
    # Показываем список доступных виз
    visas = db.get_visas()
    if not visas:
        return

    markup = types.InlineKeyboardMarkup(row_width=1)
    for visa in visas:
        button_text = f"{visa[1]} - {visa[2]} ({visa[3]} дней) - {visa[4]}₽"
        markup.add(types.InlineKeyboardButton(
            button_text, 
            callback_data=f'visa_{visa[0]}'
        ))
    markup.add(types.InlineKeyboardButton('🔙 В главное меню', callback_data='back_to_main'))
    
    bot.send_message(
        message.chat.id,
        "Выберите визу для оформления:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == '🎫 Экскурсии')
def excursions_menu(message):
    excursions = db.get_excursions()
    if not excursions:
        bot.reply_to(message, "К сожалению, сейчас нет доступных экскурсий")
        return

    markup = types.InlineKeyboardMarkup(row_width=1)
    for excursion in excursions:
        button_text = f"{excursion[1]} ({excursion[2]}) - {excursion[3]}ч - {excursion[4]}₽"
        markup.add(types.InlineKeyboardButton(
            button_text, 
            callback_data=f'excursion_{excursion[0]}'
        ))
    markup.add(types.InlineKeyboardButton('🔙 В главное меню', callback_data='back_to_main'))
    
    bot.send_message(
        message.chat.id,
        "Доступные экскурсии:",
        reply_markup=markup
    )

# Админские команды для управления данными
@bot.message_handler(commands=['add_flight'])
def add_flight(message):
    if str(message.chat.id) != ADMIN_CHAT_ID:
        return
    
    try:
        # Формат: /add_flight Москва Париж 2024-03-20 50000 100
        _, from_city, to_city, date, price, seats = message.text.split()
        flight_id = db.add_flight(from_city, to_city, date, float(price), int(seats))
        bot.reply_to(message, f"Рейс успешно добавлен (ID: {flight_id})")
    except ValueError:
        bot.reply_to(message, "Неверный формат. Используйте: /add_flight Москва Париж 2024-03-20 50000 100")

@bot.message_handler(commands=['add_tour'])
def add_tour(message):
    if str(message.chat.id) != ADMIN_CHAT_ID:
        return
    
    try:
        # Формат: /add_tour "Тур в Париж" Париж 7 100000 "Описание тура" 20
        cmd_parts = message.text.split('"')
        name = cmd_parts[1]
        rest_parts = cmd_parts[2].strip().split()
        destination, duration, price, places = rest_parts[0], rest_parts[1], rest_parts[2], rest_parts[-1]
        description = " ".join(rest_parts[3:-1]) if len(rest_parts) > 4 else ""
        
        tour_id = db.add_tour(name, destination, int(duration), float(price), description, int(places))
        bot.reply_to(message, f"Тур успешно добавлен (ID: {tour_id})")
    except (ValueError, IndexError):
        bot.reply_to(message, 'Неверный формат. Используйте: /add_tour "Название тура" Место 7 100000 "Описание" 20')

@bot.callback_query_handler(func=lambda call: call.data.startswith(('flight_', 'tour_', 'hotel_', 'visa_', 'excursion_')))
def handle_service_selection(call):
    service_type, service_id = call.data.split('_')
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('📝 Оформить заявку', callback_data=f'book_{service_type}_{service_id}'))
    markup.add(types.InlineKeyboardButton('🔙 Назад', callback_data=f'back_to_{service_type}s'))
    
    if service_type == 'flight':
        flight = db.get_flights()[int(service_id)-1]
        text = f"Рейс: {flight[1]} ➡️ {flight[2]}\nДата: {flight[3]}\nЦена: {flight[4]}₽\nСвободных мест: {flight[5]}"
    elif service_type == 'tour':
        tour = db.get_tours()[int(service_id)-1]
        text = f"Тур: {tour[1]}\nНаправление: {tour[2]}\nДлительность: {tour[3]} дней\nЦена: {tour[4]}₽\nОписание: {tour[5]}"
    elif service_type == 'hotel':
        hotel = db.get_hotels()[int(service_id)-1]
        text = f"Отель: {hotel[1]}\nЛокация: {hotel[2]}\nКатегория: {hotel[3]}⭐\nЦена за ночь: {hotel[4]}₽\nОписание: {hotel[5]}"
    elif service_type == 'visa':
        visa = db.get_visas()[int(service_id)-1]
        text = f"Виза: {visa[1]}\nТип: {visa[2]}\nСрок действия: {visa[3]} дней\nСтоимость: {visa[4]}₽\nСрок оформления: {visa[5]} дней\nТребования: {visa[6]}"
    else:  # excursion
        excursion = db.get_excursions()[int(service_id)-1]
        text = f"Экскурсия: {excursion[1]}\nМесто: {excursion[2]}\nДлительность: {excursion[3]} часов\nЦена: {excursion[4]}₽\nОписание: {excursion[5]}"
    
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('book_'))
def handle_booking(call):
    _, service_type, service_id = call.data.split('_')
    
    # Создаем заявку
    request_id = db.create_request(
        call.message.chat.id,
        call.message.chat.first_name,
        service_type,
        service_id,
        ""  # Контактная информация будет добавлена позже
    )
    
    # Отправляем уведомление администратору
    admin_text = f"Новая заявка #{request_id}!\nУслуга: {service_type}\nID услуги: {service_id}\nПользователь: {call.message.chat.first_name}"
    bot.send_message(ADMIN_CHAT_ID, admin_text)
    
    # Отправляем подтверждение пользователю
    user_text = "Ваша заявка принята! Наш менеджер свяжется с вами в ближайшее время."
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=user_text
    )

@bot.message_handler(commands=['export_excel'])
def export_to_excel(message):
    if str(message.chat.id) != ADMIN_CHAT_ID:
        return
    
    try:
        file_path = excel_mgr.create_excel()
        with open(file_path, 'rb') as file:
            bot.send_document(message.chat.id, file)
        bot.reply_to(message, "Excel файл с данными успешно создан и отправлен!")
    except Exception as e:
        bot.reply_to(message, f"Ошибка при создании Excel файла: {str(e)}")

@bot.message_handler(commands=['import_excel'])
def import_from_excel(message):
    if str(message.chat.id) != ADMIN_CHAT_ID:
        return
    
    bot.reply_to(message, "Пожалуйста, отправьте Excel файл с обновленными данными")
    bot.register_next_step_handler(message, process_excel_file)

def process_excel_file(message):
    if not message.document:
        bot.reply_to(message, "Пожалуйста, отправьте Excel файл")
        return
    
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        with open('travel_data.xlsx', 'wb') as new_file:
            new_file.write(downloaded_file)
        
        success, msg = excel_mgr.update_from_excel()
        bot.reply_to(message, msg)
    except Exception as e:
        bot.reply_to(message, f"Ошибка при обработке файла: {str(e)}")

@bot.callback_query_handler(func=lambda call: call.data == 'back_to_main')
def handle_back_to_main(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    welcome_text = "Выберите интересующий вас раздел:"
    bot.send_message(call.message.chat.id, welcome_text, reply_markup=create_main_menu())

@bot.message_handler(commands=['edit_text'])
def edit_text_command(message):
    if str(message.chat.id) != ADMIN_CHAT_ID:
        return
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    sections = [
        '✈️ Авиабилеты', '🏝 Туры',
        '🏠 Отели', '🚗 Аренда авто',
        '🌍 Визы', '🛡 Страховка',
        '🎫 Экскурсии', '🛄 Консьерж-сервис',
        '💳 Бонусы и акции', '💱 Обмен валют'
    ]
    markup.add(*[types.KeyboardButton(section) for section in sections])
    markup.add(types.KeyboardButton('🔙 Отмена'))
    
    bot.reply_to(message, "Выберите раздел для редактирования:", reply_markup=markup)
    bot.register_next_step_handler(message, process_section_selection)

def process_section_selection(message):
    if message.text == '🔙 Отмена':
        bot.reply_to(message, "Редактирование отменено", reply_markup=create_main_menu())
        return
    
    # Проверяем, что это не команда
    if message.text.startswith('/'):
        return
    
    current_text = db.get_text_block(message.text) or "Текст не задан"
    bot.reply_to(message, 
                 f"Текущий текст для раздела '{message.text}':\n\n{current_text}\n\n"
                 "Отправьте новый текст для этого раздела:",
                 reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, save_section_text, section=message.text)

def save_section_text(message, section):
    # Проверяем, что это не команда
    if message.text.startswith('/'):
        bot.reply_to(message, "Редактирование отменено. Используйте /edit_text для начала редактирования.",
                    reply_markup=create_main_menu())
        return
        
    db.update_text_block(section, message.text)
    bot.reply_to(message, f"✅ Текст для раздела '{section}' успешно обновлен!",
                 reply_markup=create_main_menu())

@bot.message_handler(commands=['add_visa'])
def add_visa(message):
    if str(message.chat.id) != ADMIN_CHAT_ID:
        return
    
    try:
        # Формат: /add_visa "Страна" "Тип визы" длительность цена срок_оформления "требования"
        parts = message.text.split('"')
        country = parts[1]
        visa_type = parts[3]
        rest = parts[4].strip().split()
        duration = int(rest[0])
        price = float(rest[1])
        processing_time = int(rest[2])
        requirements = parts[5] if len(parts) > 5 else ""
        
        visa_id = db.add_visa(country, visa_type, duration, price, processing_time, requirements)
        bot.reply_to(message, f"Виза успешно добавлена (ID: {visa_id})")
    except (ValueError, IndexError):
        bot.reply_to(message, 'Неверный формат. Используйте: /add_visa "Вьетнам" "Туристическая" 90 40 5 "Загранпаспорт, фото"')

@bot.message_handler(commands=['edit_visas'])
def edit_visas_text(message):
    if str(message.chat.id) != ADMIN_CHAT_ID:
        return
    current_text = db.get_text_block('🌍 Визы') or "Текст не задан"
    bot.reply_to(message, 
                 f"Текущий текст раздела Визы:\n\n{current_text}\n\n"
                 "Отправьте новый текст для этого раздела:")
    bot.register_next_step_handler(message, save_section_text, '🌍 Визы')

@bot.message_handler(commands=['edit_insurance'])
def edit_insurance_text(message):
    if str(message.chat.id) != ADMIN_CHAT_ID:
        return
    current_text = db.get_text_block('🛡 Страховка') or "Текст не задан"
    bot.reply_to(message, 
                 f"Текущий текст раздела Страховка:\n\n{current_text}\n\n"
                 "Отправьте новый текст для этого раздела:")
    bot.register_next_step_handler(message, save_section_text, '🛡 Страховка')

@bot.message_handler(commands=['edit_concierge'])
def edit_concierge_text(message):
    if str(message.chat.id) != ADMIN_CHAT_ID:
        return
    current_text = db.get_text_block('🛄 Консьерж-сервис') or "Текст не задан"
    bot.reply_to(message, 
                 f"Текущий текст раздела Консьерж-сервис:\n\n{current_text}\n\n"
                 "Отправьте новый текст для этого раздела:")
    bot.register_next_step_handler(message, save_section_text, '🛄 Консьерж-сервис')

@bot.message_handler(commands=['edit_bonuses'])
def edit_bonuses_text(message):
    if str(message.chat.id) != ADMIN_CHAT_ID:
        return
    current_text = db.get_text_block('💳 Бонусы и акции') or "Текст не задан"
    bot.reply_to(message, 
                 f"Текущий текст раздела Бонусы и акции:\n\n{current_text}\n\n"
                 "Отправьте новый текст для этого раздела:")
    bot.register_next_step_handler(message, save_section_text, '💳 Бонусы и акции')

@bot.message_handler(commands=['edit_exchange'])
def edit_exchange_text(message):
    if str(message.chat.id) != ADMIN_CHAT_ID:
        return
    current_text = db.get_text_block('💱 Обмен валют') or "Текст не задан"
    bot.reply_to(message, 
                 f"Текущий текст раздела Обмен валют:\n\n{current_text}\n\n"
                 "Отправьте новый текст для этого раздела:")
    bot.register_next_step_handler(message, save_section_text, '💱 Обмен валют')

def save_section_text(message, section):
    db.update_text_block(section, message.text)
    bot.reply_to(message, f"✅ Текст для раздела '{section}' успешно обновлен!",
                 reply_markup=create_main_menu())

@bot.message_handler(func=lambda message: message.text == '🛡 Страховка')
def insurance_menu(message):
    custom_text = db.get_text_block('🛡 Страховка')
    if custom_text:
        bot.send_message(message.chat.id, custom_text, parse_mode='HTML')

@bot.message_handler(func=lambda message: message.text == '🛄 Консьерж-сервис')
def concierge_menu(message):
    custom_text = db.get_text_block('🛄 Консьерж-сервис')
    if custom_text:
        bot.send_message(message.chat.id, custom_text, parse_mode='HTML')

@bot.message_handler(func=lambda message: message.text == '💳 Бонусы и акции')
def bonuses_menu(message):
    custom_text = db.get_text_block('💳 Бонусы и акции')
    if custom_text:
        bot.send_message(message.chat.id, custom_text, parse_mode='HTML')

@bot.message_handler(func=lambda message: message.text == '💱 Обмен валют')
def exchange_menu(message):
    custom_text = db.get_text_block('💱 Обмен валют')
    if custom_text:
        bot.send_message(message.chat.id, custom_text, parse_mode='HTML')

bot.polling(none_stop=True) 