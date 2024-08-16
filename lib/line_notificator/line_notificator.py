import os
import requests

class LineNotificater:
    def __init__(self):
        self.token = os.getenv('LINE_NOTIFY_TOKEN')
        self.url = 'https://notify-api.line.me/api/notify'
        self.headers = {'Authorization': 'Bearer ' + self.token}

    def notify(self, msg):
        payload = {'message': msg}
        response = requests.post(self.url, headers=self.headers, data=payload)
        return response.status_code
