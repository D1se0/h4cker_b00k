# 🔌 05 · Cableado Físico y Práctica

> Parece lo menos "hacker" de todo... hasta que en un CTF físico, un montaje de laboratorio o una auditoría con infraestructura legacy el problema es **el cable**. Conocer TIA-568A/B, el cable cruzado, el AWG o qué significa CCA te salva horas de "no hay conexión" y de comprar cable malo.

---

## Cables de par trenzado: categorías

| Categoría | Velocidad | Distancia máx. | Uso actual |
|-----------|-----------|----------------|------------|
| Cat5 | 100 Mbps | 100 m | Obsoleto |
| **Cat5e** | 1 Gbps | 100 m | Aún común en instalaciones viejas |
| **Cat6** | 1 Gbps (10 Gbps hasta 55 m) | 100 m | Estándar actual de oficina |
| Cat6a | 10 Gbps | 100 m | Instalaciones nuevas, 10G |
| Cat7 | 10 Gbps (apantallado S/FTP) | 100 m | Niche, requiere conectores especiales |
| Cat8 | 25/40 Gbps | 30 m | Datacenters |

> 💡 La distancia estándar es **100 metros**: 90 m de cable fijo + 10 m de latiguillos. Más allá, la señal se degrada (atenuación) y aparecen errores y renegociaciones.

---

## Pares y el estándar TIA-568A / TIA-568B

Dentro del cable hay **4 pares trenzados** (8 hilos), identificados por colores:

| Par | Hilos |
|-----|-------|
| 1 | Naranja / blanco-naranja |
| 2 | Verde / blanco-verde |
| 3 | Azul / blanco-azul |
| 4 | Marrón / blanco-marrón |

Los dos estándares definen **el orden de los hilos en el conector RJ-45**:

```
TIA-568A:  1 B-N · 2 N · 3 V-N · 4 AZ · 5 AZ-N · 6 V · 7 M-N · 8 M
TIA-568B:  1 N-N · 2 N · 3 V-N · 4 AZ · 5 AZ-N · 6 V · 7 M-N · 8 M
           (solo cambian el par naranja y el verde)
```

- **Cable directo (straight-through):** ambos extremos con el MISMO estándar (hoy casi siempre **B**). Es lo habitual: PC → switch, PC → router.
- **Cable cruzado (crossover):** un extremo **A** y el otro **B**. Cruza el par de transmisión con el de recepción.

### ¿Cuándo cruzado?

**Históricamente** (hasta ~1998, y sigue en exámenes):

| Conexión | Cable |
|----------|-------|
| PC ↔ Switch, Switch ↔ Router | Directo |
| **PC ↔ PC** (100BASE-TX), Switch ↔ Switch (viejos) | **Cruzado** |

De PC a PC en 100BASE-TX el cable tiene que ser **cruzado**, porque ambos equipos transmiten por el mismo par y recibirían por el mismo → sin cruce, cada uno transmite donde el otro transmite y no se entienden.

### Auto-MDIX: por qué hoy casi nadie se acuerda

Las **tarjetas de red y switches actuales son Auto-MDIX**: detectan automáticamente el tipo de cable (directo o cruzado) y **hacen eléctricamente el cruce ellos mismos** en el chip. Es como "auto MDI/MDI-X".

Por eso:
- Puedes unir dos PCs modernos con un cable directo y funcionará.
- El cable cruzado solo importa en equipos antiguos o con auto-MDIX desactivado.
- **Pero sigue siendo materia de examen** y de entender el "por qué" físico del cruce: el estándar MDI (tarjeta de PC) transmite por los pines 1-2 y recibe por 3-6; el MDI-X (puerto de switch) ya cruza internamente.

> 🎯 En pruebas de intrusión física (sala de comunicaciones accesible), un cable cruzado "colado" o un latiguillo mal pinzado puede servir para provocar errores y renegociaciones en un switch — y también para tu propio lab, saber soldar/crimpear evita depender de nadie.

---

## AWG: el grosor del cobre importa

**AWG (American Wire Gauge)** mide el grosor del conductor. **Cuanto menor el número, más grueso el hilo**:

| AWG | Diámetro | Uso típico |
|-----|----------|------------|
| **23 AWG** | ~0,57 mm | Cat6/Cat6a sólido de calidad (el "23 awg" de la caja) |
| **24 AWG** | ~0,51 mm | Cat5e/Cat6 estándar |
| 26 AWG | ~0,40 mm | Cables patch finos, latiguillos flexibles |

Implicaciones prácticas:

