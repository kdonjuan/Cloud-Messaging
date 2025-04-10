# db_config.py (logic file)
from google.cloud.sql.connector import Connector
import pymysql
from config import INSTANCE_CONNECTION_NAME, DB_USER, DB_PASSWORD, DB_NAME

connector = Connector()

def get_db_connection():
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pymysql",
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME
    )
    return conn
