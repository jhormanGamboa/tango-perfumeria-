import tkinter as tk
from tkinter import messagebox
from Registro import vista_formulario
from iniciar_secion import vista_formulario
from catalogo import App  # Asegúrate de que el archivo de la vista del catálogo esté nombrado correctamente
from modelo import modelo

class Controlador:
    def __init__(self, root):
        self.modelo = modelo()
        self.root = root
        self.vista_login = vista_login()
        self.vista_formulario = vista_formulario()
        self.catalogo = None

        # Configura las vistas
        self.setup_vistas()

    def setup_vistas(self):
        # Configura la vista de inicio de sesión
        self.vista_login.crear_ventana()
        self.vista_login.iniciar()

        # Establece el comando para el botón de inicio de sesión
        self.vista_login.set_login_command(self.iniciar_sesion)

        # Configura la vista de registro
        self.vista_formulario.crear_ventana()
        self.vista_formulario.iniciar()

        # Establece el comando para el botón de registro
        self.vista_formulario.set_register_command(self.registrar_usuario)

    def iniciar_sesion(self):
        correo = self.vista_login.get_correo()
        contraseña = self.vista_login.get_contraseña()

        if self.validar_usuario(correo, contraseña):
            self.vista_login.ventana.destroy()  # Cierra la ventana de inicio de sesión
            self.catalogo = App(self.root)
            self.catalogo.show_products()  # Muestra los productos en la vista del catálogo
        else:
            messagebox.showerror("Error", "Correo o contraseña incorrectos.")

    def validar_usuario(self, correo, contraseña):
        # Aquí puedes agregar la lógica para validar el usuario desde la base de datos
        try:
            con = self.modelo.conectar()
            cursor = con.cursor()
            cursor.execute("SELECT * FROM `registrar usuario` WHERE correo = %s AND contraseña = %s", (correo, contraseña))
            user = cursor.fetchone()
            con.close()
            return user is not None
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al conectar con la base de datos: {err}")
            return False

    def registrar_usuario(self):
        nombrec = self.vista_formulario.get_nombrec()
        correo = self.vista_formulario.get_correo()
        contraseña = self.vista_formulario.get_contraseña()

        if self.validar_registro(nombrec, correo, contraseña):
            self.vista_formulario.enviar_datos()
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

    def validar_registro(self, nombrec, correo, contraseña):
        return nombrec and correo and contraseña

if __name__ == "__main__":
    root = tk.Tk()
    controlador = Controlador(root)
    root.mainloop()
