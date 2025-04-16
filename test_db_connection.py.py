from db_config import get_db_connection

try:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT NOW();")
    result = cursor.fetchone()
    print("✅ Database connected successfully!")
    print("Current time from DB:", result)
    cursor.close()
    conn.close()
except Exception as e:
    print("❌ Failed to connect to database.")
    print("Error:", e)
