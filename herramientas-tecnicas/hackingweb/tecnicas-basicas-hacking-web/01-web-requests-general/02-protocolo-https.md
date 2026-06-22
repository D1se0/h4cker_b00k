# HTTPS y cifrado en tránsito

## El problema de fondo: HTTP viaja en texto plano

HTTP, tal y como se diseñó originalmente, transmite toda la información sin cifrar. Esto significa que cualquier dispositivo situado entre el cliente y el servidor —un router intermedio, un punto de acceso WiFi malicioso, un proxy corporativo— puede leer literalmente todo el contenido de la conversación: credenciales, cookies de sesión, datos de formularios, todo.

Esta debilidad es lo que hace posible los ataques de tipo **Man-in-the-Middle (MitM)**: un atacante se posiciona en el camino de la comunicación (por ejemplo, mediante ARP spoofing en una red local, o montando un punto de acceso WiFi falso) y captura el tráfico con herramientas como Wireshark. Si la comunicación va en claro, ver un usuario y contraseña enviados por un formulario de login es tan sencillo como filtrar los paquetes capturados por el método POST.

**HTTPS** (*HTTP Secure*) nace exactamente para resolver esto: añade una capa de cifrado (TLS, antes llamado SSL) por debajo de HTTP, de forma que aunque alguien intercepte el tráfico, lo único que ve es un flujo de bytes cifrados sin ningún sentido legible.

Por este motivo, HTTPS se ha convertido en el estándar de facto en la web moderna, hasta el punto de que los navegadores actuales marcan activamente como "no seguro" cualquier sitio que siga sirviendo contenido sensible por HTTP.

## Identificar HTTPS

Un sitio que usa HTTPS se reconoce por dos señales:

- La URL empieza por `https://`
- El navegador muestra un icono de candado junto a la barra de direcciones

Si alguien captura tráfico HTTPS, en lugar de ver credenciales en claro, observará un flujo cifrado indescifrable sin la clave de sesión correspondiente.

> **Nota sobre privacidad**: que el contenido vaya cifrado no significa que toda la actividad sea invisible. Si el sistema resuelve los dominios contra un servidor DNS que no cifra sus propias consultas, alguien que observe ese tráfico DNS puede ver qué dominios estás visitando, aunque no pueda ver el contenido de esas visitas. Por eso se recomiendan resolutores DNS cifrados (como `1.1.1.1` o `8.8.8.8` sobre DoH/DoT) o el uso de una VPN para anonimizar también esa capa.

## Cómo se establece una conexión HTTPS: el handshake TLS

A grandes rasgos, el flujo es el siguiente:

1. El cliente intenta acceder a un recurso. Si escribe `http://` en lugar de `https://` y el servidor exige HTTPS, primero se envía la petición al puerto 80 (HTTP).
2. El servidor detecta esto y responde con un código de redirección **`301 Moved Permanently`**, indicando al cliente que debe repetir la petición contra el puerto 443 usando HTTPS.
3. El cliente envía un mensaje **"Client Hello"**, anunciando qué versiones de TLS y qué algoritmos de cifrado soporta.
4. El servidor responde con un **"Server Hello"**, eligiendo los parámetros de cifrado, y envía su certificado SSL/TLS.
5. Se realiza un **intercambio de claves** (*key exchange*): el cliente valida el certificado del servidor (comprobando que está firmado por una entidad de confianza, que no ha caducado, que el dominio coincide, etc.) y ambas partes generan una clave de sesión simétrica que usarán para cifrar el resto de la comunicación.
6. Una vez el *handshake* concluye con éxito, la comunicación HTTP normal se reanuda, pero ahora completamente cifrada.

Este proceso ocurre en milisegundos y es completamente transparente para el usuario final, pero entenderlo es importante para un pentester porque revela varias superficies de ataque potenciales: degradación de protocolo, certificados mal configurados, *cipher suites* débiles, etc.

> **Degradación HTTPS → HTTP (SSL Stripping)**: en determinadas condiciones, un atacante puede interponerse como proxy MitM y forzar a que la comunicación entre el cliente y el servidor "real" sea HTTPS, pero entre el cliente y el atacante sea HTTP sin cifrar, capturando así los datos en claro sin que el usuario lo perciba a simple vista. Los navegadores modernos incorporan protecciones contra esto (como la cabecera `Strict-Transport-Security`, que veremos en el apartado de cabeceras de seguridad), pero sigue siendo un vector relevante en redes mal protegidas.

## `curl` y certificados

`curl` gestiona automáticamente todo el proceso de cifrado: hace el *handshake*, valida el certificado y cifra/descifra los datos sin que tengamos que preocuparnos por ello. El problema aparece cuando el certificado del servidor no es válido —algo extremadamente común en entornos de laboratorio, máquinas internas o aplicaciones recién desplegadas que usan certificados autofirmados.

Por defecto, `curl` rechaza continuar la conexión si detecta un certificado inválido, justamente para protegernos de un posible MitM:

```bash
curl https://10.10.10.5

curl: (60) SSL certificate problem: unable to get local issuer certificate
```

Cuando sabemos que estamos en un entorno controlado (un laboratorio, una máquina interna de pentest) y el certificado simplemente no está validado por una CA reconocida —no porque exista un ataque real—, podemos forzar a `curl` a ignorar esa validación con el parámetro `-k` (*insecure*):

```bash
curl -k https://10.10.10.5
```

> **Importante**: usar `-k` desactiva una protección de seguridad real. Es perfectamente razonable hacerlo en un laboratorio donde controlamos ambos extremos de la comunicación, pero nunca se debería usar como práctica habitual contra sistemas en producción o desconocidos, ya que anula precisamente la protección que evita ataques MitM.

## Resumen práctico

| Situación | Acción |
|---|---|
| Sitio con certificado válido | `curl` funciona sin parámetros adicionales |
| Laboratorio/máquina interna con certificado autofirmado | `curl -k https://...` |
| Queremos inspeccionar el certificado | `openssl s_client -connect host:443` |
| Sospechamos degradación HTTP/HTTPS | Revisar si el sitio implementa `Strict-Transport-Security` |
