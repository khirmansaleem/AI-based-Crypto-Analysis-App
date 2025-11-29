import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()  # <-- REQUIRED

DATABASE_URL = os.getenv("DATABASE_URL")

print("DB URL read by script:", DATABASE_URL)

try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT NOW();")
    print("Connected OK:", cur.fetchone())
except Exception as e:
    print("Error connecting to DB:", e)
