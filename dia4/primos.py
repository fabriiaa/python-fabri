n = 1000000000
es_primo = True
while True:
    n += 1
    es_primo = True
    # CAMBIO 1: Buscamos solo hasta la raíz cuadrada en lugar de n/2
    for x in range (2, int(n**0.5) + 1):
        if n % x == 0:
            es_primo = False
            break
    if es_primo:
        print(n)
        
