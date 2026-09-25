from model import ModelTraduccion

class ControladorTraduccion:
    def __init__(self):
        # 1. Instanciar el modelo agregando ()
        # 2. Usar 'modelo' para mantener consistencia con los otros métodos
        self.modelo = ModelTraduccion()

    def cargar_palabra(self, esp, ing):
        self.modelo.agregar_palabra(esp, ing)

    def traducir(self, palabra):
        resultado = self.modelo.buscar_palabra(palabra)
        if resultado is not None:
            return resultado

        return None
    