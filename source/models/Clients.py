from Vehicle import VehicleCatalog
from LCG import LCG

class Clients:
    def __init__(self, vehicle_catalog, lcg):
        self.vehicle_catalog = vehicle_catalog
        self.lcg = lcg
        self.vehicles = []

    def generate_random_vehicles(self, num_vehicles):
        random_numbers = self.lcg.generate(num_vehicles)  # Generar todos los números necesarios de antemano
        #e recorre cada número pseudoaleatorio y se utiliza para seleccionar una categoría del catálogo de vehículos.
        for i in range(num_vehicles):
            category = self.generate_random_category(random_numbers[i])
            vehicle = self.vehicle_catalog.get_vehicle(category)
            if vehicle:
                self.vehicles.append((vehicle, random_numbers[i]))
            else:
                print(f"Error: Vehículo no encontrado para la categoría {category}")

    def generate_random_category(self, random_number):
        categories = list(self.vehicle_catalog.vehicles.keys())
        #Multiplicando el número pseudoaleatorio por la longitud de la lista de categorías 
        #se obtiene un valor en el rango de índices válidos.
        index = int(random_number * len(categories))
        return categories[index]

# Ejemplo de uso:
if __name__ == "__main__":
    # Parámetros del generador según tus entradas
    seed = 1  # Xo
    k = 4
    c = 3
    g = 7
    m = 2 ** g
    a = 1 + 2 * k

    # Crear una instancia del generador con los parámetros especificados
    lcg = LCG(m, a, c, seed)
    vehicle_catalog = VehicleCatalog()
    vehicle_catalog.load_from_file("source/models/vehiculos.csv")

    clients = Clients(vehicle_catalog, lcg)
    clients.generate_random_vehicles(65)

    print("Vehículos generados aleatoriamente:")
    for vehicle, random_number in clients.vehicles:
        print(f"Categoria: {vehicle.category}, Tipo: {vehicle.vehicle_type}, Tarifa: ${vehicle.tariff}, Numero Aleatorio: {random_number}")
