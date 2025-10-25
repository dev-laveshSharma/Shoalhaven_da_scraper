from flask import Flask, render_template
from dotenv import load_dotenv
import os, requests

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
TABLE_NAME = os.getenv("TABLE_NAME", "shoalhaven_da_scraper_db")

app = Flask(__name__)

def fetch_records(limit=500):
    url = f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}"
    headers = {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
        "Accept": "application/json"
    }
    params = {"select": "*", "limit": limit}
    r = requests.get(url, headers=headers, params=params)
    r.raise_for_status()
    return r.json()

@app.route("/")
def index():
    rows = fetch_records(limit=500)
    # rows is a list of dicts
    columns = list(rows[0].keys()) if rows else []
    return render_template("index.html", rows=rows, columns=columns)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
