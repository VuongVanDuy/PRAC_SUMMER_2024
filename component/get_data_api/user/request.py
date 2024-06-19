import requests

BASE_URL = 'http://127.0.0.1:5000'
TOKEN = 'token1'  # Thay thế bằng token hợp lệ của bạn

# Headers chung
headers = {
    'Authorization': TOKEN,
    'Content-Type': 'application/json'
}

# Hàm để lấy tất cả người dùng
def get_users():
    url = f"{BASE_URL}/users"
    response = requests.get(url, headers=headers)
    return response.json()

# Hàm để thêm người dùng mới
def add_user(username, password, link_icon):
    url = f"{BASE_URL}/user"
    data = {
        'username': username,
        'password': password,
        'link_icon': link_icon
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Hàm để cập nhật link_icon của người dùng
def update_link_icon(username, link_icon):
    url = f"{BASE_URL}/user/{username}/link_icon"
    data = {
        'link_icon': link_icon
    }
    response = requests.put(url, headers=headers, json=data)
    return response.json()

# Hàm để cập nhật mật khẩu của người dùng
def update_password(username, password):
    url = f"{BASE_URL}/user/{username}/password"
    data = {
        'password': password
    }
    response = requests.put(url, headers=headers, json=data)
    return response.json()

# Hàm để lấy mật khẩu của người dùng
def get_user_password(username):
    url = f"{BASE_URL}/user/{username}/password"
    response = requests.get(url, headers=headers)
    return response.json()

# Hàm để lấy link_icon của người dùng
def get_user_link_icon(username):
    url = f"{BASE_URL}/user/{username}/link_icon"
    response = requests.get(url, headers=headers)
    return response.json()

# Hàm để lấy ID của người dùng
def get_id_user(username):
    url = f"{BASE_URL}/user/{username}/id_user"
    response = requests.get(url, headers=headers)
    return response.json()

# Ví dụ sử dụng các hàm trên
if __name__ == "__main__":
    # Lấy tất cả người dùng
    users_response = get_users()
    print(f"Get Users Response: {users_response}")

    # Thêm người dùng mới
    user_response = add_user('user1', 'password1', './pictures/avatar_default.png')
    print(f"Add User Response: {user_response}")

    # Cập nhật link_icon của người dùng
    update_icon_response = update_link_icon('user1', './pictures/new_avatar.png')
    print(f"Update Link Icon Response: {update_icon_response}")

    # Cập nhật mật khẩu của người dùng
    update_password_response = update_password('user1', 'new_password1')
    print(f"Update Password Response: {update_password_response}")

    # Lấy mật khẩu của người dùng
    password_response = get_user_password('user1')
    print(f"Get User Password Response: {password_response}")

    # Lấy link_icon của người dùng
    link_icon_response = get_user_link_icon('user1')
    print(f"Get User Link Icon Response: {link_icon_response}")

    # Lấy ID của người dùng
    user_id_response = get_id_user('user1')
    print(f"Get User ID Response: {user_id_response}")
