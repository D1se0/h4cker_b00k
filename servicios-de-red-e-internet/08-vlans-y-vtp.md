# 🏷️ 08 · VLANs y VTP

> Las VLANs son la forma de partir una red física en varias redes lógicas sin comprar más switches. En las empresas y en los CTFs de red están por todas partes — y su mala configuración es una puerta trasera clásica (VLAN hopping).

---

## ¿Qué es una VLAN?

**VLAN (Virtual LAN)** = agrupar puertos/dispositivos en **redes lógicas separadas**, aunque estén conectados al mismo switch físico.

Cada VLAN es **su propio dominio de broadcast**: un broadcast en la VLAN 10 **no** llega a la VLAN 20. Para comunicar VLANs distintas hace falta un **router (o firewall/L3 switch)** — que además es el punto natural donde poner ACLs e inspección.

**Para qué se usan:**

- 🔒 **Seguridad:** separar invitados, empleados, cámaras IP, servidores, IoT.
- 🚀 **Rendimiento:** cada broadcast muere en su VLAN.
- 🧹 **Organización:** por departamentos (RRHH, IT, Ventanas...), por tipo de dispositivo.

```
Un solo switch físico:
┌─────────────────────────────────┐
│  P1─P8   = VLAN 10 (RRHH)       │
│  P9─P16  = VLAN 20 (IT)         │
│  P17─P24 = VLAN 30 (Invitados)  │
└─────────────────────────────────┘
   ↑ tres redes lógicas, un solo chasis
```

---

## Acceso vs Trunk: los dos tipos de puerto

| Tipo de puerto | Qué lleva | Dónde se usa |
|----------------|-----------|--------------|
| **Access** | Tráfico de **UNA sola VLAN**, sin etiquetas | Puertos hacia PCs, impresoras, APs domésticos |
| **Trunk** | Tráfico de **VARIAS VLANs etiquetadas** | Enlaces entre switches, y switch↔router |

### La etiqueta 802.1Q

El estándar **IEEE 802.1Q** inserta una **etiqueta de 4 bytes** en la trama Ethernet con el ID de la VLAN (1–4094):

```
[ Dest MAC | Origen MAC | 802.1Q tag (VLAN ID) | Datos | FCS ]
```

Cuando la trama sale por un puerto **access**, la etiqueta se **elimina** (el PC final nunca la ve). Por los trunks viaja etiquetada.

> 💡 **VLAN nativa:** en un trunk, una VLAN se configura como "nativa" y su tráfico viaja **SIN etiquetar**. Por defecto es la VLAN 1 — y es la causa de bastantes saltos de VLAN (ver más abajo).

---

## Router-on-a-Stick: comunicar VLANs

Con un solo router y un solo cable hacia el switch, el router se divide en subinterfaces, una por VLAN:

```
Router Gig0/0
├── Gig0/0.10 → VLAN 10 → 192.168.10.1/24
├── Gig0/0.20 → VLAN 20 → 192.168.20.1/24
└── Gig0/0.30 → VLAN 30 → 192.168.30.1/24
```

```cisco
# Configuración en el router
interface GigabitEthernet0/0.10
 encapsulation dot1Q 10
 ip address 192.168.10.1 255.255.255.0

interface GigabitEthernet0/0.20
 encapsulation dot1Q 20
 ip address 192.168.20.1 255.255.255.0

# Configuración en el switch
interface GigabitEthernet0/1
 switchport mode trunk
```

Cada PC pone como gateway la IP de su subinterface → el router enruta entre VLANs (y ahí puedes meter ACLs: "la VLAN de invitados no puede tocar la de servidores").

---

## VTP: VLAN Trunking Protocol

> 📌 *De tu apunte:* **VTP (VLAN Trunking Protocol)** es un **protocolo de Cisco** que **centraliza y distribuye la información de las VLANs** entre switches de una red.

El **VTP Server crea, modifica y elimina VLANs**, y esos cambios se **sincronizan automáticamente** con los switches VTP Client.

### Roles VTP

| Rol | Qué puede hacer |
|-----|-----------------|
| **Server** | Crear/borrar/modificar VLANs y difundirlas (por defecto todo switch es server) |
| **Client** | No puede crear VLANs: solo **recibe** y sincroniza las del server |
| **Transparent** | No participa; reenvía anuncios pero mantiene sus VLANs locales |

