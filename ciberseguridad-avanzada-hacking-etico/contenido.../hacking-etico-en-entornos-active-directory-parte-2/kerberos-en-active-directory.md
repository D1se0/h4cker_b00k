---
icon: key
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

# Kerberos en Active Directory

Para ver como funciona el tema de el `Ticket-Granting Ticket` de forma practica, si reiniciamos la maquina cuando queramos entrara al equipo veremos que nos pide que iniciemos sesion a nivel de dominio con las credenciales de un usuario de dominio.

Este paso sera en el que nosotros tengamos que meter la contraseña para que se realice todo este proceso del `Ticket-Granting Ticket` y podamos entrar al escritorio de forma autenticada.

<figure><img src="../../../.gitbook/assets/image (129).png" alt=""><figcaption></figcaption></figure>

En esa imagen de ahi se ve mediante `Wireshark` como se hace el proceso a nivel de red cuando nosotros metemos la contraseña y se hacer el proceso de autenticacion, en el protocolo de `AS-REQ` significa el `Authentication Service Request` como bien estabamos viendo antes.

Esto es lo que estaria dentro del `Request`:

<figure><img src="../../../.gitbook/assets/image (130).png" alt=""><figcaption></figcaption></figure>

Como bien vimos antes aqui se esta haciendo de la misma forma enviando su `Common Name: empleado1` y despues el `Service Principal Name (SPN)` que seria el `krbtgt` y `CORP`.

Despues vemos que da un mini error por que requiere una `preverificacion` con un `timestamp` para verificar que somos nosotros, por lo que enviamos otro `request` y si nos vamos al segundo `request` ahora veremos 2 campos:

<figure><img src="../../../.gitbook/assets/image (131).png" alt=""><figcaption></figcaption></figure>

El `TIMESTAMP` y el `REQUEST`, si vemos dentro del `TIMESTAMP` veremos el valor cifrado con nuestra clave privada que le estamos enviando al `SA`, para que luego este mismo la descifre y verifique que somos nosotros.

<figure><img src="../../../.gitbook/assets/image (132).png" alt=""><figcaption></figcaption></figure>

Y una vez verificado nos responde con un `Replay` que seria el `AS-REP` que esto contendra el paquetito cifrado mas el `ticket` del que tanto estabamos hablando antes:

<figure><img src="../../../.gitbook/assets/image (133).png" alt=""><figcaption></figcaption></figure>

Despues vemos que hacemos un `Request` al `Ticket-Granting Service` que seria la parte del primer `TGS-REQ` que es la parte en la que le enviamos nuestro `ticket` y el `Authenticator` y nos devuelve el `Ticket` de servicio.

<figure><img src="../../../.gitbook/assets/image (134).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../../.gitbook/assets/image (135).png" alt=""><figcaption></figcaption></figure>

Si vemos un poco mas el paquete, vemos que le estamos pidiendo que nos deje entrara en el servicio llamado `host` del `WS01`:

<figure><img src="../../../.gitbook/assets/image (136).png" alt=""><figcaption></figcaption></figure>

Ahora en la parte del `Replay` vemos a ver que nos esta dando el `Ticket` de servicio mas un paquete cifrado que contiene la `clave de sesion`:

<figure><img src="../../../.gitbook/assets/image (137).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../../.gitbook/assets/image (138).png" alt=""><figcaption></figcaption></figure>

Despues vemos otro `Replay` y `Request` el cual hace el mismo proceso que el anterior solo que se esta intentando autenticar contra el servicio `LDAP` el cual es necesario para entrar:

<figure><img src="../../../.gitbook/assets/image (139).png" alt=""><figcaption></figcaption></figure>

Ya despues lo que hace es autenticarse contra los servicios por el protocolo necesario en este caso por `DCERPC` con el `ticket` de servicio junto al `Authenticator`:

<figure><img src="../../../.gitbook/assets/image (140).png" alt=""><figcaption></figcaption></figure>

Esto seria el proceso de `Kerberos` de forma practica.

Si nosotros nos vamos a nuestro `DC` y vemos el siguiente usuario que es esencial para todo esto anterior:

<figure><img src="../../../.gitbook/assets/image (141).png" alt=""><figcaption></figcaption></figure>

Se llama `krbtgt` que en su descripcion pone:

```
Cuenta de servicio del centro de distribución de claves
```

Por lo que este usuario tiene una clave muy larga y no es recomentable cambiarle la clava, ya que cuando se haga el proceso de `kerberos` estariamos cifrando con dicha clave el `Ticket-Granting Ticket` con esa clave muy corta o poco segura, por lo que seria un riesgo de seguridad.

Si nosotros queremos ver el `Service Principal Name` del equipo del `empleado1`, abriremos `PowerShell` y pondremos lo siguiente:

```powershell
cd .\Desktop
. .\new_powerview.ps1
Get-NetComputer -Identity WS01 | select serviceprincipalname
```

Info:

```
serviceprincipalname
--------------------
{RestrictedKrbHost/WS01, RestrictedKrbHost/WS01.corp.local, HOST/WS01, HOST/WS01.corp.local}
```

Y nos aparece los servicios que corren en el mas el identificador del mismo.

Por ejemplo con el `DC` veremos que hay mas servicios corriendo en el:

```powershell
Get-NetComputer -Identity DC01 | select serviceprincipalname
```

Info:

```
serviceprincipalname: {Dfsr-12F9A27C-BF97-4787-9364-D31B6C55EB04/DC01.corp.local,
ldap/DC01.corp.local/ForestDnsZones.corp.local,
ldap/DC01.corp.local/DomainDnsZones.corp.local, DNS/DC01.corp.local...}
```

Si nosotros intentamos acceder al servicio de `SMB` entarndo en un recurso compartido, podremos ver si capturamos las peticiones con `Wireshark` que se hace una autenticacion con el `Ticket-Granting Ticket` que ya tenemos al servicio como estuvimos viendo anteriormente.

```powershell
cd \\WS02\C$
```

Claramente esto dara un error por que no podremos acceder a el, pero si vamos a `Wireshark` veremos que se intento autenticar con el `TGS` para dicho servicio, para que le diera el `Ticket` de servicio para la autenticacion por `SMB`.
