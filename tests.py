import unittest
from utils import get_weather_meteoservice_ru, pretty_info

class TestFunctions(unittest.TestCase):

    def test_weather(self):
        weather = get_weather_meteoservice_ru()
        print(weather)

    def test_pretty_info(self):
        buff = pretty_info()
        print(buff)

if __name__ == '__main__':
    unittest.main()