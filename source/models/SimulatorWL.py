from Vehicle import VehicleCatalog
from LCG import LCG
from Clients import Clients
import math

class SimuladorLineaEspera:
    """
    Clase para simular una línea de espera con la generación de vehículos aleatorios.

    Parámetros:
    - tasa_llegada: La tasa de llegada de clientes a la línea de espera.

    Atributos:
    - tasa_llegada (float): La tasa de llegada de clientes.
    - lcg (LCG): Instancia de la clase LCG para generar números pseudoaleatorios.
    - vehicle_catalog (VehicleCatalog): Catálogo de vehículos.
    - clients (Clients): Instancia de la clase Clients para la generación de vehículos.
    - client_counter (int): Contador para el número total de clientes generados.
    - tiempo_acumulado_llegada (float): Tiempo acumulado de llegada.
    - iat_anterior (float): Valor del IAT del cliente anterior.
    """

    def __init__(self, tasa_llegada):
        """
        Inicializa un objeto SimuladorLineaEspera.

        Parámetros:
        - tasa_llegada: La tasa de llegada de clientes a la línea de espera.
        """
        # Parámetros del generador 
        seed = 1  # Xo
        k = 4
        c = 3
        g = 7
        m = 2 ** g
        a = 1 + 2 * k

        self.tasa_llegada = tasa_llegada
        self.lcg = LCG(m, a, c, seed)
        self.vehicle_catalog = VehicleCatalog()
        self.vehicle_catalog.load_from_file("source/models/vehiculos.csv")
        self.clients = Clients(self.vehicle_catalog, self.lcg)
        self.client_counter = 0
        self.tiempo_acumulado_llegada = 0
        self.iat_anterior = 0

    def generar_vehiculos(self, num_vehiculos):
        """
        Genera vehículos aleatorios e imprime información incremental sobre cada vehículo en la llegada.

        Parámetros:
        - num_vehiculos: Número de vehículos a generar.
        """
        self.clients.generate_random_vehicles(num_vehiculos)
        for vehicle, random_number in self.clients.vehicles:
            self.client_counter += 1
            iat = -math.log(1 - random_number) / self.tasa_llegada
            if self.client_counter == 1:
                self.tiempo_acumulado_llegada = 0  # Para el primer cliente, el AT es 0
            else:
                self.tiempo_acumulado_llegada += self.iat_anterior  # Actualiza el tiempo acumulado de llegada
            print(f"Cliente #{self.client_counter}: Categoría: {vehicle.category}, Tipo: {vehicle.vehicle_type}, R(i): {random_number:.4f}, IAT: {iat:.4f}, AT: {self.tiempo_acumulado_llegada:.4f}")
            self.iat_anterior = iat  # Actualiza el IAT anterior para el próximo cálculo


if __name__ == "__main__":
    tasa_llegada = 3  # Tasa de llegada 
    simulador = SimuladorLineaEspera(tasa_llegada)
    simulador.generar_vehiculos(50)
