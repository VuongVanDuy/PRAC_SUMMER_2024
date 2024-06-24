import json
from PyQt5.QtCore import QThread, pyqtSignal
from ..data_app import data_update

class UpdateThread(QThread):
    update_progress = pyqtSignal(int)
    update_status = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.data_update = data_update()

    def run(self):
        self.update_status.emit("Starting update...")
        self.info_update = self.data_update.get_data_update()
        self.data_files_update = self.info_update['files_update']
        
        files_path = list(self.data_files_update.keys())
        total_files = len(files_path)
        
        for index, file_path in enumerate(files_path):
            with open(file_path, 'w') as file:
                json.dump(self.data_files_update[file_path], file, indent=4)
            progress = int(((index + 1) / total_files) * 100)
            self.update_progress.emit(progress)
        
        self.update_status.emit("Update completed!")