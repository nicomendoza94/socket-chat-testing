from server import validar_mensaje, salir, formatear_mensaje

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