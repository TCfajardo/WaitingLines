from Vehicle import VehicleCatalog
from LCG import LCG
from Clients import Clients
from collections import deque
import math
import threading
import time
import matplotlib.pyplot as plt

class SimuladorLineaEspera:
    def __init__(self, tasa_llegada, tasa_servicio, num_servidores):
       seed_arrival = 123
       k_arrival = 4
       c_arrival = 3
       g_arrival = 7
       m_arrival = 2 ** g_arrival
       a_arrival = 1 + 2 * k_arrival

       seed_service = 12345
       k_service = 4
       c_service = 3
       g_service = 7
       m_service = 2 ** g_service
       a_service = 1 + 5 * k_service


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
       self.cola = deque()
       self.start_time = 0
       self.exit_time = 0
       self.semaforo_cola = threading.Semaphore()
       self.num_servidores = num_servidores
       self.tiempos = []
       self.longitud_cola = []
       self.frecuencia_vehiculos = {}

    def procesar_servidor(self, num_servidor, cliente, st):
       with self.semaforo_cola:
           print(f"Servidor #{num_servidor + 1} - Cola #{num_servidor + 1}: Atendiendo al Cliente #{cliente}")


           self.start_time = max(self.exit_time, self.tiempo_acumulado_llegada)
           self.exit_time = self.start_time + st
           print(f"Tiempo de inicio del servidor #{num_servidor + 1}: {self.start_time:.4f}")
           print(f"Tiempo de salida del servidor #{num_servidor + 1}: {self.exit_time:.4f}")

    def asignar_a_cola(self, cliente, vehicle_type):
        with self.semaforo_cola:
            self.cola.append(cliente)
            self.tiempos.append(self.tiempo_acumulado_llegada)
            self.longitud_cola.append(len(self.cola))
            tipo_vehiculo = vehicle_type
            self.frecuencia_vehiculos[tipo_vehiculo] = self.frecuencia_vehiculos.get(tipo_vehiculo, 0) + 1
            print(f"Cliente #{cliente} asignado a la cola - Tipo de vehículo: {tipo_vehiculo}")

    def generateArrival(self, num_vehiculos):
       self.clients.generate_random_vehicles(num_vehiculos)
       random_numbers_service = self.lcg_service.generate(num_vehiculos * 2)


       for vehicle, random_number in self.clients.vehicles:
           self.client_counter += 1
           iat = -math.log(1 - random_number) / self.tasa_llegada
           st = -math.log(1 - random_numbers_service[self.client_counter - 1]) / self.tasa_servicio


           if self.client_counter == 1:
               self.tiempo_acumulado_llegada = 0
           else:
               self.tiempo_acumulado_llegada += self.iat_anterior


           print(f"Cliente #{self.client_counter}, {vehicle.vehicle_type}, "
                 f"R(i) Llegada: {random_number:.4f}, IAT: {iat:.4f}, "
                 f"AT: {self.tiempo_acumulado_llegada:.4f}, "
                 f"R(i) Servicio: {random_numbers_service[self.client_counter - 1]:.4f}, "
                 f"ST: {st:.4f}")
           time.sleep(0.2)
           self.asignar_a_cola(self.client_counter, vehicle.vehicle_type)
           # Modificamos la llamada para pasar el número del servidor
           self.procesar_servidor(self.client_counter % self.num_servidores, self.client_counter, st)
           self.iat_anterior = iat
    
    def generar_grafico(self):
        if hasattr(plt, 'plot'):  # Verificar si plt.plot está definido
            # Graficar la longitud de la cola
            plt.figure(figsize=(12, 6))
            plt.subplot(1, 2, 1)
            plt.plot(self.tiempos, self.longitud_cola, label="Longitud de la cola")
            plt.xlabel("Tiempo")
            plt.ylabel("Cantidad de vehículos en cola")
            plt.title("Simulación de Línea de Espera")
            plt.legend()

            # Graficar la frecuencia de cada tipo de vehículo
            plt.subplot(1, 2, 2)
            tipos_vehiculos = list(self.frecuencia_vehiculos.keys())
            frecuencias = list(self.frecuencia_vehiculos.values())
            plt.bar(tipos_vehiculos, frecuencias, color='skyblue')
            plt.xlabel("Tipo de Vehículo")
            plt.ylabel("Frecuencia")
            plt.title("Frecuencia de Tipos de Vehículo en el Peaje")
            plt.xticks(rotation=45, ha="right")  # Rotar las etiquetas en el eje x
            plt.tight_layout()  # Ajustar el diseño automáticamente
            plt.show()
        else:
            print("Matplotlib no está correctamente importado. Asegúrate de tenerlo instalado.")


def simulacion_servidor(simulador, num_vehiculos):
   simulador.generateArrival(num_vehiculos)
   simulador.generar_grafico()


import tkinter as tk
from tkinter import ttk, scrolledtext
import sys
import io

class RedirectText(io.StringIO):
   def __init__(self, text_widget):
       self.text_widget = text_widget


   def write(self, string):
       self.text_widget.insert(tk.END, string)

class Application(tk.Tk):
   def __init__(self):
       super().__init__()
       self.title("Simulador de Línea de Espera")
       self.geometry("800x600")

       self.create_widgets()

   def create_widgets(self):
       frame = ttk.Frame(self)
       frame.pack(padx=10, pady=10)

       self.entry_tasa_llegada = self.create_entry(frame, "Tasa de Llegada:", 0)
       self.entry_tasa_servicio = self.create_entry(frame, "Tasa de Servicio:", 1)
       self.entry_num_servidores = self.create_entry(frame, "Número de Servidores:", 2)
       self.entry_num_vehiculos = self.create_entry(frame, "Número de Vehículos:", 3)

       button_run = ttk.Button(frame, text="Ejecutar Simulación", command=self.run_simulation)
       button_run.grid(row=4, column=0, columnspan=2)

       self.text_output = scrolledtext.ScrolledText(frame, width=90, height=20)
       self.text_output.grid(row=5, column=0, columnspan=2, pady=10)

       sys.stdout = RedirectText(self.text_output)

   def create_entry(self, frame, text, row):
       label = ttk.Label(frame, text=text)
       label.grid(row=row, column=0, sticky=tk.W)
       entry = ttk.Entry(frame)
       entry.grid(row=row, column=1, sticky=(tk.W, tk.E))
       return entry

   def run_simulation(self):
       tasa_llegada = float(self.entry_tasa_llegada.get())
       tasa_servicio = float(self.entry_tasa_servicio.get())
       num_servidores = int(self.entry_num_servidores.get())
       num_vehiculos = int(self.entry_num_vehiculos.get())

       # Instanciar la clase SimuladorLineaEspera
       simulador = SimuladorLineaEspera(tasa_llegada, tasa_servicio, num_servidores)

       # Llamar a la función de simulación
       simulacion_servidor(simulador, num_vehiculos)


if __name__ == "__main__":
   app = Application()
   app.mainloop()
