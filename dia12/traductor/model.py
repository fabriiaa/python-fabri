import mysql.connector

class ModelTraduccion:
    def __init__(self):
        self.conexion = mysql.connector.connect(
            host="localhost", # Corregido: localhost
            user="root",
            password="root",
            database="bd_traducciones"
        )

    def agregar_palabra(self, espanol, ingles):
        cursor = self.conexion.cursor()
        # Se especifican las columnas y se usan marcadores %s por seguridad
        sql = "INSERT INTO traducciones (palabra_espanol, palabra_ingles) VALUES (%s, %s)"
        cursor.execute(sql, (espanol, ingles))
        self.conexion.commit()
        cursor.close()

    def buscar_palabra(self, espanol):
        cursor = self.conexion.cursor()
        sql = "SELECT palabra_ingles FROM traducciones WHERE palabra_espanol = %s"
        cursor.execute(sql, (espanol,))
        resultado = cursor.fetchone()
        cursor.close()
        
        # Extrae solo el valor traducido de la tupla (si se encontró)
        if resultado:
            return resultado[0]
            
        return None