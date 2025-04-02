import requests
from config import API_KEY, CITY, LANG, UNITS

def fetch_weather():
    return _fetch_weather_at_index(0)

def fetch_weather_later():
    return _fetch_weather_at_index(2)  # ~6h später

def _fetch_weather_at_index(index):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units={UNITS}&lang={LANG}"
    try:
        res = requests.get(url)
        data = res.json()

        if "list" not in data:
            raise Exception(data.get("message", "Fehler beim Abruf"))

        item = data["list"][index]
        return {
            "temperature": round(item["main"]["temp"], 1),
            "description": item["weather"][0]["description"].capitalize(),
            "wind": f"{item['wind']['speed']}km/h",
            "icon": item["weather"][0]["icon"]
        }

    except Exception as e:
        return {
            "temperature": "-",
            "description": f"Fehler: {e}",
            "wind": "-",
            "icon": "01d"
        }
