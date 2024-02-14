import cv2
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt
from PyQt6.uic import loadUi

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load the UI file
        loadUi('main.ui', self)
        self.btnBrowse.clicked.connect(self.browse_and_load_video)
        self.btnPlay.clicked.connect(self.play_video)
        self.btnPause.clicked.connect(self.pause_video)  # Connect btnPause to pause_video method
        self.btnResume.clicked.connect(self.resume_video)  # Connect btnResume to resume_video method
        
        # Initialize video capture object
        self.cap = None
        self.paused = False  # Flag to track whether the video is paused

    def browse_and_load_video(self):
        # Get the file path from the file selection dialog
        filename, _ = QFileDialog.getOpenFileName(
            self, "Select Video File", "", "Video Files (*.mp4 *.avi *.mkv)"
        )

        # Check if a file was selected
        if not filename:
            return

        try:
            # Load the video using OpenCV
            self.cap = cv2.VideoCapture(filename)

            # Check if video capture was successful
            if not self.cap.isOpened():
                raise RuntimeError("Error opening video file.")

            # Get the target width and height
            target_width = self.lblVideo.width()
            target_height = self.lblVideo.height()

            while True:
                # Capture a frame from the video
                ret, frame = self.cap.read()

                # Check if video is still playing
                if not ret:
                    break

                # Resize the frame to fit the target dimensions
                frame = cv2.resize(frame, (target_width, target_height))

                # Convert the frame to QImage format
                qimage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                qt_image = QImage(qimage.data, qimage.shape[1], qimage.shape[0], qimage.strides[0], QImage.Format.Format_RGB888)

                # Display the frame in the label
                pixmap = QPixmap.fromImage(qt_image)
                self.lblVideo.setPixmap(pixmap)

                # Apply any further processing or display options as needed

                # Check if video is paused
                if self.paused:
                    cv2.waitKey(-1)  # Wait indefinitely until the video is resumed

        except Exception as e:
            # Handle errors gracefully (e.g., display an error message to the user)
            print(f"Error loading video: {e}")

    def play_video(self):
        # Check if video capture object is initialized
        if self.cap is None or not self.cap.isOpened():
            return

        while True:
            # Capture a frame from the video
            ret, frame = self.cap.read()

            # Check if video is still playing
            if not ret:
                break

            # Resize the frame to fit the target dimensions
            target_width = self.lblVideo.width()
            target_height = self.lblVideo.height()
            frame = cv2.resize(frame, (target_width, target_height))

            # Convert the frame to QImage format
            qimage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            qt_image = QImage(qimage.data, qimage.shape[1], qimage.shape[0], qimage.strides[0], QImage.Format.Format_RGB888)

            # Display the frame in the label
            pixmap = QPixmap.fromImage(qt_image)
            self.lblVideo.setPixmap(pixmap)

            # Apply any further processing or display options as needed

            # Wait for a short duration to simulate video playback speed
            cv2.waitKey(30)

    def pause_video(self):
        self.paused = True

    def resume_video(self):
        self.paused = False
        cv2.waitKey(1)  # Unblock the video playback loop

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MyMainWindow()
    mainWindow.show()
    sys.exit(app.exec())
