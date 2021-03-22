# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 19:53:07 2021

@author: Alogon
"""

import sys
import socket
import threading 

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
                
                lista = mensaje.split('\n')
                sublista = lista[0].split(' ')
                if len(sublista)==3:
                    respuesta = ('HTTP/1.0 400 BAD REQUEST\n\nBad request').encode()
                    socketCliente.send(respuesta)
                print(sublista)
                archivo = sublista[1]
                
                if archivo == '/':
                    archivo = '/index.html'
            
                
                try:    
                    if sublista[0] == 'GET':
                        
                       try: 
                            
                            if archivo.endswith('.txt'):
                                with open('data' + archivo, "r") as f:
                                    contenido = f.read()
                                    respuesta = (contenido).encode('utf-8') 
                        
                        
                         
                                    
                            elif archivo.endswith('.html'):
                                with open ('data' + archivo,'r', encoding='utf-8') as f:
                                    contenido = f.read()
                                    respuesta = (contenido).encode('utf-8') 
                                    
                            else:
                                respuesta = ('HTTP/1.0 200 OK\n\nNo se ha identificado el formato del fichero.').encode()
                                
                       except FileNotFoundError: 
                            respuesta = ('HTTP/1.0 404 NOT FOUND\n\nArchivo no encontrado').encode()
                       
                        
                    elif sublista[0] == 'HEAD':                
                            
                            try: 
                                
                                if archivo.endswith('.txt'):
                                    with open ('data' + archivo, encoding= 'UTF-8') as f:
                                        respuesta =('\nHTTP/1.0 200 OK\nInformacion\n\n').encode()
                               
                                        
                                elif archivo.endswith('.html'):
                                    with open ('data' + archivo, encoding= 'UTF-8') as f:
                                        respuesta =('\nHTTP/1.0 200 OK\nInformacion\n\n').encode()
                                       
                                    
                                else:
                                    respuesta = ('HTTP/1.0 200 OK\n\nNo se ha identificado el formato del fichero.').encode()
                                
                            except FileNotFoundError: 
                                respuesta = ('HTTP/1.0 404 NOT FOUND\n\nArchivo no encontrado').encode()
                            
                         
                except:
                    respuesta = ('HTTP/1.0 400 BAD REQUEST\n\nBad request').encode()
                socketCliente.send(respuesta)   
                
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