from collections import Counter
file_path = "table_personajes.md"

aportes = []

with open(file_path, "r", encoding="utf-8") as archivo:
    lineas = archivo.readlines()
    
for linea in lineas[2:]:  #para que no lea las rayitas 
    partes = linea.split()
    if len(partes) > 2:
        aporte =  "  ".join(partes[2:])
        aportes.append(aporte.lower())
        
contador = Counter(aportes)

top3 = contador.most_common(3)

print("El top 3 son:\n")
for aporte, cantidad in top3:
    print(f"- {aporte} (mencionado {cantidad} vez/veces)")
    
    