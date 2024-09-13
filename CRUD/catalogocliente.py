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

class App:
    def __init__(self, root):  
        self.root = root
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
        self.product_frame.place(x=180, y=100, width=750, height=400)
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

        self.conteiner2 = tk.Frame(self.main_frame, bg="black")
        self.conteiner2.place(x=784, y=80, width=2, height=900)

        self.conteiner = tk.Frame(self.main_frame, bg="black")
        self.conteiner.place(x=0, y=510, width=150, height=2)

        self.conteiner = tk.Frame(self.main_frame, bg="black")
        self.conteiner.place(x=0, y=380, width=150, height=2)

        self.conteiner = tk.Frame(self.main_frame, bg="black")
        self.conteiner.place(x=0, y=270, width=150, height=2)

        self.IMG_cargar()

    def conectar(self):
        conection = mysql.connector.connect(
            host="localhost",
            database="tango-perfumeria",
            user="root",
            password=""
        )
        return conection

    def load_categories(self):
        try:
            con = self.conectar()
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
        tk.Button(self.nav_frame, text="comprar", command=self.sell_product, bg="#b9030f", fg="white",borderwidth=0, font=("Arial", 10, "bold")).place(x=790, y=30, width=150, height=40)

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
            con = self.conectar()
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
            frame.place(x=col*205, y=row*20, width=180, height=210)

            imagen = Image.open(io.BytesIO(imagen_data))
            imagen = imagen.resize((100, 100), RESAMPLING_METHOD)
            imagen = ImageTk.PhotoImage(imagen)

            img_label = tk.Label(frame, image=imagen)
            img_label.image = imagen
            img_label.place(x=30, y=10)

            # Mostrar detalles del producto
            details = f"Nombre: {nombre}\nCodigo{code}\nCantidad: {cantidad}\nPrecio: ${precio}\nDescripción: {descripcion}"
            tk.Label(frame, text=details, anchor="w", justify="left").place(x=-1, y=120)

            col += 1
            if col > 2:
                col = 0
                row += 1
    def sell_product(self):
        product_code = simpledialog.askstring("Comprar Producto", "Código del Producto:")
        if product_code:
            try:
                con = self.conectar()
                cursor = con.cursor()
                cursor.execute("SELECT id, cantidad FROM productos WHERE codigo = %s", (product_code,))
                product = cursor.fetchone()

                if product:
                    product_id, cantidad_actual = product
                    quantity = simpledialog.askinteger("Comprar Producto", "Cantidad a vender:")

                    if quantity and quantity <= cantidad_actual:
                        cursor.execute("INSERT INTO ventas (producto_id, cantidad) VALUES (%s, %s)", (product_id, quantity))
                        cursor.execute("UPDATE productos SET cantidad = cantidad - %s WHERE id = %s", (quantity, product_id))
                        con.commit()

                        messagebox.showinfo("Éxito", "Compra registrada correctamente.")
                        self.show_products()
                    else:
                        messagebox.showwarning("Advertencia", "Cantidad inválida o insuficiente.")
                else:
                    messagebox.showerror("Error", "Producto no encontrado.")
                
                cursor.close()
                con.close()

            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al registrar la compra: {err}")

   
    
if __name__ == "__main__":
    root = tk.Tk()  
    app = App(root)  
    root.mainloop()