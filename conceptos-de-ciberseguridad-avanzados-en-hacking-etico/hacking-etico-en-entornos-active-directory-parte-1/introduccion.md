---
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

# Introducción

> ¿Que es `Active Directory`?

`Active Directory` es simplemente un almacen de informacion acerca de todos los recursos que tenemos en una red y facilita su organizacion, busqueda y gestion por parte de los usuarios y administradores.

Utiliza un almacen de datos estructurado y jerarquico como base para una organizacion jerarquica de la informacion. Este almacen se denomina `directorio`.

Los recursos almacenados en `Active Directory` suelen incluir:

* Servidores
* Impresoras
* Cuentas de usuario
* Equipo de red

Ademas de un almacen de informacion (base de datos), `Active Directory` esta formado por un conjunto de servicios.

`Active Directory Domain Server` (AD DS) se corresponde con un conjunto de servicios que controlan diferentes operaciones dentro de un entorno `IT`:

* Autenticacion: Asegura que cada entidad es quien dice ser
* Autorizacion: Asegura que cada entidad tiene acceso a los datos y servicios que tiene permitidos
* Resolucion de nombres: Permite la comunicacion entre elementos en la red a traves de un nombre
* Gestion centralizada: Permite la aplicacion de politicas de grupo

> Estructura de `Active Directory`

`Bosques` (forests), `Dominios` (domains) y `Unidades Organizativas` (Organizational Units) son los elementos principales de una estructura logica de `Active Directory`.

Un `Bosque` es el nivel organizativo mas alto dentro de `Active Directory`. Cada `bosque` comparte un unico directorio y representa un limite de seguridad.

Los `bosques` pueden contener uno o varios `Dominios`.

Los `Dominios` pueden contener uno o varios `OUs`

La informacion de los `Dominios` y de las `OUs` se almacenan en un `controlador de dominio` para el dominio especifico. Este almacen se denomina `Data Store`.

La informacion se almacena en forma de `objeto`, todos los objetos estan definidos por un `esquema`. El directorio valida que los datos son validos basandose en este esquema.

> ¿Que es un `dominio`?

Un `Dominio` es una **particion logica de objetos dentro de un bosque** que comparten configuraciones comunes de administracion, seguridad y replicacion. Concretamente:

* **Garantiza la identidad** de un usuario en toda la red
* Proporciona servicios de `autenticacion`
* Proporciona servicios de `autorizacion`
* Permiten **replicar la informacion** entre diferentes `controladores de dominio (DC)` y gestionarlos como una unica unidad.
* Permite la creacion de `relaciones de confianza`

> ¿Que es la `unidad organizativa (OU)`?

Una `unidad organizativa (OU)` es un objeto contenedor que permite organizar otros objetos dentro de un `dominio`. Tiene tres funciones principales:

* Permite una `visualizacion organizada` de los objetos del `dominio`
* Agrupa diferentes objetos a los que aplicar `Politicas de Grupo`
* Agrupa diferentes objetos de manera que se puedan `delegar permisos de gestion` a otros usuarios y grupos dentro del `dominio`.

> ESQUEMA DE UN BOSQUE:

<figure><img src="../../.gitbook/assets/image (126).png" alt=""><figcaption></figcaption></figure>

> Active Directory Schema

<figure><img src="../../.gitbook/assets/image (127).png" alt=""><figcaption></figcaption></figure>

Todo lo que se almacena en `Active Directory` se almacena en forma de `objeto`. El esquema define los atributo para cada tipo de objeto.

Se define un esquema por `Bosque`

Una copia del esquema reside en todos los controladores de dominio del `Bosque` de manera que la definicion de los objetos sea la misma.

El `Data Store` utiliza el esquema para forzar la `integridad de la informacion`

El resultado es que todos los objetos se crean de manera uniforme, independientemente del `controlador de dominio` que los cree o modifique.

> Componentes del `Data Store`

`Interfaces (LDAP, REPL, MAPI, SAM):` Las interfaces proporcionan una manera de comunicarse con la base de datos

`DSA:` Permite obtener acceso al directorio. Mantiene el esquema, garantiza la identidad de los objetos, fuerza los tipos de datos en los atributos...

`Database Layer:` Es una API que sirve de interfaz entre las aplicaciones y el directorio, de manera que las aplicaciones no puedan interactuar directamente con la base de datos.

`ESE:` Se comunica directamente con los registros individuales que se encuentran en el directorio.

`Database Files:` La informacion del directorio se almacena en un unico fichero de base de datos. Adicionalmente utiliza ficheros de logs para transacciones que no terminan adecuadamente.
