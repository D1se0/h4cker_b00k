---
icon: hose-reel
---

# NAT, CGNAT y Hole Punching

> ¿Por qué tu PC tiene IP `192.168.1.x` pero Google te ve con otra? ¿Por qué no puedes abrir puertos aunque lo configures todo bien? La respuesta son las siglas **NAT**, y entender sus tipos (Full Cone vs Simétrico) es lo que separa a quien "usa Internet" de quien entiende cómo funcionan las conexiones P2P, VoIP, juegos y VPN.

***

## ¿Qué es el NAT?

**NAT (Network Address Translation)** es el proceso de **reescribir las direcciones IP (y puertos) de los paquetes** que cruzan un dispositivo, normalmente un router.

Funciona en la **capa 4 (Transporte)**: no basta con entender IPs (capa 3), debe entender también **puertos**. Por eso hablamos de **NAPT/PAT** (_Network/Port Address Translation_) como el nombre técnico del NAT moderno.

### ¿Para qué existe?

1. **Ahorrar IPv4** (hay solo \~4.300 millones): millones de dispositivos comparten pocas IPs públicas.
2. **Ocultar la red interna:** desde fuera solo se ve el router.
3. **Control:** el router decide qué conexiones entran y cuáles no.

### La tabla NAT: el corazón del invento

El router mantiene una **tabla de traducciones** que asocia cada conexión interna con su traducción pública:

```
┌──────────────────────────────────────────────────────────┐
│ IP interna:puerto   →   IP pública:puerto   →  Destino   │
│ 192.168.1.50:51234 →   83.45.120.7:51234  →  1.2.3.4:443│
│ 192.168.1.51:49152 →   83.45.120.7:49152  →  1.2.3.4:80 │
└──────────────────────────────────────────────────────────┘
```

Cuando el paquete de respuesta vuelve del destino, el router consulta la tabla y lo devuelve al host interno correcto. Por eso **cada navegador usa un puerto de origen diferente**: es el router quien asigna y distingue los sockets.

> 💡 **Límite práctico:** los routers domésticos tienen **tablas NAT muy limitadas** (cientos o pocos miles de entradas). Con torrents, muchos dispositivos o P2P agresivo la tabla se llena → páginas que no cargan, conexiones que se cortan. Sí, hay un límite de conexiones simultáneas por equipo detrás de un NAT.

***

## SNAT y DNAT: cambiar origen o destino

