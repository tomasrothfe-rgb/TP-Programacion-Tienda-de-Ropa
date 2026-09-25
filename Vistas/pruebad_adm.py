from collections import defaultdict

lista = [
    {'color': 'Negro', 'talle': 'XS', 'cantidad': 1},
    {'color': 'Negro', 'talle': 'S', 'cantidad': 1},
    {'color': 'Azul', 'talle': 'S', 'cantidad': 1}
]
agrupado = defaultdict(list)

for i in lista:
    agrupado[i['color']].append((i['talle'], i['cantidad']))

print(dict(agrupado))
