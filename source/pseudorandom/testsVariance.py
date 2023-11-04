import scipy.stats
from LCG import LCG
# Parámetros del generador según tus entradas
seed = 1  # Xo
k = 4
c = 3
g = 7
m = 2 ** g
a = 1 + 2 * k

# Cantidad de números pseudoaleatorios a generar
num_to_generate = 100

# Crear una instancia del generador con los parámetros especificados
lcg = LCG(m, a, c, seed)

# Generar la secuencia de números pseudoaleatorios
random_numbers = lcg.generate(num_to_generate)

# Imprimir los números generados
for i, number in enumerate(random_numbers):
    print(f'Número {i + 1}: {number}')


# Calcular la varianza
mean = sum(random_numbers) / num_to_generate
variance = sum((x - mean) ** 2 for x in random_numbers) / (num_to_generate - 1)

# Calcular los valores para la prueba de varianza
a = 0.05
aceptacion = 0.95

adivtwo = a/2
onelessadivtwo = 1-(a/2)

valor_critico = scipy.stats.chi2.ppf(adivtwo, num_to_generate -1)
valor_critico2 = scipy.stats.chi2.ppf(onelessadivtwo, num_to_generate -1)

LI = (valor_critico) / (12 * (num_to_generate - 1))
LS = (valor_critico2) / (12 * (num_to_generate - 1))

# Verificar si la varianza está dentro de los límites aceptables
if LI <= variance <= LS:
    print("La secuencia es consistente con una distribución aleatoria (pasa la prueba de varianza).")
else:
    print("La secuencia no es consistente con una distribución aleatoria (no pasa la prueba de varianza).")
