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

        file4 = "CRUD\\IMG\\youtube.png"
        img4 = Image.open(file4)
        img4 = img4.resize((205, 150))
        self.img_tk4 = ImageTk.PhotoImage(img4)
        
        self.label_img4 = tk.Label(self.category_frame, image=self.img_tk4, bg="#d4ddb1")
        self.label_img4.place(x=-30, y=300)

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
                img = original_img.resize((100, 100), RESAMPLING_METHOD)
                img_tk = ImageTk.PhotoImage(img)
                product_image_label.config(image=img_tk)
                product_image_label.image = img_tk


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
                con = self.conectar()
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

        # Ventana para registrar producto
        register_window = tk.Toplevel(self.root)
        register_window.title("Registrar Producto")
        register_window.geometry("400x400")
        register_window.resizable(False, False)

        # Configuración de la ventana de registro
        tk.Label(register_window, text="Categoría:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Label(register_window, text="Código:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Label(register_window, text="Nombre:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        tk.Label(register_window, text="Cantidad:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        tk.Label(register_window, text="Precio:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        tk.Label(register_window, text="Descripción:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        tk.Label(register_window, text="Imagen:").grid(row=6, column=0, padx=5, pady=5, sticky="e")

        category_var = tk.StringVar(value=self.categories[0])
        tk.OptionMenu(register_window, category_var, *self.categories).grid(row=0, column=1, padx=5, pady=5)
        code_entry = tk.Entry(register_window)
        code_entry.grid(row=1, column=1, padx=5, pady=5)
        name_entry = tk.Entry(register_window)
        name_entry.grid(row=2, column=1, padx=5, pady=5)
        quantity_entry = tk.Entry(register_window)
        quantity_entry.grid(row=3, column=1, padx=5, pady=5)
        price_entry = tk.Entry(register_window)
        price_entry.grid(row=4, column=1, padx=5, pady=5)
        description_entry = tk.Entry(register_window)
        description_entry.grid(row=5, column=1, padx=5, pady=5)

        product_image_label = tk.Label(register_window, text="Imagen", width=10, height=10, bg="#d4ddb1")
        product_image_label.grid(row=6, column=1, padx=5, pady=5)
        tk.Button(register_window, text="Seleccionar Imagen", command=select_image).grid(row=6, column=2, padx=5, pady=5)

        product_data = {}

        # Botón "Registrar Producto" dentro de la ventana de registro
        tk.Button(register_window, text="Registrar Producto", command=save_product, bg="#b9030f", fg="white").grid(row=7, column=0, columnspan=3, pady=10)

    def Editar_Productos(self):
        product_code = simpledialog.askstring("Editar Producto", "Código del Producto:")
        if product_code:
            try:
                con = self.conectar()
                cursor = con.cursor()
                cursor.execute("SELECT codigo, nombre, cantidad, precio, descripcion FROM productos WHERE codigo = %s", (product_code,))
                product = cursor.fetchone()
                cursor.close()
                con.close()

                if product:
                    codigo, nombre, cantidad, precio, descripcion = product

                    edit_window = tk.Toplevel(self.root)
                    edit_window.title(f"Editar {product_code}")
                    edit_window.geometry("300x200")
                    edit_window.resizable(False, False)

                    tk.Label(edit_window, text="Precio:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
                    tk.Label(edit_window, text="Cantidad:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
                    tk.Label(edit_window, text="Descripción:").grid(row=2, column=0, padx=5, pady=5, sticky="e")

                    price_entry = tk.Entry(edit_window)
                    price_entry.insert(0, precio)
                    price_entry.grid(row=0, column=1, padx=5, pady=5)
                    quantity_entry = tk.Entry(edit_window)
                    quantity_entry.insert(0, cantidad)
                    quantity_entry.grid(row=1, column=1, padx=5, pady=5)
                    description_entry = tk.Entry(edit_window)
                    description_entry.insert(0, descripcion)
                    description_entry.grid(row=2, column=1, padx=5, pady=5)

                    def save_changes():
                        new_price = price_entry.get()
                        new_quantity = quantity_entry.get()
                        new_description = description_entry.get()

                        if new_price and new_quantity and new_description:
                            try:
                                con = self.conectar()
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

                    tk.Button(edit_window, text="Guardar Cambios", command=save_changes, bg="#b9030f", fg="white").grid(row=3, column=0, columnspan=2, pady=10)
                else:
                    messagebox.showerror("Error", "Producto no encontrado.")

            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al conectar a la base de datos: {err}")

    def Eliminar_Productos(self):
        product_code = simpledialog.askstring("Eliminar Producto", "Código del Producto:")
        if product_code:
            try:
                con = self.conectar()
                cursor = con.cursor()
                cursor.execute("DELETE FROM productos WHERE codigo = %s", (product_code,))
                con.commit()
                cursor.close()
                con.close()

                messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
                self.show_products()

            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al eliminar el producto: {err}")
        else:
            messagebox.showerror("Error", "Producto no encontrado.")

    def sell_product(self):
        product_code = simpledialog.askstring("Vender Producto", "Código del Producto:")
        if product_code:
            try:
                con = self.conectar()
                cursor = con.cursor()
                cursor.execute("SELECT id, cantidad FROM productos WHERE codigo = %s", (product_code,))
                product = cursor.fetchone()

                if product:
                    product_id, cantidad_actual = product
                    quantity = simpledialog.askinteger("Vender Producto", "Cantidad a vender:")

                    if quantity and quantity <= cantidad_actual:
                        cursor.execute("INSERT INTO ventas (producto_id, cantidad) VALUES (%s, %s)", (product_id, quantity))
                        cursor.execute("UPDATE productos SET cantidad = cantidad - %s WHERE id = %s", (quantity, product_id))
                        con.commit()

                        messagebox.showinfo("Éxito", "Venta registrada correctamente.")
                        self.show_products()
                    else:
                        messagebox.showwarning("Advertencia", "Cantidad inválida o insuficiente.")
                else:
                    messagebox.showerror("Error", "Producto no encontrado.")
                
                cursor.close()
                con.close()

            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al registrar la venta: {err}")

    def generate_report(self):
        report_window = tk.Toplevel(self.root)
        report_window.title("Informe de Ventas")
        report_window.geometry("400x400")
        report_window.resizable(False, False)

        try:
            con = self.conectar()
            cursor = con.cursor()

            tk.Label(report_window, text="Productos Más Vendidos (más de 5 unidades):", font=("Arial", 12, "bold")).pack(padx=5, pady=5)
            cursor.execute("""
                SELECT productos.nombre, SUM(ventas.cantidad) as total_vendido 
                FROM ventas 
                INNER JOIN productos ON ventas.producto_id = productos.id 
                GROUP BY productos.nombre 
                HAVING total_vendido > 5
            """)
            mas_vendidos = cursor.fetchall()
            for producto in mas_vendidos:
                tk.Label(report_window, text=f"{producto[0]}: {producto[1]} unidades vendidas").pack(padx=5, pady=5)

            tk.Label(report_window, text="Productos Menos Vendidos (menos de 5 unidades):", font=("Arial", 12, "bold")).pack(padx=5, pady=5)
            cursor.execute("""
                SELECT productos.nombre, SUM(ventas.cantidad) as total_vendido 
                FROM ventas 
                INNER JOIN productos ON ventas.producto_id = productos.id 
                GROUP BY productos.nombre 
                HAVING total_vendido < 5
            """)
            menos_vendidos = cursor.fetchall()

            report_data = {
            "Productos Más Vendidos": mas_vendidos,
            "Productos Menos Vendidos": menos_vendidos,
        }

            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if file_path:
                with open(file_path, 'w') as file:
                    file.write("INFORME DE VENTAS\n\n")
                    file.write("---------------------------------------------------\n")
                    file.write("Productos Mas Vendidos:\n")
                    file.write("---------------------------------------------------\n\n")
                    for producto in report_data["Productos Más Vendidos"]:
                        file.write(f"Producto: {producto[0]:<30} | Vendido: {producto[1]} unidades\n")
                    file.write("\n\n---------------------------------------------------\n")
                    file.write("Productos Menos Vendidos:\n")
                    file.write("---------------------------------------------------\n\n")
                    for producto in report_data["Productos Menos Vendidos"]:
                        file.write(f"Producto: {producto[0]:<30} | Vendido: {producto[1]} unidades\n")
                    file.write("\nFin del informe.\n")
                
                messagebox.showinfo("Éxito", f"Informe guardado en {file_path}")

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al generar el informe: {err}")

    def NuevaCategoria(self):
        new_category = simpledialog.askstring("Nueva Categoría", "Nombre de la Nueva Categoría:")
        if new_category:
            try:
                con = self.conectar()
                cursor = con.cursor()
                cursor.execute("INSERT INTO categorias (nombre) VALUES (%s)", (new_category,))
                con.commit()
                cursor.close()
                con.close()

                self.categories.append(new_category)
                self.current_category.set(new_category)
                self.show_products()
                self.Botone_Categoria()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al guardar la categoría: {err}")

if __name__ == "__main__":
    root = tk.Tk()  
    app = App(root)  
    root.mainloop()
