import sys
import requests
from PyQt5.QtWidgets import QApplication, QTableView, QVBoxLayout, QWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class DataUsers:
    def __init__(self):
        self.base_url = 'http://127.0.0.1:5000'
    
    def login_and_get_token(self, username, password):
        url = f"{self.base_url}/login"
        data = {
            'username': username,
            'password': password
        }
        response = requests.post(url, json=data)

        if response.status_code == 200:
            token = response.json()['access_token']
            return token, True
        else:
            return None, False
      
    # Hàm để lấy tất cả người dùng
    def get_users(self):
        url = f"{self.base_url}/users"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    # Hàm để thêm người dùng mới
    def register(self, username, password, link_icon):
        url = f"{self.base_url}/register"
        data = {
            'username': username,
            'password': password,
            'link_icon': link_icon,
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    # Hàm để cập nhật link_icon của người dùng
    def update_link_icon(self, username, link_icon, token):
        url = f"{self.base_url}/user/{username}/link_icon"
        data = {
            'link_icon': link_icon
        }
        headers = {
                    'Authorization': f'Bearer {token}'
                }
        response = requests.put(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    # Hàm để cập nhật mật khẩu của người dùng
    def update_password(self, username, password, token):
        url = f"{self.base_url}/user/{username}/password"
        data = {
            'password': password
        }
        headers = {
                    'Authorization': f'Bearer {token}'
                }
        response = requests.put(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    # Hàm để lấy mật khẩu của người dùng
    def get_user_password(self, username, token):
        url = f"{self.base_url}/user/{username}/password"
        headers = {
                    'Authorization': f'Bearer {token}'
                }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return result['password']
        else:
            return None

    # Hàm để lấy link_icon của người dùng
    def get_user_link_icon(self, username, token):
        url = f"{self.base_url}/user/{username}/link_icon"
        headers = {
                    'Authorization': f'Bearer {token}'
                }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return result['link_icon']
        else:
            return None

    # Hàm để lấy ID của người dùng
    def get_id_user(self, username, token):
        url = f"{self.base_url}/user/{username}/id_user"
        headers = {
                    'Authorization': f'Bearer {token}'
                }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return result['id_user']
        else:
            return None

    # Hàm để lấy tất cả đánh giá của một tuyến đường
    def get_reviews_of_route(self, id_route):
        url = f"{self.base_url}/reviews/{id_route}"
        response = requests.get(url)
        if response.status_code == 200:
            result = response.json()
            return result['result']
        else:
            return None
    
    # Hàm để thêm đánh giá mới
    def add_review(self, id_user, id_route, star_vote, comment, token):
        url = f"{self.base_url}/review"
        data = {
            'id_user': id_user,
            'id_route': id_route,
            'star_vote': star_vote,
            'comment': comment
        }
        headers = {
                    'Authorization': f'Bearer {token}'
                }
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()  # Kiểm tra lỗi HTTP
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return None
        except Exception as err:
            print(f"Other error occurred: {err}")
            return None

class EmployeeTableView(QWidget):
    def __init__(self, data, headers):
        super().__init__()
        self.setGeometry(100, 100, 600, 600)
        self.layout = QVBoxLayout()
        self.table_view = QTableView()
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(headers)
        
        for row in data:
            items = [QStandardItem(str(field)) for field in row]
            self.model.appendRow(items)
        
        self.table_view.setModel(self.model)
        self.layout.addWidget(self.table_view)
        self.setLayout(self.layout)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)

    get_user = DataUsers()
    results = get_user.get_users()['result']
    # password = get_user.get_user_link_icon('daicaduy')
    # print(password)
    users_data = []
    for res in results:
        user = [res['id'], res['username'], res['password'], res['link_icon'], res['token']]
        users_data.append(user)
    users_headers = ["ID", "Username", "Password", "Link Icon", "token"]
    # review_headers = ["ID", "ID_User", "Star vote", "Comment"]
    
    view = EmployeeTableView(users_data, users_headers)
    view.show()
    
    sys.exit(app.exec_())
