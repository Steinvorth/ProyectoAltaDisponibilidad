# user_gui.py

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QWidget


class UserGUI(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.initUI()

    def initUI(self):
        self.setWindowTitle("User Section")
        self.setGeometry(100, 100, 400, 300)

        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        welcome_label = QLabel(f"Welcome, {self.username}!")
        layout.addWidget(welcome_label)

        self.setCentralWidget(widget)
