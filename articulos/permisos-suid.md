---
icon: magnifying-glass-arrow-right
---

# Permisos SUID

Para encontrar archivos con permisos _SUID_ en un sistema Linux/Unix, puedes utilizar el siguiente comando:

```bash
find / -type f -perm -4000 -ls 2>/dev/null
```

#### Explicación paso a paso:

* **`find /`**: Inicia la búsqueda desde la raíz del sistema (`/`), lo que significa que revisará todo el sistema de archivos.
* **`-type f`**: Limita la búsqueda a solo archivos (_f_ de _file_), excluyendo directorios, enlaces simbólicos, etc.
* **`-perm -4000`**: Busca archivos que tengan el permiso especial _SUID_ (Set User ID). Este permiso, representado por el número 4000, permite que el archivo se ejecute con los privilegios del propietario, no del usuario que lo ejecuta. Es un permiso sensible y debe ser monitoreado.
* **`-ls`**: Muestra información detallada de los archivos encontrados, como su tamaño, permisos, propietario, fecha de modificación, etc.
* **`2>/dev/null`**: Redirige cualquier error (como problemas de acceso a directorios restringidos) a un "agujero negro" (`/dev/null`), de manera que no se muestren en la salida.

## <mark style="color:purple;">¿Qué conseguimos con este comando?</mark>

Este comando nos permite listar todos los archivos en el sistema que tienen el permiso _SUID_ activado, lo cual es importante para auditar la seguridad, ya que archivos con este permiso pueden ser utilizados para ejecutar procesos con privilegios elevados.

Este comando es útil cuando queremos asegurarnos de que no haya archivos con permisos _SUID_ innecesarios o peligrosos en el sistema.
