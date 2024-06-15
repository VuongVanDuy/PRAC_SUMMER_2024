import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QUrl, QSize, Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtWebEngineWidgets import QWebEngineView
from init_data import init_data_route, get_info_general_routes
from component.detail.detail import DetailRoute
from component.authen.authen import AuthWidget
from component.data_app.data_app import DatabaseManager
import os

class BusMapApp(QMainWindow):
    status_logined = pyqtSignal(bool, str)
    
    def __init__(self):
        super().__init__()

        self.status_login = False
        self.username = None
        self.password = None
        self.data_app = DatabaseManager("./data/data.db")
        self.setWindowTitle('BusMap')
        self.setGeometry(100, 100, 1200, 700)
        self.setWindowIcon(QIcon('./pictures/bus_app.png'))
        self.setIconSize(QSize(30, 30))
        # create main widget of app
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)
        
        self.create_header_layout()
        self.create_body_layout()
        self.main_layout.addLayout(self.header_layout)
        self.main_layout.addLayout(self.body_layout)
        
    def create_header_layout(self):
        # create header layout
        self.header_layout = QVBoxLayout()
        # Set the frame for the green background
        self.header_frame = QFrame()
        self.header_frame.setContentsMargins(0, 0, 0, 0)
        self.header_frame.setStyleSheet("background-color: #00A76F; padding: 10px;")
        self.header_frame_layout = QHBoxLayout()
        self.header_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.header_frame.setFixedHeight(60)
        
        icon_label = QLabel()
        icon_label.setFixedSize(150, 60) 
        icon_pixmap = QPixmap('./pictures/Logo_BusMap.png').scaled(150, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_label.setPixmap(icon_pixmap)
        icon_label.setContentsMargins(0, 0, 0, 10)
        self.header_frame_layout.addWidget(icon_label, Qt.AlignmentFlag.AlignTop)
        
        # Spacer to push the login button to the right
        self.header_frame_layout.addStretch()
        
        # Login Button
        self.login_button = QPushButton('Авторизоваться')
        self.login_button.setStyleSheet("""
            QPushButton {
                border: 2px solid white;
                color: white;
                background-color: #00A76F;
                padding: 5px 15px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #007E5C;
            }
        """)
        self.header_frame_layout.addWidget(self.login_button)
        self.header_frame.setLayout(self.header_frame_layout)
        self.header_layout.addWidget(self.header_frame)
        self.login_button.clicked.connect(self.showLogin)
        
    def create_body_layout(self):
        # create body layout
        self.body_layout = QHBoxLayout()
        self.buttons = []
        
        # frame tabs
        self.frame_tabs = QFrame()
        self.frame_tabs.setFixedWidth(470)
        self.frame_tabs.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.body_layout.addWidget(self.frame_tabs)
        
        # frame button hide tabs
        self.frame_hide_tab = QFrame()
        self.body_layout.addWidget(self.frame_hide_tab)
        
        # frame view map
        self.frame_view = QFrame()
        self.frame_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.body_layout.addWidget(self.frame_view)
        
        self.create_tabs()
        self.createBtnHideTab()
        self.createMapRoute()
        
    def create_tabs(self):
        main_tab_widget = QTabWidget()
        # Tab 1
        tab1 = QWidget()
        tab1_layout = QHBoxLayout()

        # Create a frame to hold the scroll area and hide button
        self.scroll_frame = QFrame()
        self.scroll_layout = QVBoxLayout(self.scroll_frame)
        
        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        scroll_content = QWidget()
        scroll_content_layout = QVBoxLayout(scroll_content)

        # Add search bar
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Поиск автобусных маршрутов")
        scroll_content_layout.addWidget(search_bar)

        # Add bus info widgets
        self.all_routes = get_info_general_routes()
        for route in self.all_routes:
            scroll_content_layout.addWidget(self.create_bus_info(route[0], route[1], route[2], route[3]))
        
        scroll_area.setWidget(scroll_content)
        
        # Add scroll area to the scroll frame layout
        self.scroll_layout.addWidget(scroll_area)

        # Add scroll frame to tab layout
        tab1_layout.addWidget(self.scroll_frame)
        
        tab1.setLayout(tab1_layout)
        main_tab_widget.addTab(tab1, 'Поиск')

        # Tab 2
        tab2 = QWidget()
        tab2_layout = QVBoxLayout()
        tab2_layout.addWidget(QLabel('Content for TÌM ĐƯỜNG'))
        tab2.setLayout(tab2_layout)
        main_tab_widget.addTab(tab2, 'Поиск маршрута')
        
        frame_layout = QVBoxLayout(self.frame_tabs)
        frame_layout.addWidget(main_tab_widget)
        self.frame_tabs.setLayout(frame_layout)
        self.frame_tabs.adjustSize()

    def showLogin(self):
        self.auth_widget = AuthWidget()
        self.auth_widget.show()
        self.auth_widget.login_form.check_login.connect(self.acceptLogin)
        self.auth_widget.register_form.check_register.connect(self.added_new_user)
    
    def acceptLogin(self, username, password):
        password_true = self.data_app.get_password(username)
        if password_true is None:
            QMessageBox.warning(self.auth_widget, 'Login Failed', 'User does not exist!')
            self.auth_widget.login_form.username_input.clear()
            self.auth_widget.login_form.password_input.clear()
            return
        elif password_true != password:
            QMessageBox.warning(self.auth_widget, 'Login Failed', 'Password is incorrect!')
            self.auth_widget.login_form.password_input.clear()
            return
        else:
            QMessageBox.information(self.auth_widget, 'Login Successful', 'Login successful!')
            self.status_login = True
            self.username = username
            self.password = password
            self.status_logined.emit(True, self.username)
            self.login_button.setText(' Выйти')
            self.icon_btn = QPushButton()
            link_icon = self.data_app.get_link_icon(username)
            self.icon_btn.setIcon(QIcon(link_icon))
            self.icon_btn.setFixedSize(30, 30)  
            self.icon_btn.setIconSize(QSize(30, 30))
            self.icon_btn.setStyleSheet("""
                QPushButton {
                    background-color: #00A76F;
                    border: 2px solid #00A76F;
                    border-radius: 15px;
                }
                QPushButton:pressed {
                    background-color: #00A76F;
                }
                QPushButton:hover {
                    background-color: #00A76F;
                }
            """)
            self.icon_btn.clicked.connect(self.changeIconUser)
            self.header_frame_layout.addWidget(self.icon_btn)
            self.auth_widget.close()
            del self.auth_widget
            self.login_button.clicked.connect(self.logout)
            self.login_button.clicked.disconnect(self.showLogin)
    
    def added_new_user(self, username, password, link_icon='./pictures/avatar_default.png'):
        if self.data_app.insert_user(username, password, link_icon):
            QMessageBox.information(self.auth_widget, 'Registration Successful', f'User {username} registered successfully!')
        else:
            QMessageBox.warning(self.auth_widget, 'Registration Failed', f'User {username} already exists!')
            
    def changeIconUser(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose New Icon", "", "Images (*.png *.xpm *.jpg);;All Files (*)", options=options)
        confirm = self.ask_user_confirm_active("Вы уверены, что хотите изменить иконку пользователя?")
        
        if file_path and confirm:
            self.icon_btn.setIcon(QIcon(file_path))
            dir_root_file = os.path.dirname(file_path)
            dir_root_dir = os.path.dirname(dir_root_file)
            relative_path = './' + os.path.relpath(file_path, dir_root_dir).replace('\\', '/')
            self.data_app.update_link_icon(self.username, relative_path)
            QMessageBox.information(self, 'Change Icon Successful', 'Change icon successful!')
    
    def logout(self):
        confirm_logout = self.ask_user_confirm_active("Вы уверены, что хотите выйти?")
        if confirm_logout:
            self.status_login = False
            self.username = None
            self.password = None
            self.status_logined.emit(False, self.username)
            self.login_button.setText('Авторизоваться')
            self.header_frame_layout.removeWidget(self.icon_btn)
            del self.icon_btn
            self.login_button.clicked.disconnect(self.logout)
            self.login_button.clicked.connect(self.showLogin)
            QMessageBox.information(self, 'Logout Successful', 'Logout successful!')
    
    def ask_user_confirm_active(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle("Подтверждение")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        return_value = msg_box.exec()
        if return_value == QMessageBox.Yes:
            return True
        else:
            return False
        
    def createBtnHideTab(self):
        hide_tab_layout = QVBoxLayout(self.frame_hide_tab)
        self.hide_button = QPushButton("◀")
        self.hide_button.setFixedSize(30, 70)
        self.hide_button.setStyleSheet("background-color: green; color: white; font-size: 20px;")
        self.hide_button.clicked.connect(self.toggle_visibility_tabs)
        hide_tab_layout.addWidget(self.hide_button)
        self.frame_hide_tab.setLayout(hide_tab_layout)
    
    def createMapRoute(self):
        view_map_layout = QVBoxLayout(self.frame_view)
        
        self.map = QWebEngineView()
        html_file = './map/map_spb.html'
        url = QUrl.fromLocalFile(os.path.realpath(html_file))
        self.map.load(url)
        
        view_map_layout.addWidget(self.map)
        self.frame_view.setLayout(view_map_layout)
    
    def showRoute(self, html_file):
        url = QUrl.fromLocalFile(os.path.realpath(html_file))
        self.map.setUrl(url)
        
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
        time_label = QLabel(f"Время: {time}")
        price_label = QLabel(f"Стоимость билета: {price}")

        buttonLayout.addWidget(route_label)
        buttonLayout.addWidget(desc_label)
        buttonLayout.addWidget(time_label)
        buttonLayout.addWidget(price_label)
        
        h_layout.addLayout(buttonLayout)
        button.setLayout(h_layout)
        
        button.clicked.connect(lambda: self.showDetailRoute(route))
        return button

    def showDetailRoute(self, route):
        try:
            self.direction = 0
            self.cur_data_route = init_data_route(route, self.direction)
        except Exception as e:
            print(e)
        
        self.frame_tabs.setVisible(False)
        self.frame_detail = DetailRoute(self.cur_data_route, self.status_login, self.username, self.data_app)
        self.body_layout.insertWidget(0, self.frame_detail)
        #self.main_widget.setLayout(self.main_layout)   
        self.showRoute(f"./map/direction_{self.direction}/{route}" + ".html")   
        self.frame_detail.back_button.clicked.connect(self.backMainTabs)
        self.hide_button.clicked.disconnect(self.toggle_visibility_tabs)
        self.hide_button.clicked.connect(self.toggle_visibility_details)
        self.frame_detail.changedAddr.connect(self.update_location)
        self.frame_detail.changedDirection.connect(self.change_direction)
        self.status_logined.connect(self.frame_detail.update_status_login)
    
    def change_direction(self, direction):
        self.direction = direction
        self.cur_data_route = init_data_route(self.cur_data_route.routeId, self.direction)
        self.showRoute(f"./map/direction_{self.direction}/{self.cur_data_route.routeId}.html")
        self.frame_detail.update_direction(self.cur_data_route)
    
    def update_location(self, newAddr):
        stops_of_route = self.cur_data_route.get_stops_of_route()
        lat = stops_of_route[newAddr][0]
        lon = stops_of_route[newAddr][1]
        # Call JavaScript function to update marker location
        self.map.page().runJavaScript(f"updateMarker({lat}, {lon});")
    
    def backMainTabs(self):
        self.showRoute('./map/map_spb.html')
        self.frame_detail.setVisible(False)
        self.frame_tabs.setVisible(True)
        self.hide_button.clicked.disconnect(self.toggle_visibility_details)
        self.hide_button.clicked.connect(self.toggle_visibility_tabs)
        
    def toggle_visibility_tabs(self):
        if self.frame_tabs.isVisible():
            self.frame_tabs.setVisible(False)
            self.hide_button.setText('▶')
        else:
            self.frame_tabs.setVisible(True)
            self.hide_button.setText('◀')
    
    def toggle_visibility_details(self):
        if self.frame_detail.isVisible():
            self.frame_detail.setVisible(False)
            self.hide_button.setText('▶')
        else:
            self.frame_detail.setVisible(True)
            self.hide_button.setText('◀')
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = BusMapApp()
    main_window.show()
    sys.exit(app.exec_())
