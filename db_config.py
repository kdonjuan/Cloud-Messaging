import pymysql

def get_db_connection():
    conn = pymysql.connect(
        host="35.231.173.84",
        user="test_user1",
        password="is-capstone",
        db="iscapstone_db",
        connect_timeout=5,
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn

