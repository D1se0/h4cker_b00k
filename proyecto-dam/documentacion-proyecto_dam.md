---
icon: file-lines
---

# Documentación PROYECTO\_DAM

## 🛡️ Sistema de Autenticación - Backend con Flask + Flet + PostgreSQL (PYTHON)

Este módulo implementa un sistema de autenticación de usuarios para una aplicación híbrida que combina **Flet (Python)** como interfaz gráfica inicial, **Flask** como `API REST`, y **JWT (JSON Web Tokens)** para el manejo seguro de sesiones. Además, se utiliza **PostgreSQL** como sistema gestor de base de datos.

### ⚙️ Tecnologías utilizadas

* **Python** `>=3.9`
* **Flet** – Para crear la interfaz de login y registro.
* **Flask** – Framework para la creación de endpoints backend.
* **PostgreSQL** – Base de datos para el almacenamiento de usuarios.
* **JWT** – Tokens seguros para mantener sesiones activas.
* **Werkzeug** – Hash de contraseñas.
* **CORS** – Compartición de cookies entre Flask y otras apps (como Java frontend).
* **UUID** – Identificadores únicos para cookies de sesión.

***

### 📁 Estructura general del proyecto

El código se divide en dos partes principales:

1. **Interfaz Flet**:
   * Permite al usuario registrarse e iniciar sesión.
   * Muestra mensajes de error o éxito.
   * Lanza peticiones HTTP a los endpoints de Flask.
2. **API Flask**:
   * `/login`: Inicia sesión y establece una cookie `token`.
   * `/actualizar-datos`: Permite actualizar perfil y contraseña, tanto en la base de datos como en el token.
   * `/logout`: Elimina la cookie del navegador y de la base de datos.

***

### 🔐 Proceso de Autenticación

#### Registro de Usuario

* Se validan los campos del formulario.
* Se genera una cookie única con `uuid`.
* La contraseña se guarda **hasheada** con `generate_password_hash()`.
* Se inserta en la base de datos `appusers.usuarios`.

```python
register_user(conn, nombre, apellidos, email, usuario, password)
```

***

#### Login de Usuario

* Se permite autenticarse por **usuario** o **email**.
* Si el usuario existe y la contraseña coincide, se genera un **token JWT**.
* El token contiene:
  * ID, nombre, email, rol, cookie, último login.
  * Expira en **1 hora**.
* Se guarda el token en una cookie segura y `httponly`.

```python
token = generate_token(user_data)
response.set_cookie("token", token, httponly=True, max_age=3600, samesite="Strict")
```

***

#### Actualización de Datos (`/actualizar-datos`)

* El frontend Java accede a este endpoint para editar:
  * Nombre, apellidos, email, usuario.
* Contraseña (requiere la actual para validarlo).
* Se actualiza la base de datos y se **regenera el token JWT**.
* La cookie antigua se mantiene, pero el token se renueva.

***

#### Logout (`/logout`)

* Elimina la cookie `token` del navegador.
* Elimina también la cookie asociada al usuario en la base de datos.
* Redirige al login.

```python
response.set_cookie("token", "", max_age=0)
remove_cookie_from_db(cookie)
```

***

#### 🗂 **Endpoint `/eliminar-cuenta`**

📁 **Ubicación:** Backend Flask – rutas de usuario\
🔍 **Propósito:** Eliminar completamente la cuenta de un usuario autenticado.\
🧠 **Responsabilidad principal:** Validar la identidad del usuario mediante un token, eliminar su cuenta de la base de datos y limpiar su sesión eliminando la cookie.\
🛡 **Autenticación:** Requiere token JWT válido enviado como cookie.\
💾 **Tabla involucrada:** `usuarios`\
🔐 **Método HTTP:** `GET`

**Pasos clave del flujo:**

* **Obtener `userId` desde la URL:**\
  Extrae el ID del usuario a eliminar desde los parámetros de la query (`request.args.get("userId")`).\
  Si no se proporciona, devuelve un error `400`.
* **Validación del token JWT:**\
  Extrae el token de la cookie del navegador (`request.cookies.get("token")`).\
  Si falta o es inválido (usando `verify_token(token)`), devuelve un error `400` o `403`.
* **Conexión a la base de datos y eliminación:**\
  Se conecta a la base de datos PostgreSQL y ejecuta un `DELETE FROM usuarios WHERE id = %s`.\
  Si el usuario existe y se elimina correctamente (`cursor.rowcount > 0`), se continúa.
* **Eliminación de la cookie de sesión:**\
  Crea una respuesta de redirección al login y elimina la cookie `token` del navegador:

```python
response.set_cookie("token", "", max_age=0)
```

* **Redirección final:**\
  El usuario es redirigido al login (`http://localhost:30050/`).

**Código destacado:**

```python
response.set_cookie("token", "", max_age=0)
cursor.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
```

📌 **Nota:**

El endpoint gestiona errores de forma clara, devolviendo mensajes informativos ante fallos en parámetros, autenticación o conexión a base de datos.

***

### 🧠 Seguridad y Buenas Prácticas

* Las contraseñas se almacenan **encriptadas** (`hash`).
* Los JWT tienen una duración limitada (`1h`).
* Las cookies son `httponly` y `samesite=strict`.
* Se verifica la validez del token en cada endpoint sensible.

***

### 🧩 Bases de Datos

#### Base de datos: `appusers`

Contiene la tabla `usuarios`:

| Campo           | Tipo      | Descripción                          |
| --------------- | --------- | ------------------------------------ |
| id              | SERIAL    | Clave primaria                       |
| nombre          | TEXT      | Nombre del usuario                   |
| apellidos       | TEXT      | Apellidos del usuario                |
| email           | TEXT      | Correo electrónico                   |
| usuario         | TEXT      | Nombre de usuario único              |
| password\_hash  | TEXT      | Contraseña encriptada                |
| cookie          | UUID      | Token de sesión interno              |
| rol             | TEXT      | Rol del usuario (por defecto `user`) |
| estado          | BOOLEAN   | Estado de la cuenta                  |
| fecha\_registro | TIMESTAMP | Fecha de creación                    |
| ultimo\_login   | TIMESTAMP | Último acceso                        |

***

### 🖼️ Interfaz con Flet

Flet permite mostrar una interfaz web simple:

* Registro de nuevos usuarios.
* Inicio de sesión.
* Redirección a `animation.jsp` del sistema Java tras iniciar sesión.

***

### 🧪 Ejecución del sistema

1. Inicia la app de Flask en un hilo:

```python
threading.Thread(target=run_flask, daemon=True).start()
```

2. Arranca la interfaz Flet:

```python
ft.app(target=flet_app, view=ft.WEB_BROWSER, port=30050)
```

3. El puerto `5000` queda disponible para peticiones desde Java u otros `frontends`.

***

### 📬 Endpoints disponibles

| Endpoint            | Método   | Descripción                                    |
| ------------------- | -------- | ---------------------------------------------- |
| `/login`            | GET/POST | Inicia sesión y genera una cookie con el token |
| `/actualizar-datos` | POST     | Actualiza el perfil del usuario autenticado    |
| `/logout`           | POST     | Cierra la sesión y elimina la cookie           |
| `/eliminar-cuenta`  | GET      | Elimina la cuenta del usuario mediante el ID   |

***

### 📌 Notas

* Este sistema sirve como backend **para aplicaciones Java** (por ejemplo, desde JSP).
* Las cookies compartidas permiten mantener sesiones cruzadas entre **Flask y Java**.
* Ideal para separar lógica de autenticación del sistema principal.

### 🧱 **Estructura del Proyecto Java Web (JSP/Servlets + Flask Backend)**

***

#### 🔌 **1. Conexión a Base de Datos**

* **`main/java/conexionDDBB/ConexionDDBB.java`**\
  Clase responsable de establecer la conexión con la base de datos.\
  📌 _Conectada a servicios de backend denominados "Hackend"._

***

#### 🧠 **2. Lógica de Negocio – Controladores**

Estos controladores (Servlets y clases Java) gestionan la interacción entre la vista (JSPs) y la base de datos o el backend de Flask. Todos requieren autenticación mediante token JWT.

* **`ActualizarPerfilServlet.java`**\
  Actualiza los datos del usuario autenticado. Se comunica con un endpoint en Flask.
* **`AgregarLaboratorioControlador.java`**\
  Permite al usuario con rol _Designer_ insertar nuevos laboratorios en la base de datos.
* **`FotoControlador.java`**\
  Gestiona operaciones de foto de perfil: subir, modificar y eliminar.
* **`LogControlador.java`**\
  Encargado de registrar eventos del sistema (auditoría, seguridad, etc.).
* **`LogoutServlet.java`**\
  Maneja el cierre de sesión invocando un endpoint Flask.
* **`ValidateFlagControlador.java`**\
  Valida la bandera del laboratorio (para verificar si fue resuelto correctamente por el usuario).

***

#### 🗃️ **3. Acceso a Datos – DAOs**

Implementan el acceso a base de datos para cada componente del sistema. Separan la lógica de persistencia del resto del código.

* **`FotoDAO.java` / `FotoPerfilDAO.java`**\
  Gestionan la obtención, inserción y modificación de las fotos de perfil del usuario en la base de datos.
* **`LaboratorioDAO.java`**\
  Realiza operaciones sobre los datos de los laboratorios (crear, listar, etc.).
* **`ValidateFlagDAO.java`**\
  Accede a los datos necesarios para validar los flags enviados por los usuarios en cada laboratorio.

***

#### 🧰 **4. Utilidades**

* **`JWTUtils.java`**\
  Contiene lógica para crear, verificar o manejar tokens JWT.
* **`UsuariosJWT.java`**\
  Extrae la información del usuario contenida en un token JWT (como nombre, rol, id, etc.).

***

#### 🎨 **5. Vista – JSP, CSS, JS, Recursos Estáticos**

Las páginas JSP son el frontend del sistema. Se combinan con CSS/JS y recursos estáticos para la experiencia de usuario.\
**Acceso restringido mediante JWT.**

**📄 Páginas JSP**

* **`animation.jsp`** – Página de animación al abrir el navegador.
* **`editarPerfil.jsp`** – Permite al usuario autenticado editar su perfil.
* **`profile.jsp`** – Muestra la información del perfil del usuario.
* **`home_directory/*.jsp`** – Páginas de navegación principales (Home, Page1 a Page4).
* **`labs/foro-xss.jsp`** – Laboratorio para pruebas de XSS.
* **`labs/hackend.jsp`** – Página informativa relacionada con el backend Flask.
* **`labs/none.jsp`** – Página de “en construcción” para laboratorios no implementados.

**🎨 CSS**

* `animation.css`, `editarPerfilUpdate.css`, `foro-xss.css`, `home.css`, `profileUpdate.css`\
  Archivos de estilo asociados a sus respectivas vistas JSP.

**💻 JS**

* `animation.js`, `foro-xss.js`, `home.js`\
  Scripts que complementan la interacción de usuario en las páginas específicas.

**🖼️ Recursos**

* **`main/webapp/img/`** – Carpeta de imágenes usadas por el sistema (íconos, avatares, ilustraciones, etc.).

***

### 🔐 Seguridad

