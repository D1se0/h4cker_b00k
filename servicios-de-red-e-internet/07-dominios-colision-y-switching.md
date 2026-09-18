---
icon: tower-cell
---

# Dominios de Colisión y Switching

> ¿Por qué un switch "separa" y un hub "mezcla"? ¿Cómo sabe la red quién transmite y cuándo? Aquí están los conceptos que explican el funcionamiento físico de Ethernet y Wi-Fi — y que te permiten entender por qué puedes (o no) **oler tráfico ajeno** en una red.

***

## Dominio de colisión y dominio de difusión

Dos conceptos que se confunden siempre:

| Concepto                            | Definición                                                                                                                                                    | Lo separa                   |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------- |
| **Dominio de colisión**             | Zona de la red donde varios dispositivos pueden transmitir al mismo tiempo y **provocar una colisión** (dos señales eléctricas solapándose = datos corruptos) | El **switch** (por puerto)  |
| **Dominio de difusión (broadcast)** | Zona donde un paquete broadcast llega a todos (una MAC `FF:FF:FF:FF:FF:FF` inunda la zona)                                                                    | El **router** (y las VLANs) |

```
HUB:   [PC1][PC2][PC3] ── todo en UN dominio de colisión
SWITCH: cada puerto = un dominio de colisión propio
ROUTER: cada interfaz = un dominio de broadcast propio
```

> 🎯 **Para el hacker ético:** el dominio de broadcast es tu zona de visibilidad. Todo lo que compartes dominio de broadcast (misma VLAN/red sin router de por medio) es donde ARP Spoofing, rogue DHCP y descubrimiento (mDNS, NetBIOS) funcionan de forma natural. Los routers y las VLANs son los "muros" que hay que saltar con otras técnicas (pivoting).

***

## CSMA: escuchar antes de hablar

Para gestionar las colisiones existe **CSMA (Carrier Sense Multiple Access)**: **escuchar el medio antes de transmitir** ("si está ocupado, espera").

### CSMA/CD — Ethernet cableada (Collision **D**etection)

1. Escuchas el cable: ¿está libre?
2. Si está libre, transmites mientras sigues escuchando.
3. Si detectas que otra señal pisó la tuya (**colisión detectada**), paras, envías una señal de jamming y **esperas un tiempo aleatorio** (backoff exponencial) antes de reintentar.

> 💡 En **ethernet conmutada moderna (full-duplex)**, cada puerto es un dominio de colisión con solo dos hablantes (tú y el switch) y se transmite y recibe a la vez por pares distintos → **ya no hay colisiones que detectar**. CSMA/CD es historia en el cable, pero sigue en el temario y explica el legado (half-duplex, hubs).

### CSMA/CA — Wi-Fi (Collision **A**voidance)

En el aire no puedes escuchar mientras transmites (tu propia señal ahoga a la otra), así que en vez de detectar colisiones se intentan **evitar**:

1. Escuchas el canal: ¿está libre durante DIFS?
2. Esperas un tiempo aleatorio adicional (backoff) **antes** de transmitir.
3. Opcional (modo RTS/CTS): pedir permiso ("Request To Send") y esperar el "Clear To Send" del AP para reservar el canal.
4. El receptor confirma cada trama con un **ACK**; sin ACK = colisión asumida → reintento.

> 🔑 Diferencia de examen: **CD detecta** colisiones (ethernet half-duplex), **CA las evita** (Wi-Fi). El switch separa dominios de colisión y el router separa dominios de broadcast.

***

## Hub vs Switch vs Router (a fondo)

|                      | **Hub**                               | **Switch**                            | **Router**            |
| -------------------- | ------------------------------------- | ------------------------------------- | --------------------- |
| Capa                 | 1                                     | 2 (MAC)                               | 3 (IP)                |
| Inteligencia         | Ninguna: repite por todos los puertos | Aprende MACs en una tabla CAM         | Lee IPs y elige rutas |
| Dominio de colisión  | Único (todos peleándose)              | Uno por puerto                        | Uno por interfaz      |
| Dominio de broadcast | Único                                 | Único (sin VLANs)                     | Separa                |
| ¿Ves tráfico ajeno?  | **Sí, todo** (modo promiscuo y listo) | No, salvo ARP spoofing / mirror ports | No                    |
| Uso hoy              | Ninguno (obsoleto)                    | Todo                                  | Entre redes           |

