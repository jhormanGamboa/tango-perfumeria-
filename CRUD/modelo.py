class modelo:
    def __init__(self):
        self.nombrec = None
        self.correo = None
        self.contraseña = None
        self.cantidad = None
        self.precio = None
        self.descripcion = None
    
    def get_nombrec(self):
        return self.nombrec
    
    def get_correo(self):
        return self.correo
    
    def get_contraseña(self):
        return self.contraseña
    
    def get_cantidad(self):
        return self.cantidad
    
    def get_precio(self):
        return self.precio
    
    def get_descripcion(self):
        return self.descripcion
    
    def set_nombrec(self,datonombrec):
        self.nombrec = datonombrec
        
    def set_correo(self, datocorreo):
        self.correo = datocorreo
    
    def set_contraseña(self,datocorntraseña):
        self.contraseña = datocorntraseña
        
    def set_cantidad(self,datocantidad):
        self.cantidad = datocantidad
    
    def set_precio(self,datoprecio):
        self.precio = datoprecio
    
    def set_descripcion(self,datodescripcion):
        self.descripcion = datodescripcion
        
    def imprimir(self):
        pass