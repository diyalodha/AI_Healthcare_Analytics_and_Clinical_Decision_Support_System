import os
import pandas as pd
import mysql.connector


# ============================================================
# PROJECT CONFIGURATION
# ============================================================

PROJECT_ROOT = r"E:\College Final Year\Major Project\Healthcare_AI_Project"

CSV_PATH = os.path.join(
    PROJECT_ROOT,
    "datasets",
    "synthetic",
    "diagnoses.csv"
)


# ============================================================
# HEADER
# ============================================================

print("=" * 75)
print("53 - PATIENT DISEASES MAPPING")
print("=" * 75)


# ============================================================
# 1. LOAD DIAGNOSES CSV
# ============================================================

print("\nLoading diagnoses.csv...")

df = pd.read_csv(
    CSV_PATH,
    usecols=[
        "Diagnosis_ID",
        "Patient_ID",
        "Disease_ID",
        "Doctor_ID",
        "Diagnosis_Date",
        "Diagnosis_Status",
        "Severity",
        "Notes"
    ],
    dtype=str
)

print(
    f"Diagnosis rows loaded: {len(df):,}"
)


# ============================================================
# 2. CLEAN REQUIRED DATA
# ============================================================

print("\nCleaning diagnosis data...")

df = df.dropna(
    subset=[
        "Diagnosis_ID",
        "Patient_ID",
        "Disease_ID",
        "Diagnosis_Date"
    ]
)

df["Diagnosis_Date"] = pd.to_datetime(
    df["Diagnosis_Date"],
    errors="coerce"
)

df = df.dropna(
    subset=["Diagnosis_Date"]
)

print(
    f"Valid diagnosis rows after cleaning: {len(df):,}"
)


# ============================================================
# 3. SELECT MOST RECENT RECORD PER
#    PATIENT + DISEASE PAIR
# ============================================================

print(
    "\nSelecting the most recent diagnosis for each "
    "Patient-Disease pair..."
)

df = df.sort_values(
    by=[
        "Patient_ID",
        "Disease_ID",
        "Diagnosis_Date",
        "Diagnosis_ID"
    ],
    ascending=[
        True,
        True,
        False,
        False
    ]
)

df = df.drop_duplicates(
    subset=[
        "Patient_ID",
        "Disease_ID"
    ],
    keep="first"
)

print(
    f"Unique Patient-Disease pairs selected: {len(df):,}"
)


# ============================================================
# 4. CONNECT TO MYSQL
# ============================================================

print("\nConnecting to MySQL...")

password = input("MySQL password: ")

try:

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=password,
        database="healthcare_ai_db"
    )

    cursor = conn.cursor()

    print("MySQL connection successful.")

except mysql.connector.Error as e:

    print("\nERROR: Could not connect to MySQL.")
    print(e)

    raise SystemExit(1)


# ============================================================
# 5. LOAD VALID PATIENT IDS
# ============================================================

print("\nLoading valid Patient IDs...")

cursor.execute("""
    SELECT Patient_ID
    FROM patients
""")

valid_patients = {
    str(row[0])
    for row in cursor.fetchall()
}

print(
    f"Valid patients: {len(valid_patients):,}"
)


# ============================================================
# 6. LOAD VALID DISEASE IDS
# ============================================================

print("\nLoading valid Disease IDs...")

cursor.execute("""
    SELECT
        Disease_ID,
        Disease_Type
    FROM diseases
""")

disease_types = {
    str(row[0]): row[1]
    for row in cursor.fetchall()
}

valid_diseases = set(
    disease_types.keys()
)

print(
    f"Valid diseases: {len(valid_diseases):,}"
)


# ============================================================
# 7. LOAD VALID DOCTOR IDS
# ============================================================

print("\nLoading valid Doctor IDs...")

cursor.execute("""
    SELECT Doctor_ID
    FROM doctors
""")

valid_doctors = {
    str(row[0])
    for row in cursor.fetchall()
}

print(
    f"Valid doctors: {len(valid_doctors):,}"
)


# ============================================================
# 8. VALIDATE PATIENT IDS
# ============================================================

original_count = len(df)

df = df[
    df["Patient_ID"].isin(valid_patients)
]

