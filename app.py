from db import init_db

init_db()

from flask import Flask, render_template, request, redirect
from db import cursor, conn
from flask import Flask, render_template, request, redirect
from db import cursor, conn
from datetime import datetime
import requests

from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)

# 🔁 Background job function
def check_websites():
    print("Running background check...")

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

        cursor.execute(
            "UPDATE websites SET status=%s, last_checked=%s WHERE id=%s",
            (status, datetime.now(), site_id)
        )
        conn.commit()

        print(f"{url} → {status}")

# 🚀 Start scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(check_websites, 'interval', minutes=1)
scheduler.start()

@app.route('/')
def index():
    cursor.execute("SELECT * FROM websites")
    data = cursor.fetchall()
    return render_template("index.html", websites=data)

@app.route('/add', methods=['POST'])
def add():
    url = request.form['url']
    cursor.execute("INSERT INTO websites (url, status) VALUES (%s, %s)", (url, "UNKNOWN"))
    conn.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)