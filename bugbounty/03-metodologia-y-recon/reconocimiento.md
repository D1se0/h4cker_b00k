# Reconocimiento (Recon)

## 🎯 Objetivo de esta fase

Antes de intentar "romper" nada, necesitas un mapa completo de qué existe. Cuanto mejor sea tu recon, más superficie de ataque real vas a ver — y muchas vulnerabilidades aparecen precisamente en activos "olvidados" que nadie mira (subdominios de staging, apps antiguas, endpoints de APIs internas expuestas por error...).

## 🗺️ Recon pasivo (sin tocar directamente el objetivo)

- **Subdominios**: `subfinder`, `amass`, certificados SSL/TLS (crt.sh), motores de búsqueda con `site:dominio.com`.
- **Tecnologías usadas**: extensiones como Wappalyzer, cabeceras HTTP, `builtwith.com`.
- **Historial de URLs**: `waybackurls`, `gau`, Google cache, Wayback Machine — a veces revelan endpoints antiguos que siguen activos.
- **Repositorios públicos**: búsquedas en GitHub/GitLab de código relacionado con la empresa (cuidado: solo mirar lo público, nunca intentar acceder a repos privados).
- **Documentación pública**: swagger/OpenAPI expuestos, documentación de desarrolladores, App Store / Google Play (para apps móviles).

## 🔬 Recon activo (interactuando ya con el objetivo, dentro de scope)

- **Enumeración de hosts vivos**: `httpx` sobre la lista de subdominios encontrados.
- **Fuzzing de rutas y parámetros**: `ffuf`/`gobuster` para encontrar endpoints no enlazados desde el frontend.
- **Mapear la app como usuario normal**: navega con el proxy (Burp/ZAP) activado y deja que capture TODO el tráfico — así construyes un mapa real de endpoints usados por la app.
- **Comparar el comportamiento en distintos roles** si el programa lo permite (usuario normal vs. usuario premium, por ejemplo, usando cuentas propias de cada tipo).

## 🧩 Priorizar dónde mirar

No todo el scope merece el mismo tiempo. Prioriza:

1. **Funcionalidades que manejan identidad de otros usuarios** (perfiles, mensajes, favoritos, facturación) → candidatos a IDOR/BOLA.
2. **Flujos de autenticación y recuperación de contraseña** → candidatos a broken authentication.
3. **Zonas nuevas o recién desplegadas** (versión beta, apps recién actualizadas) → menos testeadas, más probabilidad de fallos frescos.
4. **Integraciones con terceros** (SSO, pagos, webhooks) → superficie de ataque a menudo peor auditada que el core del producto.

## 🧾 Cómo documentar el recon

Lleva, por programa, una nota con:

- Lista de subdominios/activos encontrados y su estado (vivo/caído, tecnología).
- Endpoints interesantes detectados, con una línea de qué hacen.
- Hipótesis a probar ("este endpoint recibe un `userId` en el body, probar si se puede cambiar por el de otra cuenta").
- Lo que ya probaste y descartaste (para no repetir trabajo semanas después).

> ⚠️ Recuerda: todo esto debe hacerse siempre dentro del scope autorizado por el programa y respetando explícitamente sus reglas sobre herramientas automatizadas.
