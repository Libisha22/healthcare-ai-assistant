import pandas as pd

print("Loading hospitals dataset...")

# Read the extracted dataset
df = pd.read_csv("data_pipeline/osm_data/hospitals.csv")

print("Original Records:", len(df))

# -----------------------------
# Remove duplicate hospitals
# -----------------------------
df = df.drop_duplicates()

# -----------------------------
# Remove hospitals without names
# -----------------------------
df = df.dropna(subset=["hospital_name"])

df["hospital_name"] = df["hospital_name"].astype(str).str.strip()

df = df[df["hospital_name"] != ""]

# -----------------------------
# Remove invalid coordinates
# -----------------------------
df = df.dropna(subset=["latitude", "longitude"])

# -----------------------------
# Remove duplicate hospitals by name + location
# -----------------------------
df = df.drop_duplicates(
    subset=["hospital_name", "latitude", "longitude"]
)

# -----------------------------
# Reset index
# -----------------------------
df = df.reset_index(drop=True)

print("Clean Records:", len(df))

# Save cleaned dataset
output_path = "data_pipeline/osm_data/cleaned_hospitals.csv"

df.to_csv(output_path, index=False)

print("Saved:", output_path)