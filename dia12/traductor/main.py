from controller import ControladorTraduccion

controlador = ControladorTraduccion()

while True:
    print("1. Cargar palabra")
    print("2. Traducir")
    print("3. Salir")
    opcion = input("Elige una opción: ")

    if opcion == "1":
        esp = input("Escribe la palabra en español: ")
        ing = input("Escribe su traducción en inglés: ")
        controlador.cargar_palabra(esp, ing)
        print("Palabra cargada exitosamente.")
        
    elif opcion == "2":
        palabra = input("Escribe la palabra a traducir: ")
        traduccion = controlador.traducir(palabra)
        if traduccion:
            print(f"{palabra} -> {traduccion}")
        else:
            print(f"La palabra '{palabra}' no se encuentra registrada.")

    elif opcion == "3":
        print("¡Hasta luego!")
        break
    else:
        print("Opción no válida. Intenta de nuevo.")
        