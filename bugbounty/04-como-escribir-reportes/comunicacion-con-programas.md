# Comunicación con los programas

## 🕰️ Qué esperar del ciclo de vida de un reporte

```
Enviado → New / Nuevo
   ↓
Under Review / Under Triage  (el equipo/triager lo está revisando)
   ↓
   ├── Need More Info / Necesita más información  →  (tú respondes)  →  vuelve a Under Review
   ├── Not Applicable / N/A  →  (rechazado, con explicación)
   ├── Duplicate  →  (ya reportado antes por otra persona)
   └── Accepted / Triaged / Valid  →  se pasa a la empresa para corregir
         ↓
      Resolved / Fixed  →  (a veces) Disclosed públicamente
```

## 💬 Cómo responder a un "Need More Info" (necesita más información)

Este estado **no es un rechazo**. Es, literalmente, el equipo dándote la oportunidad de reforzar tu hallazgo. Cómo responder bien:

1. **No te lo tomes como algo personal ni respondas a la defensiva.**
2. **Entiende exactamente qué están pidiendo.** ¿Piden más pasos? ¿Piden pruebas de impacto real? ¿Piden que confirmes algo que asumiste?
3. **Responde con evidencia nueva, no solo con más palabras.** Si piden impacto real, aporta una captura/JSON nuevo que lo demuestre de forma innegable.
4. **Si no puedes demostrar algo sin cruzar una línea ética/legal** (por ejemplo, tocar datos reales de un cliente), dilo explícitamente y ofrece una alternativa: pide al propio equipo que reproduzca el último paso con datos internos suyos, explicando exactamente qué comando ejecutar y qué comparar.
5. **Sé rápido respondiendo.** Los programas valoran mucho la agilidad de un investigador, y una respuesta tardía puede hacer que el reporte se enfríe o se archive.

> Ejemplo real de esta situación en [YesWeHack — JWT hardcodeado](../06-ejemplos-reales/yeswehack-jwt-hardcodeado.md): el equipo pidió pruebas de impacto real más allá de "un 200 en vez de un 401", y la respuesta fue aportar evidencia estructurada del propio JSON de la API (que demuestra una consulta real en base de datos), variar el identificador de entrada, comprobar ausencia de rate limiting, y ofrecer explícitamente al equipo un test interno que ellos mismos pudieran ejecutar sin que el investigador tuviera que cruzar la línea de tocar datos reales.

## 🙅 Cómo aceptar un "N/A" (No Aplica) con elegancia

- Lee la explicación completa antes de responder.
- Si no la entiendes, pregunta con educación y de forma concreta: "¿Podríais aclarar si X está intencionalmente permitido / fuera de scope?"
- Si sigues en desacuerdo con argumentos técnicos sólidos, puedes exponerlos una vez, de forma clara y sin repetir el mismo argumento en bucle.
- Evita la confrontación. La relación a largo plazo con un programa vale más que "ganar" una discusión puntual.

## 🤝 Buenas prácticas generales de comunicación

- Usa un tono profesional y neutro, incluso si el rechazo te parece injusto.
- Agradece al equipo su tiempo de revisión — cuesta poco y genera buena relación.
- Si trabajas en colaboración con otra persona, decláralo desde el principio (ver "Colaboradores" en las plantillas de plataforma).
- Si detectas por casualidad otra vulnerabilidad distinta mientras investigas esta, **no la mezcles en el mismo hilo** — abre un reporte nuevo.
- Guarda un histórico propio de tus interacciones con cada programa: te ayuda a calibrar su nivel de exigencia y estilo de comunicación para futuros reportes.
