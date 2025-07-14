---
icon: hard-drive
layout:
  width: default
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

# Herramienta Volatility2/3 + LAB

## Fase 1

Lo primero a la hora de sacar la principal informacion de un archivo de la imagen del sistema para realizar el análisis forense es lo siguiente.

Utilizaremos la herramienta `Volatility` la cual nos podremos descargar en el siguiente repositorio de `GitHub`.

URL = [Download Volatility](https://github.com/volatilityfoundation/volatility3)

Una vez descargado, podremos probarla ejecutando el siguiente comando.

```shell
./vol.py -h
```

Info:

```
Volatility 3 Framework 2.26.2
usage: vol.py [-h] [-c CONFIG] [--parallelism [{processes,threads,off}]] [-e EXTEND] [-p PLUGIN_DIRS] [-s SYMBOL_DIRS] [-v] [-l LOG] [-o OUTPUT_DIR] [-q]
              [-r RENDERER] [-f FILE] [--write-config] [--save-config SAVE_CONFIG] [--clear-cache] [--cache-path CACHE_PATH] [--offline | -u URL]
              [--filters FILTERS] [--hide-columns [HIDE_COLUMNS ...]] [--single-location SINGLE_LOCATION] [--stackers [STACKERS ...]]
              [--single-swap-locations [SINGLE_SWAP_LOCATIONS ...]]
              PLUGIN ...

An open-source memory forensics framework

options:
  -h, --help            Show this help message and exit, for specific plugin options use 'vol.py <pluginname> --help'
  -c, --config CONFIG   Load the configuration from a json file
  --parallelism [{processes,threads,off}]
                        Enables parallelism (defaults to off if no argument given)
  -e, --extend EXTEND   Extend the configuration with a new (or changed) setting
  -p, --plugin-dirs PLUGIN_DIRS
                        Semi-colon separated list of paths to find plugins
  -s, --symbol-dirs SYMBOL_DIRS
                        Semi-colon separated list of paths to find symbols
  -v, --verbosity       Increase output verbosity
  -l, --log LOG         Log output to a file as well as the console
  -o, --output-dir OUTPUT_DIR
                        Directory in which to output any generated files
  -q, --quiet           Remove progress feedback
  -r, --renderer RENDERER
                        Determines how to render the output (quick, none, csv, pretty, json, jsonl)
  -f, --file FILE       Shorthand for --single-location=file:// if single-location is not defined
  --write-config        Write configuration JSON file out to config.json
  --save-config SAVE_CONFIG
                        Save configuration JSON file to a file
  --clear-cache         Clears out all short-term cached items
  --cache-path CACHE_PATH
                        Change the default path (/root/.cache/volatility3) used to store the cache
  --offline             Do not search online for additional JSON files
  -u, --remote-isf-url URL
                        Search online for ISF json files
  --filters FILTERS     List of filters to apply to the output (in the form of [+-]columname,pattern[!])
  --hide-columns [HIDE_COLUMNS ...]
                        Case-insensitive space separated list of prefixes to determine which columns to hide in the output if provided
  --single-location SINGLE_LOCATION
                        Specifies a base location on which to stack
  --stackers [STACKERS ...]
                        List of stackers
  --single-swap-locations [SINGLE_SWAP_LOCATIONS ...]
                        Specifies a list of swap layer URIs for use with single-location

Plugins:
..................................<RESTO_HELP>.....................................
```

Vemos que esta funcionando de forma correcta, por lo que ya podremos utilizarla.

Si por ejemplo queremos utilizar la de `Volatility2` o `Volatility`, podremos descargarnoslo en este repositorio de `GitHub` tambien del mismo creador, pero ya esta un poco desactualizado.

URL = [Download Volatility2 GitHub](https://github.com/volatilityfoundation/volatility)

Una vez descargado, le daremos permisos de ejeccion ya que viene sin ellos.

```shell
chmod +x vol.py
```

Ahora entraremos a nivel de codigo con `nano` y cambiaremos la siguiente linea:

```python
#!/usr/bin/env python
```

Por esta:

```python
#!/usr/bin/env python2
```

Lo guardamos y ahora la probaremos de esta forma:

```shell
./vol.py -h
```

Info:

```
Volatility Foundation Volatility Framework 2.6.1
Usage: Volatility - A memory forensics analysis platform.

Options:
  -h, --help            list all available options and their default values.
                        Default values may be set in the configuration file
                        (/etc/volatilityrc)
  --conf-file=/root/.volatilityrc
                        User based configuration file
  -d, --debug           Debug volatility
  --plugins=PLUGINS     Additional plugin directories to use (colon separated)
  --info                Print information about all registered objects
  --cache-directory=/root/.cache/volatility
                        Directory where cache files are stored
  --cache               Use caching
  --tz=TZ               Sets the (Olson) timezone for displaying timestamps
                        using pytz (if installed) or tzset
  -f FILENAME, --filename=FILENAME
                        Filename to use when opening an image
  --profile=WinXPSP2x86
                        Name of the profile to load (use --info to see a list
                        of supported profiles)
  -l LOCATION, --location=LOCATION
                        A URN location from which to load an address space
  -w, --write           Enable write support
  --dtb=DTB             DTB Address
  --shift=SHIFT         Mac KASLR shift address
  --output=text         Output in this format (support is module specific, see
                        the Module Output Options below)
  --output-file=OUTPUT_FILE
                        Write output in this file
  -v, --verbose         Verbose information
  --physical_shift=PHYSICAL_SHIFT
                        Linux kernel physical shift address
  --virtual_shift=VIRTUAL_SHIFT
                        Linux kernel virtual shift address
  -g KDBG, --kdbg=KDBG  Specify a KDBG virtual address (Note: for 64-bit
                        Windows 8 and above this is the address of
                        KdCopyDataBlock)
  --force               Force utilization of suspect profile
  -k KPCR, --kpcr=KPCR  Specify a specific KPCR address
  --cookie=COOKIE       Specify the address of nt!ObHeaderCookie (valid for
                        Windows 10 only)

        Supported Plugin Commands:
..................................<RESTO_HELP>.....................................
```

Vemos que funciona de forma correcta.

Tambien podemos ver como se utiliza en esta pagina:

URL = [Info Uso de Volatility](https://book.hacktricks.wiki/en/generic-methodologies-and-resources/basic-forensic-methodology/memory-dump-analysis/volatility-cheatsheet.html)

Ahora vamos a entrar en un repositorio de `GitHub` donde descargarnos imagenes ya preparadas para parcticar esto mismo.

URL = [GitHub Labs Analisis Forense](https://github.com/stuxnet999/MemLabs)

Vamos a irnos a `Lab 0` y dentro clicaremos el link del `drive` que nos descarga dicho archivo, lo descomprimiremos y ahora vamos a empezar con el analisis forense con la herramienta `Volatility3` con dicho archivo.

### Obtener información del sistema de la imagen

Vamos a probarlo tanto para la `v2` como para la `v3` ya que cambian en las dos versiones de `volatility`.

#### Volatility2

```shell
./vol.py -f Challenge.raw imageinfo
```

Info:

```
INFO    : volatility.debug    : Determining profile based on KDBG search...
          Suggested Profile(s) : Win7SP1x86_23418, Win7SP0x86, Win7SP1x86_24000, Win7SP1x86
                     AS Layer1 : IA32PagedMemoryPae (Kernel AS)
                     AS Layer2 : FileAddressSpace (/home/kali/Desktop/volatility/Challenge.raw)
                      PAE type : PAE
                           DTB : 0x185000L
                          KDBG : 0x8273cb78L
          Number of Processors : 1
     Image Type (Service Pack) : 1
                KPCR for CPU 0 : 0x80b96000L
             KUSER_SHARED_DATA : 0xffdf0000L
           Image date and time : 2018-10-23 08:30:51 UTC+0000
     Image local date and time : 2018-10-23 14:00:51 +0530
```

#### Volatility3

```shell
./vol.py -f Challenge.raw windows.info
```

Info:

```
Volatility 3 Framework 2.26.2
Progress:  100.00               PDB scanning finished                                                                                              
Variable        Value

Kernel Base     0x82604000
DTB     0x185000
Symbols file:///home/kali/Desktop/volatility3/volatility3/symbols/windows/ntkrpamp.pdb/EDD3760CEE2B45D2A63BF8C26EE11FAF-2.json.xz
Is64Bit False
IsPAE   True
layer_name      0 WindowsIntelPAE
memory_layer    1 FileLayer
KdDebuggerDataBlock     0x8273cb78
NTBuildLab      7601.24260.x86fre.win7sp1_ldr.18
CSDVersion      1
KdVersionBlock  0x8273cb50
Major/Minor     15.7601
MachineType     332
KeNumberProcessors      1
SystemTime      2018-10-23 08:30:51+00:00
NtSystemRoot    C:\Windows
NtProductType   NtProductWinNt
NtMajorVersion  6
NtMinorVersion  1
PE MajorOperatingSystemVersion  6
PE MinorOperatingSystemVersion  1
PE Machine      332
PE TimeDateStamp        Sun Sep  9 00:14:23 2018
```

Con esto sabremos el `profile` determinado (El `S.O.` especifico que es) para posteriormente poder ejecutar los comandos correctos respecto al sistema que sea.

### Obtener información de la memoria RAM

#### Volatility2

```shell
./vol.py -f Challenge.raw kdbgscan
```

Info:

```
**************************************************
Instantiating KDBG using: /home/kali/Desktop/volatility/Challenge.raw WinXPSP2x86 (5.1.0 32bit)
Offset (P)                    : 0x273cb78
KDBG owner tag check          : True
Profile suggestion (KDBGHeader): Win7SP1x86_23418
Version64                     : 0x273cb50 (Major: 15, Minor: 7601)
PsActiveProcessHead           : 0x82751d70
PsLoadedModuleList            : 0x82759730
KernelBase                    : 0x82604000

**************************************************
Instantiating KDBG using: /home/kali/Desktop/volatility/Challenge.raw WinXPSP2x86 (5.1.0 32bit)
Offset (P)                    : 0x273cb78
KDBG owner tag check          : True
Profile suggestion (KDBGHeader): Win7SP1x86
Version64                     : 0x273cb50 (Major: 15, Minor: 7601)
PsActiveProcessHead           : 0x82751d70
PsLoadedModuleList            : 0x82759730
KernelBase                    : 0x82604000

**************************************************
Instantiating KDBG using: /home/kali/Desktop/volatility/Challenge.raw WinXPSP2x86 (5.1.0 32bit)
Offset (P)                    : 0x273cb78
KDBG owner tag check          : True
Profile suggestion (KDBGHeader): Win7SP1x86_24000
Version64                     : 0x273cb50 (Major: 15, Minor: 7601)
PsActiveProcessHead           : 0x82751d70
PsLoadedModuleList            : 0x82759730
KernelBase                    : 0x82604000

**************************************************
Instantiating KDBG using: /home/kali/Desktop/volatility/Challenge.raw WinXPSP2x86 (5.1.0 32bit)
Offset (P)                    : 0x273cb78
KDBG owner tag check          : True
Profile suggestion (KDBGHeader): Win7SP0x86
Version64                     : 0x273cb50 (Major: 15, Minor: 7601)
PsActiveProcessHead           : 0x82751d70
PsLoadedModuleList            : 0x82759730
KernelBase                    : 0x82604000
```

#### Volatility3

Para `Volatility3` al realizar el comando anterior de obtener informacion, ya de forma automatica hace lo del `kdbgscan` de `volatility2`, por lo que seria el mismo comando que el anterior de esta version.

Con esto obtenemos informacion respecto al `dump` de la memoria `RAM` solo que no se suele utilizar mucho si no es un caso real.

Esta seria la primera fase de informacion que siempre tendremos que hacer para recopilar la informacion esencial desde la memoria `RAM` del `dump`.

## Fase 2

### Obtener los procesos activos de cuando se realizo el dump del archivo

Vamos a ejecutar el parametro de `pstree` que nos muestra todos los procesos de memoria `RAM` en formato de árbol (Proceso padre, hijo, subprocesos, etc...).

#### Volatility2

El `--profile=...` vamos a obtenerlo del anterior comando que ejecutamos en la linea llamada `Suggested Profile(s)` mismamente el primer nombre sirve.

```shell
./vol.py -f Challenge.raw --profile=Win7SP1x86_23418 pstree
```

Info:

```
Name                                                  Pid   PPid   Thds   Hnds Time
-------------------------------------------------- ------ ------ ------ ------ ----
 0x84d93c68:wininit.exe                               388    332      3     79 2018-10-23 08:29:23 UTC+0000
. 0x84debd20:services.exe                             484    388     10    191 2018-10-23 08:29:25 UTC+0000
.. 0x84e8c648:svchost.exe                             896    484     30    809 2018-10-23 08:29:33 UTC+0000
.. 0x84e41708:VBoxService.ex                          652    484     12    116 2018-10-23 08:29:31 UTC+0000
.. 0x84e7ad20:svchost.exe                             804    484     19    378 2018-10-23 08:29:32 UTC+0000
... 0x84ea7d20:audiodg.exe                            988    804      6    127 2018-10-23 08:29:35 UTC+0000
.. 0x84f7d578:svchost.exe                            1460    484     11    148 2018-10-23 08:29:44 UTC+0000
.. 0x84f323f8:spoolsv.exe                            1336    484     16    295 2018-10-23 08:29:43 UTC+0000
.. 0x850b2538:taskhost.exe                            308    484      8    151 2018-10-23 08:29:55 UTC+0000
.. 0x850d0030:sppsvc.exe                             1164    484      6    154 2018-10-23 08:29:57 UTC+0000
.. 0x84e54030:svchost.exe                             716    484      9    243 2018-10-23 08:29:32 UTC+0000
.. 0x84e84898:svchost.exe                             848    484     20    400 2018-10-23 08:29:33 UTC+0000
... 0x85109030:dwm.exe                               1992    848      5    132 2018-10-23 08:30:04 UTC+0000
.. 0x84f4dca0:svchost.exe                            1364    484     19    307 2018-10-23 08:29:43 UTC+0000
.. 0x84f828f8:svchost.exe                            1488    484      8    170 2018-10-23 08:29:44 UTC+0000
.. 0x84e89c68:svchost.exe                             872    484     19    342 2018-10-23 08:29:33 UTC+0000
.. 0x85164030:SearchIndexer.                         2032    484     14    614 2018-10-23 08:30:14 UTC+0000
... 0x8515cd20:SearchFilterHo                        1292   2032      5     80 2018-10-23 08:30:17 UTC+0000
... 0x8515ad20:SearchProtocol                         284   2032      7    235 2018-10-23 08:30:16 UTC+0000
.. 0x84f033c8:svchost.exe                            1192    484     15    365 2018-10-23 08:29:40 UTC+0000
.. 0x84e23030:svchost.exe                             592    484     12    358 2018-10-23 08:29:30 UTC+0000
. 0x84def3d8:lsass.exe                                492    388      7    480 2018-10-23 08:29:25 UTC+0000
. 0x84df2378:lsm.exe                                  500    388     10    146 2018-10-23 08:29:25 UTC+0000
 0x84d69030:csrss.exe                                 340    332      8    347 2018-10-23 08:29:21 UTC+0000
 0x83d09c58:System                                      4      0     85    483 2018-10-23 08:29:16 UTC+0000
. 0x8437db18:smss.exe                                 260      4      2     29 2018-10-23 08:29:16 UTC+0000
 0x85097870:explorer.exe                              324   1876     33    827 2018-10-23 08:30:04 UTC+0000
. 0x845a8d20:DumpIt.exe                              2412    324      2     38 2018-10-23 08:30:48 UTC+0000
. 0x851a6610:cmd.exe                                 2096    324      1     22 2018-10-23 08:30:18 UTC+0000
. 0x85135af8:VBoxTray.exe                            1000    324     14    159 2018-10-23 08:30:08 UTC+0000
 0x84dcbd20:winlogon.exe                              424    372      6    117 2018-10-23 08:29:23 UTC+0000
 0x84d8d030:csrss.exe                                 380    372      9    188 2018-10-23 08:29:23 UTC+0000
. 0x84d83d20:conhost.exe                             2424    380      2     51 2018-10-23 08:30:48 UTC+0000
. 0x851a5cd8:conhost.exe                             2104    380      2     52 2018-10-23 08:30:18 UTC+0000
```

#### Volatility3

En este caso no hace falta especificar el `profile` ya que lo detecta de forma automatica.

```shell
./vol.py -f Challenge.raw windows.pstree
```

Info:

```
Volatility 3 Framework 2.26.2
Progress:  100.00               PDB scanning finished                        
PID     PPID    ImageFileName   Offset(V)       Threads Handles SessionId       Wow64   CreateTime      ExitTime        Audit   Cmd     Path

4       0       System  0x83d09c58      85      483     N/A     False   2018-10-23 08:29:16.000000 UTC  N/A     -       -       -
* 260   4       smss.exe        0x8437db18      2       29      N/A     False   2018-10-23 08:29:16.000000 UTC  N/A     \Device\HarddiskVolume2\Windows\System32\smss.exe    \SystemRoot\System32\smss.exe   \SystemRoot\System32\smss.exe
340     332     csrss.exe       0x84d69030      8       347     0       False   2018-10-23 08:29:21.000000 UTC  N/A     \Device\HarddiskVolume2\Windows\System32\csrss.exe   %SystemRoot%\system32\csrss.exe ObjectDirectory=\Windows SharedSection=1024,12288,512 Windows=On SubSystemType=Windows ServerDll=basesrv,1 ServerDll=winsrv:UserServerDllInitialization,3 ServerDll=winsrv:ConServerDllInitialization,2 ServerDll=sxssrv,4 ProfileControl=Off MaxRequestThreads=16   C:\Windows\system32\csrss.exe
380     372     csrss.exe       0x84d8d030      9       188     1       False   2018-10-23 08:29:23.000000 UTC  N/A     \Device\HarddiskVolume2\Windows\System32\csrss.exe   %SystemRoot%\system32\csrss.exe ObjectDirectory=\Windows SharedSection=1024,12288,512 Windows=On SubSystemType=Windows ServerDll=basesrv,1 ServerDll=winsrv:UserServerDllInitialization,3 ServerDll=winsrv:ConServerDllInitialization,2 ServerDll=sxssrv,4 ProfileControl=Off MaxRequestThreads=16   C:\Windows\system32\csrss.exe
* 2104  380     conhost.exe     0x851a5cd8      2       52      1       False   2018-10-23 08:30:18.000000 UTC  N/A     \Device\HarddiskVolume2\Windows\System32\conhost.exe \??\C:\Windows\system32\conhost.exe "9597847671419376088700206021-7055470871162148935-704730587-1400429052-1906668177   C:\Windows\system32\conhost.exe
* 2424  380     conhost.exe     0x84d83d20      2       51      1       False   2018-10-23 08:30:48.000000 UTC  N/A     \Device\HarddiskVolume2\Windows\System32\conhost.exe \??\C:\Windows\system32\conhost.exe "499080522-1749980471992366858-146566314551631531-193375578852495345-1447858489     C:\Windows\system32\conhost.exe
388     332     wininit.exe     0x84d93c68      3       79      0       False   2018-10-23 08:29:23.000000 UTC  N/A     \Device\HarddiskVolume2\Windows\System32\wininit.exe wininit.exe     C:\Windows\system32\wininit.exe
* 500   388     lsm.exe 0x84df2378      10      146     0       False   2018-10-23 08:29:25.000000 UTC  N/A     \Device\HarddiskVolume2\Windows\System32\lsm.exe     C:\Windows\system32\lsm.exe     C:\Windows\system32\lsm.exe
* 484   388     services.exe    0x84debd20      10      191     0       False   2018-10-23 08:29:25.000000 UTC  N/A     \Device\HarddiskVolume2\Windows\System32\services.exe        C:\Windows\system32\services.exe        C:\Windows\system32\services.exe
** 896  484     svchost.exe     0x84e8c648      30      809     0       False   2018-10-23 08:29:33.000000 UTC  N/A     \Device\HarddiskVolume2\Windows\System32\svchost.exe C:\Windows\system32\svchost.exe -k netsvcs      C:\Windows\system32\svchost.exe
** 804  484     svchost.exe     0x84e7ad20      19      378     0       False   2018-10-23 08:29:32.000000 UTC  N/A     \Device\HarddiskVolume2\Windows\System32\svchost.exe C:\Windows\System32\svchost.exe -k LocalServiceNetworkRestricted        C:\Windows\System32\svchost.exe
*** 988 804     audiodg.exe     0x84ea7d20      6       127     0       False   2018-10-23 08:29:35.000000 UTC  N/A     \Device\HarddiskVolume2\Windows\System32\audiodg.exe C:\Windows\system32\AUDIODG.EXE 0x2ac   C:\Windows\system32\AUDIODG.EXE
** 872  484     svchost.exe     0x84e89c68      19      342     0       False   2018-10-23 08:29:33.000000 UTC  N/A     \Device\HarddiskVolume2\Windows\System32\svchost.exe C:\Windows\system32\svchost.exe -k LocalService C:\Windows\system32\svchost.exe
** 1192 484     svchost.exe     0x84f033c8      15      365     0       False   2018-10-23 08:29:40.000000 UTC  N/A     \Device\HarddiskVolume2\Windows\System32\svchost.exe C:\Windows\system32\svchost.exe -k NetworkService       C:\Windows\system32\svchost.exe
** 716  484     svchost.exe     0x84e54030      9       243     0       False   2018-10-23 08:29:32.000000 UTC  N/A     \Device\HarddiskVolume2\Windows\System32\svchost.exe C:\Windows\system32\svchost.exe -k RPCSS        C:\Windows\system32\svchost.exe
** 652  484     VBoxService.ex  0x84e41708      12      116     0       False   2018-10-23 08:29:31.000000 UTC  N/A     \Device\HarddiskVolume2\Windows\System32\VBoxService.exe     C:\Windows\System32\VBoxService.exe     C:\Windows\System32\VBoxService.exe
** 1164 484     sppsvc.exe      0x850d0030      6       154     0       False   2018-10-23 08:29:57.000000 UTC  N/A     \Device\HarddiskVolume2\Windows\System32\sppsvc.exe  C:\Windows\system32\sppsvc.exe  C:\Windows\system32\sppsvc.exe
** 592  484     svchost.exe     0x84e23030      12      358     0       False   2018-10-23 08:29:30.000000 UTC  N/A     \Device\HarddiskVolume2\Windows\System32\svchost.exe C:\Windows\system32\svchost.exe -k DcomLaunch   C:\Windows\system32\svchost.exe
** 848  484     svchost.exe     0x84e84898      20      400     0       False   2018-10-23 08:29:33.000000 UTC  N/A     \Device\HarddiskVolume2\Windows\System32\svchost.exe C:\Windows\System32\svchost.exe -k LocalSystemNetworkRestricted C:\Windows\System32\svchost.exe
*** 1992        848     dwm.exe 0x85109030      5       132     1       False   2018-10-23 08:30:04.000000 UTC  N/A     \Device\HarddiskVolume2\Windows\System32\dwm.exe     "C:\Windows\system32\Dwm.exe"   C:\Windows\system32\Dwm.exe
** 1488 484     svchost.exe     0x84f828f8      8       170     0       False   2018-10-23 08:29:44.000000 UTC  N/A     \Device\HarddiskVolume2\Windows\System32\svchost.exe C:\Windows\system32\svchost.exe -k LocalServiceAndNoImpersonation       C:\Windows\system32\svchost.exe
** 2032 484     SearchIndexer.  0x85164030      14      614     0       False   2018-10-23 08:30:14.000000 UTC  N/A     \Device\HarddiskVolume2\Windows\System32\SearchIndexer.exe   C:\Windows\system32\SearchIndexer.exe /Embedding        C:\Windows\system32\SearchIndexer.exe
*** 284 2032    SearchProtocol  0x8515ad20      7       235     0       False   2018-10-23 08:30:16.000000 UTC  N/A     \Device\HarddiskVolume2\Windows\System32\SearchProtocolHost.exe      "C:\Windows\system32\SearchProtocolHost.exe" Global\UsGthrFltPipeMssGthrPipe1_ Global\UsGthrCtrlFltPipeMssGthrPipe1 1 -2147483646 "Software\Microsoft\Windows Search" "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT; MS Search 4.0 Robot)" "C:\ProgramData\Microsoft\Search\Data\Temp\usgthrsvc" "DownLevelDaemon"       C:\Windows\system32\SearchProtocolHost.exe
*** 1292        2032    SearchFilterHo  0x8515cd20      5       80      0       False   2018-10-23 08:30:17.000000 UTC  N/A     \Device\HarddiskVolume2\Windows\System32\SearchFilterHost.exe        "C:\Windows\system32\SearchFilterHost.exe" 0 520 524 532 65536 528      C:\Windows\system32\SearchFilterHost.exe
** 1364 484     svchost.exe     0x84f4dca0      19      307     0       False   2018-10-23 08:29:43.000000 UTC  N/A     \Device\HarddiskVolume2\Windows\System32\svchost.exe C:\Windows\system32\svchost.exe -k LocalServiceNoNetwork        C:\Windows\system32\svchost.exe
** 1460 484     svchost.exe     0x84f7d578      11      148     0       False   2018-10-23 08:29:44.000000 UTC  N/A     \Device\HarddiskVolume2\Windows\System32\svchost.exe C:\Windows\System32\svchost.exe -k utcsvc       C:\Windows\System32\svchost.exe
** 308  484     taskhost.exe    0x850b2538      8       151     1       False   2018-10-23 08:29:55.000000 UTC  N/A     \Device\HarddiskVolume2\Windows\System32\taskhost.exe        "taskhost.exe"  C:\Windows\system32\taskhost.exe
** 1336 484     spoolsv.exe     0x84f323f8      16      295     0       False   2018-10-23 08:29:43.000000 UTC  N/A     \Device\HarddiskVolume2\Windows\System32\spoolsv.exe C:\Windows\System32\spoolsv.exe C:\Windows\System32\spoolsv.exe
* 492   388     lsass.exe       0x84def3d8      7       480     0       False   2018-10-23 08:29:25.000000 UTC  N/A     \Device\HarddiskVolume2\Windows\System32\lsass.exe   C:\Windows\system32\lsass.exe   C:\Windows\system32\lsass.exe
424     372     winlogon.exe    0x84dcbd20      6       117     1       False   2018-10-23 08:29:23.000000 UTC  N/A     \Device\HarddiskVolume2\Windows\System32\winlogon.exe        winlogon.exe    C:\Windows\system32\winlogon.exe
324     1876    explorer.exe    0x85097870      33      827     1       False   2018-10-23 08:30:04.000000 UTC  N/A     \Device\HarddiskVolume2\Windows\explorer.exe C:\Windows\Explorer.EXE C:\Windows\Explorer.EXE
* 1000  324     VBoxTray.exe    0x85135af8      14      159     1       False   2018-10-23 08:30:08.000000 UTC  N/A     \Device\HarddiskVolume2\Windows\System32\VBoxTray.exe        "C:\Windows\System32\VBoxTray.exe"      C:\Windows\System32\VBoxTray.exe
* 2096  324     cmd.exe 0x851a6610      1       22      1       False   2018-10-23 08:30:18.000000 UTC  N/A     \Device\HarddiskVolume2\Windows\System32\cmd.exe     "C:\Windows\system32\cmd.exe"   C:\Windows\system32\cmd.exe
* 2412  324     DumpIt.exe      0x845a8d20      2       38      1       False   2018-10-23 08:30:48.000000 UTC  N/A     \Device\HarddiskVolume2\Users\hello\Desktop\DumpIt\DumpIt.exe        "C:\Users\hello\Desktop\DumpIt\DumpIt.exe"      C:\Users\hello\Desktop\DumpIt\DumpIt.exe
```

Hay una pagina en la que podemos consultar para detectar procesos no maliciosos que estan recogidos en una pagina de `hacking etico` llamada `HackTricks` en la que podremos investigar respecto a la informacion que nos haya volcado la herramienta si hay algun proceso sospechoso en el `dump`.

URL = [Info Procesos HackTricks](https://book.hacktricks.wiki/en/generic-methodologies-and-resources/basic-forensic-methodology/windows-forensics/interesting-windows-registry-keys.html)

URL2 = [Info Procesos Medium](https://medium.com/%40leo.valentic9/windows-process-genealogy-understanding-and-analyzing-key-system-processes-in-digital-forensics-a88cd5b9698f)

Con esto lo que podemos hacer es descartar los procesos que vengan en estas paginas, por que van a ser lo que vienen por defecto en el sistema de un `Windows`.

En la lista de procesos ya podemos ver alguno sospechoso como este:

```
.. 0x85109030:dwm.exe                               1992    848      5    132 2018-10-23 08:30:04 UTC+0000
```

Tiene un nombre bastante raro y no es muy comun, o desde `Volatility3` esta linea:

```
*** 1992        848     dwm.exe 0x85109030      5       132     1       False   2018-10-23 08:30:04.000000 UTC  N/A     \Device\HarddiskVolume2\Windows\System32\dwm.exe     "C:\Windows\system32\Dwm.exe"   C:\Windows\system32\Dwm.exe
```

Ahora utilizaremos el parametro `pslist` que es como el anterior pero en este caso te muestra simplemente los procesos, con su `PID` identificativo, etc... Tambien super importante si se tuviera el `Offset Virtual` se mostraria.

#### Volatility2

```shell
./vol.py -f Challenge.raw --profile=Win7SP1x86_23418 pslist
```

Info:

```
Offset(V)  Name                    PID   PPID   Thds     Hnds   Sess  Wow64 Start                          Exit                          
---------- -------------------- ------ ------ ------ -------- ------ ------ ------------------------------ ------------------------------
0x83d09c58 System                    4      0     85      483 ------      0 2018-10-23 08:29:16 UTC+0000                                 
0x8437db18 smss.exe                260      4      2       29 ------      0 2018-10-23 08:29:16 UTC+0000                                 
0x84d69030 csrss.exe               340    332      8      347      0      0 2018-10-23 08:29:21 UTC+0000                                 
0x84d8d030 csrss.exe               380    372      9      188      1      0 2018-10-23 08:29:23 UTC+0000                                 
0x84d93c68 wininit.exe             388    332      3       79      0      0 2018-10-23 08:29:23 UTC+0000                                 
0x84dcbd20 winlogon.exe            424    372      6      117      1      0 2018-10-23 08:29:23 UTC+0000                                 
0x84debd20 services.exe            484    388     10      191      0      0 2018-10-23 08:29:25 UTC+0000                                 
0x84def3d8 lsass.exe               492    388      7      480      0      0 2018-10-23 08:29:25 UTC+0000                                 
0x84df2378 lsm.exe                 500    388     10      146      0      0 2018-10-23 08:29:25 UTC+0000                                 
0x84e23030 svchost.exe             592    484     12      358      0      0 2018-10-23 08:29:30 UTC+0000                                 
0x84e41708 VBoxService.ex          652    484     12      116      0      0 2018-10-23 08:29:31 UTC+0000                                 
0x84e54030 svchost.exe             716    484      9      243      0      0 2018-10-23 08:29:32 UTC+0000                                 
0x84e7ad20 svchost.exe             804    484     19      378      0      0 2018-10-23 08:29:32 UTC+0000                                 
0x84e84898 svchost.exe             848    484     20      400      0      0 2018-10-23 08:29:33 UTC+0000                                 
0x84e89c68 svchost.exe             872    484     19      342      0      0 2018-10-23 08:29:33 UTC+0000                                 
0x84e8c648 svchost.exe             896    484     30      809      0      0 2018-10-23 08:29:33 UTC+0000                                 
0x84ea7d20 audiodg.exe             988    804      6      127      0      0 2018-10-23 08:29:35 UTC+0000                                 
0x84f033c8 svchost.exe            1192    484     15      365      0      0 2018-10-23 08:29:40 UTC+0000                                 
0x84f323f8 spoolsv.exe            1336    484     16      295      0      0 2018-10-23 08:29:43 UTC+0000                                 
0x84f4dca0 svchost.exe            1364    484     19      307      0      0 2018-10-23 08:29:43 UTC+0000                                 
0x84f7d578 svchost.exe            1460    484     11      148      0      0 2018-10-23 08:29:44 UTC+0000                                 
0x84f828f8 svchost.exe            1488    484      8      170      0      0 2018-10-23 08:29:44 UTC+0000                                 
0x850b2538 taskhost.exe            308    484      8      151      1      0 2018-10-23 08:29:55 UTC+0000                                 
0x850d0030 sppsvc.exe             1164    484      6      154      0      0 2018-10-23 08:29:57 UTC+0000                                 
0x85109030 dwm.exe                1992    848      5      132      1      0 2018-10-23 08:30:04 UTC+0000                                 
0x85097870 explorer.exe            324   1876     33      827      1      0 2018-10-23 08:30:04 UTC+0000                                 
0x85135af8 VBoxTray.exe           1000    324     14      159      1      0 2018-10-23 08:30:08 UTC+0000                                 
0x85164030 SearchIndexer.         2032    484     14      614      0      0 2018-10-23 08:30:14 UTC+0000                                 
0x8515ad20 SearchProtocol          284   2032      7      235      0      0 2018-10-23 08:30:16 UTC+0000                                 
0x8515cd20 SearchFilterHo         1292   2032      5       80      0      0 2018-10-23 08:30:17 UTC+0000                                 
0x851a6610 cmd.exe                2096    324      1       22      1      0 2018-10-23 08:30:18 UTC+0000                                 
0x851a5cd8 conhost.exe            2104    380      2       52      1      0 2018-10-23 08:30:18 UTC+0000                                 
0x845a8d20 DumpIt.exe             2412    324      2       38      1      0 2018-10-23 08:30:48 UTC+0000                                 
0x84d83d20 conhost.exe            2424    380      2       51      1      0 2018-10-23 08:30:48 UTC+0000
```

#### Volatility3

```shell
./vol.py -f Challenge.raw windows.pslist
```

Info:

```
Volatility 3 Framework 2.26.2
Progress:  100.00               PDB scanning finished                        
PID     PPID    ImageFileName   Offset(V)       Threads Handles SessionId       Wow64   CreateTime      ExitTime        File output

4       0       System  0x83d09c58      85      483     N/A     False   2018-10-23 08:29:16.000000 UTC  N/A     Disabled
260     4       smss.exe        0x8437db18      2       29      N/A     False   2018-10-23 08:29:16.000000 UTC  N/A     Disabled
340     332     csrss.exe       0x84d69030      8       347     0       False   2018-10-23 08:29:21.000000 UTC  N/A     Disabled
380     372     csrss.exe       0x84d8d030      9       188     1       False   2018-10-23 08:29:23.000000 UTC  N/A     Disabled
388     332     wininit.exe     0x84d93c68      3       79      0       False   2018-10-23 08:29:23.000000 UTC  N/A     Disabled
424     372     winlogon.exe    0x84dcbd20      6       117     1       False   2018-10-23 08:29:23.000000 UTC  N/A     Disabled
484     388     services.exe    0x84debd20      10      191     0       False   2018-10-23 08:29:25.000000 UTC  N/A     Disabled
492     388     lsass.exe       0x84def3d8      7       480     0       False   2018-10-23 08:29:25.000000 UTC  N/A     Disabled
500     388     lsm.exe 0x84df2378      10      146     0       False   2018-10-23 08:29:25.000000 UTC  N/A     Disabled
592     484     svchost.exe     0x84e23030      12      358     0       False   2018-10-23 08:29:30.000000 UTC  N/A     Disabled
652     484     VBoxService.ex  0x84e41708      12      116     0       False   2018-10-23 08:29:31.000000 UTC  N/A     Disabled
716     484     svchost.exe     0x84e54030      9       243     0       False   2018-10-23 08:29:32.000000 UTC  N/A     Disabled
804     484     svchost.exe     0x84e7ad20      19      378     0       False   2018-10-23 08:29:32.000000 UTC  N/A     Disabled
848     484     svchost.exe     0x84e84898      20      400     0       False   2018-10-23 08:29:33.000000 UTC  N/A     Disabled
872     484     svchost.exe     0x84e89c68      19      342     0       False   2018-10-23 08:29:33.000000 UTC  N/A     Disabled
896     484     svchost.exe     0x84e8c648      30      809     0       False   2018-10-23 08:29:33.000000 UTC  N/A     Disabled
988     804     audiodg.exe     0x84ea7d20      6       127     0       False   2018-10-23 08:29:35.000000 UTC  N/A     Disabled
1192    484     svchost.exe     0x84f033c8      15      365     0       False   2018-10-23 08:29:40.000000 UTC  N/A     Disabled
1336    484     spoolsv.exe     0x84f323f8      16      295     0       False   2018-10-23 08:29:43.000000 UTC  N/A     Disabled
1364    484     svchost.exe     0x84f4dca0      19      307     0       False   2018-10-23 08:29:43.000000 UTC  N/A     Disabled
1460    484     svchost.exe     0x84f7d578      11      148     0       False   2018-10-23 08:29:44.000000 UTC  N/A     Disabled
1488    484     svchost.exe     0x84f828f8      8       170     0       False   2018-10-23 08:29:44.000000 UTC  N/A     Disabled
308     484     taskhost.exe    0x850b2538      8       151     1       False   2018-10-23 08:29:55.000000 UTC  N/A     Disabled
1164    484     sppsvc.exe      0x850d0030      6       154     0       False   2018-10-23 08:29:57.000000 UTC  N/A     Disabled
1992    848     dwm.exe 0x85109030      5       132     1       False   2018-10-23 08:30:04.000000 UTC  N/A     Disabled
324     1876    explorer.exe    0x85097870      33      827     1       False   2018-10-23 08:30:04.000000 UTC  N/A     Disabled
1000    324     VBoxTray.exe    0x85135af8      14      159     1       False   2018-10-23 08:30:08.000000 UTC  N/A     Disabled
2032    484     SearchIndexer.  0x85164030      14      614     0       False   2018-10-23 08:30:14.000000 UTC  N/A     Disabled
284     2032    SearchProtocol  0x8515ad20      7       235     0       False   2018-10-23 08:30:16.000000 UTC  N/A     Disabled
1292    2032    SearchFilterHo  0x8515cd20      5       80      0       False   2018-10-23 08:30:17.000000 UTC  N/A     Disabled
2096    324     cmd.exe 0x851a6610      1       22      1       False   2018-10-23 08:30:18.000000 UTC  N/A     Disabled
2104    380     conhost.exe     0x851a5cd8      2       52      1       False   2018-10-23 08:30:18.000000 UTC  N/A     Disabled
2412    324     DumpIt.exe      0x845a8d20      2       38      1       False   2018-10-23 08:30:48.000000 UTC  N/A     Disabled
2424    380     conhost.exe     0x84d83d20      2       51      1       False   2018-10-23 08:30:48.000000 UTC  N/A     Disabled
```

Con este listado podremos ver en mas profundidad procesos que a lo mejor no veiamos antes de forma un poco mas detallada y clara.

Con el parametro `psscan` podremos obtener los procesos que en ese momento se estaban ejecutando en memoria, es decir, los procesos con mayor importancia (Procesos grandes) se estaban ejecutando en ese momento.

#### Volatility2

```shell
./vol.py -f Challenge.raw --profile=Win7SP1x86_23418 psscan
```

Info:

```
Offset(P)          Name                PID   PPID PDB        Time created                   Time exited                   
------------------ ---------------- ------ ------ ---------- ------------------------------ ------------------------------
```

#### Volatility3

```shell
./vol.py -f Challenge.raw windows.psscan
```

Info:

```
Volatility 3 Framework 2.26.2
Progress:  100.00               PDB scanning finished                        
PID     PPID    ImageFileName   Offset(V)       Threads Handles SessionId       Wow64   CreateTime      ExitTime        File output

324     1876    explorer.exe    0x3d297870      33      827     1       False   2018-10-23 08:30:04.000000 UTC  N/A     Disabled
308     484     taskhost.exe    0x3d2b2538      8       151     1       False   2018-10-23 08:29:55.000000 UTC  N/A     Disabled
1164    484     sppsvc.exe      0x3d2d0030      6       154     0       False   2018-10-23 08:29:57.000000 UTC  N/A     Disabled
1992    848     dwm.exe 0x3d309030      5       132     1       False   2018-10-23 08:30:04.000000 UTC  N/A     Disabled
1000    324     VBoxTray.exe    0x3d335af8      14      159     1       False   2018-10-23 08:30:08.000000 UTC  N/A     Disabled
284     2032    SearchProtocol  0x3d35ad20      7       235     0       False   2018-10-23 08:30:16.000000 UTC  N/A     Disabled
1292    2032    SearchFilterHo  0x3d35cd20      5       80      0       False   2018-10-23 08:30:17.000000 UTC  N/A     Disabled
2032    484     SearchIndexer.  0x3d364030      14      614     0       False   2018-10-23 08:30:14.000000 UTC  N/A     Disabled
2104    380     conhost.exe     0x3d3a5cd8      2       52      1       False   2018-10-23 08:30:18.000000 UTC  N/A     Disabled
2096    324     cmd.exe 0x3d3a6610      1       22      1       False   2018-10-23 08:30:18.000000 UTC  N/A     Disabled
1992    848     dwm.exe 0x3d3bc030      5       132     1       False   2018-10-23 08:30:04.000000 UTC  N/A     Disabled
1000    324     VBoxTray.exe    0x3d3e8af8      14      159     1       False   2018-10-23 08:30:08.000000 UTC  N/A     Disabled
592     484     svchost.exe     0x3d423030      12      358     0       False   2018-10-23 08:29:30.000000 UTC  N/A     Disabled
652     484     VBoxService.ex  0x3d441708      12      116     0       False   2018-10-23 08:29:31.000000 UTC  N/A     Disabled
716     484     svchost.exe     0x3d454030      9       243     0       False   2018-10-23 08:29:32.000000 UTC  N/A     Disabled
804     484     svchost.exe     0x3d47ad20      19      378     0       False   2018-10-23 08:29:32.000000 UTC  N/A     Disabled
848     484     svchost.exe     0x3d484898      20      400     0       False   2018-10-23 08:29:33.000000 UTC  N/A     Disabled
872     484     svchost.exe     0x3d489c68      19      342     0       False   2018-10-23 08:29:33.000000 UTC  N/A     Disabled
896     484     svchost.exe     0x3d48c648      30      809     0       False   2018-10-23 08:29:33.000000 UTC  N/A     Disabled
988     804     audiodg.exe     0x3d4a7d20      6       127     0       False   2018-10-23 08:29:35.000000 UTC  N/A     Disabled
1192    484     svchost.exe     0x3d5033c8      15      365     0       False   2018-10-23 08:29:40.000000 UTC  N/A     Disabled
1336    484     spoolsv.exe     0x3d5323f8      16      295     0       False   2018-10-23 08:29:43.000000 UTC  N/A     Disabled
1364    484     svchost.exe     0x3d54dca0      19      307     0       False   2018-10-23 08:29:43.000000 UTC  N/A     Disabled
1460    484     svchost.exe     0x3d57d578      11      148     0       False   2018-10-23 08:29:44.000000 UTC  N/A     Disabled
1488    484     svchost.exe     0x3d5828f8      8       170     0       False   2018-10-23 08:29:44.000000 UTC  N/A     Disabled
340     332     csrss.exe       0x3d769030      8       347     0       False   2018-10-23 08:29:21.000000 UTC  N/A     Disabled
2424    380     conhost.exe     0x3d783d20      2       51      1       False   2018-10-23 08:30:48.000000 UTC  N/A     Disabled
380     372     csrss.exe       0x3d78d030      9       188     1       False   2018-10-23 08:29:23.000000 UTC  N/A     Disabled
388     332     wininit.exe     0x3d793c68      3       79      0       False   2018-10-23 08:29:23.000000 UTC  N/A     Disabled
424     372     winlogon.exe    0x3d7cbd20      6       117     1       False   2018-10-23 08:29:23.000000 UTC  N/A     Disabled
484     388     services.exe    0x3d7ebd20      10      191     0       False   2018-10-23 08:29:25.000000 UTC  N/A     Disabled
492     388     lsass.exe       0x3d7ef3d8      7       480     0       False   2018-10-23 08:29:25.000000 UTC  N/A     Disabled
500     388     lsm.exe 0x3d7f2378      10      146     0       False   2018-10-23 08:29:25.000000 UTC  N/A     Disabled
2412    324     DumpIt.exe      0x3dfa8d20      2       38      1       False   2018-10-23 08:30:48.000000 UTC  N/A     Disabled
260     4       smss.exe        0x3e17db18      2       29      N/A     False   2018-10-23 08:29:16.000000 UTC  N/A     Disabled
4       0       System  0x3e7b3c58      85      483     N/A     False   2018-10-23 08:29:16.000000 UTC  N/A     Disabled
```

En este caso con la `v2` de `volatility` no nos detecto ningun proceso asi grande, pero con la `v3` si nos detecto unos cuantos procesos, pero siguen siendo practicamente los mismos que antes, por lo que no pasa nada.

Con el parametro `psxview` podremos ver si algun proceso que hemos listado antes con los anteriores parametros, estaba de forma oculta, es decir, con este parametro podremos visualizar procesos que estaban ocultos cuando se realizo el `dump`.

#### Volatility2

```shell
./vol.py -f Challenge.raw --profile=Win7SP1x86_23418 psxview
```

Info:

```
Offset(P)  Name                    PID pslist psscan thrdproc pspcid csrss session deskthrd ExitTime
---------- -------------------- ------ ------ ------ -------- ------ ----- ------- -------- --------
0x3d441708 VBoxService.ex          652 True   False  True     True   True  True    False    
0x3dfa8d20 DumpIt.exe             2412 True   False  True     True   True  True    True     
0x3d3a6610 cmd.exe                2096 True   False  True     True   True  True    True     
0x3d3a5cd8 conhost.exe            2104 True   False  True     True   True  True    True     
0x3d484898 svchost.exe             848 True   False  True     True   True  True    True     
0x3d35ad20 SearchProtocol          284 True   False  True     True   True  True    True     
0x3d7ebd20 services.exe            484 True   False  True     True   True  True    False    
0x3d2d0030 sppsvc.exe             1164 True   False  True     True   True  True    True     
0x3d364030 SearchIndexer.         2032 True   False  True     True   True  True    True     
0x3d54dca0 svchost.exe            1364 True   False  True     True   True  True    True     
0x3d7cbd20 winlogon.exe            424 True   False  True     True   True  True    True     
0x3d454030 svchost.exe             716 True   False  True     True   True  True    True     
0x3d5033c8 svchost.exe            1192 True   False  True     True   True  True    True     
0x3d2b2538 taskhost.exe            308 True   False  True     True   True  True    True     
0x3d7f2378 lsm.exe                 500 True   False  True     True   True  True    False    
0x3d4a7d20 audiodg.exe             988 True   False  True     True   True  True    True     
0x3d48c648 svchost.exe             896 True   False  True     True   True  True    True     
0x3d423030 svchost.exe             592 True   False  True     True   True  True    True     
0x3d57d578 svchost.exe            1460 True   False  True     True   True  True    True     
0x3d47ad20 svchost.exe             804 True   False  True     True   True  True    True     
0x3d7ef3d8 lsass.exe               492 True   False  True     True   True  True    False    
0x3d5828f8 svchost.exe            1488 True   False  True     True   True  True    True     
0x3d35cd20 SearchFilterHo         1292 True   False  True     True   True  True    True     
0x3d793c68 wininit.exe             388 True   False  True     True   True  True    True     
0x3d309030 dwm.exe                1992 True   False  True     True   True  True    True     
0x3d335af8 VBoxTray.exe           1000 True   False  True     True   True  True    True     
0x3d297870 explorer.exe            324 True   False  True     True   True  True    True     
0x3d489c68 svchost.exe             872 True   False  True     True   True  True    True     
0x3d5323f8 spoolsv.exe            1336 True   False  True     True   True  True    True     
0x3d783d20 conhost.exe            2424 True   False  True     True   True  True    True     
0x3e7b3c58 System                    4 True   False  True     True   False False   False    
0x3e17db18 smss.exe                260 True   False  True     True   False False   False    
0x3d78d030 csrss.exe               380 True   False  True     True   False True    True     
0x3d769030 csrss.exe               340 True   False  True     True   False True    True
```

#### Volatility3

```shell
./vol.py -f Challenge.raw windows.psxview
```

Info:

```
Volatility 3 Framework 2.26.2
Offset(Virtual) Name    PID     pslist  psscan  thrdscan        csrss   Exit Time

0x84f7d578      svchost.exe     1460    True    False   True    True
0x3d57d578      svchost.exe     1460    False   True    False   False
0x3d54dca0      svchost.exe     1364    False   True    False   False
0x84e41708      VBoxService.ex  652     True    False   True    True
0x3d441708      VBoxService.ex  652     False   True    False   False
0x3d35ad20      SearchProtocol  284     False   True    False   False
0x3d35cd20      SearchFilterHo  1292    False   True    False   False
0x3d47ad20      svchost.exe     804     False   True    False   False
0x3d4a7d20      audiodg.exe     988     False   True    False   False
0x3d783d20      conhost.exe     2424    False   True    False   False
0x3d7cbd20      winlogon.exe    424     False   True    False   False
0x851a6610      cmd.exe 2096    True    False   True    True
0x3d3a6610      cmd.exe 2096    False   True    False   False
0x3d7ebd20      services.exe    484     False   True    False   False
0x3d3e8af8      VBoxTray.exe    1000    False   True    False   False
0x8437db18      smss.exe        260     True    False   True    False
0x84e84898      svchost.exe     848     True    False   True    True
0x3d484898      svchost.exe     848     False   True    False   False
0x3e17db18      smss.exe        260     False   True    False   False
0x84dcbd20      winlogon.exe    424     True    False   True    True
0x84debd20      services.exe    484     True    False   True    True
0x84e7ad20      svchost.exe     804     True    False   True    True
0x84ea7d20      audiodg.exe     988     True    False   True    True
0x84f4dca0      svchost.exe     1364    True    False   True    True
0x84f828f8      svchost.exe     1488    True    False   True    True
0x8515ad20      SearchProtocol  284     True    False   True    True
0x8515cd20      SearchFilterHo  1292    True    False   True    True
0x845a8d20      DumpIt.exe      2412    True    False   True    True
0x84d83d20      conhost.exe     2424    True    False   True    True
0x3d5323f8      spoolsv.exe     1336    False   True    False   False
0x3d5828f8      svchost.exe     1488    False   True    False   False
0x84d69030      csrss.exe       340     True    False   True    False
0x84d8d030      csrss.exe       380     True    False   True    False
0x84e23030      svchost.exe     592     True    False   True    True
0x84e54030      svchost.exe     716     True    False   True    True
0x850d0030      sppsvc.exe      1164    True    False   True    True
0x85109030      dwm.exe 1992    True    False   True    True
0x85135af8      VBoxTray.exe    1000    True    False   True    True
0x85164030      SearchIndexer.  2032    True    False   True    True
0x850b2538      taskhost.exe    308     True    False   True    True
0x3d2b2538      taskhost.exe    308     False   True    False   False
0x3d335af8      VBoxTray.exe    1000    False   True    False   False
0x84e8c648      svchost.exe     896     True    False   True    True
0x84f033c8      svchost.exe     1192    True    False   True    True
0x3d48c648      svchost.exe     896     False   True    False   False
0x3d5033c8      svchost.exe     1192    False   True    False   False
0x3dfa8d20      DumpIt.exe      2412    False   True    False   False
0x84def3d8      lsass.exe       492     True    False   True    True
0x83d09c58      System  4       True    False   True    False
0x851a5cd8      conhost.exe     2104    True    False   True    True
0x3d3a5cd8      conhost.exe     2104    False   True    False   False
0x3d7ef3d8      lsass.exe       492     False   True    False   False
0x3e7b3c58      System  4       False   True    False   False
0x84d93c68      wininit.exe     388     True    False   True    True
0x84e89c68      svchost.exe     872     True    False   True    True
0x3d489c68      svchost.exe     872     False   True    False   False
0x3d793c68      wininit.exe     388     False   True    False   False
0x85097870      explorer.exe    324     True    False   True    True
0x3d297870      explorer.exe    324     False   True    False   False
0x3d2d0030      sppsvc.exe      1164    False   True    False   False
0x3d309030      dwm.exe 1992    False   True    False   False
0x84df2378      lsm.exe 500     True    False   True    True
0x3d364030      SearchIndexer.  2032    False   True    False   False
0x3d3bc030      dwm.exe 1992    False   True    False   False
0x3d423030      svchost.exe     592     False   True    False   False
0x84f323f8      spoolsv.exe     1336    True    False   True    True
0x3d454030      svchost.exe     716     False   True    False   False
0x3d769030      csrss.exe       340     False   True    False   False
0x3d78d030      csrss.exe       380     False   True    False   False
0x3d7f2378      lsm.exe 500     False   True    False   False
```

Si en la parte de los comandos que hemos lanzado anteriormente como por ejemplo `psscan, pslist, etc...` aparece como `True` significa que no tienen ningun `subproceso` oculto, por lo que con esta vista no hay nada oculto cuando se realizo el `dump` en la parte de la `v2` de `volatility` en la columna de `psscan` vemos todo en `False` ya que no detecto nada anteriormente eso es un falso positivo.

Pero en la `v3` si esta detectando algunos `subprocesos` ocultos, que tambien pueden ser falsos positivos, pero nunca esta demas investigarlo.

## Fase 3

### Obtener informacion de las conexiones (IPs) dentro de los procesos

Con el parametro `connscan` para la `v2`, pero para la `v3` seria con `netscan`, lo que podremos ver sera las conexiones que ha realizado el sistema clasificando la `IP` local hacia la `IP` remota (`IP publica`) de cualquier conexion que se haya echo, con esto podremos ver si hay alguna conexion remota sospechosa o no.

#### Volatility2

```shell
./vol.py -f Challenge.raw --profile=Win7SP1x86_23418 connscan
```

Info:

```
ERROR   : volatility.debug    : This command does not support the profile Win7SP0x86
```

Aqui por lo que se ve en este tipo de perfil da un error, pero si lo hacemos en la `v3` de `Volatility`...

#### Volatility3

```shell
./vol.py -f Challenge.raw windows.netscan
```

Info:

```
Volatility 3 Framework 2.26.2
Progress:  100.00               PDB scanning finished                        
Offset  Proto   LocalAddr       LocalPort       ForeignAddr     ForeignPort     State   PID     Owner   Created

0x3d23ff58      TCPv4   0.0.0.0 49156   0.0.0.0 0       LISTENING       484     services.exe    N/A
0x3d23ff58      TCPv6   ::      49156   ::      0       LISTENING       484     services.exe    N/A
0x3d257308      UDPv4   0.0.0.0 0       *       0               652     VBoxService.ex  2018-10-23 08:31:02.000000 UTC
0x3d25d6a8      UDPv4   0.0.0.0 3702    *       0               1488    svchost.exe     2018-10-23 08:29:53.000000 UTC
0x3d25d6a8      UDPv6   ::      3702    *       0               1488    svchost.exe     2018-10-23 08:29:53.000000 UTC
0x3d25dc30      UDPv4   0.0.0.0 3702    *       0               1488    svchost.exe     2018-10-23 08:29:53.000000 UTC
0x3d31c310      UDPv4   0.0.0.0 0       *       0               652     VBoxService.ex  2018-10-23 08:31:07.000000 UTC
0x3d38a008      UDPv4   0.0.0.0 0       *       0               652     VBoxService.ex  2018-10-23 08:31:13.000000 UTC
0x3d3cf310      UDPv4   0.0.0.0 0       *       0               652     VBoxService.ex  2018-10-23 08:31:07.000000 UTC
0x3d435008      UDPv6   fe80::147b:c8fd:e2c6:69de       546     *       0               804     svchost.exe     2018-10-23 08:29:41.000000 UTC
0x3d43c350      UDPv4   10.0.2.15       137     *       0               4       System  2018-10-23 08:29:41.000000 UTC
0x3d43cc90      TCPv4   10.0.2.15       139     0.0.0.0 0       LISTENING       4       System  N/A
0x3d43e8c0      UDPv4   10.0.2.15       138     *       0               4       System  2018-10-23 08:29:41.000000 UTC
0x3d45cf58      TCPv4   0.0.0.0 135     0.0.0.0 0       LISTENING       716     svchost.exe     N/A
0x3d45cf58      TCPv6   ::      135     ::      0       LISTENING       716     svchost.exe     N/A
0x3d465508      TCPv4   0.0.0.0 135     0.0.0.0 0       LISTENING       716     svchost.exe     N/A
0x3d46c1a0      TCPv4   0.0.0.0 49152   0.0.0.0 0       LISTENING       388     wininit.exe     N/A
0x3d46c1a0      TCPv6   ::      49152   ::      0       LISTENING       388     wininit.exe     N/A
0x3d46cd28      TCPv4   0.0.0.0 49152   0.0.0.0 0       LISTENING       388     wininit.exe     N/A
0x3d48b530      TCPv4   0.0.0.0 49153   0.0.0.0 0       LISTENING       804     svchost.exe     N/A
0x3d48b530      TCPv6   ::      49153   ::      0       LISTENING       804     svchost.exe     N/A
0x3d48d808      TCPv4   0.0.0.0 49153   0.0.0.0 0       LISTENING       804     svchost.exe     N/A
0x3d507120      TCPv4   0.0.0.0 49154   0.0.0.0 0       LISTENING       492     lsass.exe       N/A
0x3d508850      TCPv4   0.0.0.0 49154   0.0.0.0 0       LISTENING       492     lsass.exe       N/A
0x3d508850      TCPv6   ::      49154   ::      0       LISTENING       492     lsass.exe       N/A
0x3d51dd10      UDPv4   0.0.0.0 0       *       0               1192    svchost.exe     2018-10-23 08:29:41.000000 UTC
0x3d51dd10      UDPv6   ::      0       *       0               1192    svchost.exe     2018-10-23 08:29:41.000000 UTC
0x3d521a38      UDPv4   0.0.0.0 5355    *       0               1192    svchost.exe     2018-10-23 08:29:46.000000 UTC
0x3d521a38      UDPv6   ::      5355    *       0               1192    svchost.exe     2018-10-23 08:29:46.000000 UTC
0x3d52f0d0      TCPv4   0.0.0.0 49155   0.0.0.0 0       LISTENING       896     svchost.exe     N/A
0x3d530d58      TCPv4   0.0.0.0 49155   0.0.0.0 0       LISTENING       896     svchost.exe     N/A
0x3d530d58      TCPv6   ::      49155   ::      0       LISTENING       896     svchost.exe     N/A
0x3d5be698      UDPv4   0.0.0.0 5355    *       0               1192    svchost.exe     2018-10-23 08:29:46.000000 UTC
0x3d5d3268      TCPv4   0.0.0.0 5357    0.0.0.0 0       LISTENING       4       System  N/A
0x3d5d3268      TCPv6   ::      5357    ::      0       LISTENING       4       System  N/A
0x3d7fb008      UDPv4   0.0.0.0 0       *       0               652     VBoxService.ex  2018-10-23 08:30:56.000000 UTC
0x3e708a70      UDPv4   0.0.0.0 3702    *       0               1488    svchost.exe     2018-10-23 08:29:53.000000 UTC
0x3e708a70      UDPv6   ::      3702    *       0               1488    svchost.exe     2018-10-23 08:29:53.000000 UTC
0x3e708e98      UDPv4   0.0.0.0 3702    *       0               1488    svchost.exe     2018-10-23 08:29:53.000000 UTC
0x3e70f570      UDPv4   0.0.0.0 55478   *       0               1488    svchost.exe     2018-10-23 08:29:49.000000 UTC
0x3e70f570      UDPv6   ::      55478   *       0               1488    svchost.exe     2018-10-23 08:29:49.000000 UTC
0x3e70fad8      UDPv4   0.0.0.0 55477   *       0               1488    svchost.exe     2018-10-23 08:29:49.000000 UTC
0x3e71fba0      TCPv4   0.0.0.0 49156   0.0.0.0 0       LISTENING       484     services.exe    N/A
0x3e725008      TCPv4   0.0.0.0 445     0.0.0.0 0       LISTENING       4       System  N/A
0x3e725008      TCPv6   ::      445     ::      0       LISTENING       4       System  N/A
```

En este caso no veremos nada raro, ni extraño, pero imaginemos que este proceso nos parece extraño o sospechoso:

```
0x3d435008      UDPv6   fe80::147b:c8fd:e2c6:69de       546     *       0               804     svchost.exe     2018-10-23 08:29:41.000000 UTC
```

Podremos filtrarlo con el `pstree` y con `grep` de esta forma.

#### Volatility2

```shell
./vol.py -f Challenge.raw --profile=Win7SP1x86_23418 pstree | grep "804"
```

Info:

```
Volatility Foundation Volatility Framework 2.6.1
.. 0x84e7ad20:svchost.exe                             804    484     19    378 2018-10-23 08:29:32 UTC+0000
... 0x84ea7d20:audiodg.exe                            988    804      6    127 2018-10-23 08:29:35 UTC+0000
```

Con esto veremos que podremos filtrar en la seccion de `PID` y despues utilizar `pstree` para mostrarnos el proceso que tiene ese `PID` junto con su árbol de procesos.

#### Volatility3

```shell
./vol.py -f Challenge.raw windows.pstree | grep "804"
```

Info:

```
* 2424ss380100.0conhost.exe     0x84d83d20ng fin2shed   51      1       False   2018-10-23 08:30:48.000000 UTC  N/A     \Device\HarddiskVolume2\Windows\System32\conhost.exe \??\C:\Windows\system32\conhost.exe "499080522-1749980471992366858-146566314551631531-193375578852495345-1447858489     C:\Windows\system32\conhost.exe
** 804  484     svchost.exe     0x84e7ad20      19      378     0       False   2018-10-23 08:29:32.000000 UTC  N/A     \Device\HarddiskVolume2\Windows\System32\svchost.exe C:\Windows\System32\svchost.exe -k LocalServiceNetworkRestricted        C:\Windows\System32\svchost.exe
*** 988 804     audiodg.exe     0x84ea7d20      6       127     0       False   2018-10-23 08:29:35.000000 UTC  N/A     \Device\HarddiskVolume2\Windows\System32\audiodg.exe C:\Windows\system32\AUDIODG.EXE 0x2ac   C:\Windows\system32\AUDIODG.EXE
```

De la misma forma que el anterior, pero en este caso en la `v3`.

Con el parametro `sockets` podremos ver las conexiones a nivel de `procesos` que ha tenido el sistema en ese momento, para investigar mas a fondo esto, pero como en la `v2` da un fallo o no tiene directamente la imagen `sockets` no veremos nada.

#### Volatility2

```shell
./vol.py -f Challenge.raw --profile=Win7SP1x86_23418 sockets
```

Info:

```
ERROR   : volatility.debug    : This command does not support the profile Win7SP1x86_23418
```

#### Volatility3

En este caso para la `v3` con el parametro `windows.netscan` ya te muestra lo del comando anterior de `v2` como hemos visto antes en el de `v3`.

### Obtener información de las instrucciones que se ha realizado en el sistema

Con el parametro `cmdscan` podremos ver todas las instrucciones que se ha realizado en el sistema, tanto los comandos que se hayan ejecutado, como las ventanas de consola que se haya abierto, etc... Podremos ver todo lo que se haya ejecutando a nivel de comandos con dicho parametro.

#### Volatility2

```shell
./vol.py -f Challenge.raw --profile=Win7SP1x86_23418 cmdscan
```

Info:

```
**************************************************
CommandProcess: conhost.exe Pid: 2104
CommandHistory: 0x300498 Application: cmd.exe Flags: Allocated, Reset
CommandCount: 1 LastAdded: 0 LastDisplayed: 0
FirstCommand: 0 CommandCountMax: 50
ProcessHandle: 0x5c
Cmd #0 @ 0x2f43c0: C:\Python27\python.exe C:\Users\hello\Desktop\demon.py.txt
Cmd #12 @ 0x2d0039: ???
Cmd #19 @ 0x300030: ???
Cmd #22 @ 0xff818488: ?
Cmd #25 @ 0xff818488: ?
Cmd #36 @ 0x2d00c4: /?0?-???-
Cmd #37 @ 0x2fd058: 0?-????
**************************************************
CommandProcess: conhost.exe Pid: 2424
CommandHistory: 0x2b04c8 Application: DumpIt.exe Flags: Allocated
CommandCount: 0 LastAdded: -1 LastDisplayed: -1
FirstCommand: 0 CommandCountMax: 50
ProcessHandle: 0x5c
Cmd #22 @ 0xff818488: ?
Cmd #25 @ 0xff818488: ?
Cmd #36 @ 0x2800c4: *?+?(???(
Cmd #37 @ 0x2ad070: +?(????
```

#### Volatility3

```shell
./vol.py -f Challenge.raw windows.cmdscan 
```

Con este comando dara error pero por que no soporta perfiles tan bajos a nivel de sistema operativo, en este caso es recomendable la de `v2`, ya que al tratarse de un `Windows` de versiones tan bajas el de `v3` nos dara un error, pero para versiones altas si nos sirve.

Por lo que vemos en la salida de `v2` veremos que se han registrado varios comandos a nivel de sistema y veremos bastante raro estas lineas:

```
Cmd #0 @ 0x2f43c0: C:\Python27\python.exe C:\Users\hello\Desktop\demon.py.txt

CommandHistory: 0x2b04c8 Application: DumpIt.exe Flags: Allocated
```

Por lo que ya vamos obteniendo informacion mucho mas valiosa que antes.

Con el parametro `consoles` podremos ver todas las instrucciones que el usuario a ejecutado en la terminal del sistema, absolutamente todas, por lo que con ese parametro nos detalla mas la busqueda.

#### Volatility2

```shell
./vol.py -f Challenge.raw --profile=Win7SP1x86_23418 consoles
```

Info:

```
**************************************************
ConsoleProcess: conhost.exe Pid: 2104
Console: 0xe981c0 CommandHistorySize: 50
HistoryBufferCount: 2 HistoryBufferMax: 4
OriginalTitle: %SystemRoot%\system32\cmd.exe
Title: C:\Windows\system32\cmd.exe
AttachedProcess: cmd.exe Pid: 2096 Handle: 0x5c
----
CommandHistory: 0x300690 Application: python.exe Flags: 
CommandCount: 0 LastAdded: -1 LastDisplayed: -1
FirstCommand: 0 CommandCountMax: 50
ProcessHandle: 0x0
----
CommandHistory: 0x300498 Application: cmd.exe Flags: Allocated, Reset
CommandCount: 1 LastAdded: 0 LastDisplayed: 0
FirstCommand: 0 CommandCountMax: 50
ProcessHandle: 0x5c
Cmd #0 at 0x2f43c0: C:\Python27\python.exe C:\Users\hello\Desktop\demon.py.txt
----
Screen 0x2e6368 X:80 Y:300
Dump:
Microsoft Windows [Version 6.1.7601]                                            
Copyright (c) 2009 Microsoft Corporation.  All rights reserved.                 
                                                                                
C:\Users\hello>C:\Python27\python.exe C:\Users\hello\Desktop\demon.py.txt       
335d366f5d6031767631707f                                                        
                                                                                
C:\Users\hello>                                                                 
**************************************************
ConsoleProcess: conhost.exe Pid: 2424
Console: 0xe981c0 CommandHistorySize: 50
HistoryBufferCount: 1 HistoryBufferMax: 4
OriginalTitle: C:\Users\hello\Desktop\DumpIt\DumpIt.exe
Title: C:\Users\hello\Desktop\DumpIt\DumpIt.exe
AttachedProcess: DumpIt.exe Pid: 2412 Handle: 0x5c
----
CommandHistory: 0x2b04c8 Application: DumpIt.exe Flags: Allocated
CommandCount: 0 LastAdded: -1 LastDisplayed: -1
FirstCommand: 0 CommandCountMax: 50
ProcessHandle: 0x5c
----
Screen 0x2963a0 X:80 Y:300
Dump:
  DumpIt - v1.3.2.20110401 - One click memory memory dumper                     
  Copyright (c) 2007 - 2011, Matthieu Suiche <http://www.msuiche.net>           
  Copyright (c) 2010 - 2011, MoonSols <http://www.moonsols.com>                 
                                                                                
                                                                                
    Address space size:        1048510464 bytes (    999 Mb)                    
    Free space size:          20896800768 bytes (  19928 Mb)                    
                                                                                
    * Destination = \??\C:\Users\hello\Desktop\DumpIt\HELLO-PC-20181023-083048.r
aw                                                                              
                                                                                
    --> Are you sure you want to continue? [y/n] y                              
    + Processing...
```

#### Volatility3

```shell
./vol.py -f Challenge.raw windows.consoles 
```

En esta parte de aqui pasa lo mismo de antes, si no es compatible con el `profile` dara un error.

Con esta linea de la `v2` podemos ver mejor que se trata del `dump` de la memoria por lo que no es malicioso:

```
* Destination = \??\C:\Users\hello\Desktop\DumpIt\HELLO-PC-20181023-083048.r
aw
```

Pero en esta linea de aqui si es bastante sospechosa:

```
Cmd #0 at 0x2f43c0: C:\Python27\python.exe C:\Users\hello\Desktop\demon.py.txt
```

Con el parametro `cmdline` podremos ver como una especie de agrupacion o combinacion de los comandos anteriores mostrando directamente toda la informacion de lo que se ha estado ejecutando en el sistema.

#### Volatility2

```shell
./vol.py -f Challenge.raw --profile=Win7SP1x86_23418 cmdline
```

Info:

```
************************************************************************
System pid:      4
************************************************************************
smss.exe pid:    260
Command line : \SystemRoot\System32\smss.exe
************************************************************************
csrss.exe pid:    340
Command line : %SystemRoot%\system32\csrss.exe ObjectDirectory=\Windows SharedSection=1024,12288,512 Windows=On SubSystemType=Windows ServerDll=basesrv,1 ServerDll=winsrv:UserServerDllInitialization,3 ServerDll=winsrv:ConServerDllInitialization,2 ServerDll=sxssrv,4 ProfileControl=Off MaxRequestThreads=16
************************************************************************
csrss.exe pid:    380
Command line : %SystemRoot%\system32\csrss.exe ObjectDirectory=\Windows SharedSection=1024,12288,512 Windows=On SubSystemType=Windows ServerDll=basesrv,1 ServerDll=winsrv:UserServerDllInitialization,3 ServerDll=winsrv:ConServerDllInitialization,2 ServerDll=sxssrv,4 ProfileControl=Off MaxRequestThreads=16
************************************************************************
wininit.exe pid:    388
Command line : wininit.exe
************************************************************************
winlogon.exe pid:    424
Command line : winlogon.exe
************************************************************************
services.exe pid:    484
Command line : C:\Windows\system32\services.exe
************************************************************************
lsass.exe pid:    492
Command line : C:\Windows\system32\lsass.exe
************************************************************************
lsm.exe pid:    500
Command line : C:\Windows\system32\lsm.exe
************************************************************************
svchost.exe pid:    592
Command line : C:\Windows\system32\svchost.exe -k DcomLaunch
************************************************************************
VBoxService.ex pid:    652
Command line : C:\Windows\System32\VBoxService.exe
************************************************************************
svchost.exe pid:    716
Command line : C:\Windows\system32\svchost.exe -k RPCSS
************************************************************************
svchost.exe pid:    804
Command line : C:\Windows\System32\svchost.exe -k LocalServiceNetworkRestricted
************************************************************************
svchost.exe pid:    848
Command line : C:\Windows\System32\svchost.exe -k LocalSystemNetworkRestricted
************************************************************************
svchost.exe pid:    872
Command line : C:\Windows\system32\svchost.exe -k LocalService
************************************************************************
svchost.exe pid:    896
Command line : C:\Windows\system32\svchost.exe -k netsvcs
************************************************************************
audiodg.exe pid:    988
Command line : C:\Windows\system32\AUDIODG.EXE 0x2ac
************************************************************************
svchost.exe pid:   1192
Command line : C:\Windows\system32\svchost.exe -k NetworkService
************************************************************************
spoolsv.exe pid:   1336
Command line : C:\Windows\System32\spoolsv.exe
************************************************************************
svchost.exe pid:   1364
Command line : C:\Windows\system32\svchost.exe -k LocalServiceNoNetwork
************************************************************************
svchost.exe pid:   1460
Command line : C:\Windows\System32\svchost.exe -k utcsvc
************************************************************************
svchost.exe pid:   1488
Command line : C:\Windows\system32\svchost.exe -k LocalServiceAndNoImpersonation
************************************************************************
taskhost.exe pid:    308
Command line : "taskhost.exe"
************************************************************************
sppsvc.exe pid:   1164
Command line : C:\Windows\system32\sppsvc.exe
************************************************************************
dwm.exe pid:   1992
Command line : "C:\Windows\system32\Dwm.exe"
************************************************************************
explorer.exe pid:    324
Command line : C:\Windows\Explorer.EXE
************************************************************************
VBoxTray.exe pid:   1000
Command line : "C:\Windows\System32\VBoxTray.exe" 
************************************************************************
SearchIndexer. pid:   2032
Command line : C:\Windows\system32\SearchIndexer.exe /Embedding
************************************************************************
SearchProtocol pid:    284
Command line : "C:\Windows\system32\SearchProtocolHost.exe" Global\UsGthrFltPipeMssGthrPipe1_ Global\UsGthrCtrlFltPipeMssGthrPipe1 1 -2147483646 "Software\Microsoft\Windows Search" "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT; MS Search 4.0 Robot)" "C:\ProgramData\Microsoft\Search\Data\Temp\usgthrsvc" "DownLevelDaemon" 
************************************************************************
SearchFilterHo pid:   1292
Command line : "C:\Windows\system32\SearchFilterHost.exe" 0 520 524 532 65536 528 
************************************************************************
cmd.exe pid:   2096
Command line : "C:\Windows\system32\cmd.exe" 
************************************************************************
conhost.exe pid:   2104
Command line : \??\C:\Windows\system32\conhost.exe "9597847671419376088700206021-7055470871162148935-704730587-1400429052-1906668177
************************************************************************
DumpIt.exe pid:   2412
Command line : "C:\Users\hello\Desktop\DumpIt\DumpIt.exe" 
************************************************************************
conhost.exe pid:   2424
Command line : \??\C:\Windows\system32\conhost.exe "499080522-1749980471992366858-146566314551631531-193375578852495345-1447858489
```

#### Volatility3

```shell
./vol.py -f Challenge.raw windows.cmdline
```

Info:

```
Volatility 3 Framework 2.26.2
Progress:  100.00               PDB scanning finished                        
PID     Process Args

4       System  -
260     smss.exe        \SystemRoot\System32\smss.exe
340     csrss.exe       %SystemRoot%\system32\csrss.exe ObjectDirectory=\Windows SharedSection=1024,12288,512 Windows=On SubSystemType=Windows ServerDll=basesrv,1 ServerDll=winsrv:UserServerDllInitialization,3 ServerDll=winsrv:ConServerDllInitialization,2 ServerDll=sxssrv,4 ProfileControl=Off MaxRequestThreads=16
380     csrss.exe       %SystemRoot%\system32\csrss.exe ObjectDirectory=\Windows SharedSection=1024,12288,512 Windows=On SubSystemType=Windows ServerDll=basesrv,1 ServerDll=winsrv:UserServerDllInitialization,3 ServerDll=winsrv:ConServerDllInitialization,2 ServerDll=sxssrv,4 ProfileControl=Off MaxRequestThreads=16
388     wininit.exe     wininit.exe
424     winlogon.exe    winlogon.exe
484     services.exe    C:\Windows\system32\services.exe
492     lsass.exe       C:\Windows\system32\lsass.exe
500     lsm.exe C:\Windows\system32\lsm.exe
592     svchost.exe     C:\Windows\system32\svchost.exe -k DcomLaunch
652     VBoxService.ex  C:\Windows\System32\VBoxService.exe
716     svchost.exe     C:\Windows\system32\svchost.exe -k RPCSS
804     svchost.exe     C:\Windows\System32\svchost.exe -k LocalServiceNetworkRestricted
848     svchost.exe     C:\Windows\System32\svchost.exe -k LocalSystemNetworkRestricted
872     svchost.exe     C:\Windows\system32\svchost.exe -k LocalService
896     svchost.exe     C:\Windows\system32\svchost.exe -k netsvcs
988     audiodg.exe     C:\Windows\system32\AUDIODG.EXE 0x2ac
1192    svchost.exe     C:\Windows\system32\svchost.exe -k NetworkService
1336    spoolsv.exe     C:\Windows\System32\spoolsv.exe
1364    svchost.exe     C:\Windows\system32\svchost.exe -k LocalServiceNoNetwork
1460    svchost.exe     C:\Windows\System32\svchost.exe -k utcsvc
1488    svchost.exe     C:\Windows\system32\svchost.exe -k LocalServiceAndNoImpersonation
308     taskhost.exe    "taskhost.exe"
1164    sppsvc.exe      C:\Windows\system32\sppsvc.exe
1992    dwm.exe "C:\Windows\system32\Dwm.exe"
324     explorer.exe    C:\Windows\Explorer.EXE
1000    VBoxTray.exe    "C:\Windows\System32\VBoxTray.exe" 
2032    SearchIndexer.  C:\Windows\system32\SearchIndexer.exe /Embedding
284     SearchProtocol  "C:\Windows\system32\SearchProtocolHost.exe" Global\UsGthrFltPipeMssGthrPipe1_ Global\UsGthrCtrlFltPipeMssGthrPipe1 1 -2147483646 "Software\Microsoft\Windows Search" "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT; MS Search 4.0 Robot)" "C:\ProgramData\Microsoft\Search\Data\Temp\usgthrsvc" "DownLevelDaemon" 
1292    SearchFilterHo  "C:\Windows\system32\SearchFilterHost.exe" 0 520 524 532 65536 528 
2096    cmd.exe "C:\Windows\system32\cmd.exe" 
2104    conhost.exe     \??\C:\Windows\system32\conhost.exe "9597847671419376088700206021-7055470871162148935-704730587-1400429052-1906668177
2412    DumpIt.exe      "C:\Users\hello\Desktop\DumpIt\DumpIt.exe" 
2424    conhost.exe     \??\C:\Windows\system32\conhost.exe "499080522-1749980471992366858-146566314551631531-193375578852495345-1447858489
```

En este caso funciona para las `2` versiones el parametro `cmdline` con este tipo de `profile`.

### Obtener informacion de las DLLs que estan ejecutandose dentro del sistema en ese momento

Con el parametro `dlllist` podremos obtener la informacion de todas las `DLLs` que se estaban ejecutando en ese momento, con esto podremos ver de forma mas detallada que procesos pueden ser maliciosos respecto a las `DLLs` que estaban activas en ese momento.

#### Volatility2

```shell
./vol.py -f Challenge.raw --profile=Win7SP1x86_23418 dlllist
```

Info:

```
************************************************************************
System pid:      4
Unable to read PEB for task.
************************************************************************
smss.exe pid:    260
Command line : \SystemRoot\System32\smss.exe


Base             Size  LoadCount LoadTime                       Path
---------- ---------- ---------- ------------------------------ ----
0x47640000    0x13000     0xffff 1513472                        \SystemRoot\System32\smss.exe
0x76e50000   0x142000     0xffff 1513600                        C:\Windows\SYSTEM32\ntdll.dll
************************************************************************
csrss.exe pid:    340
Command line : %SystemRoot%\system32\csrss.exe ObjectDirectory=\Windows SharedSection=1024,12288,512 Windows=On SubSystemType=Windows ServerDll=basesrv,1 ServerDll=winsrv:UserServerDllInitialization,3 ServerDll=winsrv:ConServerDllInitialization,2 ServerDll=sxssrv,4 ProfileControl=Off MaxRequestThreads=16
Service Pack 1

Base             Size  LoadCount LoadTime                       Path
---------- ---------- ---------- ------------------------------ ----
0x4a5a0000     0x5000     0xffff 3675776                        C:\Windows\system32\csrss.exe
0x76e50000   0x142000     0xffff 3675904                        C:\Windows\SYSTEM32\ntdll.dll
0x74fa0000     0xd000     0xffff 3677352                        C:\Windows\system32\CSRSRV.dll
0x74f90000     0xe000        0x4 3677008                        C:\Windows\system32\basesrv.DLL
0x74f60000    0x2c000        0x2 3679208                        C:\Windows\system32\winsrv.DLL
0x75430000    0xc9000        0xb 3678536                        C:\Windows\system32\USER32.dll
0x762d0000    0x4e000        0xc 3678760                        C:\Windows\system32\GDI32.dll
0x76980000    0xd5000       0x44 3678992                        C:\Windows\SYSTEM32\kernel32.dll
0x75050000    0x4b000       0xe0 3679496                        C:\Windows\system32\KERNELBASE.dll
0x75280000     0xa000        0x3 3679808                        C:\Windows\system32\LPK.dll
0x76fe0000    0x9d000        0x3 3725264                        C:\Windows\system32\USP10.dll
0x75290000    0xac000        0x3 3725464                        C:\Windows\system32\msvcrt.dll
0x74f50000     0x9000        0x1 3735856                        C:\Windows\system32\sxssrv.DLL
0x74ea0000    0x5f000        0x1 3741696                        C:\Windows\system32\sxs.dll
0x76660000    0xa2000        0x1 3771560                        C:\Windows\system32\RPCRT4.dll
0x74e90000     0xc000        0x1 3771688                        C:\Windows\system32\CRYPTBASE.dll
************************************************************************
csrss.exe pid:    380
Command line : %SystemRoot%\system32\csrss.exe ObjectDirectory=\Windows SharedSection=1024,12288,512 Windows=On SubSystemType=Windows ServerDll=basesrv,1 ServerDll=winsrv:UserServerDllInitialization,3 ServerDll=winsrv:ConServerDllInitialization,2 ServerDll=sxssrv,4 ProfileControl=Off MaxRequestThreads=16
Service Pack 1

Base             Size  LoadCount LoadTime                       Path
---------- ---------- ---------- ------------------------------ ----
0x4a5a0000     0x5000     0xffff 2299520                        C:\Windows\system32\csrss.exe
0x76e50000   0x142000     0xffff 2299648                        C:\Windows\SYSTEM32\ntdll.dll
0x74fa0000     0xd000     0xffff 2301096                        C:\Windows\system32\CSRSRV.dll
0x74f90000     0xe000        0x4 2300768                        C:\Windows\system32\basesrv.DLL
0x74f60000    0x2c000        0x2 2302952                        C:\Windows\system32\winsrv.DLL
0x75430000    0xc9000        0xb 2302280                        C:\Windows\system32\USER32.dll
0x762d0000    0x4e000        0xc 2302504                        C:\Windows\system32\GDI32.dll
0x76980000    0xd5000       0x63 2302736                        C:\Windows\SYSTEM32\kernel32.dll
0x75050000    0x4b000      0x13a 2303240                        C:\Windows\system32\KERNELBASE.dll
0x75280000     0xa000        0x3 2303552                        C:\Windows\system32\LPK.dll
0x76fe0000    0x9d000        0x3 2349008                        C:\Windows\system32\USP10.dll
0x75290000    0xac000        0x5 2349208                        C:\Windows\system32\msvcrt.dll
0x74f50000     0x9000        0x1 2359040                        C:\Windows\system32\sxssrv.DLL
0x74ea0000    0x5f000        0x1 2366704                        C:\Windows\system32\sxs.dll
0x76660000    0xa2000        0x3 2400600                        C:\Windows\system32\RPCRT4.dll
0x74e90000     0xc000        0x2 2400728                        C:\Windows\system32\CRYPTBASE.dll
0x76380000    0xa1000        0x1 2400856                        C:\Windows\system32\ADVAPI32.dll
0x762b0000    0x19000        0x4 2400984                        C:\Windows\SYSTEM32\sechost.dll
************************************************************************
wininit.exe pid:    388
Command line : wininit.exe
Service Pack 1

Base             Size  LoadCount LoadTime                       Path
---------- ---------- ---------- ------------------------------ ----
0x00b20000    0x1a000     0xffff 4265048                        C:\Windows\system32\wininit.exe
0x76e50000   0x142000     0xffff 4265176                        C:\Windows\SYSTEM32\ntdll.dll
0x76980000    0xd5000     0xffff 4265936                        C:\Windows\system32\kernel32.dll
0x75050000    0x4b000     0xffff 4266168                        C:\Windows\system32\KERNELBASE.dll
0x75430000    0xc9000     0xffff 4268000                        C:\Windows\system32\USER32.dll
0x762d0000    0x4e000     0xffff 4268224                        C:\Windows\system32\GDI32.dll
0x75280000     0xa000     0xffff 4268512                        C:\Windows\system32\LPK.dll
0x76fe0000    0x9d000     0xffff 4268832                        C:\Windows\system32\USP10.dll
0x75290000    0xac000     0xffff 4269032                        C:\Windows\system32\msvcrt.dll
0x76660000    0xa2000     0xffff 4314488                        C:\Windows\system32\RPCRT4.dll
0x762b0000    0x19000     0xffff 4315240                        C:\Windows\SYSTEM32\sechost.dll
0x74f10000     0xb000     0xffff 4314808                        C:\Windows\system32\profapi.dll
0x75340000    0x1f000        0x2 4320128                        C:\Windows\system32\IMM32.DLL
0x75360000    0xcd000        0x1 4319576                        C:\Windows\system32\MSCTF.dll
0x74f00000     0xe000        0x1 4330104                        C:\Windows\system32\RpcRtRemote.dll
0x74e40000    0x4c000     0xffff 4366168                        C:\Windows\system32\apphelp.dll
0x74e90000     0xc000        0x1 4366296                        C:\Windows\system32\CRYPTBASE.dll
0x76fa0000    0x35000        0x6 4366424                        C:\Windows\system32\WS2_32.dll
0x76320000     0x6000        0x6 4366552                        C:\Windows\system32\NSI.dll
0x74960000    0x3c000        0x3 4366680                        C:\Windows\system32\mswsock.dll
0x74440000     0x5000        0x1 4366936                        C:\Windows\System32\wshtcpip.dll
0x74950000     0x6000        0x1 4367192                        C:\Windows\System32\wship6.dll
0x74c20000     0x8000        0x1 4367576                        C:\Windows\system32\secur32.dll
0x74e20000    0x1b000        0x2 4367704                        C:\Windows\system32\SSPICLI.DLL
0x74630000     0x8000        0x1 4367960                        C:\Windows\system32\credssp.dll
0x76380000    0xa1000        0x1 4367832                        C:\Windows\system32\ADVAPI32.dll
************************************************************************
winlogon.exe pid:    424
Command line : winlogon.exe
Service Pack 1

Base             Size  LoadCount LoadTime                       Path
---------- ---------- ---------- ------------------------------ ----
0x00bb0000    0x4c000     0xffff 2298976                        C:\Windows\system32\winlogon.exe
0x76e50000   0x142000     0xffff 2299104                        C:\Windows\SYSTEM32\ntdll.dll
0x76980000    0xd5000     0xffff 2299864                        C:\Windows\system32\kernel32.dll
0x75050000    0x4b000     0xffff 2300096                        C:\Windows\system32\KERNELBASE.dll
0x75430000    0xc9000     0xffff 2301952                        C:\Windows\system32\USER32.dll
0x762d0000    0x4e000     0xffff 2302176                        C:\Windows\system32\GDI32.dll
0x75280000     0xa000     0xffff 2302464                        C:\Windows\system32\LPK.dll
0x76fe0000    0x9d000     0xffff 2302784                        C:\Windows\system32\USP10.dll
0x75290000    0xac000     0xffff 2302984                        C:\Windows\system32\msvcrt.dll
0x74f20000    0x29000     0xffff 2349112                        C:\Windows\system32\WINSTA.dll
0x76660000    0xa2000     0xffff 2348440                        C:\Windows\system32\RPCRT4.dll
0x75340000    0x1f000        0x2 2353880                        C:\Windows\system32\IMM32.DLL
0x75360000    0xcd000        0x1 2353328                        C:\Windows\system32\MSCTF.dll
0x76380000    0xa1000        0x6 2362816                        C:\Windows\system32\ADVAPI32.dll
0x762b0000    0x19000       0x22 2363568                        C:\Windows\SYSTEM32\sechost.dll
0x74f10000     0xb000        0x1 2363344                        C:\Windows\system32\profapi.dll
0x74f00000     0xe000        0x1 2376920                        C:\Windows\system32\RpcRtRemote.dll
0x74e40000    0x4c000     0xffff 2377048                        C:\Windows\system32\apphelp.dll
0x72eb0000     0x8000        0x1 2377176                        C:\Windows\system32\UXINIT.dll
0x73a10000    0x40000        0x3 2377944                        C:\Windows\system32\UxTheme.dll
0x749a0000    0x17000        0x1 2378072                        C:\Windows\system32\CRYPTSP.dll
0x74730000    0x3b000        0x1 2378200                        C:\Windows\system32\rsaenh.dll
0x74e90000     0xc000        0x1 2378328                        C:\Windows\system32\CRYPTBASE.dll
0x735d0000   0x130000        0x1 2378456                        C:\Windows\system32\WindowsCodecs.dll
0x75500000   0x15d000        0x1 2378584                        C:\Windows\system32\ole32.dll
0x73520000     0xf000        0x1 2378712                        C:\Windows\system32\wkscli.dll
0x74a70000    0x2b000        0x1 2378840                        C:\Windows\system32\netjoin.dll
0x73530000     0x9000        0x2 2378968                        C:\Windows\system32\netutils.dll
0x74e20000    0x1b000        0x1 2379096                        C:\Windows\system32\SspiCli.dll
0x730b0000     0xa000        0x1 2379224                        C:\Windows\system32\slc.dll
0x74360000    0x12000        0x1 2379352                        C:\Windows\system32\MPR.dll
************************************************************************
.................................<RESTO_DE_DLLs>...................................
```

#### Volatility3

```shell
./vol.py -f Challenge.raw windows.dlllist 
```

Info:

```
Volatility 3 Framework 2.26.2
Progress:  100.00               PDB scanning finished                        
PID     Process Base    Size    Name    Path    LoadTime        File output

260     smss.exe        0x47640000      0x13000 smss.exe        \SystemRoot\System32\smss.exe   N/A     Disabled
260     smss.exe        0x76e50000      0x142000        ntdll.dll       C:\Windows\SYSTEM32\ntdll.dll   N/A     Disabled
340     csrss.exe       0x4a5a0000      0x5000  csrss.exe       C:\Windows\system32\csrss.exe   N/A     Disabled
340     csrss.exe       0x76e50000      0x142000        ntdll.dll       C:\Windows\SYSTEM32\ntdll.dll   N/A     Disabled
340     csrss.exe       0x74fa0000      0xd000  CSRSRV.dll      C:\Windows\system32\CSRSRV.dll  2018-10-23 08:29:21.000000 UTC  Disabled
340     csrss.exe       0x74f90000      0xe000  basesrv.DLL     C:\Windows\system32\basesrv.DLL 2018-10-23 08:29:21.000000 UTC  Disabled
340     csrss.exe       0x74f60000      0x2c000 winsrv.DLL      C:\Windows\system32\winsrv.DLL  2018-10-23 08:29:22.000000 UTC  Disabled
340     csrss.exe       0x75430000      0xc9000 USER32.dll      C:\Windows\system32\USER32.dll  2018-10-23 08:29:22.000000 UTC  Disabled
340     csrss.exe       0x762d0000      0x4e000 GDI32.dll       C:\Windows\system32\GDI32.dll   2018-10-23 08:29:22.000000 UTC  Disabled
340     csrss.exe       0x76980000      0xd5000 kernel32.dll    C:\Windows\SYSTEM32\kernel32.dll        2018-10-23 08:29:22.000000 UTC  Disabled
340     csrss.exe       0x75050000      0x4b000 KERNELBASE.dll  C:\Windows\system32\KERNELBASE.dll      2018-10-23 08:29:22.000000 UTC  Disabled
340     csrss.exe       0x75280000      0xa000  LPK.dll C:\Windows\system32\LPK.dll     2018-10-23 08:29:22.000000 UTC  Disabled
340     csrss.exe       0x76fe0000      0x9d000 USP10.dll       C:\Windows\system32\USP10.dll   2018-10-23 08:29:22.000000 UTC  Disabled
340     csrss.exe       0x75290000      0xac000 msvcrt.dll      C:\Windows\system32\msvcrt.dll  2018-10-23 08:29:22.000000 UTC  Disabled
340     csrss.exe       0x74f50000      0x9000  sxssrv.DLL      C:\Windows\system32\sxssrv.DLL  2018-10-23 08:29:23.000000 UTC  Disabled
340     csrss.exe       0x74ea0000      0x5f000 sxs.dll C:\Windows\system32\sxs.dll     2018-10-23 08:29:25.000000 UTC  Disabled
340     csrss.exe       0x76660000      0xa2000 RPCRT4.dll      C:\Windows\system32\RPCRT4.dll  2018-10-23 08:29:25.000000 UTC  Disabled
340     csrss.exe       0x74e90000      0xc000  CRYPTBASE.dll   C:\Windows\system32\CRYPTBASE.dll       2018-10-23 08:29:25.000000 UTC  Disabled
380     csrss.exe       0x4a5a0000      0x5000  csrss.exe       C:\Windows\system32\csrss.exe   N/A     Disabled
380     csrss.exe       0x76e50000      0x142000        ntdll.dll       C:\Windows\SYSTEM32\ntdll.dll   N/A     Disabled
380     csrss.exe       0x74fa0000      0xd000  CSRSRV.dll      C:\Windows\system32\CSRSRV.dll  2018-10-23 08:29:23.000000 UTC  Disabled
380     csrss.exe       0x74f90000      0xe000  basesrv.DLL     C:\Windows\system32\basesrv.DLL 2018-10-23 08:29:23.000000 UTC  Disabled
380     csrss.exe       0x74f60000      0x2c000 winsrv.DLL      C:\Windows\system32\winsrv.DLL  2018-10-23 08:29:23.000000 UTC  Disabled
380     csrss.exe       0x75430000      0xc9000 USER32.dll      C:\Windows\system32\USER32.dll  2018-10-23 08:29:23.000000 UTC  Disabled
380     csrss.exe       0x762d0000      0x4e000 GDI32.dll       C:\Windows\system32\GDI32.dll   2018-10-23 08:29:23.000000 UTC  Disabled
380     csrss.exe       0x76980000      0xd5000 kernel32.dll    C:\Windows\SYSTEM32\kernel32.dll        2018-10-23 08:29:23.000000 UTC  Disabled
380     csrss.exe       0x75050000      0x4b000 KERNELBASE.dll  C:\Windows\system32\KERNELBASE.dll      2018-10-23 08:29:23.000000 UTC  Disabled
380     csrss.exe       0x75280000      0xa000  LPK.dll C:\Windows\system32\LPK.dll     2018-10-23 08:29:23.000000 UTC  Disabled
380     csrss.exe       0x76fe0000      0x9d000 USP10.dll       C:\Windows\system32\USP10.dll   2018-10-23 08:29:23.000000 UTC  Disabled
380     csrss.exe       0x75290000      0xac000 msvcrt.dll      C:\Windows\system32\msvcrt.dll  2018-10-23 08:29:23.000000 UTC  Disabled
380     csrss.exe       0x74f50000      0x9000  sxssrv.DLL      C:\Windows\system32\sxssrv.DLL  2018-10-23 08:29:23.000000 UTC  Disabled
380     csrss.exe       0x74ea0000      0x5f000 sxs.dll C:\Windows\system32\sxs.dll     2018-10-23 08:29:32.000000 UTC  Disabled
380     csrss.exe       0x76660000      0xa2000 RPCRT4.dll      C:\Windows\system32\RPCRT4.dll  2018-10-23 08:29:32.000000 UTC  Disabled
380     csrss.exe       0x74e90000      0xc000  CRYPTBASE.dll   C:\Windows\system32\CRYPTBASE.dll       2018-10-23 08:29:32.000000 UTC  Disabled
380     csrss.exe       0x76380000      0xa1000 ADVAPI32.dll    C:\Windows\system32\ADVAPI32.dll        2018-10-23 08:30:18.000000 UTC  Disabled
380     csrss.exe       0x762b0000      0x19000 sechost.dll     C:\Windows\SYSTEM32\sechost.dll 2018-10-23 08:30:18.000000 UTC  Disabled
388     wininit.exe     0xb20000        0x1a000 wininit.exe     C:\Windows\system32\wininit.exe N/A     Disabled
388     wininit.exe     0x76e50000      0x142000        ntdll.dll       C:\Windows\SYSTEM32\ntdll.dll   N/A     Disabled
388     wininit.exe     0x76980000      0xd5000 kernel32.dll    C:\Windows\system32\kernel32.dll        2018-10-23 08:29:23.000000 UTC  Disabled
388     wininit.exe     0x75050000      0x4b000 KERNELBASE.dll  C:\Windows\system32\KERNELBASE.dll      2018-10-23 08:29:23.000000 UTC  Disabled
388     wininit.exe     0x75430000      0xc9000 USER32.dll      C:\Windows\system32\USER32.dll  2018-10-23 08:29:23.000000 UTC  Disabled
388     wininit.exe     0x762d0000      0x4e000 GDI32.dll       C:\Windows\system32\GDI32.dll   2018-10-23 08:29:23.000000 UTC  Disabled
388     wininit.exe     0x75280000      0xa000  LPK.dll C:\Windows\system32\LPK.dll     2018-10-23 08:29:23.000000 UTC  Disabled
388     wininit.exe     0x76fe0000      0x9d000 USP10.dll       C:\Windows\system32\USP10.dll   2018-10-23 08:29:23.000000 UTC  Disabled
388     wininit.exe     0x75290000      0xac000 msvcrt.dll      C:\Windows\system32\msvcrt.dll  2018-10-23 08:29:23.000000 UTC  Disabled
388     wininit.exe     0x76660000      0xa2000 RPCRT4.dll      C:\Windows\system32\RPCRT4.dll  2018-10-23 08:29:23.000000 UTC  Disabled
388     wininit.exe     0x762b0000      0x19000 sechost.dll     C:\Windows\SYSTEM32\sechost.dll 2018-10-23 08:29:23.000000 UTC  Disabled
388     wininit.exe     0x74f10000      0xb000  profapi.dll     C:\Windows\system32\profapi.dll 2018-10-23 08:29:23.000000 UTC  Disabled
388     wininit.exe     0x75340000      0x1f000 IMM32.DLL       C:\Windows\system32\IMM32.DLL   2018-10-23 08:29:23.000000 UTC  Disabled
388     wininit.exe     0x75360000      0xcd000 MSCTF.dll       C:\Windows\system32\MSCTF.dll   2018-10-23 08:29:23.000000 UTC  Disabled
388     wininit.exe     0x74f00000      0xe000  RpcRtRemote.dll C:\Windows\system32\RpcRtRemote.dll     2018-10-23 08:29:24.000000 UTC  Disabled
388     wininit.exe     0x74e40000      0x4c000 apphelp.dll     C:\Windows\system32\apphelp.dll 2018-10-23 08:29:25.000000 UTC  Disabled
388     wininit.exe     0x74e90000      0xc000  CRYPTBASE.dll   C:\Windows\system32\CRYPTBASE.dll       2018-10-23 08:29:30.000000 UTC  Disabled
388     wininit.exe     0x76fa0000      0x35000 WS2_32.dll      C:\Windows\system32\WS2_32.dll  2018-10-23 08:29:32.000000 UTC  Disabled
388     wininit.exe     0x76320000      0x6000  NSI.dll C:\Windows\system32\NSI.dll     2018-10-23 08:29:32.000000 UTC  Disabled
388     wininit.exe     0x74960000      0x3c000 mswsock.dll     C:\Windows\system32\mswsock.dll 2018-10-23 08:29:32.000000 UTC  Disabled
388     wininit.exe     0x74440000      0x5000  wshtcpip.dll    C:\Windows\System32\wshtcpip.dll        2018-10-23 08:29:32.000000 UTC  Disabled
388     wininit.exe     0x74950000      0x6000  wship6.dll      C:\Windows\System32\wship6.dll  2018-10-23 08:29:32.000000 UTC  Disabled
388     wininit.exe     0x74c20000      0x8000  secur32.dll     C:\Windows\system32\secur32.dll 2018-10-23 08:29:32.000000 UTC  Disabled
388     wininit.exe     0x74e20000      0x1b000 SSPICLI.DLL     C:\Windows\system32\SSPICLI.DLL 2018-10-23 08:29:32.000000 UTC  Disabled
388     wininit.exe     0x74630000      0x8000  credssp.dll     C:\Windows\system32\credssp.dll 2018-10-23 08:29:32.000000 UTC  Disabled
388     wininit.exe     0x76380000      0xa1000 ADVAPI32.dll    C:\Windows\system32\ADVAPI32.dll        2018-10-23 08:29:35.000000 UTC  Disabled
424     winlogon.exe    0xbb0000        0x4c000 winlogon.exe    C:\Windows\system32\winlogon.exe        N/A     Disabled
424     winlogon.exe    0x76e50000      0x142000        ntdll.dll       C:\Windows\SYSTEM32\ntdll.dll   N/A     Disabled
424     winlogon.exe    0x76980000      0xd5000 kernel32.dll    C:\Windows\system32\kernel32.dll        2018-10-23 08:29:23.000000 UTC  Disabled
424     winlogon.exe    0x75050000      0x4b000 KERNELBASE.dll  C:\Windows\system32\KERNELBASE.dll      2018-10-23 08:29:23.000000 UTC  Disabled
424     winlogon.exe    0x75430000      0xc9000 USER32.dll      C:\Windows\system32\USER32.dll  2018-10-23 08:29:23.000000 UTC  Disabled
424     winlogon.exe    0x762d0000      0x4e000 GDI32.dll       C:\Windows\system32\GDI32.dll   2018-10-23 08:29:23.000000 UTC  Disabled
424     winlogon.exe    0x75280000      0xa000  LPK.dll C:\Windows\system32\LPK.dll     2018-10-23 08:29:23.000000 UTC  Disabled
424     winlogon.exe    0x76fe0000      0x9d000 USP10.dll       C:\Windows\system32\USP10.dll   2018-10-23 08:29:23.000000 UTC  Disabled
424     winlogon.exe    0x75290000      0xac000 msvcrt.dll      C:\Windows\system32\msvcrt.dll  2018-10-23 08:29:23.000000 UTC  Disabled
424     winlogon.exe    0x74f20000      0x29000 WINSTA.dll      C:\Windows\system32\WINSTA.dll  2018-10-23 08:29:23.000000 UTC  Disabled
424     winlogon.exe    0x76660000      0xa2000 RPCRT4.dll      C:\Windows\system32\RPCRT4.dll  2018-10-23 08:29:23.000000 UTC  Disabled
424     winlogon.exe    0x75340000      0x1f000 IMM32.DLL       C:\Windows\system32\IMM32.DLL   2018-10-23 08:29:23.000000 UTC  Disabled
424     winlogon.exe    0x75360000      0xcd000 MSCTF.dll       C:\Windows\system32\MSCTF.dll   2018-10-23 08:29:23.000000 UTC  Disabled
424     winlogon.exe    0x76380000      0xa1000 ADVAPI32.dll    C:\Windows\system32\ADVAPI32.dll        2018-10-23 08:29:24.000000 UTC  Disabled
424     winlogon.exe    0x762b0000      0x19000 sechost.dll     C:\Windows\SYSTEM32\sechost.dll 2018-10-23 08:29:24.000000 UTC  Disabled
424     winlogon.exe    0x74f10000      0xb000  profapi.dll     C:\Windows\system32\profapi.dll 2018-10-23 08:29:24.000000 UTC  Disabled
424     winlogon.exe    0x74f00000      0xe000  RpcRtRemote.dll C:\Windows\system32\RpcRtRemote.dll     2018-10-23 08:29:24.000000 UTC  Disabled
424     winlogon.exe    0x74e40000      0x4c000 apphelp.dll     C:\Windows\system32\apphelp.dll 2018-10-23 08:29:32.000000 UTC  Disabled
424     winlogon.exe    0x72eb0000      0x8000  UXINIT.dll      C:\Windows\system32\UXINIT.dll  2018-10-23 08:29:40.000000 UTC  Disabled
424     winlogon.exe    0x73a10000      0x40000 UxTheme.dll     C:\Windows\system32\UxTheme.dll 2018-10-23 08:29:40.000000 UTC  Disabled
424     winlogon.exe    0x749a0000      0x17000 CRYPTSP.dll     C:\Windows\system32\CRYPTSP.dll 2018-10-23 08:29:40.000000 UTC  Disabled
424     winlogon.exe    0x74730000      0x3b000 rsaenh.dll      C:\Windows\system32\rsaenh.dll  2018-10-23 08:29:40.000000 UTC  Disabled
424     winlogon.exe    0x74e90000      0xc000  CRYPTBASE.dll   C:\Windows\system32\CRYPTBASE.dll       2018-10-23 08:29:40.000000 UTC  Disabled
424     winlogon.exe    0x735d0000      0x130000        WindowsCodecs.dll       C:\Windows\system32\WindowsCodecs.dll   2018-10-23 08:29:40.000000 UTC  Disabled
424     winlogon.exe    0x75500000      0x15d000        ole32.dll       C:\Windows\system32\ole32.dll   2018-10-23 08:29:40.000000 UTC  Disabled
424     winlogon.exe    0x73520000      0xf000  wkscli.dll      C:\Windows\system32\wkscli.dll  2018-10-23 08:29:40.000000 UTC  Disabled
424     winlogon.exe    0x74a70000      0x2b000 netjoin.dll     C:\Windows\system32\netjoin.dll 2018-10-23 08:29:40.000000 UTC  Disabled
424     winlogon.exe    0x73530000      0x9000  netutils.dll    C:\Windows\system32\netutils.dll        2018-10-23 08:29:40.000000 UTC  Disabled
424     winlogon.exe    0x74e20000      0x1b000 SspiCli.dll     C:\Windows\system32\SspiCli.dll 2018-10-23 08:29:52.000000 UTC  Disabled
424     winlogon.exe    0x730b0000      0xa000  slc.dll C:\Windows\system32\slc.dll     2018-10-23 08:29:55.000000 UTC  Disabled
424     winlogon.exe    0x74360000      0x12000 MPR.dll C:\Windows\system32\MPR.dll     2018-10-23 08:30:04.000000 UTC  Disabled
484     services.exe    0xa80000        0x41000 services.exe    C:\Windows\system32\services.exe        N/A     Disabled
484     services.exe    0x76e50000      0x142000        ntdll.dll       C:\Windows\SYSTEM32\ntdll.dll   N/A     Disabled
484     services.exe    0x76980000      0xd5000 kernel32.dll    C:\Windows\system32\kernel32.dll        2018-10-23 08:29:25.000000 UTC  Disabled
484     services.exe    0x75050000      0x4b000 KERNELBASE.dll  C:\Windows\system32\KERNELBASE.dll      2018-10-23 08:29:25.000000 UTC  Disabled
484     services.exe    0x75290000      0xac000 msvcrt.dll      C:\Windows\system32\msvcrt.dll  2018-10-23 08:29:25.000000 UTC  Disabled
484     services.exe    0x76660000      0xa2000 RPCRT4.dll      C:\Windows\system32\RPCRT4.dll  2018-10-23 08:29:25.000000 UTC  Disabled
484     services.exe    0x74e20000      0x1b000 SspiCli.dll     C:\Windows\system32\SspiCli.dll 2018-10-23 08:29:25.000000 UTC  Disabled
484     services.exe    0x74f10000      0xb000  profapi.dll     C:\Windows\system32\profapi.dll 2018-10-23 08:29:25.000000 UTC  Disabled
484     services.exe    0x762b0000      0x19000 sechost.dll     C:\Windows\SYSTEM32\sechost.dll 2018-10-23 08:29:25.000000 UTC  Disabled
484     services.exe    0x74e90000      0xc000  CRYPTBASE.dll   C:\Windows\system32\CRYPTBASE.dll       2018-10-23 08:29:25.000000 UTC  Disabled
484     services.exe    0x74cd0000      0xf000  scext.dll       C:\Windows\system32\scext.dll   2018-10-23 08:29:25.000000 UTC  Disabled
484     services.exe    0x75430000      0xc9000 USER32.dll      C:\Windows\system32\USER32.dll  2018-10-23 08:29:25.000000 UTC  Disabled
484     services.exe    0x762d0000      0x4e000 GDI32.dll       C:\Windows\system32\GDI32.dll   2018-10-23 08:29:25.000000 UTC  Disabled
484     services.exe    0x75280000      0xa000  LPK.dll C:\Windows\system32\LPK.dll     2018-10-23 08:29:25.000000 UTC  Disabled
484     services.exe    0x76fe0000      0x9d000 USP10.dll       C:\Windows\system32\USP10.dll   2018-10-23 08:29:25.000000 UTC  Disabled
484     services.exe    0x74c20000      0x8000  Secur32.dll     C:\Windows\system32\Secur32.dll 2018-10-23 08:29:26.000000 UTC  Disabled
484     services.exe    0x74bd0000      0x4e000 SCESRV.dll      C:\Windows\system32\SCESRV.dll  2018-10-23 08:29:26.000000 UTC  Disabled
484     services.exe    0x74b40000      0x19000 srvcli.dll      C:\Windows\system32\srvcli.dll  2018-10-23 08:29:26.000000 UTC  Disabled
484     services.exe    0x75340000      0x1f000 IMM32.DLL       C:\Windows\system32\IMM32.DLL   2018-10-23 08:29:26.000000 UTC  Disabled
484     services.exe    0x75360000      0xcd000 MSCTF.dll       C:\Windows\system32\MSCTF.dll   2018-10-23 08:29:26.000000 UTC  Disabled
484     services.exe    0x74f00000      0xe000  RpcRtRemote.dll C:\Windows\system32\RpcRtRemote.dll     2018-10-23 08:29:30.000000 UTC  Disabled
484     services.exe    0x74630000      0x8000  credssp.dll     C:\Windows\system32\credssp.dll 2018-10-23 08:29:30.000000 UTC  Disabled
484     services.exe    0x74b10000      0x1b000 AUTHZ.dll       C:\Windows\system32\AUTHZ.dll   2018-10-23 08:29:30.000000 UTC  Disabled
484     services.exe    0x74600000      0x2d000 UBPM.dll        C:\Windows\system32\UBPM.dll    2018-10-23 08:29:30.000000 UTC  Disabled
484     services.exe    0x76380000      0xa1000 ADVAPI32.dll    C:\Windows\system32\ADVAPI32.dll        2018-10-23 08:29:30.000000 UTC  Disabled
484     services.exe    0x74e40000      0x4c000 apphelp.dll     C:\Windows\system32\apphelp.dll 2018-10-23 08:29:30.000000 UTC  Disabled
484     services.exe    0x74430000      0xd000  WTSAPI32.dll    C:\Windows\system32\WTSAPI32.dll        2018-10-23 08:29:43.000000 UTC  Disabled
484     services.exe    0x74f20000      0x29000 WINSTA.dll      C:\Windows\system32\WINSTA.dll  2018-10-23 08:29:43.000000 UTC  Disabled
484     services.exe    0x76fa0000      0x35000 WS2_32.dll      C:\Windows\system32\WS2_32.dll  2018-10-23 08:29:50.000000 UTC  Disabled
484     services.exe    0x76320000      0x6000  NSI.dll C:\Windows\system32\NSI.dll     2018-10-23 08:29:50.000000 UTC  Disabled
484     services.exe    0x74960000      0x3c000 mswsock.dll     C:\Windows\system32\mswsock.dll 2018-10-23 08:29:50.000000 UTC  Disabled
484     services.exe    0x74440000      0x5000  wshtcpip.dll    C:\Windows\System32\wshtcpip.dll        2018-10-23 08:29:50.000000 UTC  Disabled
484     services.exe    0x74950000      0x6000  wship6.dll      C:\Windows\System32\wship6.dll  2018-10-23 08:29:50.000000 UTC  Disabled
492     lsass.exe       0x5b0000        0x9000  lsass.exe       C:\Windows\system32\lsass.exe   N/A     Disabled
492     lsass.exe       0x76e50000      0x142000        ntdll.dll       C:\Windows\SYSTEM32\ntdll.dll   N/A     Disabled
492     lsass.exe       0x76980000      0xd5000 kernel32.dll    C:\Windows\system32\kernel32.dll        2018-10-23 08:29:25.000000 UTC  Disabled
492     lsass.exe       0x75050000      0x4b000 KERNELBASE.dll  C:\Windows\system32\KERNELBASE.dll      2018-10-23 08:29:25.000000 UTC  Disabled
492     lsass.exe       0x75290000      0xac000 msvcrt.dll      C:\Windows\system32\msvcrt.dll  2018-10-23 08:29:25.000000 UTC  Disabled
492     lsass.exe       0x76660000      0xa2000 RPCRT4.dll      C:\Windows\system32\RPCRT4.dll  2018-10-23 08:29:25.000000 UTC  Disabled
492     lsass.exe       0x74e10000      0x7000  SspiSrv.dll     
.................................<RESTO_DE_DLLs>...................................
```

Con esto podremos ver que nos muestra muchisima informacion sobre las `DLLs`.

### Obtener información de un proceso malicioso dumpeando dicho proceso entero

Con el parametro `memdump` junto con el `PID` del proceso y la ruta donde queremos que se nos descargue la informacion, podremos volcar la informacion de ficheros o de lo que conlleve dicho proceso a nuestro `host` para poder analizarlo de forma mas detallada.

Con el parametro que utilizamos de `cmdline` pongamos que el proceso con `PID` `2096` (`cmd.exe`) creemos que puede ser sospechoso, por lo que vamos a volcarlo de esta forma.

#### Volatility2

```shell
./vol.py -f Challenge.raw --profile=Win7SP1x86_23418 memdump -p 2096 --dump-dir .
```

Info:

```
************************************************************************
Writing cmd.exe [  2096] to 2096.dmp
```

Con esto veremos que ya se nos ha realizado el `dump` de dicho proceso.

#### Volatility3

```shell
mkdir dumps
./vol.py -f Challenge.raw -o ./dumps windows.dumpfiles --pid 2096
```

Info:

```
Volatility 3 Framework 2.26.2
Progress:  100.00               PDB scanning finished                        
Cache   FileObject      FileName        Result

DataSectionObject       0x851ac410      cmd.exe.mui     file.0x851ac410.0x851a9518.DataSectionObject.cmd.exe.mui.dat
ImageSectionObject      0x843d7908      KernelBase.dll  file.0x843d7908.0x84d5df10.ImageSectionObject.KernelBase.dll.img
DataSectionObject       0x851a9ec8      cmd.exe.mui     file.0x851a9ec8.0x851a9518.DataSectionObject.cmd.exe.mui.dat
ImageSectionObject      0x85188a80      cmd.exe file.0x85188a80.0x851a73f0.ImageSectionObject.cmd.exe.img
ImageSectionObject      0x84eb5ec8      winbrand.dll    file.0x84eb5ec8.0x84eb5da0.ImageSectionObject.winbrand.dll.img
ImageSectionObject      0x84deca60      apphelp.dll     file.0x84deca60.0x84dee5e8.ImageSectionObject.apphelp.dll.img
ImageSectionObject      0x844227b8      ntdll.dll       file.0x844227b8.0x84374a38.ImageSectionObject.ntdll.dll.img
ImageSectionObject      0x84d0ed68      user32.dll      file.0x84d0ed68.0x84d0ea58.ImageSectionObject.user32.dll.img
ImageSectionObject      0x8438b928      msvcrt.dll      file.0x8438b928.0x84385798.ImageSectionObject.msvcrt.dll.img
ImageSectionObject      0x8438a7e8      lpk.dll file.0x8438a7e8.0x84385da0.ImageSectionObject.lpk.dll.img
ImageSectionObject      0x84d1dca0      imm32.dll       file.0x84d1dca0.0x84383360.ImageSectionObject.imm32.dll.img
ImageSectionObject      0x84d23c80      msctf.dll       file.0x84d23c80.0x84d22700.ImageSectionObject.msctf.dll.img
ImageSectionObject      0x845af548      kernel32.dll    file.0x845af548.0x843e4c58.ImageSectionObject.kernel32.dll.img
ImageSectionObject      0x83d094a8      gdi32.dll       file.0x83d094a8.0x83d8c0e0.ImageSectionObject.gdi32.dll.img
ImageSectionObject      0x8454f0a0      apisetschema.dll        file.0x8454f0a0.0x84563d38.ImageSectionObject.apisetschema.dll.img
ImageSectionObject      0x845f74e8      usp10.dll       file.0x845f74e8.0x845f5378.ImageSectionObject.usp10.dll.img
```

Con esto veremos que en la `v3` sera con este comando, el cual nos habra volcado la informacion de dicho proceso a la carpeta `dumps`.

En la parte de `v2` podremos investigar el archivo dumpeado de esta forma:

```shell
strings 2096.dmp | less
```

Y en la parte de `v3` sera de la misma forma pero con los archivos separados uno por uno.

```shell
strings file.0x851ac410.0x851a9518.DataSectionObject.cmd.exe.mui.dat | less
```

Y ya con esto ir viendo irregularidades dentro del proceso dumpeado.

### Obtener información de los hashes de los usuarios logueados/registrados en el sistema

Con el parametro `hashdump` podremos obtener un listado de `hashes NTLM` de los usuarios que estan registrados o logueados en el sistema, esto en tal caso de que la imagen del `dump` tuviera estos `hashes` inyectados, si no, no veremos nada.

Pero para comprobar que nos va a funcionar el `hashdump` podremos hacer un `hivelist` para ver todos los registros que tenemos disponibles en nuestro `dump`, si aparece el `SAM` sabremos que si podremos obtener dichos `hashes`.

#### Volatility2

```shell
./vol.py -f Challenge.raw --profile=Win7SP1x86_23418 hivelist
```

Info:

```
Virtual    Physical   Name
---------- ---------- ----
0x8780a6a8 0x251a16a8 [no name]
0x87818218 0x251e7218 \REGISTRY\MACHINE\SYSTEM
0x87838008 0x250c7008 \REGISTRY\MACHINE\HARDWARE
0x878c23b0 0x1fc543b0 \SystemRoot\System32\Config\DEFAULT
0x88575460 0x18cc1460 \SystemRoot\System32\Config\SECURITY
0x885cb3d8 0x183063d8 \SystemRoot\System32\Config\SAM
0x8f4ef008 0x20d43008 \Device\HarddiskVolume1\Boot\BCD
0x8f589510 0x20d9e510 \SystemRoot\System32\Config\SOFTWARE
0x9140b9c8 0x180ae9c8 \??\C:\Windows\ServiceProfiles\NetworkService\NTUSER.DAT
0x914619c8 0x184a79c8 \??\C:\Windows\ServiceProfiles\LocalService\NTUSER.DAT
0x9687a198 0x0d4af198 \??\C:\Users\hello\ntuser.dat
0x96923648 0x0d44d648 \??\C:\Users\hello\AppData\Local\Microsoft\Windows\UsrClass.dat
```

Por lo que vemos en este caso si tenemos el `SAM` por lo que podremos obtener los `hashes` de los usuarios.

```shell
./vol.py -f Challenge.raw --profile=Win7SP1x86_23418 hashdump
```

En este caso nos da un error, por que a lo mejor no es compatible, pero con ese comando tiene que funcionar.

#### Instalar snap volatility2

Pero si lo instalamos desde `snap` en `Kali Linux`.

```shell
snap install volatility-phocean
```

El `dump` lo tenemos que copiar a nuestra carpeta `/home` ya que `snap` no puede acceder a ningun sitio extra de nuestra carpeta `/home`.

```shell
cp /<PATH>/Challenge.raw ~/
```

Ahora vamos a ejecutar la herramienta de esta forma:

```shell
/snap/bin/volatility -f ~/Challenge.raw --profile=Win7SP1x86_23418 hashdump
```

Info:

```
Volatility Foundation Volatility Framework 2.6.1
Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
hello:1000:aad3b435b51404eeaad3b435b51404ee:101da33f44e92c27835e64322d72e8b7:::
```

Con esto veremos que ha funcionado de forma correcta.

#### Volatility3

```shell
./vol.py -f Challenge.raw windows.registry.hivelist
```

Info:

```
Volatility 3 Framework 2.26.2
Progress:  100.00               PDB scanning finished                        
Offset  FileFullPath    File output

0x8780a6a8              Disabled
0x87818218      \REGISTRY\MACHINE\SYSTEM        Disabled
0x87838008      \REGISTRY\MACHINE\HARDWARE      Disabled
0x878c23b0      \SystemRoot\System32\Config\DEFAULT     Disabled
0x88575460      \SystemRoot\System32\Config\SECURITY    Disabled
0x885cb3d8      \SystemRoot\System32\Config\SAM Disabled
0x8f4ef008      \Device\HarddiskVolume1\Boot\BCD        Disabled
0x8f589510      \SystemRoot\System32\Config\SOFTWARE    Disabled
0x9140b9c8      \??\C:\Windows\ServiceProfiles\NetworkService\NTUSER.DAT        Disabled
0x914619c8      \??\C:\Windows\ServiceProfiles\LocalService\NTUSER.DAT  Disabled
0x9687a198      \??\C:\Users\hello\ntuser.dat   Disabled
0x96923648      \??\C:\Users\hello\AppData\Local\Microsoft\Windows\UsrClass.dat Disabled
```

Ahora para obtener el `SAM` haremos lo siguiente:

```shell
./vol.py -f Challenge.raw windows.hashdump.Hashdump
```

En este caso tambien nos dara un error, por que a lo mejor es incompatible la memoria dumpeada o cualquier otro factor, pero con eso deberia de funcionar, tambien tenemos este otro:

```shell
./vol.py -f Challenge.raw windows.lsadump.Lsadump
```

En este caso es para el `LSA`.

## Resolver el Lab 0

Siguiendo todo lo que tenemos descubierto, ya dijimos que el proceso de `demon.py.txt` era bastante sospechoso, si realizamos de nuevo el parametro `consoles` para ver lo que nos muestra, veremos esta linea interesante.

```
C:\Users\hello>C:\Python27\python.exe C:\Users\hello\Desktop\demon.py.txt       
335d366f5d6031767631707f
```

Estamos viendo este numero codificado:

```
335d366f5d6031767631707f
```

Esto esta en `Hexadecimal` si lo intentamos decodificar veremos esto:

```
3]6o]`1vv1p
```

Veremos esto tan raro, por lo que ya dudamos en que pueda ser ese tipo de decodificacion, vamos a investigar un poco mas en las variables de entorno.

```shell
./vol.py -f Challenge.raw windows.envars
```

Info:

```
Volatility 3 Framework 2.26.2
Progress:  100.00               PDB scanning finished                        
PID     Process Block   Variable        Value

260     smss.exe        0x1708c0        Path    C:\Windows\System32
260     smss.exe        0x1708c0        SystemDrive     C:
260     smss.exe        0x1708c0        SystemRoot      C:\Windows
340     csrss.exe       0x380db0        ComSpec C:\Windows\system32\cmd.exe
340     csrss.exe       0x380db0        FP_NO_HOST_CHECK        NO
340     csrss.exe       0x380db0        NUMBER_OF_PROCESSORS    1
340     csrss.exe       0x380db0        OS      Windows_NT
340     csrss.exe       0x380db0        Path    C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShell\v1.0\
340     csrss.exe       0x380db0        PATHEXT .COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC
340     csrss.exe       0x380db0        PROCESSOR_ARCHITECTURE  x86
340     csrss.exe       0x380db0        PROCESSOR_IDENTIFIER    x86 Family 6 Model 142 Stepping 9, GenuineIntel
340     csrss.exe       0x380db0        PROCESSOR_LEVEL 6
340     csrss.exe       0x380db0        PROCESSOR_REVISION      8e09
340     csrss.exe       0x380db0        PSModulePath    C:\Windows\system32\WindowsPowerShell\v1.0\Modules\
340     csrss.exe       0x380db0        SystemDrive     C:
340     csrss.exe       0x380db0        SystemRoot      C:\Windows
340     csrss.exe       0x380db0        TEMP    C:\Windows\TEMP
340     csrss.exe       0x380db0        Thanos  xor and password
340     csrss.exe       0x380db0        TMP     C:\Windows\TEMP
340     csrss.exe       0x380db0        USERNAME        SYSTEM
340     csrss.exe       0x380db0        windir  C:\Windows
340     csrss.exe       0x380db0        windows_tracing_flags   3
340     csrss.exe       0x380db0        windows_tracing_logfile C:\BVTBin\Tests\installpackage\csilogfile.log
380     csrss.exe       0x230db0        ComSpec C:\Windows\system32\cmd.exe
380     csrss.exe       0x230db0        FP_NO_HOST_CHECK        NO
380     csrss.exe       0x230db0        NUMBER_OF_PROCESSORS    1
380     csrss.exe       0x230db0        OS      Windows_NT
380     csrss.exe       0x230db0        Path    C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShell\v1.0\
380     csrss.exe       0x230db0        PATHEXT .COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC
380     csrss.exe       0x230db0        PROCESSOR_ARCHITECTURE  x86
380     csrss.exe       0x230db0        PROCESSOR_IDENTIFIER    x86 Family 6 Model 142 Stepping 9, GenuineIntel
380     csrss.exe       0x230db0        PROCESSOR_LEVEL 6
380     csrss.exe       0x230db0        PROCESSOR_REVISION      8e09
380     csrss.exe       0x230db0        PSModulePath    C:\Windows\system32\WindowsPowerShell\v1.0\Modules\
380     csrss.exe       0x230db0        SystemDrive     C:
380     csrss.exe       0x230db0        SystemRoot      C:\Windows
380     csrss.exe       0x230db0        TEMP    C:\Windows\TEMP
380     csrss.exe       0x230db0        Thanos  xor and password
380     csrss.exe       0x230db0        TMP     C:\Windows\TEMP
380     csrss.exe       0x230db0        USERNAME        SYSTEM
380     csrss.exe       0x230db0        windir  C:\Windows
380     csrss.exe       0x230db0        windows_tracing_flags   3
380     csrss.exe       0x230db0        windows_tracing_logfile C:\BVTBin\Tests\installpackage\csilogfile.log
...............................<RESTO_DE_LOGS>.....................................
```

Si vemos en esos primeros procesos nos viene uno bastante raro llamado `Thanos` como variable de entorno y que contiene lo siguiente:

```
340     csrss.exe       0x380db0        Thanos  xor and password
```

Vemos que esta mencionando la codificacion de `XOR` por lo que vamos a probar a decodificar el numero de antes en `XOR`, a ver que vemos.

Vamos a montarnos un script.

> decode\_XOR.py

```python
# Hexadecimal a texto y prueba todas las claves XOR posibles

# Hex string
hex_data = "335d366f5d6031767631707f"

# Convertir de hex a bytes
decoded_bytes = bytes.fromhex(hex_data)
print("[*] Texto decodificado del hex (sin XOR):")
print(decoded_bytes.decode(errors="ignore"))
print("\n[*] Probando todas las claves XOR posibles:\n")

# Probar todas las claves XOR (0-255)
for key in range(256):
    xor_decoded = bytes([b ^ key for b in decoded_bytes])
    try:
        # Intentar decodificar como texto legible
        text = xor_decoded.decode("utf-8")
    except UnicodeDecodeError:
        # Ignorar claves que no producen texto legible
        continue
    print(f"Clave XOR {key:02x}: {text}")
```

Hay que probar las `255` posibilidades de resultados y quedarnos con la que tenga un texto aparentemente normal.

```shell
python3 decode_XOR.py
```

Info:

```
[*] Texto decodificado del hex (sin XOR):
3]6o]`1vv1p

[*] Probando todas las claves XOR posibles:

Clave XOR 00: 3]6o]`1vv1p
Clave XOR 01: 2\7n\a0ww0q~
Clave XOR 02: 1_4m_b3tt3r}
Clave XOR 03: 0^5l^c2uu2s|
Clave XOR 04: 7Y2kYd5rr5t{
Clave XOR 05: 6X3jXe4ss4uz
Clave XOR 06: 5[0i[f7pp7vy
Clave XOR 07: 4Z1hZg6qq6wx
Clave XOR 08: ;U>gUh9~~9xw
Clave XOR 09: :T?fTi88yv
Clave XOR 0a: 9W<eWj;||;zu
Clave XOR 0b: 8V=dVk:}}:{t
Clave XOR 0c: ?Q:cQl=zz=|s
Clave XOR 0d: >P;bPm<{{<}r
Clave XOR 0e: =S8aSn?xx?~q
Clave XOR 0f: <R9`Ro>yy>p
Clave XOR 10: #M&Mp!ff!`o
Clave XOR 11: "L'~Lq gg an
Clave XOR 12: !O$}Or#dd#bm
Clave XOR 13:  N%|Ns"ee"cl
Clave XOR 14: 'I"{It%bb%dk
Clave XOR 15: &H#zHu$cc$ej
Clave XOR 16: %K yKv'``'fi
Clave XOR 17: $J!xJw&aa&gh
Clave XOR 18: +E.wEx)nn)hg
Clave XOR 19: *D/vDy(oo(if
Clave XOR 1a: )G,uGz+ll+je
Clave XOR 1b: (F-tF{*mm*kd
Clave XOR 1c: /A*sA|-jj-lc
Clave XOR 1d: .@+r@},kk,mb
Clave XOR 1e: -C(qC~/hh/na
Clave XOR 1f: ,B)pB.ii.o`
................................<RESTO_DE_CODIGO>..................................
```

Vemos que la mas clara es esta linea de aqui:

```
Clave XOR 02: 1_4m_b3tt3r}
```

Pertenece al final de una `flag`, tendremos que obtener la primera parte que es lo que falta, por lo que vamos a obtener los `hashes` de los usuarios, a ver si esta por ahi lo que falta de forma codificada.

Si hacemos como antes para dumpearnos todos los `hashes` `NTLM` de esta forma:

```shell
/snap/bin/volatility -f ~/Challenge.raw --profile=Win7SP1x86_23418 hashdump
```

Info:

```
Volatility Foundation Volatility Framework 2.6.1
Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
hello:1000:aad3b435b51404eeaad3b435b51404ee:101da33f44e92c27835e64322d72e8b7:::
```

Veremos que hay un usuario que no viene por defecto llamado `hello`, vamos a intentar `crackear` dicha contraseña con el `hash NTLM`.

URL = [Crack Hash Page](https://hashes.com/en/decrypt/hash)

Si metemos simplemente el `NT` para ver que encuentra, veremos lo siguiente:

```
flag{you_are_good_but
```

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-07-13 163247.png" alt=""><figcaption></figcaption></figure>

Ahora si juntamos las `2` partes que tenemos para formar la `flag` nos quedara asi:

```
flag{you_are_good_but1_4m_b3tt3r}
```

Con esto ya habremos obtenido bien toda la informacion.
