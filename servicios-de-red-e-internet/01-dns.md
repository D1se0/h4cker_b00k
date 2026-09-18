# 📖 01 · DNS: El Teléfono de Internet

> Internet funciona con direcciones IP, pero los humanos recordamos nombres. El **DNS (Domain Name System)** es el traductor: convierte `google.com` en `142.250.x.x`. Es, además, **uno de los servicios más explotados en hacking**: fugas de información, transferencias de zona, subdominios olvidados, tunneling...

---

## ¿Qué es y para qué sirve?

El DNS es un **servicio distribuido y jerárquico** que resuelve nombres de dominio a direcciones IP (y viceversa). Sin él tendrías que memorizar `142.250.200.46` en vez de `google.com`.

### Jerarquía del DNS

```
.                  (raíz)
└── com.           (TLD — Top Level Domain)
    └── ejemplo.com.   (dominio)
        ├── www        (subdominio / host)
        └── mail       (subdominio / host)
```

- **Root servers:** 13 grupos de servidores raíz (a.root-servers.net ... m.root-servers.net) que saben dónde están los TLDs.
- **TLDs:** `.com`, `.es`, `.org`, `.dev`... gestionados por registradores.
- **Autoritativo:** el servidor que tiene **la información oficial** de la zona del dominio.
- **Recursivo/resolver:** el de tu operador o el público (8.8.8.8, 1.1.1.1, 9.9.9.9) que hace la búsqueda por ti y **guarda caché**.

### Cómo se resuelve un nombre (paso a paso)

1. Escribes `www.ejemplo.com` → tu equipo pregunta al **resolver** (el DNS configurado, p. ej. el router).
2. Si el resolver lo tiene en **caché**, responde al instante. Si no...
3. Pregunta a los **servidores raíz** → "ve a preguntar a los del TLD `.com`".
4. Los del TLD `.com` → "ve a preguntar a los DNS autoritativos de `ejemplo.com`" (los NS).
5. El **autoritativo** responde: `www.ejemplo.com` → `93.184.216.34`.
6. La respuesta se guarda en caché durante el **TTL** (Time To Live, en segundos) y se te devuelve.

> 🎯 **Para el hacker ético:** el TTL corto significa cambios rápidos (y también respuestas más fáciles de envenenar en ataques de cache poisoning). Y el resolver de tu operador puede estar filtrando o reescribiendo respuestas — con `dig +trace` ves toda la cadena.

---

## Tipos de registros DNS (imprescindibles)

La información del DNS se guarda en **registros** dentro de las zonas. Estos son los que hay que dominar:

| Tipo | Nombre | Qué hace | Ejemplo |
|------|--------|----------|---------|
| **A** | Address | Dice qué **IPv4** tiene un dominio | `google.com → 142.250.x.x` |
| **AAAA** | IPv6 Address | Lo mismo que A, pero para **IPv6** | `google.com → 2a00:1450:...` |
| **CNAME** | Canonical Name | Hace que un dominio sea **alias** de otro | `www.ejemplo.com → ejemplo.com` |
| **MX** | Mail Exchange | Dice **qué servidor recibe el correo** del dominio | `ejemplo.com → mail.ejemplo.com` |
| **NS** | Name Server | Dice **qué servidores DNS** tienen la información del dominio | `ejemplo.com → ns1.ejemplo.com` |
| **TXT** | Text | Guarda texto asociado al dominio: verificación de dominios, **SPF**, DKIM, DMARC | `v=spf1 include:_spf.google.com ~all` |
| **PTR** | Pointer | Lo contrario que A: **IP → dominio** (DNS inverso) | `8.8.8.8 → dns.google` |
| **SOA** | Start of Authority | Información básica de la zona: servidor principal, correo del admin, números de serie, TTLs | — |
| SRV | Service | Localiza servicios por protocolo/puerto (VoIP, AD) | `_ldap._tcp.dominio` |
| CAA | Certification Authority Authorization | Qué CAs pueden emitir certificados para el dominio | `0 issue "letsencrypt.org"` |

> 💡 **Curiosidad importante:** un mismo nombre puede tener **varios registros A** (balanceo de carga round-robin) y **varios MX** con prioridades (10, 20, 30...: si el primero falla, pasa al siguiente).

### 🎯 Para el hacker ético

