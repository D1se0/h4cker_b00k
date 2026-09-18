---
icon: envelope
---

# El Servicio de Correo Electrónico

> El correo es el servicio más veterano de Internet y **la puerta de entrada favorita del atacante** (phishing). Entender cómo viaja un email te permite montar el tuyo gratis, saber si un dominio puede recibir spoofing y detectar correos falsos. En este capítulo: la teoría + cómo gestionar el correo **de tu propio dominio sin pagar nada**.

***

## ¿Cómo funciona el correo? Los 3 protagonistas

| Protocolo | Puerto                                                                   | Función                                                                      |
| --------- | ------------------------------------------------------------------------ | ---------------------------------------------------------------------------- |
| **SMTP**  | 25 (servidor↔servidor), 587 (cliente→servidor con STARTTLS), 465 (SMTPS) | **Enviar** correo                                                            |
| **IMAP**  | 143 (STARTTLS) / 993 (TLS)                                               | **Leer** correo dejándolo en el servidor (sincroniza múltiples dispositivos) |
| **POP3**  | 110 / 995                                                                | **Descargar** el correo al dispositivo (normalmente lo borra del servidor)   |

> 💡 Regla fácil: **SMTP = salida**, **IMAP/POP3 = lectura**. IMAP si usas el correo en móvil y PC a la vez.

### El viaje de un email

1. Escribes un correo a `destinatario@dominio.com` desde `gmail.com`.
2. Tu cliente habla con el servidor SMTP de Gmail (puerto 587, con autenticación).
3. Gmail consulta el **registro MX de `dominio.com`** → "¿quién recibe el correo de este dominio?".
4. El servidor SMTP de Gmail **entrega** el mensaje al servidor MX del destino (puerto 25).
5. El destinatario lo lee por IMAP/POP3 o webmail.

> 🔑 Aquí está la clave de todo: **el registro MX es quien decide qué servidor recibe el correo de un dominio**. Si controlas el DNS de un dominio, controlas su correo.

### 🎯 Para el hacker ético

* `nslookup -type=mx dominio.com` te dice qué proveedor de correo usa el objetivo (Google Workspace, M365, un Exchange propio...) → filtra qué exploits y phishing aplican.
* Un dominio **sin SPF/DKIM/DMARC** configurados es un dominio que se puede **suplantar** fácilmente desde cualquier servidor SMTP propio.
* Los puertos 25/587 abiertos en un servidor del objetivo son superficie de ataque: relay abierto, enumeración de usuarios (`VRFY`, `EXPN`), fuerza bruta de cuentas.

***

## Los registros que protegen (o exponen) tu dominio

Estos tres registros TXT son el escudo anti-spoofing del correo:

### SPF (Sender Policy Framework)

Declara **qué IPs/servidores tienen permiso para enviar correo** en nombre del dominio.

```
ejemplo.com.  IN TXT  "v=spf1 include:_spf.google.com -all"
```

* `include:` delega en el SPF de otro proveedor.
* `~all` (softfail): sospechoso pero no bloqueado. `-all` (hardfail): rechazar todo lo demás. `+all`: ¡todo permitido! (terrible configuración, muy rara hoy).

### DKIM (DomainKeys Identified Mail)

Firma criptográfica: el servidor de salida firma el correo con clave privada; el receptor verifica la clave pública publicada en el DNS.

```
selector._domainkey.ejemplo.com.  IN TXT  "v=DKIM1; k=rsa; p=MIIBI..."
```

### DMARC (Domain-based Message Authentication, Reporting & Conformance)

La política que le dice al receptor **qué hacer** si SPF/DKIM fallan:

```
_dmarc.ejemplo.com.  IN TXT  "v=DMARC1; p=reject; rua=mailto:dmarc@ejemplo.com"
```

* `p=none` → no hagas nada (débil), `p=quarantine` → a spam, `p=reject` → rechazar.

> 🎯 **Herramienta favorita en recon:** `dig txt _dmarc.dominio.com` en segundos te dice si puedes spoofear el dominio del objetivo. Si no hay DMARC con `p=reject`, un email firmado desde un servidor propio con su nombre en el "From" llega a bandeja con mucha más frecuencia.

***

## Monta tu propio servidor de correo (gratis)

¿Por qué? **Para no pagar ninguno** — tener `tucorreo@tudominio.com` con control total, sin límites de envío ni lectura de un tercero. Opciones reales en 2026:

### Opción A — Servidor completo propio (nivel medio-avanzado)

