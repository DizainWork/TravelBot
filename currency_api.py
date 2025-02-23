import json
from datetime import datetime
import requests
import os

RATES_FILE = 'currency_rates.json'

def get_currency_rates():
    """Получение курсов валют из внешнего API"""
    api_key = os.getenv('EXCHANGE_RATE_API_KEY')
    base_url = f"http://api.exchangeratesapi.io/v1/latest?access_key={api_key}&base=EUR"
    
    try:
        response = requests.get(base_url)
        data = response.json()
        return data['rates']
    except Exception as e:
        print(f"Error fetching rates: {e}")
        return None

def get_stored_rates():
    """Получение сохраненных курсов валют"""
    try:
        with open(RATES_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def update_currency_rate(currency, rate):
    """Обновление курса валюты"""
    rates = get_stored_rates()
    
    rates[currency] = {
        'rate': rate,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    with open(RATES_FILE, 'w') as f:
        json.dump(rates, f, indent=4) 