* **⚠️ Todas las páginas y endpoints están protegidos por validación de token JWT.**
* La validación ocurre tanto en el frontend (para acceso visual) como en el backend (para procesar las acciones).

## DOCUMENTACIÓN APLICACION JAVA (CODIGO)

### 🔌 `ConexionDDBB.java`

📁 **Ubicación**: `main/java/conexionDDBB/`\
🧠 **Función**: Gestiona la conexión y desconexión con la base de datos PostgreSQL.

#### ✨ Descripción

Esta clase encapsula la lógica necesaria para conectarse a una base de datos PostgreSQL. Carga el driver al iniciar y ofrece métodos públicos para abrir y cerrar la conexión.

#### 📄 Código Documentado

```java
package conexionDDBB;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

/**
 * Clase encargada de establecer y cerrar la conexión con la base de datos PostgreSQL.
 */
public class ConexionDDBB {
    // Datos de conexión
    private static final String DRIVER = "org.postgresql.Driver";
    private static final String URL = "jdbc:postgresql://localhost:5432/hackend";
    private static final String USER = "postgres";
    private static final String PASSWORD = "1234";

    private Connection conexion = null;

    // Carga del driver al inicializar la clase
    static {
        try {
            Class.forName(DRIVER);
        } catch (ClassNotFoundException e) {
            System.err.println("Error al cargar el driver de la base de datos.");
            e.printStackTrace();
        }
    }

    /**
     * Establece una conexión con la base de datos.
     * @return Objeto Connection si la conexión fue exitosa, null si falló.
     */
    public Connection conectar() {
        try {
            conexion = DriverManager.getConnection(URL, USER, PASSWORD);
            System.out.println("Conexión a BBDD OK");
        } catch (SQLException e) {
            System.err.println("Error en la conexión a BBDD");
            e.printStackTrace();
        }
        return conexion;
    }

    /**
     * Cierra la conexión activa con la base de datos.
     */
    public void cerrarConexion() {
        try {
            if (conexion != null && !conexion.isClosed()) {
                conexion.close();
                System.out.println("¡¡Conexión con BBDD cerrada!!");
            }
        } catch (SQLException e) {
            System.err.println("Error al cerrar la BBDD");
            e.printStackTrace();
        }
    }
}
```

***

### 🔐 `ActualizarPerfilServlet.java`

📁 **Ubicación**: `main/java/controlador/`\
🧠 **Función**: Servlet encargado de actualizar los datos del usuario a través de un endpoint en Flask, usando JWT para autenticación.

#### ✨ Descripción

Este servlet procesa solicitudes POST desde un formulario JSP (`editarPerfil.jsp`) para actualizar los datos del perfil del usuario autenticado. Extrae el token JWT desde una cookie, lo valida, y envía los datos al backend Flask. Si se recibe un nuevo token tras la actualización, lo reemplaza en las cookies activas del navegador.

#### 📄 Código Documentado

```java
package controlador;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureException;
import org.json.JSONObject;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;
import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;

/**
 * Servlet que gestiona la actualización de los datos del usuario.
 * Valida el JWT, recoge los datos del formulario y los envía a Flask.
 */
@WebServlet("/actualizarPerfil")
public class ActualizarPerfilServlet extends HttpServlet {

    private static final String SECRET_KEY = "clave_super_secreta";

    /**
     * Procesa la solicitud POST para actualizar el perfil.
     */
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String token = null;

        // Extrae el token desde las cookies
        Cookie[] cookies = request.getCookies();
        if (cookies != null) {
            for (Cookie cookie : cookies) {
                if ("token".equals(cookie.getName())) {
                    token = cookie.getValue();
                    break;
                }
            }
        }

        // Verificación básica del token
        if (token == null || token.isEmpty()) {
            response.sendRedirect("editarPerfil.jsp?mensaje=Error: Token no proporcionado");
            return;
        }

        String userId = null;
        try {
            // Validación del JWT
            Claims claims = Jwts.parser()
                    .setSigningKey(SECRET_KEY.getBytes())
                    .parseClaimsJws(token)
                    .getBody();
            userId = claims.getSubject();
        } catch (SignatureException e) {
            response.sendRedirect("editarPerfil.jsp?mensaje=Error: Token no válido");
            return;
        } catch (Exception e) {
            response.sendRedirect("editarPerfil.jsp?mensaje=Error: No se pudo verificar el token");
            return;
        }

        // Recolección de parámetros del formulario
        String nombre = request.getParameter("nombre");
        String apellidos = request.getParameter("apellidos");
        String email = request.getParameter("email");
        String usuario = request.getParameter("usuario");
        String currentPassword = request.getParameter("currentPassword");
        String newPassword = request.getParameter("newPassword");
        String confirmNewPassword = request.getParameter("confirmNewPassword");

        // Validación de nuevas contraseñas
        if (newPassword != null && !newPassword.isEmpty() && !newPassword.equals(confirmNewPassword)) {
            response.sendRedirect("editarPerfil.jsp?mensaje=Las contraseñas no coinciden");
            return;
        }

        try {
            // Envío de datos al backend Flask
            URL url = new URL("http://localhost:5000/actualizar-datos");
            HttpURLConnection con = (HttpURLConnection) url.openConnection();
            con.setRequestMethod("POST");
            con.setRequestProperty("Content-Type", "application/json");
            con.setRequestProperty("Cookie", "token=" + token);
            con.setDoOutput(true);

            // Construcción del cuerpo JSON
            JSONObject json = new JSONObject();
            json.put("nombre", nombre);
            json.put("apellidos", apellidos);
            json.put("email", email);
            json.put("usuario", usuario);
            json.put("currentPassword", currentPassword);
            json.put("newPassword", newPassword);

            // Envío del cuerpo JSON
            try (OutputStream os = con.getOutputStream()) {
                byte[] input = json.toString().getBytes("utf-8");
                os.write(input, 0, input.length);
            }

            // Lectura de la respuesta
            BufferedReader br = new BufferedReader(new InputStreamReader(con.getInputStream(), "utf-8"));
            StringBuilder responseText = new StringBuilder();
            String line;
            while ((line = br.readLine()) != null) {
                responseText.append(line.trim());
            }

            JSONObject jsonResponse = new JSONObject(responseText.toString());
            String nuevoToken = jsonResponse.getString("token");

            // Elimina la cookie vieja
            Cookie cookieAntigua = new Cookie("token", "");
            cookieAntigua.setMaxAge(0);
            cookieAntigua.setPath("/");
            response.addCookie(cookieAntigua);

            // Añade la cookie nueva con el nuevo token
            Cookie nueva = new Cookie("token", nuevoToken);
            nueva.setHttpOnly(true);
            nueva.setPath("/");
            nueva.setMaxAge(3600); // 1 hora
            response.addCookie(nueva);

            // Redirige al perfil
            response.sendRedirect("profile.jsp");

        } catch (Exception e) {
            e.printStackTrace();
            response.sendRedirect("editarPerfil.jsp?mensaje=Error: No se pudo actualizar el perfil.");
        }
    }
}
```

### 🧪 `AgregarLaboratorioControlador.java`

📁 **Ubicación**: `main/java/controlador/`\
🧠 **Función**: Gestiona la lógica para agregar un nuevo laboratorio desde un formulario en la interfaz.

#### ✨ Descripción

Este servlet se encarga de procesar el formulario para registrar un nuevo laboratorio en el sistema. Valida que los puntos sean un número entero positivo antes de insertar la información en la base de datos mediante `LaboratorioDAO`.

#### 📄 Código Documentado

```java
package controlador;

import dao.LaboratorioDAO;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;
import java.io.IOException;

/**
 * Servlet que maneja la creación de nuevos laboratorios.
 */
@WebServlet("/agregarLaboratorio")
public class AgregarLaboratorioControlador extends HttpServlet {
    private static final long serialVersionUID = 1L;

    /**
     * Procesa solicitudes POST desde el formulario para crear un nuevo laboratorio.
     */
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        // Obtener parámetros del formulario
        String nombre = request.getParameter("nombre");
        String flag = request.getParameter("flag");
        String puntosStr = request.getParameter("puntos");

        String mensaje;

        try {
            // Validar que puntos sea un número positivo
            int puntos = Integer.parseInt(puntosStr);
            if (puntos <= 0) {
                mensaje = "Los puntos deben ser un número positivo.";
            } else {
                // Llamada al DAO para insertar el laboratorio
                boolean exito = LaboratorioDAO.agregarLaboratorio(nombre, flag, puntos);
                mensaje = exito ? "Laboratorio agregado con éxito." : "Hubo un error al agregar el laboratorio.";
            }
        } catch (NumberFormatException e) {
            mensaje = "Los puntos deben ser un número válido.";
        }

        // Redirigir con mensaje a la vista JSP
        request.setAttribute("mensaje", mensaje);
        request.getRequestDispatcher("designer/agregarLaboratorio.jsp").forward(request, response);
    }
}
```

***

### 🖼️ `FotoControlador.java`

📁 **Ubicación**: `main/java/controlador/`\
🧠 **Función**: Maneja la subida o eliminación de la foto de perfil de un usuario.

#### ✨ Descripción

Este servlet permite a los usuarios subir o eliminar su foto de perfil. Valida el archivo recibido (nombre, formato y extensión) y lo guarda en el directorio `/uploads`. Luego, actualiza la ruta de la imagen en la base de datos mediante el `FotoPerfilDAO`.

#### 📄 Código Documentado

```java
package controlador;

import dao.FotoPerfilDAO;

import javax.servlet.ServletException;
import javax.servlet.annotation.MultipartConfig;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;
import java.io.File;
import java.io.IOException;

/**
 * Servlet que permite a los usuarios subir o eliminar su foto de perfil.
 */
@WebServlet("/SubirFotoPerfil")
@MultipartConfig
public class FotoControlador extends HttpServlet {
    private static final long serialVersionUID = 1L;

    /**
     * Procesa solicitudes POST para subir o eliminar fotos de perfil.
     */
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String userId = request.getParameter("user_id");
        if (userId == null || userId.isEmpty()) {
            response.sendError(HttpServletResponse.SC_BAD_REQUEST, "ID de usuario no proporcionado.");
            return;
        }

        // Eliminar foto si se especificó
        if (request.getParameter("eliminar") != null) {
            FotoPerfilDAO.eliminarFoto(userId, getServletContext());
            response.sendRedirect("profile.jsp");
            return;
        }

        // Procesar subida de nueva imagen
        Part filePart = request.getPart("profilePhoto");
        String fileName = extractFileName(filePart);

        if (fileName == null || fileName.isEmpty()) {
            response.sendError(HttpServletResponse.SC_BAD_REQUEST, "No se proporcionó una foto de perfil.");
            return;
        }

        // Validar extensión del archivo
        String fileExtension = getFileExtension(fileName).toLowerCase();
        if (!fileExtension.equals("png") && !fileExtension.equals("jpg") && !fileExtension.equals("jpeg")) {
            response.sendError(HttpServletResponse.SC_BAD_REQUEST, "Solo se permiten archivos .png, .jpg o .jpeg.");
            return;
        }

        // Ruta de almacenamiento
        String relativePath = "uploads";
        String absolutePath = getServletContext().getRealPath(relativePath);

        File uploadDir = new File(absolutePath);
        if (!uploadDir.exists()) {
            uploadDir.mkdirs();
        }

        String uploadPath = absolutePath + File.separator + fileName;

        try {
            filePart.write(uploadPath);
        } catch (IOException e) {
            e.printStackTrace();
            response.sendError(HttpServletResponse.SC_INTERNAL_SERVER_ERROR, "Error al guardar el archivo.");
            return;
        }

        // Actualiza la referencia en la base de datos
        FotoPerfilDAO.actualizarFoto(userId, "uploads/" + fileName);

        response.sendRedirect("profile.jsp");
    }

    /**
     * Extrae el nombre real del archivo desde el encabezado 'content-disposition'.
     */
    private String extractFileName(Part part) {
        String contentDisposition = part.getHeader("content-disposition");
        for (String cd : contentDisposition.split(";")) {
            if (cd.trim().startsWith("filename")) {
                return cd.substring(cd.indexOf('=') + 2, cd.length() - 1);
            }
        }
        return null;
    }

    /**
     * Obtiene la extensión del archivo a partir del nombre.
     */
    private String getFileExtension(String fileName) {
        int dotIndex = fileName.lastIndexOf('.');
        return dotIndex == -1 ? "" : fileName.substring(dotIndex + 1);
    }
}
```

