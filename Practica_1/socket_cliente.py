import base64
import pickle
import shutil
import socket
import os
import json
import tkinter as Tk
from tkinter import filedialog


FORMAT = "utf-8"
SIZE = 1024

# Definir la ruta de la carpeta "raiz" (raíz de la aplicación)
ruta_raiz = 'C:\\Users\\Alan Sigala\\Desktop\\CarpetaCliente'

#Función para crear carpeta
def crear_carpeta():
    root = Tk.Tk()
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
    root = Tk.Tk()
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
    root = Tk.Tk()
    root.withdraw()  # Ocultar la ventana principal

    nueva_ruta = filedialog.askdirectory(title="Selecciona la carpeta a moverse1", initialdir=ruta_base)
    try:
        os.chdir(nueva_ruta)
        print(f"Carpeta actual: {nueva_ruta}")
    except OSError as error:
        print(f"Error al cambiar de carpeta: {error}")



def enviar_archivo(host, puerto):
    """Envía un archivo como JSON a través de un socket."""
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Conecta el socket al servidor
        server_address = (host, puerto)
        sock.connect(server_address)

        # Abre una ventana de diálogo para seleccionar el archivo
        root = Tk.Tk()
        root.withdraw()  # Ocultar la ventana principal
        ruta_archivo = filedialog.askopenfilename(title="Selecciona el archivo para enviar")
        
        #sock.sendall(ruta_archivo.encode())
        if ruta_archivo:
            #Obtenemos el nombre del archivo
            nombre_archivo = os.path.basename(ruta_archivo)

            # Envía el nombre del archivo
            sock.sendall(nombre_archivo.encode())

            #Envia tamaño del archivo
            sock.sendall(str(os.path.getsize(ruta_archivo)).encode())

            # Abre el archivo y lee su contenido
            with open(ruta_archivo, 'rb') as file:
                contenido = file.read()

            # Convierte el contenido del archivo a base64
            contenido_base64 = base64.b64encode(contenido).decode('utf-8')

            # Crear un diccionario con el contenido base64
            datos = {"archivo": contenido_base64}

            
            # Convierte el contenido del archivo a JSON
            contenido_json = json.dumps(datos)

            # Envía el contenido del archivo como JSON
            sock.sendall(contenido_json.encode())
    finally:
        # Cierra el socket
        sock.close()

#Funcion para enviar carpetas
def enviar_carpeta(host, puerto):
    """Envía una carpeta como JSON a través de un socket."""
    # Crea un socket TCP/IP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Conecta el socket al servidor
        server_address = (host, puerto)
        sock.connect(server_address)

        # Abre una ventana de diálogo para seleccionar la carpeta
        root = Tk.Tk()
        root.withdraw()  # Ocultar la ventana principal
        ruta_carpeta = filedialog.askdirectory(title="Selecciona la carpeta para enviar")

        if ruta_carpeta:
            # Lee el contenido de la carpeta
            contenido = os.listdir(ruta_carpeta)

            # Convierte el contenido de la carpeta a JSON
            contenido_json = json.dumps(contenido)

            # Envía el contenido de la carpeta como JSON
            sock.sendall(contenido_json.encode())
    finally:
        # Cierra el socket
        sock.close()



if __name__ == "__main__":
    """ Creando un socket para el cliente."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12345) #IP y puerto del servidor
    """ Conectando al servidor."""
    client.connect(server_address) # Conectando al servidor

     
    msg=client.recv(SIZE).decode(FORMAT)
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
        path=client.recv(SIZE)
        print("Tu carpeta remota: \n")
        d=pickle.loads(path[100:])
        resultado='\n'.join(d)
        print(resultado)
    
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
            enviar_archivo('localhost', 1234)
        elif opc=="1" and opc2=="6":
            # Enviamos la opción "carpeta" al servidor
            client.sendall("carpeta".encode())
            enviar_carpeta('localhost', 1234)
        elif opc=="1" and opc2=="7":
            break
        elif opc2=="7":
            break
        
    
    """ Closing the connection from the server. """
    client.close()
