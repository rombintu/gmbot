import pytest 
from api.weather import cities, log
from tools.image import Assets

def test_weather():
    msk = cities.get('msk')
    msk.load_waether()
    data = msk.waether()
    assert data is not None, "Weather data not loaded"
    log.info(f"Weather data for Moscow: {data}")

def test_draw():
    canvas = Assets(400, "./assets")
    canvas.draw_weather_temp( "light-rain", "сильная гроза", "+11°C", "+10°C")
    canvas.draw_suntime("07:00", "21:00")
    canvas.draw_weather_options(40, 10, 75)
    canvas.draw_finance(70.0, 80.0, 5623221)
    canvas.bg_image.save(canvas.save_path)