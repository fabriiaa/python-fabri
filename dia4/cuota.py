def calcular_cuota(capital, tasa_anual, cantidad_cuotas):
    interes_total = capital * (tasa_anual / 100)
    monto_total = capital + interes_total
    cuota = monto_total / cantidad_cuotas
    return cuota

print("calculadora de cuotas")
c = int(input("Ingrese en monto a prestar: "))
t = float(input("Ingrese la tasa de interes anual: "))
cu = int(input("Ingrese la cantidad de cuotas: "))


print(f"Su cuota mensual será de: {calcular_cuota(c, t, cu)}")