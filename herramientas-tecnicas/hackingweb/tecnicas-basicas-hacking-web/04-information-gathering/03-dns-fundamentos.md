# DNS: conceptos y registros

## El "GPS" de internet

El Sistema de Nombres de Dominio (DNS) traduce nombres legibles para humanos (`www.ejemplo.com`) en direcciones IP (`192.0.2.1`) que las máquinas usan realmente para comunicarse. Sin DNS, navegar la web requeriría memorizar direcciones IP numéricas para cada sitio — tan inviable como memorizar coordenadas GPS exactas para cada destino que se quiere visitar.

## El recorrido de una consulta DNS

1. **El cliente pregunta**: al escribir un dominio, el sistema primero revisa su caché local y el archivo `/etc/hosts` (o el equivalente en Windows); si no encuentra coincidencia, consulta a un **resolver DNS** (normalmente el del ISP, o uno público como `8.8.8.8`/`1.1.1.1`).
2. **El resolver consulta la jerarquía**: si tampoco tiene la respuesta en caché, inicia una búsqueda recursiva empezando por un **servidor raíz**.
3. **El servidor raíz orienta**: no conoce la respuesta exacta, pero sabe qué servidor TLD (`.com`, `.org`, etc.) es responsable de esa extensión, y redirige ahí.
4. **El servidor TLD concreta**: indica qué servidor de nombres **autoritativo** gestiona el dominio exacto consultado.
5. **El servidor autoritativo responde**: devuelve la dirección IP real asociada al dominio.
6. **El resolver entrega y cachea**: la respuesta vuelve al cliente, que la almacena en caché temporalmente para futuras consultas.
7. **Conexión directa**: con la IP ya conocida, el cliente se conecta directamente al servidor que aloja el recurso.

## El archivo hosts

`/etc/hosts` (Linux/macOS) o `C:\Windows\System32\drivers\etc\hosts` (Windows) permite mapear manualmente nombres de host a direcciones IP, evitando por completo la resolución DNS para esas entradas concretas.

```
127.0.0.1       localhost
10.10.10.5      maquina.htb
```

Esto es extremadamente relevante en pentesting: muchos laboratorios y entornos de prueba usan dominios internos que no están publicados en ningún DNS público, y la única forma de resolverlos correctamente es añadiéndolos manualmente al archivo hosts — el mismo mecanismo que ya se mencionó en el bloque de *Web Requests*.

## Zonas DNS y archivos de zona

Una **zona DNS** es la porción del espacio de nombres gestionada por una entidad concreta — por ejemplo, `ejemplo.com` y todos sus subdominios suelen pertenecer a la misma zona. El **archivo de zona** es el documento que define todos los registros de esa zona:

```
$TTL 3600
@       IN SOA   ns1.ejemplo.com. admin.ejemplo.com. (
                2026060401 3600 900 604800 86400 )
@       IN NS    ns1.ejemplo.com.
@       IN MX 10 mail.ejemplo.com.
www     IN A     192.0.2.1
ftp     IN CNAME www.ejemplo.com.
```

## Tipos de registro DNS

| Tipo | Nombre completo | Función | Ejemplo |
|---|---|---|---|
| `A` | Address | Nombre de host → IPv4 | `www.ejemplo.com. IN A 192.0.2.1` |
| `AAAA` | IPv6 Address | Nombre de host → IPv6 | `www.ejemplo.com. IN AAAA 2001:db8::1` |
| `CNAME` | Canonical Name | Alias hacia otro nombre de host | `blog.ejemplo.com. IN CNAME servidor.net.` |
| `MX` | Mail Exchange | Servidor(es) de correo del dominio | `ejemplo.com. IN MX 10 mail.ejemplo.com.` |
| `NS` | Name Server | Delega la zona a un servidor autoritativo | `ejemplo.com. IN NS ns1.ejemplo.com.` |
| `TXT` | Text | Texto libre — verificación, SPF, DKIM | `IN TXT "v=spf1 mx -all"` |
| `SOA` | Start of Authority | Metadatos administrativos de la zona | servidor primario, email admin, número de serie |
| `SRV` | Service | Host y puerto de un servicio concreto | `_sip._udp.ejemplo.com.` |
| `PTR` | Pointer | Búsqueda inversa: IP → nombre de host | `1.2.0.192.in-addr.arpa. IN PTR www.ejemplo.com.` |

## Por qué el DNS es tan valioso en reconocimiento

- **Descubrimiento de activos**: un registro `CNAME` apuntando a un servidor con nombre sospechoso (`dev.ejemplo.com CNAME viejoservidor.net`) puede señalar un sistema obsoleto y potencialmente vulnerable.
- **Mapeo de infraestructura**: los registros `NS` revelan el proveedor de hosting/DNS; un registro `A` apuntando a `loadbalancer.ejemplo.com` indica la presencia (y posiblemente la ubicación) de un balanceador de carga.
- **Monitorización de cambios**: la aparición repentina de un nuevo subdominio (`vpn.ejemplo.com`) puede señalar un nuevo punto de entrada a la red; un registro `TXT` con un valor como `_1password=...` revela qué herramientas usa internamente la organización, información reutilizable en ingeniería social dirigida.

Con estos fundamentos claros, el siguiente paso es ver las herramientas prácticas para consultar y explotar esta información — empezando por `dig`.
