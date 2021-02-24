# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 11:45:26 2021

@author: Alogon
"""

import sys
import socket 

def main():
    if len(sys.argv) != 4:
        print("Formato ClienteUDP <maquina> <puerto> <mensaje>")
        sys.exit()
    try:
        maquina = sys.argv[1]
        puerto = int(sys.argv[2])
        mensaje = sys.argv[3]
        socketCliente = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)


        # Instrucciones sockets
        ...
    except socket.timeout:
        # Captura excepci´on si el tiempo de espera se agota.
        print("{} segundos sin recibir nada.".format(timeout))
    except:
        # Captura excepci´on gen´erica.
        print("Error: {}".format(sys.exc_info()[0]))
        raise
    finally:
        # En cualquier caso cierra el socket.
        socketCliente.close()
