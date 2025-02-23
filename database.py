import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('travel_agency.db', check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Таблица для авиабилетов
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS flights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_city TEXT NOT NULL,
            to_city TEXT NOT NULL,
            date TEXT NOT NULL,
            price REAL NOT NULL,
            available_seats INTEGER NOT NULL
        )
        ''')

        # Таблица для туров
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tours (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            destination TEXT NOT NULL,
            duration INTEGER NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            available_places INTEGER NOT NULL
        )
        ''')

        # Таблица для отелей
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS hotels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            stars INTEGER NOT NULL,
            price_per_night REAL NOT NULL,
            description TEXT
        )
        ''')

        # Таблица для виз
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS visas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            country TEXT NOT NULL,
            type TEXT NOT NULL,
            duration INTEGER NOT NULL,
            price REAL NOT NULL,
            processing_time INTEGER NOT NULL,
            requirements TEXT
        )
        ''')

        # Таблица для экскурсий
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS excursions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            duration INTEGER NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            available_places INTEGER NOT NULL
        )
        ''')

        # Таблица для заявок пользователей
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            user_name TEXT,
            service_type TEXT NOT NULL,
            service_id INTEGER NOT NULL,
            status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            contact_info TEXT
        )
        ''')

        # Таблица для текстовых блоков
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS text_blocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            section TEXT NOT NULL,
            content TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        self.conn.commit()

    def add_flight(self, from_city, to_city, date, price, seats):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO flights (from_city, to_city, date, price, available_seats)
        VALUES (?, ?, ?, ?, ?)
        ''', (from_city, to_city, date, price, seats))
        self.conn.commit()
        return cursor.lastrowid

    def add_tour(self, name, destination, duration, price, description, places):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO tours (name, destination, duration, price, description, available_places)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, destination, duration, price, description, places))
        self.conn.commit()
        return cursor.lastrowid

    def add_hotel(self, name, location, stars, price, description):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO hotels (name, location, stars, price_per_night, description)
        VALUES (?, ?, ?, ?, ?)
        ''', (name, location, stars, price, description))
        self.conn.commit()
        return cursor.lastrowid

    def create_request(self, user_id, user_name, service_type, service_id, contact_info):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO requests (user_id, user_name, service_type, service_id, status, contact_info)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, user_name, service_type, service_id, 'new', contact_info))
        self.conn.commit()
        return cursor.lastrowid

    def get_flights(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM flights WHERE available_seats > 0')
        return cursor.fetchall()

    def get_tours(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM tours WHERE available_places > 0')
        return cursor.fetchall()

    def get_hotels(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM hotels')
        return cursor.fetchall()

    def get_requests(self, status=None):
        cursor = self.conn.cursor()
        if status:
            cursor.execute('SELECT * FROM requests WHERE status = ?', (status,))
        else:
            cursor.execute('SELECT * FROM requests')
        return cursor.fetchall()

    def update_request_status(self, request_id, new_status):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE requests SET status = ? WHERE id = ?', (new_status, request_id))
        self.conn.commit()

    def add_visa(self, country, visa_type, duration, price, processing_time, requirements):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO visas (country, type, duration, price, processing_time, requirements)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (country, visa_type, duration, price, processing_time, requirements))
        self.conn.commit()
        return cursor.lastrowid

    def add_excursion(self, name, location, duration, price, description, available_places):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO excursions (name, location, duration, price, description, available_places)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, location, duration, price, description, available_places))
        self.conn.commit()
        return cursor.lastrowid

    def get_all_flights(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM flights')
        return cursor.fetchall()

    def get_all_tours(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM tours')
        return cursor.fetchall()

    def get_all_hotels(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM hotels')
        return cursor.fetchall()

    def get_all_visas(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM visas')
        return cursor.fetchall()

    def get_all_excursions(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM excursions')
        return cursor.fetchall()

    def clear_flights(self):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM flights')
        self.conn.commit()

    def clear_tours(self):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM tours')
        self.conn.commit()

    def clear_hotels(self):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM hotels')
        self.conn.commit()

    def clear_visas(self):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM visas')
        self.conn.commit()

    def clear_excursions(self):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM excursions')
        self.conn.commit()

    def create_text_blocks_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS text_blocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            section TEXT NOT NULL,
            content TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        self.conn.commit()

    def update_text_block(self, section, content):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT OR REPLACE INTO text_blocks (section, content, updated_at)
        VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (section, content))
        self.conn.commit()

    def get_text_block(self, section):
        cursor = self.conn.cursor()
        cursor.execute('SELECT content FROM text_blocks WHERE section = ?', (section,))
        result = cursor.fetchone()
        return result[0] if result else None

    def get_visas(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM visas')
        return cursor.fetchall() 