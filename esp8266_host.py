
from machine import UART, Pin
import time
from mfrc522 import MFRC522

# Configuración del UART para la ESP8266
uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))

# Inicialización del lector RFID
lector = MFRC522(spi_id=0, sck=2, miso=4, mosi=3, cs=1, rst=0)

# Configuración de LEDs y buzzer
rojo = Pin(13, Pin.OUT)
verde = Pin(12, Pin.OUT)
buzzer = Pin(14, Pin.OUT)

# Listas de UIDs para acceso permitido y denegado
accesos_permitidos = [207865937, 543617918]  # TARJETA1, LLAVERO1
accesos_denegados = [3829981459, 49736097]   # TARJETA2, LLAVERO2

# Credenciales de WiFi
SSID = "infinix hot 30"
PASSWORD = "12345678"

def send_command(cmd, timeout=2000):
    """Envía un comando AT al ESP8266 y devuelve la respuesta."""
    uart.write(cmd + '\r\n')
    time.sleep(0.1)
    start = time.ticks_ms()
    response = b""
    while time.ticks_diff(time.ticks_ms(), start) < timeout:
        if uart.any():
            response += uart.read()
    return response.decode('utf-8', errors='ignore') if response else "No response"

def connect_to_wifi(ssid, password):
    """Conecta la ESP8266 a una red WiFi."""
    print("Conectando a WiFi...")
    send_command("AT+CWMODE=1")  # Configurar como estación
    response = send_command(f'AT+CWJAP="{ssid}","{password}"', timeout=15000)
    if "OK" in response:
        print("Conexión WiFi exitosa!")
    else:
        print("Error al conectar a WiFi:", response)

def send_email(subject, message):
    """Envía un correo usando un servidor SMTP."""
    print("Enviando correo...")
    host = "smtp.gmail.com"
    path = f"/send_email?subject={subject}&message={message}"
    response = send_command(f'AT+CIPSTART="TCP","{host}",80', timeout=5000)
    if "OK" not in response:
        print("Error al iniciar conexión TCP:", response)
        return
    send_command(f'AT+CIPSEND={len(path) + 4 + len(host) + 22}', timeout=2000)
    response = send_command(f"GET {path} HTTP/1.1\r\nHost: {host}\r\n\r\n", timeout=5000)
    print("Respuesta del servidor:", response)

def buzzer_suave():
    """Activa el buzzer con una alerta suave."""
    for _ in range(5):
        buzzer.value(1)
        time.sleep(0.1)
        buzzer.value(0)
        time.sleep(0.1)

def buzzer_fuerte():
    """Activa el buzzer con una alerta fuerte."""
    for _ in range(5):
        buzzer.value(1)
        time.sleep(0.3)
        buzzer.value(0)
        time.sleep(0.1)

def busqueda_secuencial(lista, valor):
    """Devuelve True si el valor está en la lista, de lo contrario False."""
    for item in lista:
        if item == valor:
            return True
    return False

# Conectar a WiFi al inicio
connect_to_wifi(SSID, PASSWORD)

print("Lector RFID activo...\n")
while True:
    try:
        lector.init()
        (stat, tag_type) = lector.request(lector.REQIDL)
        if stat == lector.OK:
            (stat, uid) = lector.SelectTagSN()
            if stat == lector.OK:
                identificador = int.from_bytes(bytes(uid), "little", False)

                if busqueda_secuencial(accesos_permitidos, identificador):
                    print(f"UID: {identificador} - Acceso concedido")
                    rojo.value(0)
                    verde.value(1)
                    buzzer_suave()
                    time.sleep(2)
                    verde.value(0)

                elif busqueda_secuencial(accesos_denegados, identificador):
                    print(f"UID: {identificador} - Acceso denegado")
                    rojo.value(1)
                    verde.value(0)
                    buzzer_fuerte()
                    time.sleep(2)
                    rojo.value(0)
                    # Enviar notificación por correo
                    send_email("Acceso denegado", f"Intento de acceso no autorizado con UID: {identificador}")

                else:
                    print(f"UID: {identificador} - Desconocido: Acceso denegado")
                    rojo.value(1)
                    verde.value(0)
                    buzzer_fuerte()
                    time.sleep(2)
                    rojo.value(0)
                    # Enviar notificación por correo
                    send_email("Acceso desconocido", f"Intento de acceso con UID desconocido: {identificador}")
    except Exception as e:
        print(f"Error en el bucle principal: {e}")


