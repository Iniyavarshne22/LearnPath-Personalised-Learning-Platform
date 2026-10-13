
from db import get_db_connection

try:
    connection = get_db_connection()
    print("MySQL connected successfully!")
    connection.close()
except Exception as error:
    print("Connection failed:", error)
