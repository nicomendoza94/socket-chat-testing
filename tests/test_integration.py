import socket
import threading
import time

from server import iniciar_servidor

# Integration Tests

#el servidor debe aceptar conexiones de clientes
def test_server_accepts_client_connection():

    servidor = threading.Thread(
        target=iniciar_servidor,
        daemon=True
    )

    servidor.start()

    #espera breve para permitir que el servidor comience a escuchar
    time.sleep(0.5)

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(("127.0.0.1", 8000))

    assert cliente.fileno() != -1

    cliente.close()