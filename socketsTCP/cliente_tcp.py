# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 15:02:16 2021

@author: Alogon
"""

import sys
import socket

def main():
    
    if len(sys.argv) != 4:
        print("Formato ClienteTCP <maquina> <puerto> <mensaje>")
        sys.exit()
        # Comprueba que solo tenemos 4 argumentos.
    try:
        maquina = sys.argv[1]
        puerto =int(sys.argv[2])
        mensaje = sys.argv[3]
        socketCliente =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Creamos argumentos y socket orientado a conexión.
        
        timeout=300
        socketCliente.settimeout(timeout)
        # Establecemos timeout.
        
        socketCliente.connect((maquina,puerto))
        # Conectamos con el servidor.
        
        socketCliente.sendto(mensaje.encode('UTF-8'),(maquina, puerto))
        # Enviamos el mensaje.
        
        mensajeEco, a = socketCliente.recvfrom(len(mensaje))
        print("CLIENTE: Recibido {} de {}:{}".format(mensajeEco.decode('UTF-8'),maquina,puerto))
        # Decodificamos y mostramos el mensaje recibido.
        
    except socket.timeout:
        print("{} segundos sin recibir nada.".format(timeout))
        # Captura excepción por timeout.
        
    except:
       print("Error: {}".format(sys.exc_info()[0]))
       raise
       # Captura excepción genérica.
       
    finally:
        socketCliente.close()
        # En cualquier caso cerramos el socket.
        
if __name__ == "__main__":
    main()
