---
icon: ubuntu
---

# Linux Ubuntu-Windows Server 2008 - Metasploitable3

Empezando por la de `ubuntu` las credenciales por defecto seran:

```
User: vagrant
Pass: vagrant
```

Una vez dentro, le daremos click derecho a la pestaña de la maquina `ubuntu` y nos iremos a `Settings` -> `Network Adapter` -> lo cambiaremos a la opcion `Host-only`.

Despues para que nos de la IP mas rapido, pondremos el siguiente comando:

```shell
sudo dhclient
```

Con esto lo que estas haciendo es forzar a que nos de una direccion IP, por lo que si ponemos el ocmando `ip a` podremos ver la direccion IP que nos ha dado.

En mi caso me ha dado la `192.168.16.129/24`.

Vamos a modificar una regla del `iptables` que es como un `firewall` de sistema operativo, para que no se limite ninguna conexion con todas las maquinas que esten conectadas a nuestro entorno, lo haremos de la siguiente forma:

```shell
sudo iptables -F
```

Con esto ya habriamos eliminado cualquier restriccion de lo que comente antes.

Y con la de `Windows` haremos lo mismo, la pondremos en `Host-only`, en mi caso me dara la siguiente IP... (`192.168.16.130/24`)

En la maquina `windows` le daremos click derecho al adaptador de red -> `Open Network and Sharing center` -> `Changue advanced sharing settings` y ponemos todo a `On` lo que este en `off`.

<figure><img src="../../../.gitbook/assets/image (27) (1).png" alt=""><figcaption></figcaption></figure>

Con esto lo que estamos haciendo es que esta maquina se pueda comunicar con otros `nodos` (Maquinas) para posteriormente poder ser explotadas.
