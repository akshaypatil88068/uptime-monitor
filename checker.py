import requests
from db import cursor, conn
from datetime import datetime

# Get all websites
cursor.execute("SELECT * FROM websites")
websites = cursor.fetchall()

for site in websites:
    site_id = site[0]
    url = site[1]

    try:
        response = requests.get(url, timeout=5)
        status = "UP" if response.status_code == 200 else "DOWN"
    except:
        status = "DOWN"

    # Update database
    cursor.execute(
        "UPDATE websites SET status=%s, last_checked=%s WHERE id=%s",
        (status, datetime.now(), site_id)
    )
    conn.commit()

    print(f"{url} → {status}")

print("Checked all websites")