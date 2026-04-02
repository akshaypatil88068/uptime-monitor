from flask import Flask, render_template, request, redirect
from db import get_connection, init_db
import requests
from datetime import datetime
import threading
import time

app = Flask(__name__)

# Initialize DB
init_db()


# -------------------------------
# ROUTES
# -------------------------------

@app.route("/")
def index():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM websites")
    websites = cursor.fetchall()

    conn.close()

    return render_template("index.html", websites=websites)


@app.route("/add", methods=["POST"])
def add():
    url = request.form["url"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO websites (url, status, last_checked) VALUES (?, ?, ?)",
                   (url, "UNKNOWN", "None"))

    conn.commit()
    conn.close()

    return redirect("/")


# -------------------------------
# BACKGROUND CHECKER
# -------------------------------

def check_websites():
    while True:
        print("Running background check...")

        conn = get_connection()
        cursor = conn.cursor()

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

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute(
                "UPDATE websites SET status=?, last_checked=? WHERE id=?",
                (status, now, site_id)
            )

            print(f"{url} → {status}")

        conn.commit()
        conn.close()

        time.sleep(60)  # check every 60 seconds


# Start background thread
threading.Thread(target=check_websites, daemon=True).start()


# -------------------------------
# RUN APP
# -------------------------------

if __name__ == "__main__":
    app.run()