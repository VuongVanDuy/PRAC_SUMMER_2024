import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from .info_route import InfoRoute 

class tab3(QWidget):
    def __init__(self, bus_info):
        super().__init__()
        self.bus_info = bus_info
        self.main_layout = QVBoxLayout(self)
        self.scroll_frame = QFrame()
        self.scroll_layout = QVBoxLayout(self.scroll_frame)
        
        # Create scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        
        self.scroll_content = QWidget()
        self.scroll_content_layout = QVBoxLayout(self.scroll_content)
        
        self.info_widget = InfoRoute(self.bus_info)
        self.scroll_content_layout.addWidget(self.info_widget)
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_layout.addWidget(self.scroll_area)
        self.main_layout.addWidget(self.scroll_frame)
        self.setLayout(self.main_layout)
    
    def update_layout_tab(self, new_bus_info):
        self.bus_info = new_bus_info
        self.scroll_content_layout.removeWidget(self.info_widget)
        self.info_widget = InfoRoute(self.bus_info)
        self.scroll_content_layout.addWidget(self.info_widget)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    stops = ['HN', 'HP', 'TP HCM', 'Hung Yen']
    bus_info = [
            f"Номер маршрута: 1362",
            f"Название маршрута: HN - HP",
            f"Тип маршрута: обратный маршрут",
            f"Стоимость билета: 450k",
            f"Время работы: 6:00 - 22:00",
            f"Остановки: {' ➞ '.join(stops)}"
        ]
    tab_3 = tab3(bus_info)
    tab_3.show()
    sys.exit(app.exec_())
