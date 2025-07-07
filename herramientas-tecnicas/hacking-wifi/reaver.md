---
icon: chart-network
---

# Reaver

Para el hacking wifi hay una herramienta muy utilizada llamada `Reaver` o tambien `wpspingenerator` de `wifislax`...

Para hacer auditorias wifi se utilizaria la herramienta `wifimosys`...

Por lo que `Reaver` se utilizaria de la siguiente manera...

> EJEMPLO

Supongamos que estamos en una maquina que al hacer `ifconfig` vemos que hay una red en modo monitor, que se suele asignar el nombre tipico de `mon0` dependiendo de cuantas redes haya...

Como esta herramienta solo se puede ejecutar con privilegios de `root` como usuario normal no se podria tocar, pero si hacemos...

```shell
getcap -r / 2>/dev/null
```

Para ver las `capabilitys` que tiene dicho usuario y vemos que entre ellas esta la siguiente...

```
/usr/bin/reaver = cap_net_raw+ep
```

Veremos que podremos ejecutar ese binario como si lo estuviera ejecutando `root` por decirlo de alguna manera, por lo que lo podremos utilizar para la red que esta en modo monitor u otras posibles redes wifi que empiezan con el termino `wlan`...

```shell
iw dev
```

Con esto podremos ver de forma mas detallada la estructura de redes como esta compuesta e identificar el `Punto de Acceso` a la red representado como `AP`...

```
Type AP
```

Se veria algo como lo de arriba...

Tambien viendo que el `ssid` es `OpenWrt` por lo que supongamos que esa red que simula tener un punto de acceso se llama `wlan0`...

Identificando de esa red la `pssid` que se representa como la `MAC` llamada `addr` y la red en modo monitor llamada `mon0` podremos explotar esto...

Ya que necesitamos la `addr` de un tipo que sea `AP` (Punto de Acceso) para acceder y despues poniendo la red que esta en modo monitor para capturarlo por asi decirlo con la herramienta dicha anteriormente...

```shell
reaver -i mon0 -b <ADDR_WLAN0> -vv
```

Una vez hecho esto te mostrara el parametro `WPS PIN` con el `PIN` de la misma red y el parametro `WPA PSK` con la contraseña en texto plano...

Por lo que habria funcionado y tendramos la contraseña de algun posible usuario o de alguna posible red wifi...

