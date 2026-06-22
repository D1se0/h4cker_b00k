# Validación responsable de hallazgos

## El fuzzing genera pistas, no certezas

El fuzzing es excelente para cubrir un espectro amplio rápidamente, pero produce inevitablemente **falsos positivos**: anomalías que activan los criterios de detección sin representar una vulnerabilidad real. Antes de reportar (o de seguir explotando) cualquier hallazgo, hay que **validarlo**.

## Por qué validar

- **Confirmar la vulnerabilidad**: distinguir un hallazgo real de una falsa alarma.
- **Entender el impacto**: evaluar la gravedad real, no solo la existencia del problema.
- **Reproducibilidad**: poder repetir el hallazgo de forma consistente, esencial para documentarlo y para que el equipo de desarrollo pueda verificarlo tras una corrección.
- **Recopilar evidencia**: material concreto que sustente el hallazgo ante desarrolladores o clientes.

## El proceso de verificación manual

1. **Reproducir la petición**: repetir manualmente (con `curl`, el navegador, o Repeater del proxy) la misma petición que disparó la respuesta anómala durante el fuzzing.
2. **Analizar la respuesta**: revisar con detenimiento si efectivamente indica una vulnerabilidad — mensajes de error, contenido inesperado, comportamiento que se desvía de lo normal.
3. **Explotación controlada**: si el hallazgo parece prometedor, intentar explotarlo en un entorno controlado para confirmar impacto y gravedad — siempre con la autorización correspondiente y dentro del alcance acordado.

## El principio de la prueba de concepto mínima

Al validar y explotar un hallazgo, el objetivo es **demostrar la vulnerabilidad sin causar daño**. Esto significa construir siempre la prueba de concepto (PoC) menos invasiva posible que aún así demuestre el problema de forma convincente.

> **Ejemplo**: ante una sospecha de inyección SQL, en lugar de intentar extraer o modificar datos sensibles directamente, basta con una consulta inofensiva que devuelva, por ejemplo, la cadena de versión del motor de base de datos. Eso ya demuestra control sobre la consulta SQL subyacente sin necesidad de tocar datos reales.

## Ejemplo práctico: validando un directorio de backup expuesto

Supongamos que el fuzzing reportó `/backup/` con un código `200 OK`. Esto, por sí solo, no confirma una vulnerabilidad explotable — hay que comprobar **qué hay realmente** ahí.

```bash
curl http://10.10.10.5/backup/
```

Si el servidor responde con un listado de directorio (*directory listing*) habilitado:

```html
<title>Index of /backup/</title>
...
<a href="backup.sql">backup.sql</a>  2024-Jun-12  0.2K
```

Esto confirma una vulnerabilidad real: listado de directorio habilitado, exponiendo un volcado de base de datos potencialmente accesible directamente.

### Por qué los directorios de backup son especialmente críticos

Los archivos de respaldo están, por definición, diseñados para preservar datos — lo que significa que pueden contener:

- **Volcados de base de datos**: credenciales de usuario, datos personales, información sensible completa.
- **Archivos de configuración**: claves de API, claves de cifrado, cadenas de conexión con credenciales embebidas.
- **Copias del código fuente**: revelando lógica interna, comentarios de desarrollador, o vulnerabilidades de implementación no visibles desde fuera.

## Precaución operativa al validar

- **Nunca** descargar, modificar o eliminar datos de producción más allá de lo estrictamente necesario para demostrar el hallazgo.
- Documentar el paso a paso completo de la reproducción, para que el hallazgo sea verificable de forma independiente por terceros.
- Si la validación requiere algo más invasivo que una simple comprobación de lectura (por ejemplo, confirmar una vulnerabilidad de escritura), detenerse en el punto mínimo que demuestre el riesgo sin llegar a ejecutar la acción potencialmente dañina por completo.

Esta disciplina de validación cuidadosa y mínimamente invasiva es la misma que se aplicará, con matices propios, en cada bloque de explotación posterior de este temario — desde SQL Injection hasta File Upload Attacks: siempre demostrar lo justo y necesario, nunca más.