from machine import UART, Pin
import time
from mfrc522 import MFRC522

# Configuración del UART para la ESP8266
uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))

# Inicialización del lector RFID
lector = MFRC522(spi_id=0, sck=2, miso=4, mosi=3, cs=1, rst=0)

# Configuración de LEDs y buzzer
rojo = Pin(13, Pin.OUT)
verde = Pin(12, Pin.OUT)
buzzer = Pin(14, Pin.OUT)

# Listas de UIDs para acceso permitido y denegado
accesos_permitidos = [207865937, 543617918]  # TARJETA1, LLAVERO1
accesos_denegados = [3829981459, 49736097]   # TARJETA2, LLAVERO2

# Credenciales de WiFi
SSID = "infinix hot 30"
PASSWORD = "12345678"

def send_command(cmd, timeout=2000):
    """Envía un comando AT al ESP8266 y devuelve la respuesta."""
    uart.write(cmd + '\r\n')
    time.sleep(0.1)
    start = time.ticks_ms()
    response = b""
    while time.ticks_diff(time.ticks_ms(), start) < timeout:
        if uart.any():
            response += uart.read()
    return response.decode('utf-8', errors='ignore') if response else "No response"

def connect_to_wifi(ssid, password):
    """Conecta la ESP8266 a una red WiFi."""
    print("Conectando a WiFi...")
    send_command("AT+CWMODE=1")  # Configurar como estación
    response = send_command(f'AT+CWJAP="{ssid}","{password}"', timeout=15000)
    if "OK" in response:
        print("Conexión WiFi exitosa!")
    else:
        print("Error al conectar a WiFi:", response)

def send_email(subject, message):
    """Envía un correo usando un servidor SMTP."""
    print("Enviando correo...")
    host = "smtp.gmail.com"
    path = f"/send_email?subject={subject}&message={message}"
    response = send_command(f'AT+CIPSTART="TCP","{host}",80', timeout=5000)
    if "OK" not in response:
        print("Error al iniciar conexión TCP:", response)
        return
    send_command(f'AT+CIPSEND={len(path) + 4 + len(host) + 22}', timeout=2000)
    response = send_command(f"GET {path} HTTP/1.1\r\nHost: {host}\r\n\r\n", timeout=5000)
    print("Respuesta del servidor:", response)

def buzzer_suave():
    """Activa el buzzer con una alerta suave."""
    for _ in range(5):
        buzzer.value(1)
        time.sleep(0.1)
        buzzer.value(0)
        time.sleep(0.1)

def buzzer_fuerte():
    """Activa el buzzer con una alerta fuerte."""
    for _ in range(5):
        buzzer.value(1)
        time.sleep(0.3)
        buzzer.value(0)
        time.sleep(0.1)

def busqueda_secuencial(lista, valor):
    """Devuelve True si el valor está en la lista, de lo contrario False."""
    for item in lista:
        if item == valor:
            return True
    return False

# Conectar a WiFi al inicio
connect_to_wifi(SSID, PASSWORD)

print("Lector RFID activo...\n")
while True:
    try:
        lector.init()
        (stat, tag_type) = lector.request(lector.REQIDL)
        if stat == lector.OK:
            (stat, uid) = lector.SelectTagSN()
            if stat == lector.OK:
                identificador = int.from_bytes(bytes(uid), "little", False)

                if busqueda_secuencial(accesos_permitidos, identificador):
                    print(f"UID: {identificador} - Acceso concedido")
                    rojo.value(0)
                    verde.value(1)
                    buzzer_suave()
                    time.sleep(2)
                    verde.value(0)

                elif busqueda_secuencial(accesos_denegados, identificador):
                    print(f"UID: {identificador} - Acceso denegado")
                    rojo.value(1)
                    verde.value(0)
                    buzzer_fuerte()
                    time.sleep(2)
                    rojo.value(0)
                    # Enviar notificación por correo
                    send_email("Acceso denegado", f"Intento de acceso no autorizado con UID: {identificador}")

                else:
                    print(f"UID: {identificador} - Desconocido: Acceso denegado")
                    rojo.value(1)
                    verde.value(0)
                    buzzer_fuerte()
                    time.sleep(2)
                    rojo.value(0)
                    # Enviar notificación por correo
                    send_email("Acceso desconocido", f"Intento de acceso con UID desconocido: {identificador}")
    except Exception as e:
        print(f"Error en el bucle principal: {e}")


