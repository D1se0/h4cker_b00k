# Introducción (Técnica de Post-Explotación)

Una vez que ha hemos sido capaces en una organizacion de vulnerar sus sistemas la mayoria no quiere que sigamos con las fases, que lo reportemos y listo, pero en algunas organizaciones quieren que sigamos probando su sistema para ver que mas vulnerabilidades tiene, por lo que esta fase no es muy comun en organizaciones.

Una vez que hayamos vulnerado algun equipo o servidor, tendremos que valorar como de sensible es que hayamos comprometido dicha maquina o no, teniendo informacion muy delicada o en otro caso algo que no importe es haber vulnerado un ordenador que esta aislado de todo y no tiene apenas informacion, hay que determinar todo eso, para saber la gravedad.

Tambien hay que tener cuidado cuando utilizamos herramientas de `hacking` para que no afecte a los servicios que se esten corriendo en ese momento, ya que algunas técnicas puedes ser muy intrusivas y hay que tener cuidado.

Luego entramos a las recomendaciones cuando se ejecuten este tipo de técnicas:

* No modificar ningun servicio que se considere critico a no ser que te dejes expresamente hacerlo.
* Las modificaciones y cambios en la configuracion realizados a los servicios deben ser documentados y revertidos (Si creemos que no podremos despues revertir ese ataque, mejor no efectuarlo.)
* Se debe de entregar una lista detallada de todas las acciones tomadas contra los sistemas del cliente y el periodo de tiempo en el que se realiza.
* Toda la informacion privada o personal que se descubra puede ser utilizada para ganar mas privilegios u obtener informacion adiccional, solo si se tiene autorizacion expresa del cliente y del que posee la informacion.
* Las contraseñas (aunque este cifrados) no deben adjuntarse en el reporte final
* No establecer mecanismos de persistencia en una maquina sin el consentimiento expreso del cliente.
* Toda la informacion recolectada durante la auditoria debe estar cifrada en los equipos de los analistas.
* Toda la informacion recopilada debe ser destruida una vez que el cliente acepte el reporte final.
