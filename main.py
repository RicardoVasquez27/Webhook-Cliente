import tkinter as tk
from tkinter import messagebox
import sqlite3
import requests

class RegistroPagoApp:
    SERVER_IP = "http://192.168.3.113:8000"

    def __init__(self, master):
        self.master = master
        master.title("Registro de Pago")
        # Crear widgets
        self.label_fecha = tk.Label(master, text="Fecha:")
        self.entry_fecha = tk.Entry(master)

        self.label_id_multa = tk.Label(master, text="ID Multa:")
        self.entry_id_multa = tk.Entry(master)

        self.boton_guardar = tk.Button(master, text="Guardar Pago", command=self.guardar_pago)

        # Colocar widgets en la ventana
        self.label_fecha.grid(row=0, column=0, padx=10, pady=10)
        self.entry_fecha.grid(row=0, column=1, padx=10, pady=10)
        self.label_id_multa.grid(row=1, column=0, padx=10, pady=10)
        self.entry_id_multa.grid(row=1, column=1, padx=10, pady=10)
        self.boton_guardar.grid(row=2, column=0, columnspan=2, pady=10)

        # Botón para ver multas
        self.boton_ver_multas = tk.Button(master, text="Ver Multas", command=self.obtener_multas)
        self.boton_ver_multas.grid(row=3, column=0, columnspan=2, pady=10)

    def guardar_pago(self):
        fecha = self.entry_fecha.get()
        id_multa = self.entry_id_multa.get()

        if not fecha or not id_multa:
            messagebox.showerror("Error", "Por favor, completa todos los campos.")
            return

        try:
            conexion = sqlite3.connect("Pagos.db")
            cursor = conexion.cursor()

            cursor.execute("INSERT INTO pagos (fecha, id_multa) VALUES (?, ?)", (fecha, id_multa))
            conexion.commit()

            id_pago = cursor.lastrowid
            conexion.close()

            self.enviar_a_servidor(id_multa)

            messagebox.showinfo("Éxito", f"Pago registrado con éxito. ID de pago: {id_pago}")

        except sqlite3.Error as sqle:
            messagebox.showerror("Error de SQLite", f"Error al registrar el pago: {str(sqle)}")

        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar el pago: {str(e)}")

    def enviar_a_servidor(self, id_multa):
        url_servidor = f"{self.SERVER_IP}/actualizar_estado/{id_multa}"

        try:
            response = requests.put(url_servidor)
            response.raise_for_status()

            print(f"ID_multa {id_multa} enviado al servidor con éxito.")

        except requests.exceptions.RequestException as err:
            self.mostrar_error("Error en la solicitud", str(err))

    def obtener_multas(self):
        url_servidor = f"{self.SERVER_IP}/tabla_multas"

        try:
            response = requests.get(url_servidor)
            response.raise_for_status()
            multas = response.json()

            self.mostrar_vista_multas(multas)

        except requests.exceptions.RequestException as err:
            self.mostrar_error("Error al obtener multas", str(err))

    def mostrar_vista_multas(self, multas):
        ventana_multas = tk.Toplevel(self.master)
        ventana_multas.title("Lista de Multas")

        texto_multas = tk.Text(ventana_multas, wrap=tk.WORD)
        texto_multas.grid(row=0, column=0, padx=10, pady=10)

        for multa in multas:
            texto_multas.insert(tk.END, f"ID Multa: {multa['id_multa']}\n"
                                        f"Placa: {multa['placa']}\n"
                                        f"Concepto Multa: {multa['concepto_multa']}\n"
                                        f"Estado: {multa['estado']}\n"
                                        f"Monto: {multa['monto']}\n\n")

    def mostrar_error(self, titulo, mensaje):
        messagebox.showerror(titulo, mensaje)

if __name__ == "__main__":
    ventana = tk.Tk()
    app = RegistroPagoApp(ventana)
    ventana.mainloop()
