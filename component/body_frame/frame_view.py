import sys
from PyQt5.QtWidgets import QFrame, QApplication, QSizePolicy, QVBoxLayout
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
import os

class frame_view(QFrame):
    def __init__(self, html_file=None):
        super().__init__()
        self.html_file = html_file
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.view_map_layout = QVBoxLayout(self)
        
        self.map = QWebEngineView()
        if html_file:
            url = QUrl.fromLocalFile(os.path.realpath(html_file))
            self.map.load(url)
        
        self.view_map_layout.addWidget(self.map)
        self.setLayout(self.view_map_layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    h_lay = frame_view('./map/direction_0/1062.html')
    h_lay.show()
    sys.exit(app.exec_())