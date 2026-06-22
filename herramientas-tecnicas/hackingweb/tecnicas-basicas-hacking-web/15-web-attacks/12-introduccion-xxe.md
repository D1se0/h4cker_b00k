# Introducción a XXE

## Qué es XML

**XML (Extensible Markup Language)** es un lenguaje de marcado diseñado para almacenar y transportar datos de forma estructurada. A diferencia de HTML (que describe cómo mostrar datos), XML describe los datos en sí. Su estructura es un árbol de elementos etiquetados:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<email>
  <date>01-01-2024</date>
  <sender>usuario@ejemplo.com</sender>
  <body>Contenido del mensaje</body>
</email>
```

### Componentes esenciales

| Componente | Descripción | Ejemplo |
|---|---|---|
| Tag | Etiqueta que delimita un elemento | `<date>` |
| Entity | Variable XML (`&nombre;`) | `&lt;` representa `<` |
| Element | Nodo del árbol con su valor | `<date>01-01-2024</date>` |
| Attribute | Propiedad de un elemento | `version="1.0"` |
| Declaration | Primera línea con metadatos | `<?xml version="1.0"?>` |

## XML DTD y entidades externas

Un **DTD (Document Type Definition)** define la estructura válida de un documento XML. Puede estar embebido en el propio documento o referenciarse desde un archivo externo:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE email SYSTEM "email.dtd">
```

Dentro de un DTD se pueden declarar **entidades** — esencialmente variables que el parser XML sustituye al procesar el documento:

```xml
<!DOCTYPE email [
  <!ENTITY company "InlaneFreight">
]>
<email>
  <from>&company;</from>
</email>
<!-- El parser sustituye &company; por "InlaneFreight" -->
```

### Entidades externas: la fuente de la vulnerabilidad

La especificación XML permite que una entidad apunte a un recurso **externo** mediante la palabra clave `SYSTEM`:

```xml
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<data><value>&xxe;</value></data>
```

Si el parser XML procesa esta entidad con entidades externas habilitadas, sustituirá `&xxe;` por el contenido del archivo `/etc/passwd` del servidor. Esto es la base de la **inyección XXE**.

## Por qué XXE ocurre

El parser XML procesa el documento de entrada con entidades externas habilitadas de forma predeterminada en muchas librerías antiguas (o mal configuradas). Cuando la aplicación acepta XML del usuario y lo procesa con un parser vulnerable, ese XML puede contener una declaración DTD maliciosa que apunte a recursos locales del servidor, produciendo su divulgación en la respuesta.

## El impacto potencial

| Tipo de XXE | Qué puede lograr |
|---|---|
| Lectura de archivos locales | Extraer `/etc/passwd`, archivos de configuración, código fuente |
| SSRF vía XXE | Forzar al servidor a realizar peticiones HTTP hacia servicios internos (mismo impacto que SSRF, visto en *Server-side Attacks*) |
| Exfiltración ciega | Filtrar datos a través de DNS o peticiones externas cuando la respuesta no muestra el contenido directamente |
| DoS (Billion Laughs) | Crear entidades anidadas que expanden exponencialmente el consumo de memoria del parser |

## Reconociendo la superficie de ataque

XXE afecta a cualquier funcionalidad de la aplicación que **acepte y procese XML** del usuario:

- APIs tipo SOAP (basadas en XML — mencionadas en el bloque de *Web Requests*)
- Funcionalidad de importación/carga de documentos (SVG, DOCX, XLSX, que internamente son XML)
- Formularios que envían datos en formato XML
- APIs REST que aceptan `Content-Type: application/xml`

La señal de alarma durante el reconocimiento: cualquier petición cuyo cuerpo sea XML estructurado, o cualquier funcionalidad de carga de archivos que acepte formatos basados en XML (SVG es el caso más habitual, ya tratado en el bloque de *File Upload Attacks*).
