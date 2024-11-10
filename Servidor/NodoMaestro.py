import socket
import pickle

class NodoMaestro:
    def __init__(self):
        self.metadatos = {}  # Almacena en qué nodos está cada fragmento de los archivos
        self.nodos = [8001, 8002]  # Lista de puertos de nodos disponibles

    def registrar_archivo(self, archivo, contenido):
        # Dividir el contenido en dos fragmentos
        mitad = len(contenido) // 2
        fragmentos = [contenido[:mitad], contenido[mitad:]]
        self.metadatos[archivo] = {
            'nodo1': (self.nodos[0], fragmentos[0]),
            'nodo2': (self.nodos[1], fragmentos[1])
        }

    def obtener_archivo(self, archivo):
        if archivo not in self.metadatos:
            return None
        fragmentos = self.metadatos.get(archivo, {})
        contenido = fragmentos.get('nodo1', ('', ''))[1] + fragmentos.get('nodo2', ('', ''))[1]
        return contenido

    def actualizar_archivo(self, archivo, contenido):
        self.registrar_archivo(archivo, contenido)

    def eliminar_archivo(self, archivo):
        if archivo in self.metadatos:
            del self.metadatos[archivo]

    def manejar_peticion(self, data):
        comando = data['comando']
        archivo = data['archivo']
        
        if comando == 'crear' or comando == 'actualizar':
            contenido = data['contenido']
            if comando == 'crear':
                self.registrar_archivo(archivo, contenido)
            else:
                self.actualizar_archivo(archivo, contenido)
            return {'status': 'ok'}
        elif comando == 'leer':
            contenido = self.obtener_archivo(archivo)
            if contenido is None:
                return {'error': f'El archivo {archivo} no existe'}
            return {'contenido': contenido}
        elif comando == 'eliminar':
            if archivo not in self.metadatos:
                return {'error': f'El archivo {archivo} no existe'}
            self.eliminar_archivo(archivo)
            return {'status': 'ok'}
        else:
            return {'status': 'comando no reconocido'}

def iniciar_servidor(host='localhost', port=5000):
    nodo_maestro = NodoMaestro()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Servidor escuchando en {host}:{port}")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Conexión establecida con {addr}")
                data = conn.recv(1024)
                if not data:
                    break
                peticion = pickle.loads(data)
                respuesta = nodo_maestro.manejar_peticion(peticion)
                conn.sendall(pickle.dumps(respuesta))

if __name__ == "__main__":
    iniciar_servidor()