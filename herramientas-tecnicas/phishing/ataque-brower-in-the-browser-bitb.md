---
icon: browser
layout:
  width: default
  title:
    visible: true
  description:
    visible: false
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
  metadata:
    visible: true
  tags:
    visible: true
  actions:
    visible: true
  anchors:
    visible: true
---

# Ataque Brower-in-the-browser (BitB)

# Ataque Browser-in-the-Browser (BitB) mediante navegador remoto en Docker

## Objetivo y contexto

Este documento explica, con fines de concienciación en ciberseguridad, una variante práctica del ataque **Browser-in-the-Browser (BitB)**: en lugar de simular una ventana de login falsa con CSS/HTML dentro de una página, en este caso el atacante hace que la víctima navegue *literalmente* dentro de un navegador controlado por él, alojado en un contenedor Docker y accesible vía web (VNC/noVNC). El resultado práctico es el mismo que persigue un BitB clásico —capturar credenciales y sesiones autenticadas sin que la víctima lo perciba— pero el vector técnico es distinto: no se falsea visualmente una ventana, se **intercepta la sesión real** del usuario en tiempo real.

> **Nota ética:** esta prueba debe realizarse exclusivamente en un entorno de laboratorio controlado, con máquinas y redes propias (en este caso, Kali Linux como atacante y Windows 11 como víctima, ambas bajo tu control), y nunca contra terceros sin su consentimiento explícito. El objetivo del vídeo es que la audiencia entienda el mecanismo para poder detectarlo y defenderse de él, no replicarlo contra usuarios reales.

---
## Fase 1 — Primer despliegue: navegador remoto básico
### Atacante

Lo primero es situarnos en Kali Linux e importar una imagen Docker que contiene un navegador completo, accesible por red. La víctima se conectará a ese navegador sin saberlo, y nosotros, como atacantes, podremos observar en tiempo real todo lo que haga dentro de él. En esta primera fase lo desplegamos en su forma más simple, sin ocultar nada, para entender la base del ataque antes de refinarlo.

```bash
sudo docker pull jlesage/firefox:latest
```

Una vez descargada la imagen, la iniciamos:

```bash
sudo docker run -d \
  --name ors4-firefox \
  -p 5800:5800 \
  -v /home/kali/firefox-config:/config:rw \
  jlesage/firefox
```

Esto deja el puerto `5800` escuchando en la red del Kali, sirviendo la interfaz web (noVNC) del navegador contenido dentro del contenedor.
### Víctima

Con el puerto ya expuesto, desde la máquina víctima basta con abrir cualquier navegador convencional y acceder a:

```
http://<IP_ATACANTE>:5800/
```

Respuesta:

<figure><img src="../../.gitbook/assets/Pasted image 20260929162250.png" alt=""><figcaption></figcaption></figure>

Lo que la víctima ve en su pantalla es, en realidad, el navegador que corre dentro del contenedor del atacante, transmitido como streaming web. Cualquier cosa que teclee o pulse ahí ocurre físicamente en la máquina del atacante.

Antes de que la víctima acceda, el atacante debe configurar previamente estas opciones para adaptar la presentación del navegador:

<figure><img src="../../.gitbook/assets/Pasted image 20260929162329.png" alt=""><figcaption></figcaption></figure>

De este modo el navegador se expande a pantalla completa. Aun así, este primer montaje sigue siendo delatante: la víctima ve un navegador dentro de otro navegador, con sus propias pestañas visibles, lo cual resulta sospechoso para cualquier usuario mínimamente atento. Por eso, en la siguiente fase, se detiene este contenedor para desplegar una versión mejorada: la misma técnica, pero en modo *kiosco*, sin barra de pestañas visible y apuntando directamente a un destino concreto, de forma que la víctima no perciba que está dentro de un navegador ajeno.

---
## Fase 2 — Despliegue mejorado: modo kiosco enmascarado

### Atacante

Antes de continuar, detenemos y eliminamos el contenedor anterior:

```bash
docker stop <ID_CONTENEDOR>
docker rm <ID_CONTENEDOR>
```

Y desplegamos uno nuevo, esta vez en modo kiosco, apuntando directamente a la web objetivo (en este ejemplo, Google) y sin decoraciones de navegador:

