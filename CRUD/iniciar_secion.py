import tkinter as tk
from tkinter import messagebox
import mysql.connector

class vista_formulario:
    def __init__(self):
        self.ventana = None

    def crear_ventana(self):
        self.ventana = tk.Tk()
        self.ventana.title("Ventana de formulario")
        self.ventana.geometry("350x350")
        self.ventana.config(bg="white")
        
        self.contenedor = tk.Frame(self.ventana, bg="red")
        self.contenedor.place(relx=0.5, rely=0.5, anchor="center", width=200, height=200)
        
        self.label_correo = tk.Label(self.contenedor, text="Ingrese su correo : ", bg="#bbffd5")
        self.label_correo.pack(pady=5, padx=5, anchor='center')
        self.entry_correo = tk.Entry(self.contenedor)
        self.entry_correo.pack(pady=5, padx=5)
        
        self.label_contraseña = tk.Label(self.contenedor,text="Ingrese la contraseña: ", bg="#bbffd5")
        self.label_contraseña.pack(pady=5, padx=5, anchor='center')
        self.entry_contraseña = tk.Entry(self.contenedor)
        self.entry_contraseña.pack(pady=5,padx=5)

    def crear_boton(self):
        self.boton = tk.Button(self.contenedor, text="Enviar datos", command=self.enviar_datos)
        self.boton.pack(pady=10)
    
    def conectar(self):
        conection = mysql.connector.connect(
            host = "localhost",
            database = "iniciar sesion",
            user = "root",
            password = ""
        )
        return conection
    
    def enviar_datos(self):
        correo = self.entry_correo.get()
        contraseña = self.entry_contraseña.get()
        
        if correo and contraseña:
            try:
                con = self.conectar()
                cursor = con.cursor()
                query = "INSERT INTO Datos (correo, contraseña) VALUES (%s, %s)"
                cursor.execute(query, (correo, contraseña))

                con.commit()  
                cursor.close()
                con.close()

                messagebox.showinfo("Éxito", "Datos insertados correctamente.")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al insertar datos: {err}")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
    

    def iniciar(self):
        self.ventana.mainloop()

objvista = vista_formulario()
objvista.crear_ventana()
objvista.crear_boton()
aux=objvista.conectar()
objvista.iniciar()