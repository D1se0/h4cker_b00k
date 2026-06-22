# Herramientas para auditar GraphQL

## graphw00f — fingerprinting del motor

Identifica qué motor GraphQL usa la aplicación observando el comportamiento ante consultas malformadas y errores:

```bash
git clone https://github.com/dolevf/graphw00f.git
python3 main.py -d -f -t http://objetivo.com
```

Conecta con la [GraphQL Threat Matrix](https://github.com/nicholasaleks/graphql-threat-matrix) para identificar qué vectores son más relevantes según el motor detectado.

## GraphQL Voyager — visualización del esquema

Convierte la respuesta de introspección en un grafo visual de las relaciones entre tipos. Especialmente útil para identificar ciclos (candidatos para ataques DoS) y campos sensibles que no deberían ser accesibles:

```
https://graphql-kit.com/graphql-voyager/
```

Se puede pegar directamente la respuesta JSON de la consulta de introspección completa.

## GraphiQL — interfaz web interactiva

Si la aplicación expone la interfaz GraphiQL sin autenticación, es el explorador más cómodo para pruebas interactivas: autocompletado basado en el esquema, historial de consultas, y visualización de respuestas formateadas.

La presencia de GraphiQL sin autenticación en producción es en sí misma un hallazgo reportable — indica que la introspección está habilitada y que el entorno no está endurecido para producción.

## InQL — extensión de Burp Suite

Plugin de Burp que automatiza la introspección y presenta el esquema de forma navegable directamente dentro de Burp, facilitando probar cada query y mutación desde el propio proxy de intercepción.

## Consultas de introspección manuales en cualquier cliente HTTP

Para entornos donde no hay acceso a las herramientas anteriores, las consultas de introspección se pueden enviar con curl o cualquier cliente HTTP que soporte POST JSON:

```bash
curl -X POST http://objetivo/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __schema { types { name } } }"}'
```

El resultado en JSON es procesable directamente con `jq` para extraer nombres de tipos, campos, y argumentos.

## Resumen de cuándo usar cada herramienta

| Necesidad | Herramienta |
|---|---|
| Identificar el motor y sus particularidades | graphw00f |
| Visualizar relaciones del esquema y detectar ciclos | GraphQL Voyager |
| Exploración interactiva si está disponible | GraphiQL |
| Pruebas integradas con el flujo de proxy | InQL (Burp) |
| Entornos con acceso solo a línea de comandos | curl + jq |
