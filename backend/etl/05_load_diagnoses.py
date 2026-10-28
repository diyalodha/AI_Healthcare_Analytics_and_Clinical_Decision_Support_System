import os
import csv
import mysql.connector
from datetime import datetime

# ============================================================
# CONFIGURATION
# ============================================================

DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = os.environ.get("MYSQL_USER", "root")
DB_PASSWORD = os.environ.get("MYSQL_PASSWORD")
DB_NAME = "healthcare_ai_db"

if not DB_PASSWORD:
    raise RuntimeError(
        "MYSQL_PASSWORD environment variable is not set."
    )

CSV_FILE = os.path.join(
    "datasets",
    "synthetic",
    "diagnoses.csv"
)

BATCH_SIZE = 1000


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clean(value):
    """Convert empty CSV values to None and strip whitespace."""
    if value is None:
        return None

    value = str(value).strip()

    if value == "":
        return None

    return value


def parse_datetime(value):
    """Convert CSV datetime into MySQL-compatible datetime."""

    value = clean(value)

    if value is None:
        return None

    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M",
        "%Y-%m-%d"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue

    return None


def parse_date(value):
    """Convert CSV date into MySQL-compatible date."""

    value = clean(value)

    if value is None:
        return None

    formats = [
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue

    return None


def parse_decimal(value):
    """Convert numeric value to float."""

    value = clean(value)

    if value is None:
        return None

    try:
        return float(value)
    except ValueError:
        return None


def parse_boolean(value, default=0):
    """Convert common boolean representations to 0/1."""

    value = clean(value)

    if value is None:
        return default

    value_lower = value.lower()

    if value_lower in ("1", "true", "yes", "y"):
        return 1

    if value_lower in ("0", "false", "no", "n"):
        return 0

    return default


# ============================================================
# MAIN ETL
# ============================================================

def main():

    print("=" * 70)
    print("        AI HEALTHCARE PROJECT - DIAGNOSIS ETL")
    print("=" * 70)
    print(f"CSV File     : {os.path.abspath(CSV_FILE)}")
    print(f"Batch Size   : {BATCH_SIZE}")
    print(f"Database     : {DB_NAME}")
    print("=" * 70)

    # --------------------------------------------------------
    # CHECK CSV FILE
    # --------------------------------------------------------

    if not os.path.exists(CSV_FILE):
        print("\nâŒ CSV file not found.")
        print(f"Expected location: {os.path.abspath(CSV_FILE)}")
        return

    print("\nCSV file found successfully.")

    # --------------------------------------------------------
    # DATABASE CONNECTION
    # --------------------------------------------------------

    try:
        conn = get_connection()
        cursor = conn.cursor()

        print("MySQL connection successful.")

    except mysql.connector.Error as err:
        print("\nâŒ MySQL connection failed.")
        print(err)
        return

    # --------------------------------------------------------
    # LOAD EXISTING REFERENCE IDs
    # --------------------------------------------------------

    print("\nLoading reference IDs...")

    cursor.execute("""
        SELECT Patient_ID
        FROM patients
        WHERE Is_Deleted = 0
    """)

    valid_patients = {row[0] for row in cursor.fetchall()}

    cursor.execute("""
        SELECT Doctor_ID
        FROM doctors
        WHERE Is_Active = 1
          AND Is_Deleted = 0
    """)

    valid_doctors = {row[0] for row in cursor.fetchall()}

    cursor.execute("""
        SELECT Disease_ID
        FROM diseases
        WHERE Is_Active = 1
          AND Is_Deleted = 0
    """)

    valid_diseases = {row[0] for row in cursor.fetchall()}

    cursor.execute("""
        SELECT Appointment_ID
        FROM appointments
    """)

    valid_appointments = {row[0] for row in cursor.fetchall()}

    cursor.execute("""
        SELECT Admission_ID
        FROM admissions
    """)

    valid_admissions = {row[0] for row in cursor.fetchall()}

    print(f"Valid patients       : {len(valid_patients):,}")
    print(f"Valid doctors        : {len(valid_doctors):,}")
    print(f"Valid diseases       : {len(valid_diseases):,}")
    print(f"Valid appointments   : {len(valid_appointments):,}")
    print(f"Valid admissions     : {len(valid_admissions):,}")

    # --------------------------------------------------------
    # LOAD EXISTING DIAGNOSIS NUMBERS
    # --------------------------------------------------------

    cursor.execute("""
        SELECT Diagnosis_ID, Diagnosis_Number
        FROM diagnoses
    """)

    existing_diagnosis_ids = {
        row[0]
        for row in cursor.fetchall()
    }

    print(
        f"Existing diagnoses  : "
        f"{len(existing_diagnosis_ids):,}"
    )

    # --------------------------------------------------------
    # REQUIRED CSV COLUMNS
    # --------------------------------------------------------

    required_columns = {
        "Diagnosis_ID",
        "Patient_ID",
        "Admission_ID",
        "Disease_ID",
        "Diagnosis_Date",
        "Diagnosis_Type",
        "Diagnosis_Status",
        "Doctor_ID",
        "Severity",
        "Notes"
    }

    # --------------------------------------------------------
    # READ CSV
    # --------------------------------------------------------

    print("\nReading diagnoses.csv...")

    try:
        with open(
            CSV_FILE,
            "r",
            encoding="utf-8-sig",
            newline=""
        ) as file:

            reader = csv.DictReader(file)

            csv_columns = set(reader.fieldnames or [])

            missing_columns = required_columns - csv_columns

            if missing_columns:
                print("\nâŒ Missing required CSV columns:")
                for column in sorted(missing_columns):
                    print(f"   - {column}")

                cursor.close()
                conn.close()
                return

            print("CSV columns verified successfully.")

            # ------------------------------------------------
            # PREPARE BATCH
            # ------------------------------------------------

            insert_query = """
                INSERT INTO diagnoses (
                    Diagnosis_ID,
                    Patient_ID,
                    Doctor_ID,
                    Disease_ID,
                    Appointment_ID,
                    Admission_ID,
                    Diagnosis_Number,
                    Diagnosis_Date,
                    Chief_Complaint,
                    Symptoms,
                    Clinical_Notes,
                    Severity,
                    Diagnosis_Status,
                    Diagnosis_Method,
                    Stage,
                    Is_Primary_Diagnosis,
                    Follow_Up_Required,
                    Follow_Up_Date,
                    AI_Prediction_Used,
                    AI_Confidence,
                    AI_Model_Name,
                    Ground_Truth_Verified,
                    Is_Active,
                    Is_Deleted,
                    Record_Version,
                    Created_By,
                    Updated_By
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s
                )
            """

            batch = []

            total_rows = 0
            inserted_rows = 0

            skipped_existing = 0
            skipped_duplicate_csv = 0

            invalid_patient = 0
            invalid_doctor = 0
            invalid_disease = 0
            invalid_appointment = 0
            invalid_admission = 0
            invalid_date = 0

            seen_diagnosis_ids = set()

            print("\nPreparing diagnosis records...")
            print("-" * 70)

            # ------------------------------------------------
            # PROCESS EACH CSV ROW
            # ------------------------------------------------

            for row in reader:

                total_rows += 1

                diagnosis_id = clean(row.get("Diagnosis_ID"))
                patient_id = clean(row.get("Patient_ID"))
                doctor_id = clean(row.get("Doctor_ID"))
                disease_id = clean(row.get("Disease_ID"))

                appointment_id = clean(row.get("Appointment_ID"))
                admission_id = clean(row.get("Admission_ID"))

                diagnosis_number = clean(
                    row.get("Diagnosis_Number")
                )

                diagnosis_date = parse_datetime(
                    row.get("Diagnosis_Date")
                )

                # ------------------------------------------------
                # DIAGNOSIS NUMBER
                # ------------------------------------------------

                if not diagnosis_number:

                    # Generate a deterministic diagnosis number
                    diagnosis_number = (
                        f"DX-{total_rows:07d}"
                    )

                # ------------------------------------------------
                # EXISTING RECORD
                # ------------------------------------------------

                if diagnosis_id in existing_diagnosis_ids:
                    skipped_existing += 1
                    continue

                # ------------------------------------------------
                # DUPLICATE IN CURRENT CSV
                # ------------------------------------------------

                if diagnosis_id in seen_diagnosis_ids:
                    skipped_duplicate_csv += 1
                    continue

                seen_diagnosis_ids.add(diagnosis_id)

                # ------------------------------------------------
                # REQUIRED REFERENCES
                # ------------------------------------------------

                if patient_id not in valid_patients:
                    invalid_patient += 1
                    continue

                if doctor_id not in valid_doctors:
                    invalid_doctor += 1
                    continue

                if disease_id not in valid_diseases:
                    invalid_disease += 1
                    continue

                # ------------------------------------------------
                # OPTIONAL APPOINTMENT
                # ------------------------------------------------

                if appointment_id:

                    if appointment_id not in valid_appointments:
                        invalid_appointment += 1
                        appointment_id = None

                # ------------------------------------------------
                # OPTIONAL ADMISSION
                # ------------------------------------------------

                if admission_id:

                    if admission_id not in valid_admissions:
                        invalid_admission += 1
                        admission_id = None

                # ------------------------------------------------
                # DIAGNOSIS DATE
                # ------------------------------------------------

                if diagnosis_date is None:
                    invalid_date += 1
                    continue

                # ------------------------------------------------
                # SOURCE â†’ DATABASE MAPPING
                # ------------------------------------------------

                chief_complaint = None

                symptoms = None

                clinical_notes = clean(
                    row.get("Notes")
                )

                # Severity
                severity = clean(
                    row.get("Severity")
                )

                valid_severities = {
                    "Low",
                    "Moderate",
                    "High",
                    "Critical"
                }

                if severity not in valid_severities:
                    severity = None

                # Diagnosis status
                diagnosis_status = clean(
                    row.get("Diagnosis_Status")
                )

                valid_statuses = {
                    "Confirmed",
                    "Suspected",
                    "Ruled Out"
                }

                if diagnosis_status not in valid_statuses:
                    diagnosis_status = "Confirmed"

                # Diagnosis type â†’ Diagnosis_Method
                diagnosis_type = clean(
                    row.get("Diagnosis_Type")
                )

                method_mapping = {
                    "Clinical": "Clinical Examination",
                    "Clinical Examination": "Clinical Examination",
                    "Laboratory": "Laboratory",
                    "Lab": "Laboratory",
                    "Radiology": "Radiology",
                    "Imaging": "Radiology",
                    "AI": "AI Prediction",
                    "AI Prediction": "AI Prediction",
                    "Combined": "Combined"
                }

                diagnosis_method = method_mapping.get(
                    diagnosis_type,
                    "Clinical Examination"
                )

                # ------------------------------------------------
                # DEFAULT / DERIVED FIELDS
                # ------------------------------------------------

                stage = None

                is_primary = 1

                follow_up_required = 0

                follow_up_date = None

                ai_prediction_used = 0

                ai_confidence = None

                ai_model_name = None

                ground_truth_verified = 0

                # Synthetic data is treated as ground truth
                if diagnosis_status == "Confirmed":
                    ground_truth_verified = 1

                # AI mapping
                if diagnosis_method == "AI Prediction":
                    ai_prediction_used = 1

                # ------------------------------------------------
                # BUILD RECORD
                # ------------------------------------------------

                record = (
                    diagnosis_id,
                    patient_id,
                    doctor_id,
                    disease_id,
                    appointment_id,
                    admission_id,
                    diagnosis_number,
                    diagnosis_date,
                    chief_complaint,
                    symptoms,
                    clinical_notes,
                    severity,
                    diagnosis_status,
                    diagnosis_method,
                    stage,
                    is_primary,
                    follow_up_required,
                    follow_up_date,
                    ai_prediction_used,
                    ai_confidence,
                    ai_model_name,
                    ground_truth_verified,
                    1,              # Is_Active
                    0,              # Is_Deleted
                    1,              # Record_Version
                    "Synthetic_ETL",
                    None            # Updated_By
                )

                batch.append(record)

                # ------------------------------------------------
                # INSERT BATCH
                # ------------------------------------------------

                if len(batch) >= BATCH_SIZE:

                    try:
                        cursor.executemany(
                            insert_query,
                            batch
                        )

                        conn.commit()

                        inserted_rows += len(batch)

                        print(
                            f"Inserted "
                            f"{inserted_rows:,} records..."
                        )

                        batch.clear()

                    except mysql.connector.Error as err:

                        conn.rollback()

                        print(
                            "\nâŒ Batch insertion error:"
                        )
                        print(err)

                        cursor.close()
                        conn.close()

                        return

            # ------------------------------------------------
            # INSERT REMAINING RECORDS
            # ------------------------------------------------

            if batch:

                try:

                    cursor.executemany(
                        insert_query,
                        batch
                    )

                    conn.commit()

                    inserted_rows += len(batch)

                except mysql.connector.Error as err:

                    conn.rollback()

                    print(
                        "\nâŒ Final batch insertion error:"
                    )
                    print(err)

                    cursor.close()
                    conn.close()

                    return

    except Exception as e:

        print("\nâŒ ETL ERROR")
        print("-" * 70)
        print(e)

        cursor.close()
        conn.close()

        return

    # --------------------------------------------------------
    # FINAL DATABASE COUNT
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM diagnoses
        WHERE Is_Deleted = 0
    """)

    total_database_records = cursor.fetchone()[0]

    # --------------------------------------------------------
    # RESULTS
    # --------------------------------------------------------

    print("\n")
    print("=" * 70)
    print("DIAGNOSIS ETL COMPLETED")
    print("=" * 70)

    print(f"CSV rows processed          : {total_rows:,}")
    print(f"Existing records skipped    : {skipped_existing:,}")
    print(f"CSV duplicates skipped      : {skipped_duplicate_csv:,}")
    print(f"Invalid Patient_ID          : {invalid_patient:,}")
    print(f"Invalid Doctor_ID           : {invalid_doctor:,}")
    print(f"Invalid Disease_ID          : {invalid_disease:,}")
    print(f"Invalid Appointment_ID      : {invalid_appointment:,}")
    print(f"Invalid Admission_ID        : {invalid_admission:,}")
    print(f"Invalid Diagnosis_Date      : {invalid_date:,}")
    print(f"Inserted this run           : {inserted_rows:,}")
    print(f"Total diagnoses in database : {total_database_records:,}")

    print("=" * 70)

    # --------------------------------------------------------
    # SAMPLE RECORDS
    # --------------------------------------------------------

    cursor.execute("""
        SELECT
            Diagnosis_ID,
            Patient_ID,
            Doctor_ID,
            Disease_ID,
            Admission_ID,
            Diagnosis_Number,
            Diagnosis_Date,
            Severity,
            Diagnosis_Status,
            Diagnosis_Method
        FROM diagnoses
        WHERE Is_Deleted = 0
        ORDER BY Diagnosis_Date
        LIMIT 10
    """)

    samples = cursor.fetchall()

    print("\nSample diagnosis records:")
    print("-" * 70)

    for row in samples:
        print(row)

    cursor.close()
    conn.close()

    print("\nDatabase connection closed.")
    print("Diagnosis ETL finished.")


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
