# Fuerza bruta de contraseñas en profundidad

## Repaso: este terreno ya se trabajó en detalle

El bloque de *Login Brute Forcing* desarrolló en profundidad los fundamentos matemáticos, los tipos de ataque (diccionario, híbrido, spraying, credential stuffing) y las herramientas dedicadas (Hydra, Medusa). Este apartado retoma el mismo terreno desde la perspectiva específica de **explotar un formulario de login ya enumerado** — es decir, una vez confirmado un nombre de usuario válido (apartado anterior de este bloque), el siguiente paso lógico es atacar su contraseña.

## Por qué filtrar la wordlist según la política de contraseñas sigue siendo el paso más rentable

Una wordlist masiva sin filtrar desperdicia tiempo probando candidatos que la propia aplicación rechazaría de antemano por no cumplir su política (longitud mínima, requisitos de complejidad). Filtrar previamente, como ya se vio en el bloque anterior, reduce drásticamente el tiempo de ataque sin perder cobertura real:

```bash
wc -l rockyou.txt
# 14.344.391 contraseñas

grep '[[:upper:]]' rockyou.txt \
  | grep '[[:lower:]]' \
  | grep '[[:digit:]]' \
  | grep -E '.{10}' > wordlist_filtrada.txt

wc -l wordlist_filtrada.txt
# ~150.000 contraseñas — una reducción de ~99%
```

O, de forma equivalente y más compacta, con un único comando `awk`:

```bash
awk 'length($0) >= 10 && /[a-z]/ && /[A-Z]/ && /[0-9]/' rockyou.txt > wordlist_filtrada.txt
```

Una reducción del 99% en el tamaño de la wordlist se traduce directamente en un ataque proporcionalmente más rápido, sin sacrificar ningún candidato que realmente pudiera cumplir la política observada de la aplicación.

## El flujo completo: de la enumeración a la contraseña

1. **Confirmar un nombre de usuario válido** mediante enumeración (apartado anterior de este bloque).
2. **Capturar la petición de login real** con un proxy de intercepción, identificando los nombres exactos de los parámetros POST y el mensaje de error devuelto ante una contraseña incorrecta.
3. **Filtrar la wordlist** según cualquier indicio conocido de política de contraseñas.
4. **Lanzar el ataque** con `ffuf` (u Hydra/Medusa, vistos en el bloque anterior) fijando el usuario ya confirmado y haciendo *fuzz* sobre el campo de contraseña.

```bash
ffuf -w wordlist_filtrada.txt \
     -u http://10.10.10.5/index.php \
     -X POST \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin&password=FUZZ" \
     -fr "Invalid username"
```

Nótese el filtro `-fr "Invalid username"`: dado que el usuario `admin` ya se confirmó como válido en la fase de enumeración, cualquier respuesta que **no** contenga ese mensaje de error específico de "usuario inválido" corresponde a un intento donde el usuario fue aceptado — la señal de que el password probado en esa iteración tuvo éxito.

```
[Status: 302, Size: 0] FUZZ: Buttercup1
```

Un código de redirección (`302`) distinto del patrón de fallo habitual confirma el hallazgo — exactamente el mismo principio de "comparar contra una respuesta de control conocida" trabajado de forma constante a lo largo de este temario, desde el fuzzing de directorios hasta la inyección SQL ciega.

## Por qué este apartado no repite todo el contenido del bloque anterior

El bloque de *Login Brute Forcing* sigue siendo la referencia completa para fundamentos, tipos de ataque y herramientas dedicadas (Hydra, Medusa). Este apartado se centra específicamente en cómo ese conocimiento se aplica como **un paso dentro de una cadena de explotación de autenticación más amplia** — tras la enumeración de usuario, antes de los apartados siguientes sobre tokens de restablecimiento, 2FA, y mecanismos de protección contra fuerza bruta.

## Hacia dónde profundizar más

Para descifrado de hashes de contraseñas capturados (en lugar de fuerza bruta directa contra un formulario en vivo) y construcción avanzada de wordlists, el ecosistema de herramientas dedicadas como Hashcat —mencionado también en cursos especializados de ataques a contraseñas— ofrece capacidades adicionales que exceden el alcance introductorio de este bloque, centrado en la explotación directa de mecanismos de autenticación web.
