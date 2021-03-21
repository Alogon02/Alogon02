# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 12:34:57 2021

@author: Alogon
"""

import sys
import socket
import threading 
import os 
import datetime

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
                                    with open('data' + archivo, "r") as f:
                                        filetype = 'text/txt'
                                        tamaño = str(os.path.getsize('data'+archivo))
                                        mod = datetime.datetime.fromtimestamp(os.path.getmtime('data'+archivo)).strftime("%a, %d %b %Y %H:%M:%S %Z")
                                        fecha = (datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S %Z"))
                                        server = ('Alfonso')
                                        contenido = f.read()
                                        respuesta =('\nHTTP/1.0 200 OK\n Content-Length: {}\n Last-Modified: {}\n Date: {}\n Server:{}\n Content-Type: {}\n\n'.format(
                                            tamaño, mod, fecha, server, filetype) + contenido).encode()
                            
                                elif archivo.endswith('.gif'):
                                    with open ('data' + archivo, 'rb') as f:
                                        filetype = 'image/gif'
                                        tamaño = str(os.path.getsize('data'+archivo))
                                        mod = datetime.datetime.fromtimestamp(os.path.getmtime('data'+archivo)).strftime("%a, %d %b %Y %H:%M:%S %Z")
                                        fecha = (datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S %Z"))
                                        server = ('Alfonso')
                                        contenido = f.read() 
                                        respuesta = ('\nHTTP/1.0 200 OK\n Content-Length: {}\n Last-Modified: {}\n Date: {}\n Server:{}\n Content-Type: {}\n\n'.format(
                                            tamaño, mod, fecha, server, filetype)).encode()+contenido
                                        
                                elif archivo.endswith('.jpg'):
                                    with open ('data' + archivo, 'rb') as f:
                                        filetype = 'image/jpeg'
                                        tamaño = str(os.path.getsize('data'+archivo))
                                        mod = datetime.datetime.fromtimestamp(os.path.getmtime('data'+archivo)).strftime("%a, %d %b %Y %H:%M:%S %Z")
                                        fecha = (datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S %Z"))
                                        server = ('Alfonso')
                                        contenido = f.read() 
                                        respuesta = ('\nHTTP/1.0 200 OK\n Content-Length: {}\n Last-Modified: {}\n Date: {}\n Server:{}\n Content-Type: {}\n\n'.format(
                                            tamaño, mod, fecha, server, filetype)).encode()+contenido
                                        
                                elif archivo.endswith('.html'):
                                    with open ('data' + archivo,'r', encoding='utf-8') as f:
                                        filetype = 'text/html'
                                        tamaño = str(os.path.getsize('data'+archivo))
                                        mod = datetime.datetime.fromtimestamp(os.path.getmtime('data'+archivo)).strftime("%a, %d %b %Y %H:%M:%S %Z")
                                        fecha = (datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S %Z"))
                                        server = ('Alfonso')
                                        contenido = f.read()
                                        respuesta = ('\nHTTP/1.0 200 OK\n Content-Length: {}\n Last-Modified: {}\n Date: {}\n Server:{}\n Content-Type: {}\n\n'.format(
                                            tamaño, mod, fecha, server, filetype) + contenido).encode('utf-8') 
                                        
                                else:
                                    filetype = "application/octet-stream"
                                    respuesta = ('HTTP/1.0 200 OK\n\nNo se ha identificado el formato del fichero.').encode()
                                    
                           except FileNotFoundError: 
                                respuesta = ('HTTP/1.0 404 NOT FOUND\n\nArchivo no encontrado').encode()
                           socketCliente.send(respuesta)
                           socketCliente.close()
                            
                    elif sublista[0] == 'HEAD':                
                                
                                try: 
                                
                                    if archivo.endswith('.txt'):
                                        with open('data' + archivo, "r") as f:
                                            filetype = 'text/txt'
                                            tamaño = str(os.path.getsize('data'+archivo))
                                            mod = datetime.datetime.fromtimestamp(os.path.getmtime('data'+archivo)).strftime("%a, %d %b %Y %H:%M:%S %Z")
                                            fecha = (datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S %Z"))
                                            server = ('Alfonso')
                                            contenido = f.read()
                                            respuesta =('\nHTTP/1.0 200 OK\n Content-Length: {}\n Last-Modified: {}\n Date: {}\n Server:{}\n Content-Type: {}\n\n'.format(
                                                tamaño, mod, fecha, server, filetype) + contenido).encode()
                                
                                    elif archivo.endswith('.gif'):
                                        with open ('data' + archivo, 'rb') as f:
                                            filetype = 'image/gif'
                                            tamaño = str(os.path.getsize('data'+archivo))
                                            mod = datetime.datetime.fromtimestamp(os.path.getmtime('data'+archivo)).strftime("%a, %d %b %Y %H:%M:%S %Z")
                                            fecha = (datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S %Z"))
                                            server = ('Alfonso')
                                            contenido = f.read() 
                                            respuesta = ('\nHTTP/1.0 200 OK\n Content-Length: {}\n Last-Modified: {}\n Date: {}\n Server:{}\n Content-Type: {}\n\n'.format(
                                                tamaño, mod, fecha, server, filetype)).encode()+contenido
                                            
                                    elif archivo.endswith('.jpg'):
                                        with open ('data' + archivo, 'rb') as f:
                                            filetype = 'image/jpeg'
                                            tamaño = str(os.path.getsize('data'+archivo))
                                            mod = datetime.datetime.fromtimestamp(os.path.getmtime('data'+archivo)).strftime("%a, %d %b %Y %H:%M:%S %Z")
                                            fecha = (datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S %Z"))
                                            server = ('Alfonso')
                                            contenido = f.read() 
                                            respuesta = ('\nHTTP/1.0 200 OK\n Content-Length: {}\n Last-Modified: {}\n Date: {}\n Server:{}\n Content-Type: {}\n\n'.format(
                                                tamaño, mod, fecha, server, filetype)).encode()
                                            
                                    elif archivo.endswith('.html'):
                                        with open ('data' + archivo,'r', encoding='utf-8') as f:
                                            filetype = 'text/html'
                                            tamaño = str(os.path.getsize('data'+archivo))
                                            mod = datetime.datetime.fromtimestamp(os.path.getmtime('data'+archivo)).strftime("%a, %d %b %Y %H:%M:%S %Z")
                                            fecha = (datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S %Z"))
                                            server = ('Alfonso')
                                            contenido = f.read()
                                            respuesta = ('\nHTTP/1.0 200 OK\n Content-Length: {}\n Last-Modified: {}\n Date: {}\n Server:{}\n Content-Type: {}\n\n'.format(
                                                tamaño, mod, fecha, server, filetype)).encode('utf-8') 
                                            
                                    else:
                                        filetype = "application/octet-stream"
                                        respuesta = ('HTTP/1.0 200 OK\n\nNo se ha identificado el formato del fichero.').encode()
                                        
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