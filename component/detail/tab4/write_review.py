import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox, QMessageBox, QFrame)
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize, pyqtSignal

class StarRatingWidget(QWidget):
    ratingChanged = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        self.stars = []

        for i in range(5):
            star = QPushButton("☆")
            star.setFont(QFont('Arial', 20))
            star.setStyleSheet("border: none;")
            star.setCheckable(True)
            star.clicked.connect(self.update_rating)
            self.stars.append(star)
            layout.addWidget(star)

        self.setLayout(layout)
        self.rating = 0

    def update_rating(self):
        button = self.sender()
        for i in range(5):
            if self.stars[i] == button:
                for j in range(i+1):
                    self.stars[j].setText("★")
                for j in range(i+1, 5):
                    self.stars[j].setText("☆")
                self.rating = i + 1
                self.ratingChanged.emit(self.rating)
                break

    def reset_rating(self):
        self.rating = 0
        self.ratingChanged.emit(self.rating)
        for star in self.stars:
            star.setText("☆")
            star.setChecked(False)

class ReviewForm(QWidget):
    request_review = pyqtSignal(int, str)
    
    def __init__(self, routeId, user_name, link_icon):
        super().__init__()
        self.routeId = routeId
        self.user_name = user_name
        self.link_icon = link_icon
        self.initUI()
        
        self.star_rating.ratingChanged.connect(lambda: self.submit_button.setEnabled(False if self.star_rating.rating == 0 else True))
        self.star_rating.ratingChanged.connect(lambda: self.error_label.setVisible(False if self.star_rating.rating != 0 else True))
    
    def initUI(self):
        self.setWindowTitle('Review Form')
        self.setGeometry(100, 100, 400, 400)
        self.setWindowIcon(QIcon('./pictures/review.png'))
        layout = QVBoxLayout()

        title_label = QLabel('ОТЗЫВ АВТОБУСНОГО МАРШРУТА')
        title_label.setFont(QFont('Arial', 14, QFont.Bold))
        title_label.setStyleSheet("color: #00A76F;")
        layout.addWidget(title_label, alignment=Qt.AlignCenter)

        route_label = QLabel(f'№ маршрута {self.routeId}')
        route_label.setFont(QFont('Arial', 10))
        route_label.setStyleSheet("color: #00A76F;")
        layout.addWidget(route_label)

        user_info_layout = QHBoxLayout()
        
        user_icon = QLabel()
        user_icon.setFixedSize(50, 50)
        user_icon.setPixmap(QPixmap(self.link_icon).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Replace with your user icon path
        user_info_layout.addWidget(user_icon)

        user_info_text_layout = QVBoxLayout()
        user_name_label = QLabel(f'{self.user_name}')
        user_name_label.setFont(QFont('Arial', 12, QFont.Bold))
        user_info_text_layout.addWidget(user_name_label)
        public_label = QLabel('Опубликовать публично')
        public_label.setFont(QFont('Arial', 10))
        user_info_text_layout.addWidget(public_label)
        user_info_layout.addLayout(user_info_text_layout)
        layout.addLayout(user_info_layout)

        self.star_rating = StarRatingWidget()
        layout.addWidget(self.star_rating)

        self.error_label = QLabel('Пожалуйста, оцените это!')
        self.error_label.setFont(QFont('Arial', 10))
        self.error_label.setStyleSheet("color: red;")
        layout.addWidget(self.error_label)

        self.review_input = QTextEdit()
        self.review_input.setPlaceholderText('Напишите свой отзыв...')
        layout.addWidget(self.review_input)

        buttons_layout = QHBoxLayout()
        
        cancel_button = QPushButton('Отмена')
        cancel_button.setFont(QFont('Arial', 12))
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #F0F0F0;
                color: black;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
        """)
        cancel_button.clicked.connect(self.cancel_review)
        buttons_layout.addWidget(cancel_button, alignment=Qt.AlignRight)

        self.submit_button = QPushButton('Отправлять')
        self.submit_button.setFont(QFont('Arial', 12))
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #00A76F;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #007E5C;
            }
            QPushButton:disabled {
                background-color: #BEBEBE;
                color: white;
            }
        """)
        
        self.submit_button.clicked.connect(self.submit_review)
        self.submit_button.setEnabled(False)
        buttons_layout.addWidget(self.submit_button, alignment=Qt.AlignRight)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def submit_review(self):
        if self.star_rating.rating == 0:
            self.error_label.setVisible(True)
        else:
            self.error_label.setVisible(False)
            self.request_review.emit(self.star_rating.rating, self.review_input.toPlainText())
            QMessageBox.information(self, 'Отзыв отправлен', 'Спасибо за отзыв!', QMessageBox.Ok)

    def cancel_review(self):
        self.star_rating.reset_rating()
        self.review_input.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = ReviewForm(1062, "Linh", '')
    mainWin.show()
    sys.exit(app.exec_())
