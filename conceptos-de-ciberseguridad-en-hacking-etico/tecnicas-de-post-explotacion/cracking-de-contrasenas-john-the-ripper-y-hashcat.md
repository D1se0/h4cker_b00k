# Cracking de contraseñas (John the ripper y Hashcat)

Estas 2 herramientas son similares en funcionamiento, se utilizar para crackear `hashes`, contraseñas, etc... pasandole un `wordlist` o utilizando el que viene por defecto, tambien se le puede especificar el formato del `hash`, etc...

Por ejemplo vamos a `hashear` una palabra:

```shell
echo -n "1234" | md5sum | cut -f 1 -d " " > hash.md5
```

Y con esto nos generara un fichero con un `hash` que se corresponde a un tipo de `md5` que significa esa cadena de numeros `1234`:

```
81dc9bdb52d04dc20036dbd8313ed055
```

Por lo que para poder crackear esto y que nos lo de en texto plano, vamos a utilizar una de las 2 herramientas que mencione anteriormente:

> NOTA:

Un `hash` es una funcion criptografica que lo que hace es recibir informacion y proporciona un valor determinado para esa informacion, los `hashes` tienen una propiedad muy relevante, y es que si nosotros `hasheamos` por ejemplo este algoritmo en `md5` la misma palabra siempre nos va a dar el mismo `hash`, si nosotros modificamos algun `byte`/`letra` de esa cadena, el `hash` va a cambiar por completo y a partir del `hash` tambien es muy complicado realizar `ingenieria inversa` para poder romperlo y obtener la palabra original.

Para crackear dicho `hash`:

```shell
john --format=Raw-MD5 --wordlist=/usr/share/wordlists/rockyou.txt hash.md5
```

Con esto lo que estamos haciendo es que le especificamos el formato que tiene dicho `hash`, le pasamos una lista de palabras las cuales va a comparar por si se encontrara ahi y pasarle el `hash` que queremos que `deshashe` (Por dentro lo que va hacer `john` es `hashear` cada una de las palabras del diccionario y comparar los `hashes` con el `hash` que le hemos pasado, hasta encontrar el correcto)

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (Raw-MD5 [MD5 128/128 AVX 4x3])
Warning: no OpenMP support for this hash type, consider --fork=8
Press 'q' or Ctrl-C to abort, almost any other key for status
1234             (?)     
1g 0:00:00:00 DONE (2024-11-24 04:09) 100.0g/s 115200p/s 115200c/s 115200C/s marie1..summer1
Use the "--show --format=Raw-MD5" options to display all of the cracked passwords reliably
Session completed.
```

Una vez que lo haya encontrado nos pondra esto y veremos que lo ha conseguido.

En tal caso de que ya la hubieramos crackeado, solo tendremos que poner el siguiente comando para visualizarla mejor:

```shell
john --format=Raw-MD5 hash.md5 --show
```

Info:

```
?:1234

1 password hash cracked, 0 left
```

Ahora si lo hicieramos con `hashcat` sera de una forma un poco mas distinta, la particularidad de esta herramienta es que deberemos de indicarle el tipo de `hash` conforme a su numero, ya que cada `hash` su formato se identifica por un numero y despues otros parametros de la misma herramienta.

URL = [Pagina codigos hash Hashcat](https://hashcat.net/wiki/doku.php?id=example_hashes)

```shell
hashcat -m 0 -a 0 hash.md5 /usr/share/wordlists/rockyou.txt
```

Y esto nos dara como resultado la palabra en texto plano del `hash` parecido a `john`, si lo quisieramos ver en especifico hariamos lo siguiente:

```shell
hashcat -m 0 -a 0 hash.md5 /usr/share/wordlists/rockyou.txt --show
```

Y esto te dara el `hash` con el valor en texto plano.

Si queremos realizar fuerza brura con dicho `hash` sera de la siguiente forma:

```shell
hashcat -m 0 -a 3 hash.md5
```