### 📄 `LogControlador.java`

📁 **Ubicación**: `main/java/controlador/`\
🧠 **Función**: Mostrar el archivo de logs de Eclipse en el navegador, útil para depuración en desarrollo.

#### ✨ Descripción

Este servlet permite acceder desde el navegador al contenido del archivo `.log` de Eclipse ubicado en el workspace del usuario. Es especialmente útil para desarrolladores al momento de revisar excepciones o errores recientes sin necesidad de abrir Eclipse.

#### 📄 Código Documentado

```java
package controlador;

import javax.servlet.*;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;
import java.io.*;
import java.nio.file.*;

/**
 * Servlet que expone el contenido del archivo .log de Eclipse en formato HTML.
 */
@WebServlet("/getLogs")
public class LogControlador extends HttpServlet {
    /**
     * Muestra el contenido del archivo de log .metadata/.log del workspace de Eclipse.
     */
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String logFilePath = System.getProperty("user.home") + "/eclipse-workspace/.metadata/.log";
        File logFile = new File(logFilePath);

        if (logFile.exists() && logFile.isFile()) {
            try (BufferedReader reader = Files.newBufferedReader(logFile.toPath())) {
                StringBuilder logContent = new StringBuilder();
                String line;
                while ((line = reader.readLine()) != null) {
                    logContent.append(line).append("<br>");
                }

                response.setContentType("text/html");
                response.getWriter().write(logContent.toString());
            }
        } else {
            response.getWriter().write("No se puede acceder al archivo de log.");
        }
    }
}
```

> ⚠️ **Nota**: Este servlet no debe estar activo en producción, ya que expone información sensible del entorno de desarrollo.

***

### 🔐 `LogoutServlet.java`

📁 **Ubicación**: `main/java/controlador/`\
🧠 **Función**: Cierra la sesión del usuario tanto en el sistema Java como en el backend Flask, y elimina el token de autenticación.

#### ✨ Descripción

Este servlet maneja el proceso de cierre de sesión del usuario. Invalida la sesión actual, borra la cookie del token JWT y realiza una llamada HTTP al backend Flask para invalidar la sesión desde ese lado también. Finalmente, redirige al frontend (ejecutado con Flet) para que el usuario vea la pantalla de login.

#### 📄 Código Documentado

```java
package controlador;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;
import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

/**
 * Servlet que maneja el cierre de sesión del usuario.
 */
@WebServlet("/logout")
public class LogoutServlet extends HttpServlet {
    private static final long serialVersionUID = 1L;

    /**
     * Invalida la sesión actual, elimina la cookie y comunica el cierre al backend Flask.
     */
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        // Extraer el token desde las cookies
        String token = null;
        Cookie[] cookies = request.getCookies();
        if (cookies != null) {
            for (Cookie cookie : cookies) {
                if ("token".equals(cookie.getName())) {
                    token = cookie.getValue();
                    break;
                }
            }
        }

        if (token != null && !token.isEmpty()) {
            // Invalida sesión en el servidor Java
            HttpSession session = request.getSession(false);
            if (session != null) {
                session.invalidate();
            }

            // Eliminar la cookie de autenticación
            Cookie authCookie = new Cookie("token", "");
            authCookie.setMaxAge(0);
            authCookie.setPath("/");
            response.addCookie(authCookie);

            // Llamar al backend Flask para cerrar la sesión ahí también
            try {
                HttpClient client = HttpClient.newHttpClient();
                HttpRequest flaskRequest = HttpRequest.newBuilder()
                        .uri(URI.create("http://localhost:5000/logout"))
                        .header("Cookie", "token=" + token)
                        .POST(HttpRequest.BodyPublishers.noBody())
                        .build();

                HttpResponse<String> flaskResponse = client.send(flaskRequest, HttpResponse.BodyHandlers.ofString());

                if (flaskResponse.statusCode() == 200) {
                    System.out.println("Sesión cerrada correctamente en backend Flask.");
                } else {
                    System.out.println("Error al cerrar sesión en Flask: código " + flaskResponse.statusCode());
                }

            } catch (Exception e) {
                System.out.println("Error llamando al backend Flask: " + e.getMessage());
            }
        }

        // Redirigir al login de Flet (frontend)
        response.sendRedirect("http://localhost:30050");
    }
}
```

### 🏁 `ValidateFlagControlador.java`

📁 **Ubicación**: `main/java/controlador/`\
🧠 **Función**: Validar si una flag ingresada por el usuario es correcta para un laboratorio específico.

#### ✨ Descripción

Este servlet se encarga de validar flags en retos del tipo CTF (Capture The Flag). Usa JWT para identificar al usuario, verifica si ya ha validado la flag, y si no lo ha hecho, comprueba si la flag ingresada es correcta. Si lo es, registra la validación en la base de datos y asigna los puntos correspondientes.

#### 📄 Código Documentado

```java
package controlador;

import dao.LaboratorioDAO;
import dao.ValidateFlagDAO;
import utils.JWTUtils;
import utils.UsuarioJWT;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.*;
import java.io.IOException;

/**
 * Servlet que valida una flag ingresada por el usuario para un laboratorio específico.
 */
@WebServlet("/validarFlag")
public class ValidateFlagControlador extends HttpServlet {
    private static final long serialVersionUID = 1L;

    /**
     * Valida la flag enviada por el usuario desde un formulario o desde la URL.
     */
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        try {
            // Obtener datos del usuario desde el token JWT
            UsuarioJWT usuario = JWTUtils.obtenerUsuarioDesdeRequest(request);
            String userId = usuario.getUserId();

            // Obtener ID del laboratorio
            String labIdParam = request.getParameter("lab_id");
            int labId = Integer.parseInt(labIdParam);

            // Verificar si el usuario ya validó esta flag
            boolean flagValidada = ValidateFlagDAO.hasFlagBeenValidated(Integer.parseInt(userId), labId);
            if (flagValidada) {
                request.setAttribute("mensaje", "Ya has validado esta flag.");
            } else {
                // Validar flag ingresada
                String flagIngresada = request.getParameter("flag");
                String flagCorrecta = LaboratorioDAO.obtenerFlagPorLaboratorio(labId);

                if (flagIngresada != null && flagIngresada.equals(flagCorrecta)) {
                    int puntos = LaboratorioDAO.obtenerPuntosPorLaboratorio(labId);

                    // Registrar validación exitosa
                    ValidateFlagDAO.registerFlagValidation(Integer.parseInt(userId), labId, flagIngresada, puntos);

                    request.setAttribute("mensaje", "Flag validada con éxito. Puntos: " + puntos);
                } else {
                    request.setAttribute("mensaje", "Flag incorrecta, intenta nuevamente.");
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
            request.setAttribute("mensaje", "Hubo un error al validar la flag.");
        }

        // Redirigir al frontend con el mensaje como parámetro
        String mensaje = (String) request.getAttribute("mensaje");
        response.sendRedirect(request.getContextPath() + "/labs/foro-xss.jsp?mensaje=" + mensaje);
    }
}
```

> 🔐 **Seguridad**: El uso de JWT garantiza que solo usuarios autenticados pueden validar flags.

***

#### 🗂 **Vista `TablaController`**

📁 **Ubicación:** `controlador/TablaControlador.java`\
🔍 **Propósito:** Controlador para gestionar operaciones CRUD sobre tablas (insertar, eliminar, actualizar).\
🧠 **Responsabilidad principal:** Procesar solicitudes `POST` para insertar, eliminar y actualizar registros en las tablas de la base de datos.\
🎯 **Método HTTP:** `POST`\
🎨 **Estilo:** Tema oscuro con enfoque en lógica de negocio y acceso a datos.

**Funcionalidades principales:**

* **Insertar registros:**\
  Utiliza el método `insertar` del `TablaDAO` para agregar un nuevo registro a la tabla indicada.
* **Eliminar registros:**\
  Llama al método `eliminar` del `TablaDAO` pasando el valor de la clave primaria y el nombre de la tabla.
* **Actualizar registros:**\
  Utiliza el método `actualizar` del `TablaDAO` para modificar un registro específico basándose en el valor de la clave primaria.

**Código destacado:**

```java
switch (accion) {
    case "insert":
        dao.insertar(tabla, valores);
        break;
    case "delete":
        dao.eliminar(tabla, columnaClave, valorClave);
        break;
    case "update":
        dao.actualizar(tabla, valoresUpdate, valorClaveUpdate);
        break;
}
```

***

#### 🗂 **Vista `TablaDAO`**

📁 **Ubicación:** `dao/TablaDAO.java`\
🔍 **Propósito:** Acceso a datos para realizar operaciones CRUD sobre las tablas de la base de datos.\
🧠 **Responsabilidad principal:** Gestionar las operaciones sobre tablas y registros en la base de datos (consultas, inserciones, eliminaciones y actualizaciones).\
🎯 **Método HTTP:** N/A (Clase de acceso a datos).

**Funcionalidades principales:**

* **Obtener lista de tablas:**\
  El método `getListaTablas` obtiene los nombres de todas las tablas de la base de datos.
* **Obtener columnas de una tabla:**\
  `getColumnas` permite obtener los nombres de las columnas de una tabla específica.
* **Obtener datos de una tabla:**\
  `getDatos` obtiene todas las filas de una tabla dada.
* **Insertar un nuevo registro:**\
  El método `insertar` crea una sentencia SQL dinámica para insertar un registro en la tabla especificada.
* **Eliminar un registro:**\
  `eliminar` construye una consulta SQL para borrar un registro de la tabla según su clave primaria.
* **Actualizar un registro:**\
  `actualizar` construye y ejecuta una sentencia SQL `UPDATE` para modificar un registro específico de la tabla.

**Código destacado:**

```java
public void insertar(String tabla, Map<String, String> valores) {
    // Lógica de inserción dinámica
}
```

***

#### 🗂 **Vista `ViewTablesControlador`**

