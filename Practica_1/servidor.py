import json
import os
import shutil
import socket
SIZE = 1024
ruta_remota ='C:\\Users\\Alan\\Desktop\\CarpetaRemota'

def recibir_archivo(socket_cliente):
    try:
        # Recibir el nombre del archivo
        nombre_archivo = socket_cliente.recv(SIZE).decode()

        # Recibir el tamaño del archivo
        tamaño_archivo = int(socket_cliente.recv(SIZE).decode())

        ruta_guardado = os.path.join(ruta_remota, nombre_archivo)  # Establece la ruta donde guardar el archivo

        # Abrir un archivo en modo de escritura binaria
        with open(ruta_guardado, 'wb') as file:
            total_recibido = 0
            while total_recibido < tamaño_archivo:
                datos = socket_cliente.recv(SIZE)
                file.write(datos)
                total_recibido += len(datos)

        print("Archivo recibido correctamente.")
    except Exception as e:
        print(f"Error al recibir el archivo: {e}")


# Función para recibir una carpeta
def recibir_carpeta(socket_servidor):
    try:
        # Recibe el nombre de la carpeta
        nombre_carpeta = socket_servidor.recv(1024).decode()
        print("Nombre de la carpeta recibido:", nombre_carpeta)

        ruta_carpeta = os.path.join(ruta_remota, nombre_carpeta)  # Establece la ruta donde guardar la carpeta
        # Crea la carpeta si no existe
        if not os.path.exists(ruta_carpeta):
            os.makedirs(nombre_carpeta)

        # Recibe el tamaño de la carpeta
        tamaño_carpeta = int(socket_servidor.recv(1024).decode())
        print("Tamaño de la carpeta:", tamaño_carpeta)

        # Recibe los archivos y guárdalos en la carpeta
        while tamaño_carpeta > 0:
            # Recibe el nombre del archivo
            nombre_archivo = socket_servidor.recv(1024).decode()
            print("Nombre del archivo recibido:", nombre_archivo)

            # Recibe el tamaño del archivo
            tamaño_archivo = int(socket_servidor.recv(1024).decode())
            print("Tamaño del archivo:", tamaño_archivo)

            # Recibe y guarda el contenido del archivo
            with open(os.path.join(nombre_carpeta, nombre_archivo), 'wb') as file:
                while tamaño_archivo > 0:
                    data = socket_servidor.recv(1024)
                    if not data:
                        break
                    file.write(data)
                    tamaño_archivo -= len(data)
                    tamaño_carpeta -= len(data)

        print("Carpeta recibida correctamente.")

    except Exception as e:
        print(f"Error al recibir la carpeta: {e}")


def enviar_estructura_carpeta(socket_cliente, ruta_carpeta):
    estructura_carpeta = obtener_estructura_carpeta(ruta_carpeta)
    estructura_json = json.dumps(estructura_carpeta)
    socket_cliente.send(estructura_json.encode())

def obtener_estructura_carpeta(ruta_carpeta):
    estructura = {}
    for ruta_actual, carpetas, archivos in os.walk(ruta_carpeta):
        estructura[ruta_actual] = {
            'carpetas': carpetas,
            'archivos': archivos
        }
    return estructura

def iniciar_servidor():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12345)

    try:
        server_socket.bind(server_address)
        server_socket.listen(1)
        print("Servidor escuchando en {}:{}".format(*server_address))

       
        client_socket, client_address = server_socket.accept()
        print("Conexión establecida desde {}:{}".format(*client_address))

        mensaje = "¡Hola desde el servidor!"
        client_socket.sendall(mensaje.encode())

        opcion = client_socket.recv(1024).decode()
        print(f"Opción seleccionada: {opcion}")
        if opcion == 'archivo':
            recibir_archivo(client_socket)
        elif opcion == 'carpeta':
            #nombre_carpeta = client_socket.recv(1024).decode()
            recibir_carpeta(client_socket)

        elif opcion == '2':
            enviar_estructura_carpeta(client_socket, ruta_remota)


        client_socket.close()

    finally:
        server_socket.close()

# Iniciamos el servidor
iniciar_servidor()
