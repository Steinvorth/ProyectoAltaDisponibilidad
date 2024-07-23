# login_window.py

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
)
from database_handler import DatabaseHandler
from user_gui import UserGUI
from gui_handler import GUIHandler


class LoginWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.db_handler = DatabaseHandler()
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        form_layout = QVBoxLayout()
        layout.addLayout(form_layout)

        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)

        form_layout.addWidget(QLabel("Username"))
        form_layout.addWidget(self.username)
        form_layout.addWidget(QLabel("Password"))
        form_layout.addWidget(self.password)

        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login)
        button_layout.addWidget(login_button)

        register_button = QPushButton("Register")
        register_button.clicked.connect(self.show_registration_form)
        button_layout.addWidget(register_button)

        self.setLayout(layout)

    def login(self):
        username = self.username.text()
        password = self.password.text()

        if username == "admin" and password == "admin":
            self.main_window.setCentralWidget(GUIHandler())
            self.main_window.show()
            self.close()
        elif self.db_handler.verify_user(username, password):
            self.main_window.setCentralWidget(UserGUI(username))
            self.main_window.show()
            self.close()
        else:
            QMessageBox.critical(self, "Error", "Invalid credentials")

    def show_registration_form(self):
        self.registration_window = RegistrationWindow(self)
        self.registration_window.show()


class RegistrationWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.db_handler = DatabaseHandler()
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Register")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        form_layout = QVBoxLayout()
        layout.addLayout(form_layout)

        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.email = QLineEdit()
        self.nombre = QLineEdit()
        self.apellido = QLineEdit()

        form_layout.addWidget(QLabel("Username"))
        form_layout.addWidget(self.username)
        form_layout.addWidget(QLabel("Password"))
        form_layout.addWidget(self.password)
        form_layout.addWidget(QLabel("Email"))
        form_layout.addWidget(self.email)
        form_layout.addWidget(QLabel("Nombre"))
        form_layout.addWidget(self.nombre)
        form_layout.addWidget(QLabel("Apellido"))
        form_layout.addWidget(self.apellido)

        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        register_button = QPushButton("Register")
        register_button.clicked.connect(self.register)
        button_layout.addWidget(register_button)

        self.setLayout(layout)

    def register(self):
        username = self.username.text()
        password = self.password.text()
        email = self.email.text()
        nombre = self.nombre.text()
        apellido = self.apellido.text()

        if self.db_handler.add_usuario(username, password, email, nombre, apellido):
            QMessageBox.information(self, "Success", "User registered successfully")
            self.close()
        else:
            QMessageBox.critical(self, "Error", "Error registering user")
