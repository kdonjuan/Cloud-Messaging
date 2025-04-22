import pymysql
from config import DB_NAME, DB_USER, DB_PASSWORD
 
def get_db_connection():
    return pymysql.connect(
        host="35.231.173.84",  # or your Cloud SQL instance IP if remote
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor  # ✅ Ensures fetch returns dictionaries
    )