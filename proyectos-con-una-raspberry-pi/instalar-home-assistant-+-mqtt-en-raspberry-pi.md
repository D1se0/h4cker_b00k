---
icon: house-signal
---

# Instalar Home Assistant + MQTT en Raspberry Pi

## Introducción

**Home Assistant es el cerebro central de tu casa inteligente.** Es un software de código abierto que instalas en tu Raspberry Pi para controlar y automatizar todos los dispositivos conectados de tu hogar desde una sola interfaz. En lugar de tener 10 apps diferentes para luces, enchufes, cámaras y sensores, todo se centraliza aquí.

**Con esta instalación básica** tendrás la plataforma funcionando en tu red local, donde podrás añadir dispositivos WiFi como bombillas o enchufes inteligentes, crear automatizaciones simples (como que las luces se enciendan al anochecer) y controlar todo desde tu móvil o tablet. El MQTT es el "idioma" que usarán algunos dispositivos más avanzados para comunicarse entre sí.

**Lo especial** es que todo funciona localmente en tu casa, sin depender de servidores en la nube, manteniendo tu privacidad y funcionando aunque internet falle. Es el comienzo para transformar tu hogar en uno inteligente, donde las cosas suceden automáticamente según tus rutinas y preferencias.

## **Crear directorios**

```bash
# Solo estos dos directorios:
mkdir /home/pi/homeassistant
mkdir /home/pi/mosquitto
```

## **Configurar en Portainer**

1. **Abre Portainer** en tu navegador
2. Ve a **Stacks** (izquierda)
3. Haz clic en **"+ Add stack"**
4. **Nombre:** `home-assistant-mqtt`
5. **Editor:** Pega EXACTAMENTE esto:

```yaml
version: "3"
services:
  homeassistant:
    image: ghcr.io/home-assistant/raspberrypi4-64-homeassistant:stable
    container_name: homeassistant
    network_mode: host
    restart: unless-stopped
    volumes:
      - /home/pi/homeassistant:/config
    environment:
      - TZ=Europe/Madrid

  mosquitto:
    image: eclipse-mosquitto
    container_name: mosquitto
    network_mode: host
    restart: unless-stopped
    volumes:
      - /home/pi/mosquitto:/mosquitto/data
```

6. **Haz clic en:** `Deploy the stack`

**Esperar un poco...**

* **Primera vez:** 5-10 minutos
* Verás los containers en **Containers** de Portainer
* Estado debe ser **Running**

## **Acceder**

1. Abre navegador
2. Ve a: `http://TU-IP-RASPBERRY:8123`\
   (la misma IP que usas para Portainer)
3. **Espera** hasta que cargue la pantalla de configuración inicial

## **Configuración inicial Home Assistant**

1. **Crea usuario** (el que quieras)
2. **Nombre de tu casa** (opcional)
3. **Ubicación** (importante para hora/sol)
4. **Compartir datos** (recomiendo NO compartir)
5. **Finalizar**

## **Configurar MQTT en Home Assistant**

### **Añadir integración MQTT**

1. En Home Assistant, ve a **Configuración**
2. **Dispositivos y servicios**
3. **"+ Añadir integración"**
4. Busca **"MQTT"**
5. **Broker:** `localhost`
6. **Puerto:** `1883`
7. **Usuario/Contraseña:** Déjalo en blanco (está en anónimo)
8. **Añadir**

## **VERIFICACIÓN**

### **Comprueba que todo funciona:**

1. **Home Assistant:** `http://TU-IP:8123` → Debe cargar
2. **MQTT:** (Opcional) Instala app MQTT Explorer en móvil
   * Servidor: `TU-IP`
   * Puerto: `1883`
   * Debe conectar

## **SI HAY PROBLEMAS:**

### Home Assistant no carga

```bash
# Revisa logs en Portainer:
# 1. Ve a Containers
# 2. Busca "homeassistant"
# 3. Haz clic en "Logs"
```

### MQTT no conecta

```yaml
# Cambia el stack a esto (añade configuración mosquitto):
services:
  # ... homeassistant igual ...
  
  mosquitto:
    image: eclipse-mosquitto
    container_name: mosquitto
    network_mode: host
    restart: unless-stopped
    volumes:
      - /home/pi/mosquitto:/mosquitto/data
      - /home/pi/mosquitto.conf:/mosquitto/config/mosquitto.conf
```

Crea el archivo `/home/pi/mosquitto.conf`:

```conf
listener 1883
allow_anonymous true
```

## **DISPOSITIVOS PARA EMPEZAR**

### **WiFi (fáciles):**

1. **Enchufes:** TP-Link Kasa (baratos)
2. **Bombillas:** Philips Wiz o similares
3. **Sensores:** Shelly (para persianas, luces)

### **Configuración rápida:**

1. Conecta dispositivo a tu WiFi
2. En Home Assistant: **Configuración → Dispositivos**
3. **"+ Añadir dispositivo"**
4. Debe aparecer automáticamente

## **NO TOCAR:**

* **NO** modifiques `docker-compose.yml` manualmente
* **NO** añadas `privileged: true` a menos que sea necesario
* **NO** cambies puertos (deja 8123 y 1883)
* **NO** toques la configuración de OpenMediaVault

## **BACKUP SIMPLE:**

```bash
# Copia manual cuando quieras:
cp -r /home/pi/homeassistant /home/pi/homeassistant_backup_$(date +%Y%m%d)
```

## **SI SE BLOQUEA:**

1. En Portainer → Containers
2. Selecciona "homeassistant"
3. **"Recreate"** (mantiene los datos)
4. O **"Restart"**

## **RESUMEN RÁPIDO:**

1. **`mkdir /home/pi/{homeassistant,mosquitto}`**
2. **Portainer → Stacks → Add stack**
3. **Pegar YAML**
4. **`Deploy the stack`**
5. **Esperar 5-10 min**
6. **`http://TU-IP:8123`**
7. **Configurar usuario**
8. **Añadir integración MQTT**
