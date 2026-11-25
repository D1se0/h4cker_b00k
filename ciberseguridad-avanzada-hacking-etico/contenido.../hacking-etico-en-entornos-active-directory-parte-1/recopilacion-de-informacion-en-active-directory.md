---
icon: file-circle-info
---

# Recopilación de información en Active Directory

> Tipos de auditoria de seguridad

`Auditoria externa:` No se dispone de acceso `logico` o `fisico` a la infraestructura de red de la organizacion.

`Auditoria interna:` Se dispone de acceso `logico` (ej. `VPN`) o `fisico` (instalaciones del cliente) o la infraestructura de red de la organizacion

* Sin credenciales de usuario de dominio
* Con credenciales de usuario de dominio
  * Credenciales de usuario sin privilegios
  * Credenciales de usuario con privilegios

> ¿Que informacion recopilar?

Usuarios y cuentas locales Grupos locales Usuarios y cuentas de dominio Equipos en el dominio Grupos de dominio `Ous` `GPOs` `ACLs` Relaciones de confianza entre `Bosques` y `Dominios` Atributos de los objetos de `Active Directory` ...

> Recopilacion local de informacion

`SAM (Security Account Manager)` se corresponde con una base de datos en `Windows` que almacena informacion sobre `usuarios, grupos, contraseñas...` del sistema

La base de datos `SAM` se comprueba por el `LSA (Local Security Authority)` para autenticar el acceso de los usuarios al sistema local

Las contraseñas de los usuarios se almacenan `hasheadas` en el `Registro de Windows (HKLM/SAM)`. El fichero se encuentra en `%SystemRoot%/system32/config/SAM`

La `SAM` se puede enumerar de forma local y remotamente

* A partir de la version `Windows 10 1607` y `Windows Server 2016` esta informacion solo puede obtenerla un administrador del sistema. En versiones anteriores cualquier usuario de dominio puede enumerarla.

> Recopilacion remota de informacion

`Interfaces (LDAP, REPL, MAPI, SAM):` Las interfaces proporcionan una manera de comunicarse con la `base de datos`.

`DSA:` Permite obtener acceso al directorio. Mantiene el esquema, garantiza la identidad de los objetos, fuerza los tipos de datos en los atributos...

`Database Layer:` Es una `API` que sirve de interfaz entre las aplicaciones y el directorio, de manera que las aplicaciones no puedan interactuar directamente con la base de datos.

`ESE:` Se comunica directamente con los registros individuales que se encuentran en el directorio.

`Database Files:` La informacion del directorio se almacena en un unico fichero de `base de datos`. Adicionalmente utiliza ficheros de `log` para transacciones que no permitan adecuadamente.

`LDAP (Lightweight Directory Access Protocol)` es un protocolo de aplicacion que permite interactuar con servicios de directorio (como `Active Directory`) para almacenar, leer o modificar informacion.

Cualquier usuario de dominio puede consultar `NTDS.dit` utilizando `LDAP`, independientemente de sus privilegios.

* [Forum Prevencion de LDAP](https://social.technet.microsoft.com/Forums/en-US/cf79c2f2-4467-45cb-8041-abc6abb56b33/how-do-you-prevent-ldap-enumeration?forum=winserverDS)
