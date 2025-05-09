---
icon: cloud-binary
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

# Crear Entorno Vulnerable en Nube Local (Docker)

## Instalación Docker

Primero instalaremos `docker`:

```shell
sudo apt install docker-ce
```

Despues vamos a cargar la imagen de `ubuntu` con la ultima version:

```shell
docker pull ubuntu:latest
```

Ahora tendremos que ver en que `ID` de contenedor esta para meternos con una `shell` dentro del mismo.

```shell
docker images
```

Cogeremos unicamente los `3` primeros numeros de del `IMAGE ID` por ejemplo si fuera `03a` haremos lo siguiente:

```shell
docker run -it 03a
```

Y con esto tendremos una `shell` dentro del `docker`, ahora vamos actualizarlo de esta forma:

```shell
apt update
```

Echo todo esto, podremos pasar a la instalacion del entorno vulnerable de una `nube` de forma local.

## Instalación de los requisitos

Vamos a instalar todos los requisitos necesarios para realizar la instalacion de la `nube` local.

```shell
apt install -y apache2 php php-cli php-curl php-mbstring php-xml php-zip unzip curl
curl -O https://dl.min.io/server/minio/release/linux-amd64/minio
apt install -y python3-pip curl unzip jq git default-jre
pip3 install awscli --upgrade --break-system-packages
pip3 install awscli-local --break-system-packages
chmod +x minio
mv minio /usr/local/bin/
cd /
mkdir -p /data/s3
apt install -y composer
```

Instalado todo, vamos a iniciar el servidor configurando el usuario con sus credenciales para la `nube` local.

## Inicio del servidor de la nube local

```shell
MINIO_ROOT_USER=<USER> MINIO_ROOT_PASSWORD=<PASSWORD> minio server /data/s3 --console-address ":9001" &
```

Una vez con el servidor iniciado, vamos a configurar a nivel `local` las variables que vamos a necesitar para manipular dicho servidor:

## Variables de configuracion local para la nube

```shell
aws configure
```

Echo esto nos metera en un entorno de configuracion pidiendo los datos de los cuales hemos configurado anteriormente al iniciar el servidor.

```shell
# Access Key ID: <USER>
# Secret Access Key: <PASSWORD>
# Region: us-east-1
# Output format: json
```

Configurado esto, ya podremos interactuar con la `nube` local, por ejemplo vamos a crear una `politica` para el `bucket` el cual tambien vamos a crear, para que sea vulnerable.

## Crear un bucket para la nube local

```shell
aws --endpoint-url http://localhost:9000 s3api create-bucket --bucket <BUCKET_NAME>
```

> EJEMPLO:

```shell
aws --endpoint-url http://localhost:9000 s3api create-bucket --bucket huguelogistics-data
```

Con esto ya habremos creado el `bucket` por lo que vamos a configurarle una politica que permita que cualquier usuario de la nube local puede enumerar las politicas y se puede descargar cualquier archivo de dicho `bucket`.

## Creacion de politica vulnerable

```shell
cd /tmp
```

> public-policy.json

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowPublicReadPolicy",
      "Effect": "Allow",
      "Principal": "*",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket",
        "s3:GetBucketPolicy"
      ],
      "Resource": [
        "arn:aws:s3:::<BUCKET_NAME>",
        "arn:aws:s3:::<BUCKET_NAME>/*"
      ]
    }
  ]
}
```

> EJEMPLO CON EL NOMBRE:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowPublicReadPolicy",
      "Effect": "Allow",
      "Principal": "*",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket",
        "s3:GetBucketPolicy"
      ],
      "Resource": [
        "arn:aws:s3:::huguelogistics-data",
        "arn:aws:s3:::huguelogistics-data/*"
      ]
    }
  ]
}
```

Ahora una vez creado el archivo que cargaremos desde el `/tmp` lo cargaremos con este comando:

```shell
aws --endpoint-url http://localhost:9000 s3api put-bucket-policy --bucket huguelogistics-data --policy file:///tmp/public-policy.json
```

Una vez echo esto, podemos cargar algun archivo de prueba que tenga credenciales de usuarios o cualquier cosa, por ejemplo podriamos probar a crear un `.xlsx` con usuarios y contraseñas al `bucket` si tuvieramos un archivo de este estilo, lo podremos subir de esta forma:

## Subida de archivos al bucket

```shell
cd /tmp
touch <FILE_NAME>.xlsx
aws --endpoint-url http://localhost:9000 s3 cp <FILE_NAME>.xlsx s3://huguelogistics-data/
```

Ejecutando este comando habremos subido de forma correcta el archivo `.xlsx` al `bucket`, ahora desde una maquina atacante, se podria hacer lo siguiente.

## Vista desde un atacante

Probando de forma anonima a enumerar el `bucket` veremos esto:

```shell
aws --no-sign-request --endpoint-url http://<IP_VICTIM>:9000 s3api get-bucket-policy --bucket huguelogistics-data
```

Si lo queremos filtrar para ver mejor seria algo asi:

```shell
aws --no-sign-request --endpoint-url http://<IP>:9000 s3api get-bucket-policy --bucket huguelogistics-data | jq -r '.Policy | fromjson | .Statement[] | {Effect, Principal, Action, Resource, Sid}'
```

Info:

```
{
  "Effect": "Allow",
  "Principal": {
    "AWS": [
      "*"
    ]
  },
  "Action": [
    "s3:ListBucket",
    "s3:GetBucketPolicy",
    "s3:GetObject"
  ],
  "Resource": [
    "arn:aws:s3:::huguelogistics-data",
    "arn:aws:s3:::huguelogistics-data/*"
  ],
  "Sid": "AllowPublicReadPolicy"
}
```

Veremos que esta funcionando correctamente, por lo que sabiendo todo esto vamos a probar a descargarnos el archivo que subimos al servidor anteriormente de la `nube`.

```shell
aws --no-sign-request --endpoint-url http://<IP>:9000 s3 cp s3://huguelogistics-data/<FILE_NAME>.xlsx .
```

Y con esto veremos que ha funcionado toda la vulnerabilidad, ya que nos esta descargando el archivo de forma correcta.

## \[EXTRA] Configuracion en un Apache2

Si queremos alojar el `bucket` en un entorno `web` como por ejemplo con `apache2` podremos realizar lo siguiente:

```shell
apt install apache2
service apache2 start
cd /var/www/html
```

Ahora vamos a plasmar toda la configuracion en dicha pagina web:

```shell
composer require aws/aws-sdk-php
```

Vamos asignarle los permisos necesarios, junto con las configuraciones necesarias:

```shell
chmod -R 755 /var/www/html
chown -R www-data:www-data /var/www/html
a2enmod rewrite
service apache2 restart
apt-get install -y php-gd
composer require phpoffice/phpspreadsheet
```

Y ya con esto podremos implementar `PHP` como pagina web, para poder implementar sistemas de autenticacion, validaciones, etc... Con `PHP`.
