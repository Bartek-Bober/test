import os
import psycopg2
from dotenv import load_dotenv


load_dotenv()

def main():
   
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")

    connection = None
    cursor = None

    try:
      
        print("Nawiązywanie połączenia z bazą danych...")
        connection = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password
        )
       
        connection.autocommit = True
        cursor = connection.cursor()
        print("Połączono pomyślnie!\n")

       
        print("Tworzenie tabeli 'messages'...")
        create_table_query = """
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            content VARCHAR(255) NOT NULL
        );
        """
        cursor.execute(create_table_query)

   
        message_to_insert = "Hello World z Pythona i PostgreSQL!"
        print(f"Wstawianie wiadomości: '{message_to_insert}'...")
        insert_query = "INSERT INTO messages (content) VALUES (%s);"
        cursor.execute(insert_query, (message_to_insert,))

        print("Pobieranie wiadomości z bazy...")
        select_query = "SELECT id, content FROM messages ORDER BY id DESC LIMIT 1;"
        cursor.execute(select_query)
        record = cursor.fetchone()
        
        if record:
            print(f">>> Ostatnia wiadomość w bazie (ID: {record[0]}): {record[1]}\n")

    except psycopg2.Error as e:
        print(f"Wystąpił błąd podczas pracy z bazą danych: {e}")

    finally:
       
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("Połączenie z bazą danych zostało zamknięte.")

if __name__ == "__main__":
    main()