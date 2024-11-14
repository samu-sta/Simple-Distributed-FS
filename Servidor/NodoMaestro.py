import socket
import pickle
import threading

class NodoMaestro:
    def __init__(self):
        self.metadatos = {}
        self.nodos = [8001, 8002]  # Puertos de los nodos de almacenamiento

    def registrar_archivo(self, archivo, contenido):
        mitad = len(contenido) // 2
        fragmentos = [contenido[:mitad], contenido[mitad:]]
        # Enviar fragmentos a nodos de almacenamiento
        self._enviar_fragmento(self.nodos[0], archivo, '1', fragmentos[0])
        self._enviar_fragmento(self.nodos[1], archivo, '2', fragmentos[1])
        self.metadatos[archivo] = {
            'nodo1': self.nodos[0],
            'nodo2': self.nodos[1]
        }

    def obtener_archivo(self, archivo):
        if archivo not in self.metadatos:
            return {'error': f'El archivo {archivo} no existe'}
        # Obtener fragmentos de los nodos de almacenamiento
        fragmento1 = self._recibir_fragmento(self.metadatos[archivo]['nodo1'], archivo, '1')
        fragmento2 = self._recibir_fragmento(self.metadatos[archivo]['nodo2'], archivo, '2')
        return fragmento1 + fragmento2

    def _enviar_fragmento(self, puerto, archivo, num_fragmento, contenido):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', puerto))
            data = {'comando': 'guardar', 'archivo': archivo, 'fragmento': num_fragmento, 'contenido': contenido}
            s.sendall(pickle.dumps(data))
            respuesta = pickle.loads(s.recv(1024))
            print(f"NodoMaestro: {respuesta}")

    def _recibir_fragmento(self, puerto, archivo, num_fragmento):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', puerto))
            data = {'comando': 'leer', 'archivo': archivo, 'fragmento': num_fragmento}
            s.sendall(pickle.dumps(data))
            respuesta = pickle.loads(s.recv(4096))
            if 'error' in respuesta:
                print(f"Error al obtener fragmento {num_fragmento} del archivo {archivo}: {respuesta['error']}")
                return ''
            return respuesta.get('contenido', '')

    def actualizar_archivo(self, archivo, contenido):
        if archivo not in self.metadatos:
            return {'error': f'El archivo {archivo} no existe'}
        self.registrar_archivo(archivo, contenido)

    def eliminar_archivo(self, archivo):
        if archivo not in self.metadatos:
            return {'error': f'El archivo {archivo} no existe'}
        
        del self.metadatos[archivo]
        # Eliminar fragmentos de los nodos de almacenamiento
        self._eliminar_fragmento(self.nodos[0], archivo, '1')
        self._eliminar_fragmento(self.nodos[1], archivo, '2')

    def _eliminar_fragmento(self, puerto, archivo, num_fragmento):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', puerto))
            data = {'comando': 'eliminar', 'archivo': archivo, 'fragmento': num_fragmento}
            s.sendall(pickle.dumps(data))
            respuesta = pickle.loads(s.recv(1024))
            print(f"NodoMaestro: {respuesta}")

    def manejar_peticion(self, conn, addr):
        with conn:
            print(f"Conexión establecida con {addr}")
            data = conn.recv(1024)
            if not data:
                return
            peticion = pickle.loads(data)
            comando = peticion['comando']
            archivo = peticion['archivo']

            if comando == 'crear' or comando == 'actualizar':
                contenido = peticion['contenido']
                if comando == 'crear':
                    self.registrar_archivo(archivo, contenido)
                else:
                    self.actualizar_archivo(archivo, contenido)
                respuesta = {'status': 'ok'}
            elif comando == 'leer':
                contenido = self.obtener_archivo(archivo)
                if contenido is None:
                    respuesta = {'error': f'El archivo {archivo} no existe'}
                else:
                    respuesta = {'contenido': contenido}
            elif comando == 'eliminar':
                if archivo not in self.metadatos:
                    respuesta = {'error': f'El archivo {archivo} no existe'}
                else:
                    self.eliminar_archivo(archivo)
                    respuesta = {'status': 'ok'}
            else:
                respuesta = {'error': 'Comando no reconocido'}
            conn.sendall(pickle.dumps(respuesta))

def iniciar_servidor(host='localhost', port=8000):
    nodo_maestro = NodoMaestro()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.bind((host, port))
        servidor.listen()
        print(f"Servidor escuchando en {host}:{port}")
        while True:
            conn, addr = servidor.accept()
            hilo = threading.Thread(target=nodo_maestro.manejar_peticion, args=(conn, addr))
            hilo.start()

if __name__ == "__main__":
    iniciar_servidor()