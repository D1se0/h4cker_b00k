---
icon: expeditedssl
---

# Openssl bruteforce script

Si alguna vez se necesita sacar alguna contraseña a fuerza bruta con algun archivo que esta encriptado por `openssl` que eso se mira haciendo el comando `file` a un archivo y para desencriptarlo se necesita una contraseña que no sabemos, con este script se automatiza todo...

```sh
#!/bin/bash

function ctrl_c(){
        echo -e "\n\n[!] Saliendo...\n"
        tput cnorm; exit 1
}

#Ctrl+C
trap ctrl_c INT

tput civis; for password in $(cat /usr/share/wordlists/rockyou.txt); do
        openssl aes-256-cbc -d -in file.enc -out file.decrypted -pass pass:$password &>/dev/null

        if [ "$(echo $?)" == "0" ]; then
                echo -e "\n[+] La password es $password\n"
                exit 0
        fi
done; tput cnorm
```

Un script simple que se tiene que cambiar a gusto del que lo utilice los campos de cifrado, wordlist y nombre del archivo...

#### Script mejorado

Este otro script es mejorado al anterior y te lo automatiza a la hora de elegir el tipo de archivo, wordlist y cifrado...

```sh
#!/bin/bash

function ctrl_c(){
        echo -e "\n\n[!] Saliendo...\n"
        tput cnorm; exit 1
}

#Ctrl+C
trap ctrl_c INT

# Solicitar al usuario el archivo encriptado, la lista de palabras y el método de cifrado
read -p "Introduce el archivo encriptado: " encrypted_file
read -p "Introduce la lista de palabras: " wordlist
read -p "Introduce el método de cifrado: " cipher_mode

tput civis; for password in $(cat $wordlist); do
        openssl $cipher_mode -d -in $encrypted_file -out file.decrypted -pass pass:$password &>/dev/null

        if [ "$(echo $?)" == "0" ]; then
                echo -e "\n[+] La contraseña es $password\n"
                tput cnorm
                exit 0
        fi
done; tput cnorm

echo -e "\n[!] No se encontró la contraseña correcta.\n"


# Todas las posibles codificaciones (Todo en minuscula):

# AES-128-CBC
# AES-128-CFB
# AES-128-CFB1
# AES-128-CFB8
# AES-128-CTR
# AES-128-ECB
# AES-128-OFB
# AES-192-CBC
# AES-192-CFB
# AES-192-CFB1
# AES-192-CFB8
# AES-192-CTR
# AES-192-ECB
# AES-192-OFB
# AES-256-CBC
# AES-256-CFB
# AES-256-CFB1
# AES-256-CFB8
# AES-256-CTR
# AES-256-ECB
# AES-256-OFB
# AES128
# AES192
# AES256
# BF
# BF-CBC
# BF-CFB
# BF-ECB
# BF-OFB
# CAMELLIA-128-CBC
# CAMELLIA-128-CFB
# CAMELLIA-128-CFB1
# CAMELLIA-128-CFB8
# CAMELLIA-128-CTR
# CAMELLIA-128-ECB
# CAMELLIA-128-OFB
# CAMELLIA-192-CBC
# CAMELLIA-192-CFB
# CAMELLIA-192-CFB1
# CAMELLIA-192-CFB8
# CAMELLIA-192-CTR
# CAMELLIA-192-ECB
# CAMELLIA-192-OFB
# CAMELLIA-256-CBC
# CAMELLIA-256-CFB
# CAMELLIA-256-CFB1
# CAMELLIA-256-CFB8
# CAMELLIA-256-CTR
# CAMELLIA-256-ECB
# CAMELLIA-256-OFB
# CAMELLIA128
# CAMELLIA192
# CAMELLIA256
# CAST
# CAST-cbc
# CAST5-CBC
# CAST5-CFB
# CAST5-ECB
# CAST5-OFB
# ChaCha20
# DES
# DES-CBC
# DES-CFB
# DES-CFB1
# DES-CFB8
# DES-ECB
# DES-EDE
# DES-EDE-CBC
# DES-EDE-CFB
# DES-EDE-ECB
# DES-EDE-OFB
# DES-EDE3
# DES-EDE3-CBC
# DES-EDE3-CFB
# DES-EDE3-CFB1
# DES-EDE3-CFB8
# DES-EDE3-ECB
# DES-EDE3-OFB
# DES-OFB
# DES3
# DESX
# DESX-CBC
# RC2
# RC2-40-CBC
# RC2-64-CBC
# RC2-CBC
# RC2-CFB
# RC2-ECB
# RC2-OFB
# RC4
# RC4-40
# SEED
# SEED-CBC
# SEED-CFB
# SEED-ECB
# SEED-OFB
```

## <mark style="color:purple;">Openssl brute force</mark>

Si en algun momento encuentras un archivo con alguna extension rara por ejemplo `.enc` o `.decrypt` etc... Y sobre todo si hacemos lo siguiente...

```shell
file example.enc
```

Info:

```
example.enc: openssl enc'd data with salted password
```

Si vemos alguna vez ese tipo de mensaje quiere decir que el contenido del archivo esta cifrado con una contraseña que tienes que saber para que pueda ser legible...

```shell
openssl aes-256-cbc -d -in example.enc
```

Te pedira la contraseña para desencriptarla y eso suponiendo que la codificacion es en `SHA-256`, pero para ello hay herramientas que te automatizan todo esto...

URL = https://github.com/HrushikeshK/openssl-bruteforce/tree/master

URL = https://github.com/glv2/bruteforce-salted-openssl (En vez de descargartelo desde el repositorio recomiendo instalartelo como herramienta...)

```shell
apt install bruteforce-salted-openssl
```

Una de las 2 sirve...

Sin embargo para encriptar algun archivo que contenga algo, se podra hacer de la siguiente forma...

```shell
openssl aes-256-cbc -in example.txt -out example.cypted
```

Y te pedira una contraseña que sera con la que podras desencriptarlo...

#### Uso de la herramienta openssl-bruteforce de la primera URL

```shell
python brute.py <WORDLIST> ciphers.txt <FILE_OPENSSL>
```

