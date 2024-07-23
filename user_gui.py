# user_gui.py

from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QLabel,
    QWidget,
    QScrollArea,
    QGridLayout,
    QFrame,
    QHBoxLayout,
)
from PyQt5.QtGui import QFont, QPixmap, QPainter, QBrush, QColor
from PyQt5.QtCore import Qt
from database_handler import DatabaseHandler


class UserGUI(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.db_handler = DatabaseHandler()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("User Section")
        self.setGeometry(100, 100, 800, 600)

        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        welcome_label = QLabel(f"Welcome, {self.username}!")
        welcome_label.setFont(QFont("Helvetica", 16))
        layout.addWidget(welcome_label)

        self.car_grid = QGridLayout()
        layout.addLayout(self.car_grid)

        self.display_cars()

        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        self.setCentralWidget(scroll)

    def display_cars(self):
        cars = self.db_handler.fetch_carros_user()

        row = 0
        col = 0
        for car in cars:
            car_id, marca, modelo, placa, estado = car
            car_widget = self.create_car_widget(car_id, marca, estado)
            self.car_grid.addWidget(car_widget, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1

    def create_car_widget(self, car_id, marca, estado):
        widget = QFrame()
        widget.setFrameShape(QFrame.StyledPanel)
        widget.setStyleSheet(
            """
            QFrame {
                border: 1px solid #dcdcdc;
                border-radius: 10px;
                padding: 0px;
                margin: 10px;
                background-color: #f9f9f9;
            }
            """
        )

        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Image placeholder
        image_placeholder = QFrame()
        image_placeholder.setFixedHeight(100)
        image_placeholder.setStyleSheet("background-color: #dcdcdc;")
        layout.addWidget(image_placeholder)

        # Car name and status indicator
        info_layout = QHBoxLayout()
        info_layout.setContentsMargins(10, 10, 10, 10)
        info_layout.setSpacing(10)

        status_indicator = QLabel()
        pixmap = QPixmap(10, 10)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setBrush(QBrush(self.get_status_color(estado)))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, 10, 10)
        painter.end()
        status_indicator.setPixmap(pixmap)

        name_label = QLabel(f"Marca: {marca}")
        name_label.setFont(QFont("Helvetica", 14))

        info_layout.addWidget(status_indicator)
        info_layout.addWidget(name_label)
        info_layout.addStretch()

        layout.addLayout(info_layout)

        return widget

    def get_status_color(self, estado):
        if estado == "disponible":
            return QColor("green")
        elif estado == "no disponible":
            return QColor("red")
        else:
            return QColor("gray")
