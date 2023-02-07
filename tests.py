from utils import get_holiday, get_weather
import sys
from bot import store

if __name__ == "__main__":
    # users = store.get_users()
    # for u in users:
    #     print(u)
    h = get_holiday()
    print(h)