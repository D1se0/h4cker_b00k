---
icon: window-restore
layout:
  title:
    visible: true
  description:
    visible: false
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
---

# Bypass UAC (Windows)

### Script: Ejecutar Instalador sin Pedir Permisos de Administrador (UAC Bypass)

#### Código:

```cmd
@echo off
setlocal
:: Ejecuta gu6setup.exe sin pedir privilegios elevados (RunAsInvoker)

set "__COMPAT_LAYER=RunAsInvoker"
set "APP_PATH=%~dp0gu6setup.exe"

if not exist "%APP_PATH%" (
    echo [ERROR] El archivo gu6setup.exe no fue encontrado.
    pause
    exit /b 1
)

echo Iniciando gu6setup.exe con compatibilidad RunAsInvoker...
start "" "%APP_PATH%"
pause
```

Para realizar la prueba te puedes descargar el instalador desde el siguiente link:

URL = [Download gu6setup.exe](https://www.glarysoft.com/aff/download2.php?s=GU)

***

### ¿Qué hace este script?

Este script permite **ejecutar un instalador (`gu6setup.exe`) sin que el sistema operativo solicite permisos de administrador** (sin UAC). Esto es útil cuando el programa no necesita privilegios elevados para ejecutarse, pero aún así solicita el UAC innecesariamente.

***

### ¿Qué es el UAC?

**UAC** (_User Account Control_) es un mecanismo de seguridad en Windows que:

* Previene que software haga cambios no autorizados en el sistema.
* Muestra una ventana emergente que solicita confirmación del usuario antes de ejecutar programas como administrador.

***

### ¿Qué es `RunAsInvoker`?

`RunAsInvoker` es una bandera interna del sistema operativo que se puede forzar mediante la variable de entorno `__COMPAT_LAYER`.

Cuando se establece `__COMPAT_LAYER=RunAsInvoker`:

* Se indica al sistema que **no eleve** los privilegios del proceso, aunque el ejecutable lo solicite en su manifiesto (`requireAdministrator`).
* No se mostrará la ventana de UAC.
* El programa se ejecutará con los **mismos permisos** que tiene el script (sin ser admin).

***

### Explicación línea por línea

| Línea                               | Explicación                                                                                                                                  |
| ----------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `@echo off`                         | Oculta los comandos que se están ejecutando en la consola. Más limpio.                                                                       |
| `setlocal`                          | Aísla las variables para que solo existan dentro del script.                                                                                 |
| `set "__COMPAT_LAYER=RunAsInvoker"` | Aplica la capa de compatibilidad para evitar que el proceso solicite UAC.                                                                    |
| `set "APP_PATH=%~dp0gu6setup.exe"`  | Guarda la ruta completa del archivo `gu6setup.exe`, suponiendo que está en el mismo directorio que el script. `%~dp0` es la ruta del script. |
| `if not exist ...`                  | Verifica que el archivo `gu6setup.exe` exista antes de intentar ejecutarlo.                                                                  |
| `start "" "%APP_PATH%"`             | Lanza el instalador sin abrir una nueva consola. El `""` es el título de la ventana, requerido por `start`.                                  |
| `pause`                             | Espera a que el usuario presione una tecla antes de cerrar. Útil para ver mensajes de error o éxito.                                         |

***

### Técnicas similares / Payloads posibles

Este enfoque de UAC bypass con `RunAsInvoker` **no es una vulnerabilidad en sí**, sino una técnica permitida por el sistema operativo. Sin embargo, puede ser usada de forma maliciosa.

#### Payloads o usos comunes:

1. **Instaladores personalizados**: Ejecutar `.exe` sin necesidad de pedir al usuario que acepte el UAC.
2. **Bypass UAC para scripts**: Inyectar comandos maliciosos que normalmente requerirían elevación.
3. **Cargar DLLs o backdoors** dentro de programas que no hacen verificación de integridad.
4. **Persistence**: Insertar el script en el inicio del sistema sin ser detectado por el UAC.
5. **Ingeniería social**: Ejecutar binarios que se disfrazan de algo benigno, sin levantar sospechas por la ausencia de UAC.

> ⚠️ **Advertencia ética:** Esta técnica debe utilizarse únicamente con fines educativos, administrativos legítimos o pruebas de seguridad autorizadas. El mal uso puede ser ilegal y sancionado por la ley.

***

### Limitaciones

* No funciona si el ejecutable **requiere sí o sí** privilegios de administrador para funcionar (por ejemplo, si accede a archivos del sistema).
* Solo evita la **ventana de UAC**; no eleva permisos mágicamente.
* Si el usuario **ya no tiene privilegios de admin**, el resultado será el mismo que ejecutar el programa como usuario estándar.

***

### Cuándo usar esta técnica

* Cuando el software no necesita privilegios de administrador pero está mal configurado.
* En entornos educativos para enseñar sobre compatibilidad en Windows.
* Para automatizar instalaciones internas que no requieren cambios profundos en el sistema.

### Tabla de Payloads para Bypass UAC con `RunAsInvoker`

| #  | Tipo de Payload                 | Descripción                                                                                     | Nivel de Privilegio | Notas Importantes                                                                     |
| -- | ------------------------------- | ----------------------------------------------------------------------------------------------- | ------------------- | ------------------------------------------------------------------------------------- |
| 1  | Instalador `.exe`               | Ejecutar un instalador que no requiere permisos reales de admin, pero pide UAC por defecto.     | Usuario estándar    | Ideal para software mal configurado que pide permisos innecesarios.                   |
| 2  | PowerShell Script Wrapper       | Ejecutar un script `.ps1` malicioso disfrazado como instalador o herramienta legítima.          | Usuario estándar    | Puede usarse para carga de módulos, keyloggers o descarga de payloads adicionales.    |
| 3  | Ejecutable con DLL Hijacking    | Correr un `.exe` vulnerable a cargar una DLL manipulada desde el mismo directorio.              | Usuario estándar    | No necesita privilegios si la ruta de la DLL no es protegida por el sistema.          |
| 4  | Carga de DLL vía regsvr32       | Ejecutar una DLL maliciosa usando `regsvr32`, aprovechando el `RunAsInvoker`.                   | Usuario estándar    | Técnicamente no necesita UAC si la DLL no toca el sistema.                            |
| 5  | Scripts por lotes (`.bat`)      | Ejecutar otros scripts automatizados para moverse lateralmente en la máquina.                   | Usuario estándar    | Útil para persistencia en entornos sin control de privilegios estricto.               |
| 6  | Ejecutar Binarios de Confianza  | Lanzar binarios firmados por Microsoft con parámetros modificados.                              | Usuario estándar    | Ej: usar `fodhelper.exe` o `computerdefaults.exe` con técnicas más avanzadas.         |
| 7  | Herramientas de pentesting      | Ejecutar herramientas como `mimikatz`, `revshell.exe` sin trigggear el UAC.                     | Usuario estándar    | Solo si están configuradas para no requerir elevación desde el manifiesto.            |
| 8  | Acceso a tareas programadas     | Crear o ejecutar tareas en el scheduler (`schtasks`) sin UAC.                                   | Usuario estándar    | Depende de si la política de ejecución permite crear tareas sin elevación.            |
| 9  | Abusar programas portables      | Ejecutar programas legítimos portables (como un navegador) y hacer side-loading de código.      | Usuario estándar    | No se eleva, pero se puede usar para phishing o C2 sin alertar al usuario.            |
| 10 | Puerta trasera en software real | Reempaquetar un instalador legítimo con código malicioso, y usar `RunAsInvoker` para disfrazar. | Usuario estándar    | Técnica de _trojanización_, oculta actividades maliciosas tras un programa funcional. |