from machine import UART, Pin
import time
from mfrc522 import MFRC522

# Configuración del UART para la ESP8266
uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))

# Inicialización del lector RFID
lector = MFRC522(spi_id=0, sck=2, miso=4, mosi=3, cs=1, rst=0)

# Configuración de LEDs y buzzer
rojo = Pin(13, Pin.OUT)
verde = Pin(12, Pin.OUT)
buzzer = Pin(14, Pin.OUT)

# Listas de UIDs para acceso permitido y denegado
accesos_permitidos = [207865937, 543617918]  # TARJETA1, LLAVERO1
accesos_denegados = [3829981459, 49736097]   # TARJETA2, LLAVERO2

# Credenciales de WiFi
SSID = "infinix hot 30"
PASSWORD = "12345678"

def send_command(cmd, timeout=2000):
    """Envía un comando AT al ESP8266 y devuelve la respuesta."""
    uart.write(cmd + '\r\n')
    time.sleep(0.1)
    start = time.ticks_ms()
    response = b""
    while time.ticks_diff(time.ticks_ms(), start) < timeout:
        if uart.any():
            response += uart.read()
    return response.decode('utf-8', errors='ignore') if response else "No response"

def connect_to_wifi(ssid, password):
    """Conecta la ESP8266 a una red WiFi."""
    print("Conectando a WiFi...")
    send_command("AT+CWMODE=1")  # Configurar como estación
    response = send_command(f'AT+CWJAP="{ssid}","{password}"', timeout=15000)
    if "OK" in response:
        print("Conexión WiFi exitosa!")
    else:
        print("Error al conectar a WiFi:", response)

def send_email(subject, message):
    """Envía un correo usando un servidor SMTP."""
    print("Enviando correo...")
    host = "smtp.gmail.com"
    path = f"/send_email?subject={subject}&message={message}"
    response = send_command(f'AT+CIPSTART="TCP","{host}",80', timeout=5000)
    if "OK" not in response:
        print("Error al iniciar conexión TCP:", response)
        return
    send_command(f'AT+CIPSEND={len(path) + 4 + len(host) + 22}', timeout=2000)
    response = send_command(f"GET {path} HTTP/1.1\r\nHost: {host}\r\n\r\n", timeout=5000)
    print("Respuesta del servidor:", response)

def buzzer_suave():
    """Activa el buzzer con una alerta suave."""
    for _ in range(5):
        buzzer.value(1)
        time.sleep(0.1)
        buzzer.value(0)
        time.sleep(0.1)

def buzzer_fuerte():
    """Activa el buzzer con una alerta fuerte."""
    for _ in range(5):
        buzzer.value(1)
        time.sleep(0.3)
        buzzer.value(0)
        time.sleep(0.1)

def busqueda_secuencial(lista, valor):
    """Devuelve True si el valor está en la lista, de lo contrario False."""
    for item in lista:
        if item == valor:
            return True
    return False

# Conectar a WiFi al inicio
connect_to_wifi(SSID, PASSWORD)

print("Lector RFID activo...\n")
while True:
    try:
        lector.init()
        (stat, tag_type) = lector.request(lector.REQIDL)
        if stat == lector.OK:
            (stat, uid) = lector.SelectTagSN()
            if stat == lector.OK:
                identificador = int.from_bytes(bytes(uid), "little", False)

                if busqueda_secuencial(accesos_permitidos, identificador):
                    print(f"UID: {identificador} - Acceso concedido")
                    rojo.value(0)
                    verde.value(1)
                    buzzer_suave()
                    time.sleep(2)
                    verde.value(0)

                elif busqueda_secuencial(accesos_denegados, identificador):
                    print(f"UID: {identificador} - Acceso denegado")
                    rojo.value(1)
                    verde.value(0)
                    buzzer_fuerte()
                    time.sleep(2)
                    rojo.value(0)
                    # Enviar notificación por correo
                    send_email("Acceso denegado", f"Intento de acceso no autorizado con UID: {identificador}")

                else:
                    print(f"UID: {identificador} - Desconocido: Acceso denegado")
                    rojo.value(1)
                    verde.value(0)
                    buzzer_fuerte()
                    time.sleep(2)
                    rojo.value(0)
                    # Enviar notificación por correo
                    send_email("Acceso desconocido", f"Intento de acceso con UID desconocido: {identificador}")
    except Exception as e:
        print(f"Error en el bucle principal: {e}")

