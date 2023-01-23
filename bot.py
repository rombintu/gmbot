import requests

class Bot:
    def __init__(self, token):
        self.token = token
        # self.uuid = uuid

    def send_message(self, text, too):
        response = requests.post(
                url='https://api.telegram.org/bot{0}/sendMessage'.format(self.token),
                data={'chat_id': too, 'text': text, 'parse_mode': 'markdown'}
            ).json()
        print(response)