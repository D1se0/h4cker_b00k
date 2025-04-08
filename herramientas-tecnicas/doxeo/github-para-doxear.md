---
icon: github
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

# GitHub Para Doxear

En `GitHub` tambien se puede utilizar para doxear a alguien, como veremos despues, es una pagina en la que se pueden hacer bastante cosas, desde subir repositorios, crear ayudas en diversidad de modalidades de trabajo, etc... Hasta poder doxear a alguien mediante su perfil de `GitHub`.

URL = [Pagina GitHub](https://github.com)

Si nos vamos algun perfil de algun usuario al que queremos investigar (Doxear) y nos vamos en la parte de `Repositorios` para ver sus repositorios, nos iremos a los mas antiguos para asegurarnos que no estan muy bien protegidos, por lo que entrariamos a dicho `repositorio`, dentro de el veremos una opcion llamada `<NUMBER> Commits` que sera el numero de actualizaciones que le habra echo al repositorio:

<figure><img src="../../.gitbook/assets/image (2) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Esto dependera del `repositorio`, si le pinchamos y vamos dentro, veremos algunos que estan verificados y otros que no, los `verificados` suelen tener mas proteccion, pero igualmente podremos ver informacion, por lo que probaremos a entrar en algun verificado de la siguiente forma.

<figure><img src="../../.gitbook/assets/image (3) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Donde pone el numero `2f72...` pincharemos en el y nos llevara a una pagina donde se mostrara la actualizacion del `commit` que se hizo, pero eso no nos interesa, por lo que en la URL al final de ella pondremos lo siguiente.

```
URL = https://github.com/User/Repositorio/commit/2f727067d617ec4b82ea8f2843b6e4a19d9a76c5.patch
```

Tendremos que añadirle al final el nombre de `.patch` lo que nos llevara a una parte donde veremos la informacion delicada de dicho usuario pudiendo saber de forma codificada su nombre, correo electronico, etc... Pero ya digo con la `verificacion` estara de forma codificada, si queremos verlo en texto plano, podremos hacer lo siguiente.

Nos iremos donde estan todos los `Commits` y ahora buscaremos uno que no este `verificado` a poder ser el primero `commit` que se hizo estando abajo del todo de la pagina.

<figure><img src="../../.gitbook/assets/image (4) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Le daremos al numero y realizaremos el mismo proceso anterior, poniendo el `.patch` al final de la URL, por lo que vemos ahora si se podra ver la informacion del usuario como su nombre, correo electronico, fecha, etc... Sin estar codificado, por lo que con esta informacion podremos echar mano de otras paginas de doxeo para seguir la investigacion.
