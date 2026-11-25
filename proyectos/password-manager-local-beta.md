---
icon: unlock
---

# Password Manager Local (BETA)

#### Documentación técnica y conceptual del proyecto (BETA)

***

### 📌 Visión general

**Password Manager Local** es un gestor de contraseñas **100% local**, diseñado con un enfoque claro en:

* **Seguridad**
* **Privacidad**
* **Control total del usuario**
* **Cero dependencias externas**

El proyecto nace como una alternativa a los gestores de contraseñas tradicionales basados en la nube, eliminando por completo servidores externos, sincronizaciones remotas o almacenamiento de datos fuera del dispositivo del usuario.

> ⚠️ **Estado actual**:\
> El proyecto se encuentra en **fase BETA**.\
> Las versiones funcionales se ejecutan en **modo desarrollador**.\
> El modo _release_ (producción) está en proceso de estabilización.

***

### 🎯 Objetivos del proyecto

* Garantizar que **ningún dato sensible salga del equipo**
* Aplicar **cifrado fuerte de nivel empresarial**
* Mantener una **arquitectura simple, auditable y transparente**
* Facilitar futuras mejoras y forks por parte de la comunidad
* Demostrar buenas prácticas en seguridad, frontend moderno y arquitectura local

***

### 🧩 Modos de uso disponibles

El proyecto cuenta actualmente con **dos modos principales de ejecución**, ambos completamente funcionales en **modo desarrollo**:

***

### 🌐 1. Aplicación Web (recomendada)

#### Descripción

Es la forma **más sencilla y estable** de usar el proyecto actualmente.

* Interfaz web moderna
* Backend local
* Todo se ejecuta en el propio equipo
* No hay tráfico externo

📌 **Recomendado para la mayoría de usuarios y testers**

***

#### Tecnologías utilizadas

**Frontend**

* TypeScript
* React 18
* Vite
* Framer Motion (animaciones fluidas)
* Estética **Glassmorphism**
* Blur y paleta de colores **morados / negros**
* UI oscura, moderna y elegante

**Backend**

* Node.js (v20.20.0)
* TypeScript
* Express
* SQLite3 (base de datos local)
* Arquitectura modular

***

#### Ejecución (modo desarrollo)

```
pnpm dev
```

Esto levanta automáticamente:

* Backend local (API REST)
* Frontend web en:

```
http://127.0.0.1:5173
```

Todo queda **automatizado mediante scripts** incluidos en el proyecto.

***

### 🖥️ 2. Aplicación de escritorio (Tauri)

#### Descripción

Versión **desktop** sin navegador, empaquetada con **Tauri**.

⚠️ **Estado**: funcional **solo en modo debug / dev**.\
El modo _release_ presenta problemas pendientes de resolver.

***

#### Tecnologías adicionales

* Tauri
* Rust (toolchain requerida)
* Cargo
* Build Tools de Visual Studio (C++)

***

#### Requisitos adicionales

Para ejecutar la versión de escritorio es necesario:

* Node.js v20.20.0
* pnpm
* Rust (stable)
* Visual Studio Build Tools (C++)
* Entorno de desarrollo correctamente configurado

***

#### Ejecución (modo desarrollo)

```
pnpm tauri dev
```

Este comando:

* Lanza frontend
* Lanza backend
* Inicia la app de escritorio en modo debug
* Todo queda integrado en un único flujo

***

### 🔐 Seguridad y criptografía

La seguridad es el **pilar central del proyecto**.

***

#### 🔑 Cifrado

* **AES-256-GCM**
* Derivación de claves con **PBKDF2**
* Uso de **salts únicos**
* Iteraciones altas para resistencia a ataques de fuerza bruta

***

#### 🧠 Gestión de la clave maestra

* La **master key nunca se guarda en disco**
* Solo reside en **RAM**
* Al cerrar la bóveda:
  * La clave se elimina
  * Se limpia la memoria
  * No queda rastro persistente

***

#### 🗄️ Base de datos

* SQLite3
* 100% local
* Políticas estrictas
* Ningún dato sensible en texto plano
* Campos cifrados individualmente

***

#### 🌐 Sin servidores externos

* No hay cloud
* No hay sincronización
* No hay tracking
* No hay APIs externas
* Todo el cifrado y descifrado se realiza **en el cliente**

***

### 🧱 Arquitectura técnica (resumen)

```
[ UI (React) ]
      ↓
[ API Local (Node.js) ]
      ↓
[ SQLite cifrado ]
```

* Separación clara de responsabilidades
* Código modular
* Fácil de auditar
* Fácil de extender

***

### 🧪 Estado del proyecto (BETA)

Actualmente:

* ✅ Funcional en modo desarrollo
* ⚠️ Modo release no estable
* 🧪 En pruebas continuas
* 🔧 Scripts automatizados incluidos
* 📦 Se proporcionan ZIPs del proyecto

***

### 🤝 Contribuciones y mejoras

Este proyecto está abierto a:

* Forks
* PRs
* Auditorías de seguridad
* Refactors
* Mejoras en Tauri / release
* Optimización de arquitectura

📌 **Repositorio oficial**:\
👉 [GitHub repositorio](https://github.com/D1se0/Aplicacion_Gestor_de_contrasenas_Windows)

📦 **ZIPs del proyecto**:\
👉 [Descargar ZIPs del proyecto](https://drive.google.com/drive/folders/1qw6QSZ9QkfNB5C1MpMMFTWk6aXOH1i4J?usp=sharing)

***

### 🖼️ Capturas de pantalla

<figure><img src="../.gitbook/assets/1.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/2.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/3.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/4.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/5.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/6.png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/7.png" alt=""><figcaption></figcaption></figure>

***

### 🧠 Motivación personal

Este proyecto no es solo una aplicación, sino un **ejercicio real de arquitectura segura**, frontend moderno y desarrollo consciente de la privacidad.

Está pensado como:

* Proyecto técnico
* Base para evolución futura
* Demostración de capacidades profesionales

***

### 📎 Notas finales

* No usar en producción crítica (BETA)
* Ideal para pruebas, auditoría y aprendizaje
* Cualquier feedback es bienvenido
