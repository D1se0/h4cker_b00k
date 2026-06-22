# Prevención de la manipulación de verbos HTTP

## El principio rector: cubrir todos los verbos, no solo los esperados

La vulnerabilidad nace siempre de la misma lógica incompleta: especificar explícitamente qué verbos están protegidos (lista blanca de verbos en el control de seguridad) deja automáticamente todos los demás verbos sin esa protección. La solución estructural es invertir esa lógica.

## Configuración segura en servidores web

### Apache

**Vulnerable** — solo cubre GET y POST:

```xml
<Limit GET POST>
    Require valid-user
</Limit>
```

**Correcto** — cubre todos los verbos excepto los explícitamente permitidos:

```xml
<LimitExcept GET POST>
    Require valid-user
</LimitExcept>
```

`LimitExcept` aplica la restricción a **todos los verbos** que no estén en la lista — es decir, si un verbo no está explícitamente exceptuado, queda cubierto. El comportamiento opuesto y más seguro frente a `Limit`.

También es recomendable deshabilitar `HEAD` explícitamente si la aplicación no lo necesita:

```xml
RewriteEngine On
RewriteCond %{REQUEST_METHOD} ^HEAD
RewriteRule ^ - [F]
```

### Tomcat

**Vulnerable:**

```xml
<http-method>GET</http-method>
```

**Correcto** — `http-method-omission` protege todos excepto los listados:

```xml
<http-method-omission>GET POST</http-method-omission>
```

### ASP.NET

**Vulnerable:**

```xml
<allow verbs="GET" roles="admin">
<deny verbs="GET" users="*">
```

**Correcto** — usar `add`/`remove` para gestionar permisos de forma exhaustiva sobre todos los verbos, no solo los nombrados.

## Codificación segura

La inconsistencia de variables (`$_POST` en el filtro, `$_REQUEST` en la lógica) es el segundo origen del problema. La solución: usar la misma variable en **ambos** lados.

```php
// Vulnerable:
if (!preg_match($pattern, $_POST['filename'])) {  // solo POST
    system("touch " . $_REQUEST['filename']);       // GET + POST + cookies
}

// Correcto: misma variable en filtro y en uso
if (!preg_match($pattern, $_REQUEST['filename'])) {
    system("touch " . $_REQUEST['filename']);
}
```

| Lenguaje | Variable que cubre todos los métodos |
|---|---|
| PHP | `$_REQUEST['param']` |
| Java | `request.getParameter('param')` |
| C# / ASP.NET | `Request['param']` |

## Checklist de prevención

- [ ] ¿Los controles de autenticación del servidor usan `LimitExcept` (Apache) o equivalente, en lugar de `Limit` con lista explícita?
- [ ] ¿Se han deshabilitado explícitamente los verbos que la aplicación no necesita (`HEAD`, `PUT`, `DELETE`, `OPTIONS`)?
- [ ] ¿Los filtros de seguridad en el código usan la misma variable de entrada que la lógica de negocio que protegen?
- [ ] ¿El filtro cubre todos los orígenes posibles de la entrada (GET, POST, cabeceras), no solo uno?

Cualquier "No" en este checklist es un hallazgo accionable a reportar — con el impacto directamente vinculado a qué funcionalidad queda desprotegida al omitirse el verbo no cubierto.
