import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Configuración de la conexión a MySQL
db_config = {
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "host": os.getenv("MYSQL_HOST"),
    "database": os.getenv("MYSQL_DATABASE"),
    "port": os.getenv("MYSQL_PORT"),
}


# Funciones para manejar la base de datos
def fetch_carros():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Carros")
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows
    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return []


def fetch_usuarios():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Usuarios")
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows
    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return []


def fetch_rentas():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT Rentas.ID, Usuarios.Username, Carros.Marca, Carros.Modelo, Rentas.ComienzoRenta, Rentas.FinalRenta, Rentas.CostoTotal
            FROM Rentas
            JOIN Usuarios ON Rentas.id_usuario = Usuarios.ID
            JOIN Carros ON Rentas.id_carro = Carros.ID
            WHERE Rentas.FinalRenta IS NULL
        """
        )
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows
    except Error as e:
        print(f"Error al conectarse a MySQL: {e}")
        return []


def add_renta(id_usuario, id_carro, comienzo_renta, final_renta, costo_total):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO Rentas (id_usuario, id_carro, ComienzoRenta, FinalRenta, CostoTotal) VALUES (%s, %s, %s, %s, %s)",
            (id_usuario, id_carro, comienzo_renta, final_renta, costo_total),
        )
        connection.commit()
        cursor.close()
        connection.close()
        messagebox.showinfo("Éxito", "Renta registrada exitosamente")
    except Error as e:
        messagebox.showerror("Error", f"Error al agregar renta: {e}")


def end_renta(id_renta, final_renta):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE Rentas SET FinalRenta=%s WHERE ID=%s", (final_renta, id_renta)
        )
        connection.commit()
        cursor.close()
        connection.close()
        messagebox.showinfo("Éxito", "Renta finalizada exitosamente")
    except Error as e:
        messagebox.showerror("Error", f"Error al finalizar renta: {e}")


def update_carro(id_carro, marca, modelo, placa, estado):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE Carros SET Marca=%s, Modelo=%s, Placa=%s, Estado=%s WHERE ID=%s",
            (marca, modelo, placa, estado, id_carro),
        )
        connection.commit()
        cursor.close()
        connection.close()
        messagebox.showinfo("Éxito", "Carro actualizado exitosamente")
    except Error as e:
        messagebox.showerror("Error", f"Error al actualizar carro: {e}")


def update_usuario(id_usuario, username, password, email, nombre, apellido):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE Usuarios SET Username=%s, Password=%s, Email=%s, Nombre=%s, Apellido=%s WHERE ID=%s",
            (username, password, email, nombre, apellido, id_usuario),
        )
        connection.commit()
        cursor.close()
        connection.close()
        messagebox.showinfo("Éxito", "Usuario actualizado exitosamente")
    except Error as e:
        messagebox.showerror("Error", f"Error al actualizar usuario: {e}")


def refresh_carros():
    for item in tree_carros.get_children():
        tree_carros.delete(item)
    rows = fetch_carros()
    for row in rows:
        tree_carros.insert("", tk.END, values=row)


def refresh_usuarios():
    for item in tree_usuarios.get_children():
        tree_usuarios.delete(item)
    rows = fetch_usuarios()
    for row in rows:
        tree_usuarios.insert("", tk.END, values=row)


def refresh_rentas():
    for item in tree_rentas.get_children():
        tree_rentas.delete(item)
    rows = fetch_rentas()
    for row in rows:
        tree_rentas.insert("", tk.END, values=row)


# Crear la ventana principal
root = tk.Tk()
root.title("Gestión de Carros, Usuarios y Alquileres")
root.geometry("1000x700")

# Crear el notebook (pestañas)
notebook = ttk.Notebook(root)
notebook.pack(pady=10, fill=tk.BOTH, expand=True)

# Crear las pestañas
tab_carros = tk.Frame(notebook)
tab_usuarios = tk.Frame(notebook)
tab_rentas = tk.Frame(notebook)

notebook.add(tab_carros, text="Carros")
notebook.add(tab_usuarios, text="Usuarios")
notebook.add(tab_rentas, text="Rentas")

# Página de Carros
tree_carros = ttk.Treeview(tab_carros)
tree_carros["columns"] = ("ID", "Marca", "Modelo", "Placa", "Estado")
tree_carros.column("#0", width=0, stretch=tk.NO)
tree_carros.column("ID", anchor=tk.CENTER, width=50)
tree_carros.column("Marca", anchor=tk.W, width=150)
tree_carros.column("Modelo", anchor=tk.W, width=150)
tree_carros.column("Placa", anchor=tk.W, width=150)
tree_carros.column("Estado", anchor=tk.W, width=200)
tree_carros.heading("#0", text="", anchor=tk.CENTER)
tree_carros.heading("ID", text="ID", anchor=tk.CENTER)
tree_carros.heading("Marca", text="Marca", anchor=tk.W)
tree_carros.heading("Modelo", text="Modelo", anchor=tk.W)
tree_carros.heading("Placa", text="Placa", anchor=tk.W)
tree_carros.heading("Estado", text="Estado", anchor=tk.W)
tree_carros.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

# Formulario de Carros
frame_carros = tk.Frame(tab_carros, padx=20, pady=20)
frame_carros.pack(pady=10, fill=tk.X)

tk.Label(frame_carros, text="ID", font=("Helvetica", 12)).grid(
    row=0, column=0, sticky=tk.W, padx=10
)
entry_id_carro = tk.Entry(frame_carros, font=("Helvetica", 12))
entry_id_carro.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame_carros, text="Marca", font=("Helvetica", 12)).grid(
    row=1, column=0, sticky=tk.W, padx=10
)
entry_marca = tk.Entry(frame_carros, font=("Helvetica", 12))
entry_marca.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame_carros, text="Modelo", font=("Helvetica", 12)).grid(
    row=2, column=0, sticky=tk.W, padx=10
)
entry_modelo = tk.Entry(frame_carros, font=("Helvetica", 12))
entry_modelo.grid(row=2, column=1, padx=10, pady=5)

tk.Label(frame_carros, text="Placa", font=("Helvetica", 12)).grid(
    row=3, column=0, sticky=tk.W, padx=10
)
entry_placa = tk.Entry(frame_carros, font=("Helvetica", 12))
entry_placa.grid(row=3, column=1, padx=10, pady=5)

tk.Label(frame_carros, text="Estado", font=("Helvetica", 12)).grid(
    row=4, column=0, sticky=tk.W, padx=10
)
combo_estado = ttk.Combobox(
    frame_carros,
    values=["disponible", "no disponible", "fuera de servicio"],
    font=("Helvetica", 12),
)
combo_estado.grid(row=4, column=1, padx=10, pady=5)

btn_add_carro = tk.Button(
    frame_carros,
    text="Agregar",
    command=lambda: add_carro(
        entry_marca.get(), entry_modelo.get(), entry_placa.get(), combo_estado.get()
    ),
)
btn_add_carro.grid(row=5, column=0, padx=10)

btn_update_carro = tk.Button(
    frame_carros,
    text="Actualizar",
    command=lambda: update_carro(
        entry_id_carro.get(),
        entry_marca.get(),
        entry_modelo.get(),
        entry_placa.get(),
        combo_estado.get(),
    ),
)
btn_update_carro.grid(row=5, column=1, padx=10)

btn_clear_carros = tk.Button(
    frame_carros,
    text="Limpiar",
    command=lambda: [
        entry_id_carro.delete(0, tk.END),
        entry_marca.delete(0, tk.END),
        entry_modelo.delete(0, tk.END),
        entry_placa.delete(0, tk.END),
        combo_estado.set(""),
    ],
)
btn_clear_carros.grid(row=5, column=2, padx=10)

refresh_carros()

# Página de Usuarios
tree_usuarios = ttk.Treeview(tab_usuarios)
tree_usuarios["columns"] = ("ID", "Username", "Email", "Nombre", "Apellido")
tree_usuarios.column("#0", width=0, stretch=tk.NO)
tree_usuarios.column("ID", anchor=tk.CENTER, width=50)
tree_usuarios.column("Username", anchor=tk.W, width=150)
tree_usuarios.column("Email", anchor=tk.W, width=150)
tree_usuarios.column("Nombre", anchor=tk.W, width=150)
tree_usuarios.column("Apellido", anchor=tk.W, width=150)
tree_usuarios.heading("#0", text="", anchor=tk.CENTER)
tree_usuarios.heading("ID", text="ID", anchor=tk.CENTER)
tree_usuarios.heading("Username", text="Username", anchor=tk.W)
tree_usuarios.heading("Email", text="Email", anchor=tk.W)
tree_usuarios.heading("Nombre", text="Nombre", anchor=tk.W)
tree_usuarios.heading("Apellido", text="Apellido", anchor=tk.W)
tree_usuarios.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

# Formulario de Usuarios
frame_usuarios = tk.Frame(tab_usuarios, padx=20, pady=20)
frame_usuarios.pack(pady=10, fill=tk.X)

tk.Label(frame_usuarios, text="Username", font=("Helvetica", 12)).grid(
    row=0, column=0, sticky=tk.W, padx=10
)
entry_username = tk.Entry(frame_usuarios, font=("Helvetica", 12))
entry_username.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame_usuarios, text="Password", font=("Helvetica", 12)).grid(
    row=1, column=0, sticky=tk.W, padx=10
)
entry_password = tk.Entry(frame_usuarios, font=("Helvetica", 12), show="*")
entry_password.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame_usuarios, text="Email", font=("Helvetica", 12)).grid(
    row=2, column=0, sticky=tk.W, padx=10
)
entry_email = tk.Entry(frame_usuarios, font=("Helvetica", 12))
entry_email.grid(row=2, column=1, padx=10, pady=5)

tk.Label(frame_usuarios, text="Nombre", font=("Helvetica", 12)).grid(
    row=3, column=0, sticky=tk.W, padx=10
)
entry_nombre = tk.Entry(frame_usuarios, font=("Helvetica", 12))
entry_nombre.grid(row=3, column=1, padx=10, pady=5)

tk.Label(frame_usuarios, text="Apellido", font=("Helvetica", 12)).grid(
    row=4, column=0, sticky=tk.W, padx=10
)
entry_apellido = tk.Entry(frame_usuarios, font=("Helvetica", 12))
entry_apellido.grid(row=4, column=1, padx=10, pady=5)

btn_add_usuario = tk.Button(
    frame_usuarios,
    text="Agregar",
    command=lambda: add_usuario(
        entry_username.get(),
        entry_password.get(),
        entry_email.get(),
        entry_nombre.get(),
        entry_apellido.get(),
    ),
)
btn_add_usuario.grid(row=5, column=0, padx=10)

btn_clear_usuarios = tk.Button(
    frame_usuarios,
    text="Limpiar",
    command=lambda: [
        entry_username.delete(0, tk.END),
        entry_password.delete(0, tk.END),
        entry_email.delete(0, tk.END),
        entry_nombre.delete(0, tk.END),
        entry_apellido.delete(0, tk.END),
    ],
)
btn_clear_usuarios.grid(row=5, column=1, padx=10)

refresh_usuarios()

# Página de Rentas
tree_rentas = ttk.Treeview(tab_rentas)
tree_rentas["columns"] = (
    "ID",
    "Usuario",
    "Carro",
    "ComienzoRenta",
    "FinalRenta",
    "CostoTotal",
)
tree_rentas.column("#0", width=0, stretch=tk.NO)
tree_rentas.column("ID", anchor=tk.CENTER, width=50)
tree_rentas.column("Usuario", anchor=tk.W, width=150)
tree_rentas.column("Carro", anchor=tk.W, width=150)
tree_rentas.column("ComienzoRenta", anchor=tk.W, width=150)
tree_rentas.column("FinalRenta", anchor=tk.W, width=150)
tree_rentas.column("CostoTotal", anchor=tk.W, width=150)
tree_rentas.heading("#0", text="", anchor=tk.CENTER)
tree_rentas.heading("ID", text="ID", anchor=tk.CENTER)
tree_rentas.heading("Usuario", text="Usuario", anchor=tk.W)
tree_rentas.heading("Carro", text="Carro", anchor=tk.W)
tree_rentas.heading("ComienzoRenta", text="Comienzo Renta", anchor=tk.W)
tree_rentas.heading("FinalRenta", text="Final Renta", anchor=tk.W)
tree_rentas.heading("CostoTotal", text="Costo Total", anchor=tk.W)
tree_rentas.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

# Formulario de Rentas
frame_rentas = tk.Frame(tab_rentas, padx=20, pady=20)
frame_rentas.pack(pady=10, fill=tk.X)

tk.Label(frame_rentas, text="ID Usuario", font=("Helvetica", 12)).grid(
    row=0, column=0, sticky=tk.W, padx=10
)
combo_usuario = ttk.Combobox(frame_rentas, font=("Helvetica", 12))
combo_usuario.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame_rentas, text="ID Carro", font=("Helvetica", 12)).grid(
    row=1, column=0, sticky=tk.W, padx=10
)
combo_carro = ttk.Combobox(frame_rentas, font=("Helvetica", 12))
combo_carro.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame_rentas, text="Comienzo Renta", font=("Helvetica", 12)).grid(
    row=2, column=0, sticky=tk.W, padx=10
)
entry_comienzo_renta = tk.Entry(frame_rentas, font=("Helvetica", 12))
entry_comienzo_renta.grid(row=2, column=1, padx=10, pady=5)

tk.Label(frame_rentas, text="Final Renta", font=("Helvetica", 12)).grid(
    row=3, column=0, sticky=tk.W, padx=10
)
entry_final_renta = tk.Entry(frame_rentas, font=("Helvetica", 12))
entry_final_renta.grid(row=3, column=1, padx=10, pady=5)

tk.Label(frame_rentas, text="Costo Total", font=("Helvetica", 12)).grid(
    row=4, column=0, sticky=tk.W, padx=10
)
entry_costo_total = tk.Entry(frame_rentas, font=("Helvetica", 12))
entry_costo_total.grid(row=4, column=1, padx=10, pady=5)

btn_add_renta = tk.Button(
    frame_rentas,
    text="Agregar",
    command=lambda: add_renta(
        combo_usuario.get(),
        combo_carro.get(),
        entry_comienzo_renta.get(),
        entry_final_renta.get(),
        entry_costo_total.get(),
    ),
)
btn_add_renta.grid(row=5, column=0, padx=10)

btn_clear_rentas = tk.Button(
    frame_rentas,
    text="Limpiar",
    command=lambda: [
        combo_usuario.set(""),
        combo_carro.set(""),
        entry_comienzo_renta.delete(0, tk.END),
        entry_final_renta.delete(0, tk.END),
        entry_costo_total.delete(0, tk.END),
    ],
)
btn_clear_rentas.grid(row=5, column=1, padx=10)

btn_end_renta = tk.Button(
    frame_rentas,
    text="Finalizar Renta",
    command=lambda: end_renta(selected_renta_id, entry_final_renta.get()),
)
btn_end_renta.grid(row=6, column=0, padx=10)

refresh_carros()
refresh_usuarios()
refresh_rentas()


# Actualizar los comboboxes
def update_comboboxes():
    usuarios = fetch_usuarios()
    carros = fetch_carros()

    combo_usuario["values"] = [
        u[0] for u in usuarios
    ]  # Asume que el ID está en la primera columna
    combo_carro["values"] = [
        c[0] for c in carros
    ]  # Asume que el ID está en la primera columna


update_comboboxes()

# Ejecutar la aplicación
root.mainloop()
