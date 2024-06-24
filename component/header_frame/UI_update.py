import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton, QWidget, QLabel, QProgressBar, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from .update import UpdateThread

class updateUI(QWidget):
    finishedUp = pyqtSignal(bool)
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('./pictures/update.png'))
        self.setWindowTitle('Update data app')
        self.setFixedSize(300, 130)
        
        self.label = QLabel("Click the button to update data")
        self.button = QPushButton("Update Data")
        self.button.clicked.connect(self.start_update)
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def start_update(self):
        self.update_thread = UpdateThread()
        self.update_thread.update_progress.connect(self.progress_bar.setValue)
        self.update_thread.update_status.connect(self.label.setText)
        self.update_thread.finished.connect(self.on_thread_finished)
        self.update_thread.start()
    
    def on_thread_finished(self):
        self.label.setText(self.label.text() + "\nThread has been stopped.")
        QMessageBox.information(self, 'Update Successful', 'Update completed!')
        self.update_thread.data_update.update_status_update(True)
        self.update_thread.deleteLater()
        self.update_thread = None
        self.button.setText('Close update')
        self.button.clicked.disconnect(self.start_update)
        self.button.clicked.connect(self.close)
        self.finishedUp.emit(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = updateUI()
    w.show()
    sys.exit(app.exec_())