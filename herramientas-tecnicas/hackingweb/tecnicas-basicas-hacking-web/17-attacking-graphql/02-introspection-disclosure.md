# Introspección y divulgación de información

## Qué es la introspección

**Introspección** es una característica nativa de GraphQL que permite consultar la propia API sobre su estructura — qué tipos existen, qué campos tienen, qué consultas y mutaciones están disponibles, y qué argumentos acepta cada una. Es, esencialmente, documentación autodescriptiva en tiempo real.

Para un desarrollador, es una herramienta conveniente. Para un auditor, es potencialmente la fuente de información más completa disponible sobre la superficie de ataque de la API — y si está habilitada en producción sin restricciones, un atacante puede mapear toda la estructura de datos disponible antes de intentar ninguna explotación.

## Fingerprinting del motor GraphQL

Antes de explotar nada, identificar el motor concreto ayuda a conocer sus comportamientos y posibles particularidades:

```bash
# graphw00f — fingerprinting del motor GraphQL
git clone https://github.com/dolevf/graphw00f.git
python3 main.py -d -f -t http://objetivo.com

# Resultado típico:
# [*] Discovered GraphQL Engine: (Graphene)
# [!] Attack Surface Matrix: https://github.com/nicholasaleks/graphql-threat-matrix/...
```

La [GraphQL Threat Matrix](https://github.com/nicholasaleks/graphql-threat-matrix) mantiene un catálogo de qué vulnerabilidades son más probables según el motor identificado — el mismo principio de "fingerprinting orienta el ataque" trabajado en el bloque de *Information Gathering*.

## Consultas de introspección básicas

### Listar todos los tipos del esquema

```graphql
{
  __schema {
    types {
      name
    }
  }
}
```

Los resultados incluyen tipos básicos (`Int`, `Boolean`, `String`) pero también todos los tipos personalizados definidos por la aplicación (`UserObject`, `ProductObject`, etc.) — el inventario completo de objetos de datos.

### Explorar los campos de un tipo específico

```graphql
{
  __type(name: "UserObject") {
    name
    fields {
      name
      type {
        name
      }
    }
  }
}
```

Esto revela todos los campos disponibles en ese tipo — incluyendo campos sensibles como `password`, `token`, o `apiKey` que no deberían ser accesibles.

### Introspección completa del esquema

```graphql
{
  __schema {
    queryType { name }
    mutationType { name }
    types {
      name
      kind
      fields {
        name
        args { name type { name } }
        type { name }
      }
    }
  }
}
```

Esta consulta devuelve el esquema completo de la API en un solo resultado — equivalente a tener la documentación completa de todos los endpoints, sus parámetros y tipos de retorno.

## Por qué la introspección habilitada en producción es un riesgo

La comparación directa: la introspección habilitada en una API GraphQL de producción es análoga a un servidor web con listado de directorio activo — no es en sí misma la vulnerabilidad, pero elimina completamente la fricción de reconocimiento para un atacante. En lugar de semanas de fuzzing manual para descubrir qué endpoints existen y qué parámetros aceptan, un atacante con acceso a introspección tiene ese mapa en segundos.

La guía de OWASP para GraphQL recomienda explícitamente **deshabilitar la introspección en entornos de producción** — si la documentación interna la necesita, exponerla solo en entornos de desarrollo o detrás de autenticación adicional.

## Herramienta: GraphiQL

Muchas implementaciones de GraphQL exponen por defecto la interfaz web **GraphiQL** — un explorador interactivo de consultas que además incluye autocompletado basado en el esquema. Si está accesible sin autenticación, es una señal directa de que la introspección está habilitada y el entorno no está endurecido para producción.

## Mitigación

- **Deshabilitar introspección en producción**: la mayoría de motores GraphQL incluyen una opción de configuración para esto.
- Si la introspección es necesaria por alguna razón: autenticarla y asegurarse de que no expone campos sensibles.
- **Mensajes de error genéricos**: los errores detallados del motor pueden revelar información del esquema incluso sin introspección explícita — el mismo principio de "no exponer errores internos" repetido en cada bloque de este temario.
