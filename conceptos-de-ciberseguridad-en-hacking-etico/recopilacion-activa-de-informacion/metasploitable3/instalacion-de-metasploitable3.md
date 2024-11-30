# Instalacion de Metasploitable3

El repositorio de `GitHub` donde se encuentra esta maquina la cual su creador es `Rapid7` que es la organizacion que creo `metasploit`, esta misma maquina esta diseñada para tener vulnerabilidades las cuales podamos practicar con ella varias tecnicas.

URL = [Metasploitable3 GitHub](https://github.com/rapid7/metasploitable3)

Nos tendremos que ir a ese repositorio, seguidamente pincharemos en el link que nos proporciona con las imagenes `ISO` de las cuales vamos a utilizar del servidor de la nube `vagrant` que estara en el siguiente link:

URL = [Pagina ISO's Linux/Windows](https://portal.cloud.hashicorp.com/vagrant/discover/rapid7)

Y nos descargaremos la primera `ISO` de `Windows` en mi caso para `VMWare`, el que sea de `Virtual Box` que seleccione esa, pero en mi caso elegire `VMWare_desktop` ya que esta virtualizado y no estamos en un `host`:

URL = [ISO Windows VMWare\_desktop](https://portal.cloud.hashicorp.com/vagrant/discover/rapid7/metasploitable3-win2k8)

Y despues nos descargaremos la de `Linux` de la misma forma en mi caso la de `VMWare_desktop`:

URL = [ISO Linux VMWare\_desktop](https://portal.cloud.hashicorp.com/vagrant/discover/rapid7/metasploitable3-ub1404)

Una vez que tengamos descargados las `ISO's` las pasaremos a nuestro escritorio, para poder instalar estas maquinas vulnerables sin pagar mediante `VMWare` ya que en el repositorio si lo haces desde `VMWare` tendras que pagar en un paso determinado, se podra hacer de la siguiente forma:

Tendremos que darle click derecho al archivo y cambiar el nombre, solamente tendremos que ponerle al final del nombre `.zip` para que se interprete como un `.zip` (Comprimido), por lo que le volveremos a dar click derecho y `Extraer aqui`, esto lo que hara sera descomprimirnos la carpeta.

Una vez que se haya descomprimido, eliminaremos el archivo `.zip` que ya no nos hara falta, para que no nos ocupe tanto en el sistema.

Abriremos la carpeta descomprimida y encontraremos otro archivo de la misma forma que antes, por lo que le cambiaremos el nombre poniendole al final `.zip` de nuevo y lo extraeremos en esa misma carpeta.

Una vez echo eso, eliminaremos el archivo `.zip` y como resultado veremos archivos que ahora si nos sirven para importarlos a nuestro `VMWare`, si nos lo mete en carpetas, sacaremos todos esos archivos de las carpetas poniendolas en una carpeta unicamente paar que funcione.

<figure><img src="../../../.gitbook/assets/image (26).png" alt=""><figcaption></figcaption></figure>

Cambiaremos el nombre de la carpeta que contiene estos archivos por el que se identifique por la `ISO`, por ejemplo el de `windows` sera `metasploitable3-Win2008`, una vez echo todo esto, abriremos `VMWare`.

Le daremos a `File` -> `Open` -> seleccionaremos la carpeta donde estan los archivos de dicha maquina y solo nos aparecera un fichero de imagen, que sera el que tengamos que seleccionar, una vez seleccionado le daremos a `Abrir`.

Y con esto ya se nos abria importado la maquina `Metasploitable3-WindowsServer2008`.

Haremos lo mismo pero con el `Linux`.
