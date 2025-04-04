---
icon: user-police-tie
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

# Autenticación y Autorización en Windows

> Autenticacion y credenciales en Windows

<figure><img src="../../../.gitbook/assets/image (164).png" alt=""><figcaption></figcaption></figure>

Cuando nosotros vamos a iniciar sesion en `Windows` por detras ocurre esto, en este caso una autenticacion de forma local, lo que hace es que las credenciales que enviamos, junto con el paquete de autenticacion (`Kerberos`) lo recibe el `Servidro LSA` (`Local Security Authority`) y este las valida mediante el protocolo `NTLM` que estara en la base de datos dentro de este `LSA`.

Basicamente si nosotros nos logeamos mediante un usuario de dominio, nosotros estaremos en la parte de `Credential/Login Layer` una vez que le pasamos las credenciales sobre el usuario del dominio al `LSA` este ve que es un usuario de dominio y ejecuta la `dll` de `kerberos` ya que el proceso de autenticacion tiene que ser con ese (`kerberos.dll`) y haria todo el proceso de `Kerberos` que ya vimos anteriormente, pero si nos logeamos con unas credenciales de un usuario local, lo que va hacer el `LSA` es ejecutar la autenticacion `NTLM` (`Msv1_0.dll`) ya que no seria un usuario de dominio.

Para nosotros logearnos con un usuario `local` lo que tendremos que poner en el nombre de usuario para que no nos invoque el `CORP` sera `.\username` (Donde `username` es el usuario local) y asi automaticamente veremos abajo que estara pillando el nombre del equipo local.

<figure><img src="../../../.gitbook/assets/image (165).png" alt=""><figcaption></figcaption></figure>

> LSA Logon Sessions

Cuando un usuario se autentica correctamente, el paquete de `autenticacion` crea una `logon session` y devuelve informacion a la autoridad de `seguridad local` (`LSA`)

El modulo `LSA` usa esta informacion para crear un `Access Token` para el nuevo usuario

Este `token` incluye, entre otras cosas, un `identificador unico local` (`LUID`) para la `logon session`, denominada `identificador de inicio de sesion`

