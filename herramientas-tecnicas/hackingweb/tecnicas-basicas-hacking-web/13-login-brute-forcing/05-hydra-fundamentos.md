# Hydra: fundamentos y sintaxis

## Qué es

**Hydra** es una herramienta de fuerza bruta de red, rápida y ampliamente usada en pentesting, capaz de atacar un gran número de protocolos de autenticación distintos. Viene preinstalada en la mayoría de distribuciones orientadas a pentesting (Kali, Parrot, PwnBox).

```bash
sudo apt-get update && sudo apt-get install hydra
hydra -h
```

## Por qué es tan usada

- **Velocidad**: realiza intentos en paralelo mediante múltiples hilos, acelerando drásticamente el proceso frente a probar credenciales una a una manualmente.
- **Flexibilidad**: soporta un catálogo amplio de protocolos mediante módulos específicos por servicio.
- **Sintaxis consistente**: una vez aprendida la estructura básica, se aplica de forma similar independientemente del protocolo objetivo.

## Sintaxis general

```bash
hydra [opciones_login] [opciones_password] [opciones_ataque] [opciones_servicio]
```

| Parámetro | Función |
|---|---|
| `-l LOGIN` / `-L archivo` | Un único usuario, o un archivo con lista de usuarios |
| `-p PASS` / `-P archivo` | Una única contraseña, o un archivo con lista de contraseñas |
| `-t TASKS` | Número de hilos paralelos |
| `-f` | Detiene el ataque al primer éxito |
| `-s PUERTO` | Puerto no estándar del servicio objetivo |
| `-v` / `-V` | Salida detallada (verbose) |
| `servicio://servidor` | Protocolo y objetivo |

## Ejemplo de uso básico

```bash
hydra -L usuarios.txt -P contraseñas.txt servicio://10.10.10.5
```

Hydra prueba sistemáticamente cada combinación de la lista de usuarios contra cada contraseña de la lista, deteniéndose (si se usa `-f`) en cuanto encuentra una combinación válida.

## Atacando múltiples objetivos a la vez

Cuando se dispone de una lista de direcciones potencialmente vulnerables (por ejemplo, tras un reconocimiento de red autorizado) y se sospecha de una credencial débil concreta:

```bash
hydra -l admin -p admin -M objetivos.txt servicio
```

`-M` apunta a un archivo con múltiples hosts objetivo, probando la misma combinación usuario/contraseña en paralelo contra todos ellos — útil para confirmar de forma eficiente si una credencial por defecto conocida (vista en el apartado de fundamentos de este bloque) se reutiliza en varios sistemas de un mismo entorno.

## Ajustando puerto y verbosidad

```bash
hydra -L usuarios.txt -P contraseñas.txt -s 2121 -V servidor.htb servicio
```

`-s` indica un puerto no estándar; `-V` aumenta el detalle de la salida, mostrando cada intento individual a medida que se realiza — útil para confirmar visualmente que el ataque progresa como se espera, y para depurar si algo no funciona como debería.

## El catálogo de servicios soportados

Hydra incluye módulos para una amplia variedad de protocolos de red comunes en entornos corporativos: servicios de transferencia de archivos, acceso remoto, correo electrónico, bases de datos, escritorio remoto, y por supuesto, formularios web — el caso de uso que más interesa en el contexto de este temario, y que se desarrolla en detalle en los siguientes dos apartados: autenticación HTTP básica y formularios de login personalizados.

## Por qué el reconocimiento previo sigue siendo imprescindible

Antes de lanzar cualquier ataque con Hydra, todo lo trabajado en los apartados anteriores de este bloque sigue aplicando con la misma importancia: identificar primero si existen credenciales por defecto conocidas, construir una wordlist orientada al objetivo concreto (en lugar de una genérica), y entender la política de contraseñas si es conocida. Hydra automatiza la **ejecución** del ataque, pero la **estrategia** —qué combinaciones probar y en qué orden de prioridad— sigue dependiendo del trabajo de reconocimiento previo.
