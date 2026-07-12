import requests
import pandas as pd
OVERPASS_URL = "https://overpass.kumi.systems/api/interpreter"

query = """
[out:json][timeout:180];


area["name"="Tamil Nadu"]["boundary"="administrative"]->.searchArea;

(
  node["amenity"="hospital"](area.searchArea);
  way["amenity"="hospital"](area.searchArea);
  relation["amenity"="hospital"](area.searchArea);
);
out center tags;
"""
headers = {
    "User-Agent": "MedScopeAI/1.0 (Educational Project)"
}

response = requests.post(
    OVERPASS_URL,
    data={"data": query},
    headers=headers,
    timeout=180
)

print("Status Code:", response.status_code)
if response.status_code == 200:
    data = response.json()

    print(data.keys())
    print("Hospitals Found:", len(data["elements"]))

else:
    print("Request Failed")
    print(response.text)

