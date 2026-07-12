import pandas as pd
import psycopg2

print("="*60)
print("IMPORTING HOSPITALS TO POSTGRESQL")
print("="*60)

# Read CSV
df = pd.read_csv("data_pipeline/osm_data/hospital_master.csv")

print("Hospitals:", len(df))

# PostgreSQL Connection
conn = psycopg2.connect(
    host="localhost",
    database="healthcare_ai",
    user="postgres",
    password="libi@2005"
)

cur = conn.cursor()

# Remove old data
cur.execute("DELETE FROM hospitals")

# Insert records
for _, row in df.iterrows():

    cur.execute("""
        INSERT INTO hospitals
        (
            osm_id,
            hospital_name,
            latitude,
            longitude,
            hospital_type,
            specialty,
            emergency,
            open_24x7,
            state
        )
        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """,
    (
        int(row["osm_id"]),
        row["hospital_name"],
        float(row["latitude"]),
        float(row["longitude"]),
        row["hospital_type"],
        row["specialty"],
        row["emergency"],
        row["open_24x7"],
        row["state"]
    ))

conn.commit()

cur.close()
conn.close()

print()
print("Hospital Import Completed Successfully")
print("="*60)