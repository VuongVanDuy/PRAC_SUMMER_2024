import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore  import pyqtSignal
from .tab2 import tab2
from .tab3 import tab3
from .tab4 import tab4
from .tab4.write_review import ReviewForm

class DetailRoute(QWidget):
    changedAddr = pyqtSignal(str)
    changedDirection = pyqtSignal(int)
    
    def __init__(self, info_route, status_login, data_users):
        super().__init__()
        self.info_route = info_route
        self.status_login = status_login['status']
        self.username = status_login['username']
        self.data_users = data_users
        
        self.routeId = self.info_route.routeId
        self.direction = self.info_route.direction
        self.stops = list(self.info_route.get_stops_of_route().keys())
        
        self.setFixedWidth(470)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        layout = QVBoxLayout(self)
        self.frame_detail = QFrame()
        self.create_frame()
        layout.addWidget(self.frame_detail)
        self.setLayout(layout)  

    
    def update_status_login(self, status_login, username):
        self.status_login = status_login
        self.username = username
        
    def create_frame(self):
        widget = QWidget()
        layout_widget = QHBoxLayout(widget)
        # Left panel for route information
        
        left_panel = QFrame()
        left_panel.setFrameShape(QFrame.StyledPanel)
        left_panel_layout = QVBoxLayout(left_panel)

        # Route title and back button
        header_layout = QHBoxLayout()
        self.back_button = QPushButton("←")
        self.back_button.setFixedSize(30, 30)
        route_title = QLabel(f"Маршрут № {self.routeId}")
        route_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        header_layout.addWidget(self.back_button)
        header_layout.addWidget(route_title)
        left_panel_layout.addLayout(header_layout)

        # Navigation buttons
        nav_buttons_layout = QHBoxLayout()
        self.btn_route_go = QPushButton("Посмотреть маршрут")
        self.btn_route_return = QPushButton("Посмотреть обратный маршрут")
        nav_buttons_layout.addWidget(self.btn_route_go)
        nav_buttons_layout.addWidget(self.btn_route_return)
        self.btn_route_go.setEnabled(self.direction != 0)
        self.btn_route_return.setEnabled(self.direction != 1)
        self.btn_route_go.clicked.connect(lambda: self.changedDirection.emit(0))
        self.btn_route_return.clicked.connect(lambda: self.changedDirection.emit(1))
        left_panel_layout.addLayout(nav_buttons_layout)

        # Tab with route details
        self.tab_widget = QTabWidget()
        self.create_tab1()
        self.create_tab2()
        self.create_tab3()
        self.create_tab4()
        self.tab_widget.setCurrentIndex(1)
        
        left_panel_layout.addWidget(self.tab_widget)
        layout_widget.addWidget(left_panel)
       # layout_widget.addWidget(tab_widget)
        
        main_layout = QVBoxLayout(self.frame_detail)
        main_layout.addWidget(widget)
        self.frame_detail.setLayout(main_layout)
        
    
    def create_tab1(self):
        # Tab 1
        self.tab1 = QWidget()
        self.tab_widget.addTab(self.tab1, "График")
        
    def create_tab2(self):
        self.tab2 = tab2(self.stops)
        for button in self.tab2.custom_widget.buttons:
            button.clicked.connect(self.on_button_click)
        self.tab_widget.addTab(self.tab2, "Остановка")
    
    def create_tab3(self):
        type_route = "исходящий маршрут" if self.direction == 0 else "обратный маршрут"
        bus_info = [
            f"Номер маршрута: {self.routeId}",
            f"Название маршрута: {self.info_route.name_route}",
            f"Тип маршрута: {type_route}",
            f"Стоимость билета: {self.info_route.ticket_price}",
            f"Время работы: {self.info_route.time}",
            f"Остановки: {' ➞ '.join(self.stops)}"
        ]
        self.tab3 = tab3(bus_info)
        self.tab_widget.addTab(self.tab3, "Информация")
    
    def create_tab4(self):
        result = self.data_users.get_reviews_of_route(self.routeId) #fetch_all_reviews_of_route
        reviews = []
        for review in result:
            reviews.append([review['username'], review['star_vote'], review['comment'], review['time'], review['link_icon']])
            
        self.tab4 = tab4(reviews)
        self.tab_widget.addTab(self.tab4, "Оценка")
        self.tab4.reviewWidget.write_review_button.clicked.connect(self.write_review)
        
    def write_review(self):
        if self.status_login:
            link_icon = self.data_users.get_user_link_icon(self.username)
            self.review_form = ReviewForm(self.routeId, self.username, link_icon)
            self.review_form.show()
            self.review_form.request_review.connect(self.add_review)
        else:
            QMessageBox.warning(self, 'Оценка', 'Вы должны войти в систему, чтобы оценить маршрут')

    def add_review(self, rating, comment):
        id_user = self.data_users.get_id_user(self.username)
        self.data_users.add_review(id_user, self.routeId, rating, comment)
        
        result = self.data_users.get_reviews_of_route(self.routeId) #fetch_all_reviews_of_route
        reviews = []
        for review in result:
            reviews.append([review['username'], review['star_vote'], review['comment'], review['time'], review['link_icon']])
            
        self.tab4.reviewWidget.reviews = reviews
        self.tab4.reviewWidget.set_list_reviews()
        self.review_form.close()
        
    def toggle_visibility(self):
        if self.scroll_frame.isVisible():
            self.scroll_frame.setVisible(False)
            self.hide_button.setText('▶')
        else:
            self.scroll_frame.setVisible(True)
            self.hide_button.setText('◀')
    
    def on_button_click(self):
        sender = self.sender()
        for i in range(len(self.tab2.custom_widget.buttons)):
            if sender == self.tab2.custom_widget.buttons[i]:
                self.tab2.custom_widget.buttons[i].setStyleSheet(self.tab2.custom_widget.get_button_style(True))
                self.changedAddr.emit(self.tab2.custom_widget.nameAddr[i].text())
            else:
                self.tab2.custom_widget.buttons[i].setStyleSheet(self.tab2.custom_widget.get_button_style(False))
                
    def update_direction(self, route_with_new_direction):
        self.info_route = route_with_new_direction
        self.direction = self.info_route.direction
        self.stops = list(self.info_route.get_stops_of_route().keys())
        
        # update layout tab 2
        self.tab2.update_layout_tab(self.stops)
        for button in self.tab2.custom_widget.buttons:
            button.clicked.connect(self.on_button_click)

        # update layout tab 3
        type_route = "исходящий маршрут" if self.direction == 0 else "обратный маршрут"
        new_bus_info = [
            f"Номер маршрута: {self.routeId}",
            f"Название маршрута: {self.info_route.name_route}",
            f"Тип маршрута: {type_route}",
            f"Стоимость билета: {self.info_route.ticket_price}",
            f"Время работы: {self.info_route.time}",
            f"Остановки: {' ➞ '.join(self.stops)}"
        ]
        self.tab3.update_layout_tab(new_bus_info)
        
        self.btn_route_go.setEnabled(self.direction != 0)
        self.btn_route_return.setEnabled(self.direction != 1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = DetailRoute(5)
    main_window.show()
    sys.exit(app.exec_())
