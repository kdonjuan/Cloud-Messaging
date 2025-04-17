import mysql.connector

# Establish connection
conn = mysql.connector.connect(
    host="localhost",        # Change to your MySQL server address
    user="root",    # Your MySQL username
    password="lreinha1",# Your MySQL password
    database="my_database" # Your database name (optional)
)

# Check if connection was successful
if conn.is_connected():
    print("Connected to MySQL!")

# Close the connection
conn.close()
