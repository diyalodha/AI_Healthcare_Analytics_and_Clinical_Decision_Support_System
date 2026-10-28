import os
import re
import sys
import pandas as pd
import mysql.connector
from datetime import timedelta

# ============================================================
# 54 - PATIENT MEDICATIONS MAPPING
# Source:
#   datasets/synthetic/prescriptions.csv
#   datasets/synthetic/medications.csv
#
# Target:
#   patient_medications_map
#
# ============================================================

PROJECT_ROOT = r"E:\College Final Year\Major Project\Healthcare_AI_Project"

PRESCRIPTIONS_FILE = os.path.join(
    PROJECT_ROOT,
    "datasets",
    "synthetic",
    "prescriptions.csv"
)

MEDICATIONS_FILE = os.path.join(
    PROJECT_ROOT,
    "datasets",
    "synthetic",
    "medications.csv"
)

BATCH_SIZE = 5000
ETL_NAME = "ETL_54"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=input("Enter MySQL root password: "),
        database="healthcare_ai_db",
        autocommit=False
    )


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clean_value(value):
    """Convert pandas NaN/NaT/empty strings to None."""
    if pd.isna(value):
        return None

    if isinstance(value, str):
        value = value.strip()
        if value == "":
            return None

    return value


def parse_duration_days(value):
    """
    Convert values such as:
        '14 Days' -> 14
        '2 Weeks' -> 14
        '1 Month' -> 30
        '30' -> 30
    """
    value = clean_value(value)

    if value is None:
        return None

    text = str(value).strip().lower()

    match = re.search(r"(\d+(?:\.\d+)?)", text)

    if not match:
        return None

    number = float(match.group(1))

    if "week" in text:
        return int(round(number * 7))

    if "month" in text:
        return int(round(number * 30))

    if "year" in text:
        return int(round(number * 365))

    return int(round(number))


def split_dosage(value):
    """
    Example:
        '500 mg' -> ('500', 'mg')
        '5 mg'   -> ('5', 'mg')
        '10'     -> ('10', None)
    """
    value = clean_value(value)

    if value is None:
        return None, None

    text = str(value).strip()

    match = re.match(
        r"^\s*([0-9]+(?:\.[0-9]+)?)\s*(.*)$",
        text
    )

    if not match:
        return text, None

    amount = match.group(1)
    unit = match.group(2).strip()

    return amount, unit if unit else None


def map_route(route):
    """
    Convert source CSV route values to the target table enum.
    """

    route = clean_value(route)

    if route is None:
        return "Other"

    value = str(route).strip().lower()

    mapping = {
        "oral": "Oral",
        "intravenous": "Intravenous",
        "iv": "Intravenous",
        "intramuscular": "Intramuscular",
        "im": "Intramuscular",
        "subcutaneous": "Subcutaneous",
        "topical": "Topical",
        "inhalation": "Inhalation",
        "sublingual": "Sublingual",
        "rectal": "Rectal",
        "injection": "Other",
        "ophthalmic": "Other",
        "nasal": "Other",
        "other": "Other",
    }

    return mapping.get(value, "Other")


def map_status(status):
    """
    Source:
        Active
        Completed
        Cancelled

    Target:
        Active
        Completed
        Discontinued
        On Hold
        Cancelled
    """

    status = clean_value(status)

    if status is None:
        return "Active"

    value = str(status).strip().lower()

    mapping = {
        "active": "Active",
        "completed": "Completed",
        "cancelled": "Cancelled",
        "canceled": "Cancelled",
        "discontinued": "Discontinued",
        "on hold": "On Hold",
    }

    return mapping.get(value, "Active")


def parse_date(value):
    value = clean_value(value)

    if value is None:
        return None

    parsed = pd.to_datetime(value, errors="coerce")

    if pd.isna(parsed):
        return None

    return parsed.date()


# ============================================================
# START
# ============================================================

print("=" * 70)
print("54 - PATIENT MEDICATIONS MAPPING")
print("=" * 70)

if not os.path.exists(PRESCRIPTIONS_FILE):
    print(f"ERROR: prescriptions.csv not found:")
    print(PRESCRIPTIONS_FILE)
    sys.exit(1)

if not os.path.exists(MEDICATIONS_FILE):
    print(f"ERROR: medications.csv not found:")
    print(MEDICATIONS_FILE)
    sys.exit(1)


# ============================================================
# LOAD SOURCE DATA
# ============================================================

print("\nLoading medications.csv...")

medications_df = pd.read_csv(
    MEDICATIONS_FILE,
    dtype=str
)

print(f"Medication master rows loaded: {len(medications_df):,}")

required_medication_columns = [
    "Medication_ID",
    "Medication_Name",
    "Generic_Name",
    "Drug_Class",
    "Used_For",
    "Route",
    "Dosage_Form",
    "Strength",
    "Risk_Level"
]

missing_medication_columns = [
    col for col in required_medication_columns
    if col not in medications_df.columns
]

if missing_medication_columns:
    print("\nERROR: Missing medication CSV columns:")
    for col in missing_medication_columns:
        print(f"  - {col}")
    sys.exit(1)


