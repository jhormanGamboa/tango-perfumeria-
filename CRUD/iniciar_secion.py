import tkinter as tk

class vista_formulario:
    def _init_(self):
        self.ventana = None

    def crear_ventana(self):
        self.ventana = tk.Tk()
        self.ventana.title("Ventana de formulario")
        self.ventana.geometry("350x350")
        self.ventana.config(bg="white")
        
        self.contenedor = tk.Frame(self.ventana, bg="red")
        self.contenedor.place(relx=0.5, rely=0.5, anchor="center", width=200, height=200)
        
        self.label_usuario = tk.Label(self.contenedor, text="Ingrese su nombre: ", bg="#bbffd5")
        self.label_usuario.pack(pady=5, padx=5, anchor='center')
        self.entry_usuario = tk.Entry(self.contenedor)
        self.entry_usuario.pack(pady=5, padx=5)
        
        self.label_contraseña = tk.Label(self.contenedor,text="Ingrese el apellido: ", bg="#bbffd5")
        self.label_contraseña.pack(pady=5, padx=5, anchor='center')
        self.entry_contraseña = tk.Entry(self.contenedor)
        self.entry_contraseña.pack(pady=5,padx=5)

    def crear_boton(self):
        self.boton = tk.Button(self.contenedor, text="Enviar datos")
        self.boton.pack(pady=10)

    def iniciar(self):
        self.ventana.mainloop()

objvista = vista_formulario()
objvista.crear_ventana()
objvista.crear_boton()
objvista.iniciar()