El server manda anuncios VTP periódicos con un **número de revisión** que siempre se incrementa. Los switches aceptan la configuración con **la revisión más alta**.

### ⚠️ El peligro clásico del VTP

Si conectas a la red un **switch viejo de laboratorio con una revisión VTP más alta** (un server con revisión 40 cuando el dominio va por 15), **sobrescribe las VLANs de toda la red**. Si ese switch no tenía las VLANs, pueden desaparecer de todos lados. Por eso:

- Nunca enchufes switches usados sin resetear VTP (cambia el dominio o ponlo transparent).
- En redes pequeñas, muchos admins directamente **deshabilitan VTP** y configuran VLANs a mano.

### 🎯 Para el hacker ético

- Si consigues acceso de admin a un switch del dominio VTP (credenciales por defecto, SNMP público, consola abierta), **puedes crear una VLAN a tu antojo y propagarla a toda la red**.
- Y en la otra dirección: un "server" con revisión alta puede borrar VLANs → DoS de capa 2 espectacular.

---

## VLAN Hopping: cómo se salta la segmentación

### Ataque 1 — Switch Spoofing (DTP)

**DTP (Dynamic Trunking Protocol)**, también de Cisco, negocia automáticamente si un puerto será access o trunk. Si el puerto del switch está en modo `dynamic auto` o `dynamic desirable`, un atacante que se hace pasar por switch (hablando DTP) **convence al puerto de convertirse en trunk** → recibe tráfico etiquetado de todas las VLANs.

```bash
# Yersinia: hablar DTP para forzar trunk
yersinia -G   # interfaz gráfica → attack → DTP → "enabling trunking"
```

### Ataque 2 — Double Tagging

El atacante envía una trama **con dos etiquetas 802.1Q** (la exterior = la VLAN nativa, la interior = la VLAN objetivo):

1. El switch recibe la trama, ve la etiqueta exterior (VLAN nativa) y la **quita** (las nativas van sin etiqueta).
2. Ahora la etiqueta que queda visible es la interior → la trama "aparece" ya dentro de la VLAN objetivo.
3. El switch la reenvía a la VLAN víctima. No es bidireccional (one-way), pero basta para inyectar tráfico o explotar respuestas.

**Defensas (lo que buscarás en el informe):**

- ❌ Deshabilitar DTP: `switchport nonegotiate` y forzar `switchport mode access` en todos los puertos de usuario.
- ❌ Cambiar la VLAN nativa del trunk a una VLAN muerta (no la 1) y etiquetar la nativa (`vlan dot1q tag native`).
- ✅ Deshabilitar puertos sin uso y apagar VTP si no se necesita.

---

## Configuración básica en Cisco (chuleta)

```cisco
# Crear VLANs
vlan 10
 name RRHH
vlan 20
 name IT

# Puerto de acceso (a un PC)
interface FastEthernet0/5
 switchport mode access
 switchport access vlan 10
 switchport nonegotiate        ! anti-DTP

# Puerto trunk (a otro switch o router)
interface GigabitEthernet0/1
 switchport mode trunk
 switchport trunk allowed vlan 10,20

# Ver qué hay
show vlan brief
show interfaces trunk
show vtp status
```

---

## Resumen rápido

- VLAN = red lógica dentro de un switch; cada una es su dominio de broadcast; se comunica entre sí vía router.
- Puerto **access** (una VLAN, sin etiquetas) vs **trunk** (etiquetas 802.1Q de varias VLANs).
- **VTP (Cisco):** el Server crea/modifica/elimina VLANs y se sincroniza con los Clients vía número de revisión — el riesgo es que un switch con revisión mayor sobrescribe la red.
- **VLAN hopping:** DTP spoofing (forzar trunk) y double tagging (por la VLAN nativa sin etiqueta).
- Defensa: `nonegotiate`, modo access fijo, VLAN nativa muerta y etiquetada, puertos sin uso apagados.

**Siguiente capítulo →** [09 · Herramientas de Diagnóstico](09-herramientas-diagnostico.md)