# ============================================================
# MEDICATION LOOKUP
# ============================================================

medication_lookup = {}

for _, row in medications_df.iterrows():

    medication_id = clean_value(row["Medication_ID"])

    if medication_id is None:
        continue

    medication_lookup[medication_id] = {
        "Medication_Name": clean_value(row["Medication_Name"]),
        "Generic_Name": clean_value(row["Generic_Name"]),
        "Drug_Class": clean_value(row["Drug_Class"]),
        "Used_For": clean_value(row["Used_For"]),
        "Route": clean_value(row["Route"]),
        "Dosage_Form": clean_value(row["Dosage_Form"]),
        "Strength": clean_value(row["Strength"]),
        "Risk_Level": clean_value(row["Risk_Level"]),
    }

print(f"Unique medication IDs in source: {len(medication_lookup):,}")


# ============================================================
# LOAD PRESCRIPTIONS
# ============================================================

print("\nLoading prescriptions.csv...")

prescriptions_df = pd.read_csv(
    PRESCRIPTIONS_FILE,
    dtype=str
)

print(f"Prescription rows loaded: {len(prescriptions_df):,}")

required_prescription_columns = [
    "Prescription_ID",
    "Patient_ID",
    "Admission_ID",
    "Doctor_ID",
    "Medication_ID",
    "Dosage",
    "Frequency",
    "Duration",
    "Route",
    "Prescription_Status",
    "Prescription_Date",
    "Notes"
]

missing_prescription_columns = [
    col for col in required_prescription_columns
    if col not in prescriptions_df.columns
]

if missing_prescription_columns:
    print("\nERROR: Missing prescription CSV columns:")
    for col in missing_prescription_columns:
        print(f"  - {col}")
    sys.exit(1)


# ============================================================
# BASIC SOURCE CLEANING
# ============================================================

for col in required_prescription_columns:
    prescriptions_df[col] = prescriptions_df[col].apply(clean_value)

original_rows = len(prescriptions_df)

prescriptions_df = prescriptions_df[
    prescriptions_df["Prescription_ID"].notna()
    & prescriptions_df["Patient_ID"].notna()
    & prescriptions_df["Medication_ID"].notna()
    & prescriptions_df["Prescription_Date"].notna()
].copy()

print(
    f"Valid prescription rows after required-field cleaning: "
    f"{len(prescriptions_df):,}"
)

print(
    f"Invalid/incomplete prescription rows removed: "
    f"{original_rows - len(prescriptions_df):,}"
)


# ============================================================
# CONNECT TO MYSQL
# ============================================================

print("\nConnecting to MySQL...")

connection = get_connection()
cursor = connection.cursor()

print("MySQL connection successful.")


# ============================================================
# CHECK TARGET TABLE
# ============================================================

cursor.execute(
    "SELECT COUNT(*) FROM patient_medications_map"
)

existing_count = cursor.fetchone()[0]

print(
    f"\nExisting patient_medications_map records: "
    f"{existing_count:,}"
)

if existing_count > 0:
    print(
        "\nWARNING: patient_medications_map already contains records."
    )
    print(
        "This script will stop to prevent accidental duplicate loading."
    )

    cursor.close()
    connection.close()
    sys.exit(1)


# ============================================================
# LOAD VALID FOREIGN KEYS
# ============================================================

print("\nLoading valid Patient IDs...")

cursor.execute(
    "SELECT Patient_ID FROM patients"
)

valid_patients = {
    row[0]
    for row in cursor.fetchall()
}

print(f"Valid patients: {len(valid_patients):,}")


print("Loading valid Medication IDs...")

cursor.execute(
    "SELECT Medication_ID FROM medications"
)

valid_medications = {
    row[0]
    for row in cursor.fetchall()
}

print(f"Valid medications: {len(valid_medications):,}")


print("Loading valid Doctor IDs...")

cursor.execute(
    "SELECT Doctor_ID FROM doctors"
)

valid_doctors = {
    row[0]
    for row in cursor.fetchall()
}

print(f"Valid doctors: {len(valid_doctors):,}")


# ============================================================
# VALIDATE SOURCE REFERENCES
# ============================================================

invalid_patient = 0
invalid_medication = 0
invalid_doctor = 0
invalid_date = 0

valid_rows = []

for _, row in prescriptions_df.iterrows():

    patient_id = row["Patient_ID"]
    medication_id = row["Medication_ID"]
    doctor_id = row["Doctor_ID"]

    if patient_id not in valid_patients:
        invalid_patient += 1
        continue

    if medication_id not in valid_medications:
        invalid_medication += 1
        continue

    if doctor_id is not None and doctor_id not in valid_doctors:
        # Doctor is nullable in patient_medications_map.
        doctor_id = None
        invalid_doctor += 1

    prescription_date = parse_date(row["Prescription_Date"])

    if prescription_date is None:
        invalid_date += 1
        continue

    valid_rows.append(
        (
            row,
            doctor_id,
            prescription_date
        )
    )


