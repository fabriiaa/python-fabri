#control de temperatura
temp = 25
while temp > 0:
    temp = float(input("Ingrese temp:"))
    if temp >= 28:
        print("Encender AA")
    elif temp <= 17:
        print("Encender calefacción")
    else:
        print("Temperatura agradable")
        