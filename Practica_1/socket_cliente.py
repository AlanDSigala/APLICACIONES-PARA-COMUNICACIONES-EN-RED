import base64
import pickle
import shutil
import socket
import os
import json
import tkinter as tk
from tkinter import filedialog


FORMAT = "utf-8"
SIZE = 1024

# Definir la ruta de la carpeta "raiz" (raíz de la aplicación)
ruta_raiz = 'C:\\Users\\Alan Sigala\\Desktop\\CarpetaCliente'
#ruta_raiz = 'S:\CarpetaCliente'


def obtener_tamaño_carpeta(ruta_carpeta):
    total_tamaño = 0
    # Itera sobre los archivos en la carpeta y suma sus tamaños
    for ruta_actual, carpetas, archivos in os.walk(ruta_carpeta):
        for archivo in archivos:
            ruta_archivo = os.path.join(ruta_actual, archivo)
            total_tamaño += os.path.getsize(ruta_archivo)
    return total_tamaño


def obtener_estructura_carpeta(ruta_carpeta):
    estructura = {}
    for ruta_actual, carpetas, archivos in os.walk(ruta_carpeta):
        estructura[ruta_actual] = {
            'carpetas': carpetas,
            'archivos': archivos
        }
    return estructura

#Función para crear carpeta
def crear_carpeta():
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal

    ruta_base = filedialog.askdirectory(title="Selecciona la carpeta base", initialdir=ruta_raiz)
    if ruta_base:
        nombre_carpeta = input("Introduce el nombre de la carpeta a crear: ")
        nueva_ruta = os.path.join(ruta_base, nombre_carpeta)

        try:
            os.makedirs(nueva_ruta, exist_ok=True)
            print(f"Directorio {nueva_ruta} creado correctamente")
        except OSError as error:
            print(f"Error al crear el directorio {nueva_ruta}: {error}")
              

def mostrar_archivos_en_carpeta_actual():
    ruta_actual = os.getcwd()
    print("Tu carpeta local: \n")
    for root, dirs, files in os.walk(ruta_actual, topdown=False):
        for name in files:
            print(os.path.join(root, name))
        for name in dirs:
            print(os.path.join(root, name))


#Funcion para borrar carpetas/archivos
def borrar_archivo_o_carpeta():
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal

    ruta = filedialog.askopenfilename(title="Selecciona el archivo", initialdir=ruta_raiz)
    if not ruta:
        ruta = filedialog.askdirectory(title="Selecciona la carpeta", initialdir=ruta_raiz)
    if os.path.isfile(ruta):
        try:
            os.remove(ruta)
            print(f"Archivo {ruta} eliminado correctamente")
        except OSError as error:
            print(f"Error al eliminar el archivo {ruta}: {error}")
    elif os.path.isdir(ruta):
        try:
            shutil.rmtree(ruta)
            print(f"Carpeta {ruta} eliminada correctamente")
        except OSError as error:
            print(f"Error al eliminar la carpeta {ruta}: {error}")
    else:
        print("La ruta seleccionada no corresponde a un archivo ni a una carpeta.")


#Funcion para cambiar de carpeta
def cambiar_carpeta(ruta_base):
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal

    nueva_ruta = filedialog.askdirectory(title="Selecciona la carpeta a moverse1", initialdir=ruta_base)
    try:
        os.chdir(nueva_ruta)
        print(f"Carpeta actual: {nueva_ruta}")
    except OSError as error:
        print(f"Error al cambiar de carpeta: {error}")


#Funcion para enviar archivos
def enviar_archivo(socket_cliente):
        
        # Abre una ventana de diálogo para seleccionar el archivo
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana principal
        ruta_archivo = filedialog.askopenfilename(title="Selecciona el archivo para enviar")
        
        if ruta_archivo:
            #Obtenemos el nombre del archivo
            nombre_archivo = os.path.basename(ruta_archivo)

            # Envía el nombre del archivo
            socket_cliente.sendall(nombre_archivo.encode())

            #Envia tamaño del archivo
            tamaño_archivo = os.path.getsize(ruta_archivo)
            socket_cliente.sendall(str(tamaño_archivo).encode())

            # Abre el archivo y envía su contenido en bloques
            with open(ruta_archivo, 'rb') as file:
                while True:
                    contenido = file.read(1024)
                    if not contenido:
                        break
                    socket_cliente.sendall(contenido)

            print("Archivo enviado correctamente.")

