---
icon: flag
---

# Access BugBountyLabs (Principiante)

## Instalación

Cuando obtenemos el `.zip` nos lo pasamos al entorno en el que vamos a empezar a hackear la maquina y haremos lo siguiente.

```shell
unzip bugbountylabs_access.zip
```

Nos lo descomprimira y despues montamos la maquina de la siguiente forma.

```shell
python3 bugbountylabs_access.py
```

Info:

```
██████╗ ██╗   ██╗ ██████╗     ██████╗  ██████╗ ██╗   ██╗███╗   ██╗████████╗██╗   ██╗    ██╗      █████╗ ██████╗ ███████╗
██╔══██╗██║   ██║██╔════╝     ██╔══██╗██╔═══██╗██║   ██║████╗  ██║╚══██╔══╝╚██╗ ██╔╝    ██║     ██╔══██╗██╔══██╗██╔════╝
██████╔╝██║   ██║██║  ███╗    ██████╔╝██║   ██║██║   ██║██╔██╗ ██║   ██║    ╚████╔╝     ██║     ███████║██████╔╝███████╗
██╔══██╗██║   ██║██║   ██║    ██╔══██╗██║   ██║██║   ██║██║╚██╗██║   ██║     ╚██╔╝      ██║     ██╔══██║██╔══██╗╚════██║
██████╔╝╚██████╔╝╚██████╔╝    ██████╔╝╚██████╔╝╚██████╔╝██║ ╚████║   ██║      ██║       ███████╗██║  ██║██████╔╝███████║
╚═════╝  ╚═════╝  ╚═════╝     ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝   ╚═╝      ╚═╝       ╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝

Fundadores
El Pingüino de Mario
Curiosidades De Hackers

Cofundadores
Zunderrub
CondorHacks
Lenam

Descargando la máquina access, espere por favor...

[########################################] 100%
Descarga completa.
La IP de la máquina access es -> 172.17.0.2

Presiona Ctrl+C para detener la máquina
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
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-03-25 09:14 CET
Nmap scan report for corsy.lab (172.17.0.2)
Host is up (0.000056s latency).

PORT     STATE SERVICE VERSION
80/tcp   open  http    Apache httpd 2.4.62 ((Debian))
|_http-title: Laboratorio de Broken Access Control
|_http-server-header: Apache/2.4.62 (Debian)
3000/tcp open  http    Node.js Express framework
|_http-title: Broken Access Control
5000/tcp open  http    Node.js Express framework
|_http-title: IDOR Lab
MAC Address: 02:42:AC:11:00:02 (Unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 12.50 seconds
```

Si entramos en la pagina principal del puerto `80` veremos que tendremos que realizar `2` laboratorios uno de `BAC` y el otro de `IDOR`, por lo que primero haremos el de `BAC`, si entramos dentro de dicho `LAB` veremos una pagina web sobre un `registro` y un `login`, primero vamos a `registrarnos` con un usuario.

## LAB 1: BAC

Si nos registramos, nos pondra que lo hicimos de forma exitosa, pero si nos intentamos loguear, solo nos pondra un `login exitoso`, nada mas, si inspeccionamos la pagina veremos que hay un `script.js`, si entramos dentro veremos lo siguiente:

```js
document.getElementById('register-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const username = document.getElementById('reg-username').value;
  const password = document.getElementById('reg-password').value;

  await fetch('/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  });
  alert('Usuario registrado.');
});

document.getElementById('login-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const username = document.getElementById('login-username').value;
  const password = document.getElementById('login-password').value;

  const res = await fetch('/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  });

  const data = await res.json();
  alert(data.message);
});

document.getElementById('admin-btn').addEventListener('click', async () => {
  const res = await fetch('/admin');
  const data = await res.json();
  alert(data.message);
});
```

Vemos que en la siguiente linea hay un `/admin`:

```js
document.getElementById('admin-btn').addEventListener('click', async () => {
  const res = await fetch('/admin');
  const data = await res.json();
  alert(data.message);
});
```

Si no esta bien securizado podremos entrar a la pagina sin ninguna restriccion y sin que estemos logueados como `admin` por lo que podria ser vulnerable a un `BAC`.

```
URL = http://<IP>:3000/admin
```

Con esto veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (333).png" alt=""><figcaption></figcaption></figure>

Vemos que hemos podido acceder de forma exitosa la panel de administrador, por lo que iremos al segundo `LAB` que sera sobre la vulnerabilidad de `IDOR`.

## LAB 2: IDOR

Si entramos en la pagina veremos un `login` solamente eso, pero si intentamos iniciar sesion con credenciales por defecto no nos dejara, pero lo que si veremos en la `URL` sera lo siguiente:

```
URL = http://<IP>:5000/?username=admin&password=admin
```

Vemos que se esta exponiendo unos parametros en un metodo `GET` mediante la `URL` con esto podremos deducir que dichos parametros no tengan validacion de seguridad y podremos acceder a recursos en los cuales no estamos autorizados gracias a esta vulnerabilidad.

Pero en este caso no tiene ningun directorio oculto y nada parecido en lo que puedas acceder, por lo que habremos descubierto la vulnerabilidad de `IDOR`, pero no hay ningun directorio, tampoco ningun otro usuario, por lo que ya habremos terminado los `2` laboratorios.
