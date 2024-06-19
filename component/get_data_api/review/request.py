import requests

BASE_URL = 'http://127.0.0.1:5000'
TOKEN = 'token1'  # Thay thế bằng token hợp lệ của bạn

# Headers chung
headers = {
    'Authorization': TOKEN,
    'Content-Type': 'application/json'
}

# Hàm để lấy tất cả đánh giá của một tuyến đường
def get_reviews_of_route(id_route):
    url = f"{BASE_URL}/reviews/{id_route}"
    response = requests.get(url, headers=headers)
    return response.json()

# Hàm để thêm đánh giá mới
def add_review(id_user, id_route, star_vote, comment):
    url = f"{BASE_URL}/review"
    data = {
        'id_user': id_user,
        'id_route': id_route,
        'star_vote': star_vote,
        'comment': comment
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Hàm để lấy thời gian đánh giá của một tuyến đường
def get_review_time(user_name, id_route):
    url = f"{BASE_URL}/review_time"
    params = {
        'user_name': user_name,
        'id_route': id_route
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

# Hàm để lấy tất cả đánh giá của người dùng
def get_all_reviews_of_user():
    url = f"{BASE_URL}/reviews"
    response = requests.get(url, headers=headers)
    return response.json()

# Ví dụ sử dụng các hàm trên
if __name__ == "__main__":
    # Lấy tất cả đánh giá của một tuyến đường
    id_route = 1062
    reviews_route_response = get_reviews_of_route(id_route)
    print(f"Get Reviews of Route Response: {reviews_route_response}")

    # Thêm đánh giá mới
    review_response = add_review(1, 1062, 5, 'Great route!')
    print(f"Add Review Response: {review_response}")

    # Lấy thời gian đánh giá của một tuyến đường
    review_time_response = get_review_time("user1", 1062)
    print(f"Get Review Time Response: {review_time_response}")

    # Lấy tất cả đánh giá của người dùng
    all_reviews_response = get_all_reviews_of_user()
    print(f"Get All Reviews of User Response: {all_reviews_response}")
