import requests

# URL của API
BASE_URL = "http://localhost:5000"  # Thay đổi URL này thành URL của server nếu khác
TOKEN = "token1"  # Thay thế bằng token thực tế

# Hàm gửi yêu cầu thêm thông tin
def add_info(ticket, time):
    url = f"{BASE_URL}/add-info/{ticket}/{time}"
    headers = {"Authorization": TOKEN}
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        return response.json(), True
    else:
        return response.text, False

# Hàm gửi yêu cầu lấy thông tin tuyến đường theo ID
def get_data_route_by_id(direction, routeId):
    url = f"{BASE_URL}/route/{direction}/{routeId}"
    headers = {"Authorization": TOKEN}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json(), True
    else:
        return response.text, False

# Hàm gửi yêu cầu lấy thông tin các điểm dừng
def get_data_stops():
    url = f"{BASE_URL}/stops"
    headers = {"Authorization": TOKEN}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json(), True
    else:
        return response.text, False

# Hàm gửi yêu cầu lấy thông tin các tuyến đường chung
def get_info_all_routes():
    url = f"{BASE_URL}/routes"
    headers = {"Authorization": TOKEN}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json(), True
    else:
        return response.text, False
    
def get_info_route(id_route):
    url = f"{BASE_URL}/route/{id_route}/info"
    headers = {"Authorization": TOKEN}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json(), True
    else:
        return response.text, False

def get_all_ids():
    url = f"{BASE_URL}/all-ids-route"
    headers = {"Authorization": TOKEN}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json(), True
    else:
        return response.text, False

# Ví dụ sử dụng các hàm trên
if __name__ == "__main__":
    # Gọi hàm thêm thông tin
   
    res, code = get_all_ids()
    if code:
        print(res)
    else:
        print('Error!', res)
