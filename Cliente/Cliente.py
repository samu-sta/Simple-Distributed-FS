import socket
import pickle

class Cliente:
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port

    def crear_archivo(self, archivo, contenido):
        data = {'comando': 'crear', 'archivo': archivo, 'contenido': contenido}
        return self._enviar_peticion(data)

    def leer_archivo(self, archivo):
        data = {'comando': 'leer', 'archivo': archivo}
        return self._enviar_peticion(data)

    def actualizar_archivo(self, archivo, contenido):
        data = {'comando': 'actualizar', 'archivo': archivo, 'contenido': contenido}
        return self._enviar_peticion(data)

    def eliminar_archivo(self, archivo):
        data = {'comando': 'eliminar', 'archivo': archivo}
        return self._enviar_peticion(data)

    def _enviar_peticion(self, data):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(pickle.dumps(data))
            response = s.recv(1024)
            return pickle.loads(response)