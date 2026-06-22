# Transferencia de zona DNS

## Qué es y para qué existe legítimamente

Una transferencia de zona (**AXFR**, *Full Zone Transfer*) es el mecanismo mediante el cual un servidor DNS secundario obtiene una copia completa de todos los registros de una zona desde el servidor primario, garantizando que ambos permanezcan sincronizados y aportando redundancia.

El flujo legítimo:

1. **Solicitud AXFR**: el servidor secundario pide al primario una transferencia completa.
2. **Registro SOA**: el primario responde con su registro *Start of Authority*, que incluye un número de serie para verificar si los datos del secundario están desactualizados.
3. **Transmisión de registros**: se envían todos los registros de la zona (A, AAAA, MX, CNAME, NS, etc.) uno por uno.
4. **Fin de transferencia** y **confirmación (ACK)** del secundario.

## Por qué esto es un problema de seguridad

El control de acceso sobre quién puede **solicitar** una transferencia de zona recae enteramente en la configuración del servidor DNS. En los primeros años de internet era común permitir transferencias a cualquier cliente, una práctica que simplificaba la administración pero que, mal configurada (o simplemente heredada de una configuración por defecto insegura), sigue apareciendo hoy en auditorías reales.

Si un servidor DNS mal configurado permite transferencias de zona a cualquiera, **cualquier persona** puede obtener una copia íntegra del archivo de zona — sin necesidad de fuerza bruta ni adivinar nada. Esto revela de golpe:

- **Todos los subdominios**, incluidos los que nunca se enlazan públicamente: servidores de desarrollo, paneles de administración, entornos internos.
- **Todas las direcciones IP** asociadas, ampliando directamente la superficie de ataque conocida.
- **Detalles de los servidores de nombres**, que pueden revelar el proveedor de hosting y posibles configuraciones incorrectas adicionales.

## Probando una transferencia de zona

```bash
dig axfr @servidor-de-nombres dominio.com
```

```bash
dig axfr @nsztm1.digi.ninja zonetransfer.me

zonetransfer.me.    7200 IN SOA  nsztm1.digi.ninja. robin.digi.ninja. 2019100801 ...
zonetransfer.me.    7200 IN MX   0 ASPMX.L.GOOGLE.COM.
zonetransfer.me.    7200 IN A    5.196.105.14
zonetransfer.me.    7200 IN NS   nsztm1.digi.ninja.
admin.zonetransfer.me ...
internal.zonetransfer.me ...
```

> `zonetransfer.me` es un dominio mantenido deliberadamente para fines educativos, configurado para permitir transferencias de zona y así demostrar de forma segura y legal cómo luce un volcado completo.

## Qué hacer con el resultado

Cada línea del volcado es un registro completo de la zona, lo que permite construir de un vistazo un inventario detallado de la infraestructura interna del dominio: subdominios administrativos, entornos internos, servidores de correo, e incluso direcciones IP de rangos internos que pueden no estar expuestas por ningún otro medio de reconocimiento. Conviene registrar sistemáticamente cada hostname y su IP asociada, ya que cada uno es un objetivo potencial independiente para fases posteriores de la auditoría.

## Mitigación

Los servidores DNS modernos, correctamente configurados, restringen las transferencias de zona exclusivamente a una lista explícita de servidores secundarios de confianza (mediante directivas como `allow-transfer` en BIND). A pesar de que la concienciación sobre esta vulnerabilidad ha aumentado considerablemente, los errores de configuración heredados o introducidos por fallo humano siguen apareciendo, lo que hace que **intentar siempre** una transferencia de zona (con la autorización adecuada) sea un paso de bajo coste y alto valor potencial en cualquier auditoría: incluso si falla, el propio rechazo confirma que el control de acceso está correctamente implementado, aportando información útil sobre la postura de seguridad del objetivo.