invalid_patient = (
    original_count - len(df)
)

print(
    f"\nInvalid Patient_ID: {invalid_patient:,}"
)


# ============================================================
# 9. VALIDATE DISEASE IDS
# ============================================================

before_disease = len(df)

df = df[
    df["Disease_ID"].isin(valid_diseases)
]

invalid_disease = (
    before_disease - len(df)
)

print(
    f"Invalid Disease_ID: {invalid_disease:,}"
)


# ============================================================
# 10. VALIDATE DOCTOR IDS
# ============================================================

df["Diagnosed_By_Doctor_ID"] = (
    df["Doctor_ID"].where(
        df["Doctor_ID"].isin(valid_doctors),
        None
    )
)

invalid_doctor = (
    df["Doctor_ID"].notna()
    &
    ~df["Doctor_ID"].isin(valid_doctors)
).sum()

print(
    f"Invalid Doctor_ID: {invalid_doctor:,}"
)


# ============================================================
# 11. MAP DISEASE STATUS
# ============================================================

df["Disease_Status"] = (
    df["Diagnosis_Status"].map({
        "Confirmed": "Active",
        "Suspected": "Suspected",
        "Ruled Out": "Resolved"
    })
)


# ============================================================
# 12. MAP DISEASE SEVERITY
# ============================================================

df["Disease_Severity"] = (
    df["Severity"].map({
        "Low": "Mild",
        "Moderate": "Moderate",
        "High": "Severe",
        "Critical": "Critical"
    })
)


# ============================================================
# 13. PRIMARY DISEASE
# ============================================================
#
# The source CSV has no primary-diagnosis field.
#
# Therefore we do not fabricate this information.
#

df["Is_Primary_Disease"] = 0


# ============================================================
# 14. CHRONIC DISEASE FLAG
# ============================================================

df["Is_Chronic"] = (
    df["Disease_ID"].map(
        lambda disease_id:
        1
        if disease_types.get(disease_id) == "Chronic"
        else 0
    )
)


# ============================================================
# 15. HEREDITARY FLAG
# ============================================================
#
# No hereditary field exists in diagnoses.csv.
#

df["Is_Hereditary"] = 0


# ============================================================
# 16. DIAGNOSIS SOURCE
# ============================================================

df["Diagnosis_Source"] = "Clinical Diagnosis"


# ============================================================
# 17. SYMPTOMS
# ============================================================
#
# No Symptoms column exists in diagnoses.csv.
#

df["Symptoms_At_Diagnosis"] = None


# ============================================================
# 18. TREATMENT SUMMARY
# ============================================================

df["Treatment_Summary"] = None


# ============================================================
# 19. CLINICAL NOTES
# ============================================================
#
# Actual source column:
#
# Notes
#
# Destination:
#
# Clinical_Notes
#

df["Clinical_Notes"] = df["Notes"]


# ============================================================
# 20. RESOLUTION DATE
# ============================================================

df["Resolution_Date"] = None


# ============================================================
# 21. LAST REVIEWED DATE
# ============================================================

df["Last_Reviewed_Date"] = (
    df["Diagnosis_Date"].dt.date
)


# ============================================================
# 22. AI FIELDS
# ============================================================

df["AI_Risk_Score"] = None

df["AI_Progression_Risk"] = None

df["AI_Recommendation"] = None


# ============================================================
# 23. DATA SOURCE / AUDIT FIELDS
# ============================================================

df["Data_Source"] = "Synthetic"

df["Created_By"] = "ETL_53"

df["Updated_By"] = "ETL_53"


# ============================================================
# 24. CONVERT PANDAS NaN TO PYTHON None
# ============================================================
#
# This is important.
#
# Empty CSV fields become NaN in Pandas.
# MySQL Connector may otherwise interpret NaN incorrectly.
#
# We convert every NaN/NaT to Python None,
# which MySQL Connector inserts as SQL NULL.
#
# ============================================================

df = df.astype(object)

df = df.where(
    pd.notna(df),
    None
)


# ============================================================
# 25. INSERT SQL
# ============================================================

