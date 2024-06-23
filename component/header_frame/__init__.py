import sys
import hashlib
import os
from PyQt5.QtWidgets import QFrame, QLabel, QHBoxLayout, QPushButton, QApplication, QMessageBox, QFileDialog
from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from ..authen import AuthWidget
from ..data_app import *

class header_frame(QFrame):
    status_logined = pyqtSignal(bool, str)
    
    def __init__(self):
        super().__init__()
        self.info_update = None
        self.info_login = {
            'status': False,
            'username': None,
            'password': None
        }
        self.data_users = DataUsers()
        self.initUI()
        self.login_button.clicked.connect(self.showLogin)
    
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
        self.header_frame_layout.addWidget(self.login_button)
        
        self.update_btn = QPushButton()
        self.update_btn.setIcon(QIcon('./pictures/update.png'))
        self.update_btn.setIconSize(QSize(40, 40))
        self.update_btn.setStyleSheet("border: none;")
        if self.info_update:
            self.update_btn.setVisible(self.info_update['status'])
        self.header_frame_layout.addWidget(self.update_btn)
        
        self.setLayout(self.header_frame_layout)
    
    def update_static_data(self):
        pass
    def showLogin(self):
        self.auth_widget = AuthWidget()
        self.auth_widget.show()
        self.auth_widget.login_form.check_login.connect(self.acceptLogin)
        self.auth_widget.register_form.check_register.connect(self.added_new_user)
    
    def sha256_hash(self, data):
        data_bytes = data.encode('utf-8')
        sha256 = hashlib.sha256()
        sha256.update(data_bytes)
    
        return sha256.hexdigest()

    def acceptLogin(self, username, password):
        hash_password_true = self.data_users.get_user_password(username)
        hash_password_check = self.sha256_hash(password)
        
        if hash_password_true is None:
            QMessageBox.warning(self.auth_widget, 'Login Failed', 'User does not exist!')
            self.auth_widget.login_form.username_input.clear()
            self.auth_widget.login_form.password_input.clear()
            return
        elif hash_password_true != hash_password_check:
            QMessageBox.warning(self.auth_widget, 'Login Failed', 'Password is incorrect!')
            self.auth_widget.login_form.password_input.clear()
            return
        else:
            QMessageBox.information(self.auth_widget, 'Login Successful', 'Login successful!')
            self.info_login['status'] = True
            self.info_login['username'] = username
            self.info_login['password'] = password
            self.status_logined.emit(True, self.info_login['username'])
            self.login_button.setText(' Выйти')
            self.icon_btn = QPushButton()
            link_icon = self.data_users.get_user_link_icon(username)
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
            self.data_users.update_link_icon(self.info_login['username'], relative_path)
            QMessageBox.information(self, 'Change Icon Successful', 'Change icon successful!')
    
    def logout(self):
        confirm_logout = self.ask_user_confirm_active("Вы уверены, что хотите выйти?")
        if confirm_logout:
            self.info_login['status'] = False
            self.info_login['username'] = None
            self.info_login['password'] = None
            self.status_logined.emit(False, self.info_login['username'])
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