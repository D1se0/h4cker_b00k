# Digispark Tutorial (Programandolo)

Lo que primero tendremos que hacer es conectarlo a nuestro equipo, utiliza un tipo A normal, por lo que nos servira con algun puerto de tipo A del equipo, una vez conectado, tendremos que desacragarnos el software de `Arduino IDE`.

URL = [Arduino IDE](https://www.arduino.cc/en/software)

Despues tendremos que instalar los drivers del `Digispark` para que el `Firmware` que tiene programado se pueda conectar al equipo `hardware` y lo reconozca a nivel `software`

URL = [Download Drivers Digispark](https://drive.google.com/file/d/1CPceJItGvD75XlcbRszFH5Nak19coy9m/view?usp=sharing)

Descomprimiremos el archivo y ejecutaremos el `.exe` dependiendo de nuestra arquitectura de sistema operativo ya sea de 64 o 32 bits, en mi caso es de 64 bits, por lo que ejecutare el llamado `DPinst64.exe` y seguire el proceso de instalacion.

Una vez echo esto se nos reconocera el dispositivo correctamente, ahora llendonos al `Arduino IDE`, nos iremos a `Files` -> `Preferences...` -> `Additional boards manager URLs` pondremos la siguiente URL:

```
https://raw.githubusercontent.com/digistump/arduino-boards-index/master/package_digistump_index.json
```

Para que se carguen los archivos necesarios de `digispark`, le daremos a `Ok` y nos iremos a `Tools` -> `Board:...` -> `Boards Manager...` -> buscaremos `Digistump AVR Boards by Digistump` e instalaremos esa dandole a `Install`.

Ahora configuraremos lo siguiente para que lo detecte bien, nos iremos a `Tools` -> `Board:...` -> `Digistump AVR Boards` -> `Digispark (Default - 16.5 mhz)`

Una vez instalado todo esto, ya solo tendriamos que escribir un codigo en `arduino`, para hacer un ejemplo, haremos lo siguiente:

```cpp
#include "DigiKeyboard.h"  // Incluye la librería DigiKeyboard para simular teclas

void setup() {
  DigiKeyboard.delay(3000);  // Espera 3 segundos para que el PC reconozca el Digispark

  // Abre el menú de Ejecutar usando Win + R
  DigiKeyboard.sendKeyStroke(KEY_R, MOD_GUI_LEFT);  // Win + R para abrir "Ejecutar"
  DigiKeyboard.delay(500);  // Espera 500 ms

  // Escribe el nombre del programa para abrir el Bloc de notas
  DigiKeyboard.print("notepad.exe");  // Cambia "notepad" a "notepad.exe" si es necesario
  DigiKeyboard.delay(500);

  // Presiona Enter para abrir el Bloc de notas
  DigiKeyboard.sendKeyStroke(KEY_ENTER);
  DigiKeyboard.delay(500);

  // Escribe el mensaje en el Bloc de notas
  DigiKeyboard.print("Esto es un texto de prueba");
}

void loop() {
  // Deja vacío el loop para que no repita el texto
}
```

Esto lo que hara es que cuando conectemos el `Digispark` al equipo se ejecute el bloc de notas y se escriba un texto de prueba, para cargarlo, tendremos que darle al boton con el siguiente simbolo `->` el cual se llamara `Upload`.

En la consola veremos la siguiente linea:

```cmd
>> Micronucleus done. Thank you!
```

Y con esto ya estaria cargado, por lo que si lo desconectamos y conectamos al equipo, esperaremos un rato y se ejecutara todo correctamente.
