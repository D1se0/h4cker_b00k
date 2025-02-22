---
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

# Fuzzing básico con ffuf

El **`fuzzing`** es una técnica utilizada en hacking ético para descubrir vulnerabilidades en aplicaciones web o sistemas, enviando datos aleatorios o predefinidos para detectar fallos o comportamientos inesperados. Se usa comúnmente para encontrar rutas ocultas, parámetros vulnerables o errores de configuración.

**`Wfuzz`: Una Herramienta Obsoleta**

Una de las herramientas clásicas para `fuzzing` es **`Wfuzz`**, que permite enviar múltiples solicitudes `HTTP` con diferentes cargas útiles para analizar respuestas. Sin embargo, esta herramienta está **bastante desactualizada** y ha sido reemplazada por opciones más modernas y eficientes.

**`FFUF`: La Mejor Alternativa**

Hoy en día, la herramienta más usada y actualizada es **`FFUF (Fast Fuzzing)`**, que ofrece un rendimiento superior gracias a su velocidad, compatibilidad con múltiples formatos y facilidad de uso. Es una excelente opción para realizar `fuzzing` en aplicaciones web de manera eficiente.

En las siguientes secciones, exploraremos **FFUF** en profundidad y aprenderemos cómo utilizarla para encontrar directorios, archivos y vulnerabilidades en aplicaciones web.

Se encuentra en el siguiente repositorio.

