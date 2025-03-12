---
icon: database
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

# NoSQL Injection

Esta tecnica es similar a `SQL Injection` pero con la diferencia de que haces peticiones que no tienen que coincidir entre si...

Si por ejemplo en `SQL Injection` se hacia la comparacion logica para que siempre sea cierto `' OR 1=1-- -` de esa manera, en esta tendra que ser al contrario pero en formato `JSON` de la siguiente manera...

Si tenemos un panel de login y por lo que sea descubrimos el usuario, pero nos falta la contraseña, podremos hacerlo de la siguiente forma...

Mediante el `BurpSuit` capturamos la peticion del login, seguidamente donde pone `Username` y `Password` los cambiamos de la siguiente manera...

```
Username=admin&Password=admin
```

Quedaria de la siguiente manera en `BurpSuit`...

```
{"Username": "admin", "Password":{"$ne": "example"}}
```

Y con esto si funciona estaria `Bypasseado` el login haciendo una comparacion logica negativa, ya que estamos diciendo que `admin` no es igual a `example` por lo que te logea...

Todo esto esta reflejado en la siguiente pagina...

URL = https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/NoSQL%20Injection

Cuando hay un `NoSQL Injection` en alguna web o algo parecido por detras siempre suele haber un `mongoDB` por lo que si podemos entrar en la maquina y buscar por `mongo` si esta activa la base de datos podemos entrar en `mongo` poniendo lo siguiente...

```shell
mongo
```

O irnos a `/tmp` y hacer un volcado de las bases de datos de `mongo` haciendo lo siguiente...

```shell
mongodump
```

Y esto lo que hara sera crear una carpeta llamada `dump` con todas las bases de datos que esten dentro de `mongo` con su respectiva informacion, para poder ver posibles contraseñas...

Si encontramos un archivo dentro de la carpeta `dump` bastante interesante sobre un usuario y una contraseña pero se ve muy mal por que esta en formato `.bson` podremos hacer lo siguiente...

Imaginemos que el archivo se llama `user.bson`...

```shell
bsondump user.bson
```

Y esto te lo mostrara de manera mas clara toda la informacion...

