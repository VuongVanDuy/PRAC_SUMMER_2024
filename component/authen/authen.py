import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QStackedWidget, QMessageBox)
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

class RegisterForm(QWidget):
    check_register = pyqtSignal(str, str)
    
    def __init__(self, stack_widget):
        super().__init__()
        self.stack_widget = stack_widget
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        title = QLabel('Register Account')
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
        self.show_password_button = QPushButton("Show Password")
        self.show_password_button.setFont(QFont('Arial', 10))
        self.show_password_button.setIcon(QIcon('./pictures/eye_show.png'))
        self.show_password_button.setStyleSheet("background-color: none; color: #5bc0de; border: none;")
        self.show_password_button.setIconSize(QSize(25, 25))
        self.show_password_button.setCheckable(True)
        self.show_password_button.toggled.connect(self.toggle_password_visibility)
        layout.addWidget(self.show_password_button, alignment=Qt.AlignCenter)

        # Confirm Password
        confirm_password_label = QLabel('Confirm Password:')
        confirm_password_label.setFont(QFont('Arial', 12))
        confirm_password_label.setStyleSheet("color: #555;")
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText('Confirm your password')
        self.confirm_password_input.setFont(QFont('Arial', 12))
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setStyleSheet("padding: 10px; border: 1px solid #ddd; border-radius: 4px;")
        layout.addWidget(confirm_password_label)
        layout.addWidget(self.confirm_password_input)

        # Register Button
        register_button = QPushButton('Register')
        register_button.setFont(QFont('Arial', 12))
        register_button.setStyleSheet("""
            QPushButton {
                background-color: #5bc0de;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #31b0d5;
            }
        """)
        register_button.clicked.connect(self.handle_register)
        layout.addWidget(register_button, alignment=Qt.AlignCenter)
        
        switch_to_login = QWidget()
        switch_to_login_layout = QHBoxLayout(switch_to_login)
        switch_to_login_label = QLabel("Already have an account?")
        switch_to_login_label.setFont(QFont('Arial', 10))
        switch_to_login_label.setStyleSheet("color: #555;")
        switch_to_login_layout.addWidget(switch_to_login_label)

        switch_to_login_button = QPushButton("Login here")
        font_title = QFont('Arial', 10)
        font_title.setUnderline(True)
        switch_to_login_button.setFont(font_title)
        #register_link.setStyleSheet("color: #007bff;")
        switch_to_login_button.setStyleSheet('background-color: none; color: #007bff; border: none;')
        switch_to_login_button.clicked.connect(self.switch_to_login)
        switch_to_login_layout.addWidget(switch_to_login_button)

        layout.addWidget(switch_to_login, alignment=Qt.AlignCenter)

        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(20)
        self.setLayout(layout)

    def toggle_password_visibility(self, checked):
        if checked:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.confirm_password_input.setEchoMode(QLineEdit.Normal)
            self.show_password_button.setText('Hide Password')
            self.show_password_button.setIcon(QIcon('./pictures/eye_hide.png'))
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.confirm_password_input.setEchoMode(QLineEdit.Password)
            self.show_password_button.setText('Show Password')
            self.show_password_button.setIcon(QIcon('./pictures/eye_show.png'))

    def handle_register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if len(username) < 6:
            QMessageBox.warning(self, 'Registration Failed', 'Username must be at least 6 characters long')
        elif password != confirm_password:
            QMessageBox.warning(self, 'Registration Failed', 'Passwords do not match')
        elif len(password) < 6:
            QMessageBox.warning(self, 'Registration Failed', 'Password must be at least 6 characters long')
        else:
            self.check_register.emit(username, password)
            self.username_input.clear()
            self.password_input.clear()
            self.confirm_password_input.clear()

    def switch_to_login(self):
        self.stack_widget.setCurrentIndex(0)

class AuthWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Account Authentication')
        self.setWindowIcon(QIcon('./pictures/authen.png'))
        self.setFixedSize(470, 600)

        self.stack_widget = QStackedWidget(self)
        self.login_form = LoginForm(self.stack_widget)
        self.register_form = RegisterForm(self.stack_widget)
        
        self.stack_widget.addWidget(self.login_form)
        self.stack_widget.addWidget(self.register_form)

        layout = QVBoxLayout()
        layout.addWidget(self.stack_widget)
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = AuthWidget()
    mainWin.show()
    sys.exit(app.exec_())
