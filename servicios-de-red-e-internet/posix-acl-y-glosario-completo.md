---
icon: layer-plus
---

# POSIX, ACL y Glosario Completo

> Dos conceptos que salieron en clase y que conviene dejar claros (POSIX y ACL), y después **el glosario completo de todos los términos de la sección** — tu chuleta de repaso rápido antes de un examen o un CTF.

***

## POSIX (Portable Operating System Interface)

**POSIX** es un **conjunto de estándares (IEEE 1003) que define cómo deben funcionar los sistemas operativos tipo Unix para que sean compatibles entre sí**.

* Define APIs de sistema: gestión de procesos (`fork`, `exec`), archivos y permisos, señales, hilos (pthreads), la shell básica, expresiones regulares básicas...
* **Linux sigue muchos estándares POSIX, aunque Linux no es completamente POSIX** (no está certificado; lo están macOS, AIX, etc.). Windows tiene modo parcial vía WSL/Cygwin.
* ¿Por qué importa? Gracias a esta base común, un script de bash, un programa en C con `fork()` o los permisos `chmod 755` funcionan igual en cualquier Linux/BSD/macOS.

> 🎯 Para el hacker: tus scripts y binarios compilados en Kali (POSIX-ish) corren igual en el Debian del servidor de la víctima. Y APIs POSIX (`fork`, `socket`, `setuid`) son la base de exploits y malware portables.

***

## ACL (Access Control List)

Una **ACL (Access Control List)** es una **lista de reglas que define qué usuarios o dispositivos pueden acceder a un recurso y qué acciones pueden realizar**.

*   **En sistemas de archivos (POSIX ACLs):** extienden los permisos clásicos `rwx` de dueño/grupo/otros para dar permisos a usuarios o grupos concretos:

    ```bash
    getfacl informe.txt
    setfacl -m u:pepe:rw informe.txt     # pepe puede leer y escribir sin cambiar el grupo
    ```
*   **En redes (network ACLs):** permitir o **bloquear tráfico según IP, protocolo y puerto**. Se aplican en routers, firewalls y switches:

    ```cisco
    access-list 100 permit tcp any host 10.0.0.5 eq 443
    access-list 100 deny   ip any any
    interface GigabitEthernet0/1
     ip access-group 100 in
    ```
* Existen también ACLs en AWS S3, NTFS de Windows, proxies... el concepto es siempre el mismo: **una lista ordenada de reglas permite/denegar** que se evalúa de arriba abajo (primera que aplica gana).

> 🎯 Para el hacker: las ACLs de red son las "paredes" que intentas saltar en el pivoting. Y al auditar, buscar ACLs con reglas `permit ip any any` olvidadas o heredadas es pan de cada día (over-privilege).

***

## 📖 Glosario completo de la sección

Orden alfabético. Cada entrada: definición corta + capítulo donde se explica a fondo.

### A

* **ACL (Access Control List)** — Lista de reglas que define quién puede acceder a un recurso y qué puede hacer; en redes, filtra por IP/protocolo/puerto. → [10](posix-acl-y-glosario-completo.md)
* **APIPA (169.254.0.0/16)** — Auto-IP que se asigna un equipo cuando no consigue DHCP. Señal de red rota. → [03](direccionamiento-ip-y-subnetting.md)
* **ARP** — Protocolo de capa 2 que resuelve IP→MAC dentro de un segmento. Base del ARP Spoofing. → [00](fundamentos-como-funciona-una-red.md)
* **Auto-MDIX** — Capacidad de tarjetas/switches modernos de detectar cable directo o cruzado y ajustarse automáticamente. → [05](cableado-fisico-y-practica.md)

### B

* **Broadcast (255.255.255.255)** — Envío a "todos" del segmento; limitado por routers. → [03](direccionamiento-ip-y-subnetting.md), [07](dominios-de-colision-y-switching.md)
* **Bucle de tierra** — Corriente parásita por la pantalla de un cable apantallado conectado a tierra en ambos extremos con potenciales distintos; se evita apantallando solo un extremo. → [05](cableado-fisico-y-practica.md)

### C