print("\nSource validation:")
print(f"  Invalid Patient_ID:    {invalid_patient:,}")
print(f"  Invalid Medication_ID: {invalid_medication:,}")
print(f"  Invalid Doctor_ID:     {invalid_doctor:,}")
print(f"  Invalid Prescription_Date: {invalid_date:,}")
print(f"  Valid rows:            {len(valid_rows):,}")


# ============================================================
# INSERT
# ============================================================

insert_sql = """
INSERT INTO patient_medications_map
(
    Patient_ID,
    Medication_ID,
    Prescribed_By_Doctor_ID,
    Prescription_Date,
    Start_Date,
    End_Date,
    Duration_Days,
    Dosage,
    Dosage_Unit,
    Frequency,
    Route,
    Quantity_Prescribed,
    Refills_Allowed,
    Treatment_Indication,
    Treatment_Purpose,
    Medication_Status,
    Discontinuation_Reason,
    Patient_Response,
    Adverse_Reaction,
    Adverse_Reaction_Details,
    Medication_Adherence_Percentage,
    Doctor_Notes,
    Patient_Notes,
    AI_Effectiveness_Score,
    AI_Adverse_Risk_Score,
    AI_Recommendation,
    Data_Source,
    Created_By,
    Updated_By
)
VALUES
(
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s
)
"""

inserted = 0
skipped_insert = 0

batch = []

print("\nBeginning batch insertion...")
print("-" * 70)

for index, (row, doctor_id, prescription_date) in enumerate(
    valid_rows,
    start=1
):

    medication_id = row["Medication_ID"]

    medication_info = medication_lookup.get(
        medication_id,
        {}
    )

    dosage, dosage_unit = split_dosage(
        row["Dosage"]
    )

    duration_days = parse_duration_days(
        row["Duration"]
    )

    start_date = prescription_date

    end_date = None

    if duration_days is not None and duration_days > 0:
        end_date = start_date + timedelta(
            days=duration_days - 1
        )

    source_route = clean_value(row["Route"])

    route = map_route(source_route)

    frequency = clean_value(row["Frequency"])

    status = map_status(
        row["Prescription_Status"]
    )

    notes = clean_value(row["Notes"])

    treatment_indication = medication_info.get(
        "Used_For"
    )

    # --------------------------------------------------------
    # Default clinical values
    # --------------------------------------------------------

    treatment_purpose = "Primary Treatment"

    patient_response = "Unknown"

    adverse_reaction = 0

    refills_allowed = 0

    quantity_prescribed = None

    adherence_percentage = None

    ai_effectiveness_score = None

    ai_adverse_risk_score = None

    ai_recommendation = None

    discontinuation_reason = None

    adverse_reaction_details = None

    doctor_notes = notes

    patient_notes = None

    record = (
        row["Patient_ID"],
        medication_id,
        doctor_id,
        prescription_date,
        start_date,
        end_date,
        duration_days,
        dosage,
        dosage_unit,
        frequency,
        route,
        quantity_prescribed,
        refills_allowed,
        treatment_indication,
        treatment_purpose,
        status,
        discontinuation_reason,
        patient_response,
        adverse_reaction,
        adverse_reaction_details,
        adherence_percentage,
        doctor_notes,
        patient_notes,
        ai_effectiveness_score,
        ai_adverse_risk_score,
        ai_recommendation,
        "Synthetic",
        ETL_NAME,
        ETL_NAME
    )

    batch.append(record)

    if len(batch) >= BATCH_SIZE:

        try:
            cursor.executemany(
                insert_sql,
                batch
            )

            connection.commit()

            inserted += len(batch)

            print(
                f"Inserted: {inserted:,} / "
                f"{len(valid_rows):,}"
            )

            batch = []

        except Exception as e:

            connection.rollback()

            print("\nERROR during batch insertion:")
            print(e)

            cursor.close()
            connection.close()
            sys.exit(1)


# ============================================================
# FINAL BATCH
# ============================================================

if batch:

    try:
        cursor.executemany(
            insert_sql,
            batch
        )

        connection.commit()

        inserted += len(batch)

    except Exception as e:

        connection.rollback()

        print("\nERROR during final batch insertion:")
        print(e)

        cursor.close()
        connection.close()
        sys.exit(1)


# ============================================================
# FINAL COUNT
# ============================================================

cursor.execute(
    "SELECT COUNT(*) FROM patient_medications_map"
)

database_count = cursor.fetchone()[0]


# ============================================================
# FINAL REPORT
# ============================================================

print("\n" + "=" * 70)
print("54 - PATIENT MEDICATIONS MAPPING COMPLETED")
print("=" * 70)

print(f"Prescription rows loaded:       {len(prescriptions_df):,}")
print(f"Valid rows:                     {len(valid_rows):,}")
print(f"Invalid Patient_ID:             {invalid_patient:,}")
print(f"Invalid Medication_ID:          {invalid_medication:,}")
print(f"Invalid Doctor_ID:              {invalid_doctor:,}")
print(f"Invalid Prescription_Date:      {invalid_date:,}")
print(f"Inserted mappings:              {inserted:,}")
print(f"Database mappings:              {database_count:,}")

cursor.close()
connection.close()

print("\nMySQL connection closed.")
print("=" * 70)
