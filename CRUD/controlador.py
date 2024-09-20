from iniciar_secion import vista_formulario
from Registro import vista_Registro
from modelo import modelo
from CatalogoAdministrador import App_ad
from catalogoVendedor import App_ven
from catalogocliente import App

import tkinter as tk

class controlador:
    def __init__(self, objmodelo, objvista_inicio, objvista_registro):
        self.objmodelo = objmodelo
        self.objvista_inicio = objvista_inicio
        self.objvista_registro = objvista_registro
    
    def crear_ventana_inicio(self):
        self.objvista_inicio.crear_ventana()
        self.objvista_inicio.crear_boton(self.crear_ventana_registro)
        self.objvista_inicio.crear_boton2()
        self.objvista_inicio.iniciar()
    
    def crear_ventana_registro(self):
        self.objvista_registro.crear_ventana()
        self.objvista_registro.crear_boton(self.registrar_usuario)  # Conecta el botón a registrar_usuario
        self.objvista_registro.iniciar()
    
    def registrar_usuario(self):
        # Obtener los datos de la vista de registro
        nombrec = self.objvista_registro.entry_nombrec.get()
        correoc = self.objvista_registro.entry_correoe.get()
        contraseñac = self.objvista_registro.entry_contraseñag.get()

        # Pasar los datos al modelo
        self.objmodelo.set_nombrec(nombrec)
        self.objmodelo.set_correo(correoc)
        self.objmodelo.set_contraseña(contraseñac)

        # Intentar conectar y enviar los datos a la base de datos a través del modelo
        try:
            con = self.objmodelo.conectar()
            cursor = con.cursor()
            query = "INSERT INTO `registrar usuario` (`correo`, `nombre completo`, `contraseña`) VALUES (%s, %s, %s)"
            cursor.execute(query, (correoc, nombrec, contraseñac))
            con.commit()
            cursor.close()
            con.close()
            tk.messagebox.showinfo("Éxito", "Datos insertados correctamente.")

            self.objvista_registro.ventana.destroy()
        except Exception as e:
            tk.messagebox.showerror("Error", f"No se pudo insertar el registro: {e}")

    
    def verificar_admin(self, correo, contraseña):
        try:
            con = self.objmodelo.conectar()
            cursor = con.cursor()
            query = "SELECT * FROM `registrar usuario` WHERE `correo` = %s AND `contraseña` = %s"
            cursor.execute(query, (correo, contraseña))
            resultado = cursor.fetchone()

            cursor.close()
            con.close()

            if resultado:
                if "@admin" in correo:
                    tk.messagebox.showinfo("Acceso concedido", "Bienvenido administrador.")
                    self.objvista_inicio.ventana.destroy()  
                    self.abrir_catalogo_admin()  
                elif "@vendedor" in correo:
                    tk.messagebox.showinfo("Acceso concedido", "Bienvenido vendedor.")
                    self.objvista_inicio.ventana.destroy()
                    self.abrir_catalogo_vendedor()
                elif "@gmail" in correo:
                    tk.messagebox.showinfo("Acceso concedido", "Bienvenido vendedor.")
                    self.objvista_inicio.ventana.destroy()
                    self.abrir_catalogo_vendedor()
                else:
                    tk.messagebox.showinfo("Acceso concedido", "Iniciaste sesión correctamente.")
            else:
                tk.messagebox.showerror("Acceso denegado", "Credenciales incorrectas o no tiene permisos adecuados.")
        except Exception as e:
            tk.messagebox.showerror("Error", f"No se pudo verificar el usuario: {e}")

    def abrir_catalogo_cliente(self):
        root = tk.Tk() 
        app = App(root)  
        root.mainloop()

    def abrir_catalogo_vendedor(self):
        root = tk.Tk() 
        app = App_ven(root,self.objmodelo)  
        root.mainloop()

    def abrir_catalogo_admin(self):
        root = tk.Tk() 
        app = App_ad(root,self.objmodelo)  
        root.mainloop()  

        
objmodelo = modelo()
objvista_inicio = vista_formulario(None)
objvista_registro = vista_Registro() 
objcontrolador = controlador(objmodelo, objvista_inicio, objvista_registro)
objvista_inicio.controlador = objcontrolador  
objcontrolador.crear_ventana_inicio()