import socket
import threading

IP = "127.0.0.1"
PUERTO = 8000

clientes = []

#es para enviar un mensaje a todos los dispositivos conectados menos al emisor
def broadcast(mensaje, emisor):   
    for c in clientes:
        if c != emisor:
            try:
                c.send(mensaje.encode("utf-8"))   
            except:                     
                clientes.remove(c)     
                c.close()               #se cierra el socket

#hilo para manejar a cada cliente
def manejar_cliente(cliente, direccion):
    print(f"Conexion establecida con {direccion}")
    clientes.append(cliente)
    try:                 #bucle para escuchar mensajes del cliente
        while True:
            mensaje = cliente.recv(1024).decode("utf-8")    #llama al metodo recv del objeto socket
            if not mensaje:                                 
                break

            if mensaje.lower().strip() == "/salir":
                cliente.send("cerrado".encode("utf-8"))
                break
 
            #para ver el mensaje recibido y quien envio
            print(f"{direccion}: {mensaje}")
            broadcast(f"{direccion}: {mensaje}", cliente)    #llama a la funcion para reenviar mensajes a los demas clientes
    except Exception as error:       #aca se guarda el objeto de la excepcion en la var error
        print(f"Error con {direccion}: {error}")
    finally:
        if cliente in clientes:
            clientes.remove(cliente)
        cliente.close()        #cierra formalmente la conexion de red tcp, libera el puerto local que usaba el socket
        print(f" {direccion} se desconecto")

#para crear el socket del servidor
def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((IP, PUERTO))              #asocia el socket a la direccion
    servidor.listen()                #socket en modo escucha
    servidor.settimeout(1.0)   #espera 1s por nuevas conexiones
    print(f"Servidor escuchando en {IP}:{PUERTO}")

    try:
        while True:
            try:
                cliente, direccion = servidor.accept()    #se bloquea hasta que un cliente se conecta 
                hilo = threading.Thread(target=manejar_cliente, args=(cliente, direccion), daemon=True)  #crea un hilo nuevo por cliente
                hilo.start()
            except socket.timeout:   #si en 1s nadie se conecta lanza la excepcion
                continue
    except KeyboardInterrupt:
        print("\nCerrando servidor...")
    finally:
        for c in clientes:
            c.close()         #para cerrar todos los sockets de clientes y libera el puerto usado y los recursos de SO
        servidor.close()
        print("Servidor cerrado correctamente")

if __name__ == "__main__":
    iniciar_servidor()

