---
icon: network-wired
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

# Configuración de VLANs en Switch (PuTTY)

### ¿Qué es una VLAN?

Una VLAN (Virtual Local Area Network) es una red lógica que agrupa un conjunto de dispositivos de red, independientemente de su ubicación física, en una misma red de difusión. Las VLANs permiten segmentar una red física en múltiples dominios lógicos, mejorando la seguridad, la administración y el rendimiento de la red.

***

### Acceso al Switch con PuTTY

#### Conexión por SSH (Recomendada)

1. Abre `PuTTY.exe`.
2. En "Host Name (or IP address)", introduce la IP del switch.
3. Asegúrate de seleccionar el protocolo **SSH**.
4. Pulsa en **Open** para establecer la conexión.

#### Conexión por Cable Serial (Consola)

1. Conecta el cable de consola desde tu PC al puerto **Console** del switch.
2. Abre `PuTTY.exe`.
3. En “Connection type”, selecciona **Serial**.
4. En el campo “Serial line”, introduce el puerto COM adecuado (ej. `COM3`).
5. Haz clic en **Open**.

***

### Acceso a la Interfaz de Configuración

#### Escenario 1: Switch Reseteado

Si el switch se ha restaurado a configuración de fábrica:

* Te pedirá si deseas hacer una configuración automática: selecciona **n** (no).
* Verás el prompt: `Switch#`

#### Escenario 2: Switch con Configuración Existente

1. Presiona **Enter** hasta ver `Switch>`.
2. Teclea el siguiente comando para entrar al modo privilegiado EXEC:

```bash
enable # Tambien se puede con una acortacion "en"
```

Prompt esperado: `Switch#`

***

### Modo de Configuración Global

Desde el modo privilegiado EXEC, ingresa al modo de configuración global con:

```bash
configure terminal # Para entrar en la configuracion del switch
```

o su abreviación:

```bash
conf t
```

Prompt esperado: `Switch(config)#`

***

### Creación de VLANs

#### VLAN 10

```bash
vlan 10               # Crea la VLAN con ID 10
name vlan10           # Asigna el nombre "vlan10" a la VLAN 10 para identificarla fácilmente
exit                  # Sale del modo de configuración de VLAN
```

#### VLAN 20

```bash
vlan 20               # Crea la VLAN con ID 20
name vlan20           # Asigna el nombre "vlan20" a la VLAN 20 para identificarla fácilmente
exit                  # Sale del modo de configuración de VLAN
```

***

### Asignación de Puertos a VLANs

#### VLAN 10 (Puertos 1 al 12)

```bash
interface range FastEthernet0/1-12      # Entra en el modo de configuración para los puertos del 1 al 12
description dpto vlan10                 # Agrega una descripción a los puertos (útil para identificar su uso)
switchport mode access                  # Configura los puertos en modo acceso (solo una VLAN por puerto)
switchport access vlan 10               # Asigna la VLAN 10 a esos puertos
switchport nonegotiate                  # Desactiva la negociación DTP (evita que intenten negociar trunk)
no shutdown                             # Habilita los puertos (si estaban apagados por defecto)
exit                                    # Sale del modo de configuración de interfaz
```

#### VLAN 20 (Puertos 13 al 23)

```bash
interface range FastEthernet0/13-23      # Entra en el modo de configuración para los puertos del 13 al 23
description dpto vlan20                 # Agrega una descripción a los puertos (útil para identificar su uso)
switchport mode access                  # Configura los puertos en modo acceso (solo una VLAN por puerto)
switchport access vlan 20               # Asigna la VLAN 20 a esos puertos
switchport nonegotiate                  # Desactiva la negociación DTP (evita que intenten negociar trunk)
no shutdown                             # Habilita los puertos (si estaban apagados por defecto)
exit                                    # Sale del modo de configuración de interfaz
```

***

### Configuración del Puerto Trunk (Puerto 24)

El puerto `trunk` es necesario para permitir el tráfico de múltiples `VLANs` entre el `switch` y otro dispositivo como un `firewall` o `switch` adicional.

```bash
interface FastEthernet0/24      # Entra en el modo de configuración del puerto 24
switchport mode trunk           # Configura el puerto como trunk (permite múltiples VLANs)
switchport nonegotiate          # Desactiva DTP para evitar negociaciones automáticas de trunk
no shutdown                     # Habilita el puerto trunk (si estaba en estado de "shutdown")
exit                            # Sale del modo de configuración de interfaz
```

***

### Guardar la Configuración

Después de completar todas las configuraciones, asegúrate de guardarlas:

```bash
end
write memory
```

O simplemente:

```bash
do wr
```

Esto almacenará la configuración en la memoria `NVRAM`, preservándola después de un reinicio del dispositivo.

***

### Diagrama Explicativo

> Dibujo explicativo de los pasos anteriores:

<figure><img src="../.gitbook/assets/image (5).png" alt=""><figcaption></figcaption></figure>

> Diagrama de lo que sucede en general en la red la realizar estos pasos:

<figure><img src="../.gitbook/assets/image (1) (1).png" alt=""><figcaption></figcaption></figure>

***

### Conclusión

Esta guía proporciona los pasos esenciales para configurar `VLANs` en un `switch Cisco`, incluyendo el acceso remoto, la creación de `VLANs`, asignación de puertos y configuración de `trunks`. Aplicar estas configuraciones correctamente mejora la segmentación de la red, facilita la gestión y refuerza la seguridad.
