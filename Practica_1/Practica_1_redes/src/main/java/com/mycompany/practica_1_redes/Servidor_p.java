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
        
            int pto = 9999;
              ServerSocket s = new ServerSocket(pto);
              ServerSocket s2 = new ServerSocket(pto+1);
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
                  System.out.println("Cliente conectado desde "+cl.getInetAddress()+":"+cl.getPort());
                  DataInputStream dis = new DataInputStream(cl.getInputStream());
                  PrintWriter salida = new PrintWriter(cl.getOutputStream(), true);
                  InputStream is = cl.getInputStream();
                  String nombre = dis.readUTF();
                  long tam = dis.readLong();
                  // Crear un lector de entrada para recibir los datos del cliente en formato UTF-8
                   BufferedReader lector = new BufferedReader(new InputStreamReader(cl.getInputStream(), "UTF-8"));
                   String cadenaJSON = lector.readLine();
                  
                  // Convertir JSON a objeto
                    JSONParser parser = new JSONParser();
                    JSONObject jsonObject = (JSONObject) parser.parse(cadenaJSON);

                    // Extraer datos del objeto JSON
                    int numero = Integer.parseInt(jsonObject.get("numero").toString());
                    String cadena = (String) jsonObject.get("cadena");
                    //String nom = (String) jsonObject.get("nombre");
                    System.out.println("numero"+numero);
                    System.out.println("cadena"+cadena);
                    //System.out.println("nom"+nom);
                    //while(numero != 7){
                        if(numero == 1){
                            System.out.println("Opcion 1");
                            //1.- Listado de directorios 
                            File LFR = new File (ruta_archivos_FR);

                            // Verificar si la carpeta principal existe
                            if (LFR.exists() && LFR.isDirectory()) {
                              // Obtener una matriz de objetos File que representan los archivos y carpetas dentro de la carpeta principal
                              File[] archivosYCarpetas = LFR.listFiles();

                              // Iterar sobre la matriz para imprimir los nombres de los archivos y carpetas
                              System.out.println("Contenido de la carpeta principal:");
                              for (File archivoOcarpeta : archivosYCarpetas) {
                                  if (archivoOcarpeta.isDirectory()) {
                                      // Imprimir el nombre de la carpeta
                                      System.out.println("Carpeta: " + archivoOcarpeta.getName()+". Se puede editar: "+ archivoOcarpeta.canWrite());

                                      // Obtener los archivos y carpetas dentro de esta carpeta
                                      File[] archivosEnSubcarpeta = archivoOcarpeta.listFiles();

                                      // Iterar sobre la subcarpeta para imprimir sus archivos y carpetas
                                      System.out.println("Contenido de la subcarpeta " + archivoOcarpeta.getName() + ":");
                                      for (File archivoEnSubcarpeta : archivosEnSubcarpeta) {
                                          if (archivoEnSubcarpeta.isDirectory()) {
                                              System.out.println("Subcarpeta: " + archivoEnSubcarpeta.getName() + ". Se puede editar:  " + archivoEnSubcarpeta.canWrite());
                                          } else {
                                              System.out.println("Archivo: " + archivoEnSubcarpeta.getName());
                                          }
                                      }
                                  } else {
                                      System.out.println("Archivo: " + archivoOcarpeta.getName());
                                  }
                              }
                          } else {
                              System.out.println("La carpeta principal no existe.");
                          }
                        } else if (numero == 2) {
                            System.out.println("Opcion 2");
                            String lugar = cadena;
                            File elim_AoD = new File(ruta_archivos_FR +"\\"+lugar);
                            //eliminacion de un directorio
                            if (elim_AoD.exists() && elim_AoD.isDirectory()) {
                                // Intentar eliminar el directorio
                                if (elim_AoD.delete()) {
                                    System.out.println("Directorio eliminado exitosamente.");
                                } else {
                                    System.out.println("No se pudo eliminar el directorio.");
                                }
                            }else if(elim_AoD.exists() && elim_AoD.isFile()){
                                 // Intentar eliminar el archivo
                                if (elim_AoD.delete()) {
                                    System.out.println("Archivo eliminado exitosamente.");
                                } else {
                                    System.out.println("No se pudo eliminar el archivo.");
                                }
                            } else {
                                System.out.println("La direccion del archivo/carpeta no es valida.");
                            }
                        } else if (numero == 3) {
                            // Obtener el nombre del archivo del JSON
                            String nombreArchivo = (String) jsonObject.get(nombre);

                            // Crear el archivo en el servidor
                            File archivo = new File(nombreArchivo);
                            FileOutputStream fos = new FileOutputStream(archivo);

                            // Leer los datos del archivo del InputStream del socket y escribirlos en el archivo
                            
                            byte[] buffer = new byte[4096];
                            int bytesRead;
                            while ((bytesRead = is.read(buffer)) != -1) {
                                fos.write(buffer, 0, bytesRead);
                            }

                            // Cerrar flujos
                            fos.close();
                            is.close();

                            System.out.println("Archivo recibido y guardado como: " + nombreArchivo);

                        } else if (numero == 4) {
                            System.out.println("Opcion 4");
                           JFileChooser jfc = new JFileChooser();
                            jfc.setFileSelectionMode(JFileChooser.FILES_AND_DIRECTORIES);
                            int resultado = jfc.showOpenDialog(null);

                            if (resultado == JFileChooser.APPROVE_OPTION) {
                                // Obtener el archivo o carpeta seleccionado por el cliente
                                File archivoOCarpeta = jfc.getSelectedFile();

                                // Obtener el flujo de salida para enviar los datos al servidor
                                DataOutputStream dos = new DataOutputStream(cl.getOutputStream());

                                // Enviar el nombre del archivo o carpeta al servidor
                                dos.writeUTF(archivoOCarpeta.getName());

                                // Si es un archivo, enviar los datos del archivo al servidor
                                if (archivoOCarpeta.isFile()) {
                                    // Enviar la bandera indicando que es un archivo
                                    dos.writeBoolean(true);

                                    // Enviar el tamaño del archivo al servidor
                                    dos.writeLong(archivoOCarpeta.length());

                                    // Enviar los datos del archivo al servidor
                                    FileInputStream fis = new FileInputStream(archivoOCarpeta);
                                    byte[] buffer = new byte[4096];
                                    int bytesRead;
                                    while ((bytesRead = fis.read(buffer)) != -1) {
                                        dos.write(buffer, 0, bytesRead);
                                    }
                                    fis.close();
                                } else { // Si es una carpeta, enviar los nombres de los archivos en la carpeta al servidor
                                    // Enviar la bandera indicando que es una carpeta
                                    dos.writeBoolean(false);

                                    // Enviar los nombres de los archivos en la carpeta al servidor
                                    File[] archivosEnCarpeta = archivoOCarpeta.listFiles();
                                    dos.writeInt(archivosEnCarpeta.length);
                                    for (File archivo : archivosEnCarpeta) {
                                        dos.writeUTF(archivo.getName());
                                    }
                                }

                                // Cerrar flujos y conexiones
                                dos.close();
                                cl.close();
                                System.out.println("Archivo o carpeta enviado.");
                            } else {
                                System.out.println("Operación cancelada por el usuario.");
                            }


                        } else if (numero == 5) {
                            System.out.println("Opcion 5");
                            String nueva_ruta = cadena;
                            File NDirect = new File (ruta_archivos_FR +"\\"+nueva_ruta+"\\");

                            // Verificar si el directorio existe y es un directorio válido
                            if (NDirect.exists() && NDirect.isDirectory()) {
                                // Establecer el nuevo directorio como el directorio de trabajo actual
                                System.setProperty("user.dir", ruta_archivos_FR+"\\"+nueva_ruta);
                                System.out.println("Directorio principal cambiado a: " + NDirect);
                            } else {
                                System.out.println("El directorio especificado no existe o no es válido.");
                            }
                        } else if (numero == 6) {
                            System.out.println("Opcion 6");
                            String directorioActual = System.getProperty("user.dir");

                            // Nombre de la nueva carpeta
                            String nombreNuevaCarpeta = cadena;

                            // Crear un objeto File para representar la nueva carpeta
                            File nuevaCarpeta = new File(directorioActual, nombreNuevaCarpeta);

                            // Verificar si la carpeta ya existe
                            if (!nuevaCarpeta.exists()) {
                                // Intentar crear la nueva carpeta
                                if (nuevaCarpeta.mkdir()) {
                                    System.out.println("La carpeta '" + nombreNuevaCarpeta + "' ha sido creada en el directorio actual.");
                                } else {
                                    System.out.println("No se pudo crear la carpeta '" + nombreNuevaCarpeta + "'.");
                                }
                            } else {
                                System.out.println("La carpeta '" + nombreNuevaCarpeta + "' ya existe en el directorio actual.");
                            }
                        } else if (numero == 7) {
                            // Desconectar al cliente
                            salida.println("Desconectándote del servidor. Adiós!");
                            cl.close(); // Cerrar el socket del cliente
                            s.close(); // Cerrar el socket del servidor
                            System.exit(0); // Terminar el programa del servidor
                        } else {
                            salida.println("Opción no válida.");
                        }
                    
                    //}
                    
              
                    dis.close();
                  cl.close();
              }//for 
        
              
              //cierre del servidor
              
        }catch(Exception e){
            e.printStackTrace();
        }
        
    }//main
}//class