📁 **Ubicación:** `controlador/ViewTablesControlador.java`\
🔍 **Propósito:** Controlador para visualizar las tablas y sus datos.\
🧠 **Responsabilidad principal:** Recuperar las tablas y sus datos desde la base de datos y generar el HTML para mostrarlas en la vista.\
🎯 **Método HTTP:** `GET`\
🎨 **Estilo:** Tema oscuro con vista de tablas dinámicas.

**Funcionalidades principales:**

* **Obtener y mostrar tablas:**\
  El controlador obtiene el nombre de todas las tablas en la base de datos y las muestra en una estructura HTML.
* **Obtener y mostrar columnas de cada tabla:**\
  Para cada tabla, se obtienen las columnas y se muestran en una tabla HTML.
* **Mostrar los datos de cada tabla:**\
  Se consulta y muestra el contenido de cada tabla en una tabla HTML.

**Código destacado:**

```java
for (String table : tables) {
    tableHtml.append("<h3>Tabla: ").append(table).append("</h3>");
    // Más lógica de creación de tabla HTML
}
```

***

### 🖼️ `FotoDAO.java`

📁 **Ubicación**: `main/java/dao/`\
🧠 **Función**: Recuperar la ruta de la foto de perfil de un usuario desde la base de datos.

#### ✨ Descripción

Esta clase DAO consulta la tabla `profile` para obtener la ruta (`photo_path`) de la imagen de perfil de un usuario específico. Es utilizada para mostrar o cargar la foto en distintas partes del sistema.

#### 📄 Código Documentado

```java
package dao;

import conexionDDBB.ConexionDDBB;
import java.sql.*;

/**
 * DAO para operaciones relacionadas con fotos de perfil.
 */
public class FotoDAO {

    /**
     * Retorna la ruta de la foto de perfil para el usuario con el ID proporcionado.
     *
     * @param userId ID del usuario (como String, convertido internamente a entero)
     * @return Ruta de la foto o null si no se encuentra
     */
    public String obtenerRutaFotoPerfil(String userId) {
        String photoPath = null;
        Connection conexion = null;

        try {
            ConexionDDBB conexionDDBB = new ConexionDDBB();
            conexion = conexionDDBB.conectar();

            String query = "SELECT photo_path FROM profile WHERE user_id = ?";
            PreparedStatement stmt = conexion.prepareStatement(query);
            stmt.setInt(1, Integer.parseInt(userId));

            ResultSet rs = stmt.executeQuery();
            if (rs.next()) {
                photoPath = rs.getString("photo_path");
            }

            rs.close();
            stmt.close();
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            // Cierre de la conexión
            if (conexion != null) {
                try {
                    conexion.close();
                } catch (SQLException e) {
                    e.printStackTrace();
                }
            }
        }

        return photoPath;
    }
}
```

> 💡 **Tip**: Este DAO puede extenderse para actualizar o eliminar la foto si se requiere.

### 📸 `FotoPerfilDAO.java`

📁 **Ubicación**: `main/java/dao/`\
🧠 **Función**: Gestiona la actualización y eliminación de la foto de perfil del usuario.

#### ✨ Descripción

`FotoPerfilDAO` se encarga de insertar, actualizar o eliminar la foto de perfil de un usuario en la base de datos. Además, maneja la eliminación física del archivo de imagen del servidor cuando es necesario.

#### 📄 Código Documentado

```java
package dao;

import conexionDDBB.ConexionDDBB;
import java.io.File;
import java.sql.*;
import javax.servlet.ServletContext;

/**
 * DAO para gestionar la foto de perfil del usuario.
 */
public class FotoPerfilDAO {

    /**
     * Actualiza la ruta de la foto de perfil del usuario. Si no existe entrada previa, la inserta.
     * @param userId ID del usuario
     * @param filePath Ruta relativa o absoluta de la nueva foto
     */
    public static void actualizarFoto(String userId, String filePath) {
        ConexionDDBB conexion = new ConexionDDBB();
        try (Connection conn = conexion.conectar()) {
            // Verificar si el usuario ya tiene foto
            String checkSql = "SELECT COUNT(*) FROM profile WHERE user_id = ?";
            try (PreparedStatement checkStmt = conn.prepareStatement(checkSql)) {
                checkStmt.setInt(1, Integer.parseInt(userId));
                ResultSet rs = checkStmt.executeQuery();
                rs.next();
                int count = rs.getInt(1);

                if (count > 0) {
                    // Ya existe, hacer UPDATE
                    String updateSql = "UPDATE profile SET photo_path = ? WHERE user_id = ?";
                    try (PreparedStatement stmt = conn.prepareStatement(updateSql)) {
                        stmt.setString(1, filePath);
                        stmt.setInt(2, Integer.parseInt(userId));
                        stmt.executeUpdate();
                    }
                } else {
                    // No existe, hacer INSERT
                    String insertSql = "INSERT INTO profile (user_id, photo_path) VALUES (?, ?)";
                    try (PreparedStatement stmt = conn.prepareStatement(insertSql)) {
                        stmt.setInt(1, Integer.parseInt(userId));
                        stmt.setString(2, filePath);
                        stmt.executeUpdate();
                    }
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    /**
     * Elimina la foto de perfil de la base de datos y del sistema de archivos.
     * @param userId ID del usuario
     * @param context Contexto del servlet para obtener la ruta física del archivo
     */
    public static void eliminarFoto(String userId, ServletContext context) {
        ConexionDDBB conexion = new ConexionDDBB();
        try (Connection conn = conexion.conectar()) {
            String selectSql = "SELECT photo_path FROM profile WHERE user_id = ?";
            String filePath = null;

            // Obtener ruta actual de la foto
            try (PreparedStatement selectStmt = conn.prepareStatement(selectSql)) {
                selectStmt.setInt(1, Integer.parseInt(userId));
                ResultSet rs = selectStmt.executeQuery();
                if (rs.next()) {
                    filePath = rs.getString("photo_path");
                }
            }

            if (filePath != null) {
                // Eliminar entrada de la base de datos
                String deleteSql = "DELETE FROM profile WHERE user_id = ?";
                try (PreparedStatement stmt = conn.prepareStatement(deleteSql)) {
                    stmt.setInt(1, Integer.parseInt(userId));
                    stmt.executeUpdate();
                }

                // Eliminar archivo físico
                File file = new File(context.getRealPath(filePath));
                if (file.exists()) {
                    file.delete();
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
```

> 📌 **Nota**: Asegúrate de que la aplicación tenga permisos de escritura en el directorio donde se guardan las imágenes.

***

### 🧪 `LaboratorioDAO.java`

📁 **Ubicación**: `main/java/dao/`\
🧠 **Función**: Acceso y manipulación de datos de la tabla `laboratorios`.

#### ✨ Descripción

La clase `LaboratorioDAO` proporciona operaciones para gestionar laboratorios dentro de un sistema de retos tipo CTF. Incluye funciones para crear la tabla si no existe, insertar nuevos laboratorios, y consultar información como el nombre, flag, y puntos asociados a un laboratorio.

#### 📄 Código Documentado

```java
package dao;

import java.sql.*;
import conexionDDBB.ConexionDDBB;

/**
 * DAO que gestiona las operaciones relacionadas con los laboratorios.
 */
public class LaboratorioDAO {

    /**
     * Crea la tabla 'laboratorios' si aún no existe.
     */
    public static void ensureTableExists() throws SQLException {
        String checkTableQuery = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'laboratorios'";
        try (Connection conn = new ConexionDDBB().conectar();
             PreparedStatement ps = conn.prepareStatement(checkTableQuery)) {

            ResultSet rs = ps.executeQuery();
            if (rs.next() && rs.getInt(1) == 0) {
                String createTableQuery = "CREATE TABLE laboratorios ("
                        + "lab_id SERIAL PRIMARY KEY, "
                        + "nombre VARCHAR(255) NOT NULL, "
                        + "flag VARCHAR(255) NOT NULL, "
                        + "puntos INT NOT NULL)";
                try (Statement stmt = conn.createStatement()) {
                    stmt.executeUpdate(createTableQuery);
                }
            }
        }
    }

    /**
     * Devuelve el ID del laboratorio llamado "foro-xss".
     */
    public static int obtenerIdLaboratorioForoXss() {
        return obtenerIdPorNombre("foro-xss");
    }

    /**
     * Devuelve el ID del laboratorio llamado "amashop".
     */
    public static int obtenerIdLaboratorioAmashop() {
        return obtenerIdPorNombre("amashop");
    }

    private static int obtenerIdPorNombre(String nombreLab) {
        int labId = -1;
        String query = "SELECT lab_id FROM laboratorios WHERE nombre = ?";
        try (Connection conn = new ConexionDDBB().conectar();
             PreparedStatement stmt = conn.prepareStatement(query)) {

            stmt.setString(1, nombreLab);
            ResultSet rs = stmt.executeQuery();
            if (rs.next()) {
                labId = rs.getInt("lab_id");
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return labId;
    }

    /**
     * Inserta un nuevo laboratorio en la base de datos.
     */
    public static boolean agregarLaboratorio(String nombre, String flag, int puntos) {
        boolean exito = false;
        String query = "INSERT INTO laboratorios (nombre, flag, puntos) VALUES (?, ?, ?)";
        try (Connection conn = new ConexionDDBB().conectar();
             PreparedStatement stmt = conn.prepareStatement(query)) {

            stmt.setString(1, nombre);
            stmt.setString(2, flag);
            stmt.setInt(3, puntos);

            int filasAfectadas = stmt.executeUpdate();
            exito = filasAfectadas > 0;
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return exito;
    }

    /**
     * Devuelve la flag de un laboratorio dado su ID.
     */
    public static String obtenerFlagPorLaboratorio(int labId) {
        String flag = null;
        String query = "SELECT flag FROM laboratorios WHERE lab_id = ?";
        try (Connection conn = new ConexionDDBB().conectar();
             PreparedStatement stmt = conn.prepareStatement(query)) {

            stmt.setInt(1, labId);
            ResultSet rs = stmt.executeQuery();
            if (rs.next()) {
                flag = rs.getString("flag");
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return flag;
    }

    /**
     * Devuelve el nombre del laboratorio por su ID.
     */
    public static String obtenerNombreLaboratorio(int labId) {
        String nombre = "";
        String query = "SELECT nombre FROM laboratorios WHERE lab_id = ?";
        try (Connection conn = new ConexionDDBB().conectar();
             PreparedStatement stmt = conn.prepareStatement(query)) {

            stmt.setInt(1, labId);
            ResultSet rs = stmt.executeQuery();
            if (rs.next()) {
                nombre = rs.getString("nombre");
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return nombre;
    }

    /**
     * Devuelve los puntos asignados al laboratorio.
     */
    public static int obtenerPuntosPorLaboratorio(int labId) {
        int puntos = 0;
        String query = "SELECT puntos FROM laboratorios WHERE lab_id = ?";
        try (Connection conn = new ConexionDDBB().conectar();
             PreparedStatement stmt = conn.prepareStatement(query)) {

            stmt.setInt(1, labId);
            ResultSet rs = stmt.executeQuery();
            if (rs.next()) {
                puntos = rs.getInt("puntos");
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return puntos;
    }
}
```

> 🛡️ **Recomendación**: Para mejorar robustez, considera manejar excepciones con mensajes personalizados o logs más detallados.

#### 🗂 **Clase `ValidateFlagDAO`**

