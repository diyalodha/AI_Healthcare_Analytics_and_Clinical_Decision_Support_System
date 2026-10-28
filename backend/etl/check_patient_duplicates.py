import pandas as pd
import os

PROJECT_ROOT = r"E:\College Final Year\Major Project\Healthcare_AI_Project"

CSV_FILE = os.path.join(
    PROJECT_ROOT,
    "datasets",
    "synthetic",
    "patients.csv"
)

print("=" * 70)
print("PATIENT CSV DUPLICATE CHECK")
print("=" * 70)

df = pd.read_csv(CSV_FILE)

print(f"\nTotal rows: {len(df):,}")
print(f"Unique Patient IDs: {df['Patient_ID'].nunique():,}")

# ------------------------------------------------------------
# PHONE DUPLICATES
# ------------------------------------------------------------

phone_counts = df["Phone_Number"].value_counts(dropna=False)

duplicate_phones = phone_counts[
    phone_counts > 1
]

print("\n" + "-" * 70)
print("PHONE DUPLICATE ANALYSIS")
print("-" * 70)

print(
    f"Unique phone numbers : "
    f"{df['Phone_Number'].nunique():,}"
)

print(
    f"Duplicate phone values: "
    f"{len(duplicate_phones):,}"
)

duplicate_rows = (
    phone_counts[phone_counts > 1].sum()
)

print(
    f"Rows involved in duplicates: "
    f"{duplicate_rows:,}"
)

# ------------------------------------------------------------
# SHOW DUPLICATE PHONE
# ------------------------------------------------------------

target_phone = "9258716980"

print("\n" + "-" * 70)
print(f"CHECKING PHONE: {target_phone}")
print("-" * 70)

matches = df[
    df["Phone_Number"].astype(str) == target_phone
]

print(matches[
    [
        "Patient_ID",
        "First_Name",
        "Last_Name",
        "Phone_Number"
    ]
].to_string(index=False))

# ------------------------------------------------------------
# SHOW TOP DUPLICATES
# ------------------------------------------------------------

print("\n" + "-" * 70)
print("TOP 20 DUPLICATE PHONE NUMBERS")
print("-" * 70)

print(
    duplicate_phones
    .head(20)
    .to_string()
)

print("\n" + "=" * 70)
print("CHECK COMPLETED")
print("=" * 70)