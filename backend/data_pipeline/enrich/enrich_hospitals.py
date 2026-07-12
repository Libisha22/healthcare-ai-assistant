import pandas as pd

print("=" * 60)
print("MEDSCOPE AI - HOSPITAL ENRICHMENT")
print("=" * 60)

# ------------------------------------------------
# Load cleaned dataset
# ------------------------------------------------
df = pd.read_csv("data_pipeline/osm_data/cleaned_hospitals.csv")

print("Hospitals Loaded:", len(df))


# ------------------------------------------------
# Hospital Type
# ------------------------------------------------
def hospital_type(name):

    name = str(name).lower()

    if "government" in name:
        return "Government"

    elif "gh" == name.strip():
        return "Government"

    elif "medical college" in name:
        return "Government Medical College"

    elif "district hospital" in name:
        return "Government"

    elif "apollo" in name:
        return "Private"

    elif "fortis" in name:
        return "Private"

    elif "kauvery" in name:
        return "Private"

    elif "kmch" in name:
        return "Private"

    elif "psg" in name:
        return "Private"

    elif "gknm" in name:
        return "Private"

    elif "hospital" in name:
        return "Private"

    return "Unknown"


# ------------------------------------------------
# Specialties
# ------------------------------------------------
def specialty(name):

    name = str(name).lower()

    if "eye" in name:
        return "Ophthalmology"

    elif "dental" in name:
        return "Dentistry"

    elif "ortho" in name:
        return "Orthopedics"

    elif "children" in name:
        return "Pediatrics"

    elif "child" in name:
        return "Pediatrics"

    elif "women" in name:
        return "Gynecology"

    elif "maternity" in name:
        return "Gynecology"

    elif "heart" in name:
        return "Cardiology"

    elif "cardiac" in name:
        return "Cardiology"

    elif "cancer" in name:
        return "Oncology"

    elif "neuro" in name:
        return "Neurology"

    return "General Medicine"


# ------------------------------------------------
# Emergency
# ------------------------------------------------
def emergency(htype):

    if htype == "Unknown":
        return "Unknown"

    return "Yes"


# ------------------------------------------------
# 24x7
# ------------------------------------------------
def open24(htype):

    if htype == "Unknown":
        return "Unknown"

    return "Yes"


# ------------------------------------------------
# State
# ------------------------------------------------
df["state"] = "Tamil Nadu"

df["hospital_type"] = df["hospital_name"].apply(hospital_type)

df["specialty"] = df["hospital_name"].apply(specialty)

df["emergency"] = df["hospital_type"].apply(emergency)

df["open_24x7"] = df["hospital_type"].apply(open24)

# ------------------------------------------------
# Save
# ------------------------------------------------
output = "data_pipeline/osm_data/hospital_master.csv"

df.to_csv(output, index=False)

print()

print("Hospital Master Created")

print("Saved to:", output)

print("=" * 60)