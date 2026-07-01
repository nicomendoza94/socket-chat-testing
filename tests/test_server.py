from unittest.mock import Mock
from server import validar_mensaje, salir, formatear_mensaje, agregar_cliente, eliminar_cliente, broadcast

# validar_mensaje()

 #mensaje vacio no debe ser aceptado
def test_validate_empty_message():
    assert validar_mensaje("") is False

#un mensaje compuesto solo por espacios es invalido
def test_validate_message_with_only_spaces():
    assert validar_mensaje("     ") is False

#un mensaje normal debe ser aceptado
def test_validate_valid_message():
    assert validar_mensaje("Hola mundo") is True

#el limite max permitido, 200 caracteres, sigue siendo valido
def test_validate_message_with_200_characters():
    mensaje = "a" * 200

    assert validar_mensaje(mensaje) is True

#cualquier mensaje que supere el limite debe rechazarse
def test_validate_message_with_more_than_200_characters():
    mensaje = "a" * 201

    assert validar_mensaje(mensaje) is False

# salir()

#el comando "/salir" debe ser reconocido
def test_exit_command():
    assert salir("/salir") is True


#el comando debe funcionar sin importar mayusculas o minusculas
def test_exit_command_is_case_insensitive():
    assert salir("/SALIR") is True


#los espacios al inicio o al final no deben afectar la validacion
def test_exit_command_with_surrounding_spaces():
    assert salir("   /salir   ") is True


#cualquier otro mensaje no debe interpretarse como comando de salida
def test_non_exit_command():
    assert salir("Hola") is False


#el comando debe ser exactamente "/salir".
def test_exit_command_with_additional_text():
    assert salir("/salir ahora") is False

# formatear_mensaje()

#el mensaje debe incluir la direccion seguida del contenido
def test_format_message():
    assert (
        formatear_mensaje(("127.0.0.1", 8000), "Hola")
        == "('127.0.0.1', 8000): Hola"
    )


#un mensaje vacio debe conservar el formato
def test_format_empty_message():
    assert (
        formatear_mensaje(("127.0.0.1", 8000), "")
        == "('127.0.0.1', 8000): "
    )


#el contenido del mensaje no debe modificarse
def test_format_message_with_special_characters():
    assert (
        formatear_mensaje(("127.0.0.1", 8000), "Hola!!!")
        == "('127.0.0.1', 8000): Hola!!!"
    )

# agregar_cliente()

#un cliente nuevo debe agregarse correctamente a una lista vacia
def test_add_client_to_empty_list():
    clientes_conectados = []
    cliente = object()

    agregar_cliente(clientes_conectados, cliente)

    assert cliente in clientes_conectados
    assert len(clientes_conectados) == 1


#agregar un cliente no debe eliminar ni reemplazar clientes existentes
def test_add_client_to_existing_list():
    cliente_existente = object()
    cliente_nuevo = object()
    clientes_conectados = [cliente_existente]

    agregar_cliente(clientes_conectados, cliente_nuevo)

    assert cliente_existente in clientes_conectados
    assert cliente_nuevo in clientes_conectados
    assert len(clientes_conectados) == 2


# eliminar_cliente()

#un cliente conectado debe poder eliminarse de la lista
def test_remove_existing_client():
    cliente_a_eliminar = object()
    cliente_restante = object()
    clientes_conectados = [cliente_a_eliminar, cliente_restante]

    eliminar_cliente(clientes_conectados, cliente_a_eliminar)

    assert cliente_a_eliminar not in clientes_conectados
    assert cliente_restante in clientes_conectados
    assert len(clientes_conectados) == 1


#intentar eliminar un cliente inexistente no debe alterar la lista
def test_remove_non_existing_client():
    cliente_existente = object()
    cliente_inexistente = object()
    clientes_conectados = [cliente_existente]

    eliminar_cliente(clientes_conectados, cliente_inexistente)

    assert clientes_conectados == [cliente_existente]

# broadcast()

#el mensaje debe enviarse a todos los clientes excepto al emisor
def test_broadcast_sends_message_to_all_clients_except_sender():
    emisor = Mock()
    cliente_1 = Mock()
    cliente_2 = Mock()

    clientes_conectados = [emisor, cliente_1, cliente_2]

    broadcast("Hola", emisor, clientes_conectados)

    emisor.send.assert_not_called()
    cliente_1.send.assert_called_once_with("Hola".encode("utf-8"))
    cliente_2.send.assert_called_once_with("Hola".encode("utf-8"))


#si solo existe el emisor conectado, no debe producirse ningun error
def test_broadcast_does_not_fail_when_only_sender_is_connected():
    emisor = Mock()
    clientes_conectados = [emisor]

    broadcast("Hola", emisor, clientes_conectados)

    emisor.send.assert_not_called()


#si un cliente genera un error al enviar un mensaje, debe eliminarse de la lista
def test_broadcast_removes_client_when_send_fails():
    emisor = Mock()
    cliente_con_error = Mock()

    cliente_con_error.send.side_effect = Exception("Connection error")

    clientes_conectados = [emisor, cliente_con_error]

    broadcast("Hola", emisor, clientes_conectados)

    assert cliente_con_error not in clientes_conectados
    cliente_con_error.close.assert_called_once()