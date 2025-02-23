import pandas as pd
from datetime import datetime, timedelta

def create_test_excel():
    # Создаем тестовые данные для каждого раздела
    
    # Авиабилеты
    flights_data = {
        'id': range(1, 6),
        'from_city': ['Москва', 'Санкт-Петербург', 'Москва', 'Казань', 'Екатеринбург'],
        'to_city': ['Париж', 'Лондон', 'Дубай', 'Стамбул', 'Анталья'],
        'date': [(datetime.now() + timedelta(days=x)).strftime('%Y-%m-%d') for x in range(5)],
        'price': [50000, 45000, 35000, 25000, 30000],
        'available_seats': [100, 80, 120, 90, 150]
    }
    
    # Туры
    tours_data = {
        'id': range(1, 6),
        'name': ['Романтический Париж', 'Древний Рим', 'Пляжи Мальдив', 'Сафари в Кении', 'Токио и Киото'],
        'destination': ['Франция', 'Италия', 'Мальдивы', 'Кения', 'Япония'],
        'duration': [7, 5, 10, 8, 12],
        'price': [120000, 90000, 250000, 180000, 200000],
        'description': ['Тур по романтическим местам', 'Исторические достопримечательности', 'Отдых на белоснежных пляжах', 'Путешествие по саванне', 'Знакомство с японской культурой'],
        'available_places': [20, 15, 10, 12, 8]
    }
    
    # Отели
    hotels_data = {
        'id': range(1, 6),
        'name': ['Ritz Paris', 'Burj Al Arab', 'Four Seasons', 'Hilton Resort', 'Marriott Grand'],
        'location': ['Париж', 'Дубай', 'Мальдивы', 'Анталья', 'Рим'],
        'stars': [5, 7, 5, 5, 4],
        'price_per_night': [50000, 100000, 80000, 15000, 20000],
        'description': ['Роскошный отель в центре Парижа', 'Самый роскошный отель в мире', 'Виллы на воде', 'Все включено', 'В историческом центре']
    }
    
    # Визы
    visas_data = {
        'id': range(1, 6),
        'country': ['Шенген', 'США', 'ОАЭ', 'Великобритания', 'Япония'],
        'type': ['Туристическая', 'Туристическая', 'Туристическая', 'Туристическая', 'Туристическая'],
        'duration': [90, 180, 30, 180, 90],
        'price': [8000, 15000, 5000, 12000, 7000],
        'processing_time': [10, 14, 3, 15, 5],
        'requirements': ['Загранпаспорт, справка с работы', 'Загранпаспорт, справка с работы, выписка со счета', 'Загранпаспорт', 'Загранпаспорт, справка с работы, выписка со счета', 'Загранпаспорт, бронь отеля']
    }
    
    # Экскурсии
    excursions_data = {
        'id': range(1, 6),
        'name': ['Лувр', 'Колизей', 'Пирамиды Гизы', 'Собор Святого Петра', 'Эйфелева башня'],
        'location': ['Париж', 'Рим', 'Каир', 'Ватикан', 'Париж'],
        'duration': [3, 2, 4, 2, 2],
        'price': [5000, 4000, 6000, 3000, 3500],
        'description': ['Экскурсия по главному музею Франции', 'Посещение древнего амфитеатра', 'Тур к древним пирамидам', 'Экскурсия по главному собору', 'Подъем на символ Парижа'],
        'available_places': [30, 25, 20, 35, 40]
    }
    
    # Создаем Excel файл
    with pd.ExcelWriter('travel_data.xlsx', engine='openpyxl') as writer:
        # Записываем данные на разные листы
        pd.DataFrame(flights_data).to_excel(writer, sheet_name='Flights', index=False)
        pd.DataFrame(tours_data).to_excel(writer, sheet_name='Tours', index=False)
        pd.DataFrame(hotels_data).to_excel(writer, sheet_name='Hotels', index=False)
        pd.DataFrame(visas_data).to_excel(writer, sheet_name='Visas', index=False)
        pd.DataFrame(excursions_data).to_excel(writer, sheet_name='Excursions', index=False)
    
    print("Тестовый Excel файл создан успешно!")

if __name__ == "__main__":
    create_test_excel() 