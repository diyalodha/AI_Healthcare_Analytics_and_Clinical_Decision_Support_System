
import os
import sys
import pandas as pd
import mysql.connector
from mysql.connector import Error

# ============================================================
# AI HEALTHCARE PROJECT - ADMISSION ETL
# ============================================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

CSV_FILE = os.path.join(
    BASE_DIR,
    "datasets",
    "synthetic",
    "admissions.csv"
)

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": os.environ["MYSQL_PASSWORD"],
    "database": "healthcare_ai_db"
}

BATCH_SIZE = 1000

REQUIRED_COLUMNS = [
    "Admission_ID",
    "Patient_ID",
    "Department_ID",
    "Doctor_ID",
    "Admission_Date",
    "Discharge_Date",
    "Admission_Type",
    "Admission_Status",
    "Length_of_Stay",
    "Room_Number",
    "Payment_Status"
]


def print_header():
    print("=" * 70)
    print("        AI HEALTHCARE PROJECT - ADMISSION ETL")
    print("=" * 70)
    print(f"CSV File     : {CSV_FILE}")
    print(f"Batch Size   : {BATCH_SIZE}")
    print(f"Database     : {DB_CONFIG['database']}")
    print("=" * 70)


def get_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():
            print("MySQL connection successful.")
            return connection

    except Error as e:
        print(f"\nâŒ MySQL connection failed: {e}")
        return None


def load_reference_ids(cursor):
    print("\nLoading reference IDs...")

    cursor.execute("SELECT Patient_ID FROM patients")
    valid_patients = {row[0] for row in cursor.fetchall()}

    cursor.execute("SELECT Department_ID FROM departments")
    valid_departments = {row[0] for row in cursor.fetchall()}

    cursor.execute("SELECT Doctor_ID FROM doctors")
    valid_doctors = {row[0] for row in cursor.fetchall()}

    cursor.execute("SELECT Admission_ID FROM admissions")
    existing_admissions = {row[0] for row in cursor.fetchall()}

    print(f"Valid patients       : {len(valid_patients):,}")
    print(f"Valid departments    : {len(valid_departments):,}")
    print(f"Valid doctors        : {len(valid_doctors):,}")
    print(f"Existing admissions  : {len(existing_admissions):,}")

    return (
        valid_patients,
        valid_departments,
        valid_doctors,
        existing_admissions
    )


def clean_value(value):
    if pd.isna(value):
        return None

    return value


