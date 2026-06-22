# Registros de Transparencia de Certificados (CT logs)

## El problema que resuelven

El sistema de certificados SSL/TLS depende de que las Autoridades de Certificación (CA) verifiquen correctamente la identidad antes de emitir un certificado. Cuando ese proceso falla —por error o por compromiso— pueden emitirse certificados fraudulentos capaces de suplantar sitios legítimos. Los registros de **Certificate Transparency (CT)** existen para hacer ese proceso de emisión públicamente auditable: cada certificado emitido por una CA debe registrarse en uno o varios "libros de contabilidad" públicos, de solo escritura, mantenidos por organizaciones independientes.

## Por qué importan en reconocimiento (más allá de la seguridad de certificados)

Para un pentester, los CT logs son, sobre todo, una **fuente pasiva extraordinariamente eficaz de enumeración de subdominios**. La razón es estructural: cuando se emite un certificado SSL/TLS para un dominio (incluyendo certificados comodín, que cubren múltiples subdominios), el campo **SAN (Subject Alternative Name)** del certificado suele listar explícitamente todos los nombres de host que cubre. Esa información queda registrada permanentemente en los logs de CT, de acceso público, en cuanto se emite el certificado.

Esto ofrece una ventaja decisiva frente a la fuerza bruta tradicional: **no depende de adivinar nombres**. Se obtiene un registro definitivo y muchas veces histórico de subdominios reales que han tenido un certificado emitido alguna vez — incluyendo subdominios que ya no están en uso activo pero que podrían seguir siendo accesibles, ejecutando software obsoleto y potencialmente vulnerable.

## Cómo funciona (resumen técnico)

1. Un sitio solicita un certificado a una CA.
2. La CA emite un **pre-certificado** y lo envía a varios registros CT independientes.
3. Cada registro genera un **Signed Certificate Timestamp (SCT)**, prueba criptográfica de que el certificado fue enviado en un momento dado, que se incorpora al certificado final.
4. Los navegadores verifican estos SCTs al establecer la conexión, contrastándolos contra los registros públicos.
5. Los registros son monitorizados continuamente por investigadores y proveedores de navegadores, en busca de certificados fraudulentos o anómalos.

La integridad del registro se garantiza mediante una estructura criptográfica de **árbol de Merkle**: cada certificado es una hoja del árbol, cada nodo intermedio es el hash de sus hijos, y la raíz (*root hash*) representa el estado completo del registro. Cualquier alteración, por mínima que sea, en cualquier certificado del histórico cambiaría el hash raíz, delatando inmediatamente la manipulación — lo que hace de los CT logs una fuente de información extremadamente fiable e inmutable.

## Herramientas para consultar CT logs

| Herramienta | Características |
|---|---|
| [crt.sh](https://crt.sh/) | Interfaz web sencilla, búsqueda directa por dominio, API JSON gratuita |
| [Censys](https://search.censys.io/) | Más potente y con filtrado avanzado, requiere registro (con plan gratuito) |

### Consulta vía API con `curl` y `jq`

```bash
curl -s "https://crt.sh/?q=ejemplo.com&output=json" | jq -r '.[] | .name_value' | sort -u
```

Filtrando además por un patrón concreto (por ejemplo, subdominios de desarrollo):

```bash
curl -s "https://crt.sh/?q=ejemplo.com&output=json" \
  | jq -r '.[] | select(.name_value | contains("dev")) | .name_value' \
  | sort -u

*.dev.ejemplo.com
dev.ejemplo.com
secure.dev.ejemplo.com
```

## Ventajas frente a otros métodos de enumeración de subdominios

- **No requiere wordlist**: revela subdominios reales, no candidatos adivinados — incluyendo nombres que ninguna wordlist genérica contendría.
- **Cobertura histórica**: certificados antiguos o caducados pueden seguir apuntando a subdominios olvidados, candidatos perfectos a presentar configuraciones desactualizadas o vulnerabilidades sin parchear.
- **Reconocimiento puramente pasivo**: no se interactúa en ningún momento con la infraestructura DNS o web del objetivo; toda la consulta se dirige a terceros (crt.sh, Censys), por lo que el riesgo de detección es prácticamente nulo.

## Flujo de trabajo recomendado

1. Consultar crt.sh (o Censys) para el dominio objetivo y extraer todos los `name_value` únicos.
2. Filtrar y limpiar duplicados, comodines (`*.ejemplo.com`) y ruido evidente.
3. Cruzar esta lista con los resultados de fuerza bruta DNS y virtual host fuzzing vistos en apartados anteriores, para construir un inventario consolidado de subdominios.
4. Validar cada candidato (resolución DNS + accesibilidad HTTP) antes de invertir tiempo de auditoría en él.
