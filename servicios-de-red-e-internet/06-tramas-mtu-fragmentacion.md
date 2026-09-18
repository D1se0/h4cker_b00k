# 📦 06 · Tramas, MTU y Fragmentación

> ¿Por qué tu VPN conecta pero "va mal"? ¿Por qué un ping enorme falla y el pequeño va bien? Casi siempre es la **MTU**. En este capítulo: cómo se trocea realmente la información que envías y qué pasa cuando un paquete no "cabe" en un enlace.

---

## Del dato al bit: encapsulación

Cuando envías una foto por WhatsApp, tus datos bajan por las capas y **cada capa añade su cabecera** (encapsulación):

```
[ Datos de la app ]
[ TCP | Datos ]              ← segmento (capa 4)
[ IP | TCP | Datos ]         ← paquete (capa 3)
[ Eth | IP | TCP | Datos | FCS ]  ← trama (capa 2)
0101010...                   ← bits (capa 1)
```

- **Segmento** (TCP) / **Datagrama** (UDP) — capa 4
- **Paquete** — capa 3 (IP)
- **Trama** — capa 2 (Ethernet)

Y en el receptor, el proceso inverso (desencapsulación). La cabecera de cada capa es lo que hace posible la multiplexación: **todos tus datos viajan identificados con IP, puerto y MAC de origen y destino**, mezclados con los de todo el mundo en el mismo cable.

---

## MTU: el tamaño máximo

**MTU (Maximum Transmission Unit)** = **el tamaño máximo de paquete IP que puede atravesar un camino sin tener que fragmentarse**. Si un paquete es más grande que la MTU de algún enlace del trayecto, o se fragmenta o se descarta.

| Enlace | MTU típica |
|--------|------------|
| Ethernet estándar | **1500 bytes** |
| PPPoE (fibra de Movistar, Jazztel...) | **1492** (8 bytes menos por la cabecera PPPoE) |
| WireGuard | 1420 (por la sobrecarga del túnel) |
| OpenVPN UDP | ~1450 |
| L2TP/IPsec | ~1430 |

> 📌 *Nota de tu apunte:* "Tamaño máximo de transmisión por una trama, ¿1500?" — Sí: el **payload** de la trama Ethernet estándar es 1500 bytes (la MTU de IP). La trama completa puede llegar a 1518 con cabeceras, o **~1514 bytes útiles en modo promiscuo** según el intérprete, y con jumbo frames (9000) en redes de storage/DC.

### ¿Por qué el "óptimo" se discute en ~1480?

- Con PPPoE la MTU cae a **1492**. Si dentro de eso metes IPsec u otro encapsulado, quedan menos bytes útiles.
- El valor **~1480** es un compromiso seguro que evita fragmentación en la mayoría de caminos reales (PPPoE + algún encapsulado más).
- **Movistar/PPP usa P2P (PPP)**, por eso su trama útil es **8 bytes más pequeña** que la Ethernet estándar.

### El síntoma clásico: la VPN que "va mal"

Si no se configura la MTU en la VPN, los paquetes interiores son demasiado grandes para el túnel:

- ✅ Ping pequeño va bien, SSH conecta... pero se cuelga tras el banner.
- ✅ Las webs pequeñas cargan; las grandes, no.
- ✅ Las descargas grandes fallan a mitad.
- ✅ El handshakes TLS va bien pero la transferencia de datos se congela.

**Solución:**

```bash
# WireGuard
[Interface]
MTU = 1420

# OpenVPN
mssfix 1400

# Diagnóstico: encontrar la MTU real del camino
ping -M do -s 1472 ejemplo.com     # Linux: 1472+28 cabeceras = 1500
ping -f -l 1472 ejemplo.com        # Windows: -f = DF flag
```

Baja el tamaño hasta que pase: esa + 28 es tu MTU real del camino.

---

## Fragmentación: cuando el paquete no cabe

Si un paquete IP supera la MTU del siguiente enlace y no se puede evitar, **IP lo divide en fragmentos** que se reensamblan en el destino final.

Campos IP implicados:

