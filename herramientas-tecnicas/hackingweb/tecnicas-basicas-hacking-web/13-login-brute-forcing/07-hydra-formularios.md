# Hydra contra formularios de login

## Por qué los formularios personalizados requieren más configuración que Basic Auth

A diferencia de la autenticación HTTP básica (protocolo estandarizado y predecible, visto en el apartado anterior), cada aplicación implementa su propio formulario de login con su propia estructura de campos, su propio endpoint, y su propio criterio para indicar éxito o fracaso. Esto significa que Hydra necesita información explícita sobre **cómo está construida** esa petición concreta antes de poder automatizar el ataque.

## Anatomía de un formulario de login típico

```html
<form method="POST">
    <input type="text" name="username">
    <input type="password" name="password">
    <input type="submit" value="Login">
</form>
```

Que, al enviarse, genera una petición como:

```
POST /login HTTP/1.1
Host: www.ejemplo.com
Content-Type: application/x-www-form-urlencoded

username=admin&password=algo
```

Antes de atacar este formulario con Hydra, hay que identificar tres datos exactos:

1. **La ruta del endpoint** que procesa el login (`/login`).
2. **Los nombres exactos de los parámetros** (`username`, `password` — varían entre aplicaciones: pueden llamarse `user`, `email`, `pass`, `pwd`, etc.).
3. **Cómo distinguir un intento fallido de uno exitoso** en la respuesta del servidor.

El primer y segundo dato se obtienen inspeccionando el HTML del formulario o, más fiablemente, capturando la petición real con las DevTools del navegador o un proxy de intercepción (vistos en el bloque de *Web Proxies*) — exactamente el mismo proceso de reconocimiento aplicado en cada bloque de explotación de este temario.

## El módulo `http-post-form`

```bash
hydra [opciones] objetivo http-post-form "ruta:parametros:condicion"
```

Los tres componentes separados por `:` son:

- **`ruta`**: el endpoint que procesa el login (`/login`).
- **`parametros`**: el cuerpo de la petición, con `^USER^` y `^PASS^` como marcadores de posición que Hydra sustituye en cada intento.
- **`condicion`**: cómo reconocer si el intento falló o tuvo éxito.

```bash
hydra -L usuarios.txt -P contraseñas.txt 10.10.10.5 http-post-form \
  "/login:username=^USER^&password=^PASS^:F=Invalid credentials"
```

## Condición de fallo (`F=`) vs. condición de éxito (`S=`)

| Tipo | Cuándo usarla | Ejemplo |
|---|---|---|
| `F=texto` | El servidor muestra un mensaje de error reconocible ante credenciales incorrectas | `F=Invalid credentials` |
| `S=texto` o `S=código` | El servidor no tiene un mensaje de error claro, pero sí una señal de éxito reconocible (redirección, contenido específico) | `S=302` o `S=Dashboard` |

```bash
# Detectar éxito por redirección HTTP 302
hydra ... http-post-form "/login:user=^USER^&pass=^PASS^:S=302"

# Detectar éxito por contenido específico en la respuesta
hydra ... http-post-form "/login:user=^USER^&pass=^PASS^:S=Dashboard"
```

`F=` es, en la práctica, la opción más usada: la mayoría de aplicaciones devuelven un mensaje de error consistente y fácil de identificar ante credenciales incorrectas, mientras que el contenido exacto de una página de "éxito" (un panel de control completo) puede variar más entre peticiones y resultar menos fiable como ancla de comparación.

## El flujo de trabajo completo

1. **Inspeccionar el formulario** (HTML fuente, o capturando la petición real con DevTools/proxy) para identificar ruta y nombres de parámetros exactos.
2. **Enviar manualmente un intento fallido** y observar exactamente qué distingue la respuesta — un mensaje de error textual, un código de estado, ausencia de redirección.
3. **Construir el comando Hydra** con esa información, usando `F=` o `S=` según cuál sea más fiable en ese caso concreto.
4. **Elegir la wordlist** apropiada según el contexto (genérica, orientada al objetivo, o filtrada por política de contraseñas conocida, como se vio en apartados anteriores de este bloque).

## Por qué este nivel de detalle importa

Una configuración incorrecta de la condición de éxito/fracaso es la causa más común de que un ataque con `http-post-form` parezca "no funcionar" — si Hydra no distingue correctamente un intento fallido de uno exitoso, puede reportar falsos positivos (marcar como válida una combinación que en realidad falló) o, peor, no detectar nunca la combinación correcta aunque esté en la wordlist probada. Por eso el paso de **observar manualmente** la respuesta exacta del servidor ante un intento fallido, antes de automatizar nada, es indispensable — el mismo principio de "verificar antes de confiar en la herramienta" trabajado en el bloque de *SQLMap Essentials* al hablar de diagnóstico de problemas.
