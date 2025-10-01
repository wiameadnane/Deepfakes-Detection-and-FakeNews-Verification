import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from main_screen import MainScreen
from second_screen import SecondScreen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DeepFake & Fake News Detection")
        self.setGeometry(310, 70, 800, 586)

        # Create the QStackedWidget
        self.stacked_widget = QStackedWidget()

        # Create the screens
        self.main_screen = MainScreen(self.stacked_widget)
        self.second_screen = SecondScreen(self.stacked_widget)

        # Add screens to the QStackedWidget
        self.stacked_widget.addWidget(self.main_screen)
        self.stacked_widget.addWidget(self.second_screen)

        # Set the QStackedWidget as the central widget
        self.setCentralWidget(self.stacked_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())

