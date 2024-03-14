import socket
import os

# Definir la ruta de la carpeta "raiz" (raíz de la aplicación)
ruta_raiz = '/ruta/a/la/carpeta/especial'

#Función para crear carpeta
def crear_carpeta(ruta_base, nombre_carpeta):
    nueva_ruta = os.path.join(ruta_base, nombre_carpeta)

    try:
        os.makedirs(nueva_ruta, exist_ok=True)
        print(f"Directorio {nueva_ruta} creado correctamente")
    except OSError as error:
        print(f"Error al crear el directorio {nueva_ruta}: {error}")
              

#Funcion para listar 
def listar_archivos(ruta):
    archivos = os.listdir(ruta)
    return archivos

#Funcion para borrar carpetas/archivos
def borrar_archivos(ruta, nombre_archivo):
    ruta_archivo = os.path.join(ruta, nombre_archivo)
    try:
        os.remove(ruta_archivo)
        print(f"Archivo {ruta_archivo} eliminado correctamente")
    except OSError as error:
        print(f"Error al eliminar el archivo {ruta_archivo}: {error}")




# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 12345) #IP y puerto del servidor
s.connect(server_address) # Conectando al servidor
