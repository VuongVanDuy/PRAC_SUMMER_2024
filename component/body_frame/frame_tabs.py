import sys
from PyQt5.QtWidgets import (QFrame, QLabel, QHBoxLayout, QPushButton, QApplication, QSizePolicy, 
                             QTabWidget, QWidget, QLineEdit, QScrollArea, QVBoxLayout)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap

class frame_tabs(QFrame):
    clickedRoute = pyqtSignal(int)
    
    def __init__(self, all_routes=None):
        super().__init__()
        self.all_routes = all_routes
        # frame tabs
        self.setFixedWidth(470)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        
        # frame button hide tabs
        self.frame_hide_tab = QFrame()
        
        # frame view map
        self.frame_view = QFrame()
        self.frame_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.create_tabs()

    def create_tabs(self):
        self.main_tab_widget = QTabWidget()
        # Tab 1
        self.tab1 = QWidget()
        self.tab1_layout = QHBoxLayout(self.tab1)

        # Create a frame to hold the scroll area and hide button
        self.scroll_frame = QFrame()
        self.scroll_layout = QVBoxLayout(self.scroll_frame)
        
        # Create scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        
        self.scroll_content = QWidget()
        self.scroll_content_layout = QVBoxLayout(self.scroll_content)
        self.set_scroll_content_layout()
        self.scroll_area.setWidget(self.scroll_content)
        
        # Add scroll area to the scroll frame layout
        self.scroll_layout.addWidget(self.scroll_area)

        # Add scroll frame to tab layout
        self.tab1_layout.addWidget(self.scroll_frame)
        
        self.tab1.setLayout(self.tab1_layout)
        self.main_tab_widget.addTab(self.tab1, 'Поиск')

        # Tab 2
        self.tab2 = QWidget()
        self.tab2_layout = QVBoxLayout()
        self.tab2_layout.addWidget(QLabel('Content for TÌM ĐƯỜNG'))
        self.tab2.setLayout(self.tab2_layout)
        self.main_tab_widget.addTab(self.tab2, 'Поиск маршрута')
        
        self.frame_layout = QVBoxLayout(self)
        self.frame_layout.addWidget(self.main_tab_widget)
        self.setLayout(self.frame_layout)
        self.adjustSize()
    
    def set_scroll_content_layout(self):
        if self.scroll_content_layout is not None:
            while self.scroll_content_layout.count():
                child = self.scroll_content_layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
        
        # Add search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Поиск автобусных маршрутов")
        self.scroll_content_layout.addWidget(self.search_bar)

        # Add bus info widgets
        self.buttons = []
        if self.all_routes:
            for route in self.all_routes:
                button = self.create_bus_info(route[0], route[1], route[2], route[3])
                self.buttons.append(button)
                self.scroll_content_layout.addWidget(button)
                
        for i in range(len(self.buttons)):
            self.buttons[i].clicked.connect(self.on_clicked_button)
    
    def reset_list_btns(self, new_list_routes):
        self.all_routes = new_list_routes
        self.set_scroll_content_layout()
            
    def create_bus_info(self, route, description, time, price):
        button = QPushButton()
        button.setFixedHeight(120)
        h_layout = QHBoxLayout(button)
        label_icon = QLabel()
        label_icon.setPixmap(QPixmap('./pictures/bus.png').scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        label_icon.setFixedSize(24, 24)
        h_layout.addWidget(label_icon, 0, Qt.AlignTop)
        
        buttonLayout = QVBoxLayout()

        route_label = QLabel(f"№ маршрута автобуса {route}")
        route_label.setStyleSheet("font-weight: bold; font-size: 16px; color: green")

        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        time_label = QLabel(f"Время: {time}")
        price_label = QLabel(f"Стоимость билета: {price}")

        buttonLayout.addWidget(route_label)
        buttonLayout.addWidget(desc_label)
        buttonLayout.addWidget(time_label)
        buttonLayout.addWidget(price_label)
        
        h_layout.addLayout(buttonLayout)
        button.setLayout(h_layout)
        
        return button
    
    def on_clicked_button(self):
        sender = self.sender()
        for i in range(len(self.buttons)):
            if sender == self.buttons[i]:
                self.clickedRoute.emit(self.all_routes[i][0])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    h_lay = frame_tabs()
    h_lay.show()
    sys.exit(app.exec_())