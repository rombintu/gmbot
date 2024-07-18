import requests

def get_finance_rub(valutes: list[str]):
    try:
        curs_dict = {}
        req = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
        for valute in valutes:
            curs_dict[valute] = str(round(req['Valute'][valute]['Value'], 2))
    except Exception:
        return None

def get_finance_bitcoin(convert: int = 0):
    try:
        req: dict = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json').json()
        data = int(req.get('bpi').get('USD').get('rate_float'))
        if convert:
            return data * convert
        return data
    except Exception:
        return None