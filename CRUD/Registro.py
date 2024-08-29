import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import mysql.connector

class vista_formulario:
    def __init__(self):
        self.ventana = None

    def crear_ventana(self):
        self.ventana = tk.Tk()
        self.ventana.title("Ventana de Registro")
        self.ventana.geometry("925x600")
        self.ventana.config(bg="#fff")
        self.ventana.resizable(False, False)
        
        self.contenedor = tk.Frame(self.ventana, bg="#fff")
        self.contenedor.pack(expand=True, fill=tk.BOTH)
        
        texto = tk.Label(self.contenedor, text="Registro de sesión", fg="#b9030f", bg="#fff", font=("Microsoft YaHei UI Light", 23, "bold"))
        texto.pack(pady=(20, 10))
        
        self.cargar_imagen()

        self.formulario = tk.Frame(self.contenedor, bg="white")
        self.formulario.pack(pady=10)
        
        self.nombrec_label = tk.Label(self.formulario, text="Nombre completo:", bg="white", font=("Microsoft YaHei UI Light", 11, "bold"))
        self.nombrec_label.grid(row=0, column=0, padx=20, pady=(10, 5))
        self.entry_nombrec = tk.Entry(self.formulario, width=35, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
        self.entry_nombrec.grid(row=0, column=1, padx=20, pady=(10, 5))

        self.contenedor5 = tk.Frame(self.formulario, width=295, height=2, bg="black")
        self.contenedor5.grid(row=1, column=1, padx=20, pady=(0, 10))

        self.label_correoe = tk.Label(self.formulario, text="Correo Electrónico:", bg="white", font=("Microsoft YaHei UI Light", 11, "bold"))
        self.label_correoe.grid(row=2, column=0, padx=20, pady=(10, 5))
        self.entry_correoe = tk.Entry(self.formulario, width=35, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
        self.entry_correoe.grid(row=2, column=1, padx=20, pady=(10, 5))

        self.contenedor2 = tk.Frame(self.formulario, width=295, height=2, bg="black")
        self.contenedor2.grid(row=3, column=1, padx=20, pady=(0, 10))

        self.label_contraseñag = tk.Label(self.formulario, text="Contraseña:", bg="white", font=("Microsoft YaHei UI Light", 11, "bold"))
        self.label_contraseñag.grid(row=4, column=0, padx=20, pady=(10, 5))
        self.entry_contraseñag = tk.Entry(self.formulario, width=35, show="*", fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
        self.entry_contraseñag.grid(row=4, column=1, padx=20, pady=(10, 5))

        self.contenedor3 = tk.Frame(self.formulario, width=295, height=2, bg="black")
        self.contenedor3.grid(row=5, column=1, padx=20, pady=(0, 20))

        self.crear_boton()

    def crear_boton(self):
        self.boton = tk.Button(self.contenedor, text="Registrar", command=self.enviar_datos, width=39, pady=7, bg="#b9030f", fg="white", border=0)
        self.boton.pack(pady=(10, 20))

    def cargar_imagen(self):
        file2 = "CRUD/imagines/logo persona.png"
        img2 = Image.open(file2)
        img2 = img2.resize((200, 200))
        self.img_tk2 = ImageTk.PhotoImage(img2)
        
        self.label_img = tk.Label(self.contenedor, image=self.img_tk2, bg="#fff")
        self.label_img.pack(pady=(0, 20))
    
    def conectar(self):
        conection = mysql.connector.connect(
            host="localhost",
            database="tango-perfumeria",
            user="root",
            password=""
        )
        return conection
    
    def enviar_datos(self):
        nombrec = self.entry_nombrec.get()
        correoc = self.entry_correoe.get()
        contraseñac = self.entry_contraseñag.get()

        if correoc and contraseñac:
            con = self.conectar()
            if con:
                try:
                    cursor = con.cursor()
                    query = "INSERT INTO `registrar usuario` (`correo`, `nombre completo`, `contraseña`) VALUES (%s, %s, %s) "
                    cursor.execute(query, (correoc, nombrec, contraseñac))

                    con.commit()
                    cursor.close()
                    con.close()

                    messagebox.showinfo("Éxito", "Datos insertados correctamente.")
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Error al insertar datos: {err}")
            else:
                messagebox.showerror("Error", "No se pudo establecer conexión con la base de datos.")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

    def iniciar(self):
        self.ventana.mainloop()

objvista = vista_formulario()
objvista.crear_ventana()
objvista.iniciar()
