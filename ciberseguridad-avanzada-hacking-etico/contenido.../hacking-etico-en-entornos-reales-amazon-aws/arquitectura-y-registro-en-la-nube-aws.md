---
icon: cloud
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

# Arquitectura y registro en la nube (AWS)

Vamos a montarnos una infraestructura en la nube de `amazon` (`AWS`) para que todo esto sea mas realista y lo vamos a configurar de tal manera que tenga `valanceadores`, herramientas de seguridad, subredes, etc.. Para que todo esto sea mas realista, esta sera la estructura que crearemos:

<figure><img src="../../../.gitbook/assets/image (14).png" alt=""><figcaption></figcaption></figure>

Vamos a meterle una aplicacion web que estara corriendo, en concreto correra esta aplicacion web que se puede encontrar en el siguiente repositorio:

URL = [PaginaWeb Instalador GitHub](https://github.com/aws-samples/simple-phonebook-web-application)

Ahora tendremos que irnos a la consola de administracion de la nube de `amazon` pero nos tendremos que crear una cuenta:

URL = [Consola de AWS Pagina](https://aws.amazon.com/es/console/)

**1. Creación de la cuenta de AWS**

Accedemos a la página de AWS y pulsamos sobre “Cree una cuenta de AWS”

<figure><img src="../../../.gitbook/assets/image (15).png" alt=""><figcaption></figcaption></figure>

Completamos el formulario de registro. Asegúrate de elegir el tipo de cuenta personal y el _support plan_ gratuito.

<figure><img src="../../../.gitbook/assets/image (16).png" alt=""><figcaption></figcaption></figure>

Una vez completado el registro, accedemos a nuestra cuenta introduciendo el correo electrónico y la contraseña en el formulario de login.

<figure><img src="../../../.gitbook/assets/image (17).png" alt=""><figcaption></figcaption></figure>

La interfaz que se muestra inmediatamente después de realizar el _login_ se corresponde con la consola de administración de AWS. En la esquina superior derecha podemos acceder a los detalles de nuestra cuenta y a nuestro número de cuenta, que utilizaremos más adelante para acceder a la consola de administración.

<figure><img src="../../../.gitbook/assets/image (18).png" alt=""><figcaption></figcaption></figure>

Por defecto, el acceso a la información económica solo está disponible únicamente para el usuario root.

Es una buena práctica restringir el uso de la cuenta root únicamente a operaciones críticas, por lo tanto, vamos a permitir el acceso a la actividad económica utilizando una política de IAM.

Para ello, pulsamos en **“Mi cuenta”** y hacemos _scroll_ hacia abajo hasta llegar al apartado que se muestra a continuación.

<figure><img src="../../../.gitbook/assets/image (19).png" alt=""><figcaption></figcaption></figure>

Pulsamos en **“Editar”** y marcamos la casilla **“Active el acceso de IAM”** y pulsamos sobre **“Actualizar”**

<figure><img src="../../../.gitbook/assets/image (20).png" alt=""><figcaption></figcaption></figure>

**Importante:** En la parte inferior de la página tienes las opciones para cerrar tu cuenta de AWS en el caso de que no quieras seguir utilizándola después de las clases y quieras asegurarte de que no se realizan cobros a tu cuenta.

<figure><img src="../../../.gitbook/assets/image (21).png" alt=""><figcaption></figcaption></figure>

**2. Seguridad de la cuenta de AWS**

Vamos a continuar con la seguridad de nuestra cuenta de AWS y para ello, vamos a comenzar realizando algunos cambios sobre el servicio _IAM (Identity and Access Management)_

En la barra de búsqueda escribimos **“IAM”** y pulsamos sobre el servicio.

<figure><img src="../../../.gitbook/assets/image (22).png" alt=""><figcaption></figcaption></figure>

Lo primero que vemos al acceder al panel de IAM es una alerta de seguridad que nos indica que no tenemos activado el múltiple factor de autenticación (MFA). Pulsamos sobre **“Agregar MFA”**.

<figure><img src="../../../.gitbook/assets/image (23).png" alt=""><figcaption></figcaption></figure>

En la ventana que aparece, pulsamos sobre **“Activar MFA”**

<figure><img src="../../../.gitbook/assets/image (24).png" alt=""><figcaption></figcaption></figure>

Como podemos observar, AWS soporta diferentes tipos de autenticación de múltiple factor, en nuestro caso seleccionamos **“Dispositivo MFA virtual”** y pulsamos en **“continuar”**

<figure><img src="../../../.gitbook/assets/image (25).png" alt=""><figcaption></figcaption></figure>

Utiliza una aplicación de autenticación para leer el QR que se muestra en pantalla. Entre las aplicaciones más conocidas para soportar este tipo de MFA se encuentran: _Google Authenticator y Microsoft Authenticator._

Tras leer el código QR automáticamente debería aparecer un código en la aplicación que debemos introducir en los cuadros de texto.

<figure><img src="../../../.gitbook/assets/image (26).png" alt=""><figcaption></figcaption></figure>

Tras introducir los dos códigos OTP (_One Time Password_) debería mostrarse un mensaje indicando que nuestra cuenta tiene el MFA configurado.

<figure><img src="../../../.gitbook/assets/image (27).png" alt=""><figcaption></figcaption></figure>

**3. Creación de un usuario de AWS**

Tal y como se comentaba anteriormente, la cuenta root solo debe utilizarse para actividades críticas, esto es debido a que tiene privilegios para realizar cualquier tipo de acción sobre la cuenta de AWS.

Para evitar utilizar la cuenta de root para nuestra actividad diaria, vamos a crear otro usuario dentro de nuestro entorno de AWS con el que accederemos habitualmente.

Para ello, dentro del panel de IAM pulsamos sobre usuarios y después sobre **“Agregar usuarios”.**

<figure><img src="../../../.gitbook/assets/image (28).png" alt=""><figcaption></figcaption></figure>

Introducimos un nombre para el usuario, por ejemplo, **“TESTUSER”** y activamos la opción **“Contraseña: acceso a la consola de administración de AWS”** y **“Contraseña personalizada”**.

Introducimos una contraseña robusta y desactivamos la opción **“Requerir el restablecimiento de contraseña”**. Pulsamos en **“Siguiente: Permisos”**

<figure><img src="../../../.gitbook/assets/image (29).png" alt=""><figcaption></figcaption></figure>

En la nueva pantalla que aparece, pulsamos sobre **“Crear un grupo”.**

<figure><img src="../../../.gitbook/assets/image (30).png" alt=""><figcaption></figcaption></figure>

Introducimos un nombre para el grupo, por ejemplo **“Console-Admin”** y seleccionamos el permiso **“AdministratorAccess”**. Pulsamos sobre **“Crear un grupo”**.

<figure><img src="../../../.gitbook/assets/image (32).png" alt=""><figcaption></figcaption></figure>



Asegúrate de que **“Console-Admin”** esta seleccionado y pulsa sobre **“Siguiente: Etiquetas”**

<figure><img src="../../../.gitbook/assets/image (33).png" alt=""><figcaption></figcaption></figure>



Pulsamos **“Siguiente: Revisar”** sin añadir ninguna etiqueta. Finalmente, revisamos que todos los datos son correctos y pulsamos sobre **“Crear un usuario”.**

<figure><img src="../../../.gitbook/assets/image (34).png" alt=""><figcaption></figcaption></figure>



**4. Alias para la cuenta de AWS**

En lugar utilizar el ID de cuenta para acceder a la consola de administración de AWS, vamos a configurar un alias.

En el panel de IAM, pulsamos sobre **“Crear”** en la esquina superior derecha.

<figure><img src="../../../.gitbook/assets/image (35).png" alt=""><figcaption></figcaption></figure>



En el cuadro de texto introducimos un alias. El alias debe ser único, por ejemplo **“**_**testuser-\[Iniciales de tu nombre]”**_

Una vez hecho esto ya tenemos todo listo para comenzar. Cerramos sesión de la cuenta y volvemos a iniciar sesión.

En el inicio de sesión, seleccionamos **“Usuario de IAM”** e introducimos el alias de la cuenta.

<figure><img src="../../../.gitbook/assets/image (36).png" alt=""><figcaption></figcaption></figure>



Después, introducimos el nombre de usuario (**“TESTUSER”**) y la contraseña que establecimos en los pasos anteriores y pulsamos sobre **“Iniciar Sesión”**.

Para terminar, podemos añadir `MFA` para la cuenta `TESTUSER` de la misma forma que hicimos para el usuario `root`.

<figure><img src="../../../.gitbook/assets/image (38).png" alt=""><figcaption></figcaption></figure>

Y con esto ya tendremos una cuenta de `amazon` para la nube creada de forma correcta y bien configurada.
