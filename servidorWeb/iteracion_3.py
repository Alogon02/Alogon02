# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 14:51:51 2021

@author: Alogon
"""

import sys
import socket
import threading 
import os 
import datetime

def head(mensaje):
    
    lista = mensaje.split()
    archivo = lista[1]        
    tamaño = str(os.path.getsize('data'+archivo))
    mod = datetime.datetime.fromtimestamp(os.path.getmtime('data'+archivo)).strftime("%a, %d %b %Y %H:%M:%S %Z")
    fecha = (datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S %Z"))
    server = ('Apache')
    respuesta =('HTTP/1.0 200 OK\nContent-Length: {}\nLast-Modified: {}\nDate: {}\nServer: {}\n'.format(tamaño, mod, fecha, server)).encode()
   
    return respuesta

def get_text(mensaje):
    
     lista = mensaje.split()
     archivo = lista[1] 
     with open('data' + archivo, "r", encoding= 'utf-8') as f:
         contenido = f.read()
     return contenido 
 
def get_image(mensaje):
    
     lista = mensaje.split()
     archivo = lista[1] 
     with open ('data' + archivo, 'rb') as f:
         contenido = f.read()
     return contenido 
 
def main():
    
    if len(sys.argv) != 2:
        print("Formato ServidorTCP <puerto>")
        sys.exit()
        # Comprueba que solo tenemos dos argumentos.
        
    try:
        
        puerto = int(sys.argv[1])
        socketServidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Creamos argumento y socket orientado a conexión.
        
        socketServidor.bind(("", puerto))
        # Asociamos el socket a una dirección y puerto.
        
        timeout = 300
        socketServidor.settimeout(timeout)
        # Establecemos timeout de 300 seg.
        
        print("Iniciando servidor en PUERTO: ", puerto)
        socketServidor.listen()
        # Ponemos el servidor en modo escucha.
        
        while True:
            socketCliente, direccion = socketServidor.accept()
            # Esperando petición de conexión de un cliente.
            
          
            def hilo(socketCliente):
                
                mensaje = socketCliente.recv(4096).decode('UTF-8')
                # Recibimos mensaje del cliente.
                try:
                    lista = mensaje.split('\n')
                    sublista = lista[0].split(' ')
    
                    print(sublista)
                    archivo = sublista[1]
                    
                    if archivo == '/':
                        archivo = '/index.html'
    
                     
                    if sublista[0] == 'GET':
                            
                           try: 
                                
                                if archivo.endswith('.txt'):
                                        filetype = 'text/plain'
                                        head(mensaje)
                                        respuesta = head(mensaje) + ('Content-Type: {}\n\n'.format(filetype) + get_text(mensaje)).encode()
                            
                                elif archivo.endswith('.gif'):
                                        filetype = 'image/gif'
                                        head(mensaje)
                                        respuesta = head(mensaje) + ('Content-Type: {}\n\n'.format(filetype)).encode() + get_image(mensaje)
                                        
                                elif archivo.endswith('.jpg'):
                                        filetype = 'image/jpeg'
                                        head(mensaje)
                                        respuesta = head(mensaje) + ('Content-Type: {}\n\n'.format(filetype)).encode() + get_image(mensaje) 
                                        
                                elif archivo.endswith('.html'):
                                        filetype = 'text/html'
                                        head(mensaje)
                                        respuesta = head(mensaje) + ('Content-Type: {}\n\n'.format(filetype) + get_text(mensaje)).encode()
                                        
                                else:
                                    filetype = "application/octet-stream"
                                    respuesta = ('HTTP/1.0 404 NOT FOUND\n\nArchivo no encontrado').encode()
                                    
                           except FileNotFoundError: 
                                respuesta = ('HTTP/1.0 404 NOT FOUND\n\nArchivo no encontrado').encode()
                           socketCliente.send(respuesta)
                           socketCliente.close()
                            
                    elif sublista[0] == 'HEAD':                
                                
                                try: 
                                
                                    if archivo.endswith('.txt'):
                                            filetype = 'text/plain'
                                            head(mensaje)
                                            respuesta = head(mensaje) + ('Content-Type: {}\n\n'.format(filetype)).encode() 
                                
                                    elif archivo.endswith('.gif'):
                                            filetype = 'image/gif'
                                            head(mensaje)
                                            respuesta = head(mensaje) + ('Content-Type: {}\n\n'.format(filetype)).encode()
                                            
                                    elif archivo.endswith('.jpg'):
                                            filetype = 'image/jpeg'
                                            head(mensaje)
                                            respuesta = head(mensaje) + ('Content-Type: {}\n\n'.format(filetype)).encode()
                                            
                                    elif archivo.endswith('.html'):
                                            filetype = 'text/html'
                                            head(mensaje)
                                            respuesta = head(mensaje) + ('Content-Type: {}\n\n'.format(filetype)).encode() 
                                            
                                    else:
                                        filetype = "application/octet-stream"
                                        respuesta = ('HTTP/1.0 404 NOT FOUND\n\nArchivo no encontrado').encode()
                                        
                                except FileNotFoundError: 
                                    respuesta = ('HTTP/1.0 404 NOT FOUND\n\nArchivo no encontrado').encode()
                                socketCliente.send(respuesta)
                                socketCliente.close()
                             
                    elif sublista[0]!= 'HEAD' or sublista[0]!='GET':
                            respuesta = ('HTTP/1.0 400 BAD REQUEST\n\nBad request').encode()
                            socketCliente.send(respuesta)
                            socketCliente.close()
                except:
                    respuesta = ('HTTP/1.0 400 BAD REQUEST\n\nBad request').encode()
                    socketCliente.send(respuesta)
                    socketCliente.close()
                
                
            threading.Thread(target=hilo,args=(socketCliente, )).start()
            # Creamos hilos de ejecución.

    except socket.timeout:
        print("{} segundos sin recibir nada.".format(timeout))
        # Captura excepción por timeout.
        
    except:
        print("Error: {}".format(sys.exc_info()[0]))
        raise
        # Captura excepción genérica.
        
    finally:
        socketServidor.close()
        # En cualquier caso se cierra el socket.
        
if __name__=="__main__":
    main()
