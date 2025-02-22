---
icon: rectangle-ad
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

# Vulnerable AD

Aqui vamos a ver como enumerar `ACLs` vulnerables, rutas de `ACLs` vulnerables, etc.. Y despues como explotarlas todas ellas.

Pero antes de ver todo esto, tendremos que preparar nuestro entorno de forma mas realista y hacer algunas configuraciones para que se pueda ver todo esto, para ello nos iremos a un repositorio de `GitHub`:

URL = [GitHub Vulnerable AD](https://github.com/safebuffer/vulnerable-AD)

Lo que va hacer este script es aumentar mucho los objetos de nuestro dominio, por ejemplo podremos crear los usuarios que queramos en este caso creara hasta 100 usuarios, nos va a crear tambien un monton de grupos, nuevas `ACLs` que van a relacionar unos grupos con otros, usuarios con grupos, grupos con usuarios y a demas nos va aplicar ciertos parametros de configuracion para soportar los siguientes ataques:

```
- Abusing ACLs/ACEs
- Kerberoasting
- AS-REP Roasting
- Abuse DnsAdmins
- Password in Object Description
- User Objects With Default password (Changeme123!)
- Password Spraying
- DCSync
- Silver Ticket
- Golden Ticket
- Pass-the-Hash
- Pass-the-Ticket
- SMB Signing Disabled
```

Basicamente esto lo que hara sera crear un entorno mas realista de nuestro `AD` pero tambien con configuraciones y permisos vulnerables para que nosotros podamos practicar todo este tipo de cosas.

Para poder hacer todo esto tendremos que descargarnos el script que esta en el repositorio llamado `vulnad.ps1` y pasarnoslo a nuestro equipo `DC`.

Una vez que ya este en nuestro escritorio, tendremos que editar el script para eliminar una cosita que nos recomienda el propietario del script y es la siguiente:

Para que no nos de problemas el script eliminaremos esta funcion:

```powershell
function ShowBanner {
    $banner  = @()
    $banner+= $Global:Spacing + ''
    $banner+= $Global:Spacing + 'VULN AD - Vulnerable Active Directory'
    $banner+= $Global:Spacing + ''                                                  
    $banner+= $Global:Spacing + 'By wazehell @safe_buffer'
    $banner | foreach-object {
        Write-Host $_ -ForegroundColor (Get-Random -Input @('Green','Cyan','Yellow','gray','white'))
    }                             
}

# Un poquito mas abajo eliminaremos donde se invoca el banner

ShowBanner
```

Que es para mostrar el banner del script y lo guardaremos.

Tambien vamos a eliminar el grupo que creamos anteriormente llamado `Executives` y el usuarios `empleado4` por si tuviera alguna colision con el script.

Nos vamos a `Administrador del servidor` -> `Herramientas` -> `Usuarios y equipos de Active Directory` -> `Users` -> click derecho en `Executives` -> `Eliminar` -> click derecho a `empleado4` -> `Eliminar`.

Una vez echo estas modificaciones, abriremos una consola de `PowerShell` y ejecutaremos el script.

```powershell
cd .\Desktop
. .\vulnad.ps1
```

Y con esto ya lo tendriamos cargado en `Windows` por lo que tendremos que invocar lo siguiente con el siguiente comando:

```powershell
Invoke-VulnAD -UsersLimit 100 -DomainName "corp.local"
```

Info:

```
[*] Creating maurine.bibby User
        [*] Creating henrie.kaleena User
        [*] Creating ali.alix User
        [*] Creating saree.dayna User
        [*] Creating lonnie.betti User
        [*] Creating abbi.jocelyn User
        [*] Creating arlie.gunilla User
        [*] Creating adorne.bridgette User
        [*] Creating roanna.bidget User
        [*] Creating aubry.carolan User
        [*] Creating ermina.hatti User
        [*] Creating angelika.shelly User
        [*] Creating barby.min User
        [*] Creating jannel.emalia User
        [*] Creating audre.maible User
        [*] Creating kizzie.kacy User
        [*] Creating andreana.shea User
        [*] Creating emeline.shirline User
        [*] Creating brynne.kenon User
        [*] Creating myrtia.agatha User
        [*] Creating ernaline.lowell User
        [*] Creating gerri.kathi User
        [*] Creating goldarina.nicki User
        [*] Creating avril.cheri User
        [*] Creating bobette.glenn User
        [*] Creating joanie.karine User
        [*] Creating gwenneth.gilly User
        [*] Creating saidee.kaye User
        [*] Creating cynthie.rori User
        [*] Creating cristabel.melony User
        [*] Creating mela.jacquetta User
        [*] Creating jennifer.gerry User
        [*] Creating ginevra.michel User
        [*] Creating arabella.norry User
        [*] Creating colly.katey User
        [*] Creating marsha.jordan User
        [*] Creating britni.henrieta User
        [*] Creating alejandrina.faye User
        [*] Creating philis.bertha User
        [*] Creating harriett.daron User
        [*] Creating ardine.farra User
        [*] Creating robena.prudence User
        [*] Creating pearl.judye User
        [*] Creating riva.nellie User
        [*] Creating jobina.aleta User
        [*] Creating fayina.hyacinth User
        [*] Creating loretta.jerrine User
        [*] Creating peta.adelind User
        [*] Creating ophelie.odele User
        [*] Creating cybil.alica User
        [*] Creating shay.siana User
        [*] Creating halette.martelle User
        [*] Creating audrey.hedwiga User
        [*] Creating betsey.stephine User
        [*] Creating demetris.daveta User
        [*] Creating lexy.rosaline User
        [*] Creating ilyssa.nevsa User
        [*] Creating caprice.helen-elizabeth User
        [*] Creating denice.freda User
        [*] Creating georgia.marie-ann User
        [*] Creating benny.alikee User
        [*] Creating sandye.leodora User
        [*] Creating germain.gavrielle User
        [*] Creating milicent.gracie User
        [*] Creating meg.carolee User
        [*] Creating linn.evaleen User
        [*] Creating mirna.annice User
        [*] Creating diana.sharai User
        [*] Creating deeann.amalita User
        [*] Creating kettie.shanta User
        [*] Creating estelle.kelli User
        [*] Creating guenna.jessi User
        [*] Creating allissa.lezlie User
        [*] Creating crissie.deena User
        [*] Creating olga.rhoda User
        [*] Creating anna.costanza User
        [*] Creating corie.josie User
        [*] Creating evy.britta User
        [*] Creating jaime.luise User
        [*] Creating gennifer.cleo User
        [*] Creating colly.elfie User
        [*] Creating gill.kellie User
        [*] Creating carmon.leoine User
        [*] Creating farrand.inna User
        [*] Creating donnie.lari User
        [*] Creating millie.hanny User
        [*] Creating sarita.alisha User
        [*] Creating rycca.jacinta User
        [*] Creating levin.bab User
        [*] Creating celle.sherye User
        [*] Creating chloris.ilysa User
        [*] Creating kelley.happy User
        [*] Creating darsey.jasmine User
        [*] Creating ebba.nicoline User
        [*] Creating geneva.lorrin User
        [*] Creating joellyn.pippa User
        [*] Creating renelle.jacynth User
        [*] Creating sarah.rhoda User
        [*] Creating annice.mable User
        [*] Creating aimil.evangelia User
        [+] Users Created
        [*] Creating Office Admin Group
        [*] Adding anna.costanza to Office Admin
        [*] Adding peta.adelind to Office Admin
        [*] Adding halette.martelle to Office Admin
        [*] Creating IT Admins Group
        [*] Adding colly.katey to IT Admins
        [*] Adding jaime.luise to IT Admins
        [*] Adding gennifer.cleo to IT Admins
        [*] Adding jobina.aleta to IT Admins
        [*] Adding kelley.happy to IT Admins
        [*] Adding maurine.bibby to IT Admins
        [*] Creating Executives Group
        [*] Adding shay.siana to Executives
        [*] Adding carmon.leoine to Executives
        [*] Adding evy.britta to Executives
        [*] Adding cristabel.melony to Executives
        [+] Office Admin IT Admins Executives Groups Created
        [*] Creating Senior management Group
        [*] Adding celle.sherye to Senior management
        [*] Adding darsey.jasmine to Senior management
        [*] Adding kizzie.kacy to Senior management
        [*] Adding rycca.jacinta to Senior management
        [*] Adding caprice.helen-elizabeth to Senior management
        [*] Creating Project management Group
        [*] Adding joanie.karine to Project management
        [*] Adding avril.cheri to Project management
        [+] Senior management Project management Groups Created
        [*] Creating marketing Group
        [*] Adding sarita.alisha to marketing
        [*] Adding saidee.kaye to marketing
        [*] Adding guenna.jessi to marketing
        [*] Adding colly.katey to marketing
        [*] Adding gill.kellie to marketing
        [*] Adding avril.cheri to marketing
        [*] Adding fayina.hyacinth to marketing
        [*] Creating sales Group
        [*] Adding gwenneth.gilly to sales
        [*] Adding kettie.shanta to sales
        [*] Adding gennifer.cleo to sales
        [*] Creating accounting Group
        [*] Adding saidee.kaye to accounting
        [*] Adding cristabel.melony to accounting
        [*] Adding milicent.gracie to accounting
        [+] marketing sales accounting Groups Created
        [*] BadACL GenericAll sales to Senior management
        [*] BadACL GenericWrite marketing to Senior management
        [*] BadACL WriteOwner sales to Project management
        [*] BadACL WriteDACL marketing to Senior management
        [*] BadACL Self marketing to Project management
        [*] BadACL WriteProperty sales to Senior management
        [*] BadACL GenericAll Senior management to IT Admins
        [*] BadACL GenericWrite Senior management to Executives
        [*] BadACL WriteOwner Project management to IT Admins
        [*] BadACL WriteDACL Senior management to Executives
        [*] BadACL Self Senior management to Office Admin
        [*] BadACL WriteProperty Senior management to Executives
        [*] BadACL WriteOwner levin.bab and Senior management
        [*] BadACL WriteDACL georgia.marie-ann and sales
        [*] BadACL Self allissa.lezlie and Office Admin
        [*] BadACL GenericAll fayina.hyacinth and marketing
        [*] BadACL WriteOwner geneva.lorrin and Project management
        [+] BadACL Done
        [*] Kerberoasting exchange_svc exserver


DistinguishedName : CN=exchange_svc,CN=Managed Service Accounts,DC=corp,DC=local
Enabled           : True
Name              : exchange_svc
ObjectClass       : msDS-ManagedServiceAccount
ObjectGUID        : a165ddc2-0ee8-4df4-8784-d1bca6fbc66c
SamAccountName    : exchange_svc$
SID               : S-1-5-21-3352250647-938130414-2449934813-1219
UserPrincipalName :

        [*] Creating mssql_svc services account
DistinguishedName : CN=mssql_svc,CN=Managed Service Accounts,DC=corp,DC=local
Enabled           : True
Name              : mssql_svc
ObjectClass       : msDS-ManagedServiceAccount
ObjectGUID        : fcf50a4d-d32b-4f9c-ac80-b61da9de9d20
SamAccountName    : mssql_svc$
SID               : S-1-5-21-3352250647-938130414-2449934813-1220
UserPrincipalName :

        [*] Creating http_svc services account
DistinguishedName : CN=http_svc,CN=Managed Service Accounts,DC=corp,DC=local
Enabled           : True
Name              : http_svc
ObjectClass       : msDS-ManagedServiceAccount
ObjectGUID        : 6ec1efb5-4619-41b4-8940-aa8f8a1bdc38
SamAccountName    : http_svc$
SID               : S-1-5-21-3352250647-938130414-2449934813-1221
UserPrincipalName :

        [+] Kerberoasting Done
        [*] AS-REPRoasting audre.maible
        [*] AS-REPRoasting marsha.jordan
        [*] AS-REPRoasting gerri.kathi
        [+] AS-REPRoasting Done
        [*] DnsAdmins : gill.kellie
        [*] DnsAdmins : ermina.hatti
        [*] DnsAdmins Nested Group : Senior management
        [+] DnsAdmins Done
        [+] Password In Object Description Done
        [*] Default Password : corie.josie
        [*] Default Password : celle.sherye
        [+] Default Password Done
        [*] Same Password (Password Spraying) : germain.gavrielle
        [*] Same Password (Password Spraying) : jennifer.gerry
        [*] Same Password (Password Spraying) : guenna.jessi
        [*] Same Password (Password Spraying) : adorne.bridgette
        [*] Same Password (Password Spraying) : aimil.evangelia
        [+] Password Spraying Done
        [*] Giving DCSync to : cynthie.rori
        [*] Giving DCSync to : angelika.shelly
        [*] Giving DCSync to : lonnie.betti
        [+] DCSync Done
        [+] SMB Signing Disabled
```

Y con esto ya nos habria creado todo correctamente.

Ahora para comprobar todo esto, nos iremos al `Administrador del servidor` -> `Herramientas` -> `Usuarios y equipos de Active Directory` -> `Users`.

Dentro de aqui tendremos que ver que todos los usuarios se han creado correctamente:

<figure><img src="../../.gitbook/assets/image (254).png" alt=""><figcaption></figcaption></figure>

Vamos hacer un cambio en el grupo llamado `IT Admins` -> click derecho -> `Propiedades` -> `Miembro de` -> y le vamos a poner en el grupo `Administradores`.

Haremos lo mismo con el grupo llamado `Office Admin`, pero en el grupo llamado `Administradores de empresa`.
