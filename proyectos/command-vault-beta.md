---
icon: terminal
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

# Command Vault (BETA)

Documentación Técnica – BETA

Repositorio de `GitHub` donde esta subido el proyecto: [GitHub Command\_Vault](https://github.com/D1se0/Command_Vault)

***

### 1. Visión General

**Command Vault** es una aplicación web local diseñada para almacenar, organizar y reutilizar comandos utilizados habitualmente en:

* Hacking ético
* Pruebas de penetración
* Operaciones Red Team y Blue Team
* Administración de sistemas
* Flujos de trabajo DevOps

El objetivo del proyecto es crear una **base de datos de comandos rápida y offline**, optimizada para el uso diario de usuarios técnicos que reutilizan comandos constantemente en distintos entornos y tecnologías.

Este proyecto se encuentra actualmente en **BETA** y en desarrollo activo.

#### Capturas del proyecto

<figure><img src="../.gitbook/assets/1 (3).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/2 (3).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/3 (3).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/4 (2).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/5 (3).png" alt=""><figcaption></figcaption></figure>

***

### 2. Filosofía y Motivación

Durante pentests reales, CTFs, auditorías o tareas de administración, los ingenieros reutilizan comandos de forma constante:

* Snippets de enumeración
* Ayudas para explotación
* One-liners
* Plantillas de payloads
* Helpers de automatización

Normalmente estos comandos terminan:

* Dispersos en notas
* Perdidos en historiales de chat
* Duplicados en múltiples herramientas

**Command Vault** nace para solucionar esto ofreciendo:

* Una base de datos estructurada de comandos
* Organización clara por workspaces y secciones
* Acceso rápido sin servicios externos
* Ejecución completamente local

El proyecto está construido **por y para hackers**, con la productividad y la simplicidad como principios fundamentales.

***

### 3. Características Principales

* Interfaz web local
* Organización por workspaces
* Agrupación de comandos por secciones
* Bloques de código con resaltado de sintaxis
* Resaltado de sintaxis en tiempo real al editar
* Soporte multi-lenguaje (bash, PowerShell, Python, etc.)
* Arquitectura offline-first
* Sin dependencias cloud
* Despliegue portable y sencillo

***

### 4. Visión General de la Arquitectura

El proyecto sigue una **arquitectura local cliente-servidor**:

```
┌──────────────┐
│   Navegador  │
│  (Frontend)  │
└──────┬───────┘
       │ HTTP (localhost)
┌──────▼───────┐
│   Backend    │
│  Node + API  │
└──────┬───────┘
       │
┌──────▼───────┐
│   BD Local   │
│  SQLite / FS │
└──────────────┘
```

Todo se ejecuta **de forma local** en la máquina del usuario.

***

### 5. Stack Tecnológico

#### Frontend

* **React**
* **TypeScript**
* **Vite**
* **Framer Motion**
* **React Syntax Highlighter**
* **Sistema UI personalizado**

Responsabilidades:

* Renderizado de la interfaz
* Edición de comandos
* Resaltado de sintaxis
* Interacción con el usuario

***

#### Backend

* **Node.js**
* **TypeScript**
* **API REST**
* **Base de datos local**

Responsabilidades:

* Persistencia de datos
* CRUD de Workspaces / Secciones / Comandos
* Exposición de la API

***

#### Principios de Desarrollo

* Tipado fuerte (TypeScript en todo el proyecto)
* Dependencias mínimas
* Lógica explícita
* Sin abstracciones mágicas
* Código hackeable y extensible

***

### 6. Modelo de Datos

#### Workspace

Representa un agrupador lógico (proyecto, cliente, laboratorio, categoría).

```ts
Workspace {
  id: string
  name: string
}
```

***

#### Section

Se utiliza para agrupar comandos dentro de un workspace.

```ts
Section {
  id: string
  workspace_id: string
  title: string
  icon: string        // clave del icono, no el glyph
  position: number
}
```

Los iconos se almacenan como **claves**, no como SVG ni Unicode, permitiendo flexibilidad en la UI.

***

#### Command

Representa un comando o snippet reutilizable.

```ts
Command {
  id: string
  section_id: string
  title: string
  description: string
  language: string
  command: string
  position: number
  updated_at: string
}
```

***

### 7. Sistema de Iconos

Los iconos se gestionan mediante un **sistema basado en claves**:

* La capa de datos almacena claves de iconos:

```ts
"terminal" | "folder" | "sections" | ...
```

* La capa UI resuelve los iconos dinámicamente:

```tsx
{Icons[s.icon as keyof typeof Icons]}
```

Esto evita acoplar los datos a recursos visuales y facilita cambios futuros.

***

### 8. Resaltado de Sintaxis

#### Modo Lectura

Los comandos se renderizan usando **resaltado de sintaxis basado en Prism** con un tema personalizado:

* Fondo transparente
* Contraste afinado
* Optimizado para interfaces oscuras

***

#### Modo Edición (Resaltado en Vivo)

Al editar un comando:

* Un `<textarea>` transparente captura la entrada
* Una capa inferior renderiza el código con colores
* El cursor permanece visible
* El resaltado se actualiza en tiempo real según el lenguaje seleccionado

Esto proporciona una **experiencia tipo terminal**, sin editores pesados.

***

### 9. Estilos y Diseño de UI

La interfaz sigue estos principios:

* Fondos oscuros y de bajo contraste
* Glassmorphism sutil
* Ruido visual mínimo
* Enfoque en la legibilidad
* Diseño amigable con teclado

Se presta especial atención a:

* Alineación icono + texto
* Comportamiento del scroll
* Legibilidad del código
* Contraste en comentarios y tokens de sintaxis

***

### 10. Instalación (BETA)

#### Requisitos

* Windows (objetivo actual de la BETA)
* Node.js (instalado automáticamente mediante script `install.bat`)
* Navegador moderno

***

#### Instalación Portable

1. Descargar la release en ZIP
2. Extraer en cualquier ubicación
3. Ejecutar `run.bat`
4. El navegador se abrirá automáticamente en:

```
http://localhost:5173
```

El backend se ejecuta en segundo plano.

Sin servicios cloud, sin cuentas, sin telemetría.

***

### 11. Estado Actual (BETA)

* Incluye **comandos de ejemplo únicamente**
* Se utilizan para validar:
  * La UI
  * El modelo de datos
  * El flujo de edición
* Aún no es una base de datos completa

La librería de comandos se **ampliará de forma continua** en futuras releases.

***

### 12. Roadmap

Mejoras planificadas:

* Base de datos de comandos más amplia y curada
* Funciones de importación / exportación
* Filtrado por tags
* Mejora del sistema de búsqueda
* Plantillas y placeholders
* Builds multiplataforma
* Sistema de plugins (a largo plazo)

***

### 13. Contribución y Feedback

El proyecto está abierto a:

* Feedback
* Ideas
* Aportes de comandos
* Mejoras de UI
* Reporte de bugs

Incluso pequeñas contribuciones ayudan a dar forma al futuro de la herramienta.

***

### 14. Notas Finales

Command Vault está construido con la misma mentalidad que el hacking:

* Aprender haciendo
* Mejorar continuamente
* Compartir conocimiento
* Construir herramientas que realmente se usan

Si utilizas comandos a diario, esta herramienta está pensada para ti.
