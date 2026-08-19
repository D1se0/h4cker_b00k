---
icon: square-terminal
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
  tags:
    visible: true
  actions:
    visible: true
---

# Prompts clave, plantilla por plantilla

Biblioteca de prompts que uso en cada fase del proceso. Los cuatro primeros son los que forman el ciclo principal (ver [Flujo de trabajo completo](flujo-de-trabajo-completo.md)); el resto son variaciones y prompts de apoyo que uso según la situación.

## 🚀 1. Prompt de inicio de sesión (investigación autónoma)

```
/goal Ahora lanza distintos agentes para ir probando distintas
vulnerabilidades y debes parar hasta encontrar alguna digna de
reportar
```

**Cuándo usarlo**: al empezar una sesión nueva sobre un programa ya configurado (con `CLAUDE.md`, `PROGRESS.md` y `RECON.md` ya existentes), o al retomar la investigación tras haber cerrado/reportado un hallazgo anterior.

## 🧪 2. Pedir guía de reproducción manual

```
Ahora quiero que me des la guía paso a paso para poder reproducirlo
manualmente yo y poder sacar las capturas correspondientes, para el
reporte posterior
```

**Cuándo usarlo**: en cuanto un agente reporta un hallazgo candidato. Nunca se salta este paso, aunque el agente "parezca muy seguro" — ver [¿Por qué usar IA para Bug Bounty?](por-que-usar-ia-bugbounty.md#️-lo-que-la-ia-no-hace-por-ti).

## 📝 3. Generar el reporte completo con capturas

```
Ya tienes las capturas en <PATH_IMAGES> quiero que me realices el
reporte implementando dichas capturas todo en inglés y que sigas la
estructura de example/ todo en markdown super detallado y que sea
fácil de reproducir por alguien que no entienda mucho
```

**Cuándo usarlo**: después de haber reproducido manualmente el hallazgo y guardado todas las capturas en `images/`.

## 📋 4. Rellenar los campos de la plataforma

```
Quiero que me rellenes los campos para poder reportar la
vulnerabilidad <PASAS_LOS_CAMPOS_DE_LA_PAGINA_ENTEROS> quiero que
me deposites los archivos correspondientes a los campos en temp/
con el nombre de la vulnerabilidad correspondiente para no confundirme
```

**Cuándo usarlo**: con el reporte ya redactado en `reportar/`, justo antes de ir a enviar en la plataforma correspondiente. Pega la estructura vacía de campos del formulario real (ver las [plantillas de plataforma](../bugbounty/05-plataformas/)).

***

## 🧭 Prompts de apoyo adicionales

### Retomar sesión tras un parón largo

```
Lee CLAUDE.md, PROGRESS.md y RECON.md y dame un resumen del estado
actual antes de continuar. No empieces a investigar todavía, solo
resume dónde lo dejamos.
```

Útil cuando ha pasado bastante tiempo y quieres refrescar tú mismo el contexto antes de decidir por dónde seguir, en vez de lanzar directamente el prompt de inicio autónomo.

### Pedir que un agente se centre en una clase de vulnerabilidad concreta

```
Lanza un agente centrado exclusivamente en probar IDOR/BOLA sobre
los endpoints de la API de [activo concreto], usando las cuentas de
prueba A y B ya existentes en PROGRESS.md. No toques ningún otro
activo del scope en este agente.
```

Refuerza el principio de "alcance acotado por agente" de [Agentes en paralelo](agentes-en-paralelo.md).

### Pedir una segunda verificación antes de dar algo por confirmado

```
Antes de darlo por confirmado, reproduce este hallazgo una segunda
vez desde cero, con una cuenta de prueba distinta si es posible, y
dime explícitamente si el resultado es consistente con la primera
reproducción.
```

Aplica el principio de "reproducir dos veces antes de tratarlo como real" de [Agentes en paralelo — Fase 2](agentes-en-paralelo.md#fase-2--explotación-y-verificación-en-serie).

### Pedir que argumente el CVSS

```
Ayúdame a calcular el CVSS de este hallazgo, razonando cada métrica
del vector una por una según lo que hemos confirmado en la
reproducción, no según el peor caso hipotético. Compara también con
los criterios de severidad propios del programa en CLAUDE.md.
```

Conecta con [Cálculo de severidad (CVSS)](../bugbounty/04-como-escribir-reportes/calculo-cvss.md).

### Pedir limpieza del repositorio al terminar

```
Hemos terminado por hoy. Limpia cualquier fichero o carpeta temporal
generada durante esta sesión que no sea CLAUDE.md, PROGRESS.md,
RECON.md, example/, images/, reportar/ o temp/. Actualiza PROGRESS.md
con el resumen de lo hecho hoy antes de terminar.
```

### Pedir un resumen de "qué queda por cubrir" del scope

```
Repasa RECON.md y PROGRESS.md y dime qué partes del scope todavía no
se han investigado en profundidad, priorizadas según la sección
"Estrategia de trabajo" de CLAUDE.md.
```

Muy útil para decidir hacia dónde apuntar la siguiente ronda de agentes en vez de dejarlo completamente a discreción del prompt de inicio genérico.

### Pedir que convierta el reporte de Markdown a PDF (cuando la plataforma lo exige)

```
Convierte el reporte de reportar/vulnN.md a PDF, manteniendo el
mismo formato y las capturas ya integradas, y guárdalo en temp/vulnN/
listo para adjuntar en el formulario de la plataforma.
```

***

## 🧱 Buenas prácticas al escribir tus propios prompts

* **Sé explícito con las rutas** (`images/`, `example/`, `temp/vulnN/`) — Claude Code trabaja directamente sobre el sistema de ficheros de tu proyecto, así que cuanto más preciso seas con dónde leer y dónde escribir, menos ambigüedad hay.
* **Referencia siempre tus propios archivos de contexto** (`CLAUDE.md`, `PROGRESS.md`, `RECON.md`, `example/`) en vez de repetir las reglas en cada prompt — es la ventaja principal de tenerlos bien escritos.
* **Divide en pasos pequeños y verificables**, como en el flujo de 4 prompts principal, en vez de pedir "investiga y repórtame todo" de una sola vez — así puedes intervenir y corregir el rumbo entre cada fase.
* **Usa `/goal` (o el modo autónomo equivalente) solo para las fases que quieres que corran sin supervisión constante** (recon, exploración inicial) — no para las fases de verificación y envío, donde quieres mantener control manual explícito.
