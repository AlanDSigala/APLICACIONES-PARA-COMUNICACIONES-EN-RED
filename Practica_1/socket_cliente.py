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



def enviar_archivo():
    root = Tk.Tk()
    root.withdraw()  # Ocultar la ventana principal

    ruta_archivo = filedialog.askopenfilename(title="Selecciona el archivo para enviar")
    if ruta_archivo:
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
def enviar_carpeta():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as datos_socket:
        # Conectarse al servidor
        datos_socket.connect(('localhost', 1234))
        
        root = Tk.Tk()
        root.withdraw()  # Ocultar la ventana principal

        ruta_carpeta = filedialog.askdirectory(title="Selecciona la carpeta para enviar")
        if ruta_carpeta:
            try:
               
                # Enviar la ruta de la carpeta al servidor
                datos_socket.sendall(ruta_carpeta.encode())

                # Recorrer recursivamente la estructura de directorios
                estructura_directorios = {}
                for root, dirs, files in os.walk(ruta_carpeta):
                    archivos = {}
                    for nombre_archivo in files:
                        ruta_archivo = os.path.join(root, nombre_archivo)
                        with open(ruta_archivo, 'rb') as archivo:
                            contenido_archivo = archivo.read()
                        archivos[nombre_archivo] = contenido_archivo
                    estructura_directorios[root] = archivos
            
                # Serializar la estructura de directorios a JSON
                estructura_directorios_json = json.dumps(estructura_directorios)
                # Enviar la estructura de directorios como JSON
                datos_socket.sendall(estructura_directorios_json.encode())
            
                print(f"Carpeta {ruta_carpeta} enviada correctamente")
            except OSError as error:
                print(f"Error al enviar la carpeta {ruta_carpeta}: {error}")



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
            enviar_archivo()
        elif opc=="1" and opc2=="6":
            # Enviamos la opción "carpeta" al servidor
            client.sendall("carpeta".encode())
            enviar_carpeta()
        elif opc=="1" and opc2=="7":
            break
        elif opc2=="7":
            break
        
    
    """ Closing the connection from the server. """
    client.close()
