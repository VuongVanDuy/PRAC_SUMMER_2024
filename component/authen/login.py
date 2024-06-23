import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSize, pyqtSignal

class LoginForm(QWidget):
    check_login = pyqtSignal(str, str)
    
    def __init__(self, stack_widget):
        super().__init__()
        self.stack_widget = stack_widget
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        title = QLabel('Account Authentication')
        title.setFont(QFont('Arial', 16))
        title.setStyleSheet("color: #333;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Username
        username_label = QLabel('Username:')
        username_label.setFont(QFont('Arial', 12))
        username_label.setStyleSheet("color: #555;")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter your username')
        self.username_input.setFont(QFont('Arial', 12))
        self.username_input.setStyleSheet("padding: 10px; border: 1px solid #ddd; border-radius: 4px;")
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)

        # Password
        password_label = QLabel('Password:')
        password_label.setFont(QFont('Arial', 12))
        password_label.setStyleSheet("color: #555;")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Enter your password')
        self.password_input.setFont(QFont('Arial', 12))
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("padding: 10px; border: 1px solid #ddd; border-radius: 4px;")
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)

        # Show Password Button
        self.show_password_button = QPushButton('Show Password')
        self.show_password_button.setFont(QFont('Arial', 10))
        self.show_password_button.setIcon(QIcon('./pictures/eye_show.png'))
        self.show_password_button.setIconSize(QSize(25, 25))
        self.show_password_button.setStyleSheet("background-color: none; color: #5bc0de; border: none;")
        self.show_password_button.setCheckable(True)
        self.show_password_button.toggled.connect(self.toggle_password_visibility)
        layout.addWidget(self.show_password_button, alignment=Qt.AlignCenter)

        # Login Button
        login_button = QPushButton('Login')
        login_button.setFont(QFont('Arial', 12))
        login_button.setStyleSheet("""
            QPushButton {
                background-color: #5cb85c;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #4cae4c;
            }
        """)
        login_button.clicked.connect(self.handle_login)
        layout.addWidget(login_button, alignment=Qt.AlignCenter)

         # Register link
        switch_to_register = QWidget()
        switch_to_register_layout = QHBoxLayout(switch_to_register)
        switch_to_register_label = QLabel("No account?")
        switch_to_register_label.setFont(QFont('Arial', 10))
        switch_to_register_label.setStyleSheet("color: #555;")
        switch_to_register_layout.addWidget(switch_to_register_label)

        switch_to_register_button = QPushButton("Register here")
        font_title = QFont('Arial', 10)
        font_title.setUnderline(True)
        switch_to_register_button.setFont(font_title)
        #register_link.setStyleSheet("color: #007bff;")
        switch_to_register_button.setStyleSheet('background-color: none; color: #007bff; border: none;')
        switch_to_register_button.clicked.connect(self.switch_to_register)
        switch_to_register_layout.addWidget(switch_to_register_button)

        layout.addWidget(switch_to_register, alignment=Qt.AlignCenter)
        

        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(20)
        self.setLayout(layout)

    def toggle_password_visibility(self, checked):
        if checked:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.show_password_button.setText('Hide Password')
            self.show_password_button.setIcon(QIcon('./pictures/eye_hide.png'))
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.show_password_button.setText('Show Password')
            self.show_password_button.setIcon(QIcon('./pictures/eye_show.png'))

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        self.check_login.emit(username, password)
        
    def switch_to_register(self):
        self.stack_widget.setCurrentIndex(1)