# Introducción (SQL Injection)

Un `SQL Injecction` es simplemente realizar una consulta de `mysql` de forma maliciosa para poder extraer informacion sobre ella, esta claro que este tipo de consultas van a funcionar si hay poca seguridad en la misma, pero si esta bien protegido a este tipo de ataques no van a funcionar.

Podremos saber que es vulnerable a un `SQL Injecction` cuando intentamos realizar alguna de estas tecnicas y nos devuelve un error en la propia base de datos, mostrando el error u otro tipo de informacion, por lo que pasariamos a la fase de explotacion una vez sabiendo esto.

De primeras podriamos probar a poner simplemente una `'` para ver si devuelve algun tipo de error, ya que internamente lo que hace es cerrar una de las partes de la consulta:

```
User: '
Pass: null
```

Y veriamos algo tal que asi:

<figure><img src="../../.gitbook/assets/image (67) (1).png" alt=""><figcaption></figcaption></figure>

Por lo que vemos nos esta devolviendo un error, en el que encima nos especifica donde esta dando el error y el tipo de consulta que se esta haciendo, por lo que podremos aprovechar esto para realizar un `SQL Injecction` de forma mas avanzada.

Este tipo de fallos suceden cuando el programador del `backend` no ha sanitizado adecudamente las entradas de los `input's`, por lo que es susceptible a injecciones de codigo.

Mas adelante veremos lo que es un `Blind SQL Injecction` que es cuando no podemos saber mediante un error si es susceptible a injecciones de `sql` pero si mediante tiempos de espera.

Una vez sabiendo que es vulnerable podremos probar como hicimos anteriormente a meter lo siguiente:

```
User: ' OR 1=1-- -
Pass: null
```

Ya que es una codicion que siempre se va a cumplir y asi que nos muestre la informacion de las bases de datos, con la `'` lo que estamos haciendo es cerrar el `username` y poner la condicion que queremos que se cumpla, seguido de `-- -` que en `mysql` es un comentario para que no haya ningun error, comentamos lo demas.

Esto tambien se puede utilizar para `bypassear` un login de un formulario el cual sea susceptible a `SQL Injecction`, si nos vamos al siguiente apartado en la pagina de `Mutillidae` -> `OWASP 2017` -> `A1 - Injection SQL` -> `SQLi - Bypass Authentication` -> `Login`

Podremos `Bypassearlo` para que nos logee como un usuario legitimo de la siguiente forma:

```
User: ' OR 1=1-- -
Pass: null
```

Lo que vamos hacer aqui es que va a funcionar y nos va a logear con el primero usuario que este en la base de datos, por lo que pasaremos de esto:

<figure><img src="../../.gitbook/assets/image (68) (1).png" alt=""><figcaption></figcaption></figure>

A esto:

<figure><img src="../../.gitbook/assets/image (69) (1).png" alt=""><figcaption></figcaption></figure>

Y con esto vemos que somo el usuario `admin` por lo que funciono.

Ahora nos iremos a la que estabamos antes de `Extract data` de `SQL Injection` y para poder saber a que tipo de base de datos nos estamos enfrentando, se podria hacer de la siguiente forma:

```
User: ' UNION select database()-- -
Pass: null
```

Aqui lo que estamos haciendo es con el operador `UNION` unir lo que venga de detras con lo que nosotros le pongamos despues del `UNION`, concatenando por asi decirlo los comandos, por lo que despues le decimos que nos seleccione la base de datos para asi poder saber a que nos estamos enfrentando y despues con el `-- -` comentar lo que venga despues para que no nos de ningun tipo de error.

Y con esto nos va a dar un error, pero diferente, ya que nos esta diciendo que no coincide el numero de columnas de la primera consulta con la consulta que nosotros le estamos indicando, por lo que como no sabemos cuantas columnas hay, podremos mediante injeccion de comandos de `sql` descubrir, la columna exacta en la que poder injectar esta consulta que nosotros estamos haciendo.

