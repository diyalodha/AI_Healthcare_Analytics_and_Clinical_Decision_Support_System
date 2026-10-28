import os
import sys
import pandas as pd
import mysql.connector
from mysql.connector import Error


# ============================================================
# CONFIGURATION
# ============================================================


DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = os.environ.get("MYSQL_USER", "root")
DB_PASSWORD = os.environ.get("MYSQL_PASSWORD")

if not DB_PASSWORD:
    raise RuntimeError(
        "MYSQL_PASSWORD environment variable is not set."
    )

DB_NAME = "healthcare_ai_db"


BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

CSV_PATH = os.path.join(
    BASE_DIR,
    "datasets",
    "synthetic",
    "doctors.csv"
)

BATCH_SIZE = 1000


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    try:

        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        if connection.is_connected():
            return connection

    except Error as e:

        print(f"❌ Database connection failed: {e}")

    return None


# ============================================================
# CLEANING FUNCTIONS
# ============================================================

def clean_string(value):

    if value is None:
        return None

    value = str(value).strip()

    if value == "":
        return None

    return value


def clean_int(value):

    if value is None:
        return None

    value = str(value).strip()

    if value == "":
        return None

    try:
        return int(float(value))

    except (ValueError, TypeError):
        return None


def clean_decimal(value):

    if value is None:
        return None

    value = str(value).strip()

    if value == "":
        return None

    try:
        return float(value)

    except (ValueError, TypeError):
        return None


