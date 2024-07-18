# from bs4 import BeautifulSoup as BS
import os
from datetime import datetime
from pathlib import Path
from loguru import logger as log
from pyowm import OWM
from pyowm.utils.config import get_config_from
from dotenv import load_dotenv

load_dotenv()

log.level("DEBUG")

cfg = get_config_from(Path("api").joinpath("own.json"))
owm = OWM(api_key=os.getenv("OPENWEATHER_TOKEN"), config=cfg)
mgr = owm.weather_manager()


class Weather:

    def __init__(self, text: str):
        self.text = text
        self.temp_value = None
        self.temp_feels = None
        self.cloud_percent = None
        self.humidity_percent = None
        self.wind_speed = None
        self.sunrise_time = None
        self.sunset_time = None
        self.rain_data = None
        self.snow_data = None

    @staticmethod
    def pretty_temp(value: int):
        pre = "+"
        if value < 0:
            pre = "-"
        value = {round(value)}
        return f"{pre}{value}°C"
        

class City:
    def __init__(self, ru: str, en: str, utc: int):
        self.ru = ru
        self.en = en
        self.utc = utc
        self.data = {}

    def _update(self):
        observation = mgr.weather_at_place(self.en)
        return observation.weather
    
    def waether(self):
        w = self._update()
        weather_data = Weather(w.detailed_status.title())
        weather_data.temp_value = round(w.temperature('celsius').get('temp'))
        weather_data.temp_feels = round(w.temperature('celsius').get('feels_like'))
        weather_data.cloud_percent = w.clouds
        weather_data.humidity_percent = w.humidity
        weather_data.wind_speed = w.wnd.get('speed')
        weather_data.sunrise_time = datetime.fromtimestamp(w.sunrise_time())
        weather_data.sunset_time = datetime.fromtimestamp(w.sunset_time())
        weather_data.rain_data = w.rain
        weather_data.snow_data = w.snow
    
class Cities:
    def __init__(self):
        self.cities = {}
    def add(self, key, city: City):
        self.cities[key] = city
    
    def add_many(self, cities: dict[str, City]):
        for key, city in cities.items():
            self.add(key, city)

    def get(self, key: str) -> City:
        return self.cities.get(key)
        

cities = Cities()

cities.add_many(
    {
        "msk": City("Москва", "Moscow,RU", 3),
        "spb": City("Санкт-Петербург", "Saint Petersburg", 3),
        "nvb": City("Новосибирск", "Novosibirsk", 7),
        "ekt": City("Екатеринбург", "Yekaterinburg", 5),
    }
)
