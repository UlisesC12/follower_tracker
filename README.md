# Follower Tracker

Este proyecto es un script de Python diseñado para rastrear el número de seguidores de una cuenta de red social a lo largo del tiempo y almacenar los datos en una base de datos PostgreSQL.

## Configuración del Entorno

Sigue estos pasos para configurar y ejecutar el proyecto localmente.

### 1. Prerrequisitos

- Python 3
- Una base de datos PostgreSQL accesible remotamente (por ejemplo, en un VPS).

### 2. Crear Entorno Virtual

Se recomienda encarecidamente usar un entorno virtual para gestionar las dependencias del proyecto.

```bash
# Crear el entorno virtual
python3 -m venv venv

# Activar el entorno virtual
# En macOS/Linux:
source venv/bin/activate
# En Windows:
# venv\Scripts\activate
```

### 3. Instalar Dependencias

Con el entorno virtual activado, instala las librerías necesarias desde `pip`.

```bash
pip install psycopg2-binary python-dotenv
```
- `psycopg2-binary`: Es el adaptador de PostgreSQL para Python, necesario para conectarse a la base de datos.
- `python-dotenv`: Se utiliza para cargar variables de entorno desde un archivo `.env`, manteniendo las credenciales seguras y fuera del código fuente.

### 4. Configurar Variables de Entorno

Para que el script se conecte a la base de datos, necesita credenciales. Por seguridad, estas se gestionan a través de un archivo `.env`.

Crea un archivo llamado `.env` en la raíz del proyecto con el siguiente contenido:

```
DB_HOST=localhost
DB_PORT=5433
DB_NAME=nombre_de_tu_db
DB_USER=usuario_de_tu_db
DB_PASSWORD="tu_contraseña_segura"
```
**Importante:** El archivo `.gitignore` ya está configurado para ignorar `.env`, por lo que tus credenciales nunca se subirán a un repositorio de Git.

### 5. Conexión Segura con Túnel SSH

Para evitar exponer el puerto de tu base de datos a internet, nos conectamos de forma segura a través de un túnel SSH.

1.  Abre una terminal y ejecuta el siguiente comando. Esto creará una "tubería" segura desde el puerto `5433` de tu máquina local al puerto `5432` de tu servidor.

    ```bash
    ssh -L 5433:localhost:5432 tu_usuario_ssh@ip_de_tu_vps
    ```
2.  Ingresa tu contraseña de SSH para el VPS y **deja esta terminal abierta**. El túnel se cerrará si cierras la sesión.

### 6. Ejecutar el Script

Con el túnel SSH activo en una terminal y el entorno virtual activado en otra, ya puedes ejecutar el script principal.

```bash
python tracker.py
```

Si todo está configurado correctamente, verás un mensaje de "Conexión exitosa" seguido de la versión de tu base de datos PostgreSQL.

## Solución de Problemas

- **`Connection refused`**: Generalmente significa que el túnel SSH no está activo o no apunta al host/puerto correcto. Asegúrate de que `DB_HOST` en tu `.env` sea `localhost`.
- **`fe_sendauth: no password supplied`**: El script no está cargando la contraseña. Asegúrate de que la variable `DB_PASSWORD` existe en tu `.env` y no está definida en tu terminal (`unset DB_PASSWORD`).
- **`password authentication failed`**: La conexión es exitosa, pero la contraseña en tu `.env` es incorrecta.
- **Caracteres especiales en la contraseña**: Si tu contraseña contiene caracteres como `*`, `%`, `#`, etc., asegúrate de envolverla en comillas dobles en el archivo `.env` (ej. `DB_PASSWORD="mi#pass*word"`). 