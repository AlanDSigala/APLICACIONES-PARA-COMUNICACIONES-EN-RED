/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany.practica_1_redes;

import java.net.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import org.json.simple.parser.JSONParser;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

/**
 *
 * @author ajbso
 */
public class Servidor_p {
    public static void main(String[] args){
        try{
        
            int pto = 12345;
            int pto2 = 1234;
              ServerSocket s = new ServerSocket(pto);
              ServerSocket s2 = new ServerSocket(pto2);
              s.setReuseAddress(true);
              System.out.println("Servidor iniciado esperando respuesta..");
              
              //Inicializacion de las carpetas tanto local como remota
                //remota
                File FR = new File ("");
                String rutaR = FR.getAbsolutePath();
                String carpetaR = "CarpetaRemota";
                String ruta_archivos_FR = rutaR+"\\"+carpetaR+"\\";
                System.out.println(ruta_archivos_FR);
              
              for(;;){
                  Socket cl = s.accept();
                  System.out.println("Cliente conectado desde "+cl.getInetAddress()+" : "+cl.getPort());
                  //declaracion de receptores de flujo de salida y entrada de datos con el cliente
                  DataInputStream dis = new DataInputStream(cl.getInputStream());
                  DataOutputStream dos = new DataOutputStream(cl.getOutputStream());
                  InputStream inputStream = cl.getInputStream();
                  InputStreamReader inputStreamReader = new InputStreamReader(inputStream);
                  BufferedReader bufferedReader = new BufferedReader(inputStreamReader);
                  
                  
                  System.out.println("Enviando mensaje...");
                  
                  //contestando al cliente
                  String mensaj = "Conexión establecida con el servidor.";
                  dos.writeUTF(mensaj);
                  
                  // Leer el mensaje enviado por el cliente
                  String mensaje = bufferedReader.readLine();
                  System.out.println("Mensaje recibido del cliente: " + mensaje);
                    
                    while(true){
                    String opc = dis.readUTF();
                        if(opc.equals("1")){
                            System.out.println("Opcion 1, Lista de directorio");
                            //1.- Listado de directorios 
                            File LFR = new File (ruta_archivos_FR);

                            // Verificar si la carpeta principal existe
                            if (LFR.exists() && LFR.isDirectory()) {
                              // Obtener una matriz de objetos File que representan los archivos y carpetas dentro de la carpeta principal
                              File[] archivosYCarpetas = LFR.listFiles();

                              // Iterar sobre la matriz para imprimir los nombres de los archivos y carpetas
                              System.out.println("Contenido de la carpeta principal:");
                              dos.writeUTF("Contenido de la carpeta principal:");
                              for (File archivoOcarpeta : archivosYCarpetas) {
                                  if (archivoOcarpeta.isDirectory()) {
                                      // Imprimir el nombre de la carpeta
                                      dos.writeUTF("Carpeta: " + archivoOcarpeta.getName()+". Se puede editar: "+ archivoOcarpeta.canWrite());

                                      // Obtener los archivos y carpetas dentro de esta carpeta
                                      File[] archivosEnSubcarpeta = archivoOcarpeta.listFiles();

                                      // Iterar sobre la subcarpeta para imprimir sus archivos y carpetas
                                      System.out.println("Contenido de la subcarpeta " + archivoOcarpeta.getName() + ":");
                                      dos.writeUTF("Contenido de la subcarpeta " + archivoOcarpeta.getName() + ":");
                                      for (File archivoEnSubcarpeta : archivosEnSubcarpeta) {
                                          if (archivoEnSubcarpeta.isDirectory()) {
                                              System.out.println("Subcarpeta: " + archivoEnSubcarpeta.getName() + ". Se puede editar:  " + archivoEnSubcarpeta.canWrite());
                                              dos.writeUTF("Subcarpeta: " + archivoEnSubcarpeta.getName() + ". Se puede editar:  " + archivoEnSubcarpeta.canWrite());
                                          } else {
                                              System.out.println("Archivo: " + archivoEnSubcarpeta.getName());
                                              dos.writeUTF("Archivo: " + archivoEnSubcarpeta.getName());
                                          }
                                      }
                                  } else {
                                      System.out.println("Archivo: " + archivoOcarpeta.getName());
                                      dos.writeUTF("Archivo: " + archivoOcarpeta.getName());
                                  }
                              }
                          } else {
                              System.out.println("La carpeta principal no existe.");
                              dos.writeUTF("La carpeta principal no existe.");
                          }
                        } else if (opc.equals("2")) {
                            System.out.println("Opcion 2, nueva carpeta");
                            String directorioActual = System.getProperty("user.dir");

                            // Nombre de la nueva carpeta
                            String nombreNuevaCarpeta = "";

                            // Crear un objeto File para representar la nueva carpeta
                            File nuevaCarpeta = new File(directorioActual, nombreNuevaCarpeta);

                            // Verificar si la carpeta ya existe
                            if (!nuevaCarpeta.exists()) {
                                // Intentar crear la nueva carpeta
                                if (nuevaCarpeta.mkdir()) {
                                    System.out.println("La carpeta '" + nombreNuevaCarpeta + "' ha sido creada en el directorio actual.");
                                    dos.writeUTF("La carpeta '" + nombreNuevaCarpeta + "' ha sido creada en el directorio actual.");
                                } else {
                                    System.out.println("No se pudo crear la carpeta '" + nombreNuevaCarpeta + "'.");
                                    dos.writeUTF("No se pudo crear la carpeta '" + nombreNuevaCarpeta + "'.");
                                }
                            } else {
                                System.out.println("La carpeta '" + nombreNuevaCarpeta + "' ya existe en el directorio actual.");
                                dos.writeUTF("La carpeta '" + nombreNuevaCarpeta + "' ya existe en el directorio actual.");
                            }
                        } else if (opc.equals("3")) {
                            System.out.println("Opcion 3, borrado de carpeta");
                            String lugar = "";
                            File elim_AoD = new File(ruta_archivos_FR +"\\"+lugar);
                            //eliminacion de un directorio
                            if (elim_AoD.exists() && elim_AoD.isDirectory()) {
                                // Intentar eliminar el directorio
                                if (elim_AoD.delete()) {
                                    System.out.println("Directorio eliminado exitosamente.");
                                    dos.writeUTF("Directorio eliminado exitosamente.");
                                } else {
                                    System.out.println("No se pudo eliminar el directorio.");
                                    dos.writeUTF("No se pudo eliminar el directorio.");
                                }
                            }else if(elim_AoD.exists() && elim_AoD.isFile()){
                                 // Intentar eliminar el archivo
                                if (elim_AoD.delete()) {
                                    System.out.println("Archivo eliminado exitosamente.");
                                    dos.writeUTF("Archivo eliminado exitosamente.");
                                } else {
                                    System.out.println("No se pudo eliminar el archivo.");
                                    dos.writeUTF("No se pudo eliminar el archivo.");
                                }
                            } else {
                                System.out.println("La direccion del archivo/carpeta no es valida.");
                                dos.writeUTF("La direccion del archivo/carpeta no es valida.");
                            }

                        } else if (opc.equals("4")) {
                            System.out.println("Opcion 4, cambiar path");
                            String nueva_ruta = "";
                            File NDirect = new File (ruta_archivos_FR +"\\"+nueva_ruta+"\\");
                            ruta_archivos_FR = ruta_archivos_FR +"\\"+nueva_ruta+"\\";

                            // Verificar si el directorio existe y es un directorio válido
                            if (NDirect.exists() && NDirect.isDirectory()) {
                                // Establecer el nuevo directorio como el directorio de trabajo actual
                                System.setProperty("user.dir", ruta_archivos_FR+"\\"+nueva_ruta);
                                System.out.println("Directorio principal cambiado a: " + NDirect);
                                dos.writeUTF("Directorio principal cambiado a: " + NDirect);
                                
                            } else {
                                System.out.println("El directorio especificado no existe o no es válido.");
                                dos.writeUTF("El directorio especificado no existe o no es válido.");
                            }

                        } else if (opc.equals("5")) {
                            System.out.println("Opcion 5, recibir un archivo");
                            try {
                            System.out.println("Esperando conexiones entrantes en el puerto " + pto2 + "...");

                            while (true) {
                                Socket clientSocket = s2.accept();
                                System.out.println("Cliente conectado desde " + clientSocket.getInetAddress());

                                // Recibir el nombre del archivo
                                String nombreArchivo = dis.readUTF();

                                // Recibir y guardar el archivo
                                FileOutputStream fos = new FileOutputStream(nombreArchivo);
                                byte[] buffer = new byte[4096];
                                int bytesRead;
                                while ((bytesRead = dis.read(buffer)) != -1) {
                                    fos.write(buffer, 0, bytesRead);
                                }
                                fos.close();
                                System.out.println("Archivo '" + nombreArchivo + "' recibido y guardado correctamente.");
                                dos.writeUTF("Archivo '" + nombreArchivo + "' recibido y guardado correctamente.");
                            }
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                            s2.close();
                        } else if (opc.equals("6")) {
                            System.out.println("opcion 6, recibir una carpeta");
                        } else if (opc.equals("7")) {
                            // Desconectar al cliente
                            System.out.println("Desconectandose del servidor. Adios!");
                            dos.writeUTF("Desconectándote del servidor. Adiós!");
                            cl.close(); // Cerrar el socket del cliente
                            s.close(); // Cerrar el socket del servidor
                            System.exit(0); // Terminar el programa del servidor
                        } else {
                            System.out.println("Opcion no valida");
                            dos.writeUTF("Opción no válida.");
                        }
                     
                  dos.close();
                  dis.close();
                  cl.close();
                  }
              }//for 
        
              
              //cierre del servidor
              
        }catch(Exception e){
            e.printStackTrace();
        }//try
        
    }//main
}//class
