import socket
import threading

IP = "127.0.0.1"
PUERTO = 8000

CANTIDAD_MENSAJE = 200
clientes = []

def validar_mensaje(mensaje):
    if not mensaje:
        return False

    if mensaje.strip() == "":
        return False

    if len(mensaje) > CANTIDAD_MENSAJE:
        return False

    return True

def salir(mensaje):
    return mensaje.lower().strip() == "/salir" 

def formatear_mensaje(direccion, mensaje):
    return f"{direccion}: {mensaje}"


def agregar_cliente(clientes_conectados, cliente):
    clientes_conectados.append(cliente)


def eliminar_cliente(clientes_conectados, cliente):
    if cliente in clientes_conectados:
        clientes_conectados.remove(cliente)

#es para enviar un mensaje a todos los dispositivos conectados menos al emisor
def broadcast(mensaje, emisor,clientes_conectados):   
    for c in clientes_conectados[:]:
        if c != emisor:
            try:
                c.send(mensaje.encode("utf-8"))   
            except:                     
                eliminar_cliente(clientes_conectados, c)    
                c.close()               #se cierra el socket

              

#hilo para manejar a cada cliente
def manejar_cliente(cliente, direccion):
    print(f"Conexion establecida con {direccion}")
    agregar_cliente(clientes, cliente)
    try:                 #bucle para escuchar mensajes del cliente
        while True:
            mensaje = cliente.recv(1024).decode("utf-8")    #llama al metodo recv del objeto socket
            if not mensaje:                                 
                break

            if salir(mensaje):
                cliente.send("cerrado".encode("utf-8"))
                break
            if not validar_mensaje(mensaje):
                cliente.send("mensaje invalido".encode("utf-8"))
                continue

            mensaje_formateado = formatear_mensaje(direccion, mensaje)
            print(mensaje_formateado)
            broadcast(mensaje_formateado, cliente, clientes)
 
    except Exception as error:       #aca se guarda el objeto de la excepcion en la var error
        print(f"Error con {direccion}: {error}")
    finally:
        eliminar_cliente(clientes, cliente)
        cliente.close()
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

