from Cliente import Cliente

def mostrar_menu():
    print("1. Crear archivo")
    print("2. Leer archivo")
    print("3. Actualizar archivo")
    print("4. Eliminar archivo")
    print("5. Salir")

def main():
    cliente = Cliente()
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            archivo = input("Nombre del archivo: ")
            contenido = input("Contenido del archivo: \n")
            respuesta = cliente.crear_archivo(archivo, contenido)
            print(respuesta.get('status', 'Error al crear el archivo') + "\n\n")

        elif opcion == '2':
            archivo = input("Nombre del archivo: ")
            respuesta = cliente.leer_archivo(archivo)
            if 'error' in respuesta:
                print(respuesta['error'] + "\n\n")
            else:
                print(f"Contenido del archivo {archivo}: \n{respuesta.get('contenido', '')} \n\n")

        elif opcion == '3':
            archivo = input("Nombre del archivo: ")
            contenido = input("Nuevo contenido del archivo: \n")
            respuesta = cliente.actualizar_archivo(archivo, contenido)
            print(respuesta.get('status', 'Error al actualizar el archivo') + "\n\n")

        elif opcion == '4':
            archivo = input("Nombre del archivo: ")
            respuesta = cliente.eliminar_archivo(archivo)
            print(respuesta.get('status', 'Error al eliminar el archivo') + "\n\n")

        elif opcion == '5':
            print("Saliendo...")
            break

        else:
            print("Opción no válida. Intente de nuevo.\n\n")

if __name__ == "__main__":
    main()