# Enumeración masiva y referencias codificadas en IDOR

## Enumeración básica con un script

Una vez confirmada la vulnerabilidad IDOR (cambiar `?uid=1` a `?uid=2` devuelve documentos de otro usuario), el siguiente paso en una auditoría es demostrar el **alcance** del problema — cuántos registros son accesibles de esta forma, no solo uno. Para ello se automatiza la iteración sobre los posibles valores del identificador.

El patrón básico en bash para enumerar y descargar todos los documentos accesibles:

```bash
for uid in $(seq 1 20); do
    # Extraer enlaces de documentos de la página de cada usuario
    curl -s "http://objetivo/documents.php?uid=$uid" \
        | grep -oP "\/documents.*?\.pdf" \
        | while read -r doc; do
            echo "UID $uid: $doc"
        done
done
```

Esto itera sobre los valores del identificador, extrae los links de documentos de cada respuesta con una expresión regular, y los lista — con opciones para descargarlos añadiendo `wget "http://objetivo$doc"`. El mismo efecto se logra con Burp Intruder o ffuf, como se vio en el bloque de *Web Proxies*.

> **Principio de PoC mínima**: en una auditoría responsable, listar los nombres de los archivos accesibles es suficiente para demostrar el alcance del IDOR sin necesidad de descargar y acceder al contenido real de cada documento. El objetivo es demostrar el fallo, no extraer datos privados de usuarios reales.

## IDOR con referencias codificadas (Base64)

Cuando el identificador no es un número plano sino un valor codificado, el patrón de ataque es el mismo — simplemente con un paso adicional de decodificación/recodificación:

```bash
# Referencia codificada en Base64 encontrada en la URL:
# ?filename=ZmlsZV8xMjMucGRm

# Decodificar:
echo "ZmlsZV8xMjMucGRm" | base64 -d
# -> file_123.pdf

# Modificar y recodificar:
echo -n "file_124.pdf" | base64
# -> ZmlsZV8xMjQucGRm

# Probar:
curl "http://objetivo/?filename=ZmlsZV8xMjQucGRm"
```

La codificación Base64 (u otra codificación estándar como hex o URL-encoding) no añade ninguna protección real si no hay un control de acceso en el servidor — solo añade un paso trivial de decodificación antes de poder manipular el identificador.

## IDOR con referencias hasheadas predecibles

Si el código JavaScript frontend revela el algoritmo usado para generar el identificador, es posible reproducirlo para otros valores:

```javascript
// En el JS del frontend, encontrado durante revisión de código:
data: {filename: CryptoJS.MD5('file_1.pdf').toString()}
// -> c81e728d9d4c2f636f067f89cc14862c

// Para file_2.pdf, ejecutar en la consola del navegador:
CryptoJS.MD5('file_2.pdf').toString()
// -> c4ca4238a0b923820dcc509a6f75849b
```

Un hash calculable a partir de un valor conocido tampoco es protección — el hash resuelve "¿cómo se construye el identificador?" pero no responde a "¿tiene este usuario permiso sobre este objeto?".

## El IDOR de funciones no solo de datos

Más allá del acceso a datos de otro usuario, IDOR puede también permitir invocar **funciones** que deberían estar restringidas a un rol superior:

```json
POST /api/update_employee
{
  "uid": 183,
  "role": "admin",
  "is_admin": true
}
```

Si el servidor no verifica que el usuario autenticado tiene permiso para asignar roles (solo comprueba que la sesión es válida, no su nivel de privilegio), un usuario estándar puede escalar sus propios privilegios — el mismo patrón visto en el bloque de *Broken Authentication* al hablar de bypass por modificación de parámetros.

## La diferencia que marca el control de acceso

| Situación | Resultado | Vulnerabilidad |
|---|---|---|
| `?uid=124` devuelve datos de otro usuario | IDOR confirmado — falta control de acceso |
| `?uid=124` devuelve `403 Forbidden` | No hay IDOR — el control de acceso funciona |
| `?uid=124` devuelve exactamente los mismos datos que `?uid=123` | No hay IDOR — probablemente ignora el parámetro y usa la sesión |

El tercer caso es un buen diseño: el servidor ignora el `uid` de la URL y deriva la identidad exclusivamente del token de sesión, que el usuario no puede alterar para hacerse pasar por otro.
