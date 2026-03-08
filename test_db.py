import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT', 3306)),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
)

cursor = conn.cursor()
cursor.execute("SELECT VERSION()")
print("MySQL version: " + cursor.fetchone()[0])
cursor.close()
print("Connected: ", conn.is_connected())
conn.close()