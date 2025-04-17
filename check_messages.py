from db_config import get_db_connection

conn = get_db_connection()
cursor = conn.cursor()

cursor.execute("SELECT * FROM messages ORDER BY transaction_datetime DESC LIMIT 5")
rows = cursor.fetchall()

for row in rows:
    print(row)