def main():

    print_header()

    # --------------------------------------------------------
    # Check CSV
    # --------------------------------------------------------
    if not os.path.exists(CSV_FILE):
        print("\nâŒ CSV file not found:")
        print(CSV_FILE)
        sys.exit(1)

    print("\nCSV file found successfully.")

    # --------------------------------------------------------
    # Database connection
    # --------------------------------------------------------
    connection = get_connection()

    if connection is None:
        sys.exit(1)

    cursor = connection.cursor()

    try:

        # ----------------------------------------------------
        # Reference IDs
        # ----------------------------------------------------
        (
            valid_patients,
            valid_departments,
            valid_doctors,
            existing_admissions
        ) = load_reference_ids(cursor)

        # ----------------------------------------------------
        # Read CSV
        # ----------------------------------------------------
        print("\nReading admissions.csv...")

        df = pd.read_csv(CSV_FILE)

        print(f"Rows loaded from CSV: {len(df):,}")

        # ----------------------------------------------------
        # Verify columns
        # ----------------------------------------------------
        missing_columns = [
            column for column in REQUIRED_COLUMNS
            if column not in df.columns
        ]

        if missing_columns:
            print("\nâŒ Missing CSV columns:")

            for column in missing_columns:
                print(f"   - {column}")

            sys.exit(1)

        print("CSV columns verified successfully.")

        # ----------------------------------------------------
        # Counters
        # ----------------------------------------------------
        csv_duplicates = 0
        existing_skipped = 0
        invalid_patient = 0
        invalid_department = 0
        invalid_doctor = 0
        invalid_admission_date = 0
        invalid_discharge_date = 0
        invalid_type = 0
        invalid_status = 0
        invalid_length_of_stay = 0
        invalid_rows = 0

        prepared_records = []

        seen_ids = set()

        # ----------------------------------------------------
        # Allowed ENUM values
        # ----------------------------------------------------
        allowed_admission_types = {
            "Emergency",
            "Routine",
            "Referral",
            "Transfer"
        }

        allowed_statuses = {
            "Admitted",
            "Under Observation",
            "ICU",
            "Discharged",
            "Transferred",
            "Expired"
        }

        # ----------------------------------------------------
        # Prepare records
        # ----------------------------------------------------
        print("\nPreparing admission records...")
        print("-" * 70)

        for csv_row_number, (_, row) in enumerate(
            df.iterrows(),
            start=1
        ):

            admission_id = clean_value(row["Admission_ID"])
            patient_id = clean_value(row["Patient_ID"])
            department_id = clean_value(row["Department_ID"])
            doctor_id = clean_value(row["Doctor_ID"])

            # -----------------------------------------------
            # Admission ID
            # -----------------------------------------------
            if not admission_id:
                invalid_rows += 1
                continue

            if admission_id in seen_ids:
                csv_duplicates += 1
                continue

            seen_ids.add(admission_id)

            if admission_id in existing_admissions:
                existing_skipped += 1
                continue

            # -----------------------------------------------
            # Patient
            # -----------------------------------------------
            if not patient_id or patient_id not in valid_patients:
                invalid_patient += 1
                continue

            # -----------------------------------------------
            # Department
            # -----------------------------------------------
            if not department_id or department_id not in valid_departments:
                invalid_department += 1
                continue

            # -----------------------------------------------
            # Doctor
            # -----------------------------------------------
            if not doctor_id or doctor_id not in valid_doctors:
                invalid_doctor += 1
                continue

            # -----------------------------------------------
            # Admission Date
            # -----------------------------------------------
            admission_date = pd.to_datetime(
                row["Admission_Date"],
                errors="coerce"
            )

            if pd.isna(admission_date):
                invalid_admission_date += 1
                continue

            # -----------------------------------------------
            # Discharge Date
            # -----------------------------------------------
            discharge_date = pd.to_datetime(
                row["Discharge_Date"],
                errors="coerce"
            )

            if pd.isna(discharge_date):
                discharge_date = None

            # -----------------------------------------------
            # Admission Type
            # -----------------------------------------------
            admission_type = clean_value(row["Admission_Type"])

            if admission_type not in allowed_admission_types:
                invalid_type += 1
                continue

            # -----------------------------------------------
            # Admission Status
            # -----------------------------------------------
            admission_status = clean_value(row["Admission_Status"])

            if admission_status not in allowed_statuses:
                invalid_status += 1
                continue

            # -----------------------------------------------
            # Length of Stay
            # -----------------------------------------------
            length_of_stay = clean_value(row["Length_of_Stay"])

            try:
                if length_of_stay is not None:
                    length_of_stay = int(length_of_stay)

                    if length_of_stay < 0:
                        invalid_length_of_stay += 1
                        continue

            except (ValueError, TypeError):
                invalid_length_of_stay += 1
                continue

            # -----------------------------------------------
            # Room Number
            # -----------------------------------------------
            room_number = clean_value(row["Room_Number"])

            if room_number is not None:
                room_number = str(room_number)

                if room_number.endswith(".0"):
                    room_number = room_number[:-2]

            # -----------------------------------------------
            # Generate UNIQUE Admission Number
            #
            # CSV does not contain Admission_Number.
            # Generate a deterministic number based on
            # the CSV row position.
            #
            # Example:
            # ADM-000001
            # ADM-000002
            # ...
            # ADM-300000
            # -----------------------------------------------
            admission_number = f"ADM-{csv_row_number:06d}"

            prepared_records.append(
                (
                    admission_id,
                    patient_id,
                    department_id,
                    doctor_id,
                    None,                       # Bed_ID
                    None,                       # Room_ID
                    admission_number,
                    admission_date.to_pydatetime(),
                    (
                        discharge_date.date()
                        if discharge_date is not None
                        else None
                    ),
                    (
                        discharge_date.date()
                        if discharge_date is not None
                        else None
                    ),
                    admission_type,
                    None,                       # Admission_Reason
                    None,                       # Initial_Diagnosis
                    None,                       # Ward
                    room_number,
                    None,                       # Bed_Number
                    admission_status,
                    length_of_stay,
                    1 if admission_status == "ICU" else 0,
                    0,                          # Requires_Surgery
                    1 if admission_type == "Emergency" else 0,
                    None,                       # Notes
                    "Low",                      # AI_Risk_Level
                    None,                       # Predicted_Disease_ID
                    1,                          # Is_Active
                    0,                          # Is_Deleted
                    1,                          # Record_Version
                    "Synthetic Generator",
                    "Synthetic Generator"
                )
            )

        # ----------------------------------------------------
        # Preparation Summary
        # ----------------------------------------------------
        print(f"Prepared records        : {len(prepared_records):,}")
        print(f"Existing records skipped: {existing_skipped:,}")
        print(f"CSV duplicates skipped  : {csv_duplicates:,}")
        print(f"Invalid Patient_ID      : {invalid_patient:,}")
        print(f"Invalid Department_ID   : {invalid_department:,}")
        print(f"Invalid Doctor_ID       : {invalid_doctor:,}")
        print(f"Invalid Admission_Date  : {invalid_admission_date:,}")
        print(f"Invalid Discharge_Date  : {invalid_discharge_date:,}")
        print(f"Invalid Admission_Type  : {invalid_type:,}")
        print(f"Invalid Status          : {invalid_status:,}")
        print(f"Invalid Length_of_Stay  : {invalid_length_of_stay:,}")
        print(f"Other invalid rows      : {invalid_rows:,}")

        # ----------------------------------------------------
        # Insert
        # ----------------------------------------------------
        print("\nStarting database insertion...")
        print("-" * 70)

        insert_query = """
            INSERT INTO admissions (
                Admission_ID,
                Patient_ID,
                Department_ID,
                Admitting_Doctor_ID,
                Bed_ID,
                Room_ID,
                Admission_Number,
                Admission_Date,
                Expected_Discharge_Date,
                Actual_Discharge_Date,
                Admission_Type,
                Admission_Reason,
                Initial_Diagnosis,
                Ward,
                Room_Number,
                Bed_Number,
                Current_Status,
                Length_of_Stay,
                Is_ICU_Admission,
                Requires_Surgery,
                Is_Emergency,
                Notes,
                AI_Risk_Level,
                Predicted_Disease_ID,
                Is_Active,
                Is_Deleted,
                Record_Version,
                Created_By,
                Updated_By
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """

        inserted = 0

        for start in range(
            0,
            len(prepared_records),
            BATCH_SIZE
        ):

            batch = prepared_records[
                start:start + BATCH_SIZE
            ]

            cursor.executemany(
                insert_query,
                batch
            )

            connection.commit()

            inserted += len(batch)

            print(
                f"Inserted {inserted:,} / "
                f"{len(prepared_records):,} admissions"
            )

        # ----------------------------------------------------
        # Final Count
        # ----------------------------------------------------
        cursor.execute(
            "SELECT COUNT(*) FROM admissions"
        )

        total_admissions = cursor.fetchone()[0]

        print("\n" + "=" * 70)
        print("ADMISSION ETL COMPLETED SUCCESSFULLY")
        print("=" * 70)

        print(f"CSV rows processed        : {len(df):,}")
        print(f"Existing records skipped  : {existing_skipped:,}")
        print(f"CSV duplicates skipped    : {csv_duplicates:,}")
        print(f"Invalid Patient_ID        : {invalid_patient:,}")
        print(f"Invalid Department_ID     : {invalid_department:,}")
        print(f"Invalid Doctor_ID         : {invalid_doctor:,}")
        print(f"Invalid Admission_Date    : {invalid_admission_date:,}")
        print(f"Invalid Discharge_Date   : {invalid_discharge_date:,}")
        print(f"Invalid Admission_Type    : {invalid_type:,}")
        print(f"Invalid Status            : {invalid_status:,}")
        print(f"Invalid Length_of_Stay    : {invalid_length_of_stay:,}")
        print(f"Inserted this run         : {inserted:,}")
        print(f"Total admissions          : {total_admissions:,}")

        print("=" * 70)

        # ----------------------------------------------------
        # Sample Records
        # ----------------------------------------------------
        print("\nSample admission records:")
        print("-" * 70)

        cursor.execute("""
            SELECT
                Admission_ID,
                Patient_ID,
                Department_ID,
                Admitting_Doctor_ID,
                Admission_Date,
                Current_Status,
                Length_of_Stay,
                Room_Number,
                Admission_Number
            FROM admissions
            ORDER BY Admission_Date
            LIMIT 10
        """)

        for record in cursor.fetchall():
            print(record)

        print("\nDatabase connection closed.")
        print("Admission ETL finished.")

    except Error as e:

        connection.rollback()

        print("\n" + "=" * 70)
        print("âŒ ADMISSION ETL FAILED")
        print("=" * 70)
        print(f"Database error: {e}")
        print("=" * 70)

        sys.exit(1)

    except Exception as e:

        connection.rollback()

        print("\n" + "=" * 70)
        print("âŒ ADMISSION ETL FAILED")
        print("=" * 70)
        print(f"Error: {e}")
        print("=" * 70)

        sys.exit(1)

    finally:

        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    main()

