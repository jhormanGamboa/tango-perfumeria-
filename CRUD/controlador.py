from iniciar_secion import vista_formulario
from Registro import vista_Registro
from modelo import modelo
from PIL import ImageTk, Image
import tkinter as tk

class controlador:
    def __init__(self, objmodelo, objvista_inicio, objvista_registro):
        self.objmodelo = objmodelo
        self.objvista_inicio = objvista_inicio
        self.objvista_registro = objvista_registro
    
    def crear_ventana_inicio(self):
        self.objvista_inicio.crear_ventana()
        self.objvista_inicio.crear_boton(self.crear_ventana_registro)
        self.cargar_imagen_inicio()
        self.objvista_inicio.iniciar()
        
    def cargar_imagen_inicio(self):
        file = "CRUD\\imagines\\tango logo.png"
        img = Image.open(file)
        img = img.resize((400, 400))
        self.img_tk = ImageTk.PhotoImage(img)
        self.objvista_inicio.cargar_imagen(self.img_tk)
    
    def cargar_imagen_registro(self):
        file2 = "CRUD/imagines/logo persona.png"
        img2 = Image.open(file2)
        img2 = img2.resize((200, 200))
        self.img_tk2 = ImageTk.PhotoImage(img2)
        self.objvista_registro.cargar_imagen(self.img_tk2)
    
    def crear_ventana_registro(self):
        self.objvista_registro.crear_ventana()
        self.objvista_registro.crear_boton()
        self.cargar_imagen_registro()
        self.objvista_registro.iniciar()

# Inicialización de los objetos
objmodelo = modelo()
objvista_inicio = vista_formulario()
objvista_registro = vista_Registro()
objcontrolador = controlador(objmodelo, objvista_inicio, objvista_registro)

# Configurar el botón de registro en la vista de inicio
objvista_inicio.crear_boton(objcontrolador.crear_ventana_registro)
objcontrolador.crear_ventana_inicio()
