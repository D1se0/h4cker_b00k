---
icon: house-chimney
---

# Direccionamiento IP y Subnetting

> Cada dispositivo en Internet necesita una dirección. Aquí aprenderás a leerla, saber qué rangos son especiales, calcular subredes sin miedo y entender por qué tu móvil tiene una IP `192.168.x.x` pero Internet te ve con otra.

***

## IPv4: anatomía de una dirección

Una dirección IPv4 son **32 bits** escritos como 4 octetos en decimal:

```
192.168.1.50
  = 11000000.10101000.00000001.00110010
```

Cada dirección lleva implícita otra información: **qué parte identifica la red** y **qué parte el host**. Eso lo determina la **máscara de subred**.

### Notación CIDR

Se escribe `/n` indicando cuántos bits (empezando por la izquierda) son de **red**:

| CIDR | Máscara decimal | IPs totales | Hosts útiles                   |
| ---- | --------------- | ----------- | ------------------------------ |
| /8   | 255.0.0.0       | 16.777.216  | 16.777.214                     |
| /16  | 255.255.0.0     | 65.536      | 65.534                         |
| /24  | 255.255.255.0   | 256         | 254                            |
| /30  | 255.255.255.252 | 4           | 2 (enlaces punto a punto)      |
| /31  | 255.255.255.254 | 2           | 2 (RFC 3021, enlaces modernos) |
| /32  | 255.255.255.255 | 1           | host único                     |

> 💡 Cálculo mental rápido: hosts útiles = 2^(32-n) − 2 (se restan la **dirección de red** — todos los bits de host a 0 — y el **broadcast** — todos a 1). Con /24: 2⁸ − 2 = 254.

### IP pública vs privada

* **Pública:** única en Internet, la asigna tu operador. Es "quién eres" para el mundo.
* **Privada:** solo válida dentro de tu LAN. Se reutiliza en millones de casas a la vez. Para salir a Internet hace falta **NAT** (capítulo [04](04-nat-y-cgnat.md)).

***

## Los rangos especiales que hay que saber de memoria

Estos rangos **no se enrutan igual que el resto** y los verás constantemente en `ipconfig`, `ifconfig` y en los CTFs:

| Rango               | Nombre                            | Para qué sirve                                                                               |
| ------------------- | --------------------------------- | -------------------------------------------------------------------------------------------- |
| **10.0.0.0/8**      | Privada (10.x.x.x)                | Redes privadas grandes (empresas, Docker por defecto usa 172.17, AWS VPC usa 10.x)           |
| **172.16.0.0/12**   | Privada (172.16.x.x – 172.31.x.x) | Redes privadas medianas                                                                      |
| **192.168.0.0/16**  | Privada (192.168.x.x)             | Redes privadas pequeñas: tu casa                                                             |
| **127.0.0.0/8**     | **Loopback**                      | "Tú mismo". `127.0.0.1` = localhost. Nunca sale del equipo                                   |
| **169.254.0.0/16**  | **Link-local / APIPA**            | Auto-IP cuando el equipo no consigue DHCP → ¡señal de que el DHCP está caído o inalcanzable! |
| **255.255.255.255** | **Broadcast** limitado            | "A todos" en el segmento local                                                               |
| **0.0.0.0**         | Red no especificada               | "Cualquier IP" en rutas y reglas de firewall; "todas mis interfaces" al escuchar             |
| **224.0.0.0/4**     | **Multicast** (Clase D)           | Uno-a-muchos: streaming, descubrimiento (mDNS 224.0.0.251)                                   |
| **100.64.0.0/10**   | **CGNAT**                         | Espacio compartido del operador entre su red y la tuya (capítulo [04](04-nat-y-cgnat.md))    |
| 240.0.0.0/4         | Clase E                           | Experimental, no enrutable                                                                   |
| ::1                 | Loopback IPv6                     | Equivalente IPv6 de 127.0.0.1                                                                |
| fe80::/10           | Link-local IPv6                   | Autoconfiguración (equivale a APIPA)                                                         |
| fc00::/7            | ULA IPv6                          | "IP privadas" en IPv6                                                                        |

### 🎯 Para el hacker ético

* **Ver una 169.254.x.x en el objetivo** = su DHCP falló → posible posicionamiento en la red sin servir IPs.
* **Redes privadas al ganar acceso**: `ip a` / `ipconfig` te revela redes internas adicionales (10.x, 172.16-31.x, 192.168.x) → siguiente salto (pivoting).
* **127.0.0.1**: servicios que escuchan _solo_ en loopback no son accesibles desde fuera... salvo con SSRF, port forwarding o acceso local. Cuidado en los informes.
* Escanear `0.0.0.0` no tiene sentido; escanea el rango **de la subred real** que descubras.

***

## Subnetting: dividir redes sin morir

