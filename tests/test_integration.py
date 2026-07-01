import socket
import threading
import time

import pytest

from server import iniciar_servidor


HOST = "127.0.0.1"
PORT = 8000
TIMEOUT = 2


@pytest.fixture(scope="session", autouse=True)
def start_server_once():
    #el servidor se inicia una sola vez para evitar conflictos con el puerto 8000
    server_thread = threading.Thread(
        target=iniciar_servidor,
        daemon=True
    )

    server_thread.start()

    #espera breve para permitir que el servidor comience a escuchar
    time.sleep(0.5)


def create_client():
    #cada cliente usa timeout para evitar que recv() bloquee indefinidamente
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(TIMEOUT)
    client_socket.connect((HOST, PORT))

    return client_socket


def test_server_accepts_client_connection():
    #el servidor debe aceptar conexiones de clientes
    client_socket = create_client()

    assert client_socket.fileno() != -1

    client_socket.close()


def test_server_broadcasts_messages_between_clients():
    #el servidor debe reenviar un mensaje a todos los clientes excepto al emisor
    sender_client = create_client()
    receiver_client = create_client()

    #espera breve para asegurar que ambos clientes esten registrados en el servidor
    time.sleep(0.2)

    message = "Hola"

    sender_client.send(message.encode("utf-8"))

    received_message = receiver_client.recv(1024).decode("utf-8")

    assert message in received_message

    sender_client.close()
    receiver_client.close()