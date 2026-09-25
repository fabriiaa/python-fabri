import google.generativeai as genai

genai.configure(api_key="AQ.Ab8RN6IbROO4Mc3YQTi_DujzxBz_kdQ9FIECIRM681KTxAJHew")
modelo = genai.GenerativeModel("gemini-3.6-flash")

class Chatbot:
    def __init__(self, nombre):
        self.nombre = nombre
        self.base_conocimiento = {
            "hola": "Hola, ¿Hola, qué hago por ti?",
           
        }
        self.historial = []
        self.nombre_usuario = None

    def responder(self, mensaje):
        mensaje = mensaje.lower().strip()
        self.historial.append(mensaje)

        if mensaje == "historial":
            if len(self.historial) <= 1:
                return "Aún no hay mensajes anteriores."
            mensajes = self.historial[:-1]
            return "Historial:\n" + "\n".join(
                f"{indice}. {texto}" for indice, texto in enumerate(mensajes, 1)
            )

        if mensaje.startswith("me llamo "):
            nombre = mensaje[len("me llamo "):].strip()
            if nombre:
                self.nombre_usuario = nombre.title()
                return f"¡Mucho gusto, {self.nombre_usuario}!"

        for clave, respuesta in self.base_conocimiento.items():
            if clave in mensaje:
                return self._personalizar_respuesta(respuesta)
        try:
            resultado = modelo.generate_content(mensaje)
            return resultado.text
            return wikipedia.summary(mensaje,sentences=2)
        except Exception:
            return "No entendí tu mensaje, ¿Podrías reformularlo?"
            

        return self._personalizar_respuesta("No entendí tu mensaje, ¿Podrías reformularlo?")
    
    def agregar_conocimiento(self, clave, respuesta):
        self.base_conocimiento[clave.lower()] = respuesta

    def _personalizar_respuesta(self, respuesta):
        if self.nombre_usuario:
            return f" {respuesta}"
        return respuesta


def main():
    bot = Chatbot("Miki")
    print(f"{bot.nombre}: Hola, en qué puedo ayudarte?")

    while True:
        entrada = input("Tú: ")

        if entrada.lower().strip() == "salir":
            print("Hasta luego")
            break

        respuesta = bot.responder(entrada)
        print(f"{bot.nombre}: {respuesta}")

if __name__ == "__main__":
    main()