### Cómo "aprende" un switch

1. Recibe una trama del puerto 1 con MAC origen `AA:AA:...` → anota en la tabla CAM: `AA:AA → puerto 1`.
2. Si la MAC destino está en la tabla → envía **solo** por ese puerto (_forwarding_).
3. Si no está → envía por todos los puertos excepto el de origen (_flooding_).
4. Las entradas envejecen ( aging time \~300 s).

> 🎯 Un **switch malicioso o saturado** de MACs inexistentes (MAC flooding) llena la tabla CAM y empieza a hacer flooding permanente → vuelve a ser "hub" y se puede oler todo. Contraesto en switches serios: _port security_ limitando MACs por puerto.

***

## Rutas y métricas: cómo decide un equipo por dónde enviar

Tu PC también enruta: para cada destino consulta su **tabla de rutas**.

```
Destination     Gateway         Genmask         Metric Iface
0.0.0.0         192.168.1.1     0.0.0.0         100    eth0    ← ruta por defecto
192.168.1.0     0.0.0.0         255.255.255.0   100    eth0    ← mi red, directamente conectada
10.8.0.0        10.8.0.1        255.255.255.0   0      tun0    ← red de la VPN
```

### Distancia administrativa y métrica

Un equipo **aprende rutas por distintos orígenes**, cada uno con una **distancia administrativa** (prioridad de la fuente) y, dentro de la misma fuente, por **métrica** (coste del camino):

| Origen de la ruta  | Distancia admin. típica (Cisco) |
| ------------------ | ------------------------------- |
| Interfaz conectada | 0                               |
| Estática           | 1                               |
| EIGRP (interno)    | 90                              |
| OSPF               | 110                             |
| RIP                | 120                             |

* Si dos rutas al mismo destino vienen de **fuentes distintas**, gana la de **menor distancia administrativa**.
* Si vienen de la **misma fuente**, gana la de **menor métrica** (saltos, ancho de banda, retraso... según el protocolo).

> 💡 Esto explica por qué al conectar una VPN tu tráfico va por `tun0` aunque la ruta "por defecto" exista: la ruta VPN es más específica o tiene mejor métrica/distancia.

### Cómo contar redes en un plano (truco del "agua")

> 📌 _De tu apunte:_ "Para contar redes se identifican elementos de capa 3 o superior. Imaginamos que metemos agua por todas las conexiones hasta que encontramos un elemento que corta el flujo."

Cada **elemento de capa 3+ (router, firewall, PC con dos interfaces...) que corta el "flujo"** delimita una red distinta. Todo lo que el agua alcanza sin pasar por un router es **una única red/broadcast domain**. Los switches y hubs no cortan nada: son "tubería".

***

## Ping, traceroute y lo que te cuentan

```bash
ping -c 4 ejemplo.com            # ¿Responde? ¿latencia? ¿TTL?
traceroute ejemplo.com           # routers intermedios (TTL decreciente)
traceroute -I ejemplo.com        # con ICMP (algunos firewalls lo dejan pasar más)
mtr ejemplo.com                  # traceroute en vivo con estadísticas
```

> 💡 El **TTL** del ping te dice cuántos saltos hay (empieza en 64 en Linux, 128 en Windows: si un ping a una máquina "cercana" responde con TTL 63, había un router de por medio). El TTL también se usa para **fingerprinting de S.O.** — ya lo usas en los CTFs para distinguir Linux de Windows antes del escaneo.

***

## Resumen rápido

* **Dominio de colisión:** zona donde pueden chocar transmisiones → lo separa el **switch por puerto**.
* **Dominio de broadcast:** zona donde llega un broadcast → lo separa el **router** (y las VLANs).
* **CSMA/CD** (ethernet half-duplex) detecta colisiones y reintenta; **CSMA/CA** (Wi-Fi) las evita con backoff y ACKs.
* Hub = un solo dominio de colisión (se oye todo); switch = tabla CAM; router = separa redes.
* Las rutas se eligen por **distancia administrativa** (fuente) y **métrica** (coste).
* Truco: para contar redes, busca los equipos **de capa 3** que cortan el "flujo de agua".

**Siguiente capítulo →** [08 · VLANs y VTP](08-vlans-y-vtp.md)
