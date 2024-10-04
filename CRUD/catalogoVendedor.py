import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from PIL import Image, ImageTk
import mysql.connector
import io

try:
    from PIL import Image, ImageTk, Resampling
    RESAMPLING_METHOD = Resampling.LANCZOS
except ImportError:
    RESAMPLING_METHOD = Image.Resampling.LANCZOS

class App_ven:
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
        self.product_frame.place(x=180, y=100, width=700, height=800)
        self.show_products()

        
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
        tk.Button(self.nav_frame, text="Vender", command=self.sell_product, bg="#b9030f", fg="white",borderwidth=0, font=("Arial", 10, "bold")).place(x=790, y=30, width=150, height=40)

    def Botone_Categoria(self):
        tk.Label(self.category_frame, text="Categorías",fg="black", bg="#d4ddb1", font=("Arial Rounded MT Bold",15,"bold")).place(x=10, y=10)
        y_pos = 40
        for category in self.categories:
            tk.Radiobutton(self.category_frame, text=category, variable=self.current_category, value=category, bg="#d4ddb1", command=self.show_products).place(x=10, y=y_pos)
            y_pos += 30

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

        file4 = "CRUD\\IMG\\youtube.png"
        img4 = Image.open(file4)
        img4 = img4.resize((205, 150))
        self.img_tk4 = ImageTk.PhotoImage(img4)
        
        self.label_img4 = tk.Label(self.category_frame, image=self.img_tk4, bg="#d4ddb1")
        self.label_img4.place(x=-30, y=300)

      
       

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


   