- **NS + AXFR:** si el servidor autoritativo permite **transferencia de zona** (`dig axfr @ns1.ejemplo.com ejemplo.com`), te da TODO el mapa del dominio: subdominios, hosts, IPs. Es un fallo clásico de config.
- **TXT (SPF/DKIM/DMARC):** te dicen quién puede enviar correo legítimo de ese dominio → clave para hacer **phishing creíble** o para detectar que el objetivo puede recibir spoofing.
- **Registros antiguos:** subdominios que apuntan a servicios ya borrados → **subdomain takeover**.
- Herramientas: `dig`, `nslookup`, `host`, `dnsrecon`, `sublist3r`, `dnsdumpster` (ya tienes capítulos en la sección de [Reconocimiento](../herramientas-tecnicas/reconocimiento/dominios-subdominios.md)).

---

## Herramientas: `nslookup` y `dig`

Son las dos utilidades clásicas para consultar DNS:

1. **`nslookup`** → más sencillo y fácil de usar. Ideal para consultas rápidas.
2. **`dig`** → más completo y detallado. Da mucha más información sobre la consulta y la respuesta DNS (cabeceras, flags, TTLs, sección AUTHORITY...).

### `nslookup` — lo rápido

```bash
nslookup google.com              # Consulta A básica
nslookup -type=mx ejemplo.com    # Registros MX del dominio
nslookup -type=ns ejemplo.com    # Servidores autoritativos
nslookup -type=txt ejemplo.com   # Registros TXT (SPF, verificaciones)
nslookup 8.8.8.8                 # Resolución inversa (usa PTR)
nslookup google.com 1.1.1.1      # Preguntar a un DNS concreto
```

### `dig` — lo profesional

```bash
dig google.com                   # Consulta A con toda la info
dig +short google.com            # Solo la respuesta (perfecto para scripts)
dig mx ejemplo.com +short        # MX en formato corto
dig ANY ejemplo.com +nostatistics
dig @1.1.1.1 ejemplo.com         # Preguntar a otro resolver
dig -x 8.8.8.8                   # Resolución inversa (PTR)
dig +trace ejemplo.com           # 🔥 Muestra TODA la cadena: raíz → TLD → autoritativo
dig axfr @ns1.ejemplo.com ejemplo.com   # 🔥 Transferencia de zona (inténtalo en los CTF)
```

> 💡 La sección **ANSWER** es la respuesta; **AUTHORITY** quién responde oficialmente; **ADDITIONAL** info extra. El flag **AA** en flags significa que responde un servidor autoritativo (no desde caché).

---

## DNS inverso (PTR)

Normalmente resuelves *nombre → IP*. El **DNS inverso** hace *IP → nombre* usando la zona especial `in-addr.arpa` (IPv4) o `ip6.arpa` (IPv6).

```bash
dig -x 8.8.8.8
# 8.8.8.8.in-addr.arpa.  IN  PTR  dns.google.
```

Sirve para saber qué hostname hay detrás de una IP — útil al enumerar rangos de un objetivo.

---

## Conceptos modernos que debes conocer

| Concepto | Qué es |
|----------|--------|
| **DoH** (DNS over HTTPS) | Consultas DNS dentro de HTTPS (puerto 443): el ISP no ve qué dominios preguntas |
| **DoT** (DNS over TLS) | Lo mismo, pero por TLS directo al puerto 853 |
| **DNSSEC** | Firma criptográfica de las respuestas DNS para evitar envenenamiento de caché |
| **Split-horizon DNS** | El mismo dominio resuelve distinto dentro/fuera de la red interna |

> 🎯 El **split-horizon** es oro en pentesting: los DNS internos de una empresa (los que están en la VLAN del empleado) suelen resolver nombres de servidores que **nunca aparecen en Internet**. Si consigues acceso a un host interno, pregunta al DNS interno con todo lo que encuentres.

---

## Resumen rápido

- DNS traduce nombres → IPs con una jerarquía: raíz → TLD → autoritativo, con caché y TTL.
- Registros clave: **A/AAAA** (IPs), **CNAME** (alias), **MX** (correo), **NS** (servidores), **TXT** (SPF/DKIM/DMARC), **PTR** (inverso), **SOA** (info de zona).
- `nslookup` para consultas rápidas; `dig` para análisis completo (`+trace`, `axfr`).
- En hacking: transferencias de zona, subdomain takeover, DNS interno y tunneling son los vectores clásicos.

**Siguiente capítulo →** [02 · Correo Electrónico](02-correo-electronico.md)
