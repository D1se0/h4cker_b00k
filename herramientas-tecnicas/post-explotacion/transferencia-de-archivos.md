---
icon: download
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

# Transferencia de archivos

## Verificación de integridad

{% tabs %}
{% tab title="Linux" %}
```bash
md5sum <file>
```
{% endtab %}

{% tab title="Windows" %}
```powershell
certutil -hashfile <file> md5
```
{% endtab %}
{% endtabs %}

## HTTP

### HTTP Server

{% tabs %}
{% tab title="Python3" %}
```bash
python3 -m http.server <port>
```
{% endtab %}

{% tab title="Python2" %}
```bash
python2 -m SimpleHTTPServer <port>
```
{% endtab %}

{% tab title="PHP" %}
```bash
php -S 0:<port>
```
{% endtab %}
{% endtabs %}

## Download

{% tabs %}
{% tab title="Wget" %}
```bash
wget <url>
```
{% endtab %}

{% tab title="Curl" %}
```bash
curl -s <url> -o <out_file>
```
{% endtab %}

{% tab title="PowerShell" %}
```powershell
(New-Object Net.WebClient).DownloadString('<url>') > <out_file>
```

```powershell
Invoke-WebRequest <url> -o <out_file>
```
{% endtab %}

{% tab title="CMD" %}
```cmd
certutil -urlcache -split -f <url> <out_file>
```
{% endtab %}
{% endtabs %}

## SMB

### SMB Server

```bash
smbserver.py <share_name> <share_path> -smb2support [-username <out_file> -password <out_file>]
```

### Download

{% tabs %}
{% tab title="Linux" %}
```bash
smbclient -U '<user>[%<password>]' //<ip>/<share> -c "get <src_file> <out_file>"
```
{% endtab %}

{% tab title="Windows" %}
```powershell
# mount smb Share to drive
net use z: \\<ip>\<share> [/user:$USERNAME $PASSWORD]
# copy from share
copy \\<ip>\<share>\<src_file> <out_file>
```
{% endtab %}
{% endtabs %}

## Netcat

{% tabs %}
{% tab title="Send" %}
```bash
nc -nlvp <port> < <src_file>
```
{% endtab %}

{% tab title="Recieve" %}
```bash
nc <ip> <port> > <out_file>
```
{% endtab %}
{% endtabs %}

## Bash

{% tabs %}
{% tab title="Send" %}
```bash
cat <src_file> > /dev/tcp/<ip>/<port>
```
{% endtab %}

{% tab title="Recieve" %}
```bash
cat < /dev/tcp/<ip>/<port> > <out_file>
```
{% endtab %}
{% endtabs %}
