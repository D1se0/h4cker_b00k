# Virtual Hosts

## El problema: una IP, múltiples sitios

Un servidor web no está limitado a alojar un único sitio. Mediante el **alojamiento virtual** (*virtual hosting*), Apache, Nginx o IIS pueden servir contenido completamente distinto dependiendo de qué dominio se haya solicitado, todo desde la misma dirección IP. Esto se logra gracias a la cabecera HTTP **`Host`**, que el navegador incluye en cada petición indicando qué dominio está solicitando.

## Virtual Hosts vs. Subdominios: la diferencia clave

Aunque suelen confundirse, son conceptos distintos relacionados con capas diferentes:

- **Subdominio**: una extensión de un dominio principal (`blog.ejemplo.com`), con su propio registro DNS, que puede (o no) apuntar a la misma IP que el dominio raíz.
- **Virtual Host**: una configuración a nivel de **servidor web** que determina qué contenido servir según el valor de la cabecera `Host` recibida — independientemente de si ese nombre tiene un registro DNS público o no.

Esto tiene una implicación crucial para reconocimiento: **un virtual host puede existir y ser perfectamente accesible aunque no tenga ningún registro DNS asociado**. Si se conoce (o se adivina) el nombre exacto, basta con enviar una petición a la IP del servidor especificando manualmente ese nombre en la cabecera `Host` — o añadiendo una entrada al archivo `/etc/hosts` local — para acceder a ese contenido, sin que nunca haya sido "descubrible" mediante una consulta DNS pública normal.

## Cómo decide el servidor qué contenido servir

1. El navegador solicita un dominio; se resuelve su IP (vía DNS o `/etc/hosts`).
2. La petición HTTP incluye la cabecera `Host: nombre-solicitado`.
3. El servidor web recibe la petición y compara ese valor contra su configuración interna de virtual hosts.
4. Encuentra la configuración correspondiente y sirve el contenido de ese sitio concreto.

```apache
<VirtualHost *:80>
    ServerName www.sitio1.com
    DocumentRoot /var/www/sitio1
</VirtualHost>

<VirtualHost *:80>
    ServerName www.sitio2.org
    DocumentRoot /var/www/sitio2
</VirtualHost>
```

Ambos sitios comparten la misma IP; el servidor decide qué `DocumentRoot` servir únicamente en función del `Host` recibido.

## Tipos de alojamiento virtual

| Tipo | Cómo distingue el sitio | Ventajas | Limitaciones |
|---|---|---|---|
| **Basado en nombre** | Cabecera `Host` | No requiere IPs adicionales, configuración flexible | Requiere soporte explícito del servidor; complicaciones históricas con SSL/TLS (mitigadas hoy con SNI) |
| **Basado en IP** | Dirección IP de destino | Mejor aislamiento, compatible con cualquier protocolo | Requiere una IP por sitio — más costoso y menos escalable |
| **Basado en puerto** | Puerto de conexión | Útil cuando las IPs son limitadas | Menos común; obliga a especificar el puerto en la URL |

## Por qué descubrir virtual hosts es tan valioso

Muchos sitios mantienen virtual hosts internos o de prueba que **deliberadamente no tienen registro DNS público**, precisamente para que no sean descubribles mediante reconocimiento DNS convencional. Esta práctica de "seguridad por oscuridad" es frágil: basta con probar sistemáticamente nombres plausibles contra la IP conocida del servidor, observando si la respuesta varía (tamaño, contenido, código de estado) respecto a una petición de control con un `Host` inventado.

## Fuzzing de virtual hosts con Gobuster

```bash
gobuster vhost -u http://10.10.10.5 -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt --append-domain
```

- `-u`: IP o URL del objetivo.
- `-w`: wordlist de nombres candidatos.
- `--append-domain`: añade el dominio base a cada palabra de la lista para construir el nombre completo del host a probar (en versiones recientes de Gobuster es obligatorio para que la construcción del nombre sea correcta).

```
Found: forum.inlanefreight.htb:81 Status: 200 [Size: 100]
```

Cada resultado con un tamaño de respuesta distinto al de un host "control" inexistente es candidato a un virtual host real — conviene siempre comparar contra una petición de base con un nombre claramente inventado, para establecer cuál es el comportamiento "por defecto" del servidor y filtrar así falsos positivos.

Flags adicionales útiles: `-t` (más hilos, mayor velocidad), `-k` (ignorar errores de certificado SSL en HTTPS), `-o` (guardar resultados en archivo).

Otras herramientas equivalentes: `ffuf` (fuzzing manipulando directamente la cabecera `Host`) y `feroxbuster` (con soporte de recursión y detección de comodines).

## Tras el descubrimiento

Un virtual host encontrado sin registro DNS sigue siendo accesible añadiendo manualmente una entrada al archivo `/etc/hosts` apuntando ese nombre a la IP del servidor — exactamente el mismo mecanismo visto en el apartado de fundamentos DNS — permitiendo navegarlo con normalidad desde el navegador como si tuviera resolución pública.
