import sqlite3

def init_database():
    conn = sqlite3.connect('travel_agency.db')
    cursor = conn.cursor()

    # Создаем таблицы
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS flights (
        id INTEGER PRIMARY KEY,
        from_city TEXT,
        to_city TEXT,
        date TEXT,
        price REAL,
        available_seats INTEGER
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tours (
        id INTEGER PRIMARY KEY,
        name TEXT,
        destination TEXT,
        duration INTEGER,
        price REAL,
        description TEXT,
        available_places INTEGER
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS hotels (
        id INTEGER PRIMARY KEY,
        name TEXT,
        location TEXT,
        stars INTEGER,
        price_per_night REAL,
        description TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS excursions (
        id INTEGER PRIMARY KEY,
        name TEXT,
        location TEXT,
        duration INTEGER,
        price REAL,
        description TEXT,
        available_places INTEGER
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS text_blocks (
        section TEXT PRIMARY KEY,
        content TEXT
    )
    ''')

    # Добавляем текст для виз
    visa_text = """Прайс-лист на оформление виз во Вьетнам 🇻🇳

📅 Стандартная е-виза на 90 дней:

 • Однократная — 40$
 • Многократная — 65$
 • Срок оформления: 4-6 рабочих дней

⚡️ Срочная е-виза:

 • За 4 часа: 90$ (сингл) / 115$ (мульти)
 • За 1 день: 75$ (сингл) / 100$ (мульти)
 • За 2 дня: 70$ (сингл) / 95$ (мульти)

💼 Стоимость указана окончательная — все сборы и агентское вознаграждение уже включены!

*Срочные визы оформляются только в рабочие дни и часы миграционной службы. Заявку необходимо подавать заранее.

💳 Доступные способы оплаты:

 • 🇷🇺 Сбербанк, Тинькофф
 • 🇺🇦 ПриватБанк, Монобанк
 • 🇰🇿 Kaspi
 • 🟡 USDT
 • 🇻🇳 Перевод в донгах или наличными в Нячанге и Хошимине

💯Мы гарантируем соблюдение сроков! Для заказа, пишите 
WhatsApp 
+84328388945;
+79126549030 
 ✍️@TravelinNewLife.  

https://t.me/TravelNewLife"""

    cursor.execute('''
    INSERT OR REPLACE INTO text_blocks (section, content)
    VALUES (?, ?)
    ''', ('🌍 Визы', visa_text))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_database()
