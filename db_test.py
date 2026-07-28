"""Database connectivity test for CornHouse."""
import os
from typing import Optional

import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_NAME: Optional[str] = os.getenv("DB_NAME")
DB_USER: Optional[str] = os.getenv("DB_USER")
DB_PASSWORD: Optional[str] = os.getenv("DB_PASSWORD")
DB_HOST: Optional[str] = os.getenv("DB_HOST")
DB_PORT: Optional[str] = os.getenv("DB_PORT")

def test_connection() -> None:
    """Test PostgreSQL connection and list tables."""
    # Check if all required environment variables are present
    required_vars = [
        ("DB_NAME", DB_NAME),
        ("DB_USER", DB_USER),
        ("DB_PASSWORD", DB_PASSWORD),
        ("DB_HOST", DB_HOST),
        ("DB_PORT", DB_PORT),
    ]
    missing = [name for name, value in required_vars if not value]

    if missing:
        print(f"❌ Missing environment variables: {', '.join(missing)}")
        return

    try:
        # Using 'with' automatically closes the connection
        with psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                    ORDER BY table_name;
                """)
                tables = cursor.fetchall()

                print("✅ Connection successful!")
                if tables:
                    print("Tables in the database:")
                    for table in tables:
                        print(f"  - {table[0]}")
                else:
                    print("⚠️ No tables found yet. Run 'python manage.py migrate' to create them.")
    except psycopg2.Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:  # pylint: disable=W0718
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_connection()
