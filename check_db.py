from db_config import get_db_connection
 
try:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages ORDER BY created_at DESC LIMIT 5;")
    results = cursor.fetchall()
 
    print("📦 Recent messages in DB:")
    for row in results:
        print(row)
 
    if not results:
        print("🚫 No messages stored in DB.")
except Exception as e:
    print("❌ Error checking database:", e)


    