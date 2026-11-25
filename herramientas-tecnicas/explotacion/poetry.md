---
icon: user-unlock
---

# Poetry

Es similar a `hydra` o `medussa`, esta herramienta lo que hace es verificar los usuarios y contraseñas que le pases mediante el puerto del `ssh` por ejemplo, `smb`, `ftp`, etc... Se haria de la siguiente manera...

En tal caso de que se quisiera probar una contraseña con diversos usuarios, seria...

```shell
poetry run cme ssh <IP> -u <WORDLIST> -p '<PASSWORD>'
```

Si quieres que continue para que siga probando aunque de un `Success`...

```shell
poetry run cme ssh <IP> -u <WORDLIST> -p '<PASSWORD>' --continue-on-success
```

Si quieres probar contraseñas frente a un usuario...

```shell
poetry run cme ssh <IP> -u '<USER>' -p <WORDLIST>
```

