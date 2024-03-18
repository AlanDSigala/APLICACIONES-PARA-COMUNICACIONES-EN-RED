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

    nueva_ruta = filedialog.askdirectory(title="Selecciona la carpeta a moverse", initialdir=ruta_base)
    try:
        os.chdir(nueva_ruta)
        print(f"Carpeta actual: {nueva_ruta}")
    except OSError as error:
        print(f"Error al cambiar de carpeta: {error}")



#Enviar archivos como json
def enviar_archivos(ruta, nombre_archivo):
    ruta_archivo = os.path.join(ruta, nombre_archivo)
    try:
        with open(ruta_archivo, 'rb') as archivo:
            datos = archivo.read(1024)
            while datos:
                # Serializar los datos a JSON
                datos_json = json.dumps(datos.decode())
                # Enviar los datos como JSON
                client.send(datos_json.encode())
                datos = archivo.read(1024)
            print(f"Archivo {ruta_archivo} enviado correctamente")
    except OSError as error:
        print(f"Error al enviar el archivo {ruta_archivo}: {error}")

#Funcion para enviar carpetas
def enviar_carpeta(ruta):
    try:
        for raiz, dirs, archivos in os.walk(ruta):
            for nombre_archivo in archivos:
                enviar_archivos(raiz, nombre_archivo)
    except OSError as error:
        print(f"Error al enviar la carpeta {ruta}: {error}")



if __name__ == "__main__":
    """ Staring a TCP socket. """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12345) #IP y puerto del servidor
    """ Connecting to the server. """
    client.connect(server_address) # Conectando al servidor

     
    msg=client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")

while True:
    opc=input("Elige tu opcion: \n 1.Para ver tu carpeta local \n 2.Para ver tu carpeta remota \n 3. Para salir \n")
    client.send(opc.encode(FORMAT))
    
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
    #client.send(opc2.encode(FORMAT))

        if opc=="1" and opc2=="1":
            mostrar_archivos_en_carpeta_actual()
        elif opc=="1" and opc2=="2":
            crear_carpeta()
        elif opc=="1" and opc2=="3":
            borrar_archivo_o_carpeta()
        elif opc=="1" and opc2=="4":
            cambiar_carpeta(ruta_raiz)
        elif opc=="1" and opc2=="7":
            break
        elif opc2=="7":
            break
        
    
    """ Closing the connection from the server. """
    client.close()
