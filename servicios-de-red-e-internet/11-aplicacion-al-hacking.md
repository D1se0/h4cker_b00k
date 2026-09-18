---
icon: square-up-right
---

# Todo Aplicado al Hacking

> Todo lo anterior tiene una razón de ser en hacking ético. Este capítulo es el **mapa mental inverso**: de cada concepto de red → a cómo se usa, se ataca o se explota. Ideal para atar la sección entera.

***

## Recon: lo que aprendiste en [01](01-dns.md)

| Concepto                        | Uso ofensivo/defensivo                                                                                       |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| `dig axfr`                      | **AXFR mal configurado** = toda la zona DNS gratis (subdominios internos, hosts). Primer check de recon DNS. |
| Registros A/AAAA/CNAME          | Mapear superficie: subdomain enumeration → resolver → IPs → escanear.                                        |
| TXT                             | Enumeración de SPF (los SPF largos filtran rangos/proveedores internos), verificación de servicios cloud.    |
| Reverse (PTR)                   | En bug bounty, el reverse DNS de rangos del objetivo revela hosts.                                           |
| DNS hijack / subdomain takeover | Registro NS o CNAME apuntando a un servicio muerto → lo reclamas y sirve contenido en su dominio.            |
| DoT/DoH                         | Tus propios tools: exfiltra por DoH pasa desapercibido; defiende: bloquea DoT externo y fuerza tu resolver.  |

***

## Segmentación: VLANs y ACLs de [08](08-vlans-y-vtp.md) y [10](10-glosario-posix-acl.md)

* **VLAN hopping** (DTP spoofing, double tagging): si el switch tiene puertos con `switchport mode dynamic auto` o native VLAN sin retocar, la "segmentación" es papel mojado.
* **Rogue DHCP en una VLAN** te convierte en gateway/DNS de la VLAN → MITM total.
* **ACLs mal ordenadas**: se evalúan de arriba abajo; una `deny` tras una `permit broad` no hace nada. Auditar siempre el orden.
* Rediseño defensivo: native VLAN no usada ≠ 1, puertos de usuario sin DTP, ACLs explícitas con deny al final y logging.

## NAT y alcance: de [04](04-nat-y-cgnat.md)

* **Englobar el scope**: "¿la víctima está tras CGNAT?" define si puedes recibir shell reversa directa o necesitas tunnel inverso (ngrok, Cloudflare Tunnel, proxychains...).
* **NAT capas 3+4**: entendió IPs **y** puertos → el防火 masquerade de Linux también puede filtrar por puerto: replay de reglas `iptables -t nat -L -n -v` al auditar.
* **Port forwarding olvidado** en routers domésticos de la red corporativa (WAN del CTF): una crítica clásica de informe.
* **Full cone vs simétrico**: al pivotar, si el NAT del target es simétrico, el hole punching de tu VPN mesh falla → usa relay.

## Todo lo de cable/medio de [05](05-cableado-fisico.md) y [06](06-tramas-mtu-fragmentacion.md)

* **Físico**: en auditorías de pequeña empresa, el switch del armario con cables CCA apretados y sin separación de datos/luz es una causa real de "la red va lenta". Saberlo lo distingue de "el server va mal".
* **MTU**: el clásico "el VPN conecta pero no carga nada" = MTU. Diagnóstico: `ping -M do -s 1472 1.1.1.1` (1500-28=1472 payload ICMP). El -M do pone DF flag: si falla a 1472, tu camino tiene MTU <1500.
* **DF flag / PMTUD**: "black hole" cuando ICMP "fragmentation needed" está bloqueado → conexiones que se congelan. Exploit/Pentest: a veces puedes DoSear conexiones falsificando ese ICMP (raro hoy).
* **Jumbo frames** sin MTU consistente = packets silently dropped. En el informe: "unifique MTU end-to-end".

## Herramientas de [09](09-herramientas-diagnostico.md) como "cuchillo suizo" del pentester

* En un servidor comprometido (Linux minimalista sin nmap), `ping`, `traceroute`, `nc`, `curl` y `ip route` bastan para **mapear el entorno interno**: ¿qué redes ve? ¿hay gateways? ¿el DNS interno filtra nombres?
* `iperf3` entre dos hosts pivotados te dice si el canal es apto para exfiltración grande o hay QoS/shaping.
* Todo esto también lo usará el **blue team** para diagnosticar; en el informe, aporta credibilidad saberlo explicar.

***

## Checklist final del "hacker de redes"

Antes de decir "ya sé redes", responde de memoria:

1. ¿Qué protocolo resuelve nombre→IP y qué 8 tipos de registro conoces?
2. ¿Cómo sabrías si estás tras CGNAT y qué opciones tienes para recibir conexiones?
3. ¿Cuál es la MTU de Ethernet? ¿Y por qué en PPPoE o VPN cambia?
4. ¿Diferencia entre dominio de colisión y de broadcast? ¿Qué dispositivo separa cada uno?
5. ¿SNAT vs DNAT: qué campo cambia cada uno y para qué se usa?
6. ¿Qué es VLAN hopping y cómo se mitiga?
7. ¿Qué hace `setfacl` y qué hace una ACL de red?
8. ¿Qué es POSIX y por qué "Linux es casi POSIX"?
9. Si un cable dice CCA, ¿lo compras para PoE?
10. ¿Qué es el hole punching y en qué apps lo usas cada día?

Si las 10 salen fluidas, ya no eres principiante: **has terminado la base**. El siguiente nivel son protocolos concretos (HTTP, TLS, SMB, Kerberos), que son terreno de la sección HackingWeb del GitBook.

***

## Resumen rápido

* Cada concepto "aburrido" de red tiene un ángulo de seguridad: DNS→recon, NAT→alcance, VLAN→segmentación, MTU→conectividad, ACL→control.
* La misma herramienta sirve para diagnosticar y para atacar; lo que cambia es el permiso.
* Termina con el checklist de 10 preguntas: es tu examen personal.

**← Capítulo anterior:** [10 · POSIX, ACL y Glosario](10-glosario-posix-acl.md) · **Volver al inicio:** [README](./)