- **Más grosor (23 AWG)** → menos resistencia → mejoresdistancias y soporta **PoE** con menos calentamiento.
- **Cable sólido (solid)** → mejor para instalaciones fijas por pared; **trenzado (stranded)** → para latiguillos, resiste flexión.
- El grosor también condiciona la facilidad para hacer un **cable hembra** (keystone/jack) después: con 23 AWG es más cómodo pinzar en keystone.

---

## ⚠️ CCA: el cable trampa

**CCA (Copper Clad Aluminum)** = **aluminio bañado en cobre**. Se vende barato y parece cable normal. Problemas:

- **Impedancia más alta** que el cobre puro → más pérdida de señal, peor en distancias largas y PoE (se calienta).
- **Se puede partir**: el aluminio es frágil, se rompe con la flexión o al crimpar mal.
- No cumple estándares (no es TIA compliant) y muchos PoE se vuelven inestables con él.

**Cómo detectarlo:** raspa el hilo — si por dentro es plateado (aluminio) en vez de cobre rojizo, es CCA. También pesa menos y es más barato "demasiado".

> 💡 Regla: si el cable es para algo importante (o para PoE de cámaras/APs), **cobre puro siempre** (busca "pure copper" / "bare copper").

---

## Cable de exterior: PE y siempre negro

Para instalar cable **por el exterior** (fachadas, mástiles, entre edificios):

- Material del aislamiento: **PE (polietileno)**, resistente a UV, humedad y temperatura.
- **SIEMPRE son negros**: el negro es el color que mejor bloquea la radiación UV que degrada el plástico.
- Nunca uses cable interior (PVC) fuera: el sol lo vuelve quebradizo en meses.
- Para exteriores serios: cable con **mensajero** (cable de acero integrado para soportar el peso) o protector de jaula.

> ⚠️ Si el cable une **dos edificios distintos**, además hay que pensar en **protección contra sobretensiones y diferencias de potencial** (descarga eléctrica, rayos): protector de gas o fibra óptica en su lugar.

---

## RJ-49 / RJ-45 y el bucle de tierra

> 📌 *Nota de tu apunte:* "En RJ-49 se apantalla únicamente uno de los dos extremos".

- El conector de red estándar es el **RJ-45** (el "RJ-49" se refiere a la variante apantallada usada en telefonía/ datos apantallados — el principio es el mismo).
- En cables **apantallados (STP/FTP)**, la pantalla (malla/foil) debe conectarse **a tierra en un solo extremo**:
  - Si apantallas los dos extremos y hay **diferencia de potencial entre las tomas de tierra** de los dos equipos, circula corriente por la pantalla → **bucle de masa/tierra** → ruido, zumbidos, tráfico fantasma, y en el peor caso equipos dañados.
  - Un solo extremo a tierra rompe el bucle.
- Los cables UTP (sin pantalla) no tienen este problema, pero tampoco la protección frente a ruido intenso.

---

## Herramientas y verificación (tu "Práctica 1")

> 📌 *Nota de tu apunte:* "Primero hay que plantear la solución y luego hacerla físicamente" — en red, como en hacking: primero el diseño (qué red, qué cable, qué estándar), después el crimpeo.

| Herramienta | Para qué |
|-------------|----------|
| **Crimpadora** | Fijar el conector RJ-45 |
| **Pelacables** | Quitar la funda sin cortar hilos |
| **Tester de cable** | Verificar continuidad y orden de pines (1-1, 2-2...) |
| **Fluke / certificador** | Certificar categorías (longitud, NEXT, atenuación) |

Errores típicos al crimpear:

1. Pelar demasiado → pares destrenzados de más (el trenzado es la cancelación de ruido; máximo ~13 mm destrenzado en Cat6).
2. Hilos no llegan al fondo del conector → contacto intermitente.
3. Orden equivocado en un extremo → "cable cruzado accidental".
4. Usar conector sólido con cable trenzado (o viceversa): los conectores tienen cuchillas distintas para sólido/trenzado.

---

## Resumen rápido

- Estándares de orden de hilos: **TIA-568A/B**; mismo estándar = directo, A en un extremo y B en otro = **cruzado**.
- PC↔PC en 100BASE-TX pedía cruzado; hoy **Auto-MDIX** lo detecta todo automáticamente.
- **AWG menor = más grueso**: 23 AWG mejor para PoE y distancia; cuidado con el **CCA** (aluminio bañado: más impedancia y se parte).
- Exterior: **PE y siempre negro**; apantallado a tierra **solo en un extremo** para evitar bucle de tierra.
- 100 m es el límite estándar; tester obligatorio tras cada crimpado.

**Siguiente capítulo →** [06 · Tramas, MTU y Fragmentación](06-tramas-mtu-fragmentacion.md)
