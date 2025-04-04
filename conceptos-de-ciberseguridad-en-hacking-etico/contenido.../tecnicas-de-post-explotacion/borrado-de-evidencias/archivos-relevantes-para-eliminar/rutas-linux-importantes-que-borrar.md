# Rutas Linux Importantes que borrar

* `/var/log/messages`: mensajes globales del sistema operativo.
* `/var/log/secure`: información de autenticación y autorización.
* `/var/log/mail.log`: información del servidor de correo del sistema.
* `/var/log/cron`: información sobre cuando el demonio cron empieza una tarea.
* `/var/log/boot.log`: información de cuando el sistema arranca.
* `/var/log/btmp`:  logins fallidos (lastb)
* `/var/log/wtmp`: logins y logouts (last)
* `/var/log/lastlog`: logins en el sistema (lastlog)
* `/var/run/utmp`: usuarios en el sistema (who/w)
* `/var/log/dmesg`: logs del kernel (dmesg)

Comandos de shell:

* `~/.bash_history`
* `~/.sh_history`
* `~/.history`

Comando less:

* `~/.lesshst`

Clientes de FTP:

* `~/.lftp/rl_history y cwd_history`
* `~/.ncftp/history`

Equipos a los que se ha conectado con SSH:

* `~/.ssh/known_hosts`

Logs del servidor de aplicación

* `apache/logs/`
* `etc/httpd/logs/`
* `var/www/logs/`
* `var/log/`
* `usr/local/apache/logs/`
* `var/log/apache/`
* `var/log/apache2/`
