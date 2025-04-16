import pymysql

def get_db_connection():
    conn = pymysql.connect(
        host="130.218.6.188",        # replace with your Cloud SQL instance public IP
        user="test_user1",            # match your config
        password="is-capstone",       # match your config
        db="is-capstone",
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn
