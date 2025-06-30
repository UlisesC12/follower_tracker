# Follower Tracker

Este proyecto es un script de Python diseñado para rastrear automáticamente el número de seguidores de perfiles en redes sociales (actualmente X/Twitter) y almacenar un registro histórico en una base de datos PostgreSQL.

El sistema está diseñado para ser desplegado en un servidor (VPS) y ejecutarse de forma autónoma mediante un cron job.

## Estructura del Proyecto

-   `tracker.py`: Script principal que orquesta todo el proceso. Obtiene las cuentas a seguir desde la base de datos, llama al scraper correspondiente y guarda el resultado.
-   `database.py`: Módulo que gestiona toda la interacción con la base de datos PostgreSQL.
-   `scrapers/x_scraper.py`: Módulo que contiene la lógica de scraping para X/Twitter, utilizando la librería Playwright.
-   `requirements.txt`: Archivo que lista todas las dependencias de Python necesarias para el proyecto.
-   `.env`: Archivo (local, no versionado) para almacenar credenciales y variables de entorno.
-   `README.md`: Este archivo.

---

## 1. Configuración Local (Para desarrollo y pruebas)

Sigue estos pasos para ejecutar el proyecto en tu máquina local.

### 1.1. Prerrequisitos

-   Python 3
-   Una base de datos PostgreSQL accesible (puede ser local o remota).

### 1.2. Instalación

1.  **Clona el repositorio:**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd follower_tracker
    ```

2.  **Crea y activa un entorno virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Crea el archivo `requirements.txt`:**
    La mejor práctica es usar `pip freeze` para generar este archivo, ya que captura las versiones exactas de todas las librerías, garantizando consistencia entre entornos.
    ```bash
    pip freeze > requirements.txt
    ```
    *Nota: Si ya tienes el archivo del repositorio, puedes saltar este paso.*

4.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Instala los navegadores de Playwright:**
    ```bash
    playwright install
    ```

### 1.3. Configuración del `.env` local

Crea un archivo `.env` en la raíz del proyecto para conectar el script a tu base de datos. Si te conectas a una base de datos remota (en un VPS), la forma más segura de hacerlo es a través de un **túnel SSH**.

1.  **Abre el túnel SSH en una terminal:**
    Este comando crea un "puente" seguro desde el puerto `5433` de tu máquina al puerto `5432` del servidor. **Deja esta terminal abierta.**
    ```bash
    ssh -L 5433:localhost:5432 tu_usuario_ssh@ip_de_tu_vps
    ```

2.  **Configura tu archivo `.env`:**
    Como el túnel está activo, tu script se conectará a `localhost` en el puerto `5433`.
    ```
    DB_HOST=localhost
    DB_PORT=5433
    DB_NAME=nombre_de_tu_db
    DB_USER=usuario_de_tu_db
    DB_PASSWORD="tu_contraseña_segura"
    ```

### 1.4. Ejecución
Con el túnel activo y el entorno virtual activado, ejecuta el script:
```bash
python tracker.py
```

---

## 2. Despliegue en Servidor (VPS)

Estos pasos detallan cómo desplegar el proyecto para que se ejecute de forma autónoma.

### 2.1. Preparar el Servidor

1.  **Conéctate a tu VPS por SSH.**

2.  **Crea un usuario no-root (Muy Recomendado):**
    Por seguridad, no ejecutes aplicaciones desde el usuario `root`.
    ```bash
    # Crea un nuevo usuario (ej. 'ulises')
    adduser ulises
    # Dale permisos de administrador (sudo)
    usermod -aG sudo ulises
    # Inicia sesión como el nuevo usuario
    su - ulises
    ```

3.  **Instala las herramientas necesarias:**
    ```bash
    sudo apt update && sudo apt install git python3-venv -y
    ```

### 2.2. Clonar el Repositorio

1.  **Navega al directorio `home` de tu nuevo usuario (`cd ~`).**

2.  **Clona el proyecto.** Tienes dos opciones:
    *   **HTTPS (más simple):** `git clone https://github.com/tu_usuario/tu_repo.git`
    *   **SSH (más seguro):** `git clone git@github.com:tu_usuario/tu_repo.git`
        *Si usas SSH y recibes `Permission denied (publickey)`, debes generar una clave SSH en tu VPS con `ssh-keygen` y añadir la clave pública a tu perfil de GitHub.*

### 2.3. Configurar el Entorno en el VPS

1.  **Entra en la carpeta del proyecto:** `cd follower_tracker`

2.  **Crea y activa el entorno virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instala dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Instala Playwright y sus dependencias de sistema:**
    Este es un paso crucial en servidores sin interfaz gráfica.
    ```bash
    playwright install --with-deps chromium
    ```
    *`--with-deps` instala todas las librerías de Linux necesarias para que el navegador funcione.*

### 2.4. Configuración del `.env` en el VPS

Crea el archivo `.env` en el servidor (`nano .env`). **¡La configuración es diferente a la local!**

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=follower_tracker
DB_USER=postgres
DB_PASSWORD="tu_contraseña"
```
*   **¿Por qué el puerto `5432`?** Porque ahora el script se ejecuta en la misma máquina que la base de datos. Ya no necesita el túnel SSH, por lo que se conecta directamente al puerto por defecto de PostgreSQL.

---

## 3. Automatización con `cron`

`cron` es el sistema que ejecutará tu script automáticamente.

### 3.1. Editar el `crontab`
Abre el editor de tareas de `cron` para tu usuario:
```bash
crontab -e
```
*Si es la primera vez, elige `nano` como editor.*

### 3.2. Añadir la Tarea

Añade la siguiente línea al final del archivo. Esta línea está diseñada para ser robusta y explícita.

```cron
# Ejecutar el tracker de seguidores todos los días a las 4:00 AM
0 4 * * * cd /home/ulises/follower_tracker && /home/ulises/follower_tracker/venv/bin/python -u /home/ulises/follower_tracker/tracker.py >> /home/ulises/follower_tracker/tracker.log 2>&1
```
**¡Asegúrate de cambiar `/home/ulises/` por la ruta a tu directorio home!**

### 3.3. Desglose del Comando `cron`

-   **`0 4 * * *`**: El horario. "A las 4:00 AM, todos los días". Para probar cada minuto, usa `* * * * *`.
-   **`cd /home/ulises/follower_tracker &&`**: **Paso 1: Ubicación.** Primero, `cron` se mueve a la carpeta del proyecto. Esto es vital para que el script encuentre el `.env`.
-   **`/home/ulises/follower_tracker/venv/bin/python -u`**: **Paso 2: Intérprete.** Se usa la ruta **absoluta** al ejecutable de Python dentro del `venv` para asegurar que se usan las librerías correctas. El flag `-u` deshabilita el buffer de salida, haciendo que los logs se escriban en tiempo real.
-   **`/home/ulises/follower_tracker/tracker.py`**: **Paso 3: Script.** La ruta **absoluta** al script que se va a ejecutar.
-   **`>> /home/ulises/follower_tracker/tracker.log 2>&1`**: **Paso 4: Logging.** Redirige toda la salida (tanto `print` como errores) a un archivo `tracker.log` para poder revisar la ejecución y depurar si algo falla. 