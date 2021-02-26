# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 15:50:31 2021

@author: Alogon
"""

import sys
import socket

def main():
    
    if len(sys.argv) != 2:
        print("Formato ServidorTCP <puerto>")
        sys.exit()
        #Comprueba que solo tenemos dos argumentos.
        
    try:
        puerto = int(sys.argv[1])
        socketServidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Creamos argumento y socket orientado a conexión.
        
        socketServidor.bind(("", puerto))
        # Asociamos el socket a una dirección y puerto.
        
        timeout = 300
        socketServidor.settimeout(timeout)
        # Establecemos timeout.
        
        print("Iniciando servidor en PUERTO: ",puerto)
        socketServidor.listen()
        # Ponemos el servidor en modo escucha.
        
        while True:
            socketCliente, direccion = socketServidor.accept()
            # Esperando petición de conexión de un cliente.
            
            mensaje = socketCliente.recv(4096)
            # Recibimos mensaje del cliente.
            
            print("Recibido mensaje: {} de: {}:{}".format(mensaje.decode('UTF-8'),direccion[0],direccion[1]))
            # Mostramos el contenido del mensaje.
            
            socketCliente.send(mensaje)
            # Enviamos el mismo mensaje recibido a través del socket del cliente.
            
            socketCliente.close()
            # Cerramos el socketCliente.

    except socket.timeout:
        print("{} segundos sin recibir nada.".format(timeout))
        # Captura excepción por timeout.
        
    except:
        print("Error: {}".format(sys.exc_info()[0]))
        raise
        # Captura excepción genérica.
        
    finally:
        socketServidor.close()
        # En cualquier caso cerramos el socket.

if __name__=="__main__":
    main()