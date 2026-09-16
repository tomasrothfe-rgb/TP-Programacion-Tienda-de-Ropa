# Lista de diccionarios
usuarios = [
    {"id": 1, "nombre": "Ana", "rol": "Admin"},
    {"id": 2, "nombre": "Luis", "rol": "Editor"},
    {"id": 3, "nombre": "María", "rol": "Editor"}
]

nuevo = []

for i in usuarios:
    hola=(i["id"],i["nombre"],i["rol"], "cantidad")
    nuevo.append(hola)

print (nuevo)