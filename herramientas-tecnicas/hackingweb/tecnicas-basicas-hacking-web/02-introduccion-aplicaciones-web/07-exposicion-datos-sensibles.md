# Exposición de datos sensibles en el frontend

## Por qué el frontend, pese a ser "del cliente", también es objetivo

Es tentador pensar que las vulnerabilidades del lado del cliente son menos graves que las del backend, ya que atacar el frontend no compromete directamente el servidor. Pero esta visión es incompleta: el frontend expone directamente al **usuario final** a riesgo. Si un atacante explota una vulnerabilidad del lado del cliente contra un administrador (por ejemplo, mediante un XSS dirigido), puede acabar obteniendo acceso no autorizado a funcionalidades sensibles que sí derivan en comprometer todo el backend.

## Qué es la exposición de datos sensibles

Se refiere a cualquier información confidencial accesible directamente en el código fuente que el navegador descarga y que cualquier usuario puede inspeccionar — sin necesidad de ningún ataque sofisticado, solo viendo el código fuente de la página (clic derecho → *Ver código fuente*, o `Ctrl+U`).

> **Nota**: algunos sitios deshabilitan el clic derecho como medida (ineficaz) de "protección". Esto no impide nada: el atajo de teclado `Ctrl+U` sigue funcionando, y herramientas como un proxy de intercepción (Burp Suite) o simplemente `curl` muestran el código fuente sin pasar por el navegador en absoluto.

## Dónde suele aparecer

- **Comentarios HTML olvidados** por desarrolladores, a veces conteniendo credenciales de prueba, notas internas, o referencias a funcionalidad en desarrollo.
- **Código JavaScript externo** que revela lógica interna, endpoints de API no documentados, o claves de acceso embebidas por error.
- **Enlaces o rutas ocultas** que no aparecen en la navegación visible pero sí están referenciados en el código (por ejemplo, en un script de menú dinámico que aún no se ha activado en producción).

### Ejemplo ilustrativo

```html
<form action="action_page.php" method="post">
    <label for="uname"><b>Username</b></label>
    <input type="text" required>
    <label for="psw"><b>Password</b></label>
    <input type="password" required>

    <!-- TODO: remove test credentials test:test -->

    <button type="submit">Login</button>
</form>
```

El comentario `<!-- TODO: remove test credentials test:test -->` es exactamente el tipo de descuido que aparece con más frecuencia de lo que cabría esperar en entornos reales: un recordatorio de limpieza que el equipo de desarrollo olvidó ejecutar antes de desplegar a producción. Encontrar credenciales de prueba que siguen siendo válidas en producción es uno de los hallazgos "de bajo esfuerzo, alto impacto" más habituales en una auditoría.

No siempre se trata de credenciales explícitas: a veces es información indirecta —una ruta de administración, el nombre de una función interna, un comentario indicando "este endpoint no valida el parámetro X todavía"— que por sí sola no compromete nada, pero que aporta contexto valioso para dirigir el resto de la auditoría.

## Por qué conviene revisar el código fuente como primer paso

Revisar el código fuente del frontend debería ser uno de los primeros pasos al evaluar cualquier aplicación web, precisamente porque es información gratuita: no requiere enviar ningún payload, no genera tráfico sospechoso, y puede revelar de inmediato rutas, parámetros o credenciales que orienten el resto de la metodología. Existen además herramientas automatizadas (algunas integradas en proxies como Burp Suite, otras dedicadas) que escanean el código fuente de páginas en busca de patrones sospechosos: claves de API, tokens, URLs internas, etc.

## Prevención (perspectiva del desarrollador)

- El código frontend debería contener únicamente lo estrictamente necesario para el funcionamiento de la aplicación, sin comentarios de depuración ni código muerto.
- Establecer un proceso de revisión antes de cada despliegue que verifique específicamente la ausencia de credenciales, claves o comentarios sensibles.
- Clasificar qué tipo de información puede exponerse en el lado del cliente y aplicar controles explícitos sobre eso.
- Usar minificación y ofuscación de JavaScript en producción — no como medida de seguridad por sí sola (es trivialmente reversible, como veremos en el bloque de *JavaScript Deobfuscation*), pero sí como una barrera adicional que dificulta el escaneo automatizado masivo.
