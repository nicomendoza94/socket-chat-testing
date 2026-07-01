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

def test_multiple_clients_receive_same_message():
    # Todos los clientes conectados, excepto el emisor, deben recibir el mensaje.

    sender_client = create_client()
    receiver_client_1 = create_client()
    receiver_client_2 = create_client()

    time.sleep(0.2)

    message = "Mensaje para todos"

    sender_client.send(message.encode("utf-8"))

    received_message_1 = receiver_client_1.recv(1024).decode("utf-8")
    received_message_2 = receiver_client_2.recv(1024).decode("utf-8")

    assert message in received_message_1
    assert message in received_message_2

    sender_client.close()
    receiver_client_1.close()
    receiver_client_2.close()


#los mensajes deben llegar en el mismo orden en que fueron enviados
def test_messages_are_received_in_order():
    sender_client = create_client()
    receiver_client = create_client()

    time.sleep(0.2)

    messages = ["Uno", "Dos", "Tres"]

    for message in messages:
        #pausa breve para facilitar que el servidor procese cada envio
        sender_client.send(message.encode("utf-8"))
        time.sleep(0.1)

    received_data = ""

    while not all(message in received_data for message in messages):
        received_data += receiver_client.recv(1024).decode("utf-8")

    assert received_data.index("Uno") < received_data.index("Dos")
    assert received_data.index("Dos") < received_data.index("Tres")

    sender_client.close()
    receiver_client.close()


#el servidor debe continuar funcionando aunque un cliente se desconecte inesperadamente
def test_client_disconnection_does_not_stop_server():

    disconnected_client = create_client()
    active_client = create_client()
    receiver_client = create_client()

    time.sleep(0.2)

    disconnected_client.close()

    time.sleep(0.2)

    message = "Servidor sigue activo"

    active_client.send(message.encode("utf-8"))

    received_message = receiver_client.recv(1024).decode("utf-8")

    assert message in received_message

    active_client.close()
    receiver_client.close()


#el receptor debe recibir una unica copia del mensaje enviado
def test_message_is_not_duplicated():

    sender_client = create_client()
    receiver_client = create_client()

    time.sleep(0.2)

    message = "Mensaje unico"

    sender_client.send(message.encode("utf-8"))

    first_message = receiver_client.recv(1024).decode("utf-8")

    receiver_client.settimeout(0.5)

    with pytest.raises(socket.timeout):
        receiver_client.recv(1024)

    assert message in first_message

    sender_client.close()
    receiver_client.close()