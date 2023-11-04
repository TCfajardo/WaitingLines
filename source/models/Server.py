from Client import Vehicle

class TollBooth:
    def __init__(self, name, toll_rate):
        self.name = name  # Nombre del puesto de peaje
        self.toll_rate = toll_rate  # Tarifa base del peaje

    def calculate_fee(self, vehicle):
        # Calcula la tarifa del peaje para un vehículo en particular.
        # Esto puede basarse en el tipo de vehículo, horario, descuentos, etc.
        # Supongamos que el cálculo se basa en la tarifa base y el tipo de vehículo.
        if vehicle.category == 'I':
            return self.toll_rate  # Tarifa base para vehículos de categoría I
        elif vehicle.category == 'II':
            return self.toll_rate * 1.75  # Por ejemplo, tarifa para categoría II
        else:
            return self.toll_rate  # Otra tarifa base predeterminada

    def process_vehicle(self, vehicle):
        # Procesa el pago del vehículo y actualiza las estadísticas del peaje.
        fee = self.calculate_fee(vehicle)
        vehicle.set_toll_fee(fee)
        vehicle.pay_toll()

    # Otros métodos y atributos específicos del puesto de peaje.

    def set_toll_rate(self, new_toll_rate):
        # Permite actualizar la tarifa base del peaje.
        self.toll_rate = new_toll_rate

    def __str__(self):
        return f"Puesto de peaje '{self.name}' con tarifa base de ${self.toll_rate:.2f}"

# Ejemplo de uso:
if __name__ == "__main__":
    booth = TollBooth("Puesto 1", 9600)
    print(booth)  # Imprimir información del puesto de peaje

    # Simulación de procesamiento de un vehículo
    vehicle_info = {'category': 'II', 'vehicle_type': 'Buses y Busetas'}
    vehicle = Vehicle(**vehicle_info)
    booth.process_vehicle(vehicle)
    print(f"Tarifa pagada: ${vehicle.toll_fee:.2f}")