| Campo | Función |
|-------|---------|
| **Identification** | Identifica el paquete original (todos los fragmentos llevan el mismo ID) |
| **Flags** | Bit **DF** (Don't Fragment) y bit MF (More Fragments) |
| **Fragment Offset** | Posición del fragmento dentro del paquete original (en bloques de 8 bytes) |

### El flag DF (Don't Fragment)

**DF** = una bandera del header IP que indica: **"este paquete no puede fragmentarse"**.

- Si el paquete no cabe en un enlace y lleva DF puesto → **se descarta** y el router devuelve un **ICMP Type 3 Code 4** ("fragmentation needed and DF set", *Packet Too Big* en IPv6).
- Ese mensaje ICMP es el corazón de **PMTUD (Path MTU Discovery)**: el emisor reduce el tamaño y reintenta.

> ⚠️ **Un firewall mal configurado que bloquea TODO el ICMP rompe PMTUD**: los "packet too big" no llegan y las conexiones se congelan misteriosamente (el clásico "el SSH conecta pero no puedo escribir").

### Segmentación vs fragmentación (diferencia clave)

| | Segmentación (capa 4, TCP) | Fragmentación (capa 3, IP) |
|--|---------------------------|----------------------------|
| Quién | El emisor (TCP) | Los routers en el camino (IP) |
| Se hace | **Antes de enviar**, cortando el stream en segmentos ~MSS | **En ruta**, si el paquete no cabe |
| Numeración | **Sí** (números de secuencia → reordenar y retransmitir) | **No numera lógicamente**; usa ID+offset para reensamblar |
| Fiabilidad | Retransmite lo perdido | El reensamblado espera todos los fragmentos |

> 📌 *De tu apunte:* "La segmentación numera, la fragmentación no." Exactamente: si se pierde un segmento TCP, se retransmite solo ese; si se pierde un fragmento IP, **el paquete entero se reenvía** (por eso fragmentar es caro y se evita).

### 🎯 Para el hacker ético

- **Terrorismo de fragmentación:** envíos de fragmentos solapados o incompletos para evadir IDS o tirar pilas IP antiguas (teardrop). Los IDs y offsets manipulables también dan juego en fingerprinting.
- **Evadir filtros:** algunos firewalls viejos solo inspeccionan el primer fragmento → enviar el payload "interesante" en fragmentos posteriores los esquivaba (los IDS modernos reensamblan).
- **Nmap:** `--mtu 24` fragmenta la sonda en múltiplos de 8; y `-f` fragmenta paquetes en el escaneo — útil contra firewalls torpes.
- **PMTUD como oráculo:** ping con DF y tamaños decrecientes te mapea la MTU de los enlaces intermedios (y, con ello, parte de la topología).

---

## Segmentación y multiplexación (repaso conceptual)

> 📌 *De tu apunte:* "Si mando entera una trama, el cable se dedicaría únicamente a esa trama gigante".

- **Segmentación:** dividir los datos en trozos pequeños (~1480 bytes de payload) antes de enviarlos. Así el medio se **comparte** y un error no obliga a reenviar todo.
- **Multiplexación:** que **todas esas comunicaciones distintas viajen mezcladas por el mismo cable** simultáneamente, distinguiéndose por sus cabeceras (MAC destino, IP destino, puerto destino).

**Ejemplo con fibra:** una misma fibra transporta muchas comunicaciones a la vez mediante multiplexación por **longitudes de onda** (DWDM) — cada canal en un "color" de luz distinto. En cable de cobre, la multiplexación es "temporal" (TDM): cada trama de cada conversación ocupa el medio una fracción de segundo.

> 📌 *Definiciones cortas para el examen:*
> - **Segmentación:** dividir un medio físico o una red en varios canales/segmentos para transportar diferentes comunicaciones.
> - **Multiplexación:** permitir que varias señales viajen simultáneamente por el mismo medio, compartiendo su capacidad.

---

## Comandos útiles

```bash
# Ver la MTU de tus interfaces
ip link show                      # Linux
netsh interface ipv4 show subinterfaces   # Windows

# Probar el tamaño máximo sin fragmentar
ping -M do -s 1472 ejemplo.com    # Linux
ping -f -l 1472 ejemplo.com       # Windows

# Trazar dónde se corta (qué enlace tiene MTU menor)
tracepath ejemplo.com             # Linux, muestra MTU por salto

# Estadísticas de fragmentación del kernel
nstat -az | grep -i frag
netstat -s | grep -i frag
```

---

## Resumen rápido

- Encapsulación: datos → segmento → paquete → trama → bits; cada capa añade cabecera.
- **MTU = tamaño máximo de paquete IP sin fragmentar** (Ethernet 1500, PPPoE 1492, VPN ~1420-1450).
- **DF flag**: no fragmentar → si no cabe, descarte + ICMP "fragmentation needed" (PMTUD).
- **Segmentación (TCP) numera y retransmite; fragmentación (IP) usa ID+offset y es cara.**
- La VPN que "conecta pero va mal" = problema de MTU: ajusta MTU/MSS.

**Siguiente capítulo →** [07 · Dominios de Colisión y Switching](07-dominios-colision-y-switching.md)
