# Socket Chat Testing

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Pytest](https://img.shields.io/badge/Pytest-26%20Tests-success)
![Coverage](https://img.shields.io/badge/Coverage-83%25-brightgreen)

## Descripción

Este proyecto consiste en una aplicación de chat utilizando sockets TCP en Python. Fue desarrollado como parte de un challenge enfocado en testing, aplicando pruebas unitarias, pruebas de integración y medición de cobertura para verificar el correcto funcionamiento del servidor.

El servidor permite que múltiples clientes se conecten simultáneamente y retransmite los mensajes recibidos a todos los clientes conectados, excepto al emisor.

---

## Tecnologías utilizadas

- Python 3.11
- Sockets TCP
- Threading
- Pytest
- Pytest-Cov
- Git & GitHub

---

## Estructura del proyecto

```
socket-chat-testing/
│
├── server.py
├── client.py
├── tests/
│   ├── test_server.py
│   └── test_integration.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Instalación

Clonar el repositorio:

```bash
git clone <URL_DEL_REPOSITORIO>
```

Ingresar al proyecto:

```bash
cd socket-chat-testing
```

Crear el entorno virtual:

### Windows

```bash
python -m venv venv
```

Activarlo:

```bash
.\venv\Scripts\activate
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

---

## Ejecutar el servidor

```bash
python server.py
```

---

## Ejecutar un cliente

Abrir otra terminal y ejecutar:

```bash
python client.py
```

Se pueden abrir varias terminales para conectar múltiples clientes al servidor.

---

## Ejecutar las pruebas

Ejecutar toda la suite de pruebas:

```bash
python -m pytest
```

---

## Ejecutar la cobertura

Cobertura del servidor:

```bash
python -m pytest --cov=server --cov-report=term-missing
```

Resultado obtenido:

```
Coverage: 83%
```

---

## Pruebas implementadas

### Pruebas unitarias

Se realizaron pruebas para las siguientes funciones del servidor:

- Validación de mensajes.
- Comando de salida.
- Formato de mensajes.
- Gestión de clientes.
- Broadcast de mensajes.

### Pruebas de integración

Se verificó el comportamiento del sistema utilizando sockets reales:

- Conexión de clientes al servidor.
- Comunicación entre múltiples clientes.
- Broadcast de mensajes.
- Orden de recepción de mensajes.
- Desconexión inesperada de clientes.
- Verificación de que los mensajes no se duplican.

---

## Resultados

- 26 pruebas implementadas.
- Todas las pruebas aprobadas.
- Cobertura del servidor superior al 80%.
- Refactorización del servidor para facilitar su testeo.

---
