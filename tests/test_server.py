from server import validar_mensaje

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