INSERT_SQL = """
INSERT INTO patient_diseases_map (
    Patient_ID,
    Disease_ID,
    Diagnosed_By_Doctor_ID,
    Diagnosis_Date,
    Disease_Status,
    Disease_Severity,
    Is_Primary_Disease,
    Is_Chronic,
    Is_Hereditary,
    Diagnosis_Source,
    Symptoms_At_Diagnosis,
    Treatment_Summary,
    Clinical_Notes,
    Resolution_Date,
    Last_Reviewed_Date,
    AI_Risk_Score,
    AI_Progression_Risk,
    AI_Recommendation,
    Data_Source,
    Created_By,
    Updated_By
)
VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
)
"""


# ============================================================
# 26. SAFETY CHECK
# ============================================================

cursor.execute("""
    SELECT COUNT(*)
    FROM patient_diseases_map
""")

existing_count = cursor.fetchone()[0]

if existing_count > 0:

    print(
        f"\nWARNING: patient_diseases_map already contains "
        f"{existing_count:,} records."
    )

    print(
        "No records will be deleted."
    )

    print(
        "Stopping to prevent duplicate mappings."
    )

    cursor.close()
    conn.close()

    raise SystemExit(1)


# ============================================================
# 27. BATCH INSERT
# ============================================================

BATCH_SIZE = 5000

batch = []

inserted = 0

print(
    "\nInserting Patient-Disease mappings..."
)


for row in df.itertuples(index=False):

    batch.append((
        row.Patient_ID,
        row.Disease_ID,
        row.Diagnosed_By_Doctor_ID,
        row.Diagnosis_Date,
        row.Disease_Status,
        row.Disease_Severity,
        int(row.Is_Primary_Disease),
        int(row.Is_Chronic),
        int(row.Is_Hereditary),
        row.Diagnosis_Source,
        row.Symptoms_At_Diagnosis,
        row.Treatment_Summary,
        row.Clinical_Notes,
        row.Resolution_Date,
        row.Last_Reviewed_Date,
        row.AI_Risk_Score,
        row.AI_Progression_Risk,
        row.AI_Recommendation,
        row.Data_Source,
        row.Created_By,
        row.Updated_By
    ))

    if len(batch) >= BATCH_SIZE:

        cursor.executemany(
            INSERT_SQL,
            batch
        )

        conn.commit()

        inserted += len(batch)

        print(
            f"Inserted: {inserted:,}"
        )

        batch = []


# ============================================================
# 28. INSERT REMAINING RECORDS
# ============================================================

if batch:

    cursor.executemany(
        INSERT_SQL,
        batch
    )

    conn.commit()

    inserted += len(batch)


# ============================================================
# 29. FINAL DATABASE STATISTICS
# ============================================================

cursor.execute("""
SELECT
    COUNT(*) AS Total_Maps,

    COUNT(DISTINCT Patient_ID)
        AS Unique_Patients,

    COUNT(DISTINCT Disease_ID)
        AS Unique_Diseases,

    COUNT(
        DISTINCT CONCAT(
            Patient_ID,
            '|',
            Disease_ID
        )
    ) AS Unique_Patient_Disease_Pairs

FROM patient_diseases_map
""")

result = cursor.fetchone()


# ============================================================
# 30. FINAL OUTPUT
# ============================================================

print("\n" + "=" * 75)
print("53 - PATIENT DISEASES MAPPING COMPLETE")
print("=" * 75)

print(
    f"Source diagnosis rows:             {original_count:,}"
)

print(
    f"Unique Patient-Disease pairs:      {len(df):,}"
)

print(
    f"Inserted mappings:                 {inserted:,}"
)

print(
    f"Database mappings:                 {result[0]:,}"
)

print(
    f"Unique patients mapped:            {result[1]:,}"
)

print(
    f"Unique diseases mapped:            {result[2]:,}"
)

print(
    f"Unique Patient-Disease pairs DB:   {result[3]:,}"
)

print(
    f"Invalid Patient_ID:                {invalid_patient:,}"
)

print(
    f"Invalid Disease_ID:                {invalid_disease:,}"
)

print(
    f"Invalid Doctor_ID:                 {invalid_doctor:,}"
)


# ============================================================
# 31. CLOSE CONNECTION
# ============================================================

cursor.close()

conn.close()

print("\nMySQL connection closed.")

print("=" * 75)
