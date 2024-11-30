# Introducción al protocolo DNS

`DNS` es el acronimo de `Domain Name System`, traduce nombres de dominio a direcciones IP, basicamente resuelve estos dominios a direcciones IP para que asi nuestra red interprete bien hacia donde nos queremos conectar en vez de tener que meter la IP del dominio a pelo, metemos lo que se le llama el dominio (Ejemplo: www.youtube.com) que estara asociada a una IP y el servidor `DNS` se encarga de traducir ese dominio a la direccion IP asociada a dicho dominio.

Esto dedicado al `hacking` se podria utilizar los nombres de dominio para descubrirlos, resolver ese nombre de dominio con algunas herramientas y obtener asi su IP para luego poder `geolocalizarle`.

Desde un dominio podemos encontrar varias relaciones de `host`, encontrando varias direcciones IP's las cuales nos seran utiles para futuros ataques.

Tambien se pueden utilizar los protocolos `DNS` de algun dominio para realizar tecnicas de explotacion especificas para ganar acceso (Ejemplo: `DNS Spoofing`).

Los `DNS` funcionan como los llamados `DNS Zone` que es una agrupacion de registros (datos) `DNS` que se suelen almacenar en un fichero para poder resolverlo, ya sea de una organizacion o incluso de un usuario.

<figure><img src="../../.gitbook/assets/image (12).png" alt=""><figcaption></figcaption></figure>

A nivel interno, cuando estamos resolviendo un dominio y queremos que nos diga una direccion IP bajo ese dominio, lo que hara de forma interna es preguntar a `Local DNS Resolver` -> en tal caso de que no lo sepa esta misma preguntara a `DNS root name server` que es el servidor raiz de los dominios `DNS` -> en tal caso de que no lo sepa exactamente, esta le devolvera el resultado al `Local DNS Resolver` diciendo que lo tiene que saber otro servidor donde tenga alojados todos los registros de dominios acabados en `.com` (`TLD`) -> Pues este le preguntara a dicho servidor llamado `Top-Level DNS Server` que es donde tienen alojados todos los `TDL` en nuestro caso los dominios acabados en `.com` este servidor lo mas probable es que no lo tenga exactamente pero si tendra el `servidor de dominio` de ese dominio, por lo que le devolvera la informacion al `Local DNS Resolver` proporcionandole el `Name Server` del dominio que estamos intentando resolver -> y con esa informacion lo que hara `Local DNS Resolver` sera preguntar a `Authoritative DNS Server` y este servidor si tendra la IP de ese dominio al que estamos preguntando por lo que nos dara la IP al `Local DNS Resolver` y este mismo nos proporcionara la IP al `usuario` y por ultimo teniendo la IP como `usuario` lo que hariamos sera con nuestro navegador pedir una peticion directamente al `Web Server` con dicha direccion IP, que en este caso esta alojando el dominio de la IP y este `Web Server` nos devolvera la pagina web asociado a esa IP.

Y con estos diferentes `Name Servers` podremos extraer informacion del propio dominio para ver posibles vectores de entrada.

Y mas adelante aprovecharemos esto, para hacer `DNS Spoofing` que consiste en nosotros como atacantes ponernos a la escucha donde esta el `Local DNS Resolver` y en vez de que ese `Name Server` le de al `usuario` la IP correcta nosotros como atacantes le daremos una IP nuestra donde se metera el `usuario` y metiendo las credenciales nos llegara a nosotros.
