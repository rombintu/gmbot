import pytest 

from internal.utils import get_weather_meteoservice_ru, pretty_info
from internal import Text, draw

def test_weather():
    weather = get_weather_meteoservice_ru()
    print(weather)

def test_pretty_info():
    buff = pretty_info()
    print(buff)

def test_draw():
    text = Text("В прогнозе на сегодня \nв Москве холодная слегка\n облачная погода. Диапазон температур от -20 до -13° днем и от -16 до -13 ночью. Ожидается маловетреная погода,\n в основном 6 м/с, порывами до 12 м/с. Днем осадков не ожидается.  Уделите пару минут почасовому прогнозу ниже")
    draw(text)


# if __name__ == '__main__':
    # 