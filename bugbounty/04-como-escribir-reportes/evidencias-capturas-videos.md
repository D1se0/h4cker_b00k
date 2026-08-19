---
icon: camera-viewfinder
---

# Evidencias: capturas y vídeos

> 🎯 **Mi regla personal**: documentarlo TODO al detalle, como si la persona que lo va a leer no supiera nada del tema, y que pueda reproducirlo de la mejor forma posible. Siempre capturas, y si se puede, vídeo.

## 📸 Por qué importan tanto las capturas

Un triager revisa decenas de reportes. Un reporte con evidencia visual clara en cada paso:

* Se revisa más rápido (menos idas y venidas de "necesito más info").
* Genera más confianza (demuestra que el hallazgo es real y reproducible, no una teoría).
* Reduce el riesgo de malentendidos sobre qué se probó exactamente.

## 🖼️ Qué capturar en cada paso

Para cada paso de tu PoC, la captura debería mostrar, siempre que sea posible:

* **La petición completa** (URL, método, headers relevantes como `Authorization`, body si aplica).
* **La respuesta completa** (código de estado HTTP + cuerpo de la respuesta).
* **Contexto de quién eres en ese momento** (por ejemplo, qué cuenta tienes autenticada, mostrado en consola o en la UI).
* **Marcas de tiempo cuando sean relevantes** para probar persistencia entre pasos (por ejemplo, un mismo `timestamp` que aparece en la escritura y luego en la lectura desde otra cuenta — prueba irrefutable de que la acción tuvo efecto real).

## 🎥 Cuándo grabar vídeo en vez de (o además de) capturas

El vídeo es especialmente útil cuando:

* El fallo requiere **varios pasos encadenados** difíciles de seguir solo con capturas sueltas (ej. flujos de login, multi-step forms, cambios de cuenta).
* Quieres demostrar **timing** (ej. una condición de carrera, o que un evento ocurre "en directo" en otra sesión sin que el atacante haga nada más).
* El impacto se aprecia mucho mejor viendo la interfaz reaccionar en tiempo real (ej. ver aparecer un elemento en la cuenta víctima justo después de la acción del atacante).

Herramientas recomendadas: OBS Studio, o el grabador de pantalla nativo del sistema operativo. Exporta en un formato ligero (MP4/WEBM) y recorta para no mandar vídeos eternos.

## 🧷 Buenas prácticas al anotar capturas

* Usa flechas/recuadros para señalar el dato clave (código de estado, el identificador manipulado, el campo modificado).
* Numera las capturas siguiendo el mismo orden que los pasos del texto (`1.png`, `2.png`...) y referencia ese número explícitamente en el paso correspondiente.
* Evita capturas gigantes de pantalla completa sin recortar — recorta a lo relevante (ventana del proxy, consola, respuesta JSON).
* Si hay texto pequeño (JSON, headers), asegúrate de que sea legible sin tener que hacer zoom extremo.

## 🕵️ Evidencia en consola/DevTools

Para bugs de frontend/API que involucran sesión de usuario (cookies, JWT, `localStorage`), es muy potente ejecutar un pequeño script en la consola del navegador que:

1. Decodifique la cookie/token de sesión y muestre explícitamente **quién está autenticado** en ese momento.
2. Ejecute el `fetch()` de la prueba.
3. Imprima en el mismo `console.log` quién hizo la petición, a qué objetivo, y qué respondió el servidor.

Esto elimina cualquier ambigüedad sobre "¿estabas realmente autenticado como el atacante cuando accediste al recurso de la víctima?" — todo queda en la misma línea de log, verificable.

```javascript
// Patrón reutilizable: reporta quién soy yo + qué pido + qué contesta el server, todo junto
(async () => {
  const cookie = document.cookie.split('; ').find(c => c.startsWith('session='));
  const me = JSON.parse(decodeURIComponent(cookie.split('session=')[1]));
  const r = await fetch('https://ejemplo.com/api/recurso?id=OTRO_ID', {credentials: 'include'});
  const body = await r.json();
  console.log('Autenticado como:', me.userId, '| Status:', r.status, '| Respuesta:', body);
})();
```

## ⚠️ Qué NO debe aparecer nunca en tus evidencias

* Datos reales de clientes/usuarios de terceros.
* Credenciales completas de producción que sigan siendo válidas (redacta parcialmente si es imprescindible mostrarlas).
* Información personal identificable que no sea estrictamente tuya o de tu cuenta de prueba.

Si necesitas mostrar un token o dato sensible como prueba, considera si es imprescindible mostrarlo completo o si con una parte redactada basta para que el equipo de seguridad lo identifique en sus propios logs.
