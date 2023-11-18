
class LCG:
    def __init__(self, m, a, c, seed):
        """
        Inicializa el Generador Lineal Congruencial.

        Parámetros:
        - m (int): Módulo.
        - a (int): Multiplicador.
        - c (int): Incremento.
        - seed (int): Valor de semilla inicial.
        """
        self.m = m
        self.a = a
        self.c = c
        self.state = seed

    #n: cantidad de numeros a generar 
    def generate(self, n):
        """
        Genera una lista de n números pseudoaleatorios entre 0 y 1.

        Parámetros:
        - n (int): Número de números aleatorios a generar.

        Retorna:
        - list: Lista de números pseudoaleatorios.
        """
        numbers = []
        for _ in range(n):
            self.state = (self.a * self.state + self.c) % self.m
            normalized_number = self.state / self.m
            numbers.append(normalized_number)
        return numbers
