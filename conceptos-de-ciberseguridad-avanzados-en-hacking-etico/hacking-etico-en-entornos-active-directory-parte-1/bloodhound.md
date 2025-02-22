---
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

# BloodHound

Es una de las herramientas mas utilizadas y mas famosas de recopilacion de informacion y nos sirve tambien como herramienta de analisis de vulnerabilidades es una solucion que se basa en la teoria de grafos y lo que va hacer va a ser recopilar toda la informacion de nuestro dominio, todos esos objetos y representarlos en forma de grafos con la relaciones que hay entre ellos.

Encontraremos la herramienta en el siguiente repositorio:

URL = [GitHub BloodHound](https://github.com/SpecterOps/BloodHound-Legacy)

Por defecto no viene instalado en `kali` por lo que lo instalaremos de la siguiente manera:

```shell
sudo apt install bloodhound
```

Con esto se instalara todo lo necesario para dicha herramienta, pero una de las cosas que tambien tendremos que configurar para que esto vaya es el `neo4j` que es una base de datos tambien de grafos la cual depende de `bloodhound` por lo que tendremos que configurarla de forma inicial poniendo lo siguiente:

```shell
sudo neo4j console
```

Info:

```
Directories in use:
home:         /usr/share/neo4j
config:       /usr/share/neo4j/conf
logs:         /etc/neo4j/logs
plugins:      /usr/share/neo4j/plugins
import:       /usr/share/neo4j/import
data:         /etc/neo4j/data
certificates: /usr/share/neo4j/certificates
licenses:     /usr/share/neo4j/licenses
run:          /var/lib/neo4j/run
Starting Neo4j.
2025-01-11 10:26:43.799+0000 INFO  Starting...
2025-01-11 10:26:44.182+0000 INFO  This instance is ServerId{1a29ef32} (1a29ef32-306d-47c3-be55-d61e17c75b31)
2025-01-11 10:26:45.469+0000 INFO  ======== Neo4j 4.4.26 ========
2025-01-11 10:26:48.257+0000 INFO  Initializing system graph model for component 'security-users' with version -1 and status UNINITIALIZED
2025-01-11 10:26:48.265+0000 INFO  Setting up initial user from defaults: neo4j
2025-01-11 10:26:48.265+0000 INFO  Creating new user 'neo4j' (passwordChangeRequired=true, suspended=false)
2025-01-11 10:26:48.278+0000 INFO  Setting version for 'security-users' to 3
2025-01-11 10:26:48.281+0000 INFO  After initialization of system graph model component 'security-users' have version 3 and status CURRENT
2025-01-11 10:26:48.285+0000 INFO  Performing postInitialization step for component 'security-users' with version 3 and status CURRENT
2025-01-11 10:26:48.583+0000 INFO  Bolt enabled on localhost:7687.
2025-01-11 10:26:49.592+0000 INFO  Remote interface available at http://localhost:7474/
2025-01-11 10:26:49.598+0000 INFO  id: 390D82F306A1043B57D7DC446AA80EEE10DF2491E93F5D7EE2B02A438C08A41B
2025-01-11 10:26:49.598+0000 INFO  name: system
2025-01-11 10:26:49.599+0000 INFO  creationDate: 2025-01-11T10:26:46.134Z
2025-01-11 10:26:49.599+0000 INFO  Started.
```

Esto lo que va hacer es crear los ficheros necesarios para dicha base de datos y estara abierta en un link en concreto que lo veremos en la terminal, en mi caso es el siguiente:

```
URL = http://localhost:7474/
```

Por lo que nos conectaremos por ahi en un navegador web.

Lo unico que cambiaremos en la interfaz grafica sera el usuario y contraseña que es lo que nos pide `neo4j`.

```
Usuario: neo4j
Password: neo4j
```

Primero metemos la de por defecto para posteriormente cambiarla:

Ahora te pedira poner una nueva contraseña:

```
Password: <PASSWORD>
```

Y le daremos a `Change Password`.

Ahora ya podemos cerrar la pagina y abriremos otra terminal:

```shell
bloodhound
```

Nos aparecera esta ventana:

<figure><img src="../../.gitbook/assets/image (233).png" alt=""><figcaption></figcaption></figure>

Metemos el usuario que es `neo4j` y la contraseña que pusimos anteriormente en `neo4j`.

Echo esto entraremos en una interfaz blanca en la que de momento no habra datos, pero pongamos que nos dan un equipo `Windows` con el usuario de dominio, lo que haremos sera ejecutar un script del repositorio de `bloodhound` que sera en el siguiente link:

URL = [Script BloodHound WIndows](https://github.com/SpecterOps/BloodHound-Legacy/blob/master/Collectors/SharpHound.ps1)

Copiamos el codigo y lo pegamos en un fichero de texto en la maquina `Windows` del equipo que nos han proporcionado en este caso el `WS01`.

Cambiamos la extension `.txt` a un `.ps1` (`sh.ps1`) y ya estaria listo para ejecutar.

Ahora tendremos que abrir una `PowerShell` en el `empleado1`:

```powershell
cd .\Desktop
. .\sh.ps1
```

Para cargar el script y haremos lo siguiente:

```powershell
Invoke-BloodHound -CollectionMethod All -OutputDirectory "C:\Users\<USER>\Desktop"
```

Con esto lo que hara sera recopilar absolutamente toda la informacion del dominio, pero antes de ejecutarlo haremos un mini cambio en nuestro `DC`.

Nos vamos al `Servidor del Administrador` -> `Usuarios y equipos de Active Directory` -> `Users` -> vamos a crear un nuevo grupo dandole al icono de 2 personas como haciamos anteriormente `Nombre de grupo: Executives` -> `Aceptar` -> click derecho a `Executives` -> `Propiedades` -> `Miembro de` -> `Agregar` -> ponemos `admins` para que coja `admins. del dominio` -> `Aplicar` -> `Aceptar` -> vamos a crear un usuario llamado `empleado4` con inicio al dominio tambien con el mismo nombre con contraseña `Passw0rd4` marcamos el que nunca expira -> `Finalizar` -> click derecho en el `empleado4` -> `Propiedades` -> `Miembro de` -> `Agregar` -> ponemos `Exec` y nos lo rellena con `Executives` -> `Aceptar` -> `Aplicar` -> `Aceptar`.

Con esto lo que hemos echo es crear un grupo de ejecutivos en el que tiene un `subgrupo` que es el de administradores, y el usuario `empleado4` pertenece al de `executives` que a su vez esta en el de admins, por lo que seria un usuario administrador dicho usuario, para que ahora veamos que facil es identificar todo esto en los datos que nos proporciona `BloodHound`.

Ahora si nos vamos a donde estabamos en el equipo `WS01` y ejecutamos el script.

Info:

```
2025-01-11T12:01:25.4792326+01:00|INFORMATION|This version of SharpHound is compatible with the 4.3.1 Release of BloodHound
2025-01-11T12:01:25.4964604+01:00|INFORMATION|Resolved Collection Methods: Group, LocalAdmin, GPOLocalGroup, Session, LoggedOn, Trusts, ACL, Container, RDP, ObjectProps, DCOM, SPNTargets, PSRemote
2025-01-11T12:01:25.4964604+01:00|INFORMATION|Initializing SharpHound at 12:01 on 11/01/2025
2025-01-11T12:01:25.5106617+01:00|INFORMATION|[CommonLib LDAPUtils]Found usable Domain Controller for corp.local : DC01.corp.local
2025-01-11T12:01:25.5265472+01:00|WARNING|Common Library is already initialized
2025-01-11T12:01:25.5418213+01:00|INFORMATION|Flags: Group, LocalAdmin, GPOLocalGroup, Session, LoggedOn, Trusts, ACL, Container, RDP, ObjectProps, DCOM, SPNTargets, PSRemote
2025-01-11T12:01:25.5729660+01:00|INFORMATION|Beginning LDAP search for corp.local
2025-01-11T12:01:25.5889296+01:00|INFORMATION|Producer has finished, closing LDAP channel
2025-01-11T12:01:25.5889296+01:00|INFORMATION|LDAP channel closed, waiting for consumers
2025-01-11T12:01:56.3851906+01:00|INFORMATION|Status: 0 objects finished (+0 0)/s -- Using 96 MB RAM
2025-01-11T12:02:10.5251589+01:00|INFORMATION|Consumers finished, closing output channel
2025-01-11T12:02:10.5433019+01:00|INFORMATION|Output channel closed, waiting for output task to complete
Closing writers
2025-01-11T12:02:10.6275330+01:00|INFORMATION|Status: 98 objects finished (+98 2.177778)/s -- Using 97 MB RAM
2025-01-11T12:02:10.6275330+01:00|INFORMATION|Enumeration finished in 00:00:45.0609824
2025-01-11T12:02:10.6373213+01:00|INFORMATION|Saving cache with stats: 57 ID to type mappings.
 59 name to SID mappings.
 1 machine sid mappings.
 2 sid to domain mappings.
 0 global catalog mappings.
2025-01-11T12:02:10.6525162+01:00|INFORMATION|SharpHound Enumeration Completed at 12:02 on 11/01/2025! Happy Graphing!
```

Esto lo que va hacer es volcarnos 2 ficheros en el escritorio los cuales nos tendremos que pasar al `kali` que seran los que tengamos que cargar en el `BloodHound` para que nos haga el grafo, etc...

<figure><img src="../../.gitbook/assets/image (234).png" alt=""><figcaption></figcaption></figure>

El archivo que nos interesa pasar al `kali` es el `ZIP` por lo que nos lo pasaremos.

Una vez que nos lo hayamos pasado, lo arrastramos el `ZIP` a `BloodHound` y esto cargara todo de forma automatica viendose algo asi:

Le daremos a `Clear Finish` y cuando no veamos nada significa que ya habra cargado todos los archivos del dominio.

Y en la parte de la izquierda ya veremos informacion de primeras:

<figure><img src="../../.gitbook/assets/image (235).png" alt=""><figcaption></figcaption></figure>

Nosotros podremos buscar por un `nodo` en la parte de `Search for a node` pondremos por ejemplo `empleado1` y lo seleccionamos, ya que nos esta detectando que en la informacion que recopilo encontro eso mismo.

<figure><img src="../../.gitbook/assets/image (236).png" alt=""><figcaption></figcaption></figure>

Si nosotros le damos doble click a `empleado1` nos aparece toda la informacion de dicho empleado:

<figure><img src="../../.gitbook/assets/image (237).png" alt=""><figcaption></figcaption></figure>

Si nosotros queremos ver la informacion del grupo de los usuarios del dominio, buscaremos `usuarios` y seleccionamos el que nos encuentra llamado `usuarios del grupo de dominio`.

<figure><img src="../../.gitbook/assets/image (238).png" alt=""><figcaption></figcaption></figure>

Si le damos doble click:

<figure><img src="../../.gitbook/assets/image (239).png" alt=""><figcaption></figcaption></figure>

Vemos cuantos usuarios hay en el, etc...

Ahora si pulsamos en los `Miembros directos` (`Members Direct`) nos sacara todos esos usuarios de forma directa en un grafo:

<figure><img src="../../.gitbook/assets/image (240).png" alt=""><figcaption></figcaption></figure>

Pero lo mas potente que tiene `BloodHound` es que tiene diversas tecnicas, diversas `querys` las cuales podemos ver en la seccion de `Analisys`:

<figure><img src="../../.gitbook/assets/image (241).png" alt=""><figcaption></figcaption></figure>

Lo que hace esto es sacar `qerys` complejas y sacarlas en forma de grafico representandolas graficamente.

Por ejemplo si yo quiero saber de golpe cuales son los `Domains Admins.` podemos pulsar en esta de aqui:

<figure><img src="../../.gitbook/assets/image (242).png" alt=""><figcaption></figcaption></figure>

Y veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (243).png" alt=""><figcaption></figcaption></figure>

Por ejemplo habremos descubierto que `empleado4` pertenece al grupo administradores gracias al grupo `Executives`, por lo que podemos marcarle como usuario de alto valor dandole click derecho al `empleado4`:

<figure><img src="../../.gitbook/assets/image (244).png" alt=""><figcaption></figcaption></figure>

Y pinchamos en la opcion llamada `Mark User as High Value` y ahora lo veremos asi:

<figure><img src="../../.gitbook/assets/image (245).png" alt=""><figcaption></figcaption></figure>

Con el diamante, esto lo hacemos para marcar un usuario importante donde si lo comprometo podremos obtener privilegios de administrador directamente.

Tmbien podremo ver `rutas` mas cortas para llegar a ser `administrador de dominio`.

<figure><img src="../../.gitbook/assets/image (246).png" alt=""><figcaption></figcaption></figure>

Y veremos esto en el grafo:

<figure><img src="../../.gitbook/assets/image (247).png" alt=""><figcaption></figcaption></figure>

Si nosotros por ejemplo no sabemos una de las ruta que nos pone en algun grafico o cualquier cosa, solo le tendremos que dar click derecho y veremos esto:

<figure><img src="../../.gitbook/assets/image (248).png" alt=""><figcaption></figcaption></figure>

Le daremos a `Help`:

<figure><img src="../../.gitbook/assets/image (249).png" alt=""><figcaption></figcaption></figure>

Y podremos ver la informacion de lo que es este `GenericAll`, tambien nos proporciona varios tipos de abuso en los cuales podremos escalar privilegios, a parte de que tambien nos da referencias a paginas y videos en los cuales explica todo esto, etc... Asi en cada uno de ellos.

Podremos ver diversas `qerys` en el siguiente link de `GitHub`:

URL = [Custom Querys BloodHound GitHub](https://github.com/hausec/Bloodhound-Custom-Queries/blob/master/customqueries.json)

Para poder utilizar una `Query personalizda` podremos hacerlo copiando la `Qery` por ejemplo esta de aqui:

```json
		{
            "name": "Find all users that have local admin rights",
            "queryList": [
                {
                    "final": true,
                    "query": "MATCH p=(m:User)-[r:AdminTo]->(n:Computer) RETURN p"
                }
            ]
        }
```

Copiaremos esto en concreto:

```json
MATCH p=(m:User)-[r:AdminTo]->(n:Computer) RETURN p
```

Y lo pegaremos en la siguiente seccion de `BlodHound`:

<figure><img src="../../.gitbook/assets/image (250).png" alt=""><figcaption></figcaption></figure>

Abajo donde pone `Raw Query` lo abrimo y lo pegamos en esa barra de busqueda.

En mi caso me aparecera esto:

<figure><img src="../../.gitbook/assets/image (251).png" alt=""><figcaption></figcaption></figure>

Y tambien podremos importar el `JSON` del GitHub el cual te lo explica todo en los repositorios, etc...
