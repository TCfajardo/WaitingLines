import csv
import re

class Vehicle:
    def __init__(self, category, vehicle_type, tariff):
        self.category = category
        self.vehicle_type = vehicle_type
        self.tariff = tariff

class VehicleCatalog:
    def __init__(self):
        self.vehicles = {}  # Un diccionario para almacenar los vehículos

    def load_from_file(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                category = row['CATEGORÍA']
                vehicle_type = row['TIPO DE VEHÍCULO']

                # Procesar la tarifa eliminando caracteres no numéricos y espacios en blanco
                raw_tariff = row['TARIFA']
                cleaned_tariff = re.sub(r'[^\d.]', '', raw_tariff)  # Eliminar todo excepto dígitos y punto

                # Intentar convertir la tarifa en un número en coma flotante
                try:
                    tariff = float(cleaned_tariff)
                except ValueError:
                    tariff = 0.0  # Opcional: Valor predeterminado en caso de error

                vehicle = Vehicle(category, vehicle_type, tariff)
                self.vehicles[category] = vehicle

    def get_vehicle(self, category):
        if category in self.vehicles:
            return self.vehicles[category]
        else:
            return None

# Ejemplo de uso:
if __name__ == "__main__":
    vehicle_catalog = VehicleCatalog()
    vehicle_catalog.load_from_file("source/models/vehiculos.csv")

    # Consultar la información de un vehículo por categoría
    category = "II"
    vehicle = vehicle_catalog.get_vehicle(category)

    if vehicle:
        print(f"Categoría: {vehicle.category}")
        print(f"Tipo de Vehículo: {vehicle.vehicle_type}")
        print(f"Tarifa: ${vehicle.tariff}")
    else:
        print("Vehículo no encontrado.")
