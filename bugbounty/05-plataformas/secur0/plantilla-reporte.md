# Plantilla de reporte — Secur0

Estos son los campos exactos del formulario **"Enviar reporte"** de Secur0.

## 📋 Información básica

```
Idioma del reporte
  → Selecciona el idioma en el que vas a redactar (ej. Español)

Título
  → (0/100 caracteres) Título descriptivo del reporte
    Ej: IDOR en API de gestión de empleados permite acceso no autorizado

Alcance
  → Alcance específico del reporte dentro del programa
    Ej: https://github.com/empresa-ejemplo/proyecto-crm

Endpoint (Opcional)
  → (0/500 caracteres) URL o endpoint afectado
    Ej: https://ejemplo-empresa.local/modulo/accion
```

## 📋 Detalle técnico

```
Detalle técnico
  → (0/5000 caracteres) Descripción detallada de la vulnerabilidad
    (equivalente al bloque "Vulnerability Details" de la plantilla genérica:
     CWE, causa raíz, componente afectado, por qué ocurre)

Payload
  → (0/20000 caracteres) Payload utilizado para reproducir la vulnerabilidad
    (aquí caben perfectamente comandos curl completos, scripts Python,
     JSON de request/response, etc. — el límite es generoso)

Impacto
  → (0/5000 caracteres) Impacto potencial de la vulnerabilidad
    (qué puede hacer un atacante real con esto, en términos de negocio)

Prueba de concepto
  → (0/5000 caracteres) Pasos para reproducir la vulnerabilidad
    (pasos numerados, claros, reproducibles por un tercero)
```

## 📋 Criticidad (Opcional)

```
Opciones:
  ○ Omitir criticidad
      → La criticidad será evaluada por el equipo del programa

  ○ Calcular automáticamente (Recomendado)
      → Usa la calculadora CVSS v4.0 integrada:

      Métricas de explotabilidad
        - Vector de ataque:          Red / Adyacente / Local / Físico
        - Complejidad del ataque:    Bajo / Alto
        - Requisitos del ataque:     Ninguno / Presente
        - Privilegios requeridos:    Ninguno / Bajo / Alto
        - Interacción del usuario:   Ninguno / Pasivo / Activo

      Métricas de impacto del sistema vulnerable
        - Confidencialidad:  Alto / Bajo / Ninguno
        - Integridad:        Alto / Bajo / Ninguno
        - Disponibilidad:    Alto / Bajo / Ninguno

      Métricas de impacto del sistema subsiguiente
        - Confidencialidad:  Alto / Bajo / Ninguno
        - Integridad:        Alto / Bajo / Ninguno
        - Disponibilidad:    Alto / Bajo / Ninguno

      → Genera una puntuación 0.0–10.0 automáticamente

  ○ Añadir manualmente
      → Introduces tú directamente la puntuación ya calculada
```

## 📋 Adjuntos y colaboradores

```
Adjuntos (Opcional)
  → Capturas, vídeos, logs (png, jpg, jpeg, gif, txt, mp4 — hasta 200MB)

Información Adicional y Sugerencia de Solución (Opcional)
  → (0/10000 caracteres) Contexto extra + recomendación de fix

Colaboradores (Opcional)
  → Reparto porcentual del bounty entre los distintos investigadores
    Ej: Tú 60% + Colaborador 40% = Total 100%
```

## ✅ Checklist antes de enviar en Secur0

- [ ] El título cabe en 100 caracteres y es descriptivo.
- [ ] El campo "Payload" incluye todos los comandos necesarios para reproducir sin tener que ir a buscarlos a otro lado.
- [ ] La "Prueba de concepto" está numerada y es autocontenida.
- [ ] Si colaboras con alguien, el reparto de porcentaje suma 100%.
- [ ] Adjuntaste capturas — y vídeo si el flujo tiene varios pasos encadenados.
