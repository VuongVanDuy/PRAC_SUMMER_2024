import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QProgressBar, QListWidget, QListWidgetItem, QPushButton
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt

class ReviewWidget(QWidget):
    def __init__(self, reviews):
        super().__init__()
        self.reviews = reviews
        self.count_vote = len(self.reviews)
        self.average_rating = round(self.get_average_rating(), 1)
        self.rating_rate = self.get_rating_rate()
        self.initUI()

    def get_average_rating(self):
        if len(self.reviews):
            return sum(rating for _, rating, _, _, _ in self.reviews) / len(self.reviews)
        else:
            return 0
    
    def get_rating_rate(self):
        rating_rate = [0, 0, 0, 0, 0]
        if self.reviews:
            for i in range(5):
                for _, rating, _, _, _ in self.reviews:
                    if rating == i + 1:
                        rating_rate[i] += 1
            for i in range(5):
                rating_rate[i] = round(rating_rate[i] / self.count_vote * 100)
        return rating_rate[::-1]
    
    def initUI(self):
        self.setWindowTitle('Review Summary')
        self.setGeometry(100, 100, 400, 600)
        
        self.main_lay_out = QVBoxLayout()
        self.main_lay_out.setContentsMargins(10, 10, 10, 10)  # Ensure no extra margins are added
        self.main_lay_out.setSpacing(10)  # Adjust spacing as needed

        # Write Review Button
        self.write_review_button = QPushButton(' Написать отзыв')
        self.write_review_button.setIcon(QIcon('./pictures/comment.png'))  # Replace with the path to your icon
        self.main_lay_out.addWidget(self.write_review_button, alignment=Qt.AlignCenter)

        # Summary Header
        summary_label = QLabel('СОВОКУПНЫЙ РЕЙТИНГ')
        summary_label.setFont(QFont('Arial', 14))
        self.main_lay_out.addWidget(summary_label, alignment=Qt.AlignCenter)

        # Average Rating
        average_layout = QHBoxLayout()
        self.average_rating_label = QLabel(str(self.average_rating))
        self.average_rating_label.setFont(QFont('Arial', 38))
        average_layout.addWidget(self.average_rating_label, alignment=Qt.AlignCenter)
        
        #stars_label = QLabel('★★★★☆')
        stars_label = QLabel()
        for i in range(5):
            if i < round(self.average_rating):
                stars_label.setText(stars_label.text()[:i] + '★' + stars_label.text()[i+1:])
            else:
                stars_label.setText(stars_label.text()[:i] + '☆' + stars_label.text()[i+1:])
                
        stars_label.setFont(QFont('Arial', 20))
        #average_layout.addWidget(stars_label, alignment=Qt.AlignCenter)
        average_layout.addWidget(stars_label)
        
        self.people_count = QLabel('Количество отзывов: ' + str(self.count_vote))
        self.people_count.setWordWrap(True)
        self.people_count.setFont(QFont('Arial', 10))
        average_layout.addWidget(self.people_count, alignment=Qt.AlignCenter)
        
        self.main_lay_out.addLayout(average_layout)
        
        # Rating Distribution
        distribution_layout = QVBoxLayout()

        for i, value in zip(range(5, 0, -1), self.rating_rate):
            bar_layout = QHBoxLayout()
            star_label = QLabel(f'{i}★')
            bar_layout.addWidget(star_label)
            
            bar = QProgressBar()
            bar.setValue(value)
            bar_layout.addWidget(bar)
            
            distribution_layout.addLayout(bar_layout)
        
        self.main_lay_out.addLayout(distribution_layout)
        
        # Reviews Section Header
        reviews_label = QLabel('ОТЗЫВЫ')
        reviews_label.setFont(QFont('Arial', 14))
        self.main_lay_out.addWidget(reviews_label)
        
        # Reviews List
        self.reviews_list = QListWidget()
        
        self.set_list_reviews()
        
    def set_list_reviews(self):
        self.reviews_list.clear()
        if self.reviews:
            for name, rating, comment, time, link_icon in self.reviews:
                item = QListWidgetItem()
                review_widget = self.create_review_widget(name, rating, comment, time, link_icon)
                item.setSizeHint(review_widget.sizeHint())
                self.reviews_list.addItem(item)
                self.reviews_list.setItemWidget(item, review_widget)
        
        self.main_lay_out.addWidget(self.reviews_list)
        self.setLayout(self.main_lay_out)
        
    def create_review_widget(self, name, rating, comment, time, link_icon):
        widget = QWidget()
        layout = QVBoxLayout()

        # Name and Time Layout
        name_time_layout = QHBoxLayout()
        
        # Dummy Icon
        icon_label = QLabel()
        icon_label.setPixmap(QPixmap(link_icon).scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Replace with the path to your icon
        name_time_layout.addWidget(icon_label)

        name_label = QLabel(name)
        name_time_layout.addWidget(name_label)
        
        time_label = QLabel(f'{time}')
        time_label.setWordWrap(True)
        name_time_layout.addWidget(time_label)
        
        layout.addLayout(name_time_layout)
        
        stars = '★' * rating + '☆' * (5 - rating)
        stars_label = QLabel(stars)
        stars_label.setFont(QFont('Arial'))
        layout.addWidget(stars_label)
        
        if comment:
            comment_label = QLabel(comment)
            comment_label.setWordWrap(True)
            layout.addWidget(comment_label)
        
        widget.setLayout(layout)
        return widget

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # reviews = [
    #         ('Bú Mập Thích Ghẹo', 5, 'quá lâu để chạy', 2, '1 день'),
    #         ('Bùi An', 2, '', 5, '8 дней'),
    #         ('trịnh phươnng', 1, '', 5, '8 дней'),
    #         ('Nguyễn Hữu Tính', 2, '', 5, '11 дней')
    #     ]
    reviews = []
    ex = ReviewWidget(reviews)
    ex.show()
    sys.exit(app.exec_())
