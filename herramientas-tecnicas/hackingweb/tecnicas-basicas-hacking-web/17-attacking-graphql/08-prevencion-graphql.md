# Prevención de vulnerabilidades GraphQL

## El mismo principio de siempre, aplicado al contexto GraphQL

Las vulnerabilidades de GraphQL no son categorías nuevas — son IDOR, inyección SQL, XSS, y DoS aplicados a un contexto de API con características propias. La prevención sigue las mismas líneas que en los bloques correspondientes de este temario, con ajustes específicos para las particularidades de GraphQL.

## Prevención de divulgación de información

### Deshabilitar la introspección en producción

La introspección es útil en desarrollo, innecesaria en producción, y peligrosa si está sin restricciones:

```javascript
// Ejemplo en Apollo Server (Node.js)
const server = new ApolloServer({
  typeDefs,
  resolvers,
  introspection: process.env.NODE_ENV !== 'production'
});
```

Si la introspección es requerida internamente, protegerla con autenticación adicional.

### Mensajes de error genéricos

Los errores del motor GraphQL no deben exponer detalles del esquema, consultas SQL, o trazas de error internas — la misma recomendación de "no exponer errores detallados en producción" trabajada en cada bloque de este temario.

## Prevención de inyección

Los argumentos de las queries y mutaciones GraphQL deben tratarse exactamente igual que cualquier entrada de usuario en una aplicación web convencional:

- Consultas SQL parametrizadas/preparadas — nunca concatenar el argumento directamente.
- Validación del tipo de argumento (GraphQL lo facilita, pero no es suficiente solo con la comprobación de tipo).
- Sanitización de salida para campos que se renderizan como HTML.

## Prevención de DoS

### Limitar la profundidad de consulta

Establecer una profundidad máxima que el motor aceptará, rechazando consultas que la superen:

```javascript
// graphql-depth-limit (Node.js)
const depthLimit = require('graphql-depth-limit');
app.use('/graphql', graphqlHTTP({
  validationRules: [depthLimit(5)]
}));
```

### Limitar la complejidad de consulta

Asignar un "coste" a cada campo y rechazar consultas cuyo coste total supere un umbral configurable.

### Rate limiting a nivel de operación

Si se permite batching, el límite de tasa debe aplicarse por operación individual dentro del batch, no solo por petición HTTP — de lo contrario, el rate limiting es trivialmente evitable como se vio en el apartado de DoS y batching.

### Deshabilitar el batching si no es necesario

Si la aplicación no requiere enviar múltiples consultas en una sola petición, deshabilitar esta capacidad elimina el vector de amplificación de fuerza bruta.

## Prevención de IDOR y control de acceso deficiente

El mismo RBAC (Role-Based Access Control) visto en el bloque de *Web Attacks* se aplica aquí:

- El endpoint GraphQL no debería ser accesible sin autenticación salvo que sea una API pública explícita.
- Cada resolver (la función que procesa cada query o mutación) debe verificar que el usuario autenticado tiene permiso sobre el objeto concreto solicitado.
- Los campos sensibles (`password`, `apiKey`, etc.) no deberían estar en el esquema accesible por usuarios sin privilegios elevados, o deben tener sus propios controles de acceso a nivel de campo.

## Referencia

La [Guía rápida de GraphQL de OWASP](https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html) cubre estas medidas con mayor detalle técnico específico por motor y plataforma.

## Cierre del bloque de Attacking GraphQL

GraphQL concentra la superficie de ataque de una API completa en un único endpoint con capacidades muy ricas. Esta concentración hace que las consecuencias de una configuración incorrecta sean potencialmente mayores que en REST — pero también hace que el proceso de auditoría sea más sistemático: introspección primero, luego verificar IDOR, inyección, y límites de complejidad. El siguiente bloque, *API Attacks*, amplía este análisis al conjunto más amplio de APIs REST y otros estilos de API, completando el panorama de seguridad de interfaces de programación de aplicaciones.
