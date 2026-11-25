---
icon: newspaper
---

# Digispark/USB Ninja (Función)

En esta prueba veremos a como desbloquear el patron de un movil (Patron de numeros) pero ya programado sabiendo el patron y las funcionalidades del mismo una vez estando dentro del movil y las diferencias de los 2.

## <mark style="color:purple;">DigiSpark General</mark>

### DigiSpark desbloqueo de patron y escribir una frase de prueba en un bloq de notas (movil)

Primero tendremos que programar mediante `Arduino` en el microcontrolador llamado `DigiSpark` volcarle el script que utilizaremos para el desbloqueo de pantalla cuando insertemos el mismo en el movil

Utilizaremos la biblioteca `DigiKeyboard`.

Instalaremos el software llamado `Arduino IDE`, despues echo esto entraremos dentro del mismo para programar el `DigiSpark`.

URL = [Arduino IDE](https://www.arduino.cc/en/software)

Dentro del software escribiremos algo parecido a esto:

```cpp
#include "DigiKeyboard.h"

void setup() {

  // Pausa para dar tiempo a que el móvil detecte el dispositivo

  DigiKeyboard.delay(5000);  // Espera 5 segundos para que el teléfono esté listo

  // Simular la entrada del patrón numérico (por ejemplo, "1234" como código de desbloqueo)

  DigiKeyboard.sendKeyStroke(KEY_1);  // Presiona '1'

  DigiKeyboard.delay(300);  // Breve pausa entre teclas

  DigiKeyboard.sendKeyStroke(KEY_2);  // Presiona '2'

  DigiKeyboard.delay(300);

  DigiKeyboard.sendKeyStroke(KEY_3);  // Presiona '3'

  DigiKeyboard.delay(300);

  DigiKeyboard.sendKeyStroke(KEY_4);  // Presiona '4'

  DigiKeyboard.delay(300);

  DigiKeyboard.sendKeyStroke(KEY_ENTER);  // Presiona 'Enter' para confirmar el PIN

  // Pausa para asegurarse de que el móvil se ha desbloqueado

  DigiKeyboard.delay(2000);

  // Abre el bloc de notas (simulación de teclas). Dependiendo del móvil, esto puede requerir ajustar los comandos.

  // Simula la búsqueda de la aplicación de Notas usando el botón de búsqueda en Android

  DigiKeyboard.sendKeyStroke(KEY_F3);  // Presiona la tecla 'Buscar'

  DigiKeyboard.delay(1000);

  DigiKeyboard.println("notas");  // Escribe "notas" en la búsqueda

  DigiKeyboard.delay(500);

  DigiKeyboard.sendKeyStroke(KEY_ENTER);  // Presiona 'Enter' para abrir la aplicación

  // Esperar un momento para que la aplicación se abra

  DigiKeyboard.delay(2000);

  // Escribir el mensaje de prueba en el bloc de notas

  DigiKeyboard.println("Este es un mensaje de prueba desde DigiSpark");

}

void loop() {

  // No es necesario repetir nada en el loop, ya que solo necesitamos ejecutar el código una vez

}
```

Y con esto lo que hara sera que cuando introduzcamos el `DigiSpark` en el movil, desbloqueara el patron programado y buscara el bloq de notas abriendolo y escribiendo en el mismo la frase de prueba.

Con esta tecnica tambien se podria descargar desde un servidor externo de `python3` un `APK` programada por nosotros que contenga una `Reverse Shell` y estando a la escucha desde un host nuestro de la siguiente forma:

```shell
nc -lvnp <PORT>
```

Podremos ganar acceso al sistema del movil mediante una terminal en nuestro host (Todo de forma automatizada).

O se podria hacer un `KeyLogger` para capturar los pulsos de teclas del patron o de informacion debil.

## <mark style="color:purple;">USB Ninja + Cable Bluetooth General</mark>

### USB Ninja desbloqueo de patron y escribir una frase de prueba en un bloq de notas todo mediante un cable Bluetooth (movil)

El USB Ninja tiene 2 botones (A y B) que con ellos podremos desplegar diferentes cargas utiles hacia el dispositivo de la Victima (Las que programemos nosotros).

Todo este ataque se hara mediante `Bluetooth` ya que el USB Ninja lleva incorporado una antena por la que transmite la señal hacia un transmisor `Bluetooth` en el que estara conectado al dispositivo de la Victima, podremos utilizar el `Cable Ninja Bluetooth` que lleva incorporado todo lo anterior (Externamente es una cable normal de carga de tipo C, pero por dentro lleva un sistema `Bluetooth` para que se pueda conectar el USB Ninja)

En el equipo Atacante programamos mediante el software `Arduino IDE` el USB Ninja con las respectivas funciones de los botones que queremos que haga, por ejemplo estableceremos que cuando se presione el `Boton A` haga una fuerza bruta para desbloquear el patron y cuando se presione el `Boton B` que se habra el bloq de notas y se escriba la frase de prueba.

```cpp
#include <USBNinja.h>

void setup() {

  USBNinja.begin(); // Iniciar el USB Ninja
  
}

void loop() {

  // Cuando se presiona el botón A, se envía el patrón PIN para desbloquear el móvil

  if (USBNinja.buttonA()) {

    // Simular el ingreso del código PIN (por ejemplo, "1234")

    USBNinja.sendKeyStroke(KEY_1); // Presiona '1'

    USBNinja.delay(300);

    USBNinja.sendKeyStroke(KEY_2); // Presiona '2'

    USBNinja.delay(300);

    USBNinja.sendKeyStroke(KEY_3); // Presiona '3'

    USBNinja.delay(300);

    USBNinja.sendKeyStroke(KEY_4); // Presiona '4'

    USBNinja.delay(300);

    USBNinja.sendKeyStroke(KEY_ENTER); // Confirmar el PIN con 'Enter'

    USBNinja.delay(2000); // Pausa para asegurarse de que el teléfono se ha desbloqueado

  }

  // Cuando se presiona el botón B, abre el bloc de notas y escribe un mensaje de prueba

  if (USBNinja.buttonB()) {

    // Simular abrir el bloc de notas (ajustar según el dispositivo)

    USBNinja.sendKeyStroke(KEY_F3); // Buscar en el teléfono (F3 es una tecla común de búsqueda)

    USBNinja.delay(1000); // Esperar que aparezca el campo de búsqueda

    USBNinja.println("notas"); // Escribir "notas" en el campo de búsqueda

    USBNinja.delay(500); // Pausar antes de presionar Enter

    USBNinja.sendKeyStroke(KEY_ENTER); // Presiona 'Enter' para abrir la app de Notas

    USBNinja.delay(2000); // Esperar que la app de Notas se abra

    // Escribir el mensaje de prueba en el bloc de notas

    USBNinja.println("Este es un mensaje de prueba desde USB Ninja");

  }

}
```

Esto lo que hace es desbloquear el movil con el `Boton A` y cuando se presione el `Boton B` que se habra el bloq de notas y se escriba la frase de prueba.

A parte de el texto de prueba, se puede hacer mucho mas como por ejemplo `Reverse Shell` o `KeyLoggers`, tambien la tecnica de las `Stiky Keys`, etc...

URL = [Pagina USB Ninja](https://lab401.com/es-es/products/usbninja?srsltid=AfmBOoq-v9GiW8FI27gS4XAFEIymS1ttCIRpMyqGIhuVpUA9u_KYtbAK)

## <mark style="color:purple;">Conclusión final</mark>

El USB Ninja + el cable bluetooth es la mejor eleccion ya que a la hora de hacer pentesting en red team es muy eficaz y muchisimo mas discreto, sin embargo el DigiSpark es menos sigiloso y menos variedad de programación ya que es muy limitada.
