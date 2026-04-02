import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@kki8806810022",
    database="uptime_db"
)

if conn.is_connected():
    print("Connected to MySQL successfully")

cursor = conn.cursor()