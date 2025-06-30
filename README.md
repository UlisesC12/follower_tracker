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

## Automatización con Cron

Para ejecutar este script automáticamente todos los días en tu VPS, puedes usar un "cron job". Cron es un sistema que permite ejecutar comandos en un horario programado.

1.  **Abre el editor de cron:**
    En la terminal de tu VPS, ejecuta el siguiente comando. Si es la primera vez, puede que te pida elegir un editor de texto (elige `nano`, es el más sencillo).
    ```bash
    crontab -e
    ```

2.  **Añade una nueva tarea:**
    Ve al final del archivo y añade la siguiente línea. Esta línea ejecutará el script `tracker.py` todos los días a las 9:00 AM.

    ```cron
    0 9 * * * /home/user/follower_tracker/venv/bin/python /home/user/follower_tracker/tracker.py >> /home/user/follower_tracker/tracker.log 2>&1
    ```

    **¡MUY IMPORTANTE!** Debes reemplazar `/home/user/follower_tracker` con la ruta **absoluta y real** donde has clonado tu proyecto en el **VPS**.

    **Desglose del comando:**
    *   `0 9 * * *`: Esto significa "a los 0 minutos, a las 9 horas, todos los días del mes, todos los meses, todos los días de la semana".
    *   `/home/user/follower_tracker/venv/bin/python`: Es la ruta al ejecutable de Python **dentro de tu entorno virtual**. Esto asegura que se usan las librerías correctas (Playwright, etc.).
    *   `/home/user/follower_tracker/tracker.py`: Es la ruta a tu script principal.
    *   `>> /home/user/follower_tracker/tracker.log 2>&1`: Esto es opcional pero **muy recomendado**. Redirige toda la salida (tanto los `print` como los errores) a un archivo `tracker.log`. Así, si algo falla, tendrás un registro para ver qué ha pasado.

3.  **Guarda y cierra:**
    *   Si usas `nano`, presiona `Ctrl + X`, luego `Y` (para sí) y `Enter`.

¡Y listo! Tu VPS ejecutará el script por ti cada mañana. 