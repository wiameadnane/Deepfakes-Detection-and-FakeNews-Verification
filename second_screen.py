from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget, QLabel, QScrollArea
from PyQt6.QtGui import QPixmap, QPalette, QBrush

from DEEPFAKE import prediction
from FAKENEWS import fake_news_detection

from PyQt6.QtCore import Qt


class SecondScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget

        self.video_path = None

        # Set background pic
        self.setAutoFillBackground(True)
        palette = self.palette()
        background = QPixmap("black")
        palette.setBrush(QPalette.ColorRole.Window, QBrush(background))
        self.setPalette(palette)

        # Scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Main content widget
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)

        self.title_label = QLabel("TruthLens")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
        self.title_label.setStyleSheet("""
                    QLabel {
                        font-size: 25px; /* Large font size for the app name */
                        font-weight: bold;
                        color: white;
                    }
                """)
        layout.addWidget(self.title_label)

        self.deepfake_label = QLabel("DeepFake Frames Analysis Result")
        layout.addWidget(self.deepfake_label)
        self.deepfake_label.setStyleSheet("""
            QLabel {
                font-size: 17px; /* Adjust the size as needed */
                font-weight: bold;
                color: purple; /* Optional: change text color */
            }
        """)
        layout.addWidget(self.deepfake_label)

        self.label = QLabel("")
        layout.addWidget(self.label)

        self.EMPTY = QLabel("")
        layout.addWidget(self.EMPTY)

        self.fakenews_label = QLabel("News Detection Result")
        layout.addWidget(self.fakenews_label)
        self.fakenews_label.setStyleSheet("""
            QLabel {
                font-size: 17px; /* Adjust the size as needed */
                font-weight: bold;
                color: purple; /* Optional: change text color */
            }
        """)
        layout.addWidget(self.fakenews_label)

        self.text_label = QLabel("")
        layout.addWidget(self.text_label)
        self.text_label.setStyleSheet("""
                    QLabel {
                        font-size: 15px; /* Adjust the size as needed */
                        font-weight: bold;
                        color: white; /* Optional: change text color */
                    }
                """)

        self.articles_label = QLabel("")
        self.articles_label.setWordWrap(True)
        self.articles_label.setOpenExternalLinks(True)
        layout.addWidget(self.articles_label)

        # Button to go back to main
        main_button = QPushButton("Main Screen")
        main_button.clicked.connect(self.go_to_main_screen)
        layout.addWidget(main_button)

        main_button.setStyleSheet("""
                            QPushButton {
                                background-color: #ffffff;   /* Black background */
                                color: #44a2e2;              /* Blue text */
                                border: 2px solid #44a2e2;   /* Blue border */
                                font-size: 14px;          /* Optional: Adjust text size */
                                border-radius: 5px;       /* Optional: Rounded corners */
                                padding: 5px;             /* Optional: Add padding */
                            }
                            QPushButton:hover {
                                background-color: #000000; /* Slightly lighter black on hover */
                                color: #44a2e2;          /* Light blue text on hover */
                                border-color: #44a2e2;   /* Light blue border on hover */
                            }
                            QPushButton:pressed {
                                background-color: #222222; /* Darker black on press */
                                color: darkblue;           /* Dark blue text on press */
                                border-color: darkblue;    /* Dark blue border on press */
                            }
                            """)

        scroll_area.setWidget(content_widget)

        # Main layout for SecondScreen
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)

    def go_to_main_screen(self):
        self.stacked_widget.setCurrentIndex(0)

    def start_prediction(self, video_path):
        self.video_path = video_path

        #DEEPFAKE FRAMES
        prediction_score = prediction(self.video_path)
        pred = (prediction_score > 0.5).astype(int)

        if pred == 0:
            self.label.setText("The video is real !")
        elif pred == 1:
            self.label.setText("The video is deepfaked !")


        #FAKE NEWS
        summarized_articles = fake_news_detection(video_path)

        if summarized_articles:
            self.text_label.setText("Here are 5 articles most similar to the content of your video :")
            articles_text = ""
            for article in summarized_articles:
                source_name = article['source'].get('name', 'Unknown Source')  # Use 'Unknown Source' as fallback
                article_text = f"<b>Title:</b> {article['title']}<br>" \
                               f"<b>Summary:</b> {article['summary']}<br>" \
                               f"<b>Source:</b> {source_name}<br>" \
                               f"<b>URL:</b> <a href='{article['url']}'>{article['url']}</a><br><br>"

                articles_text += article_text

            self.articles_label.setText(articles_text)
        else:
            self.articles_label.setText("No summarized articles were found.")
