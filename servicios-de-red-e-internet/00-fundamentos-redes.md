# 🧱 00 · Fundamentos de Redes

> Todo lo que ocurre en Internet se reduce a esto: **máquinas conectadas intercambiando datos según reglas muy concretas**. Si entiendes las reglas, entiendes dónde se rompen y, por tanto, dónde se puede atacar.

---

## ¿Qué es una red de computadoras?

Una **red** es un conjunto de dispositivos (ordenadores, móviles, servidores, cámaras, routers...) conectados entre sí para **compartir recursos e información**.

Tipos según su alcance:

| Tipo | Significado | Ejemplo |
|------|-------------|---------|
| **PAN** | *Personal Area Network* | Tu móvil + auriculares Bluetooth |
| **LAN** | *Local Area Network* | La red de tu casa u oficina |
| **WLAN** | LAN inalámbrica | Tu Wi-Fi de casa |
| **MAN** | *Metropolitan Area Network* | Red de un campus universitario |
| **WAN** | *Wide Area Network* | Internet, o la red que une dos sedes de una empresa |

Internet no es "una red": es **la red de redes** — millones de redes LAN/WAN conectadas hablando el mismo idioma (IP).

---

## El modelo OSI y TCP/IP: las capas

Para no volverse locos, los ingenieros dividieron la comunicación en **capas**, cada una con una responsabilidad. Es el concepto más importante de toda la sección.

### Modelo OSI (7 capas) — el teórico

| # | Capa | Qué hace | Ejemplos |
|---|------|----------|----------|
| 7 | Aplicación | Datos que el usuario usa | HTTP, DNS, SMTP, SSH |
| 6 | Presentación | Formato, cifrado | TLS, JPEG, ASCII |
| 5 | Sesión | Mantener conversaciones | NetBIOS, RPC |
| 4 | Transporte | Puertos, fiabilidad | TCP, UDP |
| 3 | Red | Direccionamiento lógico | IP, ICMP |
| 2 | Enlace de datos | MAC, tramas | Ethernet, ARP, Wi-Fi |
| 1 | Física | Bits por el cable/aire | Cables, fibras, señales |

### Modelo TCP/IP (4 capas) — el real, el que se usa

| Capa | Equivale a (OSI) | Protocolos |
|------|------------------|------------|
| **Aplicación** | 7, 6, 5 | HTTP, DNS, SMTP, SSH, FTP |
| **Transporte** | 4 | TCP, UDP |
| **Internet** | 3 | IP, ICMP, ARP (prácticamente) |
| **Acceso a red** | 2, 1 | Ethernet, Wi-Fi |

> 💡 **Truco para recordar OSI** (de abajo arriba): *"Física, Enlace, Red, Transporte, Sesión, Presentación, Aplicación"* — **"FERNITA SPA"** o en inglés: *"Please Do Not Throw Sausage Pizza Away"*.

### 🎯 Para el hacker ético

- Cada capa tiene **ataques propios**: ARP Spoofing (capa 2), IP Spoofing (3), SYN Flood (4), DNS Spoofing (7).
- Las herramientas se organizan por capas: `tcpdump` ve capas 2-4, Burp Suite trabaja en la 7, Nmap escanea de la 2 a la 7.
- Cuando algo "no funciona", **piensa en capas**: ¿es el cable (1)? ¿la MAC (2)? ¿la IP (3)? ¿el puerto (4)? ¿el servicio (7)?

---

## Sockets: la identidad de una conexión

Una **conexión de Internet se produce de socket a socket**.

Un **socket** es la conjunción de:

```
IP + Puerto  →  192.168.1.50:443
```

- La **IP** identifica la máquina en la red.
- El **puerto** identifica la aplicación dentro de esa máquina.

Ejemplo real: cuando abres dos pestañas del navegador y un juego online a la vez, cada navegador **tiene un puerto de origen diferente**, por eso el router sabe a qué aplicación devolver cada respuesta.

Una conexión completa queda así:

```
PC A  (IP_A:puerto_A)  ⟷  PC B  (IP_B:puerto_B)
```

> 🔑 **Idea clave para NAT:** si tu equipo está detrás de un router, **la IP que sale a Internet es la del router** (la pública). Es el router el que "navega" y el que asigna y traduce los sockets. Esto se entiende a fondo en el capítulo [04 · NAT](04-nat-y-cgnat.md).

---

## Puertos y puertos bien conocidos

Un puerto es un número de **0 a 65535**. Hay tres rangos:

| Rango | Nombre | Uso |
|-------|--------|-----|
| 0–1023 | **Well-known** | Servicios del sistema, reservados |
| 1024–49151 | **Registered** | Aplicaciones registradas |
| 49152–65535 | **Dynamic/Ephemeral** | Puertos aleatorios de cliente |

