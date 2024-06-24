import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QStackedWidget
from PyQt5.QtGui import QIcon
from .login import LoginForm
from .register import RegisterForm

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
