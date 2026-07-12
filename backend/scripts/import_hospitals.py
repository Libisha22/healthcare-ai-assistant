import os
import sys
import csv

# Add backend folder to Python path
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from app.database import SessionLocal
from app.models.hospital import Hospital


db = SessionLocal()


with open(
    "data/hospitals.csv",
    newline="",
    encoding="utf-8"
) as csvfile:

    reader = csv.DictReader(csvfile)

    for row in reader:
        print(row)

        hospital = Hospital(
            name=row["name"],
            speciality=row["speciality"],
            address=row["address"],
            city=row["city"],
            phone=row["phone"],
            latitude=float(row["latitude"]),
            longitude=float(row["longitude"]),
            rating=float(row["rating"])
        )

        db.add(hospital)

db.commit()
print("\nChecking database after commit...")

all_hospitals = db.query(Hospital).all()

print("Total hospitals:", len(all_hospitals))

for hospital in all_hospitals:
    print(hospital.id, hospital.name)

db.close()

print("Hospitals imported successfully!")