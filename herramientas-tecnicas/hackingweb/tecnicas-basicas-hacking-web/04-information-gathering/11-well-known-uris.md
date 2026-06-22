# URIs .well-known

## Qué es el estándar `.well-known`

Definido en el [RFC 8615](https://datatracker.ietf.org/doc/html/rfc8615), `.well-known` es un directorio estandarizado en la raíz de cualquier dominio (`ejemplo.com/.well-known/`) pensado para centralizar metadatos y archivos de configuración relacionados con servicios, protocolos y mecanismos de seguridad del sitio. Al fijar una ubicación predecible y consistente, navegadores, herramientas y clientes automáticos pueden localizar esta información sin necesidad de configuración adicional — simplemente construyendo la URL esperada.

La [IANA mantiene un registro oficial](https://www.iana.org/assignments/well-known-uris/well-known-uris.xhtml) de sufijos `.well-known` reconocidos, cada uno definido por una especificación concreta. Algunos ejemplos relevantes:

| Sufijo | Propósito |
|---|---|
| `security.txt` | Información de contacto para reportar vulnerabilidades de seguridad responsablemente |
| `change-password` | URL estándar para dirigir a un usuario a la página de cambio de contraseña |
| `openid-configuration` | Metadatos de configuración de un proveedor OpenID Connect |
| `assetlinks.json` | Verificación de propiedad de activos digitales (apps) asociados a un dominio |
| `mta-sts.txt` | Política de seguridad de transporte para correo (MTA-STS) |

## Por qué importa en reconocimiento: el caso de `openid-configuration`

El endpoint `/.well-known/openid-configuration` es particularmente valioso cuando una aplicación implementa **OpenID Connect** (capa de identidad sobre OAuth 2.0). Visitarlo directamente —sin necesidad de autenticación ni interacción previa— devuelve un documento JSON con metadatos completos del proveedor de identidad:

```json
{
  "issuer": "https://ejemplo.com",
  "authorization_endpoint": "https://ejemplo.com/oauth2/authorize",
  "token_endpoint": "https://ejemplo.com/oauth2/token",
  "userinfo_endpoint": "https://ejemplo.com/oauth2/userinfo",
  "jwks_uri": "https://ejemplo.com/oauth2/jwks",
  "response_types_supported": ["code", "token", "id_token"],
  "id_token_signing_alg_values_supported": ["RS256"]
}
```

De un único endpoint sin protección se obtiene:

- **Mapeo directo de endpoints OAuth/OIDC**: dónde se autoriza, dónde se emiten tokens, dónde se consulta la información del usuario — sin necesidad de adivinar ni hacer fuzzing de rutas.
- **JWKS URI**: la ubicación de las claves criptográficas públicas usadas para verificar tokens, relevante en pruebas relacionadas con manipulación de JWT.
- **Algoritmos soportados**: información directamente relevante para evaluar la robustez criptográfica de la implementación (por ejemplo, si se permite el algoritmo `none`, una debilidad bien conocida en implementaciones JWT mal configuradas).
- **Scopes soportados**: qué niveles de acceso contempla la aplicación, útil para entender el modelo de permisos.

## Otras URIs `.well-known` con valor ofensivo

- **`security.txt`**: aunque pensado como canal legítimo de divulgación responsable, confirma indirectamente que la organización tiene (o no) un programa de seguridad activo, y a veces revela el alcance de su programa de *bug bounty* — relevante para el bloque de *Bug Bounty Hunting Process*.
- **`change-password`**: confirma de forma directa la URL exacta del flujo de cambio de contraseña, ahorrando tiempo de reconocimiento manual al auditar mecanismos de autenticación (bloque de *Broken Authentication*).

## Cómo explorarlo sistemáticamente

No hace falta memorizar todo el registro IANA: la estrategia más práctica es automatizar la comprobación de los sufijos más comunes contra cualquier objetivo nuevo, y revisar puntualmente el [registro completo de la IANA](https://www.iana.org/assignments/well-known-uris/well-known-uris.xhtml) cuando se sospeche que una aplicación implementa un protocolo o estándar específico (OAuth, ACME, seguridad de correo) que pudiera tener su propia entrada `.well-known` dedicada.

```bash
for path in security.txt openid-configuration assetlinks.json change-password mta-sts.txt; do
  curl -s -o /dev/null -w "%{http_code} /.well-known/$path\n" "https://ejemplo.com/.well-known/$path"
done
```

Este tipo de comprobación rápida, de coste prácticamente nulo, debería formar parte del checklist estándar de reconocimiento de cualquier aplicación nueva.
