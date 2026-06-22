# Herramientas DNS: dig y consultas

## Panorama de herramientas

| Herramienta | Para qué sirve |
|---|---|
| `dig` | Consultas DNS detalladas y flexibles — la herramienta de referencia |
| `nslookup` | Consultas básicas (A, AAAA, MX) |
| `host` | Consultas rápidas y concisas |
| `dnsenum` | Enumeración automatizada: fuerza bruta, transferencias de zona, scraping de Google |
| `fierce` | Descubrimiento recursivo de subdominios con detección de comodines |
| `dnsrecon` | Combina múltiples técnicas de reconocimiento DNS |
| `theHarvester` | OSINT general (correos, subdominios) a partir de múltiples fuentes |

## `dig` (Domain Information Groper)

La herramienta más versátil para consultas DNS manuales.

```bash
dig dominio.com           # registro A por defecto
dig dominio.com A         # IPv4
dig dominio.com AAAA      # IPv6
dig dominio.com MX        # servidores de correo
dig dominio.com NS        # servidores de nombres autoritativos
dig dominio.com TXT       # registros de texto
dig dominio.com CNAME     # alias
dig dominio.com SOA       # autoridad de la zona
dig @1.1.1.1 dominio.com  # usando un servidor DNS específico
dig +trace dominio.com    # muestra toda la ruta de resolución
dig -x 192.168.1.1        # búsqueda inversa (IP → nombre)
dig +short dominio.com    # respuesta concisa
dig +noall +answer dominio.com  # solo la sección de respuesta
```

> Algunos servidores ignoran las consultas `ANY` (que en teoría devuelven todos los registros disponibles) conforme a RFC 8482, para reducir carga y prevenir abuso — no hay que sorprenderse si no devuelve nada útil.

### Anatomía de una respuesta

```
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 16449
;; flags: qr rd ad; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0

;; QUESTION SECTION:
;google.com.                    IN      A

;; ANSWER SECTION:
google.com.             0       IN      A       142.251.47.142
```

- **Header**: estado de la consulta (`NOERROR` indica éxito) y conteo de entradas por sección.
- **Question**: lo que se preguntó.
- **Answer**: la respuesta concreta, incluyendo el `TTL` (tiempo en segundos que el resultado puede cachearse antes de refrescar).
- **Footer**: tiempo de consulta, servidor que respondió, protocolo usado, tamaño del mensaje.

```bash
dig +short hackthebox.com
104.18.20.126
104.18.21.126
```

## Caso de uso: búsqueda inversa (PTR)

```bash
dig -x 134.209.24.248
```

Devuelve el nombre de dominio asociado a una IP concreta (si existe un registro PTR configurado), útil para confirmar que una IP descubierta por otros medios pertenece efectivamente al objetivo que se está auditando, o para descubrir dominios adicionales alojados en la misma IP.

## Precaución operativa

Algunos servidores DNS detectan y limitan consultas excesivas en poco tiempo, lo que puede bloquear temporalmente la IP del auditor o disparar alertas. Como con cualquier técnica de reconocimiento activo, conviene contar siempre con autorización explícita antes de lanzar consultas DNS masivas o automatizadas contra un objetivo, y moderar el ritmo cuando sea razonablemente posible.
