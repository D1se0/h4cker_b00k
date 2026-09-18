# 🛠️ 09 · Herramientas de Diagnóstico de Red

> "No funciona" no es un diagnóstico. Aquí tienes las herramientas para saber **qué capa falla**: rendimiento (`iperf3`, `nPerf`), alcance (`ping`, `traceroute`), contenido (`tcpdump`, `Wireshark`) y conexiones (`ss`, `netstat`). Son las mismas que usarás en el pentesting para mapear lo que tienes delante.

---

## El método: diagnosticar por capas

Antes de lanzar comandos al azar, sigue la escala:

1. **Capa 1-2:** ¿hay enlace? → cable, Wi-Fi asociado, MAC aprendida (`ip link`, `ethtool`)
2. **Capa 3:** ¿hay IP y gateway? ¿responde el gateway? → `ip a`, `ping <gateway>`
3. **Capa 3-4:** ¿llega al destino? ¿por dónde va? → `ping`, `traceroute`, `mtr`
4. **Capa 4:** ¿el puerto está abierto? → `nc -zv`, `nmap`, `ss`
5. **Capa 7:** ¿el servicio responde? → `curl -v`, cliente del protocolo
6. **Rendimiento:** ¿va lento el camino? → `iperf3`, `nPerf`

---

## iperf3 y nPerf: midiendo el rendimiento

> 📌 *De tu apunte:* "**Iperf y Nperf**, aplicaciones para rendimiento de red bastante importantes."

### iperf3 — el medidor LAN definitivo

Mide el **caudal real (throughput)** entre dos puntos de TU red, sin depender de Internet. Necesita **servidor + cliente**:

```bash
# Máquina A (servidor)
iperf3 -s

# Máquina B (cliente, 10 segundos de prueba)
iperf3 -c 192.168.1.100
iperf3 -c 192.168.1.100 -R        # Reverse: prueba en sentido contrario
iperf3 -c 192.168.1.100 -u -b 100M   # Prueba UDP a 100 Mbps
iperf3 -c 192.168.1.100 -P 4      # 4 conexiones paralelas
iperf3 -c 192.168.1.100 -t 30     # 30 segundos
```

**Para qué lo usarás de verdad:**

- Verificar que un cable/recinto/switch entrega lo prometido (¿mi "1 Gbps" real da ~940 Mbps o se queda en 100?).
- Probar Wi-Fi en distintas estancias del hotel/oficina (¡la señal no es lo mismo que el caudal!).
- Comprobar si una VPN mata el rendimiento (iperf3 a través de la VPN vs directo).
- QoS: si configuras prioridades, iperf3 verifica si se cumplen.

### nPerf / Speedtest — midiendo Internet

Miden la conexión **hacia fuera** (latencia + bajada + subida + jitter):

```bash
# Desde la terminal (libre, sin web)
nperf                             # cliente oficial de nPerf en Linux
speedtest-cli                     # CLI de Ookla/alternativas
```

> 💡 Diferencia clave: **iperf3 mide tu red interna** (control total), **nPerf mide hasta Internet** (incluye el cuello de botella del operador). Un diagnóstico serio usa ambos: si iperf3 interno da 940 Mbps y nPerf da 30 Mbps, el problema no es tu LAN — es la línea.

---

## ping: el clásico que dice más de lo que parece

```bash
ping -c 4 ejemplo.com             # 4 pings y para
ping -i 0.2 ejemplo.com           # cada 0,2 s (rápido, puede requerir root)
ping -s 1472 -M do ejemplo.com    # prueba de MTU (capítulo 06)
ping -I eth1 192.168.1.1          # forzar interfaz de salida
```

**Cómo leerlo:**

- `time=` → latencia (RTT). <5 ms LAN, 10-40 ms nacional, >150 ms intercontinental o mala conexión.
- `ttl=` → saltos restantes: **64** = Linux/Unix/macOS, **128** = Windows (fingerprinting básico).
- `DUP!` → respuestas duplicadas: red extraña, alguien haciendo ARP spoofing, o ecocos.
- Pérdida intermitente → interferencias Wi-Fi, cable dañado, saturación.

---

## traceroute / mtr: el camino hasta el destino

```bash
traceroute ejemplo.com            # UDP por defecto en Linux
traceroute -I ejemplo.com         # ICMP (pasa más firewalls)
traceroute -T -p 443 ejemplo.com  # TCP al puerto 443 (lo dejan casi todo)
mtr ejemplo.com                   # traceroute + ping en vivo, con % de pérdida por salto
tracert ejemplo.com               # Windows
```

**Cómo leerlo:** cada salto es un router. El tiempo se dispara en un salto → cuello de botella ahí. Un salto que no responde (`* * *`) pero el siguiente sí = router que ignora ICMP, **no** es necesariamente un fallo.