El objetivo: partir una red grande en redes más pequeñas (seguridad, rendimiento, organización).

### Ejemplo paso a paso: dividir 192.168.1.0/24 en 4 subredes

Necesitas 4 redes → 2 bits más de red → /24 + 2 = **/26**.

| Subred           | Rango       | Broadcast | Hosts útiles |
| ---------------- | ----------- | --------- | ------------ |
| 192.168.1.0/26   | .1 – .62    | .63       | 62           |
| 192.168.1.64/26  | .65 – .126  | .127      | 62           |
| 192.168.1.128/26 | .129 – .190 | .191      | 62           |
| 192.168.1.192/26 | .193 – .254 | .255      | 62           |

**Método universal (el "salto")**: con /26, el tamaño de bloque es 2^(32−26) = 64. Las redes empiezan en 0, 64, 128, 192. Ese salto lo es todo.

### Otro ejemplo: ¿qué red pertenece a 10.20.130.45/22?

* /22 → bloque de 2^(32−22) = 1024 → los rangos van de 4 en 4 en el tercer octeto: 0, 4, 8, ..., 128, 132...
* 130 está entre 128 y 131 → red = **10.20.128.0/22**, broadcast = 10.20.131.255, hosts: 10.20.128.1 – 10.20.131.254.

> 💡 Practica con [subnettingpractice.com](https://subnettingpractice.com) hasta hacerlo en <30 segundos. En certificaciones y CTFs de AD se calcula constantemente.

***

## DHCP: cómo consigues tu IP

Cuando conectas un equipo a la red, el protocolo **DHCP** le asigna IP, máscara, gateway y DNS. El proceso es el _DORA_:

1. **D**iscover (broadcast): "¿hay algún servidor DHCP?"
2. **O**ffer: el servidor ofrece una IP.
3. **R**equest: el cliente pide esa IP.
4. **A**cknowledge: el servidor confirma con un tiempo de concesión (lease).

### 🎯 Para el hacker ético

* **Rogue DHCP / DHCP starvation:** un atacante puede responder antes que el DHCP legítimo y convertirse en gateway/DNS de las víctimas → MITM total. Es uno de los ataques de capa 2/3 más devastadores en redes locales.
* Los Discover son broadcasts: con una sola máquina y `tcpdump -i eth0 port 67 or port 68` ves toda la actividad DHCP del segmento.

***

## IPv6: lo básico imprescindible

* 128 bits, escrito en hexadecimal con grupos de 16 bits separados por `:` — `2001:0db8:0000:0000:0000:ff00:0042:8329`.
* Se abrevia: se suprimen ceros a la izquierda y **un solo grupo de ceros consecutivos** se sustituye por `::` → `2001:db8::ff00:42:8329`.
* **Ya no hay NAT ni broadcast**: cada dispositivo puede tener IP pública global. El "escaneo" de una subred /64 por fuerza bruta es inviable (2⁶⁴ hosts).
* Tipos: `::1` loopback, `fe80::/10` link-local, `2000::/3` global (Internet), `fc00::/7` local (ULA), `ff02::1` "todos los nodos" (multicast).

> 🎯 **La IPv6 olvidada:** muchísimas redes corporativas filtran IPv4 a conciencia y **dejan IPv6 sin configurar** (firewall sin reglas `ip6tables`, servicios escuchando en `::`). Casi siempre merece la pena mirar `ip -6 a` en un objetivo.

***

## Comandos esenciales

```bash
# Ver tus IPs, máscaras e interfaces
ip a                    # Linux moderno
ipconfig /all           # Windows (más detalle: DHCP, DNS, leases)
ifconfig                # Legacy

# Tabla de rutas (¿quién es mi gateway?)
ip route                # Linux
route print             # Windows

# Probar conectividad capa 3
ping -c 4 1.1.1.1
ping -6 2001:4860:4860::8888

# ¿Quién es mi IP pública? (la que ve Internet)
curl ifconfig.me
curl api.ipify.org

# Ver/limpiar la caché ARP (capa 2-3)
ip neigh                # Linux
arp -a                  # Ambos
```

***

## Resumen rápido

* IPv4 = 32 bits; el CIDR `/n` indica bits de red; hosts útiles = 2^(32−n) − 2.
* Privadas: `10/8`, `172.16/12`, `192.168/16`. Especiales: loopback `127/8`, APIPA `169.254/16`, broadcast `255.255.255.255`, no especificada `0.0.0.0`, multicast `224/4`, **CGNAT `100.64/10`**.
* Subnetting = técnica del "salto" (tamaño de bloque 2^(32−n)).
* DHCP asigna IPs con el baile DORA y es atacable (rogue DHCP).
* IPv6: sin NAT, `::` abreviatura, y revisa siempre si está sin proteger.

**Siguiente capítulo →** [04 · NAT, CGNAT y Hole Punching](04-nat-y-cgnat.md)