* **CCA (Copper Clad Aluminum)** — Cable de aluminio bañado en cobre: más impedancia, frágil, no apto para PoE serio. Evitar. → [05](cableado-fisico-y-practica.md)
* **CGNAT (Carrier-Grade NAT, 100.64.0.0/10)** — El operador comparte una IP pública entre muchos clientes; sin IP pública propia no puedes abrir puertos. → [04](nat-cgnat-y-hole-punching.md)
* **CIDR (/n)** — Notación que indica cuántos bits de la IP son de red. Base del subnetting. → [03](direccionamiento-ip-y-subnetting.md)
* **CSMA/CD vs CSMA/CA** — Ethernet half-duplex **detecta** colisiones; Wi-Fi las **evita**. → [07](dominios-de-colision-y-switching.md)

### D

* **DHCP / DORA** — Protocolo que asigna IP/máscara/gateway/DNS; baile Discover-Offer-Request-Acknowledge. Atacable con rogue DHCP. → [03](direccionamiento-ip-y-subnetting.md)
* **dig / nslookup** — Herramientas de consultas DNS: dig profesional (trace, axfr), nslookup rápido. → [01](dns-el-telefono-de-internet.md)
* **DKIM** — Firma criptográfica del correo saliente, verificada vía DNS. → [02](el-servicio-de-correo-electronico.md)
* **DMARC** — Política que indica qué hacer si SPF/DKIM fallan (none/quarantine/reject). → [02](el-servicio-de-correo-electronico.md)
* **DNAT** — NAT que cambia la **IP/puerto de destino**; base del port forwarding. → [04](nat-cgnat-y-hole-punching.md)
* **DNS** — Sistema que traduce nombres de dominio a IPs (y viceversa). → [01](dns-el-telefono-de-internet.md)
* **Dominio de colisión / difusión** — Zona donde pueden chocar transmisiones (separa: switch) / zona donde llega un broadcast (separa: router). → [07](dominios-de-colision-y-switching.md)
* **DoT / DoH** — DNS cifrado por TLS (853) o dentro de HTTPS (443). → [01](dns-el-telefono-de-internet.md)
* **DF flag (Don't Fragment)** — Bandera IP: el paquete no puede fragmentarse; si no cabe se descarta y vuelve ICMP "fragmentation needed" (PMTUD). → [06](tramas-mtu-y-fragmentacion.md)

### F

* **Full Cone NAT** — NAT cuyo mapeo queda abierto para cualquier origen externo; el ideal para P2P. → [04](nat-cgnat-y-hole-punching.md)
* **Fragmentación** — División en ruta de un paquete IP demasiado grande para un enlace; se reensambla en el destino (ID + offset + MF). → [06](tramas-mtu-y-fragmentacion.md)

### H

* **Hole punching** — Técnica para que dos equipos tras NAT se conecten directamente con ayuda de un servidor intermedio; usado en P2P, VoIP, juegos, VPNs mesh. → [04](nat-cgnat-y-hole-punching.md)
* **Hub** — Repetidor tonto de capa 1: todos en un dominio de colisión, todo visible. Obsoleto. → [00](fundamentos-como-funciona-una-red.md), [07](dominios-de-colision-y-switching.md)

### I

* **IMAP / POP3 / SMTP** — Lectura sincronizada (993) / descarga (995) / envío (25/587/465) de correo. → [02](el-servicio-de-correo-electronico.md)
* **iperf3 / nPerf** — Medidores de rendimiento: iperf3 interno (servidor+cliente), nPerf hacia Internet. → [09](herramientas-de-diagnostico-de-red.md)
* **IPv4 / IPv6** — 32 bits (4 octetos) / 128 bits (grupos hex con `::`). → [03](direccionamiento-ip-y-subnetting.md)

### J-L

* **Jumbo frames** — Tramas de hasta \~9000 bytes para storage/datacenter; exige MTU consistente en todo el camino. → [06](tramas-mtu-y-fragmentacion.md)
* **Link-local IPv6 (fe80::/10)** — Autoconfiguración IPv6, equivale a APIPA. → [03](direccionamiento-ip-y-subnetting.md)
* **Loopback (127.0.0.0/8, ::1)** — "Tú mismo"; nunca sale del equipo; servicios que solo escuchan ahí requieren acceso local/SSRF. → [03](direccionamiento-ip-y-subnetting.md)

### M

* **MAC** — Dirección física de 48 bits de la tarjeta (capa 2). → [00](fundamentos-como-funciona-una-red.md)
* **MTU** — Tamaño máximo de paquete IP sin fragmentar (Ethernet 1500, PPPoE 1492, VPN \~1420). → [06](tramas-mtu-y-fragmentacion.md)
* **Multiplexación** — Varias señales/comunicaciones compartiendo el mismo medio simultáneamente (por tiempo, frecuencia u onda). → [06](tramas-mtu-y-fragmentacion.md)
* **MX (registro)** — Indica qué servidor recibe el correo del dominio. → [01](dns-el-telefono-de-internet.md), [02](el-servicio-de-correo-electronico.md)

### N-P

* **NAT** — Reescritura de IP:puertos en capa 4 para que redes privadas salgan con IPs compartidas. → [04](nat-cgnat-y-hole-punching.md)
* **NS (registro)** — Servidores DNS autoritativos del dominio. → [01](dns-el-telefono-de-internet.md)
* **OSI (7 capas) / TCP-IP (4 capas)** — Modelos de referencia por capas de toda comunicación de red. → [00](fundamentos-como-funciona-una-red.md)
* **PE (polietileno)** — Material negro de cable exterior, resistente a UV. → [05](cableado-fisico-y-practica.md)
* **POSIX** — Estándares (IEEE 1003) de compatibilidad entre sistemas tipo Unix; Linux lo sigue mayormente pero no está certificado. → [10](posix-acl-y-glosario-completo.md)
* **Puertos well-known** — 0-1023: FTP 21, SSH 22, SMTP 25, DNS 53, HTTP 80, SMB 445, RDP 3389... → [00](fundamentos-como-funciona-una-red.md)
* **PTR (registro)** — DNS inverso: IP → nombre. → [01](dns-el-telefono-de-internet.md)

### R-S

* **RJ-45 / TIA-568A/B** — Conector de red y orden de hilos; A+B en extremos opuestos = cable cruzado. → [05](cableado-fisico-y-practica.md)
* **Rogue DHCP** — DHCP falso que convierte al atacante en gateway/DNS de las víctimas. → [03](direccionamiento-ip-y-subnetting.md)
* **Segmentación** — División previa de datos en trozos numerados (TCP). → [06](tramas-mtu-y-fragmentacion.md)
* **SNAT** — NAT que cambia la **IP/puerto de origen**; salida a Internet. → [04](nat-cgnat-y-hole-punching.md)
* **Socket** — IP:puerto; toda conexión va de socket a socket. → [00](fundamentos-como-funciona-una-red.md)
* **SPF** — Registro TXT que declara qué servidores pueden enviar correo del dominio. → [02](el-servicio-de-correo-electronico.md)
* **STP (Spanning Tree Protocol)** — Evita bucles de capa 2 en topologías redundantes. → [08](vlans-y-vtp.md)
* **Subnetting** — Dividir una red en subredes más pequeñas; técnica del "salto" (tamaño de bloque). → [03](direccionamiento-ip-y-subnetting.md)
* **Switch** — Conmutador de capa 2 con tabla CAM; separa dominios de colisión por puerto. → [00](fundamentos-como-funciona-una-red.md), [07](dominios-de-colision-y-switching.md)

### T-V

* **TTL** — Saltos restantes de un paquete (64 Linux, 128 Windows); fingerprinting y traceroute. → [07](dominios-de-colision-y-switching.md)
* **Tabla NAT** — Registro de traducciones activas del router; limitada en equipos domésticos. → [04](nat-cgnat-y-hole-punching.md)
* **TIA-568A/B** — Ver RJ-45. → [05](cableado-fisico-y-practica.md)
* **VLAN** — Red lógica dentro de un switch; su propio dominio de broadcast. → [08](vlans-y-vtp.md)
* **VLAN hopping** — Saltarse la segmentación: DTP spoofing o double tagging. → [08](vlans-y-vtp.md)
* **VTP** — Protocolo Cisco que sincroniza VLANs entre switches (Server/Client/Transparent); peligro: revisión alta sobrescribe. → [08](vlans-y-vtp.md)

***

## Resumen rápido

* **POSIX** = estándares de compatibilidad Unix; Linux los sigue casi todos sin estar certificado.
* **ACL** = lista ordenada de reglas permite/denegar, en archivos o en red.
* El glosario es tu **chuleta final**: si algún término se te resiste, ve al capítulo enlazado.

**Siguiente capítulo →** [11 · Todo Aplicado al Hacking](todo-aplicado-al-hacking.md)