| Tipo                       | Qué modifica                           | Caso típico                                                                         |
| -------------------------- | -------------------------------------- | ----------------------------------------------------------------------------------- |
| **SNAT** (Source NAT)      | La IP/**puerto de origen** del paquete | Que una red privada **salga a Internet** usando la IP pública del router            |
| **DNAT** (Destination NAT) | La IP/**puerto de destino**            | Redirigir tráfico que llega de Internet a un servidor interno → **port forwarding** |

```
SNAT (salida):  192.168.1.50:51234  →  [NAT]  →  83.45.120.7:51234  →  Internet
DNAT (entrada): Internet  →  83.45.120.7:8080  →  [NAT]  →  192.168.1.100:80
```

> 💡 Truco: **S**NAT = cambia el **S**ource al salir. **D**NAT = cambia el **D**estination al entrar. El router doméstico hace SNAT automático para toda la LAN; el DNAT lo configuras tú al abrir puertos.

### 🎯 Para el hacker ético

* En un CTF con `iptables`, el patrón `iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 10.0.0.5:80` es el port forwarding manual.
* Si ganas acceso a un router (configuración por defecto, CVE...), las reglas DNAT existentes te dibujan el **mapa de servicios internos expuestos**.

***

## Los 4 tipos de NAT (STUN/RFC 3489)

El comportamiento del NAT cuando abre un socket hacia fuera determina si te pueden llamar desde fuera. De más permisivo a más restrictivo:

| Tipo                          | Comportamiento                                                                                                                                     | ¿Te puede llamar cualquiera?                |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| **Full Cone** (cono completo) | Una vez creado un mapeo interno→público, **cualquier equipo externo** puede enviar tráfico a ese puerto público y el router lo redirige al interno | ✅ Sí, si conoce IP:puerto público           |
| **Restricted Cone**           | Solo acepta tráfico externo desde IPs que ya has contactado antes                                                                                  | ⚠️ Solo IPs conocidas                       |
| **Port-Restricted Cone**      | Igual, pero además exige el mismo puerto externo                                                                                                   | ⚠️ Solo IP:puerto conocidos                 |
| **Simétrico**                 | Cada destino distinto recibe **un mapeo nuevo y distinto**                                                                                         | ❌ No, salvo que ambos inicien casi a la vez |

> 🔑 **Idea central:** en el **Full Cone NAT**, tras la primera comunicación, el mapeo queda abierto para cualquiera → es el más "hackeable" y el ideal para P2P. El **simétrico** es el pesadilla: cada conexión es un socket distinto y nadie desde fuera puede adivinarlo.

**¿Cómo saber qué NAT tienes?** Con **STUN** (`stunclient stun.l.google.com 19302` o herramientas como `pystun3`): un servidor STUN te dice qué IP:puerto público te asigna y con qué tipo de NAT estás.

***

## Hole Punching: conectando dos NAT entre sí

**Hole punching (perforación de NAT)** es una técnica que permite **conectar directamente dos dispositivos que están detrás de routers con NAT o firewall**, aunque ninguno tenga puertos abiertos públicamente.

### Cómo funciona (UDP hole punching, el caso fácil)

1. **Servidor intermedio** (que sí es alcanzable): ambos peers le dicen "aquí estoy" → descubren sus **IP:puerto públicos** (esto es STUN).
2. Cada peer envía un paquete UDP **al IP:puerto público del otro**, casi a la vez.
3. Esos paquetes salientes **abren agujeros** en ambos NAT (crean el mapeo en la tabla).
4. Como cada NAT ya "conoce" al otro (full cone o restricted), los paquetes empiezan a pasar.
5. Resultado: en lugar de `PC A → NAT A → Internet → NAT B → PC B`, el tráfico va **directo**: `PC A → Internet → PC B`.

```
Antes:   PC A ── NAT A ── INTERNET ── NAT B ── PC B   (vía servidor relay)
Después: PC A ──────────── INTERNET ──────────── PC B   (conexión directa)
```

### ¿Dónde se usa?

* **P2P:** BitTorrent, WebRTC (videollamadas del navegador), Syncthing.
* **VoIP:** Skype, WhatsApp calls, Teams.
* **Videojuegos:** partidas online entre jugadores.
* **VPNs mesh:** Tailscale, ZeroTier, WireGuard con NAT traversal.

Cuando el hole punching **no es posible** (NAT simétrico en ambos lados), se usa un **relay/TURN**: un servidor intermedio reenvía todo el tráfico (menos eficiente, pero funciona siempre).

### 🎯 Para el hacker ético

* **WebRTC** expone IPs locales y públicas incluso detrás de VPN (fuga clásica de anonimato: `canyouseeme`, test de WebRTC en el navegador).
* Herramientas que usan NAT traversal y son habituales en post-explotación: **Tailscale/ZeroTier** para C2 discreto, `chisel`, `ngrok`, `cloudflared` (ya tienes capítulos de [Port Forwarding](../herramientas-tecnicas/post-explotacion/port-forwarding.md) y [Pivoting](../ciberseguridad-avanzada-hacking-etico/contenido.../hacking-etico-y-post-explotacion-avanzada/pivoting.md)).
* Entender NAT es imprescindible para montar **infraestructura de C2** con callbacks que atraviesen NAT.

***

## CGNAT: tu operador también hace NAT

**CGNAT (Carrier-Grade NAT)** es cuando **el operador comparte una misma IP pública entre muchos clientes**. Tu router ya hace un NAT doméstico... y encima el del operador hace otro encima. Doble NAT.

### Cómo saber si estás en CGNAT

1. Mira tu IP pública: `curl ifconfig.me`.
2. Entra al router y mira la IP WAN que te asignó el operador.
3. **Si la IP WAN es `100.64.x.x` – `100.127.x.x` → estás tras CGNAT** (rango reservado `100.64.0.0/10`, RFC 6598).
4. También si la IP pública que ves difiere de la WAN y los puertos no se abren nunca.

### Consecuencias

* ❌ **No tienes IP pública propia** → no puedes abrir puertos directamente hacia tu red.
* ❌ No puedes alojar servidores web, cámaras, Minecraft, VPN entrante...
* ⚠️ Riesgo añadido: compartes IP con otros clientes → si alguien hace spam, la IP acaba en listas negras y te afecta.
* ✅ A tu favor: también "esconde" tu red una capa más.

### Qué hacer (y la razón de "revisar para conseguir la línea más barata")

* Pide al operador **IP pública dinámica** (gratuito en casi todos: Movistar, Vodafone, Orange...) — a menudo los planes baratos te la dan sin CGNAT; los "baratos con móvil incluido" suelen meter CGNAT.
* Alternativas sin cambiar de tarifa: **IPv6** (sin NAT), túneles tipo Cloudflare Tunnel / ngrok / Tailscale, o un VPS con WireGuard al que ambos lados conecten hacia fuera.

> 🎯 En auditorías de redes pequeñas, detectar CGNAT cambia todo el informe: "no pueden recibir conexiones" no es un fallo de config del cliente sino del plan contratado.

***

## VPNs y NAT: el detalle que rompe todo

Los túneles VPN encapsulan paquetes ya formados: el tamaño del paquete interior **sumado** a la sobrecarga del túnel puede superar la MTU del camino (capítulo [06](06-tramas-mtu-fragmentacion.md)).

* Síntomas: la VPN conecta pero "algunas webs no cargan", SSH se queda colgado tras el banner, downloads grandes fallan.
* Solución: fijar MTU/MSS en la interfaz VPN (`mtu 1420` en WireGuard, `mssfix 1400` en OpenVPN) o dejar que PMTUD funcione (no filtrar ICMP "fragmentation needed").

***

## Resumen rápido

* NAT reescribe IP:puerto (capa 4) y mantiene una **tabla de traducciones** limitada.
* **SNAT** cambia origen (salida a Internet); **DNAT** cambia destino (port forwarding).
* Tipos: **Full Cone** (abierto a cualquiera) → Restricted → Port-Restricted → **Simétrico** (cada destino, mapeo nuevo).
* **Hole punching**: un servidor intermedio ayuda a dos NAT a abrirse mutuamente → conexión directa P2P (WebRTC, BitTorrent, Tailscale).
* **CGNAT** (`100.64.0.0/10`): el operador comparte su IP pública entre clientes → sin puertos entrantes; se soluciona pidiendo IP pública o con túneles/IPv6.

**Siguiente capítulo →** [05 · Cableado Físico y Práctica](05-cableado-fisico.md)
