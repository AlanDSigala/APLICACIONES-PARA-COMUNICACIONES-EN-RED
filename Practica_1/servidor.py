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


def recibir_carpeta(socket_cliente, ruta_destino):
    # Recibe la estructura de la carpeta como JSON
    estructura_carpeta_json = socket_cliente.recv(4096).decode()
    estructura_carpeta = json.loads(estructura_carpeta_json)

    # Recorre la estructura y crea las carpetas/archivos
    for ruta_actual, contenido in estructura_carpeta.items():
        # Crea la carpeta si no existe
        ruta_completa = os.path.join(ruta_destino, ruta_actual)
        if not os.path.exists(ruta_completa):
            os.makedirs(ruta_completa)

        # Guarda los archivos en la carpeta
        for archivo in contenido['archivos']:
            ruta_archivo = os.path.join(ruta_completa, archivo)
            with open(ruta_archivo, 'wb') as f:
                # Recibe los datos del archivo
                while True:
                    datos = socket_cliente.recv(4096)
                    if not datos:
                        break
                    f.write(datos)

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
            recibir_carpeta(client_socket, ruta_remota)

        elif opcion == '2':
            enviar_estructura_carpeta(client_socket, ruta_remota)


        client_socket.close()

    finally:
        server_socket.close()

# Iniciamos el servidor
iniciar_servidor()
