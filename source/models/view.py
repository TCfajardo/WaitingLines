import tkinter as tk
from PIL import Image, ImageTk
from SimulatorWL import SimuladorLineaEspera
from functools import partial

class SimuladorInterfaz(tk.Tk):
    def __init__(self):
        super().__init__()

        # Variables de la interfaz
        self.num_servidores_var = tk.StringVar(value="5")
        self.imagenes_var = []

        # Configuración de la ventana principal
        self.title("Simulador de Línea de Espera")
        self.geometry("800x600")

        # Etiqueta y campo de entrada para el número de servidores
        tk.Label(self, text="Número de Servidores:").pack(pady=10)
        entry_num_servidores = tk.Entry(self, textvariable=self.num_servidores_var)
        entry_num_servidores.pack(pady=10)

        # Botón para iniciar la simulación
        tk.Button(self, text="Iniciar Simulación", command=self.iniciar_simulacion).pack(pady=10)

        # Marco para mostrar las imágenes de los vehículos
        self.marco_imagenes = tk.Frame(self)
        self.marco_imagenes.pack(pady=10)

        # Configuración del simulador
        self.simulador = SimuladorLineaEspera(711.44, 2, 5)

    def cargar_imagenes(self):
        # Cargar las imágenes desde los archivos (puedes cambiar las rutas según tus necesidades)
        paths_imagenes = ["source/models/img/auto.jpg", "source/models/img/buses.jpg", "source/models/img/campero.jpg"]
        self.imagenes_var = [ImageTk.PhotoImage(Image.open(path).resize((20, 20))) for path in paths_imagenes]

    def mostrar_imagen_vehiculo(self, tipo_vehiculo):
        # Obtener el índice correspondiente al tipo de vehículo
        index = self.simulador.clients.get_index_by_vehicle_type(tipo_vehiculo)

        # Actualizar la imagen correspondiente en el marco
        if index is not None and index < len(self.imagenes_var):
            imagen = self.imagenes_var[index]
            tk.Label(self.marco_imagenes, image=imagen).pack(side=tk.LEFT)
            self.update_idletasks()  # Actualizar la interfaz para que se muestre la imagen
            self.after(2000, self.limpiar_imagen_vehiculo)  # Esperar 2 segundos y limpiar la imagen

    def limpiar_imagen_vehiculo(self):
        # Limpiar el marco después de mostrar la imagen
        for widget in self.marco_imagenes.winfo_children():
            widget.destroy()

    def iniciar_simulacion(self):
        # Cargar las imágenes de los vehículos
        self.cargar_imagenes()

        # Realizar la simulación
        self.simulador.generateArrival(10)

        # Mostrar las imágenes de los vehículos generados con una espera de 2 segundos entre cada cliente
        for cliente_info in self.simulador.clients.client_info:
            _, tipo_vehiculo, _, _, _, _ = cliente_info
            self.mostrar_imagen_vehiculo(tipo_vehiculo)


if __name__ == "__main__":
    app = SimuladorInterfaz()
    app.mainloop()
