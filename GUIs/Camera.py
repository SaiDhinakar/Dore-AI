import cv2 as cv
import numpy as np
from PyQt5.QtWidgets import (QApplication, QWidget, QFileDialog, QPushButton,
                             QLabel, QHBoxLayout, QVBoxLayout, QMessageBox)
from PyQt5.QtGui import QPixmap, QImage, QFont, QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from datetime import datetime
import os

class VideoRecorder(QThread):
    recording_started = pyqtSignal()
    recording_stopped = pyqtSignal(str)

    def __init__(self, cap):
        super().__init__()
        self.cap = cap
        self.out = None
        self.is_recording = False
        self.record_start_time = None

    def run(self):
        frame_width = int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        frame_height = int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        video_file_name = f'Video_{datetime.now().strftime("%Y%m%d_%H%M%S")}.avi'
        self.out = cv.VideoWriter(video_file_name, cv.VideoWriter_fourcc(*'XVID'), 25.0, (frame_width, frame_height))
        self.is_recording = True
        self.recording_started.emit()
        self.record_start_time = datetime.now()

        while self.is_recording:
            ret, frame = self.cap.read()
            if ret:
                self.out.write(frame)

        self.out.release()
        self.recording_stopped.emit(video_file_name)

    def stop(self):
        self.is_recording = False


class CameraFeed(QThread):
    frame_captured = pyqtSignal(np.ndarray)

    def __init__(self, cap):
        super().__init__()
        self.cap = cap
        self.is_running = True

    def run(self):
        while self.is_running:
            ret, frame = self.cap.read()
            if ret:
                self.frame_captured.emit(frame)

    def stop(self):
        self.is_running = False


class CameraApp(QWidget):
    def __init__(self):
        super().__init__()
        
        # Initialize timer_label before calling initUI
        self.timer_label = QLabel(" ")
        self.timer_label.setStyleSheet("font-size: 16px; color: #ffffff;")
        self.timer_label.setAlignment(Qt.AlignCenter)
        
        self.initUI()
        self.cap = cv.VideoCapture(0)
        self.video_thread = None
        self.camera_feed_thread = CameraFeed(self.cap)
        self.camera_feed_thread.frame_captured.connect(self.update_frame)
        self.camera_feed_thread.start()

        # Set fixed size for the picture box
        self.picture_box.setFixedSize(880, 480)  # Set this to your camera's resolution

    def initUI(self):
        self.setWindowTitle("Dore - Camera")
        self.setFixedSize(900, 600)

        # Set font
        font = QFont("Arial", 10)
        self.setFont(font)

        # Create widgets
        self.photo_btn = QPushButton("Capture Photo")
        self.video_btn = QPushButton("Record Video")
        self.picture_box = QLabel("Image will appear here!")
        self.picture_box.setAlignment(Qt.AlignCenter)

        # Set button styles
        self.set_button_style(self.photo_btn)
        self.set_button_style(self.video_btn)

        # Set picture box style
        self.picture_box.setStyleSheet("border: 2px solid #ffffff; border-radius: 5px;")

        # Layout setup
        master_layout = QVBoxLayout()
        master_layout.addWidget(self.timer_label)  # Add timer_label to layout here
        master_layout.addWidget(self.picture_box)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.photo_btn)
        button_layout.addWidget(self.video_btn)
        
        master_layout.addLayout(button_layout)
        self.setLayout(master_layout)

        # Connect button actions
        self.photo_btn.clicked.connect(self.save_image)
        self.video_btn.clicked.connect(self.toggle_video_recording)

        # Set the background gradient
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 rgba(27, 97, 173, 255),
                                            stop:1 rgba(6, 40, 78, 255));
                color: #ffffff;
            }
        """)

    def set_button_style(self, button):
        button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid #ffffff;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
            }
        """)

    def update_frame(self, frame):
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        frame = cv.flip(frame, 1)
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)

        # Update timer label if recording
        if self.video_thread and self.video_thread.is_recording:
            elapsed_time = (datetime.now() - self.video_thread.record_start_time).seconds
            timer_text = f"Time: {elapsed_time // 60}:{elapsed_time % 60:02d}"
            self.timer_label.setText(timer_text)  # Update the timer label

        # Display the image in the fixed-size picture box
        scaled_image = qt_image.scaled(self.picture_box.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.picture_box.setPixmap(QPixmap.fromImage(scaled_image))

    def save_image(self):
        if self.cap.isOpened():  # Check if the camera is active
            ret, frame = self.cap.read()
            if ret:
                save_dir = QFileDialog.getExistingDirectory(self, "Select Directory")
                if save_dir:
                    file_name = f'capture_{datetime.now().strftime("%Y%m%d_%H%M%S")}.jpg'
                    path = os.path.join(save_dir, file_name)
                    cv.imwrite(path, frame)
                    QMessageBox.information(self, "Image Saved", f"Image saved to: {path}")
        else:
            QMessageBox.warning(self, "Camera Error", "Camera is not active.")

    def toggle_video_recording(self):
        if self.video_thread is None or not self.video_thread.is_recording:
            self.start_video_recording()
        else:
            self.stop_video_recording()

    def start_video_recording(self):
        self.video_thread = VideoRecorder(self.cap)
        self.video_thread.recording_started.connect(self.on_recording_started)
        self.video_thread.recording_stopped.connect(self.on_recording_stopped)
        self.video_thread.start()

    def on_recording_started(self):
        self.video_btn.setText("Stop Recording")

    def on_recording_stopped(self, video_file_name):
        self.video_btn.setText("Record Video")
        save_dir = QFileDialog.getExistingDirectory(self, "Select Directory to Save Video")
        if save_dir:
            final_path = os.path.join(save_dir, video_file_name)
            os.rename(video_file_name, final_path)
            QMessageBox.information(self, "Video Saved", f"Video saved to: {final_path}")
        self.video_thread = None

    def stop_video_recording(self):
        if self.video_thread:
            self.video_thread.stop()
            self.video_thread.wait()
            self.timer_label.setText(" ")

    def closeEvent(self, event):
        self.cap.release()
        self.camera_feed_thread.stop()
        self.camera_feed_thread.wait()
        if self.video_thread:
            self.video_thread.stop()
            self.video_thread.wait()

if __name__ == '__main__':
    app = QApplication([])
    cam = CameraApp()
    cam.setWindowIcon(QIcon(r"assets/camera.png"))  # Add your icon here if needed
    cam.show()
    app.exec_()
