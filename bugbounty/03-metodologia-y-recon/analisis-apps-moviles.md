# Análisis de apps móviles (Android/iOS)

Las apps móviles son una fuente enorme de hallazgos porque **el binario que descargas contiene, literalmente, parte del "código fuente"** de cómo la app habla con el backend — incluyendo, a veces, cosas que nunca deberían estar ahí (tokens, claves de API, endpoints internos).

## 📦 Conseguir el APK/IPA

- Descarga directa desde tiendas alternativas públicas (APKPure, APKMirror, etc.) sin necesidad de cuenta.
- Extracción desde un dispositivo/emulador donde la tengas instalada.
- El propio Google Play, si tienes cuenta, con herramientas de extracción de APK instalado.

## 🔓 Desempaquetar

```bash
# Un XAPK es básicamente un ZIP que envuelve el APK base + configs
unzip app.xapk -d xapk_extracted
unzip xapk_extracted/com.empresa.app.apk -d apk_base
```

A partir de aquí tienes acceso a:

- `AndroidManifest.xml` → permisos, actividades, deep links.
- `assets/` y `res/` → recursos, y en apps React Native, el **bundle de JavaScript** (`index.android.bundle`).
- `classes.dex` → código compilado, descompilable con `jadx`/`apktool`.

## 🔍 Buscar secretos en texto plano

Muchísimas apps (sobre todo React Native/Hermes) guardan **cadenas de texto en claro** dentro del bundle JS, aunque esté "compilado". No siempre hace falta descompilar bytecode: a menudo con un simple `grep` sobre el bundle ya aparecen tokens, URLs internas o claves.

```bash
grep -a -o "Bearer eyJ[A-Za-z0-9_=.-]*" assets/index.android.bundle   # JWT
grep -a -oE "https?://[a-zA-Z0-9./_-]+" assets/index.android.bundle  # URLs / endpoints
grep -a -iE "(api[_-]?key|secret|token|password)" assets/index.android.bundle
```

> 💡 Ver el ejemplo real completo de esta técnica en [YesWeHack — JWT hardcodeado en app Android](../06-ejemplos-reales/yeswehack-jwt-hardcodeado.md).

## 🧬 Análisis dinámico (tráfico en tiempo real)

Para ver qué hace la app realmente al usarla:

1. Configura un proxy (Burp/mitmproxy) en el dispositivo o emulador.
2. Instala el certificado del proxy como CA de confianza.
3. Muchas apps modernas usan **SSL/Certificate Pinning**, que bloquea proxies no confiables — aquí es donde entra **Frida/Objection** para hacer bypass del pinning en runtime (siempre sobre tu propio dispositivo/emulador y dentro del scope permitido).
4. Con el tráfico ya visible, repite el mismo análisis que harías en web: ¿qué parámetros manda?, ¿hay identificadores manipulables?, ¿el backend valida realmente la propiedad de los recursos?

## ✅ Checklist rápida para apps móviles

- [ ] ¿Hay tokens/claves hardcodeadas en el bundle o en recursos?
- [ ] ¿El certificate pinning está bien implementado (o se puede saltar)?
- [ ] ¿Los endpoints usados por la app validan igual que la versión web (o son más laxos)?
- [ ] ¿Hay deep links (`intent-filter`) que se puedan abusar?
- [ ] ¿Se guardan datos sensibles sin cifrar en almacenamiento local (`SharedPreferences`, `Keychain`)?
- [ ] ¿La app confía ciegamente en datos que le manda el backend sin validarlos (o viceversa)?
