import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from PIL import Image, ImageTk
import mysql.connector
import json
import io

try:
    from PIL import Image, ImageTk, Resampling
    RESAMPLING_METHOD = Resampling.LANCZOS
except ImportError:
    RESAMPLING_METHOD = Image.Resampling.LANCZOS

class App_ad:
    def __init__(self, root,modelo):  
        self.root = root
        self.modelo = modelo
        self.root.title("Catálogo de Productos")
        self.root.geometry("950x600")
        self.root.resizable(False, False)
        self.products = {}  
        self.sales = {}  
        self.categories = []
        self.current_category = tk.StringVar()

        # Configuración del frame principal
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.place(relwidth=1, relheight=1)

        # Barra de navegación (parte superior)
        self.nav_frame = tk.Frame(self.main_frame, bg="#d4ddb1")
        self.nav_frame.place(x=0,y=0, width=950, height=80)
        self.Botones_Navegacion()

        # Área de categorías (parte izquierda)
        self.category_frame = tk.Frame(self.main_frame, bg="#d4ddb1")
        self.category_frame.place(x=0, y=80, width=150, height=700)
        self.load_categories()  # Cargamos las categorías desde la base de datos
        self.Botone_Categoria()

        # Área de productos (parte central)
        self.product_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.product_frame.place(x=180, y=100, width=750, height=800)
        self.show_products()

        # Botones de Editar y Eliminar (parte derecha)
        self.edit_delete_frame = tk.Frame(self.main_frame, bg="#d4ddb1")
        self.edit_delete_frame.place(x=785, y=80, width=190, height=700)
        self.BotonesEdicion()

        # Botón de Salir (parte inferior derecha)
        self.exit_button = tk.Button(self.main_frame, text="Salir", command=self.root.quit, bg="#b9030f", fg="white", borderwidth=0)
        self.exit_button.place(x=815, y=530, width=100, height=40)

        # Ajustes para expandir el área de productos
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        text = tk.Label(self.nav_frame,text="Tango",fg="#b9030f", bg="#d4ddb1", font=("Arial Rounded MT Bold",23,"bold"))
        text.place(x=30,y=0)

        text1 = tk.Label(self.nav_frame,text="Perfumeria",fg="#b9030f", bg="#d4ddb1", font=("Arial Rounded MT Bold",23,"bold"))
        text1.place(x=60,y=40)

        text2 = tk.Label(self.category_frame,text="Videos",fg="black", bg="#d4ddb1", font=("Arial Rounded MT Bold",18,"bold"))
        text2.place(x=25,y=140)


        #contenedor linea
        self.conteiner = tk.Frame(self.main_frame, bg="black")
        self.conteiner.place(x=0, y=80, width=1000, height=2)

        self.conteiner1 = tk.Frame(self.main_frame, bg="black")
        self.conteiner1.place(x=150, y=80, width=2, height=900)

        self.conteiner2 = tk.Frame(self.main_frame, bg="black")
        self.conteiner2.place(x=784, y=80, width=2, height=900)

        self.conteiner = tk.Frame(self.main_frame, bg="black")
        self.conteiner.place(x=0, y=510, width=150, height=2)

        self.conteiner = tk.Frame(self.main_frame, bg="black")
        self.conteiner.place(x=0, y=380, width=150, height=2)

        self.conteiner = tk.Frame(self.main_frame, bg="black")
        self.conteiner.place(x=0, y=270, width=150, height=2)

        self.IMG_cargar()

    def load_categories(self):
        try:
            con = self.modelo.conectar()
            cursor = con.cursor()
            cursor.execute("SELECT nombre FROM categorias")
            categorias = cursor.fetchall()
            self.categories = [categoria[0] for categoria in categorias]
            if self.categories:
                self.current_category.set(self.categories[0])
            cursor.close()
            con.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al cargar categorías: {err}")

    def Botones_Navegacion(self):
        tk.Button(self.nav_frame, text="Registrar Nuevo Producto", command=self.Registar_Productos, bg="#b9030f", fg="white", borderwidth=0, font=("Arial", 8, "bold")).place(x=450, y=30, width=150, height=40)
        tk.Button(self.nav_frame, text="Generar Informe", command=self.generate_report, bg="#b9030f", fg="white", borderwidth=0, font=("Arial", 10, "bold")).place(x=620, y=30, width=150, height=40)
        tk.Button(self.nav_frame, text="Vender", command=self.sell_product, bg="#b9030f", fg="white",borderwidth=0, font=("Arial", 10, "bold")).place(x=790, y=30, width=150, height=40)

    def Botone_Categoria(self):
        tk.Label(self.category_frame, text="Categorías",fg="black", bg="#d4ddb1", font=("Arial Rounded MT Bold",15,"bold")).place(x=10, y=10)
        y_pos = 40
        for category in self.categories:
            tk.Radiobutton(self.category_frame, text=category, variable=self.current_category, value=category, bg="#d4ddb1", command=self.show_products).place(x=10, y=y_pos)
            y_pos += 30
        tk.Button(self.category_frame, text="Añadir Categoría", command=self.NuevaCategoria, bg="#b9030f", fg="white", borderwidth=0).place(x=0, y=100, width=150, height=40)
    
    def IMG_cargar(self):
        file2 = "CRUD\\IMG\\tango logo.png"
        img2 = Image.open(file2)
        img2 = img2.resize((90, 90))
        self.img_tk2 = ImageTk.PhotoImage(img2)
        
        self.label_img = tk.Label(self.nav_frame, image=self.img_tk2, bg="#d4ddb1")
        self.label_img.place(x=280, y=0)

        file3 = "CRUD\\IMG\\youtube.png"
        img3 = Image.open(file3)
        img3 = img3.resize((205, 150))
        self.img_tk3 = ImageTk.PhotoImage(img3)
        
        self.label_img3 = tk.Label(self.category_frame, image=self.img_tk3, bg="#d4ddb1")
        self.label_img3.place(x=-30, y=170)

        file7 = "CRUD\\IMG\\youtube.png"
        img7 = Image.open(file7)
        img7 = img7.resize((205, 150))
        self.img_tk7 = ImageTk.PhotoImage(img7)
        
        self.label_img9 = tk.Label(self.category_frame, image=self.img_tk3, bg="#d4ddb1")
        self.label_img9.place(x=-30, y=300)

        file5 = "CRUD\\IMG\\editar.png"
        img5 = Image.open(file5)
        img5 = img5.resize((25, 25))
        self.img_tk5 = ImageTk.PhotoImage(img5)
        
        self.label_img5 = tk.Label(self.edit_delete_frame, image=self.img_tk5, bg="#b9030f")
        self.label_img5.place(x=21, y=61)

        file6 = "CRUD\\IMG\\añadir.png"
        img6 = Image.open(file6)
        img6 = img6.resize((25, 25))
        self.img_tk6 = ImageTk.PhotoImage(img6)
        
        self.label_img6 = tk.Label(self.category_frame, image=self.img_tk6, bg="#b9030f")
        self.label_img6.place(x=0, y=105)

        file7 = "CRUD\\IMG\\eliminar.png"
        img7 = Image.open(file7)
        img7 = img7.resize((25, 25))
        self.img_tk7 = ImageTk.PhotoImage(img7)
        
        self.label_img7 = tk.Label(self.edit_delete_frame, image=self.img_tk7, bg="#b9030f")
        self.label_img7.place(x=20, y=101)


    def show_products(self):
        # Limpia el área de productos
        for widget in self.product_frame.winfo_children():
            widget.destroy()

        # Muestra los productos de la categoría seleccionada
        selected_category = self.current_category.get()
        try:
            con = self.modelo.conectar()
            cursor = con.cursor()
            cursor.execute("""
                SELECT productos.codigo, productos.nombre, productos.cantidad, productos.precio, productos.descripcion, productos.imagen 
                FROM productos 
                INNER JOIN categorias ON productos.categoria_id = categorias.id 
                WHERE categorias.nombre = %s
            """, (selected_category,))
            productos = cursor.fetchall()
            con.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al cargar productos: {err}")
            return

        row, col = 0, 0
        for producto in productos:
            code, nombre, cantidad, precio, descripcion, imagen_data = producto
            frame = tk.Frame(self.product_frame, bg="#ffffff", bd=2, relief="groove", padx=5, pady=5)
            frame.place(x=col*205, y=row*240, width=190, height=220)

            imagen = Image.open(io.BytesIO(imagen_data))
            imagen = imagen.resize((100, 100), RESAMPLING_METHOD)
            imagen = ImageTk.PhotoImage(imagen)

            img_label = tk.Label(frame, image=imagen)
            img_label.image = imagen
            img_label.place(x=30, y=10)

            # Mostrar detalles del producto
            details = f"Nombre: {nombre}\nCodigo:{code}\nCantidad: {cantidad}\nPrecio: ${precio}\nDescripción: {descripcion}"
            tk.Label(frame, text=details, anchor="w", justify="left").place(x=-1, y=120)

            col += 1
            if col > 2:
                col = 0
                row += 1

    def BotonesEdicion(self):
        tk.Label(self.edit_delete_frame, text="Editar/Eliminar", borderwidth=0,fg="black", bg="#d4ddb1", font=("Arial Rounded MT Bold",15,"bold")).place(x=3, y=10)
        tk.Button(self.edit_delete_frame, text="EDITAR", command=self.Editar_Productos, borderwidth=0, bg="#b9030f", fg="white", font=("Arial", 10, "bold")).place(x=18, y=60, width=130, height=30)
        tk.Button(self.edit_delete_frame, text="ELIMINAR", command=self.Eliminar_Productos, borderwidth=0, bg="#b9030f", fg="white", font=("Arial", 10, "bold")).place(x=18, y=100, width=130, height=30)

    def Registar_Productos(self):
        def select_image():
            file_path = filedialog.askopenfilename(title="Seleccionar Imagen", filetypes=[("Image files", "*.jpg *.png")])
            if file_path:
                original_img = Image.open(file_path)
                product_data['imagen'] = original_img
                img = original_img.resize((100, 100))
                img_tk = ImageTk.PhotoImage(img)
                product_image_label.config(image=img_tk)
                product_image_label.image = img_tk
            register_window.lift()  
            register_window.focus_force()

        def save_product():
            categoria = category_var.get()
            codigo = code_entry.get()
            nombre = name_entry.get()
            cantidad = quantity_entry.get()
            precio = price_entry.get()
            descripcion = description_entry.get()
            imagen = product_data.get('imagen')

            if not (categoria and codigo and nombre and cantidad and precio and descripcion and imagen):
                messagebox.showwarning("Advertencia", "Por favor, complete todos los campos y seleccione una imagen.")
                return

            try:
                con = self.modelo.conectar()
                cursor = con.cursor()
                cursor.execute("SELECT id FROM categorias WHERE nombre = %s", (categoria,))
                categoria_id = cursor.fetchone()[0]

                img_byte_arr = io.BytesIO()
                product_data['imagen'].save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()

                cursor.execute("""
                    INSERT INTO productos (categoria_id, codigo, nombre, cantidad, precio, descripcion, imagen) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (categoria_id, codigo, nombre, cantidad, precio, descripcion, img_byte_arr))
                con.commit()
                cursor.close()
                con.close()

                messagebox.showinfo("Éxito", f"Producto '{nombre}' registrado exitosamente.")
                register_window.destroy()
                self.show_products()

            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al guardar el producto: {err}")

        register_window = tk.Toplevel(self.root)
        register_window.title("Registrar Producto")
        register_window.geometry("400x470")
        register_window.config(bg="white")
        register_window.resizable(False, False)

        self.contenedor3 = tk.Frame(register_window, bg="#b9030f")
        self.contenedor3.place(x=0, y=0, width=500, height=60)
        self.conteiner21 = tk.Frame(register_window, bg="black")
        self.conteiner21.place(x=0, y=60, width=500, height=2)
        self.conteiner8 = tk.Frame(register_window, bg="black")
        self.conteiner8.place(x=30, y=148, width=320, height=2)
        self.conteiner4 = tk.Frame(register_window, bg="black")
        self.conteiner4.place(x=30, y=188, width=320, height=2)
        self.conteiner5 = tk.Frame(register_window, bg="black")
        self.conteiner5.place(x=30, y=228, width=320, height=2)
        self.conteiner6 = tk.Frame(register_window, bg="black")
        self.conteiner6.place(x=30, y=267, width=320, height=2)
        self.conteiner7 = tk.Frame(register_window, bg="black")
        self.conteiner7.place(x=30, y=308, width=320, height=2)
        
        

        tk.Label(self.contenedor3, text="Tango", borderwidth=0, fg="white", bg="#b9030f", font=("Arial Rounded MT Bold", 15, "bold")).place(x=0, y=0)
        tk.Label(self.contenedor3, text="Perfumeria", borderwidth=0, fg="white", bg="#b9030f", font=("Arial Rounded MT Bold", 15, "bold")).place(x=30, y=30)

        file4 = "CRUD\\IMG\\tango logo.png"
        img4 = Image.open(file4)
        img4 = img4.resize((60, 60))
        self.img_tk4 = ImageTk.PhotoImage(img4)
        self.label_img4 = tk.Label(self.contenedor3, image=self.img_tk4, bg="#b9030f")
        self.label_img4.place(x=300, y=0)

        tk.Label(register_window, text="Categoría:", fg="black", bg="white", font=("Microsoft YaHei UI Light", 11, "bold")).place(x=30, y=80)
        tk.Label(register_window, text="Código:", fg="black", bg="white", font=("Microsoft YaHei UI Light", 11, "bold")).place(x=30, y=120)
        tk.Label(register_window, text="Nombre:", fg="black", bg="white", font=("Microsoft YaHei UI Light", 11, "bold")).place(x=30, y=160)
        tk.Label(register_window, text="Cantidad:", fg="black", bg="white", font=("Microsoft YaHei UI Light", 11, "bold")).place(x=30, y=200)
        tk.Label(register_window, text="Precio:", fg="black", bg="white", font=("Microsoft YaHei UI Light", 11, "bold")).place(x=30, y=240)
        tk.Label(register_window, text="Descripción:", fg="black", bg="white", font=("Microsoft YaHei UI Light", 11, "bold")).place(x=30, y=280)
        tk.Label(register_window, text="Imagen:", fg="black", bg="white", font=("Microsoft YaHei UI Light", 11, "bold")).place(x=30, y=320)

        category_var = tk.StringVar(value=self.categories[0])
        tk.OptionMenu(register_window, category_var, *self.categories).place(x=130, y=80, width=200)
        code_entry = tk.Entry(register_window,border=0,font=("Microsoft YaHei UI Light",9))
        code_entry.place(x=101, y=128, width=200)
        name_entry = tk.Entry(register_window,border=0,font=("Microsoft YaHei UI Light",9))
        name_entry.place(x=103, y=167, width=200)
        quantity_entry = tk.Entry(register_window,border=0,font=("Microsoft YaHei UI Light",9))
        quantity_entry.place(x=105, y=208, width=200)
        price_entry = tk.Entry(register_window,border=0,font=("Microsoft YaHei UI Light",9))
        price_entry.place(x=93, y=245, width=200)
        description_entry = tk.Entry(register_window,border=0,font=("Microsoft YaHei UI Light",9))
        description_entry.place(x=125, y=287, width=200)

        product_image_label = tk.Label(register_window, text="Imagen", width=100, height=100, bg="white")
        product_image_label.place(x=130, y=320)
        tk.Button(register_window, text="Seleccionar Imagen", command=select_image, bg="#b9030f", fg="white", borderwidth=0).place(x=285, y=325)

        product_data = {}

        tk.Button(register_window, text="Registrar Producto", command=save_product, bg="#b9030f", fg="white", font=("Arial", 10, "bold"), borderwidth=0).place(x=130, y=420, width=150, height=30)
    
    def Editar_Productos(self):
        code_window = tk.Toplevel(self.root)
        code_window.title("Editar Producto")
        code_window.geometry("300x200")
        code_window.config(bg="white")
        code_window.resizable(False, False)

        self.contenedor = tk.Frame(code_window, bg="#b9030f")
        self.contenedor.place(x=0, y=0, width=300, height=60)
        self.conteiner = tk.Frame(code_window, bg="black")
        self.conteiner.place(x=0, y=60, width=300, height=2)
        self.conteiner0 = tk.Frame(code_window, bg="black")
        self.conteiner0.place(x=75, y=115, width=140, height=2)
        tk.Label(self.contenedor, text="Tango", borderwidth=0, fg="white", bg="#b9030f", font=("Arial Rounded MT Bold", 15, "bold")).place(x=0, y=0)
        tk.Label(self.contenedor, text="Perfumeria", borderwidth=0, fg="white", bg="#b9030f", font=("Arial Rounded MT Bold", 15, "bold")).place(x=30, y=30)
        tk.Label(code_window, text="Código del Producto:", borderwidth=0, fg="black", bg="white", font=("Microsoft YaHei UI Light", 11, "bold")).place(x=70, y=67)
        product_code_entry = tk.Entry(code_window, width=35, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
        product_code_entry.place(x=75, y=90)

        file2 = "CRUD\\IMG\\tango logo.png"
        img2 = Image.open(file2)
        img2 = img2.resize((60, 60))
        self.img_tk2 = ImageTk.PhotoImage(img2)
        self.label_img = tk.Label(self.contenedor, image=self.img_tk2, bg="#b9030f")
        self.label_img.place(x=180, y=0)

        def submit_code():
            product_code = product_code_entry.get()
            if not product_code:
                messagebox.showwarning("Advertencia", "Por favor, introduce el código del producto.")
                return

            try:
                con = self.modelo.conectar()
                cursor = con.cursor()

                cursor.execute("SELECT codigo, nombre, cantidad, precio, descripcion FROM productos WHERE codigo = %s", (product_code,))
                product = cursor.fetchone()

                if product:
                    codigo, nombre, cantidad, precio, descripcion = product

                    edit_window = tk.Toplevel(self.root)
                    edit_window.title(f"Editar {product_code}")
                    edit_window.geometry("300x300")
                    edit_window.config(bg="white")
                    edit_window.resizable(False, False)

                    self.contenedor = tk.Frame(edit_window, bg="#b9030f")
                    self.contenedor.place(x=0, y=0, width=300, height=60)
                    self.conteiner = tk.Frame(edit_window, bg="black")
                    self.conteiner.place(x=0, y=60, width=300, height=2)
                    self.conteiner0 = tk.Frame(edit_window, bg="black")
                    self.conteiner0.place(x=75, y=190, width=140, height=2)

                    tk.Label(self.contenedor, text="Tango", borderwidth=0, fg="white", bg="#b9030f", font=("Arial Rounded MT Bold", 15, "bold")).place(x=0, y=0)
                    tk.Label(self.contenedor, text="Perfumeria", borderwidth=0, fg="white", bg="#b9030f", font=("Arial Rounded MT Bold", 15, "bold")).place(x=30, y=30)
                    tk.Label(edit_window, text="Precio:", fg="black", bg="white", font=("Microsoft YaHei UI Light", 11, "bold")).place(x=10, y=80)
                    tk.Label(edit_window, text="Cantidad:", fg="black", bg="white", font=("Microsoft YaHei UI Light", 11, "bold")).place(x=10, y=120)
                    tk.Label(edit_window, text="Descripción:", fg="black", bg="white", font=("Microsoft YaHei UI Light", 11, "bold")).place(x=10, y=160)

                    price_entry = tk.Entry(edit_window, width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
                    price_entry.insert(0, precio)
                    price_entry.place(x=100, y=80)

                    quantity_entry = tk.Entry(edit_window, width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
                    quantity_entry.insert(0, cantidad)
                    quantity_entry.place(x=100, y=120)

                    description_entry = tk.Entry(edit_window, width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
                    description_entry.insert(0, descripcion)
                    description_entry.place(x=100, y=160)

                    def save_changes():
                        new_price = price_entry.get()
                        new_quantity = quantity_entry.get()
                        new_description = description_entry.get()

                        if new_price and new_quantity and new_description:
                            try:
                                con = self.modelo.conectar()
                                cursor = con.cursor()
                                cursor.execute("""
                                    UPDATE productos 
                                    SET precio = %s, cantidad = %s, descripcion = %s 
                                    WHERE codigo = %s
                               """, (new_price, new_quantity, new_description, product_code))
                                con.commit()
                                cursor.close()
                                con.close()

                                messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
                                edit_window.destroy()
                                self.show_products()

                            except mysql.connector.Error as err:
                                messagebox.showerror("Error", f"Error al actualizar el producto: {err}")
                        else:
                            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")

                    tk.Button(edit_window, text="Guardar Cambios", command=save_changes, borderwidth=0, bg="#b9030f", fg="white", font=("Arial", 10, "bold")).place(x=85, y=230, width=130, height=30)
                    code_window.destroy()

                else:
                    messagebox.showerror("Error", "Producto no encontrado.")
            finally:
                cursor.close()
                con.close()

        tk.Button(code_window, text="Aceptar", command=submit_code, borderwidth=0, bg="#b9030f", fg="white", font=("Arial", 10, "bold")).place(x=85, y=140, width=130, height=30)


    def Eliminar_Productos(self):
        eliminar_window = tk.Toplevel(self.root)
        eliminar_window.title("Eliminar Producto")
        eliminar_window.geometry("300x200")
        eliminar_window.config(bg="white")
        eliminar_window.resizable(False, False)

        self.contenedor = tk.Frame(eliminar_window, bg="#b9030f")
        self.contenedor.place(x=0, y=0, width=300, height=60)
        self.conteiner = tk.Frame(eliminar_window, bg="black")
        self.conteiner.place(x=0, y=60, width=300, height=2)
        self.conteiner0 = tk.Frame(eliminar_window, bg="black")
        self.conteiner0.place(x=75, y=115, width=140, height=2)

        tk.Label(self.contenedor, text="Tango", borderwidth=0, fg="white", bg="#b9030f", font=("Arial Rounded MT Bold", 15, "bold")).place(x=0, y=0)
        tk.Label(self.contenedor, text="Perfumeria", borderwidth=0, fg="white", bg="#b9030f", font=("Arial Rounded MT Bold", 15, "bold")).place(x=30, y=30)

        tk.Label(eliminar_window, text="Código del Producto:", borderwidth=0, fg="black", bg="white", font=("Microsoft YaHei UI Light", 11, "bold")).place(x=70, y=67)
        product_code_entry = tk.Entry(eliminar_window, width=35, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
        product_code_entry.place(x=75, y=90)


        file2 = "CRUD\\IMG\\tango logo.png"
        img2 = Image.open(file2)
        img2 = img2.resize((60, 60))
        self.img_tk2 = ImageTk.PhotoImage(img2)

        self.label_img = tk.Label(self.contenedor, image=self.img_tk2, bg="#b9030f")
        self.label_img.place(x=180, y=0)

        def submit_deletion():
            product_code = product_code_entry.get()
            if not product_code:
                messagebox.showwarning("Advertencia", "Por favor, introduce el código del producto.")
                return

            try:
                con = self.modelo.conectar()
                cursor = con.cursor()
                cursor.execute("DELETE FROM productos WHERE codigo = %s", (product_code,))
                con.commit()
                cursor.close()
                con.close()

                messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
                self.show_products()
                eliminar_window.destroy()

            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al eliminar el producto: {err}")
                if cursor:
                    cursor.close()
                if con:
                    con.close()

        tk.Button(eliminar_window, text="Eliminar", command=submit_deletion, borderwidth=0, bg="#b9030f", fg="white", font=("Arial", 10, "bold")).place(x=85, y=140, width=130, height=30)

    def sell_product(self):
        vender = tk.Toplevel(self.root)
        vender.title("Vender Producto")
        vender.geometry("300x200")
        vender.config(bg="white")
        vender.resizable(False, False)
    
        self.contenedor = tk.Frame(vender, bg="#b9030f")
        self.contenedor.place(x=0, y=0, width=300, height=60)
        self.conteiner = tk.Frame(vender, bg="black")
        self.conteiner.place(x=0, y=60, width=300, height=2)
        self.conteiner0 = tk.Frame(vender, bg="black")
        self.conteiner0.place(x=75, y=115, width=140, height=2)

        tk.Label(self.contenedor, text="Tango", borderwidth=0, fg="white", bg="#b9030f", font=("Arial Rounded MT Bold", 15, "bold")).place(x=0, y=0)
        tk.Label(self.contenedor, text="Perfumeria", borderwidth=0, fg="white", bg="#b9030f", font=("Arial Rounded MT Bold", 15, "bold")).place(x=30, y=30)

        tk.Label(vender, text="Código del Producto:", borderwidth=0, fg="black", bg="white", font=("Microsoft YaHei UI Light", 11, "bold")).place(x=70, y=67)
        code_entry = tk.Entry(vender, width=35, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
        code_entry.place(x=75, y=90)

        file2 = "CRUD\\IMG\\tango logo.png"
        img2 = Image.open(file2)
        img2 = img2.resize((60, 60))
        self.img_tk2 = ImageTk.PhotoImage(img2)

        self.label_img = tk.Label(self.contenedor, image=self.img_tk2, bg="#b9030f")
        self.label_img.place(x=180, y=0)

        def submit_code():
            product_code = code_entry.get()
            if not product_code:
                messagebox.showwarning("Advertencia", "Por favor, introduce el código del producto.")
                return
            try:
                con = self.modelo.conectar()
                cursor = con.cursor()
                cursor.execute("SELECT id, cantidad FROM productos WHERE codigo = %s", (product_code,))
                product = cursor.fetchone()

                if product:
                    product_id, cantidad_actual = product
                    vender.destroy()  
                    quantity_window = tk.Toplevel(self.root)
                    quantity_window.title("Vender Producto")
                    quantity_window.geometry("300x200")
                    quantity_window.config(bg="white")
                    quantity_window.resizable(False, False)

                    self.contenedor2 = tk.Frame(quantity_window, bg="#b9030f")
                    self.contenedor2.place(x=0, y=0, width=300, height=60)
                    self.conteiner2 = tk.Frame(quantity_window, bg="black")
                    self.conteiner2.place(x=0, y=60, width=300, height=2)
                    self.conteiner02 = tk.Frame(quantity_window, bg="black")
                    self.conteiner02.place(x=75, y=132, width=140, height=2)

                    tk.Label(self.contenedor2, text="Tango", borderwidth=0, fg="white", bg="#b9030f", font=("Arial Rounded MT Bold", 15, "bold")).place(x=0, y=0)
                    tk.Label(self.contenedor2, text="Perfumeria", borderwidth=0, fg="white", bg="#b9030f", font=("Arial Rounded MT Bold", 15, "bold")).place(x=30, y=30)

                    tk.Label(quantity_window, text=f"Cantidad disponible: {cantidad_actual}\nIngrese la cantidad a vender:", borderwidth=0, fg="black", bg="white", font=("Microsoft YaHei UI Light", 11, "bold")).place(x=30, y=70)
                    quantity_entry = tk.Entry(quantity_window, width=35, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
                    quantity_entry.place(x=75, y=110)

                    file3 = "CRUD\\IMG\\tango logo.png"
                    img3 = Image.open(file3)
                    img3 = img3.resize((60, 60))
                    self.img_tk3 = ImageTk.PhotoImage(img3)

                    self.label_img1 = tk.Label(self.contenedor2, image=self.img_tk3, bg="#b9030f")
                    self.label_img1.place(x=180, y=0)

                    def submit_quantity():
                        try:
                            quantity = int(quantity_entry.get())
                            if 0 < quantity <= cantidad_actual:
                                quantity_window.destroy()  
                                try:
                                    con = self.modelo.conectar()
                                    cursor = con.cursor()
                                    cursor.execute("INSERT INTO ventas (producto_id, cantidad) VALUES (%s, %s)", (product_id, quantity))
                                    cursor.execute("UPDATE productos SET cantidad = cantidad - %s WHERE id = %s", (quantity, product_id))
                                    con.commit()
                                    messagebox.showinfo("Éxito", "Venta registrada correctamente.")
                                    self.show_products()
                                except mysql.connector.Error as err:
                                    messagebox.showerror("Error", f"Error al registrar la venta: {err}")
                                finally:
                                    cursor.close()
                                    con.close()
                            else:
                                messagebox.showwarning("Advertencia", "Cantidad insuficiente o inválida.")
                        except ValueError:
                            messagebox.showerror("Error", "Por favor, introduce un número válido.")

                    tk.Button(quantity_window, text="Aceptar", command=submit_quantity, borderwidth=0, bg="#b9030f", fg="white", font=("Arial", 10, "bold")).place(x=85, y=150, width=130, height=30)
                else:
                    messagebox.showerror("Error", "Producto no encontrado.")
                    cursor.close()
                    con.close()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {err}")
                if cursor:
                    cursor.close()
                if con:
                    con.close()

        tk.Button(vender, text="Aceptar", command=submit_code, borderwidth=0, bg="#b9030f", fg="white", font=("Arial", 10, "bold")).place(x=78, y=140, width=130, height=30)

    def generate_report(self):
        report_window = tk.Toplevel(self.root)
        report_window.title("Informe de Ventas")
        report_window.geometry("400x600")
        report_window.config(bg="white")
        report_window.resizable(False, False)

        self.contenedor3 = tk.Frame(report_window, bg="#b9030f")
        self.contenedor3.place(x=0, y=0, width=400, height=60)

        tk.Label(self.contenedor3, text="Tango", borderwidth=0, fg="white", bg="#b9030f", font=("Arial Rounded MT Bold", 15, "bold")).place(x=0, y=0)
        tk.Label(self.contenedor3, text="Informe de Ventas", borderwidth=0, fg="white", bg="#b9030f", font=("Arial Rounded MT Bold", 15, "bold")).place(x=30, y=30)

        file4 = "CRUD\\IMG\\tango logo.png"
        img4 = Image.open(file4)
        img4 = img4.resize((60, 60))
        self.img_tk4 = ImageTk.PhotoImage(img4)
        self.label_img4 = tk.Label(self.contenedor3, image=self.img_tk4, bg="#b9030f")
        self.label_img4.place(x=300, y=0)

        self.conteiner21 = tk.Frame(report_window, bg="black")
        self.conteiner21.place(x=0, y=60, width=400, height=2)

        try:
            con = self.modelo.conectar()
            cursor = con.cursor()

            tk.Label(report_window, text="Productos Más Vendidos:", fg="black", bg="white", font=("Microsoft YaHei UI Light", 11, "bold")).place(x=30, y=80)
            self.conteiner8 = tk.Frame(report_window, bg="black")
            self.conteiner8.place(x=30, y=108, width=320, height=2)

            cursor.execute("""
                SELECT productos.nombre, SUM(ventas.cantidad) as total_vendido 
                FROM ventas 
                LEFT JOIN productos ON ventas.producto_id = productos.id 
                GROUP BY productos.nombre 
                HAVING total_vendido > 10
            """)    
            mas_vendidos = cursor.fetchall()
            y_position = 130 
            for producto in mas_vendidos:
                tk.Label(report_window, text=f"{producto[0]}: {producto[1]} unidades", fg="black", bg="white", font=("Microsoft YaHei UI Light", 9)).place(x=30, y=y_position)
                y_position += 30
            tk.Label(report_window, text="------------------------------", fg="black", bg="white", font=("Microsoft YaHei UI Light", 9)).place(x=30, y=y_position + 10)

            tk.Label(report_window, text="Productos Menos Vendidos:", fg="black", bg="white", font=("Microsoft YaHei UI Light", 11, "bold")).place(x=30, y=y_position + 40)
            self.conteiner9 = tk.Frame(report_window, bg="black")
            self.conteiner9.place(x=30, y=y_position + 68, width=320, height=2)

            cursor.execute("""
                SELECT productos.nombre, SUM(ventas.cantidad) as total_vendido 
                FROM ventas 
                LEFT JOIN productos ON ventas.producto_id = productos.id 
                GROUP BY productos.nombre 
                HAVING total_vendido > 0 AND total_vendido < 5
            """)
            menos_vendidos = cursor.fetchall()

            y_position += 90
            for producto in menos_vendidos:
                tk.Label(report_window, text=f"{producto[0]}: {producto[1]} unidades", fg="black", bg="white", font=("Microsoft YaHei UI Light", 9)).place(x=30, y=y_position)
                y_position += 30
            def export_report():
                file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
                if file_path:
                    with open(file_path, 'w') as file:
                        file.write("INFORME DE VENTAS\n\n")
                        file.write("---------------------------------------------------\n")
                        file.write("Productos Mas Vendidos:\n")
                        file.write("---------------------------------------------------\n\n")
                        for producto in mas_vendidos:
                            file.write(f"Producto: {producto[0]:<30} | Vendido: {producto[1]} unidades\n")
                        file.write("\n\n---------------------------------------------------\n")
                        file.write("Productos Menos Vendidos:\n")
                        file.write("---------------------------------------------------\n\n")
                        for producto in menos_vendidos:
                            file.write(f"Producto: {producto[0]:<30} | Vendido: {producto[1]} unidades\n")
                        file.write("\nFin del informe.\n")

                    messagebox.showinfo("Éxito", f"Informe guardado en {file_path}")
            tk.Button(report_window, text="Guardar Informe", command=export_report, bg="#b9030f", fg="white", font=("Arial", 10, "bold"), borderwidth=0).place(x=240, y=75, width=150, height=30)

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al generar el informe: {err}")

    def NuevaCategoria(self):
        new_category_window = tk.Toplevel(self.root)
        new_category_window.title("Nueva Categoría")
        new_category_window.geometry("300x200")
        new_category_window.config(bg="white")
        new_category_window.resizable(False, False)

        self.contenedor = tk.Frame(new_category_window, bg="#b9030f")
        self.contenedor.place(x=0, y=0, width=300, height=60)
        self.conteiner = tk.Frame(new_category_window, bg="black")
        self.conteiner.place(x=0, y=60, width=300, height=2)
        self.conteiner0 = tk.Frame(new_category_window, bg="black")
        self.conteiner0.place(x=75, y=115, width=140, height=2)

        tk.Label(self.contenedor, text="Tango", borderwidth=0, fg="white", bg="#b9030f", font=("Arial Rounded MT Bold", 15, "bold")).place(x=0, y=0)
        tk.Label(self.contenedor, text="Perfumeria", borderwidth=0, fg="white", bg="#b9030f", font=("Arial Rounded MT Bold", 15, "bold")).place(x=30, y=30)

        tk.Label(new_category_window, text="Nueva Categoría:", borderwidth=0, fg="black", bg="white", font=("Microsoft YaHei UI Light", 11, "bold")).place(x=70, y=67)
        category_entry = tk.Entry(new_category_window, width=35, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
        category_entry.place(x=75, y=90)

        file2 = "CRUD\\IMG\\tango logo.png"
        img2 = Image.open(file2)
        img2 = img2.resize((60, 60))
        self.img_tk2 = ImageTk.PhotoImage(img2)

        self.label_img = tk.Label(self.contenedor, image=self.img_tk2, bg="#b9030f")
        self.label_img.place(x=180, y=0)

        def submit_category():
            new_category = category_entry.get()
            if not new_category:
                messagebox.showwarning("Advertencia", "Por favor, introduce el nombre de la nueva categoría.")
                return
            try:
                con = self.modelo.conectar()
                cursor = con.cursor()
                cursor.execute("INSERT INTO categorias (nombre) VALUES (%s)", (new_category,))
                con.commit()
                cursor.close()
                con.close()

                self.categories.append(new_category)
                self.current_category.set(new_category)
                self.show_products()
                self.Botone_Categoria()
                messagebox.showinfo("Éxito", "Categoría creada correctamente.")
                new_category_window.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al guardar la categoría: {err}")
                if cursor:
                    cursor.close()
                if con:
                    con.close()
        tk.Button(new_category_window, text="Aceptar", command=submit_category, borderwidth=0, bg="#b9030f", fg="white", font=("Arial", 10, "bold")).place(x=85, y=140, width=130, height=30)