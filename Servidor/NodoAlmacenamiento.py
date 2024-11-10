import socket
import threading

# Nodo de almacenamiento simulado
class NodoAlmacenamiento(threading.Thread):
    def __init__(self, puerto):
        threading.Thread.__init__(self)
        self.puerto = puerto
        self.almacenamiento = {}  # Diccionario para almacenar los fragmentos

    def run(self):
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.bind(("localhost", self.puerto))
        servidor.listen(5)
        print(f"Nodo de almacenamiento activo en puerto {self.puerto}")

        while True:
            try:
                cliente, direccion = servidor.accept()
                while True:
                    datos = cliente.recv(1024).decode()
                    print(f"Datos recibidos en nodo {self.puerto}: {datos}")
                    if not datos:
                        break
                    if datos.startswith("GUARDAR"):
                        _, archivo, fragmento, contenido = datos.split(" ", 3)
                        clave = f"{archivo}_{fragmento}"
                        self.almacenamiento[clave] = contenido
                        cliente.send(f"Fragmento {fragmento} de {archivo} guardado en nodo {self.puerto}".encode())
                    elif datos.startswith("LEER"):
                        _, archivo, fragmento = datos.split(" ", 2)
                        clave = f"{archivo}_{fragmento}"
                        contenido = self.almacenamiento.get(clave, "Fragmento no encontrado")
                        cliente.send(contenido.encode())
                cliente.close()
            except Exception as e:
                print(f"Error en el nodo de almacenamiento {self.puerto}: {e}")

# Iniciar nodos de almacenamiento
nodo1 = NodoAlmacenamiento(8001)
nodo2 = NodoAlmacenamiento(8002)
nodo1.start()
nodo2.start()