<figure><img src="../../.gitbook/assets/image (71) (1).png" alt=""><figcaption></figcaption></figure>

Y para ir descubriendo esto, se tiene que ir haciendo poco a poco lo siguiente.

```
User: ' UNION select null,database()-- -
Pass: null
```

Con esto lo que estamos suponiendo es que hay 2 columnas en la tabla de `mysql` pero especificamos que la primera esta vacia con un `null` y que la segunda realice nuestra consulta, si acertamos en la columna veremos la informacion de la base de datos, pero en este caso tambien dara error, por que estamos viendo que hay mas de 2 columnas.

Para adelantar todo imaginemos que ya hemos probado con unas cuantas y la correcta serian 7 columnas que es lo que tiene esta base de datos, por lo que para que esto funcione seria algo asi:

```
User: ' UNION select null,database(),null,null,null,null,null-- -
Pass: null
```

Y con esto te devuelve el nombre de la base de datos que en este caso seria `mutillidae`.

<figure><img src="../../.gitbook/assets/image (72) (1).png" alt=""><figcaption></figcaption></figure>

Para descubrir la version de esta base de datos, podremos hacerlo con otro comando cogiendo la misma consulta ahora que sabemos que tiene 7 columnas.

```
User: ' UNION select null,version(),null,null,null,null,null-- -
Pass: null
```

<figure><img src="../../.gitbook/assets/image (73) (1).png" alt=""><figcaption></figcaption></figure>

Si queremos sacar la informacion de todas las tablas, podremos hacerlo de la siguiente forma:

```
User: ' UNION select null,table_name,null,null,null,null,null FROM information_schema.tables-- -
Pass: null
```

<figure><img src="../../.gitbook/assets/image (74) (1).png" alt=""><figcaption></figcaption></figure>

Lo interesante de esto es que nosotros podremos leer algunos archivos del sistema ya que la propia base de datos suele poder leer este tipo de ficheros, y nosotros podremos aprovechar eso de la siguiente forma:

```
User: ' UNION select null,@@secure_file_priv,null,null,null,null,null-- -
Pass: null
```

<figure><img src="../../.gitbook/assets/image (75) (1).png" alt=""><figcaption></figcaption></figure>

Esto nos mostrara la ruta de donde estan esos ficheros y sabiendo esto, nosotros mediante consultas de `mysql` podremos aprovechar esto para leerlos.

```
/var/lib/mysql-files/
```

Si desde la maquina victima, nosotros ponemos un fichero en esa ruta, nosotros como atacantes podremos leer ese fichero.

Pongamos que el fichero se llama `passwords.txt` podremos leerlo de la siguiente forma:

```
User: ' UNION select null,load_file('/var/lib/mysql-files/passwords.txt'),null,null,null,null,null-- -
Pass: null
```

Y con esto podremos leer el contenido de ese fichero.

Para terminal con el `SQL Injection` de forma manual, esta la otra tecnica que se le denomina `Blind SQL Injection` que es cuando nosotros metemos una `'` pero no nos suelta ningun error, pero sabemos que puede ser vulnerable a esto, por lo que para determinar si es vulnerable o no podremos hacer una consulta de `sleep()` por lo que si tarda tantos segundos que le pongas tu en responder la pagina, veremos que realmente es vulnerable a `SQL Injection`.

Por ejemplo podremos hacerlo de la siguiente forma:

```
User: ' UNION select null,sleep(5),null,null,null,null,null-- -
Pass: null
```

Por lo que si ejecutamos esta sentencia, deberia de tardar `5` segundos que es lo que le puse yo en que nos responda la pagina.

Y con esto nos podriamos montar un script en el cual mediante fuerza bruta sacar el nombre de la base de datos, mediante ataques de tiempos, cuando tarde 5 segundos seria `true` y cuando sea instantaneo seria `false`.

Por lo que poco a poco nos estara sacando el nombre probando todas las letras del abecedario y caracteres.
