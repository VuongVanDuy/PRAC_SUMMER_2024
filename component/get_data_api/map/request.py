import requests
import webbrowser

BASE_URL = "http://localhost:5000"  # Thay đổi URL này thành URL của server nếu khác
TOKEN = "token1"

def get_map(direction, id_route):
    url = f'{BASE_URL}/get-map/{direction}/{id_route}'
    headers = {"Authorization": TOKEN}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return response.text

if __name__ == '__main__':
    res = get_map(1, 1062)
    file_path = 'temp.html'

    # Ghi đoạn HTML vào file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(res['content'])
        
    webbrowser.open(file_path)