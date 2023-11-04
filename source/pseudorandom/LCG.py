
class LCG:
    def __init__(self, m, a, c, seed):
        self.m = m
        self.a = a
        self.c = c
        self.state = seed

    #n: cantidad de numeros a generar 
    def generate(self, n):
        numbers = []
        for _ in range(n):
            self.state = (self.a * self.state + self.c) % self.m
            normalized_number = self.state / self.m
            numbers.append(normalized_number)
        return numbers
