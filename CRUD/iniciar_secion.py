import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk,Image
import mysql.connector

class vista_formulario:
    def __init__(self):
        self.ventana = None

    def crear_ventana(self):
        self.ventana = tk.Tk()
        self.ventana.title("Ventana de Inicio")
        self.ventana.geometry("925x500+300+200")
        self.ventana.config(bg="#fff")
        self.ventana.resizable(False,False)
        
        self.contenedor = tk.Frame(self.ventana,width=350, height=350, bg="white")
        self.contenedor.place(x=480,y=70)

        texto = tk.Label(self.contenedor,text="Iniciar secion",fg="#b9030f", bg="white", font=("Microsoft YaHei UI Light",23,"bold"))
        texto.place(x=80,y=0)
        
        self.label_correo = tk.Label(self.contenedor,text="Correo Electronico:",bg="white",font=("Microsoft YaHei UI Light",11,"bold"))
        self.label_correo.place(x=60,y=60)
        self.entry_correo = tk.Entry(self.contenedor,width=35,fg="black",border=0,bg="white",font=("Microsoft YaHei UI Light",11))
        self.entry_correo.place(x=60,y=80)
        self.contenedor2 = tk.Frame(self.contenedor,width=295,height=2, bg="black")
        self.contenedor2.place(x=55,y=107)

        self.label_contraseña = tk.Label(self.contenedor,text="Contraseña:",bg="white",font=("Microsoft YaHei UI Light",11,"bold"))
        self.label_contraseña.place(x=60,y=149)
        self.entry_contraseña = tk.Entry(self.contenedor,width=35,show="*",fg="black",border=0,bg="white",font=("Microsoft YaHei UI Light",11))
        self.entry_contraseña.place(x=60,y=170)
        self.contenedor3 = tk.Frame(self.contenedor,width=295,height=2, bg="black")
        self.contenedor3.place(x=55,y=197)
        
        texto_registro = tk.Label(self.contenedor,text="Si no tienes cuenta registrate ",fg="black", bg="white", font=("Microsoft YaHei UI Light",10,"bold"))
        texto_registro.place(x=55,y=220)
        
        self.cargar_imagen()
        

    def crear_boton(self):
        self.boton_registrar = tk.Button(self.contenedor, text="AQUI", borderwidth=0, width=4,pady=7, bg="white", fg="#b9030f",font=("Microsoft YaHei UI Light",10,"bold"))
        self.boton_registrar.place(x=260,y=213)
        self.boton = tk.Button(self.contenedor, text="Iniciar sesion", command=self.Verificar,width=39,pady=7,bg="#b9030f",fg="white",border=0)
        self.boton.place(x=60,y=274)
    
    
    def cargar_imagen(self):
        file = "CRUD\\imagines\\tango logo.png"
        img = Image.open(file)
        img = img.resize((400, 400))
        self.img_tk = ImageTk.PhotoImage(img)
        self.label_img = tk.Label(self.ventana, image=self.img_tk)
        self.label_img.place(x=0, y=50)
        
        self.label_img = tk.Label(self.ventana, image=self.img_tk, bg="#d4ddb1", width=450, height=500)
        self.label_img.place(x=0, y=0)
    
    def Verificar(self):
        correo = self.entry_correo.get()
        contraseña = self.entry_contraseña.get()
        
        if correo and contraseña:
            try:
                con = self.conectar()
                cursor = con.cursor()

                consulta_verificacion = "SELECT * FROM `registrar usuario` WHERE `correo` = %s"
                cursor.execute(consulta_verificacion, (correo,))
                resultado = cursor.fetchone()

                if resultado:
                    consulta_sesion = "SELECT * FROM `iniciar sesion` WHERE `correo` = %s AND `contraseña` = %s"
                    cursor.execute(consulta_sesion, (correo, contraseña))
                    sesion_existente = cursor.fetchone()

                    if sesion_existente:
                        messagebox.showinfo("Información", "Iniciaste sesión correctamente.")
                    else:
                        messagebox.showerror("Error", "La contraseña es incorrecta.")
                else:
                    messagebox.showwarning("Advertencia", "El correo no está registrado. Por favor, regístrate primero.")

                cursor.close()
                con.close()

            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {err}")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

    def iniciar(self):
        self.ventana.mainloop()

objvista = vista_formulario()
objvista.crear_ventana()
objvista.crear_boton()
objvista.iniciar()