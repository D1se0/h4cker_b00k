---
icon: camera-cctv
---

# Tipos de auditorias de seguridad

Generalmente cuando una organizacion quiere comprobar su seguridad a nivel interno, lo que hacen es darte directamente el acceso por `SSH` del servidor de la nube de `amazon` para que lo compruebes a nivel interno, suelen crear un `security group` especialmente para el `auditor` en el que te conceden los permisos de poder entrar de forma remota desde tu equipo y que ahi ya realices la auditoria.

Esto se hace ya que seria una tonteria hacerle intentar entrar en tu servidor para luego comprobar lo que realmente la organizacion quiere comprobar.

Lo que generalmente quieren las organizaciones con esto es que por si algun motivo algun empleado, usuario o hacker, pudiera llegar a conectarse por cable o estar dentro de la misma red con el equipo atacante, a ver como de seguro es el servidor a nivel interno.

Nosotros como hackers eticos, nos daran la clave `.pem` para poder conectarnos a esa instancia que se ha creado para nosotros como auditores y poder auditarla desde `kali`.

Podremos realizar la auditoria con la herramienta de `nmap` instalandola como realizamos anteriormente o utilizando otro tipo de herramienta, haciendo un escaneo para ver si hubiera alguna base de datos en la misma red que podamos auditar o algun vector de entrada.

Si encontraramos algun puerto abierto podremos obtener el `banner` con la herramienta `netcat` ya que viene implementada por defecto en el servidor.

> NOTA IMPORTANTE

Una vez que hayamos terminado de realizar nuestras pruebas de pentesting, es muy importante eliminar nuestra cuenta de la nube de `amazon` eliminando todo paso a paso de todo lo que hemos estado creando, ya que si no lo eliminamos todo nos pueden cobrar los recursos consumidos de nuestra cuenta de la nube de `amazon`, todo este proceso puede llevar un rato.
