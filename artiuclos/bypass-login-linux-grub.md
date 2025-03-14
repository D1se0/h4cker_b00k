---
icon: linux
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

# Bypass Login Linux (GRUB)

Para `bypassear` un login de practicamente cualquier `linux` tendra que ser mediante el `GRUP` que es el metodo de arranque que utilizan generalmente los sistemas `linux` en formato de un menu, por lo que para que aparezca este menu en muchas ocasiones aparece de forma automatica y en otras como por ejemplo en `hipervisores` donde tenemos maquinas virtuales `linux` tendremos que pulsar `F2` y hacer `click iquierdo` a la vez nada mas se esta arrancando, en otros casos se nos abrira la `BIOS` y le tendremos que dar al `F10` para cerrarlo, seguidamente cuando se cierre darle `click iquierdo` con esto aparecera el `GRUB` de `linux`, tendremos que ver algo tal que esto:

<figure><img src="../.gitbook/assets/image (2) (1) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Estando en este punto le tendremos que dar a la tecla `E` para entrar a la edicion del `GRUB` en el que tendremos que modificar unas lineas en concreto.

Llendonos abajo del todo y viendo algo similar a esto:

<figure><img src="../.gitbook/assets/image (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Tendremos que eliminar desde la linea `$vt_handoff` hasta la linea `find_preseed` con esta incluida, quedando algo asi:

<figure><img src="../.gitbook/assets/image (2) (1) (1) (1) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Ahora donde pone `ro` que seran los permisos, tendremos que poner permisos de `lectura` y `escritura` ya que todo esto se ejecuta bajo el usuario `root`, por lo que tendremos que modificar eso y poner `rw` seguido de la siguiente linea `init=/bin/bash` para que asi podamos obtener una shell de `root` cuando se siga la ejecucion, viendose algo asi:

<figure><img src="../.gitbook/assets/image (3) (1) (1) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Y solo le tendremos que dar a `Ctrl+X` para continuar con el arranque del sistema con dicha configuracion, por lo que cuando le demos a esta combinacion y arranque el sistema veremos que obtendremos una shell autenticada como `root`:

<figure><img src="../.gitbook/assets/image (4) (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Por lo que ahora cambiaremos la contraseña al usuario que queramos en mi caso se llama `d1se0` por lo que pondremos lo siguiente:

```shell
passwd d1se0
```

Info:

```
New password: <PASSWORD>
BAD PASSWORD: The password is shorter than 8 characters
Retype new password: <REPIT_PASSWORD>
passwd: password updated successfully
```

<figure><img src="../.gitbook/assets/image (5) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Veremos que con esto ya habremos modificado la contraseña con exito, por lo que si ahora reiniciamos la maquina y probamos las credenciales que hemos modificado como `root` veremos que nos podremos logear y habremos `bypasseado` de alguna manera este login sin sabernos la contraseña anterior.

## <mark style="color:purple;">Mitigación de esta técnica</mark>

Para mitigar y evitar esto, tendremos que establecer un bloqueo en el `GRUB` para que solo la persona con permisos y que este autenticada pueda editarlo.

Dentro de la maquina virtual cambiaremos algunas lineas del archivo `/etc/grub.d/10_linux` pero antes `hashearemos` nuestra contraseña con `grub-mkpasswd-pbkdf2`

```shell
sudo apt update
sudo apt install grub-common
```

Ahora podremos ejecutar la herramienta:

```shell
grub-mkpasswd-pbkdf2
```

Info:

```
Enter password: <PASSWORD>
Reenter password: <REPIT_PASSWORD>
PBKDF2 hash of your password is grub.pbkdf2.sha512.10000.6E2CCDCFAC301BE10E99F09120BCCF61DE3D924127B0334C2FC4E0BEC1BB67A5D1D504B10CF1FE25BC55630B215D9050BB22BE682997E2F06766B74959064E83.AF7ACF90E1DAC36AF0DA3DA469FFBA17594E5BB6FEB52F0830F50E067EFAD5ADCE2E8FDD7B22B0C6BB889CEE1ADBCCA4B9F8BA6ED241C5AFAB39BC5D4777F426
```

Obtendremos este `hash` el cual tendremos que plantar de la siguiente forma en el archivo de `GRUB` que mencione anteriormente:

```shell
nano /etc/grub.d/10_linux

#Dentro del nano
cat << EOF
set superusers="d1se0,diseo"
password_pbkdf2 d1se0 grub.pbkdf2.sha512.10000.6E2CCDCFAC301BE10E99F09120BCCF61DE3D924127B0334C2FC4E0BEC1BB67A5D1D504B10CF1FE25BC55630B215D9050BB22BE682997E2F06766B74959064E83.AF7ACF90E1DAC36AF0DA3DA469>
password_pbkdf2 diseo grub.pbkdf2.sha512.10000.6E2CCDCFAC301BE10E99F09120BCCF61DE3D924127B0334C2FC4E0BEC1BB67A5D1D504B10CF1FE25BC55630B215D9050BB22BE682997E2F06766B74959064E83.AF7ACF90E1DAC36AF0DA3DA469>
EOF
```

Ahora actualizaremos estos cambios de la siguiente forma:

```shell
sudo update-grub
sudo grub-mkconfig -o /boot/grub/grub.cfg
```

Ahora si reiniciamos la maquina nos pedira en el `GRUB` unas credenciales las cuales establecimos cuando pulsamos la tecla `E`, de esta manera:

<figure><img src="../.gitbook/assets/image (6) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Y si metemos la contraseña correcta nos metera directamente al usuario.

Pero si fallamos la contarseña nos aparecera esto y nos llevara al `GRUB`:

<figure><img src="../.gitbook/assets/image (7) (1).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (8) (1).png" alt=""><figcaption></figcaption></figure>

Y si intentamos darle a la `E` nos aparecera la autenticacion para poder entrar, y si no la tenemos podremos iniciar de forma normal el `linux`.