# Funcion para enviar carpetas
def enviar_carpeta(socket_cliente):
    try:
        # Abre una ventana de diálogo para seleccionar la carpeta
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana principal
        ruta_carpeta = filedialog.askdirectory(title="Selecciona la carpeta para enviar")

        if ruta_carpeta:
            # Envía el nombre de la carpeta
            nombre_carpeta = os.path.basename(ruta_carpeta)
            socket_cliente.sendall(nombre_carpeta.encode())
            print("Nombre de la carpeta enviado:", nombre_carpeta)

            # Envía el tamaño de la carpeta
            tamaño_carpeta = obtener_tamaño_carpeta(ruta_carpeta)
            socket_cliente.sendall(str(tamaño_carpeta).encode())
            print("Tamaño de la carpeta enviado:", tamaño_carpeta)

            # Itera sobre los archivos en la carpeta y envía cada archivo
            for root, dirs, files in os.walk(ruta_carpeta):
                for filename in files:
                    filepath = os.path.join(root, filename)
                    # Envía el nombre del archivo
                    socket_cliente.sendall(filename.encode())
                    # Envía el tamaño del archivo
                    tamaño_archivo = os.path.getsize(filepath)
                    socket_cliente.sendall(str(tamaño_archivo).encode())
                    # Abre el archivo y envía su contenido
                    with open(filepath, 'rb') as file:
                        while True:
                            contenido = file.read(1024)
                            if not contenido:
                                break
                            socket_cliente.sendall(contenido)

            print("Contenido de la carpeta enviado correctamente.")

    except Exception as e:
        print(f"Error al enviar la carpeta: {e}")




if __name__ == "__main__":
    """ Creando un socket para el cliente."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12345) #IP y puerto del servidor
    """ Conectando al servidor."""
    client.connect(server_address) # Conectando al servidor

     
    msg=client.recv(SIZE).decode()
    print(f"[SERVER]: {msg}")

while True:
    opc=input("Elige tu opcion: \n 1.Para ver tu carpeta local \n 2.Para ver tu carpeta remota \n 3. Para salir \n")
    
    
    if opc=="1":
        for root,dirs,files in os.walk(ruta_raiz,topdown=False):
            for name in files:
                print(os.path.join(root,name))
            for name in dirs:
                print(os.path.join(root,name))

    elif opc=="2":
        client.sendall(opc.encode()) # Enviar la opción al servidor
        estructura_json = client.recv(SIZE).decode() # Recibir estructura de la carpeta
        estructura_carpeta = json.loads(estructura_json) # Convertir JSON a diccionario
        for ruta_actual, contenido in estructura_carpeta.items(): # Iterar sobre la estructura de la carpeta
            print("Carpeta:", ruta_actual)
            print("Contenido:")
            for carpeta in contenido['carpetas']:
                print(" - ", carpeta)
            for archivo in contenido['archivos']:
                print(" - ", archivo)
    
    elif opc=="3":
        break



    while True:
        opc2=input("Elige tu opcion: \n 1. Para ver tu carpeta local \n 2. Para crear carpeta \n 3. Para borrar carpeta \n 4. Para cambiar de carpeta \n 5. Para enviar archivos \n 6. Para enviar carpetas \n 7. Para salir \n")
        

        if opc=="1" and opc2=="1":
            mostrar_archivos_en_carpeta_actual()
        elif opc=="1" and opc2=="2":
            crear_carpeta()
        elif opc=="1" and opc2=="3":
            borrar_archivo_o_carpeta()
        elif opc=="1" and opc2=="4":
            cambiar_carpeta(ruta_raiz)
        elif opc=="1" and opc2=="5":
            client.sendall("archivo".encode())
            enviar_archivo(client)
        elif opc=="1" and opc2=="6":
            client.sendall("carpeta".encode())
            enviar_carpeta(client)
        elif opc=="1" and opc2=="7":
            break
        elif opc2=="7":
            break
        
    
    """ Closing the connection from the server. """
    client.close()
