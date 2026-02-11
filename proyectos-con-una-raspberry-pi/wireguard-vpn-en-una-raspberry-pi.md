---
icon: reel
---

# WireGuard (VPN) en una Raspberry Pi

## Introducción

Vamos a configurar y crear una `VPN` en una `Raspberry Pi` y a demas vamos a utilizar `Duck DNS` para configurar un dominio de forma gratuita por si acaso nuestra publica es dinamica, el objetivo de este proyecto es poder conectarnos desde nuestro equipo mediante la `VPN` para establecer un tunel a nuestra red local de casa y poder utilizar contenido que tengamos alojado en dicha red en una `Raspberry Pi` por ejemplo.

En este caso lo haremos dentro de un `portainer` utilizando `docker`.

## Instalación/Configuración de WireGuard (VPN)

### Preparar DuckDNS

#### Crear cuenta en DuckDNS

1. Ve a [**https://www.duckdns.org/**](https://www.duckdns.org/)
2. Regístrate con Google/GitHub
3. Crea un subdominio (ej: `miDominio.duckdns.org`)
4. **Copia tu Token** (lo necesitarás después)

#### Anotar tus datos:

* **Subdominio**: `_______________.duckdns.org`
* **Token**: `__________________________________`

### Crear Stack de WireGuard + DuckDNS en Portainer

Anteriormente tendremos que tener instalador `Portainer` junto con las dependencias de `Docker`, ya tengo un documento explicando todo esto.

LINK DOCUMENTO

#### En Portainer ve a:

* **Stacks** → **Add Stack**
* **Name**: `wireguard-vpn`
* **Build Method**: Web editor

#### Pega esta configuración YAML:

```yaml
version: "3.8"

services:
  # Actualizador de IP dinámica
  duckdns:
    image: lscr.io/linuxserver/duckdns:latest
    container_name: duckdns
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Madrid
      - SUBDOMAINS=TU_SUBDOMINIO_AQUI # Reemplazar por subdominio personalizado
      - TOKEN=TU_TOKEN_AQUI # Reemplazar por TOKEN
    restart: unless-stopped

  # Servidor VPN
  wireguard:
    image: lscr.io/linuxserver/wireguard:latest
    container_name: wireguard
    cap_add:
      - NET_ADMIN
      - SYS_MODULE
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Madrid
      - SERVERURL=TU_SUBDOMINIO_AQUI.duckdns.org # Reemplazar por subdominio
      - SERVERPORT=51820
      - PEERS=pc,phone
      - PEERDNS=auto
      - INTERNAL_SUBNET=10.13.13.0
    volumes:
      - /home/pi/docker/wireguard/config:/config
      - /lib/modules:/lib/modules
    ports:
      - "51820:51820/udp"
    sysctls:
      - net.ipv4.conf.all.src_valid_mark=1
    restart: unless-stopped
    depends_on:
      - duckdns
```

### Configurar el Router

#### Abrir puerto UDP:

* **Puerto**: `51820`
* **Protocolo**: `UDP`
* **IP destino**: IP local de tu Raspberry Pi (Ejem. `192.168.1.160`)
* **Descripción**: `WireGuard_VPN`

#### Encontrar IP de tu Raspberry:

```shell
hostname -I
```

o

```shell
ping -4 raspberrypi.local
```

### Obtener Archivos de Configuración

Espera 2-3 minutos a que se creen los archivos

#### Buscar los archivos de cliente:

```bash
# Archivos para PC
ls -la /home/pi/docker/wireguard/config/peer_pc/

# Archivos para teléfono  
ls -la /home/pi/docker/wireguard/config/peer_telefono/
```

**Deberías ver:**

* `peer_pc.conf` → Configuración para Windows
* `peer_telefono.conf` → Configuración para móvil
* `peer_telefono.png` → QR code para móvil

### Configurar PC (Windows)

#### Instalar WireGuard:

* Descarga: [**Download WireGuard**](https://www.wireguard.com/install)
* Instala la aplicación

#### Configurar túnel:

1. Abre **WireGuard**
2. Clic en **"Add tunnel"** → **"Import tunnel from file"**
3. Selecciona: `/home/pi/docker/wireguard/config/peer_pc/peer_pc.conf`
4. Clic en **"Activate"**

#### Verificar conexión:

* Debe mostrar **"Active"** y tráfico
* Prueba acceder a: `http://192.168.1.___:8096` (Por ejemplo Jellyfin)

### Configurar Móvil (Android/iOS)

#### Instalar app WireGuard

* **Play Store** o **App Store** → "WireGuard"

#### Configurar con QR code:

1. Abre la app
2. Clic en **"+"** → **"Create from QR code"**
3. Escanea: `/home/pi/docker/wireguard/config/peer_telefono/peer_telefono.png`
4. **Activa** el túnel

#### Probar conexión:

* Abre navegador → `http://192.168.1.___:8096`
