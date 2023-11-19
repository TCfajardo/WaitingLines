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

    def __init__(self, tasa_llegada, tasa_servicio):
        """
        Inicializa un objeto SimuladorLineaEspera.

        Parámetros:
        - tasa_llegada: La tasa de llegada de clientes a la línea de espera.
        """
        # Parámetros del generador 
        seed_arrival = 123  # Xo
        k_arrival = 4
        c_arrival = 3
        g_arrival = 7
        m_arrival = 2 ** g_arrival
        a_arrival = 1 + 2 * k_arrival

        # Parámetros del generador para el servicio
        seed_service = 12345  # Puedes ajustar la semilla según tus necesidades
        k_service = 4
        c_service = 3
        g_service = 7
        m_service = 2 ** g_service
        a_service = 1 + 5 * k_service  # Ajusta el valor de 'a' según tus necesidades

        self.tasa_llegada = tasa_llegada
        self.tasa_servicio = tasa_servicio
        self.lcg = LCG(m_arrival, a_arrival, c_arrival, seed_arrival)
        self.lcg_service = LCG(m_service, a_service, c_service, seed_service)

        self.vehicle_catalog = VehicleCatalog()
        self.vehicle_catalog.load_from_file("source/models/vehiculos.csv")
        self.clients = Clients(self.vehicle_catalog, self.lcg)
        self.client_counter = 0
        self.tiempo_acumulado_llegada = 0
        self.iat_anterior = 0

    def generateArrival(self, num_vehiculos):
        """
        Genera vehículos aleatorios e imprime información incremental sobre cada vehículo en la llegada.

        Parámetros:
        - num_vehiculos: Número de vehículos a generar.
        """
        self.clients.generate_random_vehicles(num_vehiculos)
        random_numbers_service = self.lcg_service.generate(num_vehiculos)

        for vehicle, random_number in self.clients.vehicles:

            self.client_counter += 1
            iat = -math.log(1 - random_number) / self.tasa_llegada
            st = -math.log(1 - random_numbers_service[self.client_counter - 1]) / self.tasa_servicio

            if self.client_counter == 1:
                self.tiempo_acumulado_llegada = 0  # Para el primer cliente, el AT es 0
            else:
                self.tiempo_acumulado_llegada += self.iat_anterior  # Actualiza el tiempo acumulado de llegada

            print(f"Cliente #{self.client_counter}, {vehicle.vehicle_type}, R(i) Llegada: {random_number:.4f}, IAT: {iat:.4f}, AT: {self.tiempo_acumulado_llegada:.4f}, R(i) Servicio: {random_numbers_service[self.client_counter - 1]:.4f}, ST: {st:.4f}")
            self.iat_anterior = iat  # Actualiza el IAT anterior para el próximo cálculo


if __name__ == "__main__":
    tasa_llegada = 3  # Tasa de llegada 
    tasa_servicio = 2
    simulador = SimuladorLineaEspera(tasa_llegada, tasa_servicio)
    simulador.generateArrival(50)
