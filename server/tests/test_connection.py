import psycopg2

url = "postgresql://neondb_owner:REAL_PASSWORD@ep-proud-math-abftzx1a.eu-west-2.aws.neon.tech/neondb?sslmode=require"

try:
    conn = psycopg2.connect(url)
    print("OK")
except Exception as e:
    print(e)
