import random
puntaje = 0

for pregunta in range(5):
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    respuesta = int(input(f"Pregunta {pregunta + 1}: ¿Cuánto es {num1} x {num2}? "))

    if respuesta == num1 * num2:
        print("Excelente")
        puntaje += 1
    else:
        print(f"Ops, fallaste")

print(f"Acertaste {puntaje} de 5 preguntas.")
if(puntaje < 3):
    print("Debes practicar mucho más")
elif(puntaje < 5):
    print("Muy bien, pero puedes mejorar")
else:
    print("¡Felicidades! Eres un experto en multiplicación")

