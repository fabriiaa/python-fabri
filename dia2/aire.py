temperatura = 31.0
modo_ausente = False

if modo_ausente:
    print("Encender aire acondicionado")
else:
    if temperatura > 28:
        print("Encender aire acondicionado")
    else:
        print("Temperatura confortable")