📁 **Ubicación:** `dao/ValidateFlagDAO.java`\
🔍 **Propósito:** Gestionar la validación de _flags_ por parte de los usuarios en los laboratorios.\
🧠 **Responsabilidad principal:** Registrar y comprobar si un usuario ya ha validado la _flag_ de un laboratorio.\
💾 **Tabla involucrada:** `validate_flag`

**Métodos clave:**

* **`ensureTableExists()`**\
  Verifica si existe la tabla `validate_flag`, y si no, la crea con las columnas:
  * `id`, `user_id`, `lab_id`, `flag`, `puntos`
* **`hasFlagBeenValidated(int userId, int labId)`**\
  Retorna `true` si el usuario ya validó la flag de un laboratorio específico, `false` si no.
* **`registerFlagValidation(int userId, int labId, String flag, int puntos)`**\
  Inserta un registro en la tabla `validate_flag` cuando un usuario valida correctamente una flag, incluyendo los puntos ganados.

***

#### 🔐 **Clase `JWTUtils`**

📁 **Ubicación:** `utils/JWTUtils.java`\
🔍 **Propósito:** Extraer información de un JWT presente en las cookies del request HTTP.\
🧠 **Responsabilidad principal:** Obtener un objeto `UsuarioJWT` a partir del token de autenticación.\
🔑 **Clave secreta:** `"clave_super_secreta"`

**Métodos clave:**

*   **`obtenerUsuarioDesdeRequest(HttpServletRequest request)`**\
    Extrae y valida el JWT desde las cookies del `HttpServletRequest`, devolviendo un objeto `UsuarioJWT` con:

    * `nombre`, `apellidos`, `rol`, `email`, `ultimoLogin`, `usuario`, `cookie`, `userId`, `token`

    ⚠️ Lanza excepciones si:

    * No hay token en las cookies
    * El token está expirado
    * El token no es válido
* **`obtenerTokenDesdeCookies(HttpServletRequest request)`**\
  Busca la cookie llamada `"token"` y retorna su valor (el JWT).

#### 👤 **Clase `UsuarioJWT`**

📁 **Ubicación:** `utils/UsuarioJWT.java`\
🔍 **Propósito:** Representar a un usuario autenticado a través de un token JWT.\
🧠 **Responsabilidad principal:** Almacenar los detalles de un usuario extraídos de un token JWT.

**Atributos:**

* **`nombre`**: Nombre del usuario.
* **`apellidos`**: Apellidos del usuario.
* **`rol`**: Rol del usuario (ej. `admin`, `usuario`).
* **`email`**: Dirección de correo electrónico del usuario.
* **`ultimoLogin`**: Fecha/hora del último inicio de sesión.
* **`usuario`**: Nombre de usuario (username).
* **`cookie`**: Información asociada a la cookie (si corresponde).
* **`userId`**: ID único del usuario.
* **`token`**: El token JWT del usuario.

**Métodos clave:**

* **Constructor**\
  El constructor recibe todos los atributos mencionados para crear un objeto `UsuarioJWT`.
* **Getters**\
  Métodos para acceder a cada uno de los atributos (nombre, apellidos, rol, email, último login, usuario, cookie, userId, token).

#### ✅ **`ValidateFlagControlador.java`**

📁 **Ubicación:** `controlador/ValidateFlagControlador.java`\
**Método:** `GET`

**Función:**\
Controla la validación de flags cuando un usuario las envía.

**Proceso paso a paso:**

1. Obtiene el `userId` desde el JWT del usuario.
2. Toma el `lab_id` desde la URL.
3. Verifica si ese usuario ya validó la flag para ese laboratorio.
4. Si no está validada:
   * Compara la flag ingresada con la flag correcta del laboratorio.
   * Si es correcta, guarda la validación y suma puntos.
   * Si es incorrecta, informa el error.
5. Redirige a la página del laboratorio correspondiente con el mensaje.

**Redirecciones según lab\_id:**

* 1 → `/labs/foro-xss.jsp`
* 2 → `/labs/amashop/amashop.jsp`
* 3 → `/labs/hacking_community/hacking_community.jsp`
* 4 → `/labs/separo/separo.jsp`
* Default → `/home_directory/home.jsp?page=0`

***

#### 📝 **`WriteupControlador.java`**

📁 **Ubicación:** `controlador/WriteupControlador.java`\
**Método:** `POST`

**Función:**\
Recibe y guarda un nuevo _writeup_ enviado por el usuario.

**Parámetros esperados:**

* `lab_id`: ID del laboratorio
* `user_id`: ID del usuario
* `username`: nombre de usuario
* `url_writeup`: URL del writeup

**Proceso:**

* Usa `WriteupDAO.insertWriteup(...)` para guardar el writeup en la BD.
* Si se guarda con éxito → redirige a `/sendWriteups.jsp`
* Si falla → redirige a `/error.jsp`

***

#### 📄 **`WriteupTablaControlador.java`**

📁 **Ubicación:** `controlador/WriteupTablaControlador.java`\
**Método:** `GET`

**Función:**\
Carga todos los writeups disponibles para un laboratorio específico.

**Proceso:**

1. Toma el `lab_id` desde la URL.
2. Llama a `WriteupUserDAO.obtenerWriteupsPorLabId(...)` para traer los writeups.
3. Los pasa como atributo a `tablaWriteups.jsp` para renderizarlos.

***

#### 🔧 **`HttpUtils.java`**

📁 **Ubicación:** `utils/HttpUtils.java`**Función:**\
Utilidad para hacer una solicitud HTTP a un servidor Flask y obtener el nombre de usuario asociado a un `userId`.

**Método:**

* `getUsernameFromFlask(int userId)`:\
  Hace un GET a `http://localhost:5000/get_username/{userId}`\
  Devuelve el `username` (desde JSON) o `null` si hay error.

**Ejemplo de respuesta JSON esperada:**

```java
{
  "username": "pepe_el_destroyer"
}
```

#### 🧠 **Clase `RankingControlador`**

📁 **Ubicación:** `controlador/RankingControlador.java`\
🔍 **Propósito:** Consultar y devolver el ranking de usuarios según sus puntajes.\
🧠 **Responsabilidad principal:** Gestionar la lógica de negocio para obtener los datos del ranking.

**Método clave:**

*   **`obtenerRankingUsuarios()`**\
    Se conecta a la base de datos y delega a `RankingDAO` la consulta.\
    Retorna una lista de objetos `RankingEntry` con los usuarios y sus puntajes.

    🔧 Usa:

    * `ConexionDDBB` para abrir y cerrar la conexión.
    * `RankingDAO.getRankingFromAllTables()` para la lógica SQL.

    ⚠️ En caso de error, imprime el stacktrace y devuelve una lista vacía.

***

#### 📝 **Clase `WriteupDAO`**

📁 **Ubicación:** `dao/WriteupDAO.java`\
🔍 **Propósito:** Insertar o actualizar un writeup en la base de datos.\
🧠 **Responsabilidad principal:** Mantener la tabla `writeups` actualizada con las URLs compartidas por los usuarios.

**Método clave:**

*   **`insertWriteup(int labId, int userId, String url, String username)`**\
    Inserta un writeup o lo actualiza si ya existe uno del mismo `userId` para ese `labId`.

    ✅ Usa `ON CONFLICT (lab_id, user_id)` para actualizar automáticamente.\
    Retorna `true` si la operación tuvo éxito.

    ⚠️ Maneja errores SQL y cierra la conexión al final.

***

#### ✅ **Clase `ValidateFlagDAO`**

📁 **Ubicación:** `dao/ValidateFlagDAO.java`\
🔍 **Propósito:** Gestionar la validación de flags de los laboratorios.\
🧠 **Responsabilidad principal:** Controlar registros de flags validadas por los usuarios.

**Métodos clave:**

* **`ensureTableExists()`**\
  Verifica si la tabla `validate_flag` existe. Si no, la crea con las columnas necesarias (`user_id`, `lab_id`, `flag`, `puntos`).
* **`hasFlagBeenValidated(int userId, int labId)`**\
  Retorna `true` si ese usuario ya validó la flag de ese laboratorio.
*   **`registerFlagValidation(int userId, int labId, String flag, int puntos)`**\
    Inserta un nuevo registro de validación (una sola vez por usuario y laboratorio).

    ⚠️ Todas las operaciones usan `ConexionDDBB` para gestionar la conexión.

***

#### 📊 **Clase `RankingDAO`**

📁 **Ubicación:** `dao/RankingDAO.java`\
🔍 **Propósito:** Consultar los puntajes totales de los usuarios desde distintas tablas.\
🧠 **Responsabilidad principal:** Armar el ranking completo sumando puntos desde la base.

**Método clave:**

* **`getRankingFromAllTables(Connection conn)`**\
  Consulta a la tabla `validate_flag` para sumar los puntos por usuario y devolver un ranking ordenado.

***

#### 🔢 **Modelo `RankingEntry`**

📁 **Ubicación:** `modelo/RankingEntry.java`\
🔍 **Propósito:** Representar una fila del ranking de usuarios.\
🧠 **Responsabilidad principal:** Encapsular datos de ranking (`username` y `totalPoints`).

**Atributos:**

* `username` → nombre del usuario
* `totalPoints` → puntos acumulados

✔️ Constructor y getters incluidos.

***

#### 🌐 **Modelo `Writeup`**

📁 **Ubicación:** `modelo/Writeup.java`\
🔍 **Propósito:** Representar un writeup asociado a un laboratorio.\
🧠 **Responsabilidad principal:** Encapsular info de un writeup compartido.

**Atributos:**

* `username` → autor del writeup
* `url` → enlace al writeup
* `nombreLaboratorio` → nombre del lab asociado

✔️ Constructor y getters incluidos.

#### 🌀 `animation.jsp`

📁 **Ubicación:** `webapp/animation.jsp`

Este archivo representa una pantalla animada de transición o bienvenida, posiblemente usada al inicio de sesión o redirección. Aquí va su explicación:

* **🔐 Validación JWT**:
  * Se importa `JWTUtils` y `UsuarioJWT` para verificar el token del usuario.
  * Si el token no es válido o no se puede extraer el usuario → `redirect` al servlet de `/logout` (evitando cargar la página sin sesión activa).
* **🔄 Redirección automática**:
  * Utiliza `<meta http-equiv="refresh" content="4; url=home_directory/home.jsp?page=0">` para redirigir al usuario automáticamente a la página principal después de 4 segundos.
* **💻 UI / Estética**:
  * Icono de "Navegador" con clase `desktop-icon`.
  * Un div `.browser-window` simulando una ventana del navegador.
  * Cursor animado (`#cursor`) para agregar un toque retro/interactivo.
  * Estilos personalizados cargados desde `/css/animation.css`.
  * Scripts de comportamiento en `/js/animation.js`.
* **💡 Nota**:
  * Hay un video de fondo comentado —podría usarse para una experiencia más inmersiva—.
  * La estructura simula un sistema operativo o escritorio virtual antiguo, posiblemente con un enfoque nostálgico/retro.

***

#### 🏠 `home.jsp`

📁 **Ubicación:** `home_directory/home.jsp` (Le siguen el mismo estilo las paginas `Page1.jsp`, `Page2.jsp`, `Page3.jsp` y `Page4.jsp`)

