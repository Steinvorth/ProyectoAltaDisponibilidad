# database_handler.py

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os


class DatabaseHandler:
    def __init__(self):
        load_dotenv()
        self.db_config = {
            "user": os.getenv("MYSQL_USER"),
            "password": os.getenv("MYSQL_PASSWORD"),
            "host": os.getenv("MYSQL_HOST"),
            "database": os.getenv("MYSQL_DATABASE"),
            "port": os.getenv("MYSQL_PORT"),
            "auth_plugin": "mysql_native_password",
        }

    def execute_query(self, query, params=None):
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Error as e:
            print(f"Error: {e}")
            return False

    def fetch_all(self, query, params=None):
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            cursor.close()
            connection.close()
            return rows
        except Error as e:
            print(f"Error: {e}")
            return []

    def fetch_carros(self):
        query = "SELECT * FROM Carros"
        return self.fetch_all(query)

    def fetch_carros_user(self):
        query = "SELECT ID, Marca, Modelo, Placa, Estado FROM Carros"
        return self.fetch_all(query)

    def fetch_usuarios(self):
        query = "SELECT * FROM Usuarios"
        return self.fetch_all(query)

    def fetch_rentas(self):
        query = """
        SELECT Rentas.ID, Usuarios.Username, Carros.Marca, Carros.Modelo, Rentas.ComienzoRenta, Rentas.FinalRenta, Rentas.CostoTotal, Rentas.CreadoEn
        FROM Rentas
        JOIN Usuarios ON Rentas.id_usuario = Usuarios.ID
        JOIN Carros ON Rentas.id_carro = Carros.ID
        """
        return self.fetch_all(query)

    def add_renta(self, id_usuario, id_carro, comienzo_renta, final_renta, costo_total):
        query = "INSERT INTO Rentas (id_usuario, id_carro, ComienzoRenta, FinalRenta, CostoTotal) VALUES (%s, %s, %s, %s, %s)"
        return self.execute_query(
            query, (id_usuario, id_carro, comienzo_renta, final_renta, costo_total)
        )

    def end_renta(self, id_renta, final_renta):
        query = "UPDATE Rentas SET FinalRenta=%s WHERE ID=%s"
        return self.execute_query(query, (final_renta, id_renta))

    def add_carro(self, marca, modelo, placa, estado):
        query = (
            "INSERT INTO Carros (Marca, Modelo, Placa, Estado) VALUES (%s, %s, %s, %s)"
        )
        return self.execute_query(query, (marca, modelo, placa, estado))

    def update_carro(self, id_carro, marca, modelo, placa, estado):
        query = "UPDATE Carros SET Marca=%s, Modelo=%s, Placa=%s, Estado=%s WHERE ID=%s"
        return self.execute_query(query, (marca, modelo, placa, estado, id_carro))

    def update_usuario(self, id_usuario, username, password, email, nombre, apellido):
        query = "UPDATE Usuarios SET Username=%s, Password=%s, Email=%s, Nombre=%s, Apellido=%s WHERE ID=%s"
        return self.execute_query(
            query, (username, password, email, nombre, apellido, id_usuario)
        )

    def add_usuario(self, username, password, email, nombre, apellido):
        query = "INSERT INTO Usuarios (Username, Password, Email, Nombre, Apellido) VALUES (%s, %s, %s, %s, %s)"
        return self.execute_query(query, (username, password, email, nombre, apellido))

    def verify_user(self, username, password):
        query = "SELECT * FROM Usuarios WHERE Username=%s AND Password=%s"
        result = self.fetch_all(query, (username, password))
        return len(result) > 0