def clean_bool(value):

    if value is None:
        return None

    value = str(value).strip().lower()

    if value in ("true", "1", "yes"):
        return 1

    if value in ("false", "0", "no"):
        return 0

    return None


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("        AI HEALTHCARE PROJECT - DOCTOR ETL")
    print("=" * 70)

    print(f"CSV File     : {CSV_PATH}")
    print(f"Batch Size   : {BATCH_SIZE}")
    print(f"Database     : {DB_NAME}")
    print("=" * 70)

    # --------------------------------------------------------
    # 1. CHECK CSV
    # --------------------------------------------------------

    if not os.path.exists(CSV_PATH):

        print()
        print("❌ CSV file not found:")
        print(CSV_PATH)

        sys.exit(1)

    print()
    print("CSV file found successfully.")

    # --------------------------------------------------------
    # 2. DATABASE CONNECTION
    # --------------------------------------------------------

    connection = get_connection()

    if connection is None:
        sys.exit(1)

    cursor = connection.cursor()

    print("MySQL connection successful.")

    # --------------------------------------------------------
    # 3. LOAD VALID DEPARTMENT IDs
    # --------------------------------------------------------

    cursor.execute("""
        SELECT Department_ID
        FROM departments
    """)

    valid_department_ids = {
        str(row[0]).strip()
        for row in cursor.fetchall()
        if row[0] is not None
    }

    print(
        f"Valid departments : "
        f"{len(valid_department_ids):,}"
    )

    if len(valid_department_ids) == 0:

        print()
        print("❌ No departments found.")
        print("Load departments before loading doctors.")

        cursor.close()
        connection.close()

        sys.exit(1)

    # --------------------------------------------------------
    # 4. LOAD EXISTING DOCTORS
    # --------------------------------------------------------

    cursor.execute("""
        SELECT
            Doctor_ID,
            Medical_License_No,
            Phone,
            Email
        FROM doctors
    """)

    existing_doctors = cursor.fetchall()

    existing_ids = {
        str(row[0]).strip()
        for row in existing_doctors
        if row[0] is not None
    }

    existing_licenses = {
        str(row[1]).strip().lower()
        for row in existing_doctors
        if row[1] is not None
    }

    existing_phones = {
        str(row[2]).strip().lower()
        for row in existing_doctors
        if row[2] is not None
    }

    existing_emails = {
        str(row[3]).strip().lower()
        for row in existing_doctors
        if row[3] is not None
    }

    print(
        f"Existing doctors  : "
        f"{len(existing_doctors):,}"
    )

    # --------------------------------------------------------
    # 5. READ CSV
    # --------------------------------------------------------

    print()
    print("Reading doctors.csv...")

    try:

        df = pd.read_csv(
            CSV_PATH,
            dtype=str,
            keep_default_na=False
        )

    except Exception as e:

        print()
        print("❌ Failed to read doctors.csv:")
        print(e)

        cursor.close()
        connection.close()

        sys.exit(1)

    print(
        f"Rows loaded from CSV: "
        f"{len(df):,}"
    )

    # --------------------------------------------------------
    # 6. VERIFY COLUMNS
    # --------------------------------------------------------

    required_columns = [
        "Doctor_ID",
        "First_Name",
        "Middle_Name",
        "Last_Name",
        "Gender",
        "Date_of_Birth",
        "Medical_License_No",
        "Qualification",
        "Specialization",
        "Years_of_Experience",
        "Department_ID",
        "Phone",
        "Email",
        "Consultation_Fee",
        "Joining_Date",
        "Shift",
        "Employment_Type",
        "Status",
        "Is_Active",
        "Created_By",
        "Updated_By"
    ]

    missing_columns = [
        col
        for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:

        print()
        print("❌ Missing CSV columns:")

        for col in missing_columns:
            print(f"   - {col}")

        cursor.close()
        connection.close()

        sys.exit(1)

    print("CSV columns verified successfully.")

    # --------------------------------------------------------
    # 7. VALID ENUM VALUES
    # --------------------------------------------------------

    valid_genders = {
        "Male",
        "Female",
        "Other"
    }

    valid_shifts = {
        "Morning",
        "Evening",
        "Night",
        "Rotational"
    }

    valid_employment_types = {
        "Full-Time",
        "Part-Time",
        "Visiting"
    }

    valid_statuses = {
        "Active",
        "Inactive",
        "On Leave"
    }

    # --------------------------------------------------------
    # 8. PREPARE RECORDS
    # --------------------------------------------------------

    print()
    print("Preparing doctor records...")
    print("-" * 70)

    prepared_records = []

    skipped_existing = 0
    skipped_duplicates = 0
    invalid_department = 0
    invalid_rows = 0

    seen_ids = set()
    seen_licenses = set()
    seen_phones = set()
    seen_emails = set()

    for _, row in df.iterrows():

        doctor_id = clean_string(
            row["Doctor_ID"]
        )

        first_name = clean_string(
            row["First_Name"]
        )

        middle_name = clean_string(
            row["Middle_Name"]
        )

        last_name = clean_string(
            row["Last_Name"]
        )

        gender = clean_string(
            row["Gender"]
        )

        date_of_birth = clean_string(
            row["Date_of_Birth"]
        )

        license_no = clean_string(
            row["Medical_License_No"]
        )

        qualification = clean_string(
            row["Qualification"]
        )

        specialization = clean_string(
            row["Specialization"]
        )

        years_experience = clean_int(
            row["Years_of_Experience"]
        )

        department_id = clean_string(
            row["Department_ID"]
        )

        phone = clean_string(
            row["Phone"]
        )

        email = clean_string(
            row["Email"]
        )

        consultation_fee = clean_decimal(
            row["Consultation_Fee"]
        )

        joining_date = clean_string(
            row["Joining_Date"]
        )

        shift = clean_string(
            row["Shift"]
        )

        employment_type = clean_string(
            row["Employment_Type"]
        )

        status = clean_string(
            row["Status"]
        )

        is_active = clean_bool(
            row["Is_Active"]
        )

        created_by = clean_string(
            row["Created_By"]
        )

        updated_by = clean_string(
            row["Updated_By"]
        )

        # ----------------------------------------------------
        # REQUIRED FIELDS
        # ----------------------------------------------------

        if not doctor_id:
            invalid_rows += 1
            continue

        if not first_name:
            invalid_rows += 1
            continue

        if not last_name:
            invalid_rows += 1
            continue

        if not gender:
            invalid_rows += 1
            continue

        if not license_no:
            invalid_rows += 1
            continue

        if not qualification:
            invalid_rows += 1
            continue

        if not specialization:
            invalid_rows += 1
            continue

        if not department_id:
            invalid_rows += 1
            continue

        if not joining_date:
            invalid_rows += 1
            continue

        # ----------------------------------------------------
        # DEPARTMENT FOREIGN KEY
        # ----------------------------------------------------

        if department_id not in valid_department_ids:

            invalid_department += 1
            continue

        # ----------------------------------------------------
        # ENUM VALIDATION
        # ----------------------------------------------------

        if gender not in valid_genders:

            invalid_rows += 1
            continue

        if shift and shift not in valid_shifts:

            invalid_rows += 1
            continue

        if (
            employment_type
            and employment_type
            not in valid_employment_types
        ):

            invalid_rows += 1
            continue

        if status and status not in valid_statuses:

            invalid_rows += 1
            continue

        # ----------------------------------------------------
        # NUMERIC VALIDATION
        # ----------------------------------------------------

        if (
            years_experience is not None
            and years_experience < 0
        ):

            invalid_rows += 1
            continue

        if (
            consultation_fee is not None
            and consultation_fee < 0
        ):

            invalid_rows += 1
            continue

        # ----------------------------------------------------
        # EXISTING DOCTOR CHECK
        # ----------------------------------------------------

        normalized_license = license_no.lower()

        normalized_phone = (
            phone.lower()
            if phone
            else None
        )

        normalized_email = (
            email.lower()
            if email
            else None
        )

        if doctor_id in existing_ids:

            skipped_existing += 1
            continue

        # ----------------------------------------------------
        # DUPLICATE CHECK
        # ----------------------------------------------------

        duplicate = False

        if doctor_id in seen_ids:
            duplicate = True

        if normalized_license in seen_licenses:
            duplicate = True

        if (
            normalized_phone
            and normalized_phone in seen_phones
        ):
            duplicate = True

        if (
            normalized_email
            and normalized_email in seen_emails
        ):
            duplicate = True

        if normalized_license in existing_licenses:
            duplicate = True

        if (
            normalized_phone
            and normalized_phone in existing_phones
        ):
            duplicate = True

        if (
            normalized_email
            and normalized_email in existing_emails
        ):
            duplicate = True

        if duplicate:

            skipped_duplicates += 1
            continue

        # ----------------------------------------------------
        # TRACK UNIQUE VALUES
        # ----------------------------------------------------

        seen_ids.add(doctor_id)
        seen_licenses.add(normalized_license)

        if normalized_phone:
            seen_phones.add(normalized_phone)

        if normalized_email:
            seen_emails.add(normalized_email)

        # ----------------------------------------------------
        # PREPARE RECORD
        # ----------------------------------------------------

        prepared_records.append(
            (
                doctor_id,
                first_name,
                middle_name,
                last_name,
                gender,
                date_of_birth,
                license_no,
                qualification,
                specialization,
                years_experience if years_experience is not None else 0,
                department_id,
                phone,
                email,
                consultation_fee if consultation_fee is not None else 0,
                joining_date,
                shift if shift else "Morning",
                employment_type
                if employment_type
                else "Full-Time",
                status if status else "Active",
                is_active if is_active is not None else 1,
                created_by,
                updated_by
            )
        )

    # --------------------------------------------------------
    # 9. PREPARATION SUMMARY
    # --------------------------------------------------------

    print()
    print(
        f"Prepared records        : "
        f"{len(prepared_records):,}"
    )

    print(
        f"Existing records skipped: "
        f"{skipped_existing:,}"
    )

    print(
        f"CSV duplicates skipped  : "
        f"{skipped_duplicates:,}"
    )

    print(
        f"Invalid Department_ID   : "
        f"{invalid_department:,}"
    )

    print(
        f"Other invalid rows      : "
        f"{invalid_rows:,}"
    )

    # --------------------------------------------------------
    # 10. INSERT SQL
    # --------------------------------------------------------

    insert_sql = """
        INSERT INTO doctors (
            Doctor_ID,
            First_Name,
            Middle_Name,
            Last_Name,
            Gender,
            Date_of_Birth,
            Medical_License_No,
            Qualification,
            Specialization,
            Years_of_Experience,
            Department_ID,
            Phone,
            Email,
            Consultation_Fee,
            Joining_Date,
            Shift,
            Employment_Type,
            Status,
            Is_Active,
            Created_By,
            Updated_By
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s
        )
    """

    # --------------------------------------------------------
    # 11. INSERT BATCHES
    # --------------------------------------------------------

    inserted = 0

    if prepared_records:

        print()
        print("Starting database insertion...")
        print("-" * 70)

        try:

            for start in range(
                0,
                len(prepared_records),
                BATCH_SIZE
            ):

                batch = prepared_records[
                    start:start + BATCH_SIZE
                ]

                cursor.executemany(
                    insert_sql,
                    batch
                )

                connection.commit()

                inserted += len(batch)

                print(
                    f"Inserted "
                    f"{inserted:,} / "
                    f"{len(prepared_records):,} doctors"
                )

        except Error as e:

            connection.rollback()

            print()
            print("=" * 70)
            print("❌ ERROR DURING DOCTOR INSERTION")
            print("=" * 70)
            print(e)

            cursor.close()
            connection.close()

            sys.exit(1)

    else:

        print()
        print("No new doctor records to insert.")

    # --------------------------------------------------------
    # 12. FINAL COUNT
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM doctors
    """)

    total_doctors = cursor.fetchone()[0]

    # --------------------------------------------------------
    # 13. SAMPLE RECORDS
    # --------------------------------------------------------

    cursor.execute("""
        SELECT
            Doctor_ID,
            First_Name,
            Last_Name,
            Gender,
            Specialization,
            Department_ID,
            Status
        FROM doctors
        LIMIT 5
    """)

    sample_records = cursor.fetchall()

    cursor.close()
    connection.close()

    # --------------------------------------------------------
    # 14. FINAL SUMMARY
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("DOCTOR ETL COMPLETED SUCCESSFULLY")
    print("=" * 70)

    print(
        f"Existing skipped       : "
        f"{skipped_existing:,}"
    )

    print(
        f"Inserted this run      : "
        f"{inserted:,}"
    )

    print(
        f"CSV duplicates skipped : "
        f"{skipped_duplicates:,}"
    )

    print(
        f"Invalid Department_ID  : "
        f"{invalid_department:,}"
    )

    print(
        f"Other invalid rows     : "
        f"{invalid_rows:,}"
    )

    print(
        f"Total doctors          : "
        f"{total_doctors:,}"
    )

    print("=" * 70)

    print()
    print("Sample doctor records:")

    for record in sample_records:
        print(record)

    print()
    print("Database connection closed.")
    print("Doctor ETL finished.")


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()