URL = [Info Logon Sessions](https://docs.microsoft.com/es-es/windows/win32/secauthn/lsa-logon-sessions)

> Interactive Authentication

La `autenticacion es interactiva` cuando se solicita al usuario que proporcione informacion de `inicio de sesion`

La `autoridad de seguridad local` (`LSA`) realiza una `autenticacion interactiva` cuando un usuario `inicia sesion` a traves de la interfaz de usuario de `GINA`.

Si la `autenticacion` se realiza correctamente, comienza la `logon session` del usuario y se guarda un `conjunto de credenciales` de `inicio de sesion` para futuras `referencias`.

Basicamente este mecanisco es cuando iniciamos sesion en una interfaz normal de usuario y despues de hace todo este proceso anterior se queda un proceso en el sistema corriendo donde tiene las `credenciales` guardadas en `memoria` para poderlas reutilizar mas adelante. (Un vector de entrada obteniendo esas `credenciales en memoria`)

URL = [Info Interactive Authentication](https://docs.microsoft.com/es-es/windows/win32/secauthn/interactive-authentication)

> NonInteractive Authentication

La `autenticacion no interactiva` solo se puede usar despues de que se haya realizado una `autenticacion interactiva`

El usuario no introduce datos de `inicio de sesion`; en su lugar, se usan las `credenciales establecidas` y `almacenadas previamente`

Se utiliza para `conectarse` a varias maquinas y `servicios en red` sin tener que volver a introducir las `credenciales`

URL = [Info NonInteractive Authentication](https://docs.microsoft.com/es-es/windows/win32/secauthn/noninteractive-authentication)

Cuando nosotros nos hemos autenticado en un `Windows` podremos ver esas `Logon Sessions` con una herramienta que nos porporciona el propio `Microsoft` en el siguiente link:

URL = [Download LogonSessions Tool](https://learn.microsoft.com/es-es/sysinternals/downloads/logonsessions)

Vemos que se nos descarga un `ZIP`, por lo que lo tendremos que descomprimir, una vez echo eso, tendremos una carpeta con unos ejecutables, el que nos interesa es el llamado `logonsessions.exe`.

Abriremos un `PowerShell` como `Administrador` y lo ejecutaremos de la siguiente forma:

```powershell
cd C:\Users\santiago2\Desktop\logonSessions
.\logonsessions.exe
```

<figure><img src="../../../.gitbook/assets/image (166).png" alt=""><figcaption></figcaption></figure>

Nos abrira esto de aqui, le daremos `Agree` y en la terminal veremos todas las `logon sessions`:

```
LogonSessions v1.41 - Lists logon session information
Copyright (C) 2004-2020 Mark Russinovich
Sysinternals - www.sysinternals.com


[0] Logon session 00000000:000003e7:
    User name:    CORP\WS02$
    Auth package: Negotiate
    Logon type:   (none)
    Session:      0
    Sid:          S-1-5-18
    Logon time:   18/01/2025 14:08:13
    Logon server:
    DNS Domain:   corp.local
    UPN:          WS02$@corp.local

[1] Logon session 00000000:0000ca74:
    User name:
    Auth package: NTLM
    Logon type:   (none)
    Session:      0
    Sid:          (none)
    Logon time:   18/01/2025 14:08:14
    Logon server:
    DNS Domain:
    UPN:

[2] Logon session 00000000:0000cfc8:
    User name:    Font Driver Host\UMFD-1
    Auth package: Negotiate
    Logon type:   Interactive
    Session:      1
    Sid:          S-1-5-96-0-1
    Logon time:   18/01/2025 14:08:14
    Logon server:
    DNS Domain:   corp.local
    UPN:          WS02$@corp.local

[3] Logon session 00000000:0000d019:
    User name:    Font Driver Host\UMFD-0
    Auth package: Negotiate
    Logon type:   Interactive
    Session:      0
    Sid:          S-1-5-96-0-0
    Logon time:   18/01/2025 14:08:14
    Logon server:
    DNS Domain:   corp.local
    UPN:          WS02$@corp.local

[4] Logon session 00000000:000003e4:
    User name:    CORP\WS02$
    Auth package: Negotiate
    Logon type:   Service
    Session:      0
    Sid:          S-1-5-20
    Logon time:   18/01/2025 14:08:14
    Logon server:
    DNS Domain:
    UPN:

[5] Logon session 00000000:00012af7:
    User name:    Window Manager\DWM-1
    Auth package: Negotiate
    Logon type:   Interactive
    Session:      1
    Sid:          S-1-5-90-0-1
    Logon time:   18/01/2025 14:08:14
    Logon server:
    DNS Domain:
    UPN:

[6] Logon session 00000000:00012b23:
    User name:    Window Manager\DWM-1
    Auth package: Negotiate
    Logon type:   Interactive
    Session:      1
    Sid:          S-1-5-90-0-1
    Logon time:   18/01/2025 14:08:14
    Logon server:
    DNS Domain:
    UPN:

[7] Logon session 00000000:000003e5:
    User name:    NT AUTHORITY\SERVICIO LOCAL
    Auth package: Negotiate
    Logon type:   Service
    Session:      0
    Sid:          S-1-5-19
    Logon time:   18/01/2025 14:08:14
    Logon server:
    DNS Domain:
    UPN:

[8] Logon session 00000000:00103826:
    User name:    WS02\santiago2
    Auth package: NTLM
    Logon type:   Interactive
    Session:      1
    Sid:          S-1-5-21-2082512782-1542906622-3282704137-1001
    Logon time:   18/01/2025 14:23:07
    Logon server: WS02
    DNS Domain:
    UPN:

[9] Logon session 00000000:001038c3:
    User name:    WS02\santiago2
    Auth package: NTLM
    Logon type:   Interactive
    Session:      1
    Sid:          S-1-5-21-2082512782-1542906622-3282704137-1001
    Logon time:   18/01/2025 14:23:07
    Logon server: WS02
    DNS Domain:
    UPN:
```

Si ponemos:

```powershell
.\logonsessions.exe -p
```

Veremos todas las `logon sessions` asociadas a los procesos de cada una.

Si esto lo ejecutamos con un usuario de dominio, lo que podremos ver sera algo de informacion diferentes, en vez de utiliza la autenticacion en `NTLM` veremos que esta utilizando la de `Kerberos` en los usuarios de dominio.

Si nosotros desde un equipo a otro en el dominio nos conectamos a otro mediante la terminal a un recurso compartido:

```powershell
cd //WS02/c$
```

Y listamos las `logon sessions` veremos que se autentico mediante `kerberos` y es un `logon type` de tipo `Network`, de forma no interactiva, ya que no nos ha pedido ningun tipo de informacion.

> Access Token (I)

Cuando un usuario `inicia sesion`, el sistema comprueba la `contraseña` del usuario comprobandolo con la informacion almacenada en una `base de datos de seguridad`. Si se autentica correctamente, el sistema genera un `token de acceso`. Cada proceso ejecutado en nombre de este usuario tiene una copia de este `token de acceso`.

Un `token de acceso` es un objeto que describe el contexto de `seguridad` de un `proceso` o `subproceso`.

La informacion de un `token` incluye la `identidad y los privilegios` de la cuenta de usuario asociada al `proceso` o `subproceso`.

El sistema usa un `token de acceso` para `identificar` al usuario cuando un `subproceso` interactua con un `securable object` o intenta realizar una tarea del sistema que requiere `privilegios`.

URL = [Info Access Tokens](https://docs.microsoft.com/es-es/windows/win32/secauthz/access-tokens)

> Access Token (II)

Cada proceso tiene un `token principal` que describe el contexto de `seguridad` de la cuenta de usuario asociada al `proceso`.

De forma predeterminada, el sistema usa el `token principal` cuando un `subproceso` del proceso interactua con un `securable object`.

Ademas, un `subproceso` puede `suplantar` una `cuenta de cliente`. La `suplantacion` permite que los `subprocesos` interactue con `secutable objetcs` mediante el contexto de `seguridad del cliente`.

Un `subproceso` que `suplanta` a un cliente tiene un `token` principal y un `token` de `suplantacion`

Para poder ver los procesos de forma interna respecto a lo que estamos hablando, podremos hacerlo con una herramienta que nos proporciona `Microsoft`:

URL = [Download ProcessExplorer](https://learn.microsoft.com/es-es/sysinternals/downloads/process-explorer)

Esto nos dara un `ZIP` el cual tendremos que descomprimir y ejecutarlo desde `PowerShell` siguiente el mismo procedimiento que la anterior herramienta.
