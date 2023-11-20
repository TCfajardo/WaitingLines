import numpy as np
from scipy.stats import chi2
from LCG import LCG

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
# Número de categorías
num_categories = 7  # Todos diferentes, Un par, Dos pares, Tercia, Tercia y par, Cuatro cartas del mismo valor, Cinco cartas del mismo valor

# Frecuencia esperada (asumiendo igual probabilidad)
expected_frequency = len(random_numbers) / num_categories

# Frecuencia observada de cada categoría
observed_frequency = np.zeros(num_categories)

# Cuenta la frecuencia de cada categoría
for number in random_numbers:
    number_str = str(number)  # Convierte el número en una cadena
    counts = [number_str.count(digit) for digit in '0123456789']
    unique_counts = list(set(counts))
    if 2 in unique_counts and 3 not in unique_counts:
        observed_frequency[1] += 1  # Un par
    elif 2 in unique_counts and 3 in unique_counts:
        observed_frequency[2] += 1  # Dos pares
    elif 3 in unique_counts:
        observed_frequency[3] += 1  # Tercia
    elif 4 in unique_counts:
        observed_frequency[4] += 1  # Tercia y par
    elif 5 in unique_counts:
        observed_frequency[5] += 1  # Cuatro cartas del mismo valor
    elif 5 * number_str.count('0') + 4 * number_str.count('1') + 3 * number_str.count('2') + 2 * number_str.count('3') + number_str.count('4') == 9:
        observed_frequency[6] += 1  # Cinco cartas del mismo valor
    else:
        observed_frequency[0] += 1  # Todos diferentes


# Calcula el estadístico de prueba chi-cuadrado (χ²)
chi_squared = np.sum((observed_frequency - expected_frequency) ** 2 / expected_frequency)

# Grados de libertad (número de categorías - 1)
degrees_of_freedom = num_categories - 1

# Valor crítico para un nivel de significancia del 5% y grados de libertad
alpha = 0.05
critical_value = chi2.ppf(1 - alpha, degrees_of_freedom)

# Compara el valor de χ² con el valor crítico
if chi_squared < critical_value:
    print("La secuencia pasa la prueba de poker y es considerada aleatoria.")
else:
    print("La secuencia no pasa la prueba de poker y no es considerada aleatoria.")