### Los puertos que DEBES memorizar

| Puerto | Servicio | Notas para hacking |
|--------|----------|--------------------|
| **21** | FTP | A menudo anónimo o con backdoors (vsftpd 2.3.4 😉) |
| **22** | SSH | Fuerza bruta, credenciales débiles |
| **23** | Telnet | Sin cifrar — nunca debería estar abierto |
| **25** | SMTP | Relay abierto = spam, enumeración de usuarios |
| **53** | DNS | Transferencia de zona, envenenamiento |
| **80** | HTTP | Web sin cifrar |
| **110** | POP3 | Correo sin cifrar |
| **143** | IMAP | Correo sin cifrar |
| **443** | HTTPS | Web cifrada |
| **445** | SMB | EternalBlue, enumeración de compartidos |
| **1433** | MSSQL | Bases de datos |
| **3306** | MySQL/MariaDB | Bases de datos |
| **3389** | RDP | BlueKeep, fuerza bruta |
| **5432** | PostgreSQL | Bases de datos |
| **5900** | VNC | Acceso remoto a menudo sin contraseña fuerte |
| **8080** | HTTP alternativo | Paneles de administración, Tomcat, Jenkins |

> 🎯 Estos puertos son **el mapa del tesoro de un pentester**. En los CTFs, `nmap -sV -sC` contra estos puertos es el primer paso de casi cualquier máquina.

---

## Dispositivos de red: quién es quién

| Dispositivo | Capa | Qué hace | Aislamiento |
|-------------|------|----------|-------------|
| **Hub** | 1 (física) | Repite todo por todos los puertos | Nada — todos en el mismo dominio de colisión, ¡todos ven todo! |
| **Switch** | 2 (MAC) | Aprende MACs y envía tramas solo al puerto destino | Separa **dominios de colisión** por puerto |
| **Router** | 3 (IP) | Enruta paquetes entre redes distintas | Separa **dominios de broadcast** |
| **Firewall** | 3-7 | Filtra tráfico según reglas | — |
| **AP (Punto de acceso)** | 2 | Da acceso Wi-Fi | — |
| **Proxy** | 7 | Intermediario de peticiones de aplicación | — |

> 🔑 Un **hub** es un auténtico chivato: cualquier equipo conectado a él ve el tráfico de todos los demás (útil en labs viejos para sniffing). Un **switch** moderno no: para oler su tráfico necesitas técnicas como ARP Spoofing (capítulo [11](11-aplicacion-al-hacking.md)).

---

## TCP vs UDP: fiabilidad vs velocidad

| | **TCP** | **UDP** |
|--|---------|---------|
| Conexión | Orientado a conexión (3-way handshake: SYN → SYN/ACK → ACK) | Sin conexión |
| Fiabilidad | Garantiza entrega y orden | "Best effort", sin garantías |
| Velocidad | Más lento (más sobrecarga) | Más rápido |
| Uso | Web, SSH, correo, transferencia de archivos | DNS (normalmente), VoIP, streaming, videojuegos |

> 🎯 Escaneos TCP (`-sS`) son discretos con SYN scan; los UDP (`-sU`) son lentos y a menudo olvidados por los administradores → **puertos UDP olvidados = puertas traseras frecuentes** (tftp 69, snmp 161, ntp 123...).

---

## Cliente, servidor y la petición típica

Cuando escribes `https://ejemplo.com` en el navegador ocurre esto, en orden:

1. **DNS:** el sistema pregunta "¿qué IP tiene ejemplo.com?" (capítulo [01](01-dns.md)).
2. **TCP:** se abre un socket hacia la IP en el puerto 443 (three-way handshake).
3. **TLS:** se negocia el cifrado (capa 6).
4. **HTTP:** el navegador envía `GET / HTTP/1.1` (capa 7).
5. El servidor responde con el HTML, y el navegador lo pinta.

Cada paso es una superficie de ataque: envenenar el DNS, interceptar el handshake, degradar TLS, manipular la petición HTTP...

---

## Resumen rápido

- Red = dispositivos conectados para compartir datos. Internet = red de redes.
- Todo se organiza en **capas** (modelo TCP/IP de 4 u OSI de 7).
- Una conexión va de **socket a socket** (IP:puerto → IP:puerto).
- Los puertos 0–1023 son los **well-known** y hay que saberlos de memoria.
- Hub/switch/router separan dominios de colisión y broadcast (capítulo [07](07-dominios-colision-y-switching.md)).

**Siguiente capítulo →** [01 · DNS: El Teléfono de Internet](01-dns.md)
