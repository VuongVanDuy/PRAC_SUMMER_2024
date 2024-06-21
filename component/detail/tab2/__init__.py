import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from .button_stops import CustomWidget 

class tab2(QWidget):
    def __init__(self, stops):
        super().__init__()
        self.stops = stops
        self.main_layout = QVBoxLayout(self)
        self.scroll_frame = QFrame()
        self.scroll_layout = QVBoxLayout(self.scroll_frame)
        
        # Create scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        
        self.scroll_content = QWidget()
        self.scroll_content_layout = QVBoxLayout(self.scroll_content)
        
        self.custom_widget = CustomWidget(self.stops)
        self.scroll_content_layout.addWidget(self.custom_widget)
        self.scroll_area.setWidget(self.scroll_content)
        
        # Add scroll area to the scroll frame layout
        self.scroll_layout.addWidget(self.scroll_area)

        # Add scroll frame to tab layout
        self.main_layout.addWidget(self.scroll_frame)
        
        self.setLayout(self.main_layout)
    
    def update_layout_tab(self, new_stops):
        self.stops = new_stops
        self.scroll_content_layout.removeWidget(self.custom_widget)
        self.custom_widget = CustomWidget(self.stops)
        self.scroll_content_layout.addWidget(self.custom_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    stops = ['HN', 'HP', 'TP HCM', 'Hung Yen']
    tab_2 = tab2(stops)
    tab_2.show()
    sys.exit(app.exec_())
    