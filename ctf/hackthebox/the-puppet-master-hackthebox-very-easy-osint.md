---
icon: flag
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
---

# The Puppet Master HackTheBox (Very Easy) - OSINT

Una vez desplegada la instancia desde la pagina de `HTB` nos proporcionaran una `IP` publica, nos metemos desde el navegador a dicha `IP` y veremos una pagina web en la cual nos mostrar informacion sobre el reto.

En este reto si nos vamos a la parte de `Evidence` veremos la siguiente imagen:

<figure><img src="../../.gitbook/assets/image (386).png" alt=""><figcaption></figcaption></figure>

Nuestro trabajo es recopilar informacion de la imagen para descubrir la `flag`. Ahora si nos vamos al apartado `Challenge` veremos una serie de preguntas...

### Pregunta 1

> ¿Qué tipo de vehículo militar se muestra en la imagen? Observa sus características: tiene ruedas, está blindado y parece ser un transporte de personal. Busca vehículos similares en línea.

Para poder encontrar el nombre utilice `Google Lens` con la imagen para ver la fuente original y en el titular ponia lo siguiente:

URL = [Pagina fuente del origen de la imagen](https://militarnyi.com/en/news/australia-sent-a-batch-of-bushmaster-armored-vehicles-to-ukraine/)

```
Australia sent a batch of Bushmaster armored vehicles to Ukraine
```

Siguiendo la estructura que pide la pagina de respuesta, pondremos lo siguiente:

Respuesta:

```
Bushmaster
```

### Pregunta 2

> ¿Quién es el fabricante/diseñador de este vehículo? Investigue la empresa que diseñó y produjo este vehículo blindado.

Si investigamos un poco en `Wikipedia` veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-13 125504.png" alt=""><figcaption></figcaption></figure>

Respuesta:

```
Thales Australia
```

### Pregunta 3

> ¿Cuándo entró en servicio militar este vehículo por primera vez? Investigue el año en que este tipo de vehículo específico se desplegó por primera vez en operaciones.

Si seguimos mirando en `Wikipedia` veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-13 125603.png" alt=""><figcaption></figcaption></figure>

Respuesta:

```
1997
```

### Pregunta 4

> ¿Cuál es el país de origen de este vehículo? Investigue dónde se diseñó y fabricó originalmente.

Siguiendo la lógica de que la procedencia era de `Thales Australia`, si ponemos `Australia` directamente funcionara, pero en `Wikipedia` tambien lo pone:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-13 125737.png" alt=""><figcaption></figcaption></figure>

Respuesta:

```
Australia
```

### Pregunta 5

> ¿Cuál es la capacidad de pasajeros de este vehículo? Investiga cuántos pasajeros más la tripulación puede transportar (formato: X pasajeros y Y conductor).

Investigando en `Wikipedia` veremos la siguiente informacion que nos lo dice todo.

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-10-13 125824.png" alt=""><figcaption></figcaption></figure>

Respuesta:

```
9 passengers and 1 driver
```

Con esto ya habremos completado los desafios y nos aparecera un boton llamado `Submit Final Analysis`, si le damos a dicho boton veremos lo siguiente:

> flag

```
HTB{c0mb1n1ng_r34l_w0rld_4nd_s3lf_c0nt41n3d_OSINT!}
```
