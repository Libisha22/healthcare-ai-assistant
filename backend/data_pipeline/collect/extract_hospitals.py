import osmium
import csv

PBF_FILE = r"data_pipeline\osm_data\southern-zone-260711.osm.pbf"
OUTPUT_CSV = r"data_pipeline\osm_data\hospitals.csv"


class HospitalHandler(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.hospitals = []

    def node(self, n):
        if n.tags.get("amenity") == "hospital":
            self.hospitals.append([
                n.id,
                n.tags.get("name", "Unknown"),
                n.location.lat,
                n.location.lon
            ])


handler = HospitalHandler()

print("Reading PBF file...")
handler.apply_file(PBF_FILE, locations=True)

print(f"Found {len(handler.hospitals)} hospitals")

with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow([
        "osm_id",
        "hospital_name",
        "latitude",
        "longitude"
    ])

    writer.writerows(handler.hospitals)

print(f"Saved to {OUTPUT_CSV}")