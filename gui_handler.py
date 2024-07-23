# gui_handler.py

import tkinter as tk
from tkinter import ttk, messagebox
from database_handler import DatabaseHandler


class GUIHandler:
    def __init__(self, root):
        self.db_handler = DatabaseHandler()
        self.root = root
        self.setup_gui()

    def setup_gui(self):
        self.root.title("Gestión de Carros, Usuarios y Alquileres")
        self.root.geometry("1000x700")

        notebook = ttk.Notebook(self.root)
        notebook.pack(pady=10, fill=tk.BOTH, expand=True)

        self.tab_carros = tk.Frame(notebook)
        self.tab_usuarios = tk.Frame(notebook)
        self.tab_rentas = tk.Frame(notebook)

        notebook.add(self.tab_carros, text="Carros")
        notebook.add(self.tab_usuarios, text="Usuarios")
        notebook.add(self.tab_rentas, text="Rentas")

        self.setup_carros_tab()
        self.setup_usuarios_tab()
        self.setup_rentas_tab()
        self.update_comboboxes()

    def setup_carros_tab(self):
        self.tree_carros = ttk.Treeview(self.tab_carros)
        self.tree_carros["columns"] = ("ID", "Marca", "Modelo", "Placa", "Estado")
        self.tree_carros.column("#0", width=0, stretch=tk.NO)
        self.tree_carros.column("ID", anchor=tk.CENTER, width=50)
        self.tree_carros.column("Marca", anchor=tk.W, width=150)
        self.tree_carros.column("Modelo", anchor=tk.W, width=150)
        self.tree_carros.column("Placa", anchor=tk.W, width=150)
        self.tree_carros.column("Estado", anchor=tk.W, width=200)
        self.tree_carros.heading("#0", text="", anchor=tk.CENTER)
        self.tree_carros.heading("ID", text="ID", anchor=tk.CENTER)
        self.tree_carros.heading("Marca", text="Marca", anchor=tk.W)
        self.tree_carros.heading("Modelo", text="Modelo", anchor=tk.W)
        self.tree_carros.heading("Placa", text="Placa", anchor=tk.W)
        self.tree_carros.heading("Estado", text="Estado", anchor=tk.W)
        self.tree_carros.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        frame_carros = tk.Frame(self.tab_carros, padx=20, pady=20)
        frame_carros.pack(pady=10, fill=tk.X)

        tk.Label(frame_carros, text="ID", font=("Helvetica", 12)).grid(
            row=0, column=0, sticky=tk.W, padx=10
        )
        self.entry_id_carro = tk.Entry(frame_carros, font=("Helvetica", 12))
        self.entry_id_carro.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame_carros, text="Marca", font=("Helvetica", 12)).grid(
            row=1, column=0, sticky=tk.W, padx=10
        )
        self.entry_marca = tk.Entry(frame_carros, font=("Helvetica", 12))
        self.entry_marca.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(frame_carros, text="Modelo", font=("Helvetica", 12)).grid(
            row=2, column=0, sticky=tk.W, padx=10
        )
        self.entry_modelo = tk.Entry(frame_carros, font=("Helvetica", 12))
        self.entry_modelo.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(frame_carros, text="Placa", font=("Helvetica", 12)).grid(
            row=3, column=0, sticky=tk.W, padx=10
        )
        self.entry_placa = tk.Entry(frame_carros, font=("Helvetica", 12))
        self.entry_placa.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(frame_carros, text="Estado", font=("Helvetica", 12)).grid(
            row=4, column=0, sticky=tk.W, padx=10
        )
        self.combo_estado = ttk.Combobox(
            frame_carros,
            values=["disponible", "no disponible", "fuera de servicio"],
            font=("Helvetica", 12),
        )
        self.combo_estado.grid(row=4, column=1, padx=10, pady=5)

        tk.Button(frame_carros, text="Agregar", command=self.add_carro).grid(
            row=5, column=0, padx=10
        )
        tk.Button(frame_carros, text="Actualizar", command=self.update_carro).grid(
            row=5, column=1, padx=10
        )
        tk.Button(frame_carros, text="Limpiar", command=self.clear_carros).grid(
            row=5, column=2, padx=10
        )

        self.refresh_carros()

    def setup_usuarios_tab(self):
        self.tree_usuarios = ttk.Treeview(self.tab_usuarios)
        self.tree_usuarios["columns"] = (
            "ID",
            "Username",
            "Email",
            "Nombre",
            "Apellido",
        )
        self.tree_usuarios.column("#0", width=0, stretch=tk.NO)
        self.tree_usuarios.column("ID", anchor=tk.CENTER, width=50)
        self.tree_usuarios.column("Username", anchor=tk.W, width=150)
        self.tree_usuarios.column("Email", anchor=tk.W, width=150)
        self.tree_usuarios.column("Nombre", anchor=tk.W, width=150)
        self.tree_usuarios.column("Apellido", anchor=tk.W, width=150)
        self.tree_usuarios.heading("#0", text="", anchor=tk.CENTER)
        self.tree_usuarios.heading("ID", text="ID", anchor=tk.CENTER)
        self.tree_usuarios.heading("Username", text="Username", anchor=tk.W)
        self.tree_usuarios.heading("Email", text="Email", anchor=tk.W)
        self.tree_usuarios.heading("Nombre", text="Nombre", anchor=tk.W)
        self.tree_usuarios.heading("Apellido", text="Apellido", anchor=tk.W)
        self.tree_usuarios.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        frame_usuarios = tk.Frame(self.tab_usuarios, padx=20, pady=20)
        frame_usuarios.pack(pady=10, fill=tk.X)

        tk.Label(frame_usuarios, text="Username", font=("Helvetica", 12)).grid(
            row=0, column=0, sticky=tk.W, padx=10
        )
        self.entry_username = tk.Entry(frame_usuarios, font=("Helvetica", 12))
        self.entry_username.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame_usuarios, text="Password", font=("Helvetica", 12)).grid(
            row=1, column=0, sticky=tk.W, padx=10
        )
        self.entry_password = tk.Entry(frame_usuarios, font=("Helvetica", 12), show="*")
        self.entry_password.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(frame_usuarios, text="Email", font=("Helvetica", 12)).grid(
            row=2, column=0, sticky=tk.W, padx=10
        )
        self.entry_email = tk.Entry(frame_usuarios, font=("Helvetica", 12))
        self.entry_email.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(frame_usuarios, text="Nombre", font=("Helvetica", 12)).grid(
            row=3, column=0, sticky=tk.W, padx=10
        )
        self.entry_nombre = tk.Entry(frame_usuarios, font=("Helvetica", 12))
        self.entry_nombre.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(frame_usuarios, text="Apellido", font=("Helvetica", 12)).grid(
            row=4, column=0, sticky=tk.W, padx=10
        )
        self.entry_apellido = tk.Entry(frame_usuarios, font=("Helvetica", 12))
        self.entry_apellido.grid(row=4, column=1, padx=10, pady=5)

        tk.Button(frame_usuarios, text="Agregar", command=self.add_usuario).grid(
            row=5, column=0, padx=10
        )
        tk.Button(frame_usuarios, text="Limpiar", command=self.clear_usuarios).grid(
            row=5, column=1, padx=10
        )

        self.refresh_usuarios()

    def setup_rentas_tab(self):
        self.tree_rentas = ttk.Treeview(self.tab_rentas)
        self.tree_rentas["columns"] = (
            "ID",
            "Usuario",
            "Carro",
            "ComienzoRenta",
            "FinalRenta",
            "CostoTotal",
        )
        self.tree_rentas.column("#0", width=0, stretch=tk.NO)
        self.tree_rentas.column("ID", anchor=tk.CENTER, width=50)
        self.tree_rentas.column("Usuario", anchor=tk.W, width=150)
        self.tree_rentas.column("Carro", anchor=tk.W, width=150)
        self.tree_rentas.column("ComienzoRenta", anchor=tk.W, width=150)
        self.tree_rentas.column("FinalRenta", anchor=tk.W, width=150)
        self.tree_rentas.column("CostoTotal", anchor=tk.W, width=150)
        self.tree_rentas.heading("#0", text="", anchor=tk.CENTER)
        self.tree_rentas.heading("ID", text="ID", anchor=tk.CENTER)
        self.tree_rentas.heading("Usuario", text="Usuario", anchor=tk.W)
        self.tree_rentas.heading("Carro", text="Carro", anchor=tk.W)
        self.tree_rentas.heading("ComienzoRenta", text="Comienzo Renta", anchor=tk.W)
        self.tree_rentas.heading("FinalRenta", text="Final Renta", anchor=tk.W)
        self.tree_rentas.heading("CostoTotal", text="Costo Total", anchor=tk.W)
        self.tree_rentas.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        frame_rentas = tk.Frame(self.tab_rentas, padx=20, pady=20)
        frame_rentas.pack(pady=10, fill=tk.X)

        tk.Label(frame_rentas, text="ID Usuario", font=("Helvetica", 12)).grid(
            row=0, column=0, sticky=tk.W, padx=10
        )
        self.combo_usuario = ttk.Combobox(frame_rentas, font=("Helvetica", 12))
        self.combo_usuario.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame_rentas, text="ID Carro", font=("Helvetica", 12)).grid(
            row=1, column=0, sticky=tk.W, padx=10
        )
        self.combo_carro = ttk.Combobox(frame_rentas, font=("Helvetica", 12))
        self.combo_carro.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(frame_rentas, text="Comienzo Renta", font=("Helvetica", 12)).grid(
            row=2, column=0, sticky=tk.W, padx=10
        )
        self.entry_comienzo_renta = tk.Entry(frame_rentas, font=("Helvetica", 12))
        self.entry_comienzo_renta.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(frame_rentas, text="Final Renta", font=("Helvetica", 12)).grid(
            row=3, column=0, sticky=tk.W, padx=10
        )
        self.entry_final_renta = tk.Entry(frame_rentas, font=("Helvetica", 12))
        self.entry_final_renta.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(frame_rentas, text="Costo Total", font=("Helvetica", 12)).grid(
            row=4, column=0, sticky=tk.W, padx=10
        )
        self.entry_costo_total = tk.Entry(frame_rentas, font=("Helvetica", 12))
        self.entry_costo_total.grid(row=4, column=1, padx=10, pady=5)

        tk.Button(frame_rentas, text="Agregar", command=self.add_renta).grid(
            row=5, column=0, padx=10
        )
        tk.Button(frame_rentas, text="Limpiar", command=self.clear_rentas).grid(
            row=5, column=1, padx=10
        )
        tk.Button(frame_rentas, text="Finalizar Renta", command=self.end_renta).grid(
            row=6, column=0, padx=10
        )

        self.refresh_rentas()

    def add_carro(self):
        if self.db_handler.add_carro(
            self.entry_marca.get(),
            self.entry_modelo.get(),
            self.entry_placa.get(),
            self.combo_estado.get(),
        ):
            messagebox.showinfo("Éxito", "Carro agregado exitosamente")
            self.refresh_carros()
        else:
            messagebox.showerror("Error", "Error al agregar carro")

    def add_usuario(self):
        if self.db_handler.add_usuario(
            self.entry_username.get(),
            self.entry_password.get(),
            self.entry_email.get(),
            self.entry_nombre.get(),
            self.entry_apellido.get(),
        ):
            messagebox.showinfo("Éxito", "Usuario agregado exitosamente")
            self.refresh_usuarios()
        else:
            messagebox.showerror("Error", "Error al agregar usuario")

    def add_renta(self):
        if self.db_handler.add_renta(
            self.combo_usuario.get(),
            self.combo_carro.get(),
            self.entry_comienzo_renta.get(),
            self.entry_final_renta.get(),
            self.entry_costo_total.get(),
        ):
            messagebox.showinfo("Éxito", "Renta registrada exitosamente")
            self.refresh_rentas()
        else:
            messagebox.showerror("Error", "Error al agregar renta")

    def end_renta(self):
        selected_item = self.tree_rentas.selection()[0]
        selected_renta_id = self.tree_rentas.item(selected_item, "values")[0]
        if self.db_handler.end_renta(selected_renta_id, self.entry_final_renta.get()):
            messagebox.showinfo("Éxito", "Renta finalizada exitosamente")
            self.refresh_rentas()
        else:
            messagebox.showerror("Error", "Error al finalizar renta")

    def update_carro(self):
        if self.db_handler.update_carro(
            self.entry_id_carro.get(),
            self.entry_marca.get(),
            self.entry_modelo.get(),
            self.entry_placa.get(),
            self.combo_estado.get(),
        ):
            messagebox.showinfo("Éxito", "Carro actualizado exitosamente")
            self.refresh_carros()
        else:
            messagebox.showerror("Error", "Error al actualizar carro")

    def clear_carros(self):
        self.entry_id_carro.delete(0, tk.END)
        self.entry_marca.delete(0, tk.END)
        self.entry_modelo.delete(0, tk.END)
        self.entry_placa.delete(0, tk.END)
        self.combo_estado.set("")

    def clear_usuarios(self):
        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_apellido.delete(0, tk.END)

    def clear_rentas(self):
        self.combo_usuario.set("")
        self.combo_carro.set("")
        self.entry_comienzo_renta.delete(0, tk.END)
        self.entry_final_renta.delete(0, tk.END)
        self.entry_costo_total.delete(0, tk.END)

    def refresh_carros(self):
        for item in self.tree_carros.get_children():
            self.tree_carros.delete(item)
        rows = self.db_handler.fetch_carros()
        for row in rows:
            self.tree_carros.insert("", tk.END, values=row)

    def refresh_usuarios(self):
        for item in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(item)
        rows = self.db_handler.fetch_usuarios()
        for row in rows:
            self.tree_usuarios.insert("", tk.END, values=row)

    def refresh_rentas(self):
        for item in self.tree_rentas.get_children():
            self.tree_rentas.delete(item)
        rows = self.db_handler.fetch_rentas()
        for row in rows:
            self.tree_rentas.insert("", tk.END, values=row)

    def update_comboboxes(self):
        usuarios = self.db_handler.fetch_usuarios()
        carros = self.db_handler.fetch_carros()

        self.combo_usuario["values"] = [
            u[0] for u in usuarios
        ]  # Asume que el ID está en la primera columna
        self.combo_carro["values"] = [
            c[0] for c in carros
        ]  # Asume que el ID está en la primera columna
