import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
  """Establece y devuelve una conexión a la base de datos PostgreSQL."""
  try:
    conn = psycopg2.connect(
      host=os.getenv("DB_HOST"),
      port=os.getenv("DB_PORT"),
      database=os.getenv("DB_NAME"),
      user=os.getenv("DB_USER"),
      password=os.getenv("DB_PASSWORD")
    )
    return conn
  except psycopg2.OperationalError as e:
    print(f"Error al conectar a la base de datos: {e}")
    return None

def get_accounts_to_track():
    """
    Obtiene todas las cuentas configuradas para seguimiento desde la tabla social_platforms.
    Devuelve una lista de diccionarios, cada uno con 'name' y 'profile_url'.
    """
    conn = get_db_connection()
    if conn is None:
        return []

    accounts = []
    try:
        cur = conn.cursor()
        # Seleccionamos solo las plataformas que tienen una URL de perfil configurada
        cur.execute("SELECT name, profile_url FROM social_platforms WHERE profile_url IS NOT NULL AND profile_url != ''")
        rows = cur.fetchall()
        for row in rows:
            accounts.append({'name': row[0], 'profile_url': row[1]})
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error al obtener las cuentas a seguir: {error}")
    finally:
        if conn is not None:
            conn.close()
    
    print(f"Se encontraron {len(accounts)} cuentas para rastrear en la base de datos.")
    return accounts

def insert_follower_count(conn, platform_name: str, count: int):
    """
    Inserta un nuevo registro de recuento de seguidores.
    Primero, busca el ID de la plataforma y luego inserta en follower_counts.
    """
    try:
        cur = conn.cursor()
        
        # 1. Obtener el platform_id desde el nombre de la plataforma
        print(f"Buscando ID para la plataforma: '{platform_name}'")
        cur.execute("SELECT id FROM social_platforms WHERE name = %s", (platform_name,))
        platform_row = cur.fetchone()
        
        if platform_row is None:
            print(f"Error: No se encontró la plataforma '{platform_name}' en la tabla social_platforms.")
            cur.close()
            return

        platform_id = platform_row[0]
        print(f"ID de plataforma encontrado: {platform_id}")

        # 2. Insertar el recuento en la tabla follower_counts
        # La columna 'recorded_at' usará su valor por defecto (now())
        print(f"Insertando registro en 'follower_counts': (platform_id: {platform_id}, count: {count})")
        cur.execute(
            "INSERT INTO follower_counts (platform_id, count) VALUES (%s, %s)",
            (platform_id, count)
        )
        
        conn.commit()
        print("Registro insertado con éxito.")
        
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error en la operación de base de datos: {error}") 