---
icon: object-exclude
layout:
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
---

# Deserialización Insegura (PHP, Python y Java)

## **Deserialización Insegura en PHP**

> Explotación de ejemplo (`PHP`) = [LINK EJEMPLO](deserializacion-insegura-php-python-y-java.md#deserializacion-insegura-en-php)

#### **Descripción General**

La deserialización insegura en PHP ocurre cuando datos no confiables (provenientes de un atacante o fuentes no verificadas) son deserializados sin la debida validación. En el contexto del código PHP proporcionado, el problema radica en el manejo de objetos de la clase **Vulnerable** y cómo se ejecuta el destructor del objeto al deserializarlo.

#### **Flujo de Ataque**

1. **Instanciación del objeto**: En el código, se crea un objeto de la clase **Vulnerable**, que tiene una propiedad **$cmd** que contiene un comando.
2. **Serialización y almacenamiento**: El objeto se serializa y se almacena en una cookie en el navegador del usuario.
3. **Manipulación del atacante**: Un atacante puede modificar esta cookie para insertar un objeto **Vulnerable** con un comando malicioso en **$cmd**.
4. **Deserialización en el servidor**: Cuando el servidor recibe la cookie en futuras solicitudes, deserializa el objeto. Al hacerlo, el destructor (**\_\_destruct()**) se ejecuta automáticamente, ejecutando el comando malicioso.

#### **Riesgos**

* **Ejecución de código arbitrario**: El atacante puede ejecutar comandos arbitrarios en el servidor.
* **Acceso no autorizado**: El atacante puede obtener acceso a información sensible o incluso comprometer el sistema completo.

#### **Soluciones**

* Evitar deserializar datos provenientes de fuentes no confiables, como cookies o parámetros en la URL.
* Usar métodos más seguros de almacenamiento, como **JSON Web Tokens** ([JWT](https://en.wikipedia.org/wiki/JSON_Web_Token)).
* Validar y sanear todos los datos antes de procesarlos.

***

## **Deserialización Insegura en Python**

#### **Descripción General**

En Python, la deserialización insegura ocurre cuando se utiliza la función **pickle** para deserializar datos sin precauciones adecuadas. **Pickle** permite ejecutar código arbitrario durante la deserialización, lo que puede ser aprovechado por un atacante para ejecutar código malicioso.

#### **Flujo de Ataque**

1. Un atacante envía un archivo manipulado usando **pickle**, que contiene un objeto malicioso.
2. Al deserializar este objeto en la aplicación Python, el código malicioso contenido en él se ejecuta, lo que puede incluir la ejecución de comandos o funciones peligrosas.

#### **Riesgos**

* **Ejecución remota de código**: Un atacante puede ejecutar código arbitrario en el servidor.
* **Robo de información sensible**: El atacante puede obtener acceso a información confidencial almacenada en el sistema.

#### **Soluciones**

* Evitar el uso de **pickle** para deserializar datos provenientes de fuentes no confiables.
* Utilizar bibliotecas más seguras como **json** para la serialización y deserialización de datos.
* Validar y verificar todo dato deserializado antes de usarlo en el sistema.

***

## \*\*Deserialización Insegura en Java con Apache Commons

#### **Descripción General**

La deserialización insegura en Java ocurre cuando se deserializan objetos que contienen código malicioso. En este caso, herramientas como **ysoserial** se pueden usar para generar objetos maliciosos que, al ser deserializados, ejecutan código en el servidor.

#### \*\*Flujo de Ataque Paso a Paso

1. **Identificación de la vulnerabilidad**: La vulnerabilidad se encuentra cuando una aplicación web Java recibe una cookie de sesión que contiene un objeto Java serializado. Si este objeto es deserializado sin validación, un atacante puede inyectar código malicioso.
2.  **Uso de ysoserial**:

    * **Ysoserial** es una herramienta que genera objetos maliciosos que explotan vulnerabilidades de deserialización.
    * El atacante puede crear un objeto serializado que contenga un **payload** malicioso. Este payload podría ser, por ejemplo, un comando para eliminar un archivo en el sistema.

    Ejemplo de comando para generar el payload:

```shell
java \
   --add-opens=java.xml/com.sun.org.apache.xalan.internal.xsltc.trax=ALL-UNNAMED \
   --add-opens=java.xml/com.sun.org.apache.xalan.internal.xsltc.runtime=ALL-UNNAMED \
   --add-opens=java.base/java.net=ALL-UNNAMED \
   --add-opens=java.base/java.util=ALL-UNNAMED \
   -jar ysoserial-all.jar CommonsCollections4 'rm /home/carlos/morale.txt' | base64  
```

* **ysoserial-all.jar**: Herramienta que genera objetos maliciosos.
* **CommonsCollections4**: Una cadena de clases de **Apache Commons Collections** utilizadas para inyectar el payload.
* **'rm /home/carlos/morale.txt'**: El payload malicioso que se ejecutará cuando se deserialice el objeto (en este caso, eliminar un archivo).
* **base64**: Codificación para transmitir el objeto de manera segura a través de HTTP.

3. **Envío del payload al servidor**: El atacante envía el objeto serializado, codificado en base64, dentro de una cookie al servidor.
4. **Explotación**: Cuando el servidor recibe el objeto deserializado, el código malicioso en el payload se ejecuta automáticamente.

#### **Riesgos**

* **Ejecución remota de código**: El atacante puede ejecutar comandos en el servidor, lo que puede comprometer completamente el sistema.
* **Acceso a sistemas críticos**: El atacante puede obtener acceso a información sensible o modificar configuraciones críticas del sistema.

#### **Soluciones**

* Desactivar la deserialización de objetos de fuentes no confiables, como cookies o entradas de usuario.
* Utilizar bibliotecas seguras para evitar el uso de componentes vulnerables como **CommonsCollections**.
* Verificar y validar todos los objetos antes de deserializarlos, asegurándose de que provienen de fuentes confiables.

***

### **Resumen de las Vulnerabilidades**

* **PHP**: Deserializar objetos sin validación adecuada puede permitir a un atacante ejecutar comandos arbitrarios.
* **Python**: Deserializar datos manipulados con **pickle** puede ejecutar código malicioso al cargar un objeto modificado.
* **Java (con Apache Commons)**: Al deserializar objetos Java, un atacante puede inyectar un payload malicioso que se ejecutará automáticamente al deserializarse el objeto.

***

### **Conclusión**

La deserialización insegura es una vulnerabilidad crítica que afecta a diversas plataformas como **PHP**, **Python** y **Java**. La prevención de estos ataques requiere no deserializar datos de fuentes no confiables, usar mecanismos seguros para manejar sesiones, y validar rigurosamente los datos antes de procesarlos. La clave para proteger las aplicaciones contra estos ataques es adoptar buenas prácticas de seguridad en el manejo de objetos serializados.
