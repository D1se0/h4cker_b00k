---
icon: block-brick-fire
---

# Pfsense Firewall Configuración GUIA

## <mark style="color:green;"># Config VirtualBox Pfsense</mark>

### <mark style="color:purple;"># Links requisitos</mark>

LINK (Pfsense) = [https://archive.org/details/pfSense-CE-2.6.0-RELEASE-amd64](https://archive.org/details/pfSense-CE-2.6.0-RELEASE-amd64)

LINK (VirtualBox) = [https://www.virtualbox.org/wiki/Downloads](https://www.virtualbox.org/wiki/Downloads)

### <mark style="color:purple;"># Inicio Config</mark>

Lo primero que tendremos que hacer será instalar la ISO (IMAGE ISO) de Pfsense de la siguiente forma:

Elige un nombre identificativo para la máquina. En "Carpeta", especifica la ruta de instalación. En "Imagen ISO", selecciona la ISO descargada de Pfsense. Para las opciones "Tipo" y "Versión", elige "BSD" y "FreeBSD (64-bit)", respectivamente, como se muestra en la captura.

<figure><img src="https://lh7-us.googleusercontent.com/docsz/AD_4nXedQPbTH9mcW-mOsvVENiivZtgZLjNt-eiVmHDyUnCrDyePTWLG9yvhTOYi7N8ahOx2Sb3e4fHcAbUrUY9NcuZt6HLxtJy-SWEF6WDw7uhbZqXu_v2Ccm4LLFoUeQcQm6mY2th6rjeerArldHaPFPz55Yk?key=BIdnsx2kvhiLCGz7N7uenw" alt=""><figcaption></figcaption></figure>

En la siguiente sección, selecciona los recursos necesarios para la máquina. En mi caso, dejé los valores predeterminados.

<figure><img src="https://lh7-us.googleusercontent.com/docsz/AD_4nXcvD9wEZksmUtt0GTKzVQcrCAwlqTi4LaIo7F2vSr6VBbhngafROpqq8iD3ve-iBO6491KnghGdkT6e3aThGBqLGYy38WGO2o6b1PAw4nJSQABv67MNtqVDkbl20CO9ePJUllCMUnlGPbvZPVFHWcm5G6nL?key=BIdnsx2kvhiLCGz7N7uenw" alt=""><figcaption></figcaption></figure>

En la siguiente sección, selecciona el tamaño del disco virtual. Yo opté por dejar el valor predeterminado.

<figure><img src="https://lh7-us.googleusercontent.com/docsz/AD_4nXe5sdq2SNL-4CJRUGu_CSkJayziS0u0kN_5__Tnf3j_aqUWoMkkUyL3oBlWjkZccXRvCMjCiKgXPec-GE-xNl3DpHmSz013JXOaGsabkNyhWJJ22e68zQwN4uKIYLEb_q6EWIoWCsXboyt_bb7RjtUgohj0?key=BIdnsx2kvhiLCGz7N7uenw" alt=""><figcaption></figcaption></figure>

Una vez configurado todo lo anterior, finalizamos la instalación de la máquina Pfsense y procederemos a la configuración de red para asegurar su correcto funcionamiento.

### <mark style="color:purple;"># Configuración Red:</mark>

En el menú “Herramientas”, haz clic en las tres barras para desplegar una serie de opciones. Selecciona la opción llamada “Red”.

<figure><img src="https://lh7-us.googleusercontent.com/docsz/AD_4nXfOkZVlv9a2OI2P5BTQ1wX74f1351QGtj-POi1Q2eNwqkendEBF5cs9hzOG2d1sqgBxTmzWu-irKD5-pRdKQSRwNnpONe5DrDGKNfVDSutuNIeLXSEsrSu1JRg8QPNW6tdOGIGLGApyoK7XUWlVXjvOlWr0?key=BIdnsx2kvhiLCGz7N7uenw" alt=""><figcaption></figcaption></figure>

<figure><img src="https://lh7-us.googleusercontent.com/docsz/AD_4nXcZdZoKXSbWEKDomsgcqwegdJnu-c0IuilORvMn2-FMFxyBdKF99BzGTSc4MfFusJaBo1g-RO5s_Gi1qp0tiCx3j3p-sH5iglggOgO_IgotlY_uDu5DkVtF083rpW_eLFL4k10HI2NSyjkev7mvAIreDoNy?key=BIdnsx2kvhiLCGz7N7uenw" alt=""><figcaption></figcaption></figure>

Dentro de esta sección, verás lo siguiente: en tu caso, solo habrá una red en la pestaña “Redes solo-anfitrión” con una IP de tipo /16. Debes cambiar esta IP a una de tipo /24 desde tu host, ya que en nuestro caso ya estará cambiada.

<figure><img src="https://lh7-us.googleusercontent.com/docsz/AD_4nXc5z1EORDFMBqvFirLlbz7e7iVDdPKTicz_0LlWGwdAR6t33LvtZ13vY8VzN7mENN8QqLOa4D4J6E6SIF9myHxJl1aVUe5c46zpvs-M1AdCYHKPKFw9VbXazc2Y0-kI4XezGApoTOiKYG80FlsIulpzicE?key=BIdnsx2kvhiLCGz7N7uenw" alt=""><figcaption></figcaption></figure>

Abriremos las conexiones de red haciendo un atajo de teclado “Windows + R” y ponemos “ncpa.cpl” para abrirlo.

<figure><img src="https://lh7-us.googleusercontent.com/docsz/AD_4nXfrbmR7fzXosmG7FpjXZ0BdrJbuBZzWda4cCqPggejN_TQNcigG4DjM0Uh4U5l6bw4yghcb9EG_4pSHnD4I6mIaLUjiGOfHkenJTdTBYXgJDQpN-d4armx_oiRzgXP6Ox7XKJhf12pQtQ7bUMUNgVqO_O3k?key=BIdnsx2kvhiLCGz7N7uenw" alt=""><figcaption></figcaption></figure>

Debemos modificar la red de VirtualBox llamada “Ethernet 3 (VirtualBox Host-Only)”. Para ello, accede a “Propiedades”, selecciona “Protocolo de Internet versión 4 (TCP/IPv4)”, y luego elige “Usar la siguiente dirección IP:”. Configura la IP deseada; en mi caso, utilicé “192.168.56.51” (puedes usar la misma). Guarda y aplica los cambios.

<figure><img src="https://lh7-us.googleusercontent.com/docsz/AD_4nXd_vWlBFa5zYp3dabfq9diQEa9HIsUxi7BJWEp0Pscm2SOeeieOAP_Y_ClmuPosla5vI5TvoX3E6P2r1lDVlImEcyH_3EcgdSGNij8vQT51jwOqeodOO4aws6uHJMkMCwArZOR8fvSFmDTu-JsT2qlE7rw?key=BIdnsx2kvhiLCGz7N7uenw" alt=""><figcaption></figcaption></figure>

Actualizamos VirtualBox cerrando y volviendo a abrir la pestaña. Al regresar a la sección “Red”, veremos que los cambios se han aplicado correctamente.

Luego, vamos a las opciones de “Red” de la máquina Pfsense y seleccionamos “NAT” en el “Adaptador 1”.

<figure><img src="https://lh7-us.googleusercontent.com/docsz/AD_4nXfTPADNaFGgNQQs2o86vsN5oDTgWPZgQlCf-xUdIKxLEQcT74x_rM-lUHmyaJkgcJ-4f2fHKtL9zxFYm-fgJi5ZqgpHsBSut8V2HWrcu__yB-P3fJ0Hn4gxnXT5aq9JIm3pEjpFl0I3NbfSRachnedjLq0o?key=BIdnsx2kvhiLCGz7N7uenw" alt=""><figcaption></figcaption></figure>

En el “Adaptador 2”, selecciona “Adaptador solo anfitrión” y elige el “Host-Only” que actualizamos anteriormente. Guarda toda la configuración.

<figure><img src="https://lh7-us.googleusercontent.com/docsz/AD_4nXfK7mMBAe_Uql5rCdCjAwYwk6_K_vRsPMqhwUl4HVoVmH_5VJojEB0wv2kAOtAJz024-mHlnXKnX4KoYuX1CsV84GZAk0Yl4Z2FsuWl7QSY9jnwTmuErXiVSe0g50PS99FqDH3FHsq5xQmruiQzy9_27i_S?key=BIdnsx2kvhiLCGz7N7uenw" alt=""><figcaption></figcaption></figure>

Hecho esto abriremos Pfsense.

### <mark style="color:purple;"># Configuración Pfsense:</mark>

Una vez que se inicie la máquina, nos aparecerá el aceptar el Copyright, lo aceptamos.

Le damos a la primera opción “Install”.

<figure><img src="https://lh7-us.googleusercontent.com/docsz/AD_4nXeXBSjb5EBSgXMiJ38yj_n8jA0ny8a2GkghiWWWjhVkjOX0YT_ZPSYpb46Mdri7jNNzzZ9GztS25WjNWgnlKI5v0glcwKL7dwspHJYePH6VDPqe4O217RPJhYjzePs4eaJMe5Q2LV7niX8E8lOrgLQbbeCX?key=BIdnsx2kvhiLCGz7N7uenw" alt=""><figcaption></figcaption></figure>

Seleccionamos las opciones por “Default”.

<figure><img src="https://lh7-us.googleusercontent.com/docsz/AD_4nXf7-N8j2yzVr1FSmr4zD2JuDRfyFS232wdzUEv_CgsvtE8DxAaWqpiIKE2I9_2s9BfwYJE9nzDPm2d-ZeTM5JzYVXDH9YeOpZjceyUET1oElq1XszcFOZO2LOoeF05_So0QmYM23EKVtx0g3nZ1XtWmfgk?key=BIdnsx2kvhiLCGz7N7uenw" alt=""><figcaption></figcaption></figure>

Y cuando lleguemos a esta parte, le damos a la segunda llamada “Auto (UFS) BIOS”

<figure><img src="https://lh7-us.googleusercontent.com/docsz/AD_4nXdocLpOH6ZcbfEt010mQurAzmh5SPHmouo-En3jRURHq3uQLOW0DO-iBp0VQwC6SMLDevU_uv61lPUm1NLbAzfh8j88VOX11gKKMSwcAzPmuNWN8FDIzNE5MUmluoKPWf2fba7JfcML33leF9ub3m-OcNE4?key=BIdnsx2kvhiLCGz7N7uenw" alt=""><figcaption></figcaption></figure>

<figure><img src="https://lh7-us.googleusercontent.com/docsz/AD_4nXd1ONWf7SJvxIpVzTA-XJ55ElTaAB4uDOL9Ml4f8DdhFon14mCaYE6ZiO-OkiBSczz6Oa1wiwOQZpHdXA52ytG54i9cgTsfkVK6hYk5b8zPj7MI6Gdgkq6VSZooBj0N4kVyAlzDXfHNK3CAQqEOQJ8TreJQ?key=BIdnsx2kvhiLCGz7N7uenw" alt=""><figcaption></figcaption></figure>

Le damos a que “No” en esta parte.

<figure><img src="https://lh7-us.googleusercontent.com/docsz/AD_4nXc4P5a6XLNFdXEE1Q-Z_kBRKs_iSHRyDNeQXQ23UcXAuQhK2qPJvGp7s1JivoIbxlGB2yM0KuGOIZHaq1tSCgug_lPAr6WZTn-Eo8ZchmMEyy0OXfazvPcrm_JInJluDU7kbaQDSniWCLtzDFXDjDoSFnJh?key=BIdnsx2kvhiLCGz7N7uenw" alt=""><figcaption></figcaption></figure>

Y por último seleccionamos “Reboot”.

<figure><img src="https://lh7-us.googleusercontent.com/docsz/AD_4nXeKRVjlcp3Uu690LbjiqHPCzzI1pF9_U0VPxFPj21-PkG8_bGghTctuGowVx4cdpCJFOeEOLH9XIRL7k4V0KKuXfyBjChu-7Hvx40o9uJPwMupJTsjA_VttQGQKy3eOsgLOTiYt7YM6fwIHOwN7E_ZfJwWb?key=BIdnsx2kvhiLCGz7N7uenw" alt=""><figcaption></figcaption></figure>

Rápidamente ve a “Dispositivos”, luego a “Unidades Ópticas” y deselecciona el disco del instalador de Pfsense como se muestra en la captura. Esto evitará que el sistema vuelva al instalador y nos lleve directamente a la configuración por terminal.

<figure><img src="https://lh7-us.googleusercontent.com/docsz/AD_4nXdLuNJQx-7UwaFF3I4TnHAYu7J8pO8KNiBm3ZcNWFNnwkhW4oXnQweOzFvoyCOzigDTU13YXszFKxSM6xm_fmJTe3VwXlABFbU5L4KQ20LqhzDEgS7Q_G-HWlyJ6Q4rHiPGG_aBpSIqDF7ZUG0f57ga7Gf1?key=BIdnsx2kvhiLCGz7N7uenw" alt=""><figcaption></figcaption></figure>

Una vez quitada la selección del disco, si no nos lleva automáticamente a la configuración por terminal, reiniciamos la máquina. En ese punto, debería iniciarse la configuración por terminal como se muestra a continuación.

<figure><img src="https://lh7-us.googleusercontent.com/docsz/AD_4nXccTb1yX3hpOtrMaF4Rs-MwHky0EVhTEIZFYSGa71DVgky4l_klBbEVgPH82qF4Kw7knLPnaZgMuhoxmgoDnFypsfqdRCcqCfhOouNXimbOYEfeQxIs7C7heDvBGa6SW-CgCZXDjhRqra02INCgEhqPs79M?key=BIdnsx2kvhiLCGz7N7uenw" alt=""><figcaption></figcaption></figure>

Seleccionamos la opción “2” para configurar la IP que asignamos al adaptador "Host-Only" en Pfsense. Introducimos la IP “192.168.56.2” como la puerta de enlace (gateway) para acceder a la página web de Pfsense a través de esa dirección IP.

<figure><img src="https://lh7-us.googleusercontent.com/docsz/AD_4nXdUMD_2Uu6y2ZQtaqGrX3K4Y5pD1mo-D1KkSm53nPTFJ8R_L9NlCsm41xS59-5wYQW3BnDjHMzEDbccb3La_wEpSv_tOSusj7c-irvzVkjPojQpza-5X-ay4yhWd6xG_7VZtDDsZnzRi9s5Dx2pgdIU030?key=BIdnsx2kvhiLCGz7N7uenw" alt=""><figcaption></figcaption></figure>

En la opción (1 to 32), seleccionamos 24, ya que creamos una dirección IP de /24 (192.168.56.2/24). Dejamos las demás opciones en sus valores por defecto hasta llegar a la configuración de DHCP, donde seleccionaremos “y”. Configuraremos el rango de DHCP como (192.168.56.100 a 192.168.56.200) en ambas opciones de rango. Finalmente, en la opción de HTTP, seleccionamos “n” para guardar la configuración.

<figure><img src="https://lh7-us.googleusercontent.com/docsz/AD_4nXeNng7Ywuu1FtlkURlnN0Sph0c4IrUSgMFgq3HWApZm6v8ncKzoAH5aCr5AMbvo33Hlebt-mFMrnXWg0KYdrmiCbPXyfxizgm5Tv9x-9ZJ2F12OJ_wf18hjjgZXDkXGVs83iI7SB7-ETjio2P_du500fQBh?key=BIdnsx2kvhiLCGz7N7uenw" alt=""><figcaption></figcaption></figure>

Por lo que vemos en “browser:” nos pone la dirección IP de la web donde podremos visitarla (https://192.168.56.2/).

<figure><img src="https://lh7-us.googleusercontent.com/docsz/AD_4nXddeJ_iv4V9CG2xUNjAxRohEPQBvjj1C-J8YMPhizKUocDBjkNn4cMUmG6DDRc1YgMJX_RDofh3Il8xkzZF-hi4ao-SUvguVuTgf3FzNhCvzlR_U0UPspGj0kG3VVLzzbNVpcy1T5olpByHgmgbHyuTQ21x?key=BIdnsx2kvhiLCGz7N7uenw" alt=""><figcaption></figcaption></figure>

Una vez dado a “Enter” ya podremos visitar la página web de Pfsense.

<figure><img src="https://lh7-us.googleusercontent.com/docsz/AD_4nXcPqoQJIyVZRCDwgt-2arZ0iRNyRjRLqXJgWo-qNiUHJKsD_yxEYKIQW14qlgpcsJV_rUEb8hwRWzxHSwIKsyvuS82m9BxB9oLbcqX7OyI_uFTBNngyFLaCgyT4JV4rC6wqxbzJD2Awqqu8OcFqRZPyiVuS?key=BIdnsx2kvhiLCGz7N7uenw" alt=""><figcaption></figcaption></figure>

Para verificar que tenemos la IP correcta, abrimos el “cmd” y ejecutamos el comando “ipconfig” para ver nuestras redes. Deberíamos encontrar la IP que configuramos en "Host-Only" (192.168.56.51).

<figure><img src="https://lh7-us.googleusercontent.com/docsz/AD_4nXe7PEKwiT5anZD4aUiNGvawYj2FjECG5HcTjXySHXxYzqsEVgahdC7HoyGLChuBQeTVxVz11HgZKb-Rs29r8357V8G5LUFmZXNXkx1cy9YBVsXyVfoOgaLsCLTt2lFBENYGlb86q5qrTJ9RDwddvUHrQs8g?key=BIdnsx2kvhiLCGz7N7uenw" alt=""><figcaption></figcaption></figure>

### <mark style="color:purple;"># Pagina Web Pfsense:</mark>

Una vez comprobado que nos detecta la red, pondremos la dirección que nos dio Pfsense para poder entrar al login del mismo. ([https://192.168.56.2/](https://192.168.56.2/))&#x20;

\> Credenciales (Default):

User: `admin`

Password: `pfsense`

<figure><img src="https://lh7-us.googleusercontent.com/docsz/AD_4nXezXcqvihGQj2lwEn3YdyY1ruRAsp5I2K36RUTQw-f55cCFCxmb2p3K5miusw6zBAVUhx-Z1zl6-v2cRNbQgJ09SGPSsAtNTscIl5apbNmXTYnVFe5uDYW7_r91BnI2N-Okkrgctq8pwFYGhrqsAlYVmOA?key=BIdnsx2kvhiLCGz7N7uenw" alt=""><figcaption></figcaption></figure>

Una vez logueados podremos ver que estamos dentro de Pfsense.

<figure><img src="https://lh7-us.googleusercontent.com/docsz/AD_4nXf2ubWcAlDlrqp4DDT_0AsrW_mKZ_2aeSDjeaNsegL5SFYlpF6wztmY4GDhpGPy8OfmofUFb-GM2vReuYD4vYJkBMh5LDAR8IeMFlo_bEB5sIz6Z8NDv1OwuAzidbzvZE5cz40qTB5diRE8KjYA4aXYLU5u?key=BIdnsx2kvhiLCGz7N7uenw" alt=""><figcaption></figcaption></figure>
