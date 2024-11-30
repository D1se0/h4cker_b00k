# Spidering y Crawling con Burp Suite y skipfish

Si nos vamos en la pestaña de `targets` -> `Site map` -> Aqui podremos ver nuestra IP y si desplegamos veremos una carpeta de la pagina `mutillidae` y si volvemos a desplegar, veremos varios archivos los cuales conforman la pagina web, entre ellos un `index.php` pero si desplegamos ese podremos ver todas las paginas que nos ha descubierto `Burp Suite` y las que estan en gris claro significa que no las hemos visitado y las que estan en negrita significa que si las hemos visitado:

<figure><img src="../../../.gitbook/assets/image (56).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../../.gitbook/assets/image (57).png" alt=""><figcaption></figcaption></figure>

Esta herramienta consigue descubrir todo esto mediante el analisis del codigo fuente que recive del servidor, cuando recive esa peticion desde el servidor con la pagina web parsea la peticion coge todos los enlaces que puedan hacer referencia a otros apartados dentro de esa aplicacion web y te los muestra ahi.

Todo este proceso de reconocimiento (`Pasivo`) se le denomina `Spidering` o `Crawling`.

Todas las peticiones que hagamos estando en la misma escucha que `Burp Suite` pero no hace falta que este en `On` las ira almacenando en `targets`, por ejemplo si nos logeamos en alguna pagina, ese login o esa peticion la guardara la herramienta.

Si queremos hacer `Spidering Activo` con las antiguas versiones de `Burp Suite` en la version gratuita estaba implementado, pero ahora es de pago, por lo que podremos hacerlo con otra herramienta llamada `skipfish`.

`Skipfish` es una herramienta que viene por defecto en `kali`, para hacer este tipo de escaneo haremos lo siguiente:

```shell
mkdir skipfish_results
skipfish -YO -o skipfish_results http://192.168.5.177/mutillidae/src/index.php
```

Con el parametro `-YO` lo que estamos haciendo es que nuestro escaneo no sea tan intrusivo, haciendo un poco de `fuzzing` en directorios, para ir descubriendo informacion.

Una vez ejecutado esto, pulsaremos `ENTER` y estara en proceso la herramienta de escaneo activo sobre la URL indicada.

Esta tecnica (`Spidering o Crawling`) de escaneo deberia de ser la primera que deberemos de realizar para juntar toda la informacion posible sobre la pagina web y posteriormente analizar dicha informacion para una posible explotacion.

Podremos dejarlo un rato, por que depende de las paginas puede durar mucho este escaneo, por lo que cuando queramos le podemos dar a `Ctrl+C` y parar el escaneo:

```
skipfish version 2.10b by lcamtuf@google.com

  - 192.168.5.177 -

Scan statistics:

      Scan time : 0:04:24.225
  HTTP requests : 15437 (58.8/s), 10586 kB in, 4067 kB out (55.5 kB/s)   
    Compression : 3849 kB in, 14476 kB out (58.0% gain)    
    HTTP faults : 0 net errors, 0 proto errors, 0 retried, 0 drops
 TCP handshakes : 200 total (80.7 req/conn)  
     TCP faults : 0 failures, 0 timeouts, 1 purged
 External links : 549 skipped
   Reqs pending : 709         

Database statistics:

         Pivots : 150 total, 43 done (28.67%)    
    In progress : 74 pending, 13 init, 9 attacks, 11 dict     
  Missing nodes : 4 spotted
     Node types : 1 serv, 41 dir, 12 file, 21 pinfo, 52 unkn, 23 par, 0 val
   Issues found : 62 info, 3 warn, 6 low, 11 medium, 0 high impact
      Dict size : 195 words (195 new), 12 extensions, 256 candidates
     Signatures : 77 total
        
[!] Scan aborted by user, bailing out!
[+] Copying static resources...
[+] Sorting and annotating crawl nodes: 150
[+] Looking for duplicate entries: 150
[+] Counting unique nodes: 135
[+] Saving pivot data for third-party tools...
[+] Writing scan description...
[+] Writing crawl tree: 150
[+] Generating summary views...
[+] Report saved to 'skipfish_results/index.html' [0x6362bab1].
[+] This was a great day for science!
```

Lo que mola de esta herramienta es que la visualizacion de los resultados es bastante chula, por lo que si nos vamos a la carpeta que creamos donde se volcaron todos estos resultados en mi caso `skipfish_results` dentro de la misma habran varios archivos, pero el que nos interesa abrir es el llamado `index.html`.

```shell
open index.html
```

<figure><img src="../../../.gitbook/assets/image (58).png" alt=""><figcaption></figcaption></figure>

Veremos una interfaz bastante bonita y visual a la hora de poder analizar los datos.
