# Metasploit (Importando los resultados de Nessus)

Podremos importar lo que encuentre `Nessus` de vulnerabilidades a `metasploit` directamente, solo tendremos que abrir `Nessus` y `metasploit`.

En `metasploit` estando dentro de la consola, tendremos que cargar el `plugin` de `Nessus` que se hara de la siguiente forma:

```shell
load nessus
```

Info:

```
[*] Nessus Bridge for Metasploit
[*] Type nessus_help for a command listing
[*] Successfully loaded plugin: Nessus
```

Con esto ya cargado podremos utilizar los comandos reservados de `nessus` en `metasploit`, por ejemplo si ponemos:

```shell
nessus_help
```

Podremos ver toda la informacion respecto a comandos sobre este `plugin`.

Y desde ahi tendriamos que conectar nuestro `Nessus` a `metasploit` con los comandos que indica en la ayuda, despues podremos iniciar escaneos desde `metasploit` con `Nessus`, etc... Pero en este caso no vamos a utilizar este `plugin`, lo haremos de otra forma que es mucho mejor y mas comodo de forma visual.

Nos vamos a `Nessus` -> seleccionamos el escaneo que queremos importar en `metasploit` -> nos vamos a la opcion `Export` -> `Nessus`

Esto lo que hara sera descargarnos un fichero llamado `EscaneoIntrusivo_3c2b9q.nessus` o como le hayamos llamado.

Ya podremos cerrar `Nessus` y nos vamos a `metasploit` la consola, para poder importar los resultados ahi y poder gestionarlo todo desde ahi.

Lo importaremos de la siguiente forma, en mi caso utilizare una ruta `relativa`:

```shell
db_import EscaneoIntrusivo_3c2b9q.nessus
```

Una vez importado, con el comando `hosts` podremos ver que `hosts` estan almacenados en la base de datos de `metasploit`, que en mi caso son 2 IP's.

Si queremos ver los servicios que tiene dicha maquina, se podra hacer de la siguiente forma:

```shell
services 192.168.16.129
```

Y esto mostrara todos los servicios que `Nessus` pudo recopilar a la hora de hacer ese escaneo de ese `host`.

Ahora para poder ver las vulnerabilidades que encontro `Nessus` en el escaneo de tal puerto se podra hacer con el siguiente comando:

```shell
vulns -p 21
```

Y mostrara todas las vulnerabilidades de `FTP` (`Puerto 21`) que encontro `Nessus` en su escaneo y asociado al `host` que corresponda.

Si queremos ver todas las vulnerabilidades de un `host`, podremos hacer de la siguiente forma:

```shell
vulns 192.168.16.129
```

Y nos mostrara todas las vulnerabilidades de dicho `host`, a parte de que te viene con referencias para poder ver como funciona esa explotacion de mejor forma con un `CVE` asigando a cada una.

Si queremos buscar algun `exploit` con ese `CVE` podremos hacerlo utilizando `metasploit` de la siguiente forma:

```shell
search cve:2010-2075
```

Y esto nos mostrara los `exploits` que hay asociados a ese `CVE` en la base de datos de `metasploit`.
