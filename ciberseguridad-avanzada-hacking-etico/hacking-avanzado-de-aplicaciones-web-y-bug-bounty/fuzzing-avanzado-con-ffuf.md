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

# Fuzzing avanzado con ffuf

Si queremos utilizar la herramienta de forma un poco mas avanzada, podremos decirle que nos utilice `2` diccionarios en vez de uno y que nos lo identifique con un nombre en concreto de la siguiente forma:

```shell
ffuf -u http://192.168.5.211:8080/W1/W2 -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt:W1 -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt:W2
```

Aqui lo que estamos haciendo es que el primer diccionario se va a llamar `W1` y el segundo `W2` para poderlos identificar y que sepa la herramienta las zonas donde inyectarlo, que en este caso seria `/W1/W2`.

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
 :: URL              : http://192.168.5.211:8080/W1/W2
 :: Wordlist         : W1: /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt
 :: Wordlist         : W2: /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

[Status: 403, Size: 290, Words: 21, Lines: 11, Duration: 4ms]
    * W1: cgi-bin
    * W2: 

[Status: 403, Size: 288, Words: 21, Lines: 11, Duration: 0ms]
    * W1: icons
    * W2: 

[Status: 200, Size: 5153, Words: 259, Lines: 38, Duration: 10ms]
    * W1: images
    * W2: 

[Status: 200, Size: 2311, Words: 136, Lines: 23, Duration: 2ms]
    * W1: documents
    * W2: 

[Status: 200, Size: 944, Words: 65, Lines: 17, Duration: 1ms]
    * W1: apps
    * W2: 

[Status: 200, Size: 3160, Words: 539, Lines: 125, Duration: 1ms]
    * W1: admin
    * W2: 

[Status: 200, Size: 940, Words: 65, Lines: 17, Duration: 1ms]
    * W1: db
    * W2: 

[Status: 200, Size: 1555, Words: 102, Lines: 20, Duration: 8ms]
    * W1: js
    * W2: 

[Status: 200, Size: 2592, Words: 164, Lines: 25, Duration: 6ms]
    * W1: fonts
    * W2: 

[Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 546ms]
    * W1: 
    * W2: 

[Status: 200, Size: 3363, Words: 204, Lines: 28, Duration: 2ms]
    * W1: soap
    * W2: 

[Status: 200, Size: 1366, Words: 88, Lines: 19, Duration: 12ms]
    * W1: passwords
    * W2: 

[Status: 200, Size: 1437, Words: 79, Lines: 19, Duration: 17ms]
    * W1: stylesheets
    * W2: 

[Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 12ms]
    * W1: W2
    * W2: 

[Status: 302, Size: 0, Words: 1, Lines: 1, Duration: 16ms]
    * W1: 
    * W2: 

[Status: 403, Size: 295, Words: 21, Lines: 11, Duration: 58ms]
    * W1: cgi-bin
    * W2: index

[Status: 301, Size: 321, Words: 20, Lines: 10, Duration: 1ms]
    * W1: 
    * W2: images

[Status: 403, Size: 296, Words: 21, Lines: 11, Duration: 3ms]
    * W1: cgi-bin
    * W2: images

[Status: 301, Size: 321, Words: 20, Lines: 10, Duration: 8ms]
    * W1: 
    * W2: images

[Status: 403, Size: 298, Words: 21, Lines: 11, Duration: 0ms]
    * W1: cgi-bin
    * W2: download

[WARN] Caught keyboard interrupt (Ctrl-C)
```

Y veremos que nos esta utilizando los `2` diccionarios en las posiciones que le pusimos a la herramienta.

### Fuzzing sobre los campos de login de un request\_post.txt

Si por ejemplo capturamos el intento de inicio de sesion de una pagina con `BurpSuite` nos mostrara la peticion que se ha realizado, esta peticion la guardaremos en un archivo llamado `request_post` el cual le pasaremos a la herramienta `fuff`, lo que vamos hacer es que sustituya los campos en este caso de `login` para que me haga `fuzzing` de ese campo.

Primero abrimos `BurpSuite`, nos vamos a `Proxy` -> `Open Browser`.

Esto nos abrira el navegador de `BurpSuite` por lo que estara en mitad de la comunicacion entre la estructura de `Cliente-Servidor`, buscamos la siguiente `URL` para meternos en la pagina del puerto `8080`.

```
URL = http://192.168.5.211:8080/
```

Una vez que estemos dentro veremos el `login` el cual meteremos las credenciales que queramos y antes de enviarlo en `BurpSuite` le daremos a `Intercept on` para que empiece a interceptar. ahora si le daremos a enviar y nos capturara la peticion, viendo lo siguiente:

> request\_post

```
POST /login.php HTTP/1.1
Host: 192.168.5.211:8080
Content-Length: 57
Cache-Control: max-age=0
Accept-Language: en-US,en;q=0.9
Origin: http://192.168.5.211:8080
Content-Type: application/x-www-form-urlencoded
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://192.168.5.211:8080/login.php
Accept-Encoding: gzip, deflate, br
Cookie: PHPSESSID=aed4glvn1pnbt4r19s957dpos1
Connection: keep-alive

