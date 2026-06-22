# Enumeración de subdominios

## Por qué los subdominios importan tanto

Bajo el dominio principal de cualquier organización suele esconderse toda una red de subdominios: `blog.ejemplo.com`, `shop.ejemplo.com`, `mail.ejemplo.com`. Muchos de ellos no están enlazados desde el sitio principal y, precisamente por eso, suelen recibir menos atención (y menos parches) que la aplicación "de cara al público":

- **Entornos de desarrollo/staging**: protección más débil mientras se prueban nuevas funcionalidades, a veces con datos reales y deuda de seguridad acumulada.
- **Portales de login ocultos**: paneles administrativos que no deberían ser públicamente conocidos, pero que igualmente responden si se conoce (o se adivina) la URL exacta.
- **Aplicaciones heredadas (legacy)**: software antiguo, olvidado, ejecutando versiones con vulnerabilidades públicas conocidas.
- **Información sensible expuesta**: documentos internos, datos de configuración, accesibles por simple descuido.

## Dos enfoques: activo y pasivo

### Enumeración activa

Interactúa directamente con la infraestructura DNS del objetivo. La técnica más habitual es la **fuerza bruta**: probar sistemáticamente una lista de nombres de subdominio plausibles contra el dominio raíz, comprobando cuáles resuelven a una IP válida.

El proceso, en cuatro pasos:

1. **Selección de wordlist**: genérica (`dev`, `staging`, `admin`, `test`...), dirigida (basada en patrones conocidos del sector u organización), o personalizada (construida a partir de información ya recopilada).
2. **Iteración**: cada palabra se combina con el dominio base (`dev.ejemplo.com`, `staging.ejemplo.com`...).
3. **Consulta DNS**: se comprueba si cada candidato resuelve (normalmente vía registro `A`/`AAAA`).
4. **Filtrado y validación**: los que resuelven correctamente se listan como subdominios válidos, idealmente confirmando además su accesibilidad real (por ejemplo, vía HTTP).

```bash
dnsenum --enum ejemplo.com -f /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt -r
```

- `--enum`: atajo con opciones de ajuste predefinidas.
- `-f`: ruta a la wordlist.
- `-r`: habilita fuerza bruta **recursiva** — si se encuentra un subdominio, también se intenta enumerar sus propios subdominios.

Otras herramientas equivalentes incluyen `fierce`, `dnsrecon`, `amass`, `assetfinder` y `puredns`, cada una con matices propios (detección de comodines, integración con múltiples fuentes de datos, velocidad de resolución).

### Enumeración pasiva

No interactúa directamente con el DNS del objetivo, sino que se apoya en fuentes externas:

- **Registros de Transparencia de Certificados (CT logs)**: revelan subdominios que han tenido certificados SSL/TLS emitidos, incluso si ya no están en uso activo (se trata en detalle en su propio apartado).
- **Motores de búsqueda**: usando operadores como `site:` para filtrar resultados a un dominio concreto.
- **Bases de datos y agregadores en línea**: servicios que ya han recopilado datos DNS de múltiples fuentes, permitiendo consultar sin generar tráfico directo contra el objetivo.

## Comparativa de enfoques

| Aspecto | Activo (fuerza bruta) | Pasivo (CT logs, motores de búsqueda) |
|---|---|---|
| Cobertura | Limitada a lo que contiene la wordlist | Puede revelar subdominios no adivinables |
| Sigilo | Genera tráfico DNS directo, detectable | Prácticamente indetectable |
| Datos históricos | No | Sí (certificados antiguos, snapshots) |
| Velocidad | Depende del tamaño de la wordlist | Generalmente instantáneo |

La estrategia más efectiva combina ambos: empezar por fuentes pasivas para obtener una base sin coste de sigilo, y completar después con fuerza bruta dirigida (idealmente con una wordlist enriquecida con los patrones de nomenclatura ya observados en los subdominios descubiertos pasivamente).

## Ejemplo de fuerza bruta con `ffuf`

Aunque `dnsenum` resuelve directamente vía DNS, también es habitual hacer fuzzing de subdominios a nivel HTTP manipulando la cabecera `Host`:

```bash
ffuf -c -w subdomains-top1million-20000.txt -u http://ejemplo.com -H "Host: FUZZ.ejemplo.com" -fw 1
```

Esta variante es especialmente útil cuando interesa confirmar no solo que el subdominio resuelve en DNS, sino que el servidor web responde realmente con contenido distinto para ese host concreto — relevante para el siguiente apartado sobre *virtual hosts*.

## Validación tras el descubrimiento

Encontrar que un subdominio resuelve no es el final del proceso: conviene visitarlo (o consultarlo con `curl`) para confirmar que está realmente activo, qué contenido sirve, y si presenta indicios de ser un entorno de menor seguridad (mensajes de depuración, ausencia de autenticación, versiones distintas del software de producción).
