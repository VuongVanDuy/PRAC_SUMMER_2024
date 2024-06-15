import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QTableView, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class DatabaseManager:
    def __init__(self, database_name):
        try:
            self.conn = sqlite3.connect(database_name)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(e)
        self.create_table_user()
        self.create_table_review_of_user()

    def create_table_user(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS user(
                                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                    username VARCHAR(20) UNIQUE, 
                                    password VARCHAR(20) NOT NULL,
                                    link_icon VARCHAR(100) NOT NULL
                                );''')
            self.conn.commit()
        except Exception as e:
            print(e)
        
    def insert_user(self, username, password, link_icon):
        try:
            self.cursor.execute('''INSERT INTO user(username, password, link_icon) 
                                VALUES (?, ?, ?)''', (username, password, link_icon))
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
            
    def create_table_review_of_user(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS review_of_user( 
                                    id_user INTEGER,
                                    id_route INTEGER, 
                                    star_vote INTEGER,
                                    comment VARCHAR(100),
                                    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                    PRIMARY KEY(id_user, id_route)
                                    FOREIGN KEY(id_user) REFERENCES user(id)
                                );''')
            self.conn.commit()
        except Exception as e:
            print(e)
        
    def insert_review_of_user(self, id_user, id_route, star_vote, comment):
        try:
            self.cursor.execute(''' INSERT INTO review_of_user (id_user, id_route, star_vote, comment, time)
                                    VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                                    ON CONFLICT(id_user, id_route) 
                                    DO UPDATE SET
                                        star_vote = excluded.star_vote,
                                        comment = excluded.comment,
                                        time = CURRENT_TIMESTAMP;''', (id_user, id_route, star_vote, comment))
            self.conn.commit()
        except Exception as e:
            print(e)
    
    def update_link_icon(self, name_user, link_icon):
        try:
            self.cursor.execute("UPDATE user SET link_icon = ? WHERE username = ?", (link_icon, name_user))
            self.conn.commit()
        except Exception as e:
            print(e)
    
    def update_password(self, name_user, password):
        try:
            self.cursor.execute("UPDATE user SET password = ? WHERE username = ?", (password, name_user))
            self.conn.commit()
        except Exception as e:
            print(e)
    
    def get_password(self, name_user):
        try:
            self.cursor.execute("SELECT password FROM user WHERE username = ?", (name_user,))
            return self.cursor.fetchone()[0]
        except Exception as e:
            return None
        
    def get_link_icon(self, name_user):
        try:
            self.cursor.execute("SELECT link_icon FROM user WHERE username = ?", (name_user,))
            return self.cursor.fetchone()[0]
        except Exception as e:
            return None
    
    def get_time_review_route(self, user_name, id_route):
        try:
            sql = '''SELECT review_of_user.time
                    FROM review_of_user
                    WHERE review_of_user.id_user = (
                        SELECT id
                        FROM user
                        WHERE username = ?
                    )
                    AND review_of_user.id_route = ?;
                    '''
            self.cursor.execute(sql, (user_name, id_route))
            return self.cursor.fetchone()[0]
        except Exception as e:
            return None
    
    def get_id_user(self, name_user):
        try:
            self.cursor.execute("SELECT id FROM user WHERE username = ?", (name_user,))
            return self.cursor.fetchone()[0]
        except Exception as e:
            return None
    
    def fetch_all_users(self):
        try:
            self.cursor.execute("SELECT * FROM user")
            return self.cursor.fetchall()
        except Exception as e:
            return None

    def fetch_all_reviews_of_route(self, id_route):
        try:
            sql = '''SELECT user.username, review_of_user.star_vote, review_of_user.comment, review_of_user.time, user.link_icon
                    FROM review_of_user
                    INNER JOIN user ON review_of_user.id_user = user.id
                    WHERE review_of_user.id_route = ?;
                    '''
            self.cursor.execute(sql, (id_route,))
            reviews = [review for review in self.cursor.fetchall()]
            return reviews
        except Exception as e:
            return None
    
    def fetch_all_reviews_of_user(self):
        try:
            self.cursor.execute("SELECT * FROM review_of_user;")
            return self.cursor.fetchall()
        except Exception as e:
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

    db_manager = DatabaseManager("data_app.db")
   
    # 10 users in list
    list_users = [
        ("user1", "password1", "./pictures/avatar_default.png"),
        ("user2", "password2", "./pictures/avatar_default.png"),
        ("user3", "password3", "./pictures/avatar_default.png"),
        ("user4", "password4", "./pictures/avatar_default.png"),
        ("user5", "password5", "./pictures/avatar_default.png"),
        ("user6", "password6", "./pictures/avatar_default.png"),
        ("user7", "password7", "./pictures/avatar_default.png"),
        ("user8", "password8", "./pictures/avatar_default.png"),
        ("user9", "password9", "./pictures/avatar_default.png"),
        ("user10", "password10", "./pictures/avatar_default.png")
    ]
    for user in list_users:
        db_manager.insert_user(user[0], user[1], user[2])
    
    # 5 comments of users
    list_review_of_user = [
        (1, 1063, 5, "comment1"),
        (2, 1064, 4, "comment2"),
        (3, 1065, 3, "comment3"),
        (4, 1062, 2, "comment4"),
        (5, 1062, 1, "comment5")
    ]
    for review in list_review_of_user:
        db_manager.insert_review_of_user(review[0], review[1], review[2], review[3])
    
    db_manager.insert_review_of_user(1, 1062, 5, "fixed comment1")

    
    users_data = db_manager.fetch_all_users()
    reviews_user = db_manager.fetch_all_reviews_of_route(1062)
    print(reviews_user)
    users_headers = ["ID", "Username", "Password", "Link Icon"]
    review_headers = ["ID", "ID_User", "Star vote", "Comment"]
    
    view = EmployeeTableView(reviews_user, review_headers)
    view.show()
    
    sys.exit(app.exec_())
