import sys, os
from PyQt5.QtWidgets import QFrame, QLabel, QHBoxLayout, QPushButton, QApplication, QMessageBox, QFileDialog
from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from ..authen import AuthWidget
from ..data_app import *
from .UI_update import updateUI

class header_frame(QFrame):
    status_logined = pyqtSignal(dict)
    finished_update = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        self.info_login = {
            'status': False,
            'username': None,
            'token': None
        }
        self.data_users = DataUsers()
        self.data_update = data_update()
        self.initUI()
    
    def initUI(self):
        # Set the frame for the green background
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("background-color: #00A76F; padding: 10px;")
        self.header_frame_layout = QHBoxLayout()
        self.header_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.setFixedHeight(60)
        
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
        self.login_button.clicked.connect(self.showLogin)
        self.header_frame_layout.addWidget(self.login_button)
        
        self.update_btn = QPushButton()
        self.update_btn.setFixedSize(40, 40)
        self.update_btn.setIcon(QIcon('./pictures/update.png'))
        self.update_btn.setIconSize(QSize(40, 40))
        self.update_btn.setStyleSheet("""
            QPushButton {
                border: none;
                color: white;
                background-color: #00A76F;
                padding: 15px;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #007E5C;
            }
        """)
        self.header_frame_layout.addWidget(self.update_btn)
        self.info_update = self.data_update.get_info_update()
        if self.info_update:
            self.update_btn.setVisible(not self.info_update['status'])
            self.update_btn.clicked.connect(self.update_data_from_api)
        
        self.setLayout(self.header_frame_layout)
    
    def update_data_from_api(self):
        self.ui_update = updateUI()
        self.ui_update.show()
        self.ui_update.finishedUp.connect(self.on_finished_update)
    
    def on_finished_update(self, status):
        self.update_btn.setVisible(not status)
        all_routes = get_info_general_routes()
        self.finished_update.emit(all_routes)
                       
    def showLogin(self):
        self.auth_widget = AuthWidget()
        self.auth_widget.show()
        self.auth_widget.login_form.check_login.connect(self.acceptLogin)
        self.auth_widget.register_form.check_register.connect(self.added_new_user)

    def acceptLogin(self, username, password):
        token, status = self.data_users.check_login_and_get_token(username, password)
        if status:
            QMessageBox.information(self.auth_widget, 'Login Successful', 'Login successful!')
            self.info_login['status'] = True
            self.info_login['username'] = username
            self.info_login['token'] = token
            self.status_logined.emit(self.info_login)
            self.login_button.setText(' Выйти')
            self.icon_btn = QPushButton()
            link_icon = self.data_users.get_user_link_icon(username, token)
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
        else:
            QMessageBox.warning(self.auth_widget, 'Login Failed', 'Username or password is incorrect!')
            self.auth_widget.login_form.username_input.clear()
            self.auth_widget.login_form.password_input.clear()
            return
    
    def added_new_user(self, username, password, link_icon='./pictures/avatar_default.png'):
        if self.data_users.add_user(username, password, link_icon):
            QMessageBox.information(self.auth_widget, 'Registration Successful', f'User {username} registered successfully!')
        else:
            QMessageBox.warning(self.auth_widget, 'Registration Failed', f'User {username} already exists!')
            
    def changeIconUser(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose New Icon", "", "Images (*.png *.xpm *.jpg);All Files (*)", options=options)
        if file_path:
            confirm = self.ask_user_confirm_active("Вы уверены, что хотите изменить иконку пользователя?")
        
        if file_path and confirm:
            self.icon_btn.setIcon(QIcon(file_path))
            dir_root_file = os.path.dirname(file_path)
            dir_root_dir = os.path.dirname(dir_root_file)
            relative_path = './' + os.path.relpath(file_path, dir_root_dir).replace('\\', '/')
            self.data_users.update_link_icon(self.info_login['username'], relative_path, token=self.info_login['token'])
            QMessageBox.information(self, 'Change Icon Successful', 'Change icon successful!')
    
    def logout(self):
        confirm_logout = self.ask_user_confirm_active("Вы уверены, что хотите выйти?")
        if confirm_logout:
            self.info_login['status'] = False
            self.info_login['username'] = None
            self.info_login['token'] = None
            self.status_logined.emit(self.info_login)
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
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    h_lay = header_frame()
    h_lay.show()
    sys.exit(app.exec_())