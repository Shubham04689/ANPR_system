import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import QThread, pyqtSignal
from video_processor import VideoProcessor
from plate_detector import PlateDetector
from char_recognizer import CharRecognizer
from database import Database

class ANPRThread(QThread):
    update_signal = pyqtSignal(str)

    def __init__(self, video_path):
        super().__init__()
        self.video_path = video_path

    def run(self):
        video_processor = VideoProcessor(self.video_path)
        plate_detector = PlateDetector()
        char_recognizer = CharRecognizer()
        db = Database()

        for frame, timestamp in video_processor.process():
            plates = plate_detector.detect(frame)
            for plate in plates:
                chars = char_recognizer.recognize(plate)
                db.insert_record(chars, timestamp)
                self.update_signal.emit(f"Detected plate: {chars} at {timestamp}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ANPR System")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.file_button = QPushButton("Select Video File")
        self.file_button.clicked.connect(self.select_file)
        layout.addWidget(self.file_button)

        self.camera_button = QPushButton("Use Camera")
        self.camera_button.clicked.connect(self.use_camera)
        layout.addWidget(self.camera_button)

        self.status_label = QLabel("Status: Idle")
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Video File", "", "Video Files (*.mp4 *.avi)")
        if file_path:
            self.start_processing(file_path)

    def use_camera(self):
        self.start_processing(0)  # 0 is typically the default camera

    def start_processing(self, video_path):
        self.anpr_thread = ANPRThread(video_path)
        self.anpr_thread.update_signal.connect(self.update_status)
        self.anpr_thread.start()

    def update_status(self, message):
        self.status_label.setText(f"Status: {message}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())