```bash
sudo docker run -d --name ors4-firefox-kiosk -p 5800:5800 -p 5900:5900 \
  -e "FF_OPEN_URL=https://www.google.com" \
  -e "FF_KIOSK=1" \
  -v "/home/kali/firefox-config:/config:rw" \
  jlesage/firefox:latest
```

Las variables clave son:

| Variable | Función |
|---|---|
| `FF_OPEN_URL` | URL que se carga automáticamente al iniciar el navegador |
| `FF_KIOSK` | Activa el modo kiosco: oculta pestañas, barra de direcciones y elementos de la interfaz del navegador |

Esto expone de nuevo el puerto `5800`, por lo que la víctima puede acceder al mismo enlace que antes. En un escenario real fuera de tu propia red local, este acceso se haría llegar mediante un túnel (p. ej. Cloudflare Tunnel) o un VPS intermedio; en esta demostración se mantiene todo en red local para conservar el entorno controlado.
### Víctima

Accedemos de nuevo a la misma URL:

```
http://<IP_ATACANTE>:5800/
```

Respuesta:

<figure><img src="../../.gitbook/assets/Pasted image 20260929164143.png" alt=""><figcaption></figcaption></figure>

Esta vez, al no mostrarse las pestañas ni ningún elemento identificativo del navegador contenedor, la página aparenta ser un navegador normal cargando Google de forma nativa. Todo lo que el usuario busque o escriba a partir de aquí se refleja en tiempo real en la pantalla del atacante.

---
## Fase 3 — Perspectiva del atacante en tiempo real

> **Sobre la credibilidad del señuelo:** en un escenario de phishing real, el atacante reforzaría el engaño registrando un dominio visualmente similar al del servicio suplantado, de modo que el enlace que recibe la víctima resulte más convincente a simple vista. Este documento no profundiza en esa parte porque queda fuera del alcance de una demostración en entorno propio y controlado.

Desde la máquina atacante, abrimos un navegador y accedemos a la misma interfaz, pero en local:

```
http://localhost:5800/
```

Respuesta:

<figure><img src="../../.gitbook/assets/Pasted image 20260929164326.png" alt=""><figcaption></figcaption></figure>

Configuramos la vista del lado del atacante de la misma forma:

<figure><img src="../../.gitbook/assets/Pasted image 20260929164428.png" alt=""><figcaption></figcaption></figure>

Con esto, el navegador se expande y se autocompletan los huecos de la interfaz. A partir de aquí, si la víctima realiza cualquier búsqueda —por ejemplo, entra a YouTube—:

<figure><img src="../../.gitbook/assets/Pasted image 20260929164610.png" alt=""><figcaption></figcaption></figure>

El atacante observa exactamente la misma acción en tiempo real, sin que la víctima tenga forma de notarlo desde su lado:

<figure><img src="../../.gitbook/assets/Pasted image 20260929164640.png" alt=""><figcaption></figcaption></figure>

Con el contenedor funcionando correctamente, cualquier registro o inicio de sesión que la víctima realice dentro de ese navegador queda expuesto al atacante en directo: usuario, contraseña e incluso los pasos de verificación en dos factores, ya que es la propia víctima quien los introduce en la sesión ya autenticada del navegador remoto. No hay ninguna contraseña que "robar" ni ninguna verificación que "saltarse" en sentido técnico — el atacante simplemente observa una sesión legítima mientras se crea.

---
## Limpieza del entorno

Una vez terminada la demostración, es importante dejar el entorno limpio:

```bash
docker ps -a
docker stop <ID_CONTENEDOR>
docker rm <ID_CONTENEDOR>
docker images
docker rmi <ID_IMAGEN>
```

---
## Por qué funciona

- El usuario no está introduciendo sus credenciales en una réplica falsa del sitio: está usando el sitio real, dentro de un navegador que no es el suyo.
- Como la autenticación ocurre en la sesión real del navegador remoto, cualquier segundo factor (código SMS, app de autenticación, etc.) que la víctima complete queda igualmente expuesto, porque el atacante ve la sesión ya autenticada resultante.
- El eslabón débil no es la criptografía ni el protocolo de login: es la falta de contexto visual. La víctima no tiene forma de comprobar, desde una interfaz web embebida, que el navegador que está usando no es el suyo propio.