> 🎯 `mtr` es la herramienta preferida para reportes: captura % pérdida y jitter por salto durante minutos — evidencia perfecta de "la línea del cliente va mal".

---

## ss / netstat: quién escucha y qué conexiones hay

```bash
ss -tulnp                         # Puertos TCP(-t)/UDP(-u) escuchando, procesos (-p), numérico (-n)
ss -tn state established          # Conexiones establecidas
ss -tp                            # Con la app dueña de cada conexión
netstat -ano                      # Windows: -a todos, -n numérico, -o PID
netstat -anob                     # Windows + ejecutable (como admin)
```

> 🎯 **Primera cosa que haces al ganar acceso a un equipo:** `ss -tulnp` / `netstat -ano`. Te revela servicios internos escuchando en localhost (bases de datos, paneles admin), conexiones hacia otras redes (pivoting) y procesos raros (¿otro C2 ya instalado?).

---

## nc (netcat): la navaja suiza

```bash
nc -zv 192.168.1.1 22,80,443      # ¿puertos abiertos?
nc -lvp 4444                      # escuchar (reverse shells, transferencias)
nc 192.168.1.50 9999 < archivo    # enviar archivo
nc -lvp 9999 > archivo            # recibirlo
```

---

## tcpdump y Wireshark: ver el tráfico de verdad

```bash
# Todo lo que entra/sale por eth0
sudo tcpdump -i eth0

# Tráfico HTTP (puerto 80) en texto
sudo tcpdump -i eth0 -A port 80

# Solo paquetes ARP (ver who-has/is-at en vivo)
sudo tcpdump -i eth0 arp

# Guardar para abrir en Wireshark después
sudo tcpdump -i eth0 -w captura.pcap port not 22

# Los 5 paquetes DNS siguientes
sudo tcpdump -i eth0 -c 5 port 53 -nn
```

**Filtros BPF que memorizarás:** `host 1.2.3.4`, `net 192.168.1.0/24`, `port 53`, `tcp`, `udp`, `icmp`, `arp`, combinables con `and/or/not`.

> 🎯 **tcpdump en servidores** (donde no hay GUI) y **Wireshark en tu portátil** para analizar el `.pcap`. En los CTFs, una captura del tráfico de la máquina objetivo a menudo revela credenciales en claro (FTP, HTTP Basic, Telnet).

---

## Otras herramientas que complementan

| Herramienta | Para qué |
|-------------|----------|
| `arp -a` / `ip neigh` | Ver la tabla ARP: quién está en tu segmento (y detectar spoofing: dos IPs → una MAC) |
| `dig` / `nslookup` | Diagnóstico DNS (capítulo [01](01-dns.md)) |
| `ethtool eth0` | Velocidad/dúplex negociados del enlace (capa 1-2) |
| `iwconfig` / `nmcli` | Estado Wi-Fi, señal, canal |
| `nmap` | El rey del escaneo (ya tienes [capítulo](../herramientas-tecnicas/reconocimiento/nmap.md) entero) |
| `hping3` | Paquetes artesanales: tests de firewall, DoS de laboratorio, fingerprinting |
| `curl -v` / `openssl s_client` | Diagnóstico capa 7 y TLS |

---

## Flujo de diagnóstico completo (ejemplo)

**"No tengo Internet":**

```bash
ip a                              # 1. ¿Tengo IP? Si es 169.254.x.x → no hay DHCP
ping -c 2 192.168.1.1             # 2. ¿Responde mi gateway? (capa 1-3 local)
ping -c 2 8.8.8.8                 # 3. ¿Sale a Internet? (capa 3 externa)
dig google.com                    # 4. ¿Resuelve DNS? (capa 7)
curl -v https://google.com        # 5. ¿La web responde? (capa 7 + TLS)
iperf3 -c <gateway>               # 6. ¿El caudal interno está bien?
```

La primera que falla te dice la capa rota. Este mismo orden sirve en el examen, en el trabajo y en el CTF.

---

## Resumen rápido

- Diagnostica **por capas**: enlace → IP → puertos → servicio.
- **iperf3** = rendimiento interno (servidor+cliente); **nPerf** = rendimiento hacia Internet.
- **ping** te da latencia, TTL (fingerprinting S.O.) y pérdida; con `-M do -s` mides la MTU.
- **traceroute/mtr** muestran el camino y dónde se degrada.
- **ss/netstat** = qué escucha y qué conexiones hay (primer comando tras ganar acceso).
- **tcpdump/Wireshark** = ver el tráfico real y capturar credenciales.

**Siguiente capítulo →** [10 · POSIX, ACL y Glosario](10-glosario-posix-acl.md)