Este archivo representa **la página principal del sistema**, tipo buscador de labs/recursos, con navegación por páginas. Aquí va su desglose:

* **🔐 Validación del token JWT**:
  * Se usa `JWTUtils` para validar el token del usuario.
  * Si el token es inválido o no contiene `userId`, redirige al servlet `/logout` o muestra error.
* **🖼️ Carga dinámica de foto de perfil**:
  * Se obtiene vía `FotoDAO` con el `userId` contenido en el token.
  * Si no existe una foto → se muestra una por defecto (`img/Profile.png`).
* **🎨 UI y elementos visuales**:
  * Header con logo e imagen de perfil.
  * Si el usuario tiene el rol `designer`, se muestra un botón hacia `admin-panel.jsp`.
  * Navbar con secciones (Hackend, DockerPwned, OVAlabs...) y menú desplegable:
    * Filtros por tipo, dificultad, tags, creadores.
  * Barra de búsqueda `#liveSearch` con iconos (borrar, micro, cámara).
  * Sección `.results` para mostrar resultados de búsqueda.
* **🧠 JS dinámico y búsqueda**:
  * Carga resultados simulados (mockeados) desde un array de objetos en JS.
  * Cada resultado incluye: imagen, título, descripción y tags.
  * Tags se renderizan visualmente como `#nombre`.
  * Soporte para navegación entre páginas (`page=0`, `page=1`...), incluida funcionalidad del botón “Siguiente”.
* **🔢 Paginación**:
  * Muestra páginas numeradas (1 a 5).
  * Cambia el estilo de la letra "O" en el logo de Google (Hackend) para representar la página activa.
  * Función `highlightCurrentPage()` lo gestiona dinámicamente.
  * El botón "Siguiente" redirige a la siguiente página (`Page1.jsp`, `Page2.jsp`, etc).
* **🦶 Footer básico**:
  * Información de autores ("d1se0 y m4nu"), enlaces a ayuda, privacidad, términos, etc.
* **🎯 Scripts extra**:
  * Asegura que los enlaces no se abran en `_blank`, sino en la misma ventana (`_self`).
  * `home.js` es cargado adicionalmente al final, lógica extendida.

### 📄 **Archivo: `profile.jsp`**

📁 **Ubicación:** `webapp/profile.jsp`

#### 📌 **Descripción:**

Esta vista muestra al usuario su información de perfil recuperada desde el token JWT. Muestra nombre, correo, rol, última sesión, imagen de perfil, y permite cerrar sesión o navegar a la edición del perfil.

#### ✅ **Aspectos clave:**

* **Seguridad JWT:** Verifica la validez del token con `JWTUtils.obtenerUsuarioDesdeRequest(request)` y redirige a logout si no es válido.
* **Imagen de perfil:** Usa `FotoDAO` para obtener la ruta de la imagen de perfil y carga una imagen por defecto si no se encuentra.
* **Presentación personalizada:** Usa estilos visuales modernos con un diseño tipo "pantalla retro" con botones inspirados en macOS.
* **Datos mostrados del token:**
  * Usuario
  * Rol
  * Email
  * Nombre y apellidos
  * Último login
  * Cookie y token JWT como texto plano
* **Opciones de acción:**
  * Botón para cerrar sesión (`/logout`)
  * Botón para editar el perfil (`editarPerfil.jsp`)

***

### 📄 **Archivo: `editarPerfil.jsp`**

📁 **Ubicación:** `webapp/editarPerfil.jsp`

#### 📌 **Descripción:**

Vista para que el usuario edite sus datos personales y su contraseña, así como para actualizar o eliminar su foto de perfil. Toda la información se rellena automáticamente desde el token JWT.

#### ✅ **Aspectos clave:**

* **Seguridad JWT:** Igual que `profile.jsp`, valida el token y redirige a logout si no es válido.
* **Formulario dividido en dos funcionalidades:**
  1. **Editar datos personales:**
     * Nombre
     * Apellidos
     * Email
     * Usuario
     * Cambiar contraseña (requiere contraseña actual + nueva y confirmación)
     * Incluye el token como campo oculto para el backend
  2. **Subir/eliminar foto de perfil:**
     * Subida de nueva imagen (`multipart/form-data`)
     * Botón para eliminar la imagen actual
* **Reutiliza el estilo visual de `profile.jsp`** (pantalla estilo monitor, madera de fondo, botones de ventana).
* **El formulario de foto hace POST a `SubirFotoPerfil?user_id=...`**, enlazando directamente con el backend para subir o eliminar imágenes.

#### 🎞️ `animation.css`

📁 **Ubicación:** `css/animation.css`

**✅ Objetivo**

Simular una experiencia visual al estilo de un escritorio clásico (como Windows XP) con íconos de escritorio, un video de fondo, y elementos animados para dar un toque interactivo/retro.

**🧱 Estructura Clave**

* **Fuentes & Fondo:**

```css
* {
    font-family: 'JetBrains Mono', monospace;
}
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: url('../img/DesktopWINXP.jpg') no-repeat center center fixed;
    background-size: cover;
}
```

* Usa una fuente _monoespaciada_ para consistencia en ciertos elementos.
* Estilo principal retro, simulando un escritorio con imagen fija al fondo.
* **Video de fondo:**

```css
video.background-video {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    z-index: -1;
}
```

* Hace que el video se expanda a toda la pantalla y quede detrás de los elementos (por el `z-index: -1`).
* **Íconos de escritorio:**

```css
.desktop-icon {
    position: absolute;
    bottom: 40px;
    left: 40px;
    color: white;
    text-align: center;
}
```

* Estiliza íconos tipo "acceso directo" en una ubicación fija.
* **Cursor personalizado:**

```css
.cursor {
    background: url('../img/cursor.png') no-repeat;
    position: absolute;
    pointer-events: none;
}
```

* Usa una imagen personalizada como cursor. Importante para experiencias inmersivas o nostálgicas.
* **Ventana tipo navegador (oculta por defecto):**

```css
.browser-window {
    display: none;
    box-shadow: 0 0 10px #000;
}

.browser-header {
    background: #0078d7;
    color: white;
}
```

* Simula ventanas emergentes estilo navegador clásico.

**💡 Toques Interesantes**

* Cursor bloqueado en la pantalla y reemplazado por imagen personalizada.
* Simulación de un escritorio de sistema operativo.
* Muy útil si estás creando un sistema tipo "emulador visual" o "explorador vintage".

***

#### 🧩 `editarPerfilUpdate.css`

📁 **Ubicación:** `css/editarPefilUpdate.css`

**✅ Objetivo**

Dar estilo a una pantalla con apariencia de monitor retro, donde el usuario puede editar su información. Simula una ventana de sistema operativo antigua, con un toque profesional, limpio y funcional.

**🧱 Estructura Clave**

* **Contenedores:**

```css
.background, .monitor, .stand, .base
```

* Componen un "monitor de computadora" completo: pantalla, soporte y base.
* Todo centrado en la pantalla.
* **Formulario:**

```css
.formulario {
    background-color: rgba(0, 0, 0, 0.6);
    overflow-y: auto;
    color: #fff;
}
```

