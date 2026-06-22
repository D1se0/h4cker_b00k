# GitLab y otras plataformas de gestión de código

Las plataformas de gestión de código fuente (GitLab, Gitea, Gogs, Bitbucket Server) son objetivos de altísimo valor en auditorías de seguridad: contienen el código fuente completo de la organización, secretos y credenciales hardcodeadas en repositorios, tokens de acceso, y a menudo pipelines de CI/CD integrados que conectan directamente con entornos de producción.

## GitLab

GitLab Self-Managed es la instalación más extendida en entornos corporativos. Se despliega típicamente en el puerto 80/443.

**Fingerprinting:**
```bash
# Señales características
curl -I http://objetivo/ | grep -i "gitlab"
http://objetivo/users/sign_in    # Página de login estándar
http://objetivo/explore          # Explorador público (si está habilitado)

# La API de GitLab puede revelar información
curl http://objetivo/api/v4/version
```

**Vectores frecuentes:**

- **Registro abierto**: si GitLab está configurado para permitir registro público, cualquier persona puede crear una cuenta y acceder a repositorios marcados como "internos" (visibles para todos los usuarios autenticados, no solo los miembros del proyecto).
- **Repositorios públicos involuntarios**: repositorios que deberían ser privados pero están marcados como públicos — conteniendo código fuente, variables de entorno con credenciales, claves SSH, tokens de API.
- **Credenciales por defecto**: en instalaciones antiguas, `root:5iveL!fe` era la contraseña por defecto del administrador.
- **CVEs del core**: GitLab tiene un historial de vulnerabilidades graves — SSRF (usado para alcanzar servicios internos), RCE a través del procesamiento de archivos, y path traversal. La [base de datos de seguridad de GitLab](https://about.gitlab.com/security/security-releases/) publica avisos regularmente.

**Señales de alto valor durante un reconocimiento:**
- Repositorios con archivos `.env`, `config.yml`, `secrets.yml`, o similares
- Pipelines de CI/CD que contienen variables de entorno con credenciales
- Issues o commits que mencionan credenciales o tokens

## Gitea y Gogs

Plataformas más ligeras y frecuentes en entornos de desarrollo pequeños o herramientas internas.

```bash
# Fingerprinting
curl -s http://objetivo:3000/ | grep -i "gitea\|gogs"
http://objetivo:3000/explore/repos   # Repositorios públicos
```

El mismo patrón de riesgo que GitLab: registro abierto, repositorios públicos no deseados, y CVEs en versiones antiguas. Gitea en particular tiene un historial de vulnerabilidades de SSRF y path traversal en versiones sin actualizar.

## El vector de mayor impacto: secretos en repositorios

Independientemente de la plataforma, el hallazgo más frecuente y de mayor impacto en auditorías de plataformas de código es encontrar **secretos hardcodeados** en repositorios:

- Credenciales de base de datos en archivos de configuración commiteados
- Claves de AWS, tokens de API, claves privadas SSH
- Contraseñas de producción en scripts de despliegue
- Tokens de acceso de servicios externos

Herramientas como **truffleHog**, **gitleaks**, o **git-secrets** automatizan la búsqueda de patrones de secretos en el historial completo de commits — incluyendo secretos que fueron eliminados en commits posteriores pero siguen presentes en el historial de Git.

## Mitigación

- Deshabilitar el registro público si GitLab no necesita ser accesible externamente.
- Auditar la visibilidad de todos los repositorios — ninguno debería ser público por accidente.
- Implementar escaneo automático de secretos en los pipelines de CI/CD.
- Rotar cualquier credencial que haya sido commiteada, aunque se haya eliminado posteriormente (el historial de Git es permanente).
- Mantener GitLab y plataformas similares actualizadas — especialmente crítico para vulnerabilidades de SSRF y RCE.
- Restringir acceso por IP si la plataforma no necesita ser accesible desde internet.
