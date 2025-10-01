from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPalette, QBrush


class MainScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget  # Reference to the stacked widget

        # Set the background image
        self.setAutoFillBackground(True)
        palette = self.palette()
        background = QPixmap("black.png")
        palette.setBrush(QPalette.ColorRole.Window, QBrush(background))
        self.setPalette(palette)

        # Layout and widgets for the main screen
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Align all elements to the center

        # Title Label
        self.title_label = QLabel("TruthLens")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 48px; /* Large font size for the app name */
                font-weight: bold;
                color: white;
            }
        """)
        layout.addWidget(self.title_label)

        # Description Label
        self.description_label = QLabel("DeepFake Detection and News Verification")
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
        self.description_label.setStyleSheet("""
            QLabel {
                font-size: 24px; /* Slightly smaller than the title */
                font-weight: bold;
                color: purple;
            }
        """)
        layout.addWidget(self.description_label)

        self.EMPTY = QLabel("")
        layout.addWidget(self.EMPTY)
        self.EMPTY.setStyleSheet("""
                    QLabel {
                        font-size: 24px; /* Slightly smaller than the title */
                        font-weight: bold;
                        color: purple;
                    }
                """)

        # Upload Video Button
        upload_button = QPushButton("Upload Video")
        upload_button.setStyleSheet("""
                    QPushButton {
                        background-color: white;
                        border: none;
                        color: black;  /* Text color */
                        font-size: 16px;  /* Font size */
                    }
                    QPushButton:hover {
                        background-color: rgba(255, 255, 255, 50);  /* Hover effect */
                    }
                """)
        # Set fixed size for the button (Width = 150, Height = 50)
        upload_button.setFixedSize(150, 50)

        # Add the button to the layout and center it
        layout.addWidget(upload_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Connect the button to the file dialog
        upload_button.clicked.connect(self.open_file_dialog)

        self.setLayout(layout)

        # Set window size and position (if necessary)
        self.setGeometry(100, 100, 600, 800)

    def open_file_dialog(self):
        try:
            # Open a file dialog to select video files
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Select Video File",
                "",
                "Video Files (*.mp4 *.avi *.mkv *.mov *.flv);;All Files (*)",
            )

            # Check if a file was selected and update the label
            if file_path:
                if self.is_video_file(file_path):
                    print(f"Selected file path: {file_path}")
                    self.go_to_second_screen(file_path)
                else:
                    print("Invalid file type. Please select a video file.")

        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def is_video_file(file_path):
        # Check the file extension for common video formats
        video_extensions = [".mp4", ".avi", ".mkv", ".mov", ".flv"]
        return any(file_path.lower().endswith(ext) for ext in video_extensions)

    def go_to_second_screen(self, file_path):
        # Switch to the second screen and start detection
        self.stacked_widget.setCurrentIndex(1)
        second_screen = self.stacked_widget.currentWidget()
        second_screen.start_prediction(file_path)
