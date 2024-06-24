import sys
import requests

BASE_URL = 'http://127.0.0.1:5000'

class data_update():
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
    
    def get_info_update(self):
        url = f"{self.base_url}/info-update"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    
    def get_data_update(self):
        url = f"{self.base_url}/update"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    
    def update_status_update(self, status):
        url = f"{self.base_url}/status-update"
        data = {
            'status': status
        }
        response = requests.put(url, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None


if __name__ == '__main__':
    up = data_update()
    print(up.get_info_update())
        