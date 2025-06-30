from database import get_db_connection, insert_follower_count, get_accounts_to_track
from scrapers.x_scraper import get_x_follower_count
import re

def get_username_from_url(url: str) -> str | None:
    """Extrae el nombre de usuario de una URL de perfil de X.com."""
    if not url:
        return None
    # Elimina cualquier query string o fragmento y una posible barra al final
    base_url = url.split('?')[0].split('#')[0].rstrip('/')
    # Obtiene la última parte de la ruta, que debe ser el username
    if base_url.count('/') > 2:
        return base_url.split('/')[-1]
    return None

def main():
    """
    Script principal para orquestar el seguimiento de seguidores.
    1. Obtiene las cuentas a rastrear desde la base de datos.
    2. Para cada cuenta, obtiene los datos de la red social.
    3. Guarda los datos en la base de datos.
    """
    print("--- Iniciando Follower Tracker ---")
    
    accounts = get_accounts_to_track()
    if not accounts:
        print("No hay cuentas configuradas en la base de datos para rastrear. Saliendo.")
        return

    # Abrimos una única conexión a la BD para todas las inserciones
    conn = get_db_connection()
    if conn is None:
        print("No se pudo establecer la conexión con la base de datos. Saliendo.")
        return

    try:
        for account in accounts:
            platform_name = account.get('name')
            profile_url = account.get('profile_url')
            
            print(f"\n--- Procesando cuenta: {platform_name} | URL: {profile_url} ---")

            follower_count = None
            
            # --- Lógica de selección de Scraper ---
            if platform_name.lower() == 'x': # Asumiendo que el nombre en tu BD es 'x'
                username = get_username_from_url(profile_url)
                if not username:
                    print(f"No se pudo extraer el nombre de usuario de la URL: {profile_url}")
                    continue 
                
                follower_count = get_x_follower_count(username)
            else:
                print(f"Plataforma '{platform_name}' no soportada por ningún scraper.")
                continue

            # --- Inserción en Base de Datos ---
            if follower_count is not None:
                insert_follower_count(conn, platform_name, follower_count)
            else:
                print(f"No se pudo obtener el recuento de seguidores para {profile_url}. No se insertará en la BD.")

    finally:
        if conn is not None:
            conn.close()
            print("\nConexión a la base de datos cerrada.")

    print("\n--- Proceso de seguimiento completado ---")

if __name__ == "__main__":
    main()