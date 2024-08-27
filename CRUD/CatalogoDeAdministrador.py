import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from PIL import Image, ImageTk

try:
    from PIL import Image, ImageTk, Resampling
    RESAMPLING_METHOD = Resampling.LANCZOS
except ImportError:
    RESAMPLING_METHOD = Image.Resampling.LANCZOS

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Tango")
        self.products = {}  # Diccionario para almacenar productos
        self.sales = {}  # Diccionario para almacenar las ventas
        self.categories = ["CABALLERO", "DAMA"]  # Lista de categorías
        self.current_category = tk.StringVar(value=self.categories[0])

        # Configuración de la ventana principal
        self.main_frame = tk.Frame(root, bg="#b9030f")
        self.main_frame.pack(fill="both", expand=True)

        # Barra de navegación
        self.nav_frame = tk.Frame(self.main_frame, bg="#d4ddb1")
        self.nav_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")
        self.Botones_Navegacion()

        # Área de categorías
        self.category_frame = tk.Frame(self.main_frame, bg="#b9030f")
        self.category_frame.grid(row=1, column=1, columnspan=2, sticky="nsew")
        self.Botone_Categoria()

        # Área de productos
        self.product_frame = tk.Frame(self.main_frame, bg="#b9030f")
        self.product_frame.grid(row=2, column=1, columnspan=2, sticky="nsew")
        self.show_products()

        # Botones de Editar y Eliminar
        self.edit_delete_frame = tk.Frame(self.main_frame, bg="#b9030f")
        self.edit_delete_frame.grid(row=2, column=0, sticky="nsew")
        self.BotonesEdicion()

        # Botón de Salir
        self.exit_button = tk.Button(self.main_frame, text="Salir", command=root.quit, bg="#b9030f")
        self.exit_button.grid(row=3, column=2, sticky="e", padx=10, pady=10)

    def Botones_Navegacion(self):
        tk.Button(self.nav_frame, text="Registrar Nuevo Producto", command=self.Registar_Productos).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(self.nav_frame, text="Generar Informe", command=self.generate_report).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.nav_frame, text="Vender", command=self.sell_product).grid(row=0, column=2, padx=5, pady=5)

    def Botone_Categoria(self):
        for category in self.categories:
            tk.Radiobutton(self.category_frame, text=category, variable=self.current_category, value=category, bg="#d4ddb1", command=self.show_products).pack(side="left", padx=5, pady=5)
        tk.Button(self.category_frame, text="+", command=self.NuevaCategoria).pack(side="left", padx=5, pady=5)

    def show_products(self):
        # Limpia el área de productos
        for widget in self.product_frame.winfo_children():
            widget.destroy()

        # Muestra los productos de la categoría seleccionada
        selected_category = self.current_category.get()
        row, col = 0, 0
        for code, product in self.products.items():
            if product['categoria'] == selected_category:
                frame = tk.Frame(self.product_frame, bg="#d4ddb1", padx=5, pady=5)
                frame.grid(row=row, column=col, padx=5, pady=5)

                # Mostrar imagen del producto
                img_label = tk.Label(frame, image=product['imagen'])
                img_label.pack()

                # Mostrar detalles del producto
                details = f"Nombre: {product['nombre']}\nCantidad: {product['cantidad']}\nPrecio: ${product['precio']}\nDescripción: {product['descripcion']}"
                tk.Label(frame, text=details).pack()

                col += 1
                if col > 2:
                    col = 0
                    row += 1

    def BotonesEdicion(self):
        tk.Button(self.edit_delete_frame, text="EDITAR", command=self.Editar_Productos).pack(padx=5, pady=5)
        tk.Button(self.edit_delete_frame, text="ELIMINAR", command=self.Eliminar_Productos).pack(padx=5, pady=5)

    def Registar_Productos(self):
        def select_image():
            file_path = filedialog.askopenfilename(title="Seleccionar Imagen", filetypes=[("Image files", "*.jpg *.png")])
            if file_path:
                img = Image.open(file_path)
                img = img.resize((100, 100), RESAMPLING_METHOD)  # Ajuste del tamaño de la imagen
                img = ImageTk.PhotoImage(img)
                product_image_label.config(image=img)
                product_image_label.image = img
                product_data['imagen'] = img

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

            self.products[codigo] = {
                "categoria": categoria,
                "nombre": nombre,
                "cantidad": cantidad,
                "precio": precio,
                "descripcion": descripcion,
                "imagen": imagen
            }
            self.sales[codigo] = 0  # Inicializa las ventas para este producto
            messagebox.showinfo("Éxito", f"Producto '{nombre}' registrado exitosamente.")
            register_window.destroy()
            self.show_products()

        # Ventana para registrar producto
        register_window = tk.Toplevel(self.root)
        register_window.title("Registrar Producto")

        # Configuración de la ventana de registro
        tk.Label(register_window, text="Categoría:").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(register_window, text="Código:").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(register_window, text="Nombre:").grid(row=2, column=0, padx=5, pady=5)
        tk.Label(register_window, text="Cantidad:").grid(row=3, column=0, padx=5, pady=5)
        tk.Label(register_window, text="Precio:").grid(row=4, column=0, padx=5, pady=5)
        tk.Label(register_window, text="Descripción:").grid(row=5, column=0, padx=5, pady=5)
        tk.Label(register_window, text="Imagen:").grid(row=6, column=0, padx=5, pady=5)

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
        tk.Button(register_window, text="Registrar Producto", command=save_product).grid(row=7, column=0, columnspan=3, pady=10)

    def Editar_Productos(self):
        # Función para editar un producto existente
        product_code = simpledialog.askstring("Editar Producto", "Código del Producto:")
        if product_code in self.products:
            product = self.products[product_code]
            # Ventana para editar detalles del producto
            edit_window = tk.Toplevel(self.root)
            edit_window.title(f"Editar {product_code}")

            tk.Label(edit_window, text="Precio:").grid(row=0, column=0, padx=5, pady=5)
            tk.Label(edit_window, text="Cantidad:").grid(row=1, column=0, padx=5, pady=5)
            tk.Label(edit_window, text="Descripción:").grid(row=2, column=0, padx=5, pady=5)

            price_entry = tk.Entry(edit_window)
            price_entry.insert(0, product['precio'])
            price_entry.grid(row=0, column=1, padx=5, pady=5)

            quantity_entry = tk.Entry(edit_window)
            quantity_entry.insert(0, product['cantidad'])
            quantity_entry.grid(row=1, column=1, padx=5, pady=5)

            description_entry = tk.Entry(edit_window)
            description_entry.insert(0, product['descripcion'])
            description_entry.grid(row=2, column=1, padx=5, pady=5)

            def save_changes():
                new_price = price_entry.get()
                new_quantity = quantity_entry.get()
                new_description = description_entry.get()

                if new_price and new_quantity and new_description:
                    self.products[product_code]['precio'] = new_price
                    self.products[product_code]['cantidad'] = new_quantity
                    self.products[product_code]['descripcion'] = new_description
                    messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
                    edit_window.destroy()
                    self.show_products()
                else:
                    messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")

            tk.Button(edit_window, text="Guardar Cambios", command=save_changes).grid(row=3, column=0, columnspan=2, pady=10)
        else:
            messagebox.showerror("Error", "Producto no encontrado.")

    def Eliminar_Productos(self):
        # Función para eliminar un producto
        product_code = simpledialog.askstring("Eliminar Producto", "Código del Producto:")
        if product_code in self.products:
            del self.products[product_code]
            del self.sales[product_code]
            messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
            self.show_products()
        else:
            messagebox.showerror("Error", "Producto no encontrado.")

    def sell_product(self):
        # Función para registrar una venta
        product_code = simpledialog.askstring("Vender Producto", "Código del Producto:")
        if product_code in self.products:
            quantity = simpledialog.askinteger("Vender Producto", "Cantidad a vender:")
            if quantity and quantity <= int(self.products[product_code]['cantidad']):
                self.products[product_code]['cantidad'] = str(int(self.products[product_code]['cantidad']) - quantity)
                self.sales[product_code] += quantity
                messagebox.showinfo("Éxito", "Venta registrada correctamente.")
                self.show_products()
            else:
                messagebox.showwarning("Advertencia", "Cantidad inválida o insuficiente.")
        else:
            messagebox.showerror("Error", "Producto no encontrado.")

    def generate_report(self):
        # Función para generar un informe de ventas
        report_window = tk.Toplevel(self.root)
        report_window.title("Informe de Ventas")

        tk.Label(report_window, text="Productos Más Vendidos (más de 5 unidades):").pack(padx=5, pady=5)
        for code, sales_count in self.sales.items():
            if sales_count > 5:
                product = self.products[code]
                tk.Label(report_window, text=f"{product['nombre']}: {sales_count} unidades vendidas").pack(padx=5, pady=5)

        tk.Label(report_window, text="Productos Menos Vendidos (menos de 5 unidades):").pack(padx=5, pady=5)
        for code, sales_count in self.sales.items():
            if sales_count < 5:
                product = self.products[code]
                tk.Label(report_window, text=f"{product['nombre']}: {sales_count} unidades vendidas").pack(padx=5, pady=5)

    def NuevaCategoria(self):
        # Función para agregar una nueva categoría
        new_category = simpledialog.askstring("Nueva Categoría", "Nombre de la Nueva Categoría:")
        if new_category:
            self.categories.append(new_category)
            self.current_category.set(new_category)
            self.show_products()
            self.Botone_Categoria()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
