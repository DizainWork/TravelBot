import pandas as pd
from datetime import datetime
import os

class ExcelManager:
    def __init__(self, db):
        self.db = db

    def create_excel(self):
        # Получаем данные из базы
        flights = self.db.get_flights()
        tours = self.db.get_tours()
        hotels = self.db.get_hotels()
        excursions = self.db.get_excursions()

        # Создаем DataFrame для каждой таблицы
        df_flights = pd.DataFrame(flights, columns=['id', 'from_city', 'to_city', 'date', 'price', 'available_seats'])
        df_tours = pd.DataFrame(tours, columns=['id', 'name', 'destination', 'duration', 'price', 'description', 'available_places'])
        df_hotels = pd.DataFrame(hotels, columns=['id', 'name', 'location', 'stars', 'price_per_night', 'description'])
        df_excursions = pd.DataFrame(excursions, columns=['id', 'name', 'location', 'duration', 'price', 'description', 'available_places'])

        # Создаем Excel файл
        with pd.ExcelWriter('travel_data.xlsx', engine='openpyxl') as writer:
            df_flights.to_excel(writer, sheet_name='Flights', index=False)
            df_tours.to_excel(writer, sheet_name='Tours', index=False)
            df_hotels.to_excel(writer, sheet_name='Hotels', index=False)
            df_excursions.to_excel(writer, sheet_name='Excursions', index=False)

        return 'travel_data.xlsx'

    def update_from_excel(self):
        try:
            # Загружаем данные из Excel
            df_flights = pd.read_excel('travel_data.xlsx', sheet_name='Flights')
            df_tours = pd.read_excel('travel_data.xlsx', sheet_name='Tours')
            df_hotels = pd.read_excel('travel_data.xlsx', sheet_name='Hotels')
            df_excursions = pd.read_excel('travel_data.xlsx', sheet_name='Excursions')

            # Обновляем базу данных
            self.db.update_flights(df_flights.to_dict('records'))
            self.db.update_tours(df_tours.to_dict('records'))
            self.db.update_hotels(df_hotels.to_dict('records'))
            self.db.update_excursions(df_excursions.to_dict('records'))

            return True, "Данные успешно обновлены"
        except Exception as e:
            return False, f"Ошибка при обновлении данных: {str(e)}"
