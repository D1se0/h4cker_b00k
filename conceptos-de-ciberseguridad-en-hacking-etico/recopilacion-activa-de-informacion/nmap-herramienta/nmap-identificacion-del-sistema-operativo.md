# Nmap (identificación del sistema operativo)

Si nosotros queremos explotar alguna vulnerabilidad, escalar privilegios, etc... Una de las cosas mas importantes es saber a que sistema operativo nos estamos enfrentando, de esta forma podemos utilizar una serie de tecnicas u otras, dependiendo del S.O.

```shell
sudo nmap -v -O 192.168.16.129
```

Info:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-11 04:41 EST
Initiating ARP Ping Scan at 04:41
Scanning 192.168.16.129 [1 port]
Completed ARP Ping Scan at 04:41, 0.03s elapsed (1 total hosts)
Initiating Parallel DNS resolution of 1 host. at 04:41
Completed Parallel DNS resolution of 1 host. at 04:41, 13.00s elapsed
Initiating SYN Stealth Scan at 04:41
Scanning 192.168.16.129 [1000 ports]
Discovered open port 80/tcp on 192.168.16.129
Discovered open port 445/tcp on 192.168.16.129
Discovered open port 22/tcp on 192.168.16.129
Discovered open port 21/tcp on 192.168.16.129
Discovered open port 3306/tcp on 192.168.16.129
Discovered open port 8080/tcp on 192.168.16.129
Discovered open port 631/tcp on 192.168.16.129
Completed SYN Stealth Scan at 04:41, 4.07s elapsed (1000 total ports)
Initiating OS detection (try #1) against 192.168.16.129
Retrying OS detection (try #2) against 192.168.16.129
Nmap scan report for 192.168.16.129
Host is up (0.00037s latency).
Not shown: 991 filtered tcp ports (no-response)
PORT     STATE  SERVICE
21/tcp   open   ftp
22/tcp   open   ssh
80/tcp   open   http
445/tcp  open   microsoft-ds
631/tcp  open   ipp
3000/tcp closed ppp
3306/tcp open   mysql
8080/tcp open   http-proxy
8181/tcp closed intermapper
MAC Address: 00:0C:29:29:E7:FF (VMware)
Aggressive OS guesses: Linux 3.2 - 4.9 (98%), Linux 3.10 - 4.11 (94%), Linux 3.13 (94%), Linux 3.13 - 3.16 (94%), OpenWrt Chaos Calmer 15.05 (Linux 3.18) or Designated Driver (Linux 4.1 or 4.4) (94%), Linux 4.10 (94%), Android 5.0 - 6.0.1 (Linux 3.4) (94%), Linux 3.10 (94%), Linux 3.2 - 3.10 (94%), Linux 3.2 - 3.16 (94%)
No exact OS matches for host (test conditions non-ideal).
Uptime guess: 0.055 days (since Mon Nov 11 03:22:55 2024)
Network Distance: 1 hop
TCP Sequence Prediction: Difficulty=260 (Good luck!)
IP ID Sequence Generation: All zeros

Read data files from: /usr/bin/../share/nmap
OS detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 20.81 seconds
           Raw packets sent: 2042 (93.156KB) | Rcvd: 36 (2.204KB)
```

Nos esta inidicando que esta maquina, tiene un sistema operativo `Linux`:

```
Aggressive OS guesses: Linux 3.2 - 4.9 (98%), etc...
```

Y con una de `windows` tambien funciona:

```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-11 04:44 EST
Initiating ARP Ping Scan at 04:44
Scanning 192.168.16.132 [1 port]
Completed ARP Ping Scan at 04:44, 0.05s elapsed (1 total hosts)
Initiating Parallel DNS resolution of 1 host. at 04:44
Completed Parallel DNS resolution of 1 host. at 04:44, 13.00s elapsed
Initiating SYN Stealth Scan at 04:44
Scanning 192.168.16.132 [1000 ports]
Discovered open port 8080/tcp on 192.168.16.132
Discovered open port 22/tcp on 192.168.16.132
Discovered open port 21/tcp on 192.168.16.132
Discovered open port 135/tcp on 192.168.16.132
Discovered open port 139/tcp on 192.168.16.132
Discovered open port 4848/tcp on 192.168.16.132
Discovered open port 49155/tcp on 192.168.16.132
Discovered open port 80/tcp on 192.168.16.132
Discovered open port 445/tcp on 192.168.16.132
Discovered open port 3389/tcp on 192.168.16.132
Discovered open port 8009/tcp on 192.168.16.132
Discovered open port 7676/tcp on 192.168.16.132
Discovered open port 49152/tcp on 192.168.16.132
Discovered open port 49157/tcp on 192.168.16.132
Discovered open port 8383/tcp on 192.168.16.132
Discovered open port 8181/tcp on 192.168.16.132
Discovered open port 49154/tcp on 192.168.16.132
Discovered open port 49156/tcp on 192.168.16.132
Discovered open port 9200/tcp on 192.168.16.132
Discovered open port 49153/tcp on 192.168.16.132
Completed SYN Stealth Scan at 04:44, 1.70s elapsed (1000 total ports)
Initiating OS detection (try #1) against 192.168.16.132
Nmap scan report for 192.168.16.132
Host is up (0.00079s latency).
Not shown: 980 closed tcp ports (reset)
PORT      STATE SERVICE
21/tcp    open  ftp
22/tcp    open  ssh
80/tcp    open  http
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
445/tcp   open  microsoft-ds
3389/tcp  open  ms-wbt-server
4848/tcp  open  appserv-http
7676/tcp  open  imqbrokerd
8009/tcp  open  ajp13
8080/tcp  open  http-proxy
8181/tcp  open  intermapper
8383/tcp  open  m2mservices
9200/tcp  open  wap-wsp
49152/tcp open  unknown
49153/tcp open  unknown
49154/tcp open  unknown
49155/tcp open  unknown
49156/tcp open  unknown
49157/tcp open  unknown
MAC Address: 00:0C:29:EC:1E:B9 (VMware)
Device type: general purpose
Running: Microsoft Windows 7|2008|8.1
OS CPE: cpe:/o:microsoft:windows_7::- cpe:/o:microsoft:windows_7::sp1 cpe:/o:microsoft:windows_server_2008::sp1 cpe:/o:microsoft:windows_server_2008:r2 cpe:/o:microsoft:windows_8 cpe:/o:microsoft:windows_8.1
OS details: Microsoft Windows 7 SP0 - SP1, Windows Server 2008 SP1, Windows Server 2008 R2, Windows 8, or Windows 8.1 Update 1
Uptime guess: 0.017 days (since Mon Nov 11 04:20:49 2024)
Network Distance: 1 hop
TCP Sequence Prediction: Difficulty=259 (Good luck!)
IP ID Sequence Generation: Incremental

Read data files from: /usr/bin/../share/nmap
OS detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 15.85 seconds
           Raw packets sent: 1177 (52.486KB) | Rcvd: 1017 (41.438KB)
```

En esta otra maquina nos detecta que es de `windows`.
