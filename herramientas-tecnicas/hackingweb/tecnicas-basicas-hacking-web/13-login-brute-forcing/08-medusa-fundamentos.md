# Medusa: fundamentos

## Qué es y cómo se relaciona con Hydra

**Medusa** es, junto a Hydra, una de las herramientas de referencia para fuerza bruta de credenciales en pentesting — rápida, modular, y con soporte para múltiples hilos en paralelo. Funcionalmente cumple un papel muy similar a Hydra (visto en los apartados anteriores de este bloque); la diferencia práctica está sobre todo en la sintaxis y en algunos matices de diseño interno. Conocer ambas herramientas es útil porque, en la práctica, cada una puede comportarse mejor que la otra ante peticiones especialmente atípicas — disponer de una alternativa es valioso cuando una de las dos no termina de ajustarse bien a un escenario concreto.

```bash
sudo apt-get update && sudo apt-get install medusa
medusa -h
```

## Sintaxis general

```bash
medusa [opciones_objetivo] [opciones_credenciales] -M módulo [opciones_módulo]
```

| Parámetro | Función |
|---|---|
| `-h HOST` / `-H archivo` | Un único objetivo, o un archivo con lista de objetivos |
| `-u USER` / `-U archivo` | Un único usuario, o un archivo con lista de usuarios |
| `-p PASS` / `-P archivo` | Una única contraseña, o un archivo con lista de contraseñas |
| `-M módulo` | Módulo de protocolo a usar (`http`, `ssh`, `ftp`, etc.) |
| `-m "opción"` | Opciones específicas del módulo elegido |
| `-t TASKS` | Número de intentos paralelos |
| `-f` / `-F` | Detener al primer éxito (en el host actual / en cualquier host) |
| `-n PUERTO` | Puerto no estándar |
| `-v NIVEL` | Verbosidad (hasta 6) |

## Ejemplo de uso básico

```bash
medusa -h 10.10.10.5 -U usuarios.txt -P contraseñas.txt -M ssh
```

Medusa probará sistemáticamente cada combinación de la lista de usuarios contra cada contraseña de la lista, exactamente con la misma lógica de fondo vista en Hydra.

## Atacando múltiples objetivos con autenticación HTTP básica

```bash
medusa -H servidores.txt -U usuarios.txt -P contraseñas.txt -M http -m GET
```

Igual que con Hydra, esto resulta especialmente útil para confirmar de forma eficiente si una credencial débil o por defecto se reutiliza en varios sistemas de un mismo entorno (el mismo escenario visto en el apartado de fundamentos de este bloque).

## Catálogo de módulos disponibles

Medusa incluye módulos para una amplia variedad de protocolos de red habituales en entornos corporativos: servicios de transferencia de archivos, acceso remoto, correo electrónico, bases de datos, control de versiones, y por supuesto, HTTP — el módulo que más interesa en el contexto de este temario, desarrollado con detalle en el siguiente apartado dedicado específicamente a servicios web.

## Cuándo preferir Medusa frente a Hydra

No hay una regla universal — ambas herramientas son comparables en capacidad. En la práctica, suele depender de:

- **Familiaridad con la sintaxis concreta** de cada una, que en algunos escenarios resulta más intuitiva de ajustar que la otra.
- **Comportamiento ante el servicio objetivo concreto**: algunos servicios responden de forma más predecible a una herramienta que a la otra, por pequeñas diferencias en cómo cada una construye y envía las peticiones.
- **Disponibilidad de documentación o ejemplos previos** para el protocolo concreto que se está auditando.

Dominar ambas, en lugar de depender exclusivamente de una, es la recomendación práctica habitual — exactamente el mismo principio de "tener alternativas disponibles" aplicado ya en el bloque de *Web Fuzzing* al comparar `ffuf`, Gobuster y FeroxBuster.
