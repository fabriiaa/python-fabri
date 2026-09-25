class Producto:
    nombre = None

    def __int__(self,n):
        self.nombre = n 

    def ver_datos(self):
        return f"Productos: {self.nombre}"


#crear un objeto

p1 = Producto("computadora")

print(p1.ver_datos())
