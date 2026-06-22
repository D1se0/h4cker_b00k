# Descubrimiento de XSS

## Descubrimiento automatizado

La mayoría de escáneres de vulnerabilidades web (Nessus, Burp Pro, ZAP) incorporan detección de los tres tipos de XSS, combinando dos enfoques:

- **Análisis pasivo**: revisa el código del lado del cliente buscando patrones de riesgo (sinks peligrosos sin sanitización aparente), sin enviar peticiones adicionales.
- **Análisis activo**: envía sistemáticamente payloads de prueba e inspecciona las respuestas para confirmar inyección exitosa.

### Herramientas open source dedicadas

| Herramienta | Notas |
|---|---|
| [XSStrike](https://github.com/s0md3v/XSStrike) | Genera payloads de forma inteligente según cómo se refleja la entrada |
| [BruteXSS](https://github.com/rajeshmajumdar/BruteXSS) | Enfoque por fuerza bruta con listas de payloads |
| [XSSer](https://github.com/epsylon/xsser) | Framework dedicado con múltiples técnicas de evasión |

```bash
git clone https://github.com/s0md3v/XSStrike.git
cd XSStrike
pip install -r requirements.txt

python xsstrike.py -u "http://10.10.10.5/index.php?task=test"
```

```
[!] Testing parameter: task
[!] Reflections found: 1
[+] Payload: <HtMl%09onPoIntERENTER+=+confirm()>
[!] Efficiency: 100
[!] Confidence: 10
```

> **Importante**: ninguna herramienta automatizada es infalible. Pueden producirse falsos negativos (la herramienta no marca algo que sí es vulnerable, por ejemplo por una codificación inusual) y falsos positivos. La verificación manual del hallazgo —confirmando realmente que el payload se ejecuta— sigue siendo imprescindible, exactamente el mismo principio visto en el bloque de *Web Fuzzing* al hablar de validación responsable de hallazgos.

## Descubrimiento manual

### Probar payloads conocidos

Listas extensas de payloads XSS están disponibles públicamente, como las de [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XSS%20Injection/README.md) o [Payload-Box](https://github.com/payload-box/xss-payload-list). La estrategia básica: probar payloads uno a uno en cada campo de entrada, observando si se dispara una alerta.

> **XSS no se limita a campos de formulario visibles.** También puede inyectarse a través de cabeceras HTTP que la aplicación refleja de alguna forma — `Cookie`, `User-Agent`, `Referer` son vectores habituales que se pasan por alto si solo se prueban los campos visibles de la interfaz.

### Por qué la mayoría de payloads "de lista" fallarán a la primera

Cada payload está diseñado para un **contexto de inyección específico**: dentro de un atributo HTML, después de cerrar una comilla simple, dentro de una etiqueta `<script>`, dentro de un atributo de estilo CSS. Si el contexto real no coincide con el que el payload espera, simplemente no funcionará — sin que eso signifique necesariamente que la aplicación no es vulnerable, solo que hace falta el payload adaptado a *ese* contexto concreto.

Por eso, copiar y pegar payloads de una lista genérica sin entender el contexto de inyección es ineficiente. Un enfoque más metódico —y el que realmente escala bien— es **observar cómo se refleja la entrada** en el código fuente tras enviarla, y construir el payload específicamente adaptado a ese contexto.

## Revisión de código: el método más fiable

La forma más confiable de encontrar XSS —especialmente en aplicaciones que ya filtran los payloads más obvios— es la **revisión manual de código**, tanto frontend como backend. Entender con precisión cómo se procesa la entrada del usuario hasta llegar al navegador permite construir un payload altamente fiable, en lugar de probar a ciegas.

Esto es exactamente lo que se hizo en el apartado anterior con el análisis de **source y sink** en XSS basado en DOM: leyendo el JavaScript directamente, se puede confirmar la vulnerabilidad (y construir el payload exacto necesario) sin necesidad de prueba y error.

## Por qué las aplicaciones "maduras" rara vez caen ante listas de payloads genéricas

Las aplicaciones bien establecidas suelen haber pasado por escáneres de seguridad automatizados durante su desarrollo, corrigiendo los problemas más obvios antes del lanzamiento. Encontrar XSS en ese tipo de aplicaciones casi siempre requiere revisión de código manual, comprensión de la lógica de sanitización específica implementada, y construcción de payloads a medida — exactamente las habilidades avanzadas que se mencionan al final de este bloque como siguiente paso de profundización.
