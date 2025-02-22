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

# Changeme, Gitleaks y CyberChef

### Changeme

Primero vamos a ver la herramienta llamada `Changeme` que se encarga de buscar contraseñas por defecto en diferentes servicios que tenemos expuestos en nuestra infraestructura de red.

URL = [Changeme GitHub](https://github.com/ztgrace/changeme)

No viene por defecto en `kali`, por lo que tendremos que instalarlo de la siguiente forma:

```shell
sudo apt install changeme
```

Podemos utilizarla contra un `host` de la siguiente manera para intentar encontrar todos esos servicios o aplicaciones web en las que pueda tener credenciales por defecto.

```shell
changeme 192.168.5.211
```

Info:

```
 #####################################################
#       _                                             #
#   ___| |__   __ _ _ __   __ _  ___ _ __ ___   ___   #
#  / __| '_ \ / _` | '_ \ / _` |/ _ \ '_ ` _ \ / _ \\  #
# | (__| | | | (_| | | | | (_| |  __/ | | | | |  __/  #
#  \___|_| |_|\__,_|_| |_|\__, |\___|_| |_| |_|\___|  #
#                         |___/                       #
#  v1.2.3                                             #
#  Default Credential Scanner by @ztgrace             #
 #####################################################
    
Loaded 123 default credential profiles
Loaded 398 default credentials

No default credentials found
```

En este caso no va a encontrar nada ya que no tenemos puertos con credenciales por defecto.

### Gitleaks

Ahora vamos a ver la herramienta `Gitleaks` que estara en el siguiente repositorio:

URL = [Gitleaks GitHub](https://github.com/gitleaks/gitleaks)

Esta herramienta se utiliza para poder descubrir contraseñas de un repositorio de `GitHub`, pero no solo los `commits` actuales, si no tambien los antiguos, ya que era muy comun el echo de que un usuario colgara en `github` un archivo de configuracion en el que tuviera algunas credenciales o contraseñas `hardcodeadas` y cuando se diera cuenta lo eliminaba y hacia otro nuevo `commit` pero el anterior todavia se puede observar, pues esto es lo que hace esta herramienta realizar toda esta busqueda en busca de alguna clave o contraseña, no viene por defecto instalada en `kali` por lo que tendremos que realizar lo siguiente:

```shell
sudo apt install gitleaks
```

Una vez instalado, vamos a realizar la prueba con un repositorio llamado `mutillidae` que seria el siguiente link:

URL = [Mutillidae GitHub](https://github.com/webpwnized/mutillidae)

Y ahora vamos a utilizar la herramienta contra dicho repositorio de la siguiente forma:

```shell
git clone https://github.com/webpwnized/mutillidae
cd mutillidae
gitleaks detect -v
```

Info:

```

    ○
    │╲
    │ ○
    ○ ░
    ░    gitleaks

Finding:     $lSigningKey = 'MIIBPAIBAAJBANBs46xCKgSt8vSgpGlDH0C8znhqhtOZQQjFCaQzcseGCVlrbI';
Secret:      MIIBPAIBAAJBANBs46xCKgSt8vSgpGlDH0C8znhqhtOZQQjFCaQzcseGCVlrbI
RuleID:      generic-api-key
Entropy:     5.071053
File:        src/jwt.php
Line:        34
Commit:      04c309aa4b28720d7cc0569169d55b209fb03eac
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2024-10-18T14:10:15Z
Fingerprint: 04c309aa4b28720d7cc0569169d55b209fb03eac:src/jwt.php:generic-api-key:34

Finding:     var lPasswordCharset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
Secret:      ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789
RuleID:      generic-api-key
Entropy:     5.954196
File:        src/password-generator.php
Line:        49
Commit:      c9ff462f4405b921ecb6b2e96d7cb941ef6023af
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2024-10-08T21:10:28Z
Fingerprint: c9ff462f4405b921ecb6b2e96d7cb941ef6023af:src/password-generator.php:generic-api-key:49

Finding:     "hashed_secret": "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d",
Secret:      aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d
RuleID:      generic-api-key
Entropy:     3.646439
File:        .secrets.baseline
Line:        134
Commit:      e9e5328c79218612c1c120467b259afbf23c6082
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2024-10-04T17:41:53Z
Fingerprint: e9e5328c79218612c1c120467b259afbf23c6082:.secrets.baseline:generic-api-key:134

Finding:     "hashed_secret": "7c211433f02071597741e6ff5a8ea34789abbf43",
Secret:      7c211433f02071597741e6ff5a8ea34789abbf43
RuleID:      generic-api-key
Entropy:     3.762815
File:        .secrets.baseline
Line:        440
Commit:      e9e5328c79218612c1c120467b259afbf23c6082
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2024-10-04T17:41:53Z
Fingerprint: e9e5328c79218612c1c120467b259afbf23c6082:.secrets.baseline:generic-api-key:440

Finding:     "hashed_secret": "3c12d8b49a2185859491ef8c93545bac06b38051",
Secret:      3c12d8b49a2185859491ef8c93545bac06b38051
RuleID:      generic-api-key
Entropy:     3.715957
File:        .secrets.baseline
Line:        134
Commit:      35d173009b2ad59239b30d59fc06ce3e73152581
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2024-09-17T20:17:16Z
Fingerprint: 35d173009b2ad59239b30d59fc06ce3e73152581:.secrets.baseline:generic-api-key:134

Finding:     "hashed_secret": "390ae0493a4e75e69d26d908122c74dfabc89081",
Secret:      390ae0493a4e75e69d26d908122c74dfabc89081
RuleID:      generic-api-key
Entropy:     3.868454
File:        .secrets.baseline
Line:        143
Commit:      35d173009b2ad59239b30d59fc06ce3e73152581
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2024-09-17T20:17:16Z
Fingerprint: 35d173009b2ad59239b30d59fc06ce3e73152581:.secrets.baseline:generic-api-key:143

Finding:     "hashed_secret": "41ee220033b48e4399b8bf3abd8ec3abf34b451f",
Secret:      41ee220033b48e4399b8bf3abd8ec3abf34b451f
RuleID:      generic-api-key
Entropy:     3.568454
File:        .secrets.baseline
Line:        150
Commit:      35d173009b2ad59239b30d59fc06ce3e73152581
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2024-09-17T20:17:16Z
Fingerprint: 35d173009b2ad59239b30d59fc06ce3e73152581:.secrets.baseline:generic-api-key:150

Finding:     "hashed_secret": "77e30d2814eaa789641f196427dcd6c3f039e051",
Secret:      77e30d2814eaa789641f196427dcd6c3f039e051
RuleID:      generic-api-key
Entropy:     3.839823
File:        .secrets.baseline
Line:        159
Commit:      35d173009b2ad59239b30d59fc06ce3e73152581
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2024-09-17T20:17:16Z
Fingerprint: 35d173009b2ad59239b30d59fc06ce3e73152581:.secrets.baseline:generic-api-key:159

Finding:     "hashed_secret": "6b400726df61a3662c735b37fbc4b9443c11f24c",
Secret:      6b400726df61a3662c735b37fbc4b9443c11f24c
RuleID:      generic-api-key
Entropy:     3.615957
File:        .secrets.baseline
Line:        166
Commit:      35d173009b2ad59239b30d59fc06ce3e73152581
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2024-09-17T20:17:16Z
Fingerprint: 35d173009b2ad59239b30d59fc06ce3e73152581:.secrets.baseline:generic-api-key:166

Finding:     "hashed_secret": "12345a894e65f7517b0ac62226c5372d8e9d3781",
Secret:      12345a894e65f7517b0ac62226c5372d8e9d3781
RuleID:      generic-api-key
Entropy:     3.856198
File:        .secrets.baseline
Line:        173
Commit:      35d173009b2ad59239b30d59fc06ce3e73152581
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2024-09-17T20:17:16Z
Fingerprint: 35d173009b2ad59239b30d59fc06ce3e73152581:.secrets.baseline:generic-api-key:173

Finding:     "hashed_secret": "afe6b5701c1dc874f65b55a57e64e898dc64684f",
Secret:      afe6b5701c1dc874f65b55a57e64e898dc64684f
RuleID:      generic-api-key
Entropy:     3.665957
File:        .secrets.baseline
Line:        180
Commit:      35d173009b2ad59239b30d59fc06ce3e73152581
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2024-09-17T20:17:16Z
Fingerprint: 35d173009b2ad59239b30d59fc06ce3e73152581:.secrets.baseline:generic-api-key:180

Finding:     "hashed_secret": "eb359f56b6fe136d56c6e1bbc036d8750ce57c37",
Secret:      eb359f56b6fe136d56c6e1bbc036d8750ce57c37
RuleID:      generic-api-key
Entropy:     3.525070
File:        .secrets.baseline
Line:        187
Commit:      35d173009b2ad59239b30d59fc06ce3e73152581
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2024-09-17T20:17:16Z
Fingerprint: 35d173009b2ad59239b30d59fc06ce3e73152581:.secrets.baseline:generic-api-key:187

Finding:     "hashed_secret": "2fd3d703201b78d49b09b1fa0fcb3dd3dfec3d80",
Secret:      2fd3d703201b78d49b09b1fa0fcb3dd3dfec3d80
RuleID:      generic-api-key
Entropy:     3.550159
File:        .secrets.baseline
Line:        194
Commit:      35d173009b2ad59239b30d59fc06ce3e73152581
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2024-09-17T20:17:16Z
Fingerprint: 35d173009b2ad59239b30d59fc06ce3e73152581:.secrets.baseline:generic-api-key:194

Finding:     "hashed_secret": "e588744582118f5ba412b8f95cf6bdb775df63b0",
Secret:      e588744582118f5ba412b8f95cf6bdb775df63b0
RuleID:      generic-api-key
Entropy:     3.744589
File:        .secrets.baseline
Line:        203
Commit:      35d173009b2ad59239b30d59fc06ce3e73152581
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2024-09-17T20:17:16Z
Fingerprint: 35d173009b2ad59239b30d59fc06ce3e73152581:.secrets.baseline:generic-api-key:203

Finding:     "hashed_secret": "5e0f9abcad55a1eb2dcde00285ea2d2b9d96b300",
Secret:      5e0f9abcad55a1eb2dcde00285ea2d2b9d96b300
RuleID:      generic-api-key
Entropy:     3.572574
File:        .secrets.baseline
Line:        212
Commit:      35d173009b2ad59239b30d59fc06ce3e73152581
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2024-09-17T20:17:16Z
Fingerprint: 35d173009b2ad59239b30d59fc06ce3e73152581:.secrets.baseline:generic-api-key:212

Finding:     "hashed_secret": "74913f5cd5f61ec0bcfdb775414c2fb3d161b620",
Secret:      74913f5cd5f61ec0bcfdb775414c2fb3d161b620
RuleID:      generic-api-key
Entropy:     3.687326
File:        .secrets.baseline
Line:        219
Commit:      35d173009b2ad59239b30d59fc06ce3e73152581
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2024-09-17T20:17:16Z
Fingerprint: 35d173009b2ad59239b30d59fc06ce3e73152581:.secrets.baseline:generic-api-key:219

Finding:     "hashed_secret": "83bb2837d428a69beda67d8562fbf220e04d62d0",
Secret:      83bb2837d428a69beda67d8562fbf220e04d62d0
RuleID:      generic-api-key
Entropy:     3.625071
File:        .secrets.baseline
Line:        226
Commit:      35d173009b2ad59239b30d59fc06ce3e73152581
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2024-09-17T20:17:16Z
Fingerprint: 35d173009b2ad59239b30d59fc06ce3e73152581:.secrets.baseline:generic-api-key:226

Finding:     "hashed_secret": "5084602a0f6c6d69b90350357a2db815b566cc19",
Secret:      5084602a0f6c6d69b90350357a2db815b566cc19
RuleID:      generic-api-key
Entropy:     3.697085
File:        .secrets.baseline
Line:        233
Commit:      35d173009b2ad59239b30d59fc06ce3e73152581
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2024-09-17T20:17:16Z
Fingerprint: 35d173009b2ad59239b30d59fc06ce3e73152581:.secrets.baseline:generic-api-key:233

Finding:     "hashed_secret": "3c12d8b49a2185859491ef8c93545bac06b38051",
Secret:      3c12d8b49a2185859491ef8c93545bac06b38051
RuleID:      generic-api-key
Entropy:     3.715957
File:        .secrets.baseline
Line:        242
Commit:      35d173009b2ad59239b30d59fc06ce3e73152581
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2024-09-17T20:17:16Z
Fingerprint: 35d173009b2ad59239b30d59fc06ce3e73152581:.secrets.baseline:generic-api-key:242

Finding:     "hashed_secret": "de66cbee01a0c71498207e26805002c7e7040f5f",
Secret:      de66cbee01a0c71498207e26805002c7e7040f5f
RuleID:      generic-api-key
Entropy:     3.625071
File:        .secrets.baseline
Line:        251
Commit:      35d173009b2ad59239b30d59fc06ce3e73152581
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2024-09-17T20:17:16Z
Fingerprint: 35d173009b2ad59239b30d59fc06ce3e73152581:.secrets.baseline:generic-api-key:251

Finding:     "hashed_secret": "be4fc4886bd949b369d5e092eb87494f12e57e5b",
Secret:      be4fc4886bd949b369d5e092eb87494f12e57e5b
RuleID:      generic-api-key
Entropy:     3.673220
File:        .secrets.baseline
Line:        260
Commit:      35d173009b2ad59239b30d59fc06ce3e73152581
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2024-09-17T20:17:16Z
Fingerprint: 35d173009b2ad59239b30d59fc06ce3e73152581:.secrets.baseline:generic-api-key:260

Finding:     "hashed_secret": "9a9696f853f8d0877dc6f236a9a0ec4383b059d5",
Secret:      9a9696f853f8d0877dc6f236a9a0ec4383b059d5
RuleID:      generic-api-key
Entropy:     3.737326
File:        .secrets.baseline
Line:        269
Commit:      35d173009b2ad59239b30d59fc06ce3e73152581
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2024-09-17T20:17:16Z
Fingerprint: 35d173009b2ad59239b30d59fc06ce3e73152581:.secrets.baseline:generic-api-key:269

Finding:     "hashed_secret": "d4a46d37f9877a741117e8249d92d63a993d8e40",
Secret:      d4a46d37f9877a741117e8249d92d63a993d8e40
RuleID:      generic-api-key
Entropy:     3.535475
File:        .secrets.baseline
Line:        276
Commit:      35d173009b2ad59239b30d59fc06ce3e73152581
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2024-09-17T20:17:16Z
Fingerprint: 35d173009b2ad59239b30d59fc06ce3e73152581:.secrets.baseline:generic-api-key:276

Finding:     "hashed_secret": "8ae2994235b7c08d5d2b93b3831a4fef3ec29093",
Secret:      8ae2994235b7c08d5d2b93b3831a4fef3ec29093
RuleID:      generic-api-key
Entropy:     3.737326
File:        .secrets.baseline
Line:        283
Commit:      35d173009b2ad59239b30d59fc06ce3e73152581
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2024-09-17T20:17:16Z
Fingerprint: 35d173009b2ad59239b30d59fc06ce3e73152581:.secrets.baseline:generic-api-key:283

Finding:     "hashed_secret": "4c3054baf6d360c82a71ffc7e1dafa2784c1a9ed",
Secret:      4c3054baf6d360c82a71ffc7e1dafa2784c1a9ed
RuleID:      generic-api-key
Entropy:     3.856198
File:        .secrets.baseline
Line:        290
Commit:      35d173009b2ad59239b30d59fc06ce3e73152581
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2024-09-17T20:17:16Z
Fingerprint: 35d173009b2ad59239b30d59fc06ce3e73152581:.secrets.baseline:generic-api-key:290

Finding:     "hashed_secret": "db15ae43c53546da3da33a127fcc34d64ba13186",
Secret:      db15ae43c53546da3da33a127fcc34d64ba13186
RuleID:      generic-api-key
Entropy:     3.533783
File:        .secrets.baseline
Line:        297
Commit:      35d173009b2ad59239b30d59fc06ce3e73152581
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2024-09-17T20:17:16Z
Fingerprint: 35d173009b2ad59239b30d59fc06ce3e73152581:.secrets.baseline:generic-api-key:297

Finding:     "hashed_secret": "4b0d54823ef3fb1d7b49f273d6cae466fd47de4e",
Secret:      4b0d54823ef3fb1d7b49f273d6cae466fd47de4e
RuleID:      generic-api-key
Entropy:     3.718454
File:        .secrets.baseline
Line:        304
Commit:      35d173009b2ad59239b30d59fc06ce3e73152581
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2024-09-17T20:17:16Z
Fingerprint: 35d173009b2ad59239b30d59fc06ce3e73152581:.secrets.baseline:generic-api-key:304

Finding:     "hashed_secret": "637c8369257406fc9d74c0b8df1d4e8303664aac",
Secret:      637c8369257406fc9d74c0b8df1d4e8303664aac
RuleID:      generic-api-key
Entropy:     3.806198
File:        .secrets.baseline
Line:        313
Commit:      35d173009b2ad59239b30d59fc06ce3e73152581
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2024-09-17T20:17:16Z
Fingerprint: 35d173009b2ad59239b30d59fc06ce3e73152581:.secrets.baseline:generic-api-key:313

Finding:     "hashed_secret": "e875aada76e4eff92ddd55c84c81a84e90217518",
Secret:      e875aada76e4eff92ddd55c84c81a84e90217518
RuleID:      generic-api-key
Entropy:     3.675071
File:        .secrets.baseline
Line:        327
Commit:      35d173009b2ad59239b30d59fc06ce3e73152581
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2024-09-17T20:17:16Z
Fingerprint: 35d173009b2ad59239b30d59fc06ce3e73152581:.secrets.baseline:generic-api-key:327

Finding:     "hashed_secret": "aa9b2d59ba3c5e9308a640496cb9708fe4b6cea9",
Secret:      aa9b2d59ba3c5e9308a640496cb9708fe4b6cea9
RuleID:      generic-api-key
Entropy:     3.699582
File:        .secrets.baseline
Line:        334
Commit:      35d173009b2ad59239b30d59fc06ce3e73152581
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2024-09-17T20:17:16Z
Fingerprint: 35d173009b2ad59239b30d59fc06ce3e73152581:.secrets.baseline:generic-api-key:334

Finding:     "hashed_secret": "ec8aae3c54704bf2ff410f2ace955f60dfa9a983",
Secret:      ec8aae3c54704bf2ff410f2ace955f60dfa9a983
RuleID:      generic-api-key
Entropy:     3.780710
File:        .secrets.baseline
Line:        341
Commit:      35d173009b2ad59239b30d59fc06ce3e73152581
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2024-09-17T20:17:16Z
Fingerprint: 35d173009b2ad59239b30d59fc06ce3e73152581:.secrets.baseline:generic-api-key:341

Finding:     "hashed_secret": "7435c76a2794b5a23d34a1ba3d10c632c9ecec08",
Secret:      7435c76a2794b5a23d34a1ba3d10c632c9ecec08
RuleID:      generic-api-key
Entropy:     3.784830
File:        .secrets.baseline
Line:        357
Commit:      35d173009b2ad59239b30d59fc06ce3e73152581
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2024-09-17T20:17:16Z
Fingerprint: 35d173009b2ad59239b30d59fc06ce3e73152581:.secrets.baseline:generic-api-key:357

Finding:     "hashed_secret": "57bc04b0e482a3ad71adbe2f8f5d91c011771420",
Secret:      57bc04b0e482a3ad71adbe2f8f5d91c011771420
RuleID:      generic-api-key
Entropy:     3.787326
File:        .secrets.baseline
Line:        364
Commit:      35d173009b2ad59239b30d59fc06ce3e73152581
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2024-09-17T20:17:16Z
Fingerprint: 35d173009b2ad59239b30d59fc06ce3e73152581:.secrets.baseline:generic-api-key:364

Finding:     "hashed_secret": "aae8f38bd453f9d8860732e7bdb66a80f59a5526",
Secret:      aae8f38bd453f9d8860732e7bdb66a80f59a5526
RuleID:      generic-api-key
Entropy:     3.706198
File:        .secrets.baseline
Line:        371
Commit:      35d173009b2ad59239b30d59fc06ce3e73152581
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2024-09-17T20:17:16Z
Fingerprint: 35d173009b2ad59239b30d59fc06ce3e73152581:.secrets.baseline:generic-api-key:371

Finding:     "hashed_secret": "fca01d744d954284d5acbd1c111bd442ee478c73",
Secret:      fca01d744d954284d5acbd1c111bd442ee478c73
RuleID:      generic-api-key
Entropy:     3.631287
File:        .secrets.baseline
Line:        378
Commit:      35d173009b2ad59239b30d59fc06ce3e73152581
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2024-09-17T20:17:16Z
Fingerprint: 35d173009b2ad59239b30d59fc06ce3e73152581:.secrets.baseline:generic-api-key:378

Finding:     "hashed_secret": "ebdc7fbc6865266dc6db2b118df193123830b47a",
Secret:      ebdc7fbc6865266dc6db2b118df193123830b47a
RuleID:      generic-api-key
Entropy:     3.765957
File:        .secrets.baseline
Line:        387
Commit:      35d173009b2ad59239b30d59fc06ce3e73152581
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2024-09-17T20:17:16Z
Fingerprint: 35d173009b2ad59239b30d59fc06ce3e73152581:.secrets.baseline:generic-api-key:387

Finding:     "hashed_secret": "8fa8f4fcd1b98862f0a26551f87e01a95fcaa6a4",
Secret:      8fa8f4fcd1b98862f0a26551f87e01a95fcaa6a4
RuleID:      generic-api-key
Entropy:     3.649582
File:        .secrets.baseline
Line:        396
Commit:      35d173009b2ad59239b30d59fc06ce3e73152581
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2024-09-17T20:17:16Z
Fingerprint: 35d173009b2ad59239b30d59fc06ce3e73152581:.secrets.baseline:generic-api-key:396

Finding:     "hashed_secret": "6633843895c1bdc0369e45aa3ac486fa7987a21c",
Secret:      6633843895c1bdc0369e45aa3ac486fa7987a21c
RuleID:      generic-api-key
Entropy:     3.753702
File:        .secrets.baseline
Line:        405
Commit:      35d173009b2ad59239b30d59fc06ce3e73152581
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2024-09-17T20:17:16Z
Fingerprint: 35d173009b2ad59239b30d59fc06ce3e73152581:.secrets.baseline:generic-api-key:405

Finding:     "hashed_secret": "b630113eab920835f2e56fe1c2a84a23214d6bc9",
Secret:      b630113eab920835f2e56fe1c2a84a23214d6bc9
RuleID:      generic-api-key
Entropy:     3.806198
File:        .secrets.baseline
Line:        414
Commit:      35d173009b2ad59239b30d59fc06ce3e73152581
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2024-09-17T20:17:16Z
Fingerprint: 35d173009b2ad59239b30d59fc06ce3e73152581:.secrets.baseline:generic-api-key:414

Finding:     -----BEGIN RSA PRIVATE KEY-----                                 
MIISKgIBAAKCBAEAlH1pj1kxWhfJRazHPLmL+oXj3/vyXN9V6JgLE5gqFXMn+REc
mLf...                                                          -
Secret:      -----BEGIN RSA PRIVATE KEY-----                                 
MIISKgIBAAKCBAEAlH1pj1kxWhfJRazHPLmL+oXj3/vyXN9V6JgLE5gqFXMn+REc
mLf...                                                          
RuleID:      private-key
Entropy:     6.030921
File:        labs/lab-files/open-ssl-lab-files/private-key.pem
Line:        1
Commit:      55cd03eb0f76c7b23d6c53dd932555f83709f834
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2021-05-09T20:07:04Z
Fingerprint: 55cd03eb0f76c7b23d6c53dd932555f83709f834:labs/lab-files/open-ssl-lab-files/private-key.pem:private-key:1

Finding:     echo 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9tdXRpbGxpZGFlLmxvY2FsIiwiYXVkIjoiaHR0cDp... | cut -d. -f1 | bas...
Secret:      eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9tdXRpbGxpZGFlLmxvY2FsIiwiYXVkIjoiaHR0cDp...
RuleID:      jwt
Entropy:     5.666804
File:        includes/hints/jwt-hint.inc
Line:        46
Commit:      2b90452899ec9738e78412a6c078473775d71cca
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2021-04-12T20:38:03Z
Fingerprint: 2b90452899ec9738e78412a6c078473775d71cca:includes/hints/jwt-hint.inc:jwt:46

Finding:     echo 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9tdXRpbGxpZGFlLmxvY2FsIiwiYXVkIjoiaHR0cDp... | cut -d. -f1 | bas...
Secret:      eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9tdXRpbGxpZGFlLmxvY2FsIiwiYXVkIjoiaHR0cDp...
RuleID:      jwt
Entropy:     5.666804
File:        includes/hints/jwt-hint.inc
Line:        46
Commit:      4aae3da8d0dcd127997f446ac14c89da2def9be7
Author:      Jeremy Druin
Email:       webpwnized@users.noreply.github.com
Date:        2021-03-03T23:22:08Z
Fingerprint: 4aae3da8d0dcd127997f446ac14c89da2def9be7:includes/hints/jwt-hint.inc:jwt:46

Finding:     echo 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9tdXRpbGxpZGFlLmxvY2FsIiwiYXVkIjoiaHR0cDp... | cut -d. -f2 | bas...
Secret:      eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9tdXRpbGxpZGFlLmxvY2FsIiwiYXVkIjoiaHR0cDp...
RuleID:      jwt
Entropy:     5.666804
File:        includes/hints/jwt-hint.inc
Line:        50
Commit:      4aae3da8d0dcd127997f446ac14c89da2def9be7
Author:      Jeremy Druin
Email:       webpwnized@users.noreply.github.com
Date:        2021-03-03T23:22:08Z
Fingerprint: 4aae3da8d0dcd127997f446ac14c89da2def9be7:includes/hints/jwt-hint.inc:jwt:50

Finding:     echo 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9tdXRpbGxpZGFlLmxvY2FsIiwiYXVkIjoiaHR0cDp... > token
Secret:      eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9tdXRpbGxpZGFlLmxvY2FsIiwiYXVkIjoiaHR0cDp...
RuleID:      jwt
Entropy:     5.657828
File:        includes/hints/jwt-hint.inc
Line:        76
Commit:      4aae3da8d0dcd127997f446ac14c89da2def9be7
Author:      Jeremy Druin
Email:       webpwnized@users.noreply.github.com
Date:        2021-03-03T23:22:08Z
Fingerprint: 4aae3da8d0dcd127997f446ac14c89da2def9be7:includes/hints/jwt-hint.inc:jwt:76

Finding:     New Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOi8vbXV0aWxsaWRhZS5sb2NhbCIsImF1ZCI6Imh0dHA6Ly9...
Secret:      eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOi8vbXV0aWxsaWRhZS5sb2NhbCIsImF1ZCI6Imh0dHA6Ly9...
RuleID:      jwt
Entropy:     5.636582
File:        includes/hints/jwt-hint.inc
Line:        100
Commit:      4aae3da8d0dcd127997f446ac14c89da2def9be7
Author:      Jeremy Druin
Email:       webpwnized@users.noreply.github.com
Date:        2021-03-03T23:22:08Z
Fingerprint: 4aae3da8d0dcd127997f446ac14c89da2def9be7:includes/hints/jwt-hint.inc:jwt:100

Finding:     $lKey = 'MIIBPAIBAAJBANBs46xCKgSt8vSgpGlDH0C8znhqhtOZQQjFCaQzcseGCVlrbI';
Secret:      MIIBPAIBAAJBANBs46xCKgSt8vSgpGlDH0C8znhqhtOZQQjFCaQzcseGCVlrbI
RuleID:      generic-api-key
Entropy:     5.071053
File:        ajax/jwt.php
Line:        52
Commit:      063153c126b6e55dcc52307ee6cbbd576f34ac64
Author:      LucanSec
Email:       lucansilva@protonmail.com
Date:        2020-12-18T14:09:40Z
Fingerprint: 063153c126b6e55dcc52307ee6cbbd576f34ac64:ajax/jwt.php:generic-api-key:52

Finding:     $lKey = 'MIIBPAIBAAJBANBs46xCKgSt8vSgpGlDH0C8znhqhtOZQQjFCaQzcseGCVlrbI';
Secret:      MIIBPAIBAAJBANBs46xCKgSt8vSgpGlDH0C8znhqhtOZQQjFCaQzcseGCVlrbI
RuleID:      generic-api-key
Entropy:     5.071053
File:        jwt.php
Line:        32
Commit:      063153c126b6e55dcc52307ee6cbbd576f34ac64
Author:      LucanSec
Email:       lucansilva@protonmail.com
Date:        2020-12-18T14:09:40Z
Fingerprint: 063153c126b6e55dcc52307ee6cbbd576f34ac64:jwt.php:generic-api-key:32

Finding:     -----BEGIN PRIVATE KEY-----                                     
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQD5+8rWPBfpo2aj
hgOYAfI...                                                      -
Secret:      -----BEGIN PRIVATE KEY-----                                     
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQD5+8rWPBfpo2aj
hgOYAfI...                                                      
RuleID:      private-key
Entropy:     6.015054
File:        data/mutillidae-selfsigned.key
Line:        1
Commit:      86396b7f3716821f280a5b7a79c6e6fca1b9e982
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2020-04-14T00:08:07Z
Fingerprint: 86396b7f3716821f280a5b7a79c6e6fca1b9e982:data/mutillidae-selfsigned.key:private-key:1

Finding:     if ($lAuthor == "53241E83-76EC-4920-AD6D-503DD2A6BA68" || strlen($lAuthor)...
Secret:      53241E83-76EC-4920-AD6D-503DD2A6BA68
RuleID:      generic-api-key
Entropy:     3.829240
File:        view-someones-blog.php
Line:        169
Commit:      0f9d4a66f2540f5154c01476e81161935aad6291
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2018-09-28T02:48:39Z
Fingerprint: 0f9d4a66f2540f5154c01476e81161935aad6291:view-someones-blog.php:generic-api-key:169

Finding:     if ($lAuthor == "6C57C4B5-B341-4539-977B-7ACB9D42985A"){
Secret:      6C57C4B5-B341-4539-977B-7ACB9D42985A
RuleID:      generic-api-key
Entropy:     3.593400
File:        view-someones-blog.php
Line:        172
Commit:      0f9d4a66f2540f5154c01476e81161935aad6291
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2018-09-28T02:48:39Z
Fingerprint: 0f9d4a66f2540f5154c01476e81161935aad6291:view-someones-blog.php:generic-api-key:172

Finding:     }// end if ($lAuthor == "53241E83-76EC-4920-AD6D-503DD2A6BA68" || strlen($lAuthor)...
Secret:      53241E83-76EC-4920-AD6D-503DD2A6BA68
RuleID:      generic-api-key
Entropy:     3.829240
File:        view-someones-blog.php
Line:        234
Commit:      0f9d4a66f2540f5154c01476e81161935aad6291
Author:      webpwnized
Email:       webpwnized@gmail.com
Date:        2018-09-28T02:48:39Z
Fingerprint: 0f9d4a66f2540f5154c01476e81161935aad6291:view-someones-blog.php:generic-api-key:234

3:32AM INF 733 commits scanned.
3:32AM INF scan completed in 2.65s
3:32AM WRN leaks found: 51
```

Y por lo que vemos nos ha sacado varias cosas interesante, entre ellas bastantes claves.

### CyberChef

Vamos con la ultima herramienta llamada `CyberChef` que se encuentra en el siguiente repositorio:

URL = [CyberChef GitHub](https://github.com/gchq/CyberChef)

Pero tambien lo tenemos en una aplicacion web que seria en el siguiente link:

URL = [Aplicacion web CyberChef](https://gchq.github.io/CyberChef/)

Esta herramienta sirve para poder codificar o decodificar `hashes` de diferentes formatos y es muy buena la pagina, tenemos muchisimos formatos a elegir y podemos configurarlo de forma muy avanzada a nuestro gusto.

Y ya no solo sirve para `crackear` si no que podremos pasar letras mayusculas a minusculas y vicebersa, tambien podremos detectar expresiones regulares de cualquier texto, podremos hacer muchisimas mas cosas con esta herramienta, esta muy completa.
