# Definición de la variable en el ámbito global
contador = 10 

def modificar_global():
    # Indicamos a Python que use la variable global externa
    global contador 
    contador = 20

print("Antes de la función:", contador) # Imprime 10
modificar_global()
print("Después de la función:", contador) # Imprime 20
