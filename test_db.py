
from app.db.database import test_mysql_connection

try:
    result = test_mysql_connection()
    print("MySQL connection successful!")
    print("SELECT 1 result:", result)
except Exception as error:
    print("MySQL connection failed.")
    print(type(error).__name__, error)
