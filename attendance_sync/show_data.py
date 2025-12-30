import pymysql
from config import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE

def show_databases():
    try:
        print("Connecting to MySQL...")
        conn = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            connect_timeout=5
        )
        print("Connected successfully.")
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        print("Databases:")
        for db in databases:
            print(db[0])
        
        # Try to use the database
        try:
            cursor.execute(f"USE {MYSQL_DATABASE}")
            print(f"Using database {MYSQL_DATABASE}")
            cursor.execute("SELECT COUNT(*) FROM attlog")
            total = cursor.fetchone()[0]
            print(f"Total records in attlog: {total}")
        except Exception as e:
            print(f"Error with database {MYSQL_DATABASE}: {e}")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    show_databases()