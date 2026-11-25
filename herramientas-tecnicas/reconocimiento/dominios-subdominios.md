---
icon: ethernet
---

# Dominios/Subdominios

## <mark style="color:purple;">Dominios de IP</mark>

Para saber si una `IP` tiene un dominio en concreto podremos hacer lo siguiente...

```shell
nslookup
> server <IP>
> <COMMAND_INFO>
> <IP>
> <DOMAIN_INFO>
```

## <mark style="color:purple;">whatweb</mark>

Para saber que tecnologias, gestores de contenidos, versiones de cada uno de ellos, etc... que estan corriendo detras de una web seria de la siguiente manera...

```shell
whatweb http://<IP>/
```

Con esto nos mostrara la informacion dicha anteriormente...

## <mark style="color:purple;">Subdominios</mark>

En vez de utilizar fuerza bruta y ahorarrtelo se puede utilizar otra tecnica con el siguiente comando...

```shell
dig @<IP> axfr #Enumerar los subdominios
```

Y con eso nos podria descubrir subdominios interesantes y si a parte tenemos un dominio a parte de nuestra `IP`...

```shell
dig @<IP> <DOMAIN> axfr
```

Tambien podriamos mirar otras interesantes...

```shell
dig @<IP> ns #Enumerar los name servers

dig @<IP> mx #Enumerar los servidores de correo
```

## <mark style="color:purple;">Wfuzz</mark>

Tambien podemos utilizar la herramienta `wfuzz` para poder descubrir `subdominios` a fuerza bruta, si en primer lugar ponemos el siguiente comando...

```shell
wfuzz -c -t 200 -w <WORDLIST> -H "Host: FUZZ.<TARGET>" http://<TARGET>
```

Lo que nos va hacer es que va a probar todas las palabras donde se encuentra la palabra `FUZZ` con los nombres del `wordlist` indicado, devolviendonos un codigo `200 OK`, pero si todas las palabras son un codigo `200 OK` y lo queremos filtrar por los `characters` que es como se suele hacer de primeras veremos que todas las respuestas que nos esta dando tienen unos determinados `characters`, por lo que pondremos un parametro extra para que nos oculte ese numero de `characters` y solo nos muestre el diferente que seria el correcto...

```shell
wfuzz -c --hh=<CHARACTERS_NUMBER> -t 200 -w <WORDLIST> -H "Host: FUZZ.<TARGET>" http://<TARGET>
```

Donde pone `<CHARACTERS_NUMBER>` tendremos que cambiarlo por los `characters` que queremos que no nos muestre...

De la misma forma si sabemos que tiene que ir una palabra por delante del `subdirectorio` la colocaremos antes con un `.` de `FUZZ`, todo esto se puede ir ajustando conforme a las necesidades de cada uno, ya que donde este la palabra `FUZZ` es donde pondra la fuerza bruta de las palabras del diccionario...

```shell
wfuzz -c --hh=<CHARACTERS_NUMBER> -t 200 -w <WORDLIST> -H "Host: <SUBDOMAIN>.FUZZ.<TARGET>" http://<TARGET>
```

Si por ejemplo quieres ocultar los `characters` que se repiten todo el rato dejando asi solo los distintos, haremos lo siguiente...

```shell
wfuzz -c --hc=404 --hh=<CHARACTERS_NUMBER> -t 200 -w <WORDLIST> "http://<IP>/FUZZ"
```

### Crear diccionario a-z

Para crear un diccionario de la a-z podremos automatizarlos todo con el siguiente comando...

```shell
for i in {a..z}; do echo $i; done
```

Info:

```
a
b
c
d
e
f
g
h
i
j
k
l
m
n
o
p
q
r
s
t
u
v
w
x
y
z
```

Y si lo queremos pasar a un archivo de texto...

```shell
for i in {a..z}; do echo $i; done > dic.txt
```