Software todo-en-uno que instala SMTP+IMAP+webmail+SPF/DKIM/DMARC automáticamente:

| Software             | Notas                                            |
| -------------------- | ------------------------------------------------ |
| **Mailcow** (Docker) | El más popular; panel web bonito; consumo medio  |
| **Mail-in-a-Box**    | Ubuntu 22.04, muy didáctico, casi sin configurar |
| **iRedMail**         | Ligero, compatible con casi cualquier VPS        |
| **Stalwart**         | Escrito en Rust, moderno, todo en un binario     |

Requisitos y pasos generales:

1. **VPS con IP propia limpia** (no en listas negras — comprueba la IP en [mxtoolbox.com](https://mxtoolbox.com/blacklists.aspx) y [mail-tester.com](https://www.mail-tester.com)).
2. **Dominio propio** y acceso a su DNS.
3. Registros DNS a crear:
   * `A` → `mail.tudominio.com` → IP del VPS
   * `MX` → `tudominio.com` → `mail.tudominio.com` (prioridad 10)
   * `SPF` → `v=spf1 mx -all`
   * `DKIM` → lo genera el propio servidor al instalarlo (publícalo en `_domainkey`)
   * `DMARC` → `v=DMARC1; p=quarantine; rua=mailto:admin@tudominio.com`
   * `PTR` (DNS inverso) → el proveedor del VPS te deja configurarlo: debe apuntar la IP a `mail.tudominio.com`. **Sin PTR correcto, los grandes proveedores te rechazan.**
4. **Puertos 25, 465, 587 y 993 abiertos** en el firewall del VPS (algunos proveedores/hosting casero bloquean el 25 de salida — averígualo antes).
5. Instala (p. ej. `curl -sSL https://get.mailcow.email | bash`), accede al panel, crea el dominio y los buzones.

### Opción B — Solo recepción + envío vía API (nivel fácil)

Si solo quieres `algo@tudominio.com` sin servidor:

* **Recepción gratis:** Cloudflare Email Routing o ImprovMX → reenvía `algo@tudominio.com` a tu Gmail.
* **Envío gratis:** la API SMTP de Resend/Brevo/Amazon SES con el dominio verificado.

> 💡 **Para el hacker ético:** montar tu propio servidor es el mejor ejercicio para entender SMTP de verdad. Y cuando audites, prueba: `nc dominio.com 25` → `VRFY admin`, `EXPN root`, `RCPT TO:` para enumerar usuarios válidos (con `smtp-user-enum` o Metasploit `smtp_enum`).

***

## Leer el correo desde la terminal

```bash
# Cliente TUI moderno
neomutt

# Probar una entrega SMTP a mano (así funciona por dentro)
openssl s_client -starttls smtp -crlf -connect mail.ejemplo.com:587
HELO test.com
MAIL FROM: <test@test.com>
RCPT TO: <destino@ejemplo.com>
DATA
Subject: Prueba

Hola
.
QUIT
```

> 🎯 Esta conversación SMTP "a mano" con `nc`/`openssl` es exactamente lo que hace cualquier herramienta de phishing rudimentaria. Entenderla = entender cómo se falsifica un remitente.

***

## Anti-spam y seguridad del lado receptor

| Mecanismo         | Qué hace                                                                           |
| ----------------- | ---------------------------------------------------------------------------------- |
| **Greylisting**   | Rechaza el primer intento con "try again later"; los spammers serios no reintentan |
| **RBL/DNSBL**     | Comprueba si la IP emisora está en listas negras                                   |
| **Rate limiting** | Limita correos por IP/cuenta                                                       |
| **Bayes / ML**    | Clasificación estadística del contenido                                            |

Para el atacante esto significa: primero entrega 1 correo de prueba, espera, y no envíes en ráfagas desde una IP recién estrenada.

***

## Resumen rápido

* **SMTP envía** (25/587/465), **IMAP lee sincronizando** (993), **POP3 descarga** (995).
* El registro **MX** decide qué servidor recibe el correo del dominio.
* **SPF + DKIM + DMARC** son el trío anti-spoofing: su ausencia = dominio suplantables.
* Servidor propio gratis: Mailcow/Mail-in-a-Box + dominio + DNS bien configurado (incluido PTR).
* En hacking: enumeración de usuarios por SMTP, dominios sin DMARC para spoofing, y SMTP a mano con `nc`.

**Siguiente capítulo →** [03 · Direccionamiento IP](03-direccionamiento-ip.md)
