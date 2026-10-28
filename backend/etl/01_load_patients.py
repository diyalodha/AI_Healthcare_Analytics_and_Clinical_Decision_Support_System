import os
import sys
from datetime import date, timedelta

import pandas as pd
import mysql.connector
from mysql.connector import Error


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ROOT = r"E:\College Final Year\Major Project\Healthcare_AI_Project"

CSV_FILE = os.path.join(
    PROJECT_ROOT,
    "datasets",
    "synthetic",
    "patients.csv"
)

DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = os.environ.get("MYSQL_PASSWORD")
DB_NAME = "healthcare_ai_db"

TOTAL_ROWS = 100000
BATCH_SIZE = 1000


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clean_value(value):
    """Convert pandas NaN/empty values to Python None."""

    if pd.isna(value):
        return None

    if isinstance(value, str):
        value = value.strip()

        if value == "":
            return None

    return value


def clean_date(value):
    """Convert value to Python date."""

    value = clean_value(value)

    if value is None:
        return None

    converted = pd.to_datetime(value, errors="coerce")

    if pd.isna(converted):
        return None

    return converted.date()


def clean_decimal(value):
    """Convert numeric value safely."""

    value = clean_value(value)

    if value is None:
        return None

    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def clean_family_history(value):
    """Convert Yes/No values to 1/0."""

    value = clean_value(value)

    if value is None:
        return 0

    value = str(value).strip().lower()

    if value in ("yes", "y", "1", "true"):
        return 1

    return 0


def generate_registration_date(dob, row_index):
    """
    Generate deterministic synthetic registration date.

    Rules:
    - Earliest possible date: 2023-01-01
    - Latest possible date: 2026-08-31
    - Registration cannot be before 18th birthday
    - Uses row index to keep results reproducible
    """

    start_date = date(2023, 1, 1)
    end_date = date(2026, 8, 31)

    if dob is None:
        return start_date

    try:
        eighteenth_birthday = date(
            dob.year + 18,
            dob.month,
            dob.day
        )
    except ValueError:
        # Handles February 29 birthdays
        eighteenth_birthday = date(
            dob.year + 18,
            2,
            28
        )

    earliest_date = max(
        start_date,
        eighteenth_birthday
    )

    if earliest_date > end_date:
        return end_date

    available_days = (
        end_date - earliest_date
    ).days

    if available_days <= 0:
        return earliest_date

    offset = row_index % (available_days + 1)

    return earliest_date + timedelta(days=offset)


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print("        AI HEALTHCARE PROJECT - PATIENT ETL")
print("=" * 70)

print(f"CSV File     : {CSV_FILE}")
print(f"Total Rows   : {TOTAL_ROWS}")
print(f"Batch Size   : {BATCH_SIZE}")
print(f"Database     : {DB_NAME}")

print("=" * 70)


# ============================================================
# CHECK CSV
# ============================================================

if not os.path.exists(CSV_FILE):

    print("\nERROR: patients.csv not found.")
    print(f"Expected location:\n{CSV_FILE}")

    sys.exit(1)

print("\nCSV file found successfully.")


# ============================================================
# DATABASE CONNECTION
# ============================================================

try:

    connection = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    if connection.is_connected():
        print("MySQL connection successful.")

except Error as e:

    print("\nERROR: Could not connect to MySQL.")
    print(e)

    sys.exit(1)


cursor = connection.cursor()


# ============================================================
# CHECK EXISTING PATIENTS
# ============================================================

try:

    cursor.execute("""
        SELECT Patient_ID
        FROM patients
    """)

    existing_ids = {
        row[0]
        for row in cursor.fetchall()
    }

    print(
        f"Existing patients in database: "
        f"{len(existing_ids):,}"
    )

except Error as e:

    print("\nERROR while checking existing patients:")
    print(e)

    cursor.close()
    connection.close()

    sys.exit(1)


# ============================================================
# CHECK EXISTING PHONE NUMBERS
# ============================================================

try:

    cursor.execute("""
        SELECT Phone
        FROM patients
        WHERE Phone IS NOT NULL
    """)

    existing_phones = {
        str(row[0])
        for row in cursor.fetchall()
        if row[0] is not None
    }

    print(
        f"Existing phone numbers in database: "
        f"{len(existing_phones):,}"
    )

except Error as e:

    print("\nERROR while checking existing phone numbers:")
    print(e)

    cursor.close()
    connection.close()

    sys.exit(1)


# ============================================================
# READ CSV
# ============================================================

print("\nReading patients.csv...")

try:

    df = pd.read_csv(
        CSV_FILE,
        nrows=TOTAL_ROWS
    )

except Exception as e:

    print("\nERROR reading patients.csv:")
    print(e)

    cursor.close()
    connection.close()

    sys.exit(1)


print(
    f"Rows loaded from CSV: {len(df):,}"
)


# ============================================================
# REMOVE ALREADY INSERTED PATIENTS
# ============================================================

print("\nChecking for existing Patient_IDs...")

original_count = len(df)

df_new = df[
    ~df["Patient_ID"].isin(existing_ids)
].copy()

remaining_count = len(df_new)

skipped_count = (
    original_count - remaining_count
)

print(
    f"Already present / skipped : "
    f"{skipped_count:,}"
)

