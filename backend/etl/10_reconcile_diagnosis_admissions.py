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
# 3. SELECT ONE RECORD PER
#    PATIENT + DISEASE PAIR
# ============================================================
#
# A patient can have the same disease diagnosed multiple times.
#
# patient_diseases_map is intended to represent the patient's
# disease relationship rather than every individual diagnosis.
#
# Therefore, we keep the MOST RECENT diagnosis for each
# Patient_ID + Disease_ID combination.
#
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
# 5. LOAD VALID PATIENT IDs
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
# 6. LOAD VALID DISEASE IDs
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
# 7. LOAD VALID DOCTOR IDs
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
# 8. VALIDATE PATIENT IDs
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
# 9. VALIDATE DISEASE IDs
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
# 10. VALIDATE DOCTOR IDs
# ============================================================
#
# Diagnosed_By_Doctor_ID is nullable in patient_diseases_map.
#
# Therefore:
#
# Valid doctor -> keep Doctor_ID
# Invalid doctor -> NULL
#
# We do NOT invent replacement Doctor_IDs.
#
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
#
# diagnoses.Diagnosis_Status:
#
# Confirmed -> Active
# Suspected -> Suspected
# Ruled Out -> Resolved
#
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
#
# diagnoses.Severity:
#
# Low      -> Mild
# Moderate -> Moderate
# High     -> Severe
# Critical -> Critical
#
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
# diagnoses.csv does NOT contain Is_Primary_Diagnosis.
#
# Therefore we do not fabricate this information.
#
# Default:
# 0 = Not marked as primary
#
# ============================================================

df["Is_Primary_Disease"] = 0


# ============================================================
# 14. CHRONIC DISEASE FLAG
# ============================================================
#
# Derived from diseases.Disease_Type.
#
# Disease_Type = Chronic -> 1
# Otherwise -> 0
#
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
# diagnoses.csv does not contain hereditary information.
#
# Therefore we use:
# 0 = information not available / not marked hereditary
#
# ============================================================

df["Is_Hereditary"] = 0


# ============================================================
# 16. DIAGNOSIS SOURCE
# ============================================================
#
# Current diagnoses.csv contains Diagnosis_Type, but our
# selected source fields do not include it.
#
# Existing data is based on clinical diagnosis.
#
# ============================================================

df["Diagnosis_Source"] = "Clinical Diagnosis"


# ============================================================
# 17. SYMPTOMS
# ============================================================
#
# diagnoses.csv does not contain a Symptoms column.
#
# Therefore NULL is used.
#
# ============================================================

df["Symptoms_At_Diagnosis"] = None


# ============================================================
# 18. TREATMENT SUMMARY
# ============================================================
#
# diagnoses.csv does not contain treatment information.
#
# Therefore NULL is used.
#
# ============================================================

df["Treatment_Summary"] = None


# ============================================================
# 19. CLINICAL NOTES
# ============================================================
#
# The actual CSV contains:
#
# Notes
#
# We map Notes -> Clinical_Notes.
#
# ============================================================

df["Clinical_Notes"] = df["Notes"]


# ============================================================
# 20. RESOLUTION DATE
# ============================================================
#
# Only diagnoses with "Ruled Out" would normally be resolved.
#
# Since our current synthetic diagnosis data is confirmed,
# we leave this NULL.
#
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
#
# The source diagnoses.csv does not contain genuine AI risk
# or recommendation values.
#
# We intentionally leave these NULL.
#
# We do NOT use AI_Confidence as AI_Risk_Score because those
# are different concepts.
#
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
# 24. INSERT SQL
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

    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s

)

"""


# ============================================================
# 25. SAFETY CHECK
# ============================================================
#
# We do not delete existing records.
#
# If mappings already exist, the script stops to prevent
# accidental duplicate insertion.
#
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
# 26. BATCH INSERT
# ============================================================

BATCH_SIZE = 5000

batch = []

inserted = 0

print(
    "\nInserting Patient-Disease mappings..."
)


for row in df.itertuples(index=False):

    diagnosis_date = (
        row.Diagnosis_Date.date()
    )

    batch.append((

        row.Patient_ID,

        row.Disease_ID,

        row.Diagnosed_By_Doctor_ID,

        diagnosis_date,

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
# 27. INSERT REMAINING RECORDS
# ============================================================

if batch:

    cursor.executemany(
        INSERT_SQL,
        batch
    )

    conn.commit()

    inserted += len(batch)


# ============================================================
# 28. FINAL DATABASE STATISTICS
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
    )
        AS Unique_Patient_Disease_Pairs

FROM patient_diseases_map
""")

result = cursor.fetchone()


# ============================================================
# 29. FINAL OUTPUT
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
# 30. CLOSE CONNECTION
# ============================================================

cursor.close()

conn.close()

print("\nMySQL connection closed.")

print("=" * 75)