import sys
from PyQt5.QtWidgets import QFrame, QPushButton, QApplication, QVBoxLayout

class frame_hide(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedSize(50, 300)
        hide_tab_layout = QVBoxLayout(self)
        self.hide_button = QPushButton("◀")
        self.hide_button.setFixedSize(30, 70)
        self.hide_button.setStyleSheet("background-color: green; color: white; font-size: 20px;")
        hide_tab_layout.addWidget(self.hide_button)
        self.setLayout(hide_tab_layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    h_lay = frame_hide()
    h_lay.show()
    sys.exit(app.exec_())