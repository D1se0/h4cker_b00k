# 🌐 Servicios de Red e Internet — De Cero a Hacker

> **No se puede hackear lo que no se entiende.** Antes de lanzar un exploit hay que saber cómo viajan los datos: qué es un socket, qué hace un NAT, cómo funciona el DNS que resuelve tus dominios y por qué tu conexión va lenta o tus puertos no se abren. Esta sección te da **toda la base de redes** que necesitas, desde cero hasta nivel intermedio-avanzado, siempre con la mirada puesta en el hacking ético.

---

## 📚 Índice de la sección

| Cap. | Título | Qué vas a aprender |
|------|--------|--------------------|
| [00](00-fundamentos-redes.md) | **Fundamentos de Redes** | Qué es una red, modelo OSI/TCP-IP, sockets, puertos bien conocidos, dispositivos |
| [01](01-dns.md) | **DNS: El Teléfono de Internet** | Cómo se resuelven los dominios, registros A/AAAA/MX/NS/TXT/PTR/SOA, `nslookup` y `dig` |
| [02](02-correo-electronico.md) | **Correo Electrónico (SMTP, MX, SPF)** | Cómo funciona el email, montar tu propio servidor gratis, anti-phishing |
| [03](03-direccionamiento-ip.md) | **Direccionamiento IP** | IPv4/IPv6, rangos especiales (privadas, loopback, APIPA, CGNAT), subredes |
| [04](04-nat-y-cgnat.md) | **NAT, CGNAT y Hole Punching** | Cómo sales a Internet, SNAT/DNAT, tipos de NAT, por qué no puedes abrir puertos |
| [05](05-cableado-fisico.md) | **Cableado Físico y Práctica** | TIA-568A/B, cable cruzado, auto-MDIX, AWG, CCA, cables de exterior |
| [06](06-tramas-mtu-fragmentacion.md) | **Tramas, MTU y Fragmentación** | Segmentación, multiplexación, DF flag, por qué las VPN van mal sin ajustar MTU |
| [07](07-dominios-colision-y-switching.md) | **Dominios de Colisión y Switching** | CSMA/CD vs CSMA/CA, hub vs switch vs router, rutas y métricas |
| [08](08-vlans-y-vtp.md) | **VLANs y VTP** | Segmentación lógica, trunking 802.1Q, VTP Server/Client, VLAN hopping |
| [09](09-herramientas-diagnostico.md) | **Herramientas de Diagnóstico** | `iperf3`, `nPerf`, `ping`, `traceroute`, `tcpdump`, `ss` — qué usar en cada caso |
| [10](10-glosario-posix-acl.md) | **POSIX, ACL y Glosario** | Estándares POSIX, listas de control de acceso y glosario A-Z de todos los términos |
| [11](11-aplicacion-al-hacking.md) | **Todo Aplicado al Hacking** | Cómo cada concepto se convierte en vector de ataque o técnica de pentesting |

---

## 🧭 ¿Cómo leer esta sección?

- **Si empiezas de cero:** lee los capítulos **en orden** (00 → 11). Están diseñados para que cada uno apoye al anterior.
- **Si ya tienes nivel:** usa el índice como manual de referencia. Cada capítulo incluye una caja 🎯 **"Para el hacker ético"** que conecta la teoría con técnicas reales de pentesting.

---

## 🗂️ Esquema de subida al GitBook (SUMMARY.md)

**Nombre de la sección:** `## Servicios de Red e Internet`
**Carpeta en el repo:** `servicios-de-red-e-internet/` (en minúsculas y con guiones, como el resto de tu GitBook)

**Ubicación recomendada:** entre `## Hacking con IA` y la sección `## SQL` (si ya la subiste). Así el orden de lectura queda lógico:

```
BugBounty → Hacking con IA → Servicios de Red e Internet → SQL → HERRAMIENTAS/TÉCNICAS → CTF → Conceptos...
```

Primero redes (la base), luego SQL, y después las técnicas ofensivas. El bloque exacto para copiar y pegar en tu `SUMMARY.md` está en [`summary-patch.txt`](summary-patch.txt).

**Pasos:**
1. Sube primero la carpeta `servicios-de-red-e-internet/` completa a la raíz del repo del GitBook.
2. Pega después el bloque del `summary-patch.txt` en tu `SUMMARY.md`.
3. Commit → GitBook sincroniza. El orden del índice = el orden de las líneas.

---

## 🔗 Prerrequisitos y siguientes pasos

- **Prerrequisitos:** ninguno. Esto es la base.
- **Después de esta sección:** continúa con [SQL — De Cero a Hacker](../SQL/README.md) y luego con las técnicas de [HackingWeb](../herramientas-tecnicas/hackingweb/README.md), donde todo esto se pone en práctica.

---

*Última actualización: septiembre 2026 · h4cker_b00k*
