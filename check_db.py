from db_config import get_db_connection
 
conn = get_db_connection()
cursor = conn.cursor()
cursor.execute("SELECT * FROM messages ORDER BY created_at DESC LIMIT 5;")
rows = cursor.fetchall()
 
print("📦 Latest messages:")
for row in rows:
    print(row)
 
if not rows:
    print("⚠️ No messages stored.")
    