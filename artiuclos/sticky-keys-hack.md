---
icon: shield-slash
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

# Sticky Keys Hack

## <mark style="color:purple;">Explicación de la técnica</mark>

Esta tecnica se utiliza para que cuando estas en un login de windows y no sabes la contraseña de dicho usuario o quieres de alguna forma bypassear el password del usuario, intercambias el ejecutable de la tecla especial (Esta se activa dando 5 veces al `Shift` de seguido) y que en vez de aparezca el recuadro de la tecla especial, aparezca un `cmd` autenticada como `administrador`, con lo cual desde ahi cambiar la contraseña al usuario y entrarias.

## <mark style="color:purple;">Pendrive Boot Windows 10</mark>

Primero haremos un `Pendrive Boot` con Windows 10 con la propia herramienta de `Windows Tool` para generar un `Pendrive Boot` con el `Windows 10`.

URL = [Descargar Windows Tools](https://www.microsoft.com/es-es/software-download/windows10?msockid=2284017e9b096c8a2198147d9abc6d27)

Insertar el pendrive que quieres `bootear`.

> IMPORTANTE!!

Ese pendrive se borrara entero (Formateara) y se instalara la herramienta minimo 8 GB de espacio para que esto pueda funcionar, una vez sabiendo esto, seguiremos...

### Dentro del Windows Tools

Le daremos a `Siguiente` hasta llegar a la opcion de `Actualizar en este equipo` y `Exportarlo en una ISO, Pendrive, etc...` seleccionaremos la segunda opcion (ISO, Pendrive, etc...), deberia de detectar automaticamente el pendrive, pero seleccionaremos el pendrive que queremos formatear para transformarlo en un `Pendrive Boot` con windows 10, seguiremos la propia guia que ya da windows con todo por defecto.

## <mark style="color:purple;">Configuracion de Sticky Key</mark>

Una vez finalizado lo anterior, insertaremos el `Pendrive Boot` en el PC donde queremos hacer dicha tecnica, entraremos a la BIOS con la tecla `F11, Supr, F10, etc...` dependiendo de que PC sea, una vez dentro cambiaremos las opciones de arranque para que se inicie con el `Pendrive Boot`, una vez echo eso reiniciaremos el PC.

### Dentro del Pendrive Boot

Una vez que se nos inicie con el `Pendrive Boot` veremos la tipica pantalla de como si fueramos a instalar Windows 10, pero no lo haremos, daremos a siguiente la primera vez con el idioma que queramos y despues le daremos a la opcion abajo izquierda llamada `Reparar el equipo`, esto nos metera en otra interfaz donde habra unas pocas opciones, daremos a la opcion llamada `Solucionar problemas` y por ultimo a la opcion `Simbolo del sistema`.

Esto nos abrira un `cmd` con el que trabajaremos para hacer esta tecnica y copiaremos el `cmd.exe` al ejecutable llamado `sethc.exe` para que cuando le demos 5 veces de seguido al `Shift` se nos abra el `cmd` y no el recuadro de tecla especial.

Pondremos el siguiente comando:

```powershell
copy C:\Windows\System32\cmd.exe C:\Windows\System32\sethc.exe
```

Con esto ya habriamos echo lo dicho anteriormente y por ultimo para salirnos escribiremos lo siguiente:

```powershell
exit
```

Reiniciaremos el equipo, pero antes sacar el `Pendrive Boot` del slot USB y nos metera de normal al windows.

## <mark style="color:purple;">Efectuar tecnica Sticky Key</mark>

Estando en el login de windows y habiendo echo todo lo anterior pulsaremos 5 veces de seguido la tecla `Shift`, esto nos abrira el `cmd` autenticado como `administrador` y podremos cambiar el password al usuario con el que queramos entrar de la siguiente forma:

```cmd
net user <USER> <PASSWORD>
```

Y con esto ya se habria cambiado correctamente el password del usuario elegido, solo tendremos que ingresar el nuevo password y listo, estariamos dentro ya.

## <mark style="color:purple;">Restaurar el archivo</mark>

Para dejar todo como estaba antes, abriremos el `PowerShell` como `Administrador` y escribiremos lo siguiente:

```powershell
copy C:\Windows\System32\sethc.exe.bak C:\Windows\System32\sethc.exe
```

Y con esto ya estaria todo como antes.

### Segunda opción de restaurar el archivo

Antes de hacer todo lo anterior y de copiar el `cmd.exe` al archivo de la tecla especial, podremos copiarlo a nuestro pendrive o en algun lugar como copia de seguridad de la siguiente manera:

```powershell
copy D:\Windows\System32\sethc.exe C:\Windows\System32\sethc.exe
```

Cambiaremos la letra del pendrive que corresponda a vuestro pendrive.
