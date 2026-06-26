import socket
import threading
import time

SERVIDOR_IP = "127.0.0.1"
SERVIDOR_PUERTO = 8000

#para escuchar los mensajes del servidor
def escuchar_servidor(sock):
    while True:
        try:
            mensaje = sock.recv(1024).decode("utf-8")    
            if not mensaje:                    
                print("Conexion perdida con el servidor.")
                return False                #para indicar que se termino la escucha
            if mensaje.lower() == "cerrado":    #detecta mensaje enviado por el serv
                print("El servidor cerro la conexion.")
                return False     #para detener la escucha
            print(f"\n{mensaje}")      #Si no se cumplio ninguna condicion anterior
        except:
            print("Error en la conexion con el servidor.")
            return False

#para intentar conectarse al servidor si se perdio la conexion
def conectar_con_reintentos():
    while True:
        try:
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cliente.connect((SERVIDOR_IP, SERVIDOR_PUERTO))
            print(f"Conectado al servidor ({SERVIDOR_IP}:{SERVIDOR_PUERTO})")
            print("Ya puedes escribir un mensaje para enviar.")
            return cliente       #devuelve el socket ya conectado al resto del programa y rompe el bucle WT
        except ConnectionRefusedError:    #no hay ningun servidor escuchando en esa IP y puerto
            print("Servidor no disponible. Reintentando en 3 segundos...")
            time.sleep(3)

#para mantener al cliente conectado al servidor
def iniciar_cliente():
    while True:
        cliente = conectar_con_reintentos()

        #hilo para escuchar al servidor
        hilo = threading.Thread(target=escuchar_servidor, args=(cliente,), daemon=True)
        hilo.start()

        try:
            while True:
                mensaje = input("")
                if mensaje.lower().strip() == "/salir":
                    cliente.send(mensaje.encode("utf-8"))
                    cliente.close()
                    print("Saliste del chat.")
                    return      #para salir completamente de la funcion
                cliente.send(mensaje.encode("utf-8"))     #si el mensaje no es salir
        except (BrokenPipeError, ConnectionResetError, OSError):
            print("Conexion interrumpida. Intentando reconectar...")
            time.sleep(3)
            continue  #vuelve al bucle principal para reconectar
        except KeyboardInterrupt:
            print("\nCliente cerrado por el usuario.")
            cliente.close()
            break

if __name__ == "__main__":
    iniciar_cliente()