* Fondo translúcido negro para contraste.
* Scrollbar personalizado.
* Estilo moderno para inputs, con acento azul (#00aaff).
* **Botones estilo MacOS:**

```css
.ventana-macos .boton.rojo / .amarillo / .verde
```

* Estética similar a las ventanas de macOS (cerrar, minimizar, maximizar).
* **Scroll personalizado:**
  * Compatible tanto con WebKit como con navegadores Firefox.
* **Control del cursor:**

```css
body.cursor-locked { cursor: none; pointer-events: none; }
body.cursor-enabled { cursor: auto; pointer-events: auto; }
```

* Usa clases dinámicas para habilitar/deshabilitar la interacción.
* Ideal para experiencias "inmersivas".

**💡 Toques Interesantes**

* Muy elegante la separación entre "formulario de edición" y "subir foto".
* Excelente uso de `scrollbar` y `pointer-events` para experiencia inmersiva.
* Detalles visuales como `box-shadow`, `border-radius`, y colores oscuros brindan una sensación pro.

***

#### 🧠 En Resumen:

| Archivo                  | Enfoque                                        | Destaca por...                                            |
| ------------------------ | ---------------------------------------------- | --------------------------------------------------------- |
| `animation.css`          | Simulación de escritorio interactivo retro     | Video de fondo, cursor personalizado, íconos flotantes    |
| `editarPerfilUpdate.css` | UI para edición de perfil en pantalla simulada | Estilo retro-moderno, scroll personalizado, botones macOS |

#### 🔷 `home.css` (Estilo principal para la página de inicio)

📁 **Ubicación:** `css/home.css`

**🌑 Base y tipografía**

```css
* {
  font-family: 'JetBrains Mono', monospace;
}
body {
  background-color: #121212;
  color: white;
}
```

**🧭 Encabezado / Header**

```css
.header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 10px 20px;
  background-color: #1e1e1e;
}
.logo { font-size: 24px; font-weight: bold; }
.logo-image { width: 120px; height: 50px; }
.profile-icon {
  width: 40px; height: 40px;
  border-radius: 50%;
  background-color: gray;
}
```

**🔍 Barra de búsqueda**

```css
.search-bar {
  display: flex; justify-content: space-between; align-items: center;
  background-color: #2a2a2a;
  padding: 10px;
  border-radius: 25px;
  width: 600px;
  margin: 20px auto;
  border: 1px solid #5f6368;
}
.search-input {
  flex: 1;
  background: none;
  border: none;
  color: white;
}
.search-icons { display: flex; gap: 15px; }
.search-icons i {
  font-size: 20px; color: #bbb;
}
.search-icons i:hover { color: white; }
```

**🧭 Navegación / Menú**

```css
.nav-menu {
  display: flex; justify-content: center; gap: 20px;
  padding: 10px; border-bottom: 1px solid #333;
}
.nav-menu a {
  color: #ccc; font-size: 14px;
}
.nav-menu a:hover { color: #8ab4f8; }
```

**📂 Menú desplegable y submenús**

```css
.dropdown-menu {
  display: none;
  position: relative;
  background-color: #1e1e1e;
  border-top: 1px solid #333;
}
.nav-container.active .dropdown-menu {
  display: flex; justify-content: center;
}
.body-expanded { margin-top: 200px; }

.submenu-container {
  display: flex; gap: 10px; justify-content: center;
}
.submenu {
  display: none;
  position: relative;
  background-color: #262626;
}
```

**📄 Resultados de búsqueda**

```css
.result-item {
  display: flex; align-items: flex-start;
  padding: 10px;
}
.result-item a {
  color: #8ab4f8; font-weight: bold;
}
.result-item .url { color: #8d8d8d; }
.result-item p { color: #ccc; }
```

**🔢 Paginación**

```css
.pagination {
  text-align: center;
  padding: 20px;
}
.pagination a {
  color: #8ab4f8;
}
.pagination a:hover {
  text-decoration: underline;
}
```

**📦 Footer**

```css
.footer {
  background-color: #1f1f1f;
  border-top: 1px solid #333;
}
.footer a { color: #8ab4f8; }
.footer a:hover { color: white; }
```

**🏷️ Tags**

```css
.tag {
  font-size: 0.8rem;
  color: rgba(255, 140, 0, 0.8);
}
.selected {
  background-color: rgba(0, 123, 255, 0.5);
}
.unselected {
  background-color: transparent;
}
```

***

#### 🟢 `profileUpdate.css` (Estilo tipo consola/GitHub para perfil)

📁 **Ubicación:** `css/profileUpdate.css`

**🧱 Layout y fuente general**

```css
body {
  background-color: #0d1117;
  font-family: 'Courier New', monospace;
  color: #e6edf3;
}
```

**🪟 Header tipo ventana**

```css
.window-header {
  background: #161b22;
  border-bottom: 1px solid #30363d;
}
.win-btn {
  background: #21262d;
  border-radius: 4px;
}
```

**💬 Comentarios**

```css
.forum-container { overflow-y: auto; }
.comment-box {
  background: #161b22;
  border: 1px solid #30363d;
}
.username { color: #58a6ff; }
.comment-actions button:hover { color: #00ffcc; }
```

**💡 Botón solución flotante**

```css
.solution-btn {
  position: fixed;
  bottom: 10px;
  left: 10px;
  background: radial-gradient(circle, #00ffcc, #0077ff);
}
```

**💬 Popup tipo ventana**

```css
.popup {
  background-color: #0d1117;
  border: 1px solid #30363d;
  box-shadow: 0 0 15px #00ffcc4f;
}
.popup-header h2 { color: #00ffcc; }
.close-btn { color: #ff4d4d; }
.btn-solution {
  background: linear-gradient(90deg, #00ffcc, #0077ff);
}
```

**💬 Comentarios rápidos**

```css
.comment-form {
  background-color: #161b22;
}
.comment-form input {
  background-color: #21262d;
}
.comment-form button.solution-btn {
  background-color: #ffeb3b;
}
```

**⚠️ Alerta tipo XSS**

```css
.popup-xss {
  background-color: #21262d;
  color: #e6edf3;
  box-shadow: 0 0 15px rgba(0, 255, 204, 0.5);
}
.popup-xss button {
  color: #ff4d4d;
}
```

#### 🖥️ **Vista `foro-xss.jsp`**

📁 **Ubicación:** `labs/foro-xss.jsp`\
🔍 **Propósito:** Simula un foro web vulnerable a XSS como parte del laboratorio práctico para que el usuario aprenda a explotar la vulnerabilidad y obtenga una flag.\
🧠 **Responsabilidad principal:** Renderizar la interfaz del laboratorio XSS, gestionar los comentarios y mostrar la flag al explotar exitosamente la vulnerabilidad.\
💾 **Dependencias clave:** `LaboratorioDAO`, `JWTUtils`, `validarFlag`, `foro-xss.css`, `foro-xss.js`

**🛠 Funcionalidades principales:**

* **🔑 Autenticación y validación del token JWT**
  * Extrae el token desde la request usando `JWTUtils.obtenerUsuarioDesdeRequest(request)`
  * Redirige a `/logout` si el token no es válido.
* **🧪 Identificación del laboratorio**
  * Obtiene el ID del laboratorio XSS mediante `LaboratorioDAO.obtenerIdLaboratorioForoXss()`.
* **📥 Envío de FLAG**
  * Formulario que envía los parámetros `user_id`, `lab_id`, y `flag` al servlet `validarFlag` mediante método `GET`.
* **💬 Renderizado de comentarios estilo foro**
  * Se muestran comentarios estáticos simulando interacción entre usuarios sobre temas de XSS.
  * Cada bloque contiene: usuario, timestamp, texto y botones de interacción (like/responder).
* **📜 Inyección de JS desde backend**
  * Código JavaScript embebido simula un `hook` de XSS: al ejecutarse un `alert`, también muestra el mensaje con la flag.

```javascript
window.alert = function(msg) {
    originalAlert(msg);
    originalAlert('¡Lab completado! Flag: FLAG{lo_lograste}');
};
```

* **💡 Popup de solución**
  * Botón amarillo flotante muestra una explicación con ejemplos prácticos sobre cómo explotar XSS para obtener la flag.
* **📢 Popup emergente de validación de flag**
  * Si `mensaje` (param. en URL) existe, se muestra en un popup personalizado centrado en pantalla.

***

#### 🎨 **Estilo visual (CSS): `foro-xss.css`**

📁 **Ubicación:** `css/foro-xss.css`\
🎯 **Propósito:** Dar una estética _dark mode_ tipo consola con un diseño moderno, limpio y con efectos visuales llamativos para una experiencia tipo CTF.

**Destacados del diseño:**

* **Tema oscuro y tipografía tipo terminal:**\
  Usa `Courier New` y una paleta basada en `#0d1117` con acentos en `#00ffcc`.
* **Foro con tarjetas (`.comment-box`)**\
  Estilo responsive, bordes redondeados, color de fondo sobrio y comentarios organizados.
* **Popups personalizados:**\
  Diseñados para soluciones y mensajes emergentes con sombras, centrado automático y efectos de transición.
* **Botón solución flotante:**\
  Estilo brillante y con sombra tipo neón (`radial-gradient`) para llamar la atención.

#### 💬 **Script foro-xss.js**

📁 **Ubicación:** `js/foro-xss.js`\
🔍 **Propósito:** Manejar la publicación de comentarios en el foro con protección básica contra ataques XSS.\
🧠 **Responsabilidad principal:** Detectar e impedir la ejecución de scripts maliciosos inyectados por los usuarios, renderizar comentarios de forma segura, y gestionar interacciones como "me gusta".

**Funcionalidades clave:**

* **detectarXSS(texto)**\
  Detecta si el texto contiene etiquetas `<script>` usando una expresión regular. Muestra un popup y lanza una excepción si detecta XSS.
* **escapeHTML(str)**\
  Reemplaza caracteres especiales (`<`, `>`, `"`, `'`, `&`) por sus entidades HTML para evitar la ejecución de código malicioso.
* **commentForm.addEventListener('submit', ...)**\
  Maneja el envío del formulario de comentarios. Escapa el contenido y crea la estructura HTML del comentario dinámicamente. Previene XSS.
* **forumContainer.addEventListener('click', ...)**\
  Escucha clics en botones dentro de los comentarios para aumentar el contador de "me gusta".
* **showPopup() / closePopup()**\
  Funciones auxiliares para mostrar y cerrar el popup de solución cuando se valida correctamente una respuesta.

***

#### 🖱️ **Script animation.js**

📁 **Ubicación:** `js/animation.js`\
🔍 **Propósito:** Ejecutar una animación visual que simula el movimiento del cursor hacia un icono y luego mostrar el navegador.\
🧠 **Responsabilidad principal:** Crear una introducción interactiva o guía visual al cargar la interfaz.

**Funcionalidades clave:**

* **Animación del cursor:**\
  Calcula la posición del icono objetivo y anima el cursor desde el centro de la pantalla hasta él.
* **Mostrar navegador:**\
  Tras finalizar la animación del cursor (2s), muestra el elemento navegador (`#navegador`) con un pequeño retraso.

***

#### 🏠 **Script home.js**

📁 **Ubicación:** `js/home.js`\
🔍 **Propósito:** Gestionar el menú principal, buscador en vivo, filtros por tipo/tag, y renderizado dinámico de resultados en la página principal.\
🧠 **Responsabilidad principal:** Crear una experiencia interactiva e intuitiva para navegar entre retos, filtrarlos, buscarlos y clasificarlos.

**Funcionalidades clave:**

* **Menú desplegable (moreButton):**\
  Muestra/oculta el menú adicional, expandiendo o contrayendo el cuerpo de la página.
* **Motor de búsqueda en vivo:**\
  Escucha cambios en el input de búsqueda y filtra dinámicamente los resultados en base a título y tags.
* **Botón clearSearch:**\
  Limpia el input del buscador y reinicia los resultados.
* **Filtros por tipo y tags:**\
  Permite seleccionar uno por bloque. Aplica clases `selected`/`unselected`, actualiza el estado global de los filtros y vuelve a renderizar los resultados.
* **renderResults(results):**\
  Crea dinámicamente los bloques de resultados (favicon, título, descripción, tags), limpiando los anteriores.
* **Inicialización con `DOMContentLoaded`:**\
  Carga todos los resultados disponibles al iniciar la página y asigna eventos de filtros.

#### 🗂 **Archivo none.jsp**

📁 **Ubicación:** `labs/none.jsp`\
🔍 **Propósito:** Mostrar una página informativa que indique que una sección está en construcción y redirigir al usuario si no está autenticado.\
🧠 **Responsabilidad principal:** Proporcionar un mensaje de "en construcción" y manejar la autenticación del usuario a través de un JWT (JSON Web Token).\
🔑 **Funcionalidad clave:**

* **Autenticación del usuario:**\
  Utiliza el método `JWTUtils.obtenerUsuarioDesdeRequest(request)` para verificar si el usuario está autenticado. Si no es así, redirige a la página de cierre de sesión (`logout`).
* **Mensaje de construcción:**\
  Muestra un mensaje visual con un emoji de construcción 🚧 y un texto indicando que la sección está en construcción.

**Secciones clave:**

* **JWTUtils.obtenerUsuarioDesdeRequest(request):**\
  Intenta obtener la información del usuario desde el JWT en la solicitud. Si la obtención falla, redirige al usuario al servlet de logout.
* **Estructura HTML:**\
  Presenta una interfaz sencilla y centrada con un mensaje de "en construcción", un emoji que refuerza el tema, y un enlace que redirige al usuario de vuelta a la página principal (`home.jsp`).
* **Estilo básico:**\
  El estilo de la página incluye un diseño minimalista centrado, con un fondo claro, sombra para darle profundidad y un toque amigable con un emoji grande.

#### 🗂 **Vista `admin-panel.jsp`**

📁 **Ubicación:** `designer/admin-panel.jsp`\
🔍 **Propósito:** Panel administrativo exclusivo para usuarios con rol `designer`.\
🧠 **Responsabilidad principal:** Ofrecer acceso a funcionalidades avanzadas como gestión de laboratorios, logs del sistema y visualización de la base de datos.\
🛡 **Control de acceso:** Requiere token JWT válido y rol `designer`. Si el usuario no tiene permisos, se muestra un mensaje de "No autorizado".

**Funcionalidades disponibles desde el panel:**

* **🔍 Ver últimos logs del sistema:**\
  Redirecciona al formulario `verLogs.jsp` vía `POST`.
* **🧪 Insertar nuevos laboratorios:**\
  Redirecciona a `agregarLaboratorio.jsp`, donde se puede crear un nuevo laboratorio con nombre, flag y puntos.
* **📊 Visualizar tablas de la base de datos:**\
  Enlace a `viewTables.jsp` para inspeccionar tablas del backend.
* **🛠 Insertar / Eliminar / Modificar tablas:**\
  Redirecciona a `manageTables.jsp` para una gestión más profunda sobre la base de datos.
* **🔙 Volver al home:**\
  Redirige a `home.jsp?page=0`.

**Código relevante:**

```jsp
if (!"designer".equals(rol)) {
    out.println("<div class='error-message'>No autorizado.</div>");
    return;
}
```

***

#### 🗂 **Vista `agregarLaboratorio.jsp`**

📁 **Ubicación:** `designer/agregarLaboratorio.jsp`\
🔍 **Propósito:** Formulario visual para registrar un nuevo laboratorio en la base de datos.\
🧠 **Responsabilidad principal:** Enviar datos al endpoint `agregarLaboratorio` con nombre, flag y puntos.\
🎯 **Método HTTP:** `POST`\
🎨 **Estilo:** Tema oscuro con diseño centrado y tipografía tipo terminal (Courier).

**Campos del formulario:**

* **📌 Nombre del laboratorio:**\
  Campo de texto requerido (`nombre`).
* **🚩 Flag:**\
  Campo de texto requerido (`flag`).
* **⭐ Puntos:**\
  Campo numérico requerido (`puntos`).

**Funcionalidades adicionales:**

* **💬 Mensaje de éxito:**\
  Si el atributo `mensaje` está presente en la request (por ejemplo, tras insertar un laboratorio con éxito), se muestra como mensaje destacado.
* **🔙 Botón para volver al panel:**\
  Enlace estilizado que lleva de vuelta a `admin-panel.jsp`.

**Código destacado:**

```jsp
<form action="<%= request.getContextPath() %>/agregarLaboratorio" method="POST">
```

#### ✅ `manageTables.jsp` – **Gestión de Tablas**

📁 **Ubicación:** `designer/manageTables.jsp`

**🧠 Qué hace:**

* Verifica si el usuario es `designer`.
* Permite ver, insertar, actualizar y eliminar registros de cualquier tabla en la base de datos.
* Usa `TablaDAO` para operaciones de lectura.

**🛡️ Seguridad:**

* ✅ Autenticación y autorización con `JWTUtils`.
* ⚠️ **Peligro potencial:** no hay validación de los valores insertados/actualizados directamente desde el formulario.
* ⚠️ La detección de la clave primaria es manual y limitada (`id` o `lab_id`). Esto puede fallar para otras tablas.
* ⚠️ **Injection risk:** si `TablaController` no realiza validación/escapado, se expone a SQL Injection.

**🎨 UX/UI:**

* Muy funcional pero el diseño puede saturar si hay muchas columnas o filas.
* Los formularios de update se mezclan con los de lectura, lo que puede resultar algo confuso.

**💡 Sugerencias:**

* Extraer la clave primaria desde `DAO.getPrimaryKey(tabla)`.
* Añadir confirmación JavaScript para eliminar registros.
* Separar UI de edición (popup/modal o nueva sección).
* Validar y sanitizar inputs tanto en frontend como backend.

***

#### ✅ `verLogs.jsp` – **Visualización de Logs**

📁 **Ubicación:** `designer/verLogs.jsp`

**🧠 Qué hace:**

* Realiza polling AJAX cada 5 segundos a `/getLogs` para mostrar los últimos logs.
* Interfaz muy minimalista.

**🛡️ Seguridad:**

* ⚠️ No verifica autorización del usuario en este JSP directamente (aunque el acceso es desde un panel restringido).
* ⚠️ Si `/getLogs` no valida el rol, cualquier usuario podría explotarlo.

**🎨 UX/UI:**

* Simple y efectivo.
* Autoscroll al final es útil, pero puede ser molesto en logs muy largos.

**💡 Sugerencias:**

* Validar en el servlet `/getLogs` que el usuario sea `designer`.
* Añadir control para pausar la actualización automática.
* Añadir filtros por nivel de log, fecha, etc.

***

#### ✅ `viewTables.jsp` – **Vista general de las tablas**

📁 **Ubicación:** `designer/viewTables.jsp`

**🧠 Qué hace:**

* Carga dinámicamente la estructura de la base de datos vía `/getTables`.
* Muestra todo en un `div` con AJAX.

**🛡️ Seguridad:**

* ✅ Autenticación y autorización correcta.
* ⚠️ Verificar que `/getTables` haga validación del token.

**🎨 UX/UI:**

* Interfaz sencilla. La carga AJAX está bien pensada.
* Puede ser útil un spinner o animación mientras carga.

**💡 Sugerencias:**

* Añadir botón de “Recargar” o autorefresco opcional.
* Agregar capacidad de exportar a CSV/JSON.
* Visualización más amigable si hay muchas columnas.

***

#### Conclusión general 🔍

| Archivo            | Autenticación | Validación | Mejora crítica                 |
| ------------------ | ------------- | ---------- | ------------------------------ |
| `manageTables.jsp` | ✅             | ⚠️         | Evitar SQL Injection           |
| `verLogs.jsp`      | ⚠️            | ⚠️         | Validar acceso en `/getLogs`   |
| `viewTables.jsp`   | ✅             | ⚠️         | Validar acceso en `/getTables` |

#### 📊 **Página de Progreso del Usuario**

📁 **Ubicación:** `webapp/progreso.jsp`\
🔍 **Propósito:** Mostrar el progreso del usuario en diferentes laboratorios mediante gráficos y puntuaciones.\
🧠 **Responsabilidad principal:** Visualizar el avance del usuario autenticado y mostrar su foto de perfil, junto a una gráfica tipo _pie chart_ de puntuaciones.

**Lógica del backend embebida en JSP:**

* Autenticación mediante `JWTUtils` para obtener el objeto `UsuarioJWT`.
* Validación del `userId`.
* Obtención de la ruta de la foto del perfil vía `FotoDAO`.
* Si no hay foto, se establece una por defecto (`img/Profile.png`).
* Formulario oculto que envía `userId` vía POST para actualizar los puntos.

**Interfaz:**

* Foto de perfil del usuario.
* Gráfico circular (_Chart.js_) que representa puntuaciones individuales por laboratorio:
  * `foro-xss`, `amashop`, `separo`, `hacking_community`, `RCE`, `LFI`, `IDOR`
* Sección de puntuaciones individuales y totales por categoría.
* Botón para exportar a PDF (pendiente de implementación JS).

***

#### 🏆 **Ranking de Usuarios**

📁 **Ubicación:** `webapp/ranking.jsp`\
🔍 **Propósito:** Mostrar un ranking con los usuarios y sus puntos totales ordenados de mayor a menor.\
🧠 **Responsabilidad principal:** Visualizar en tabla los resultados de todos los usuarios obtenidos desde el controlador `RankingControlador`.

**Lógica del backend embebida en JSP:**

* Autenticación mediante `JWTUtils`.
* Llamada a `RankingControlador.obtenerRankingUsuarios()`.
* Iteración de la lista para mostrar los datos.

**Estética especial para los top 3:**

* 🥇 Oro → posición 1
* 🥈 Plata → posición 2
* 🥉 Bronce → posición 3

**Interfaz:**

* Tabla con tres columnas: `Posición`, `Usuario`, `Puntos Totales`.
* Botón para volver al home.

***

#### 📝 **Página de Envío de Writeups (Ranking en contexto de envíos)**

📁 **Ubicación:** `webapp/sendWriteups.jsp`\
🔍 **Propósito:** Mostrar el mismo ranking de usuarios como parte de la interfaz de envío de writeups.\
🧠 **Responsabilidad principal:** Reutilizar lógica de ranking dentro del entorno de envío de soluciones.

**Lógica:**

* Igual que `ranking.jsp`: se obtiene el usuario con JWT y luego el ranking.
* Diferencia: esta página se usará en contexto de envío de writeups.

**Interfaz:**

* Tabla de ranking con los mismos estilos (oro, plata, bronce).
* Botón para volver al inicio.

***

#### 📚 **Tabla de Writeups del Laboratorio**

📁 **Ubicación:** `webapp/tablaWriteups.jsp`\
🔍 **Propósito:** Mostrar todos los writeups disponibles para un laboratorio específico.\
🧠 **Responsabilidad principal:** Mostrar una tabla con los writeups enviados por usuarios sobre un laboratorio específico.

**Lógica:**

* Autenticación con `JWTUtils`.
* Se obtiene el atributo `writeups` desde la request (establecido por un servlet controlador).
* Se extrae el nombre del laboratorio del primer writeup (si existe).
* Se recorre la lista `writeups` para armar la tabla.

**Interfaz:**

* Tabla HTML con estilo retro tipo terminal.
* Columnas con información del writeup (no detallado aún en tu código, pero probablemente autor, fecha, link).
* Colores oscuros con verde neón y hover destacando filas.

#### 🖥️ **Vista JSP: separo.jsp**

📁 **Ubicación:** `labs/separo/separo.jsp`\
🔍 **Propósito:** Mostrar el portal principal del laboratorio **SEPARO**, simulando una interfaz institucional donde los usuarios pueden acceder a recursos, enviar writeups, o validar flags.\
🧠 **Responsabilidad principal:**\
Cargar dinámicamente los datos del usuario autenticado mediante JWT, obtener el `labId` desde la base de datos, y renderizar el contenido visual del laboratorio.

**🛠️ Dependencias Importadas:**

* `utils.JWTUtils` → Para autenticar al usuario y recuperar su información desde la cookie JWT.
* `utils.UsuarioJWT` → Modelo que representa al usuario autenticado.
* `dao.LaboratorioDAO` → Acceso a la base de datos para obtener el ID del laboratorio SEPARO.

***

**⚙️ Lógica Principal en Scriptlet JSP:**

* **Autenticación JWT:**

```jsp
UsuarioJWT usuarioJWT = JWTUtils.obtenerUsuarioDesdeRequest(request);
```

🔐 Recupera y valida el token del usuario desde las cookies.\
⚠️ Si el token no es válido o ha expirado, redirige automáticamente al servlet de logout.

* **Obtención de ID del laboratorio:**

```jsp
int labId = LaboratorioDAO.obtenerIdLaboratorioSeparo();
```

📌 Permite identificar de forma única el laboratorio SEPARO en la base de datos.

* **Manejo de mensajes desde la URL:**

```jsp
String resultadoFlag = request.getParameter("mensaje");
```

📨 Recupera posibles mensajes (como éxito/error al enviar FLAG) desde los parámetros GET.

***

**🧩 Componentes Interactivos:**

* **Botón "Enviar Writeup / FLAG"**\
  📤 Abre un popup modal donde el usuario puede:
  * Enviar un enlace a su writeup (POST).
  * Enviar una FLAG del laboratorio (GET).
* **Botón "Ver Writeups"**\
  📚 Redirige a la vista `verWriteups`, mostrando los writeups de este laboratorio.
* **Popup emergente de mensaje:**\
  🔔 Muestra feedback dinámico (por ejemplo, resultado al validar FLAG).

***

**🎨 Estilos destacados en CSS:**

* **Diseño responsivo y accesible:**\
  Se adapta a pantallas móviles y de escritorio.
* **Colores institucionales:**\
  Predominan azul oscuro (`#003366`, `#002855`) y amarillo dorado (`#ffd700`).
* **Estilo profesional con sombras, bordes redondeados y animaciones suaves.**

***

**🧠 Notas Técnicas:**

* Se evita el uso de lógica compleja en la vista. Toda la autenticación y recuperación de datos se hace con clases utilitarias externas.
* Usa `<%= usuarioJWT.getUsuario() %>` y otros métodos para mostrar valores dinámicos desde el objeto `UsuarioJWT`.
* El popup modal reutiliza formularios seguros con `hidden inputs` que validan tanto `user_id`, `username` y `lab_id`.