print(
    f"New patients to insert     : "
    f"{remaining_count:,}"
)


# ============================================================
# NOTHING TO INSERT
# ============================================================

if remaining_count == 0:

    print("\nAll patients are already loaded.")

    cursor.close()
    connection.close()

    sys.exit(0)


# ============================================================
# SQL INSERT
# ============================================================

insert_sql = """
INSERT INTO patients
(
    Patient_ID,
    First_Name,
    Last_Name,
    Date_of_Birth,
    Gender,
    Blood_Group,
    Phone,
    City,
    Occupation,
    Height_cm,
    Weight_kg,
    BMI,
    Smoking_Status,
    Alcohol_Consumption,
    Family_History,
    Emergency_Contact_Name,
    Registration_Date,
    Status
)
VALUES
(
    %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s
)
"""


# ============================================================
# PREPARE RECORDS
# ============================================================

print("\nPreparing new patient records...")

records = []

duplicate_phone_count = 0
database_phone_conflict_count = 0

# Track phone numbers while preparing this run.
# This prevents duplicate phone numbers within the CSV
# from violating the UNIQUE constraint in MySQL.

used_phones = set(existing_phones)


for index, row in df_new.iterrows():

    patient_id = clean_value(
        row.get("Patient_ID")
    )

    first_name = clean_value(
        row.get("First_Name")
    )

    last_name = clean_value(
        row.get("Last_Name")
    )

    dob = clean_date(
        row.get("Date_of_Birth")
    )

    gender = clean_value(
        row.get("Gender")
    )

    blood_group = clean_value(
        row.get("Blood_Group")
    )

    phone = clean_value(
        row.get("Phone_Number")
    )

    # --------------------------------------------------------
    # DUPLICATE PHONE HANDLING
    # --------------------------------------------------------

    if phone is not None:

        phone = str(phone).strip()

        if phone in used_phones:

            # Do not invent a phone number.
            # Keep patient record but store NULL.
            phone = None

            duplicate_phone_count += 1

        else:

            used_phones.add(phone)

    city = clean_value(
        row.get("City")
    )

    occupation = clean_value(
        row.get("Occupation")
    )

    height_cm = clean_decimal(
        row.get("Height_cm")
    )

    weight_kg = clean_decimal(
        row.get("Weight_kg")
    )

    bmi = clean_decimal(
        row.get("BMI")
    )

    smoking_status = clean_value(
        row.get("Smoking_Status")
    )

    alcohol_consumption = clean_value(
        row.get("Alcohol_Consumption")
    )

    family_history = clean_family_history(
        row.get("Family_History")
    )

    emergency_contact_name = clean_value(
        row.get("Emergency_Contact_Name")
    )

    status = clean_value(
        row.get("Status")
    )

    registration_date = generate_registration_date(
        dob,
        index
    )

    record = (
        patient_id,
        first_name,
        last_name,
        dob,
        gender,
        blood_group,
        phone,
        city,
        occupation,
        height_cm,
        weight_kg,
        bmi,
        smoking_status,
        alcohol_consumption,
        family_history,
        emergency_contact_name,
        registration_date,
        status
    )

    records.append(record)


print(
    f"Prepared records: {len(records):,}"
)

print(
    f"Duplicate phone values handled: "
    f"{duplicate_phone_count:,}"
)


# ============================================================
# INSERT IN BATCHES
# ============================================================

print("\nStarting database insertion...")
print("-" * 70)

inserted = 0

try:

    for start in range(
        0,
        len(records),
        BATCH_SIZE
    ):

        batch = records[
            start:start + BATCH_SIZE
        ]

        cursor.executemany(
            insert_sql,
            batch
        )

        connection.commit()

        inserted += len(batch)

        print(
            f"Inserted {inserted:,} / "
            f"{len(records):,} new patients"
        )


except Error as e:

    connection.rollback()

    print("\nERROR during patient insertion:")
    print(e)

    cursor.close()
    connection.close()

    sys.exit(1)


# ============================================================
# FINAL VERIFICATION
# ============================================================

cursor.execute("""
    SELECT COUNT(*)
    FROM patients
""")

total_patients = cursor.fetchone()[0]


# ============================================================
# FINAL OUTPUT
# ============================================================

print("\n" + "=" * 70)
print("PATIENT ETL COMPLETED SUCCESSFULLY")
print("=" * 70)

print(
    f"Previously loaded : {skipped_count:,}"
)

print(
    f"Inserted this run  : {inserted:,}"
)

print(
    f"Duplicate phones handled : "
    f"{duplicate_phone_count:,}"
)

print(
    f"Total patients     : {total_patients:,}"
)

print("=" * 70)


# ============================================================
# SAMPLE VERIFICATION
# ============================================================

print("\nSample patient records:")

cursor.execute("""
    SELECT
        Patient_ID,
        First_Name,
        Last_Name,
        Date_of_Birth,
        Phone,
        Registration_Date,
        Status
    FROM patients
    ORDER BY Created_At DESC
    LIMIT 5
""")

for row in cursor.fetchall():
    print(row)


# ============================================================
# CLEANUP
# ============================================================

cursor.close()
connection.close()

print("\nDatabase connection closed.")
print("Patient ETL finished.")