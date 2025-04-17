import pymysql

def get_db_connection():
    conn = pymysql.connect(
        host="130.218.6.188",
        user="test_user1",
        password="is-capstone",
        db="is-capstone",
        connect_timeout=5,  # add this line
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn

