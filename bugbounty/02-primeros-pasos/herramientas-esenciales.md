---
icon: toolbox
---

# Herramientas esenciales

No hace falta tener 200 herramientas. Con un stack sólido y saber usarlo bien vas muy lejos. Aquí va lo que uso con más frecuencia, agrupado por categoría.

## 🌐 Proxy / interceptación de tráfico

| Herramienta                      | Para qué                                                                  |
| -------------------------------- | ------------------------------------------------------------------------- |
| **Burp Suite** (Community o Pro) | El estándar de facto. Interceptar, modificar y repetir peticiones HTTP/S. |
| **OWASP ZAP**                    | Alternativa gratuita y open-source a Burp.                                |
| **mitmproxy**                    | Proxy en terminal, muy potente para scripting y tráfico de apps móviles.  |

## 🔍 Reconocimiento / enumeración

| Herramienta           | Para qué                                                                                                                            |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| **subfinder / amass** | Enumeración de subdominios.                                                                                                         |
| **httpx**             | Comprobar qué hosts están vivos y responden HTTP.                                                                                   |
| **nuclei**            | Escaneo de plantillas de vulnerabilidades conocidas (úsalo siempre respetando las reglas del programa sobre escáneres automáticos). |
| **ffuf / gobuster**   | Fuzzing de rutas, parámetros y subdominios.                                                                                         |
| **waybackurls / gau** | Recuperar URLs históricas indexadas (Wayback Machine, etc.).                                                                        |

## 📱 Análisis de apps móviles

| Herramienta                           | Para qué                                                                                                     |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| **apktool / jadx**                    | Descompilar/desempaquetar APKs de Android.                                                                   |
| **grep / strings**                    | Buscar cadenas de texto (tokens, URLs, claves) directamente en binarios y bundles JS (Hermes, React Native). |
| **apkpure / apk mirrors oficiales**   | Descargar el APK público sin necesidad de cuenta de Google Play.                                             |
| **Frida / Objection**                 | Instrumentación dinámica: bypass de SSL pinning, hooking de funciones en runtime.                            |
| **MobSF (Mobile Security Framework)** | Análisis estático y dinámico automatizado de APKs/IPAs.                                                      |

## 🧪 Peticiones manuales y scripting

| Herramienta                        | Para qué                                                                                             |
| ---------------------------------- | ---------------------------------------------------------------------------------------------------- |
| **curl**                           | El básico imprescindible para reproducir cualquier request de forma limpia y copiable en un reporte. |
| **httpie**                         | curl "amigable", más legible.                                                                        |
| **Python (requests, PyJWT, etc.)** | Automatizar pruebas, decodificar tokens, scripts de PoC.                                             |
| **jq**                             | Parsear y filtrar JSON en terminal.                                                                  |
| **JWT.io / PyJWT**                 | Decodificar y analizar tokens JWT (¡ojo!, decodificar no es lo mismo que romper la firma).           |

## 🖥️ Entorno

* **Kali Linux** (o cualquier distro con las herramientas anteriores) — no es obligatorio pero ayuda a tener todo centralizado.
* **Máquina/perfil de navegador dedicado para testing**, separado del uso personal, para no mezclar cookies/sesiones.
* **Cuentas de correo desechables** para registrar cuentas de prueba (revisa que el programa lo permita).

## 📝 Documentación mientras trabajas

| Herramienta                           | Para qué                                                                      |
| ------------------------------------- | ----------------------------------------------------------------------------- |
| **ShareX / Flameshot / Greenshot**    | Capturas de pantalla rápidas y anotadas.                                      |
| **OBS Studio**                        | Grabación de vídeo para PoCs en vídeo (login, flujos multi-paso).             |
| **Obsidian / Notion / un simple .md** | Notas de recon, hipótesis probadas, ideas pendientes por programa.            |
| **CyberChef**                         | Navaja suiza para codificar/decodificar (base64, JWT, URL encode, hashes...). |

> 💡 **Tip**: no necesitas todo esto el día 1. Empieza con navegador + Burp/ZAP + curl + un editor de notas, y ve añadiendo herramientas según te las vaya pidiendo la investigación.
