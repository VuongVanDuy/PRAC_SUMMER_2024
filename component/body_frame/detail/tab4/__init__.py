import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from .evaluation import ReviewWidget

class tab4(QWidget):
    def __init__(self, reviews):
        super().__init__()
        self.reviews = reviews
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.scroll_frame = QFrame()
        self.scroll_layout = QVBoxLayout(self.scroll_frame)
        
        # Create scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        
        self.scroll_content = QWidget()
        self.scroll_content_layout = QVBoxLayout(self.scroll_content)
        self.scroll_content_layout.setContentsMargins(0, 0, 0, 0)
            
        self.reviewWidget = ReviewWidget(self.reviews)
        self.scroll_content_layout.addWidget(self.reviewWidget)
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_layout.addWidget(self.scroll_area)
        self.main_layout.addWidget(self.scroll_frame)
        self.setLayout(self.main_layout)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    reviews = [
            ('Bú Mập Thích Ghẹo', 5, 'quá lâu để chạy', 2, '1 день'),
            ('Bùi An', 2, '', 5, '8 дней'),
            ('trịnh phươnng', 1, '', 5, '8 дней'),
            ('Nguyễn Hữu Tính', 2, '', 5, '11 дней')
        ]
    reviews = []
    ex = tab4(reviews)
    ex.show()
    sys.exit(app.exec_())