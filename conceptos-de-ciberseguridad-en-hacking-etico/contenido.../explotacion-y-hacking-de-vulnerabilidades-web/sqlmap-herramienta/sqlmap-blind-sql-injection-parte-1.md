# SQLmap (Blind SQL Injection - Parte 1)

Este tipo de injecciones de `sql` se hacen cuando no te dan ningun tipo de error al introducir algo de forma erronea, vamos por asi decirlo a ciegas, pero sabemos que hay algo detras el cual se puede aprovechar, por lo que podremos ir probando haciendo lo siguiente.

Por ejemplo tenemos nuestro usuario con contraseña, por lo que vamos a probar a introducir una condicion que se va a cumplir a parte de nuestras credenciales.

```
User: santiago' and 'h'='h
Pass: password
```

Y veremos que nos muestra los resultados correctamente, por lo que sabemos que se esta ejecutando un `mysql` por dentras.

Por lo que cuando sabemos que poniendo estas condiciones sabemos que estamos injectando codigo, podemos utilizar algun script o de forma manual en el que haga la siguiente condicion para ir sabiendo cuando hace una consulta correcta y cuando no, por ejemplo si la pagina nos devuelve un `Ok` cuando es una consulta correcta habremos descubierto la primera letras del usuario que queramos saber, cuando sea `bad` sabremos que esa no es, por lo que poco a poco sacaremos las credenciales de algun usuario, nombres de tablas, etc...

Si nosotros ponemos `current_user()` nos devuelve el nombre de usuario con el que se esta iniciado en la base de datos de `mysql`, pero como no podremos ver el resultado lo que haremos seran comparaciones con las letras del abecedario, para ir sabiendo las respuestas del servidor con `substring(<CONSULTA>,1,1)` con esto indicamos que nos diga la primera letra del usuario y despues le haremos una comparacion con la primera letras del abecedario y asi de forma sucesiva.

```
User: santiago' and substring(current_user(),1,1)='a
Pass: password
```

(Sabemos que el usuario por detras es `root`, por lo que si ponemos eso anterior va a dar fallo.)

Pero si ahora ponemos lo siguiente:

```
User: santiago' and substring(current_user(),1,1)='r
Pass: password
```

Veremos que nos carga la pagina correctamente y nos da un `Ok`, por lo que sabemos que la primera letra del usuario es `r` y asi sucesivamente.

Pero si por lo que sea, no tenemos ni si quiera un `Ok` o un `bad` para ir comparando cual esta bien o cual esta mal, lo que podemos hacer es jugar con los tiempos de respuesta con los `sleep()`, de la siguiente forma:

```
User: santiago' and sleep(5) and substring(current_user(),1,1)='r
Pass: password
```

Y con esto si tarda `5` segundos en responder la pagina es correcto y si no es erroneo utilizando una especie de `boolean`.

Y todo esto anterior es lo que va a utilizar `sqlmap` de forma automatica, todo esto lo explico para que se vea como se haria de forma interna toda la injeccion y como `sqlmap` lo suele hacer.
