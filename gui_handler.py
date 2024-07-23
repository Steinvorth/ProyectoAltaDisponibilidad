# gui_handler.py

from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QMessageBox,
    QHeaderView,
    QDateTimeEdit,
)
from PyQt5.QtCore import QDateTime
from database_handler import DatabaseHandler


class GUIHandler(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_handler = DatabaseHandler()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Gestión de Carros, Usuarios y Alquileres")
        self.setGeometry(100, 100, 1200, 800)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        self.car_tab = QWidget()
        self.user_tab = QWidget()
        self.rent_tab = QWidget()

        self.tabs.addTab(self.car_tab, "Carros")
        self.tabs.addTab(self.user_tab, "Usuarios")
        self.tabs.addTab(self.rent_tab, "Rentas")

        self.setup_car_tab()
        self.setup_user_tab()
        self.setup_rent_tab()

        self.show()

    def setup_car_tab(self):
        layout = QVBoxLayout(self.car_tab)

        self.car_table = QTableWidget()
        self.car_table.setColumnCount(5)
        self.car_table.setHorizontalHeaderLabels(
            ["ID", "Marca", "Modelo", "Placa", "Estado"]
        )
        self.car_table.horizontalHeader().setStretchLastSection(True)
        self.car_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.car_table)

        form_layout = QHBoxLayout()
        layout.addLayout(form_layout)

        self.car_id = QLineEdit()
        self.car_marca = QLineEdit()
        self.car_modelo = QLineEdit()
        self.car_placa = QLineEdit()
        self.car_estado = QComboBox()
        self.car_estado.addItems(["disponible", "no disponible", "fuera de servicio"])

        form_layout.addWidget(QLabel("ID"))
        form_layout.addWidget(self.car_id)
        form_layout.addWidget(QLabel("Marca"))
        form_layout.addWidget(self.car_marca)
        form_layout.addWidget(QLabel("Modelo"))
        form_layout.addWidget(self.car_modelo)
        form_layout.addWidget(QLabel("Placa"))
        form_layout.addWidget(self.car_placa)
        form_layout.addWidget(QLabel("Estado"))
        form_layout.addWidget(self.car_estado)

        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        add_button = QPushButton("Agregar")
        add_button.clicked.connect(self.add_car)
        update_button = QPushButton("Actualizar")
        update_button.clicked.connect(self.update_car)
        clear_button = QPushButton("Limpiar")
        clear_button.clicked.connect(self.clear_car_form)

        button_layout.addWidget(add_button)
        button_layout.addWidget(update_button)
        button_layout.addWidget(clear_button)

        self.refresh_cars()

    def setup_user_tab(self):
        layout = QVBoxLayout(self.user_tab)

        self.user_table = QTableWidget()
        self.user_table.setColumnCount(7)
        self.user_table.setHorizontalHeaderLabels(
            [
                "ID",
                "Username",
                "Email",
                "Nombre",
                "Apellido",
                "CreadoEn",
                "ActualizadoEn",
            ]
        )
        self.user_table.horizontalHeader().setStretchLastSection(True)
        self.user_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.user_table)

        form_layout = QHBoxLayout()
        layout.addLayout(form_layout)

        self.user_id = QLineEdit()
        self.user_username = QLineEdit()
        self.user_password = QLineEdit()
        self.user_email = QLineEdit()
        self.user_nombre = QLineEdit()
        self.user_apellido = QLineEdit()

        form_layout.addWidget(QLabel("ID"))
        form_layout.addWidget(self.user_id)
        form_layout.addWidget(QLabel("Username"))
        form_layout.addWidget(self.user_username)
        form_layout.addWidget(QLabel("Password"))
        form_layout.addWidget(self.user_password)
        form_layout.addWidget(QLabel("Email"))
        form_layout.addWidget(self.user_email)
        form_layout.addWidget(QLabel("Nombre"))
        form_layout.addWidget(self.user_nombre)
        form_layout.addWidget(QLabel("Apellido"))
        form_layout.addWidget(self.user_apellido)

        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        add_button = QPushButton("Agregar")
        add_button.clicked.connect(self.add_user)
        clear_button = QPushButton("Limpiar")
        clear_button.clicked.connect(self.clear_user_form)

        button_layout.addWidget(add_button)
        button_layout.addWidget(clear_button)

        self.refresh_users()

    def setup_rent_tab(self):
        layout = QVBoxLayout(self.rent_tab)

        self.rent_table = QTableWidget()
        self.rent_table.setColumnCount(7)
        self.rent_table.setHorizontalHeaderLabels(
            [
                "ID",
                "Usuario",
                "Carro",
                "Comienzo Renta",
                "Final Renta",
                "Costo Total",
                "CreadoEn",
            ]
        )
        self.rent_table.horizontalHeader().setStretchLastSection(True)
        self.rent_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.rent_table)

        form_layout = QHBoxLayout()
        layout.addLayout(form_layout)

        self.rent_id_usuario = QComboBox()
        self.rent_id_carro = QComboBox()
        self.rent_comienzo_renta = QDateTimeEdit(QDateTime.currentDateTime())
        self.rent_comienzo_renta.setCalendarPopup(True)
        self.rent_final_renta = QDateTimeEdit(QDateTime.currentDateTime())
        self.rent_final_renta.setCalendarPopup(True)
        self.rent_costo_total = QLineEdit()

        form_layout.addWidget(QLabel("ID Usuario"))
        form_layout.addWidget(self.rent_id_usuario)
        form_layout.addWidget(QLabel("ID Carro"))
        form_layout.addWidget(self.rent_id_carro)
        form_layout.addWidget(QLabel("Comienzo Renta"))
        form_layout.addWidget(self.rent_comienzo_renta)
        form_layout.addWidget(QLabel("Final Renta"))
        form_layout.addWidget(self.rent_final_renta)
        form_layout.addWidget(QLabel("Costo Total"))
        form_layout.addWidget(self.rent_costo_total)

        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        add_button = QPushButton("Agregar")
        add_button.clicked.connect(self.add_rent)
        finalize_button = QPushButton("Finalizar Renta")
        finalize_button.clicked.connect(self.end_rent)
        clear_button = QPushButton("Limpiar")
        clear_button.clicked.connect(self.clear_rent_form)

        button_layout.addWidget(add_button)
        button_layout.addWidget(finalize_button)
        button_layout.addWidget(clear_button)

        self.refresh_rents()
        self.update_comboboxes()

    def add_car(self):
        if self.db_handler.add_carro(
            self.car_marca.text(),
            self.car_modelo.text(),
            self.car_placa.text(),
            self.car_estado.currentText(),
        ):
            QMessageBox.information(self, "Éxito", "Carro agregado exitosamente")
            self.refresh_cars()
        else:
            QMessageBox.critical(self, "Error", "Error al agregar carro")

    def add_user(self):
        if self.db_handler.add_usuario(
            self.user_username.text(),
            self.user_password.text(),
            self.user_email.text(),
            self.user_nombre.text(),
            self.user_apellido.text(),
        ):
            QMessageBox.information(self, "Éxito", "Usuario agregado exitosamente")
            self.refresh_users()
        else:
            QMessageBox.critical(self, "Error", "Error al agregar usuario")

    def add_rent(self):
        comienzo_renta = self.rent_comienzo_renta.dateTime().toString(
            "yyyy-MM-dd HH:mm:ss"
        )
        final_renta = self.rent_final_renta.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        if self.db_handler.add_renta(
            self.rent_id_usuario.currentText(),
            self.rent_id_carro.currentText(),
            comienzo_renta,
            final_renta,
            self.rent_costo_total.text(),
        ):
            QMessageBox.information(self, "Éxito", "Renta registrada exitosamente")
            self.refresh_rents()
        else:
            QMessageBox.critical(self, "Error", "Error al agregar renta")

    def end_rent(self):
        selected_row = self.rent_table.currentRow()
        selected_renta_id = self.rent_table.item(selected_row, 0).text()
        if self.db_handler.end_renta(selected_renta_id, self.rent_final_renta.text()):
            QMessageBox.information(self, "Éxito", "Renta finalizada exitosamente")
            self.refresh_rents()
        else:
            QMessageBox.critical(self, "Error", "Error al finalizar renta")

    def update_car(self):
        if self.db_handler.update_carro(
            self.car_id.text(),
            self.car_marca.text(),
            self.car_modelo.text(),
            self.car_placa.text(),
            self.car_estado.currentText(),
        ):
            QMessageBox.information(self, "Éxito", "Carro actualizado exitosamente")
            self.refresh_cars()
        else:
            QMessageBox.critical(self, "Error", "Error al actualizar carro")

    def clear_car_form(self):
        self.car_id.clear()
        self.car_marca.clear()
        self.car_modelo.clear()
        self.car_placa.clear()
        self.car_estado.setCurrentIndex(0)

    def clear_user_form(self):
        self.user_id.clear()
        self.user_username.clear()
        self.user_password.clear()
        self.user_email.clear()
        self.user_nombre.clear()
        self.user_apellido.clear()

    def clear_rent_form(self):
        self.rent_id_usuario.setCurrentIndex(0)
        self.rent_id_carro.setCurrentIndex(0)
        self.rent_comienzo_renta.setDateTime(QDateTime.currentDateTime())
        self.rent_final_renta.setDateTime(QDateTime.currentDateTime())
        self.rent_costo_total.clear()

    def refresh_cars(self):
        self.car_table.setRowCount(0)
        rows = self.db_handler.fetch_carros()
        for row in rows:
            row_position = self.car_table.rowCount()
            self.car_table.insertRow(row_position)
            for col, data in enumerate(row):
                self.car_table.setItem(row_position, col, QTableWidgetItem(str(data)))

    def refresh_users(self):
        self.user_table.setRowCount(0)
        rows = self.db_handler.fetch_usuarios()
        for row in rows:
            row_position = self.user_table.rowCount()
            self.user_table.insertRow(row_position)
            for col, data in enumerate(row):
                self.user_table.setItem(row_position, col, QTableWidgetItem(str(data)))

    def refresh_rents(self):
        self.rent_table.setRowCount(0)
        rows = self.db_handler.fetch_rentas()
        for row in rows:
            row_position = self.rent_table.rowCount()
            self.rent_table.insertRow(row_position)
            for col, data in enumerate(row):
                self.rent_table.setItem(row_position, col, QTableWidgetItem(str(data)))

    def update_comboboxes(self):
        usuarios = self.db_handler.fetch_usuarios()
        carros = self.db_handler.fetch_carros()

        self.rent_id_usuario.clear()
        self.rent_id_usuario.addItems([str(u[0]) for u in usuarios])
        self.rent_id_carro.clear()
        self.rent_id_carro.addItems([str(c[0]) for c in carros])
