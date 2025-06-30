import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
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
  
def main():
  print("Iniciando tracker...")
  conn = get_db_connection()

  if conn is None:
    print("No se pudo establecer la conexión. Revisa tus variables de entorno en el archivo .env")
    return

  try:
    cur = conn.cursor()

    print("Conexión exitosa. Versión de PostgreSQL:")
    cur.execute("SELECT version();")
    db_version = cur.fetchone()
    print(db_version)

    # Aquí irá tu lógica de tracking
    
    cur.close()

  except (Exception, psycopg2.DatabaseError) as error:
    print(error)
  finally:
    if conn is not None:
      conn.close()
      print("Conexión a la base de datos cerrada.")

if __name__ == "__main__":
  main()