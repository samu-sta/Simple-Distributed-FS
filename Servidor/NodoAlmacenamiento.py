import socket
import threading
import pickle

class NodoAlmacenamiento(threading.Thread):
    def __init__(self, puerto):
        threading.Thread.__init__(self)
        self.puerto = puerto
        self.almacenamiento = {}

    def run(self):
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.bind(("localhost", self.puerto))
        servidor.listen(5)
        print(f"Nodo de almacenamiento activo en puerto {self.puerto}")

        while True:
            cliente, direccion = servidor.accept()
            hilo = threading.Thread(target=self.manejar_cliente, args=(cliente,))
            hilo.start()

    def manejar_cliente(self, conexion):
        with conexion:
            while True:
                try:
                    datos = conexion.recv(4096)
                    if not datos:
                        break
                    peticion = pickle.loads(datos)
                    respuesta = self.procesar_peticion(peticion)
                    conexion.sendall(pickle.dumps(respuesta))
                except Exception as e:
                    print(f"Error en NodoAlmacenamiento {self.puerto}: {e}")
                    break

    def guardar_fragmento(self, archivo, fragmento, contenido):
        clave = f"{archivo}_{fragmento}"
        self.almacenamiento[clave] = contenido
        return {'status': f"Fragmento {fragmento} de {archivo} guardado en nodo {self.puerto}"}

    def leer_fragmento(self, archivo, fragmento):
        clave = f"{archivo}_{fragmento}"
        contenido = self.almacenamiento.get(clave)
        if contenido is None:
            return {'error': 'Fragmento no encontrado'}
        return {'contenido': contenido}

    def eliminar_fragmento(self, archivo, fragmento):
        clave = f"{archivo}_{fragmento}"
        if clave in self.almacenamiento:
            del self.almacenamiento[clave]
            return {'status': f"Fragmento {fragmento} de {archivo} eliminado en nodo {self.puerto}"}
        else:
            return {'error': 'Fragmento no encontrado'}

    def procesar_peticion(self, peticion):
        comando = peticion.get('comando')
        archivo = peticion.get('archivo')
        fragmento = peticion.get('fragmento')
        print(f"Nodo {self.puerto}: {comando} {archivo} {fragmento}")

        if comando == 'guardar':
            return self.guardar_fragmento(archivo, fragmento, peticion.get('contenido'))
        elif comando == 'leer':
            return self.leer_fragmento(archivo, fragmento)
        elif comando == 'eliminar':
            return self.eliminar_fragmento(archivo, fragmento)
        else:
            return {'error': 'Comando no reconocido'}

# Iniciar nodos de almacenamiento
if __name__ == "__main__":
    nodo1 = NodoAlmacenamiento(8001)
    nodo2 = NodoAlmacenamiento(8002)
    nodo1.start()
    nodo2.start()