login=santiago&password=1234&security_level=0&form=submit
```

Entonces cuando lo hayamos volcado la peticion a un archivo llamado `request_post` dandole al boton `click derecho` -> `Copy to file`, podremos hacer lo siguiente.

Si queremos hacer `fuzzing` en el nombre de usuario, podremos cambiar la palabra `santiago` del apartado `login` por la palabra `FUZZ` para que reemplace esa palabra por las del diccionario.

> request\_post

```
POST /login.php HTTP/1.1
Host: 192.168.5.211:8080
Content-Length: 57
Cache-Control: max-age=0
Accept-Language: en-US,en;q=0.9
Origin: http://192.168.5.211:8080
Content-Type: application/x-www-form-urlencoded
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://192.168.5.211:8080/login.php
Accept-Encoding: gzip, deflate, br
Cookie: PHPSESSID=aed4glvn1pnbt4r19s957dpos1
Connection: keep-alive

login=FUZZ&password=1234&security_level=0&form=submit
```

Una vez teniendo todo esto estara listo para darselo a la herramienta `ffuf` y que realice la busqueda.

```shell
ffuf -request request_post -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt
```

Y con esto ya estaria reemplazando la palabra `FUZZ` por cada una del diccionario, podremos probar a poner el usuario real dentro del diccionario para que se vea que funciona de la siguiente forma:

```shell
sudo echo "santiago" >> /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt
```

Con esto ya podremos comprobar que nos daria resultado el `login`.

### Herramienta Radamsa con ffuf, denegacion de servicio

Ahora lo que vamos a ver es combinar una herramienta que genera palabras con caracteres muy raros los cuales si se insertan en un programa que no este sanitizado puede este llegar a petar con `radamsa`, pero a parte de esto lo vamos a combinar con la herramienta `ffuf`.

URL = [Radamsa GitLab](https://gitlab.com/akihe/radamsa)

Vamos a tener que instalar la herramienta, por lo que haremos lo siguiente:

```shell
sudo apt-get install gcc make git wget
git clone https://gitlab.com/akihe/radamsa.git && cd radamsa && make && sudo make install
```

Y con esto ya tendriamos el `binario` instalado de `radamsa` y totalmente funcional, ahora vamos hacer lo siguiente con el mismo.

```shell
cd /home/kali/radamsa/bin
echo "test" | radamsa
```

Lo que va a generar esto es una cadena de caracteres los cuales la mayoria de aplicaciones que no esten correctamente sanitizadas van hacer que peten:

Info:

```
tert
❯ echo "test" | radamsa
te��࿭�st
❯ echo "test" | radamsa
te'xcalc%d\n%p%n\u0\r\n%nst
❯ echo "test" | radamsa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaatest
❯ echo "test" | radamsa
❯ echo "test" | radamsa
test
❯ echo "test" | radamsa
uett
❯ echo "test" | radamsa
te3t
❯ echo "test" | radamsa
���t�est%                                                                                                                                                                                   ❯ echo "test" | radamsa
t
 est
❯ echo "test" | radamsa
testt
❯ echo "test" | radamsa
\r$1aaaa%d%$`\229$+\x0d$PATHtst
❯ echo "test" | radamsa
test 
❯ echo "test" | radamsa
s
testtet
```

Esto tambien se puede utilizar desde un texto:

```shell
echo "test" > text.txt
radamsa text.txt
```

Ahora en la herramienta `ffuf` haremos lo siguiente:

```shell
ffuf -request ~/request_post --input-cmd 'radamsa text.txt' -input-num 1000
```

Con el `-input-num` especificamos el numero de peticiones que queremos que haga, ya que por defecto esta a `100`.

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

 :: Method           : POST
 :: URL              : https://192.168.5.211:8080/login.php
 :: Header           : Accept-Encoding: gzip, deflate, br
 :: Header           : Cookie: PHPSESSID=aed4glvn1pnbt4r19s957dpos1
 :: Header           : Cache-Control: max-age=0
 :: Header           : Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
 :: Header           : Origin: http://192.168.5.211:8080
 :: Header           : Content-Type: application/x-www-form-urlencoded
 :: Header           : Upgrade-Insecure-Requests: 1
 :: Header           : User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36
 :: Header           : Referer: http://192.168.5.211:8080/login.php
 :: Header           : Connection: keep-alive
 :: Header           : Host: 192.168.5.211:8080
 :: Header           : Accept-Language: en-US,en;q=0.9
 :: Data             : login=FUZZ&password=1234&security_level=0&form=submit
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

:: Progress: [1000/1000] :: Job [1/1] :: 149 req/sec :: Duration: [0:00:06] :: Errors: 1000 ::
```

En este caso esta bien la pagina web del campo, pero si en algun momento nos diera un `status code` de `404` o de `500`, etc... Podremos ver que el campo no esta bien sanitizado y podremos aprovechar eso, pero en este caso nos estan dando codigos normales de `200`.
