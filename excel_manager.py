import pandas as pd
from datetime import datetime
import os

class ExcelManager:
    def __init__(self, db):
        self.db = db
        self.excel_file = 'travel_data.xlsx'

    def create_excel(self):
        """Создание Excel файла с данными из БД"""
        with pd.ExcelWriter(self.excel_file, engine='openpyxl') as writer:
            # Авиабилеты
            flights_data = self.db.get_all_flights()
            flights_df = pd.DataFrame(flights_data, columns=[
                'id', 'from_city', 'to_city', 'date', 'price', 'available_seats'
            ])
            flights_df.to_excel(writer, sheet_name='Flights', index=False)

            # Туры
            tours_data = self.db.get_all_tours()
            tours_df = pd.DataFrame(tours_data, columns=[
                'id', 'name', 'destination', 'duration', 'price', 'description', 'available_places'
            ])
            tours_df.to_excel(writer, sheet_name='Tours', index=False)

            # Отели
            hotels_data = self.db.get_all_hotels()
            hotels_df = pd.DataFrame(hotels_data, columns=[
                'id', 'name', 'location', 'stars', 'price_per_night', 'description'
            ])
            hotels_df.to_excel(writer, sheet_name='Hotels', index=False)

            # Визы
            visas_data = self.db.get_all_visas()
            visas_df = pd.DataFrame(visas_data, columns=[
                'id', 'country', 'type', 'duration', 'price', 'processing_time', 'requirements'
            ])
            visas_df.to_excel(writer, sheet_name='Visas', index=False)

            # Экскурсии
            excursions_data = self.db.get_all_excursions()
            excursions_df = pd.DataFrame(excursions_data, columns=[
                'id', 'name', 'location', 'duration', 'price', 'description', 'available_places'
            ])
            excursions_df.to_excel(writer, sheet_name='Excursions', index=False)

        return self.excel_file

    def update_from_excel(self):
        """Обновление БД данными из Excel"""
        if not os.path.exists(self.excel_file):
            return False, "Excel файл не найден"

        try:
            # Обновляем авиабилеты
            flights_df = pd.read_excel(self.excel_file, sheet_name='Flights')
            self.db.clear_flights()
            for _, row in flights_df.iterrows():
                self.db.add_flight(
                    str(row['from_city']), 
                    str(row['to_city']), 
                    str(row['date']), 
                    float(row['price']), 
                    int(row['available_seats'])
                )

            # Обновляем туры
            tours_df = pd.read_excel(self.excel_file, sheet_name='Tours')
            self.db.clear_tours()
            for _, row in tours_df.iterrows():
                self.db.add_tour(
                    str(row['name']), 
                    str(row['destination']), 
                    int(row['duration']),
                    float(row['price']), 
                    str(row['description']), 
                    int(row['available_places'])
                )

            # Обновляем отели
            hotels_df = pd.read_excel(self.excel_file, sheet_name='Hotels')
            self.db.clear_hotels()
            for _, row in hotels_df.iterrows():
                self.db.add_hotel(
                    str(row['name']), 
                    str(row['location']), 
                    int(row['stars']),
                    float(row['price_per_night']), 
                    str(row['description'])
                )

            # Обновляем визы
            visas_df = pd.read_excel(self.excel_file, sheet_name='Visas')
            self.db.clear_visas()
            for _, row in visas_df.iterrows():
                self.db.add_visa(
                    str(row['country']), 
                    str(row['type']), 
                    int(row['duration']),
                    float(row['price']), 
                    int(row['processing_time']), 
                    str(row['requirements'])
                )

            # Обновляем экскурсии
            excursions_df = pd.read_excel(self.excel_file, sheet_name='Excursions')
            self.db.clear_excursions()
            for _, row in excursions_df.iterrows():
                self.db.add_excursion(
                    str(row['name']), 
                    str(row['location']), 
                    int(row['duration']),
                    float(row['price']), 
                    str(row['description']), 
                    int(row['available_places'])
                )

            return True, "Данные успешно обновлены"
        except Exception as e:
            return False, f"Ошибка при обновлении данных: {str(e)}" 