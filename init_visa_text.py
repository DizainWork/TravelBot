import sqlite3

VIETNAM_VISA_TEXT = """Прайс-лист на оформление виз во Вьетнам 🇻🇳

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

def init_visa_text():
    conn = sqlite3.connect('travel_agency.db')
    cursor = conn.cursor()
    
    # Создаем таблицу, если она не существует
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS text_blocks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        section TEXT NOT NULL,
        content TEXT NOT NULL,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Добавляем текст для раздела виз
    cursor.execute('''
    INSERT OR REPLACE INTO text_blocks (section, content)
    VALUES (?, ?)
    ''', ('🌍 Визы', VIETNAM_VISA_TEXT))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_visa_text() 