---
icon: triangle-exclamation
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

# Problemas y errores instalación Covenant

En algunas ocasiones es posible que al seguir el procedimiento de instalación de `Covenant` que se muestra en el siguiente vídeo os aparezca un error similar al siguiente:

<figure><img src="../../.gitbook/assets/image (179).png" alt=""><figcaption></figcaption></figure>

El problema que aparece es debido a la versión de `.NET` que tienes instalada en tu máquina `Kali Linux`. Tienes que instalar la versión `3.1` que es la compatible con `Covenant`. Para ello, ejecuta los siguientes comandos en la terminal:

```shell
## PASO 1:

wget https://packages.microsoft.com/config/debian/11/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
rm packages-microsoft-prod.deb
sudo apt update

## PASO 2:

wget http://snapshot.debian.org/archive/debian/20190501T215844Z/pool/main/g/glibc/multiarch-support_2.28-10_amd64.deb
sudo dpkg -i multiarch-support*.deb

## PASO 3:

wget http://snapshot.debian.org/archive/debian/20170705T160707Z/pool/main/o/openssl/libssl1.0.0_1.0.2l-1%7Ebpo8%2B1_amd64.deb
sudo dpkg -i libssl1.0.0*.deb
sudo apt install -y dotnet-sdk-3.1
export DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1
```

Una vez hecho esto, ejecuta de nuevo `dotnet run` en la carpeta `Covenant/Covenant` y ya debería funcionar correctamente.