URL = [ffuf GitHub](https://github.com/ffuf/ffuf)

Viene por defecto instalada en el `kali`, por lo que haremos lo siguiente para probarla.

Pero antes de ejecutar la herramienta quitaremos los comentarios del diccionario, ya que si no tambien nos lo va a incluir de la siguiente forma:

```shell
sudo sed -i '/^#/d' /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt
```

Una vez quitados los comentarios, ahora si lo ejecutaremos.

```shell
ffuf -u http://192.168.5.211:8080/FUZZ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt
```

Con la palabra `FUZZ` especificamos el campo en concreto donde queremos que pruebe todas esas palabras del diccionario que le estamos pasando. Con `-w` especificamos el diccionario que queremos que utilice la herramienta.

Info:

```

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://192.168.5.211:8080/FUZZ
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

documents               [Status: 301, Size: 324, Words: 20, Lines: 10, Duration: 0ms]
apps                    [Status: 301, Size: 319, Words: 20, Lines: 10, Duration: 0ms]
admin                   [Status: 301, Size: 320, Words: 20, Lines: 10, Duration: 1ms]
portal                  [Status: 200, Size: 5396, Words: 22, Lines: 25, Duration: 1ms]
db                      [Status: 301, Size: 317, Words: 20, Lines: 10, Duration: 0ms]
bugs                    [Status: 200, Size: 7858, Words: 504, Lines: 159, Duration: 1ms]
js                      [Status: 301, Size: 317, Words: 20, Lines: 10, Duration: 1ms]
message                 [Status: 200, Size: 28, Words: 5, Lines: 1, Duration: 2ms]
robots                  [Status: 200, Size: 167, Words: 9, Lines: 11, Duration: 1ms]
fonts                   [Status: 301, Size: 320, Words: 20, Lines: 10, Duration: 1ms]
                        [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 622ms]
666                     [Status: 200, Size: 112, Words: 17, Lines: 7, Duration: 2ms]
soap                    [Status: 301, Size: 319, Words: 20, Lines: 10, Duration: 6ms]
images                  [Status: 301, Size: 321, Words: 20, Lines: 10, Duration: 678ms]
passwords               [Status: 301, Size: 324, Words: 20, Lines: 10, Duration: 1ms]
stylesheets             [Status: 301, Size: 326, Words: 20, Lines: 10, Duration: 5ms]
                        [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 2ms]
:: Progress: [87651/87651] :: Job [1/1] :: 3636 req/sec :: Duration: [0:00:22] :: Errors: 0 ::
```

Y por lo que vemos aqui nos muestra las rutas que ha podido encontrar con este diccionario en dicha pagina web.

Si por ejemplo queremos que cuando encuentre un directorio valido, tambien haga `fuzzing` dentro de ese directorio de forma recursiva con cada uno de esos directorios que encuentre, podremos hacerlo con el parametro `-recursion`:

```shell
ffuf -u http://192.168.5.211:8080/FUZZ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt -recursion
```

Info:

```

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://192.168.5.211:8080/FUZZ
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

                        [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 1ms]
images                  [Status: 301, Size: 321, Words: 20, Lines: 10, Duration: 3ms]
[INFO] Adding a new job to the queue: http://192.168.5.211:8080/images/FUZZ

documents               [Status: 301, Size: 324, Words: 20, Lines: 10, Duration: 1ms]
[INFO] Adding a new job to the queue: http://192.168.5.211:8080/documents/FUZZ

apps                    [Status: 301, Size: 319, Words: 20, Lines: 10, Duration: 0ms]
[INFO] Adding a new job to the queue: http://192.168.5.211:8080/apps/FUZZ

admin                   [Status: 301, Size: 320, Words: 20, Lines: 10, Duration: 0ms]
[INFO] Adding a new job to the queue: http://192.168.5.211:8080/admin/FUZZ

portal                  [Status: 200, Size: 5396, Words: 22, Lines: 25, Duration: 3ms]
db                      [Status: 301, Size: 317, Words: 20, Lines: 10, Duration: 1ms]
[INFO] Adding a new job to the queue: http://192.168.5.211:8080/db/FUZZ

bugs                    [Status: 200, Size: 7858, Words: 504, Lines: 159, Duration: 2ms]
js                      [Status: 301, Size: 317, Words: 20, Lines: 10, Duration: 1ms]
[INFO] Adding a new job to the queue: http://192.168.5.211:8080/js/FUZZ

message                 [Status: 200, Size: 28, Words: 5, Lines: 1, Duration: 1ms]
robots                  [Status: 200, Size: 167, Words: 9, Lines: 11, Duration: 1ms]
fonts                   [Status: 301, Size: 320, Words: 20, Lines: 10, Duration: 1ms]
[INFO] Adding a new job to the queue: http://192.168.5.211:8080/fonts/FUZZ

666                     [Status: 200, Size: 112, Words: 17, Lines: 7, Duration: 1ms]
soap                    [Status: 301, Size: 319, Words: 20, Lines: 10, Duration: 2ms]
[INFO] Adding a new job to the queue: http://192.168.5.211:8080/soap/FUZZ

passwords               [Status: 301, Size: 324, Words: 20, Lines: 10, Duration: 1ms]
[INFO] Adding a new job to the queue: http://192.168.5.211:8080/passwords/FUZZ

stylesheets             [Status: 301, Size: 326, Words: 20, Lines: 10, Duration: 3ms]
[INFO] Adding a new job to the queue: http://192.168.5.211:8080/stylesheets/FUZZ

                        [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 15ms]
[INFO] Starting queued job on target: http://192.168.5.211:8080/images/FUZZ

                        [Status: 200, Size: 5153, Words: 259, Lines: 38, Duration: 115ms]
cc                      [Status: 200, Size: 688, Words: 9, Lines: 7, Duration: 13ms]
blogger                 [Status: 200, Size: 1026, Words: 8, Lines: 5, Duration: 9ms]
favicon                 [Status: 200, Size: 1150, Words: 4, Lines: 6, Duration: 7ms]
nsa                     [Status: 200, Size: 15554, Words: 60, Lines: 65, Duration: 7ms]
captcha                 [Status: 200, Size: 4445, Words: 23, Lines: 28, Duration: 7ms]
mk                      [Status: 200, Size: 11226, Words: 53, Lines: 42, Duration: 13ms]
facebook                [Status: 200, Size: 2636, Words: 16, Lines: 13, Duration: 14ms]
owasp                   [Status: 200, Size: 16988, Words: 90, Lines: 65, Duration: 11ms]
zap                     [Status: 200, Size: 17557, Words: 72, Lines: 83, Duration: 2ms]
linkedin                [Status: 200, Size: 1742, Words: 7, Lines: 17, Duration: 11ms]
                        [Status: 200, Size: 5153, Words: 259, Lines: 38, Duration: 10ms]
twitter                 [Status: 200, Size: 2896, Words: 15, Lines: 10, Duration: 9ms]
mme                     [Status: 200, Size: 14477, Words: 87, Lines: 72, Duration: 12ms]
[INFO] Starting queued job on target: http://192.168.5.211:8080/documents/FUZZ

                        [Status: 200, Size: 2311, Words: 136, Lines: 23, Duration: 101ms]
                        [Status: 200, Size: 2311, Words: 136, Lines: 23, Duration: 9ms]
[INFO] Starting queued job on target: http://192.168.5.211:8080/apps/FUZZ

                        [Status: 200, Size: 944, Words: 65, Lines: 17, Duration: 74ms]
                        [Status: 200, Size: 944, Words: 65, Lines: 17, Duration: 18ms]
[INFO] Starting queued job on target: http://192.168.5.211:8080/admin/FUZZ

                        [Status: 200, Size: 3160, Words: 539, Lines: 125, Duration: 10ms]
                        [Status: 200, Size: 3160, Words: 539, Lines: 125, Duration: 3ms]
[WARN] Caught keyboard interrupt (Ctrl-C)
```

Por lo que vemos se esta recorriendo cada uno de ellos que ha encontrado, haciendo una busqueda recursiva.

Por ejemplo si de estas palabras que esta probando queremos añadirle a cada una de ellas una extension para ver si encuentra algun archivo, podremos hacerlo de la siguiente forma con el parametro `-e`:

```shell
ffuf -u http://192.168.5.211:8080/FUZZ -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt -e .php,.txt,.html
```

Info:

```

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://192.168.5.211:8080/FUZZ
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt
 :: Extensions       : .php .txt .html 
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

images                  [Status: 301, Size: 321, Words: 20, Lines: 10, Duration: 1ms]
index.php               [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 4ms]
info.php                [Status: 200, Size: 3426, Words: 411, Lines: 94, Duration: 2ms]
login.php               [Status: 200, Size: 4013, Words: 523, Lines: 134, Duration: 52ms]
security.php            [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 32ms]
documents               [Status: 301, Size: 324, Words: 20, Lines: 10, Duration: 0ms]
apps                    [Status: 301, Size: 319, Words: 20, Lines: 10, Duration: 1ms]
admin                   [Status: 301, Size: 320, Words: 20, Lines: 10, Duration: 0ms]
training.php            [Status: 200, Size: 3843, Words: 436, Lines: 102, Duration: 9ms]
.html                   [Status: 403, Size: 287, Words: 21, Lines: 11, Duration: 318ms]
.php                    [Status: 403, Size: 286, Words: 21, Lines: 11, Duration: 334ms]
portal.php              [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 3ms]
portal                  [Status: 200, Size: 5396, Words: 22, Lines: 25, Duration: 5ms]
                        [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 607ms]
test.php                [Status: 200, Size: 0, Words: 1, Lines: 1, Duration: 1ms]
credits.php             [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 5ms]
install.php             [Status: 200, Size: 2270, Words: 220, Lines: 76, Duration: 1ms]
db                      [Status: 301, Size: 317, Words: 20, Lines: 10, Duration: 79ms]
bugs.txt                [Status: 200, Size: 7858, Words: 504, Lines: 159, Duration: 2ms]
bugs                    [Status: 200, Size: 7858, Words: 504, Lines: 159, Duration: 4ms]
update.php              [Status: 200, Size: 0, Words: 1, Lines: 1, Duration: 193ms]
js                      [Status: 301, Size: 317, Words: 20, Lines: 10, Duration: 4ms]
message.txt             [Status: 200, Size: 28, Words: 5, Lines: 1, Duration: 1ms]
message                 [Status: 200, Size: 28, Words: 5, Lines: 1, Duration: 5ms]
logout.php              [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 5ms]
connect.php             [Status: 200, Size: 0, Words: 1, Lines: 1, Duration: 9ms]
robots                  [Status: 200, Size: 167, Words: 9, Lines: 11, Duration: 3ms]
robots.txt              [Status: 200, Size: 167, Words: 9, Lines: 11, Duration: 4ms]
fonts                   [Status: 301, Size: 320, Words: 20, Lines: 10, Duration: 2ms]
666                     [Status: 200, Size: 112, Words: 17, Lines: 7, Duration: 3ms]
captcha.php             [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 6ms]
soap                    [Status: 301, Size: 319, Words: 20, Lines: 10, Duration: 4ms]
passwords               [Status: 301, Size: 324, Words: 20, Lines: 10, Duration: 0ms]
aim.php                 [Status: 200, Size: 9958, Words: 608, Lines: 33, Duration: 8ms]
secret.php              [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 9ms]
reset.php               [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 8ms]
backdoor.php            [Status: 200, Size: 333, Words: 21, Lines: 1, Duration: 5ms]
lang_en.php             [Status: 200, Size: 61, Words: 7, Lines: 1, Duration: 6ms]
stylesheets             [Status: 301, Size: 326, Words: 20, Lines: 10, Duration: 7ms]
.php                    [Status: 403, Size: 286, Words: 21, Lines: 11, Duration: 0ms]
.html                   [Status: 403, Size: 287, Words: 21, Lines: 11, Duration: 0ms]
                        [Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 20ms]
top_security.php        [Status: 200, Size: 2208, Words: 320, Lines: 75, Duration: 9ms]
phpinfo.php             [Status: 200, Size: 78622, Words: 4176, Lines: 941, Duration: 94ms]
lang_fr.php             [Status: 200, Size: 65, Words: 7, Lines: 1, Duration: 7ms]
selections.php          [Status: 200, Size: 0, Words: 1, Lines: 1, Duration: 8ms]
:: Progress: [350604/350604] :: Job [1/1] :: 3333 req/sec :: Duration: [0:01:44] :: Errors: 0 ::
```

Y por lo que vemos el diccionario se duplica ya que esta buscando las palabras normales, mas con las extensiones añadidas que le hemos puesto y ya veremos que encontramos mas resultados.
