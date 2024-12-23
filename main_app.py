import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from component.header_frame import header_frame
from component.body_frame import body_frame

class BusMapApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('BusMap')
        self.setGeometry(100, 100, 1200, 700)
        self.setWindowIcon(QIcon('./pictures/bus_app.png'))
        self.setIconSize(QSize(30, 30))
        # create main widget of app
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)
        
        self.header_layout = QVBoxLayout()
        self.header_frame = header_frame()
        self.header_layout.addWidget(self.header_frame)
        self.main_layout.addLayout(self.header_layout)
        
        self.body_layout = QVBoxLayout()
        self.body_frame = body_frame()
        self.body_layout.addWidget(self.body_frame)
        self.main_layout.addLayout(self.body_layout)
        
        self.header_frame.status_logined.connect(self.body_frame.detail_widget.update_status_login)
        self.header_frame.finished_update.connect(self.body_frame.frame_tabs.reset_list_btns)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = BusMapApp()
    main_window.show()
    sys.exit(app.exec_())
