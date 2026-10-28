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
DB_USER = "root"
DB_PASSWORD = os.environ.get("MYSQL_PASSWORD")
DB_NAME = "healthcare_ai_db"

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

CSV_PATH = os.path.join(
    BASE_DIR,
    "datasets",
    "synthetic",
    "departments.csv"
)

BATCH_SIZE = 500


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
        print(f"âŒ Database connection failed: {e}")

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


def clean_bool(value):
    if value is None:
        return None

    value = str(value).strip().lower()

    if value in ("true", "1", "yes"):
        return 1

    if value in ("false", "0", "no"):
        return 0

    return None


def clean_time(value):
    if value is None:
        return None

    value = str(value).strip()

    if value == "":
        return None

    return value


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("STEP 07 - DEPARTMENTS ETL")
    print("=" * 70)

    # --------------------------------------------------------
    # 1. Check CSV
    # --------------------------------------------------------

    if not os.path.exists(CSV_PATH):
        print("âŒ Departments CSV not found:")
        print(CSV_PATH)
        sys.exit(1)

    print(f"ðŸ“ CSV: {CSV_PATH}")

    # --------------------------------------------------------
    # 2. Read CSV
    # --------------------------------------------------------

    try:
        df = pd.read_csv(
            CSV_PATH,
            dtype=str,
            keep_default_na=False
        )
    except Exception as e:
        print(f"âŒ Failed to read CSV: {e}")
        sys.exit(1)

    print(f"ðŸ“Š CSV rows: {len(df):,}")

    # --------------------------------------------------------
    # 3. Required columns
    # --------------------------------------------------------

    required_columns = [
        "Department_ID",
        "Department_Name",
        "Department_Code",
        "Description",
        "Department_Type",
        "Contact_Number",
        "Email",
        "Location",
        "Floor_Number",
        "Extension_Number",
        "Head_Doctor_ID",
        "Total_Doctors",
        "Total_Staff",
        "Capacity",
        "Opening_Time",
        "Closing_Time",
        "Is_24x7",
        "Status",
        "Is_Active"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        print("âŒ Missing CSV columns:")

        for col in missing_columns:
            print(f"   - {col}")

        sys.exit(1)

    print("âœ… CSV columns verified")

    # --------------------------------------------------------
    # 4. Connect to MySQL
    # --------------------------------------------------------

    connection = get_connection()

    if connection is None:
        sys.exit(1)

    cursor = connection.cursor()

    print("âœ… Connected to MySQL")

    # --------------------------------------------------------
    # 5. Get existing departments
    # --------------------------------------------------------

    cursor.execute("""
        SELECT
            Department_ID,
            Department_Name,
            Department_Code,
            Email
        FROM departments
    """)

    existing_rows = cursor.fetchall()

    existing_ids = {
        str(row[0]).strip()
        for row in existing_rows
        if row[0] is not None
    }

    existing_names = {
        str(row[1]).strip().lower()
        for row in existing_rows
        if row[1] is not None
    }

    existing_codes = {
        str(row[2]).strip().lower()
        for row in existing_rows
        if row[2] is not None
    }

    existing_emails = {
        str(row[3]).strip().lower()
        for row in existing_rows
        if row[3] is not None
    }

    print(f"ðŸ¥ Existing departments: {len(existing_rows):,}")

    # --------------------------------------------------------
    # 6. Prepare INSERT statement
    # --------------------------------------------------------

    insert_sql = """
        INSERT INTO departments (
            Department_ID,
            Department_Name,
            Department_Code,
            Description,
            Department_Type,
            Contact_Number,
            Email,
            Location,
            Floor_Number,
            Extension_Number,
            Head_Doctor_ID,
            Total_Doctors,
            Total_Staff,
            Capacity,
            Opening_Time,
            Closing_Time,
            Is_24x7,
            Status,
            Is_Active,
            Created_By
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s
        )
    """

    # --------------------------------------------------------
    # 7. Process CSV rows
    # --------------------------------------------------------

    prepared_rows = []

    skipped_existing = 0
    skipped_duplicates = 0
    invalid_rows = 0

    seen_ids = set()
    seen_names = set()
    seen_codes = set()
    seen_emails = set()

    valid_department_types = {
        "Clinical",
        "Diagnostic",
        "Administrative",
        "Support"
    }

    valid_statuses = {
        "Active",
        "Inactive",
        "Under Maintenance"
    }

    for _, row in df.iterrows():

        department_id = clean_string(row["Department_ID"])
        department_name = clean_string(row["Department_Name"])
        department_code = clean_string(row["Department_Code"])

        description = clean_string(row["Description"])
        department_type = clean_string(row["Department_Type"])

        contact_number = clean_string(row["Contact_Number"])
        email = clean_string(row["Email"])
        location = clean_string(row["Location"])

        floor_number = clean_int(row["Floor_Number"])
        extension_number = clean_string(row["Extension_Number"])

        head_doctor_id = clean_string(row["Head_Doctor_ID"])

        total_doctors = clean_int(row["Total_Doctors"])
        total_staff = clean_int(row["Total_Staff"])
        capacity = clean_int(row["Capacity"])

        opening_time = clean_time(row["Opening_Time"])
        closing_time = clean_time(row["Closing_Time"])

        is_24x7 = clean_bool(row["Is_24x7"])
        status = clean_string(row["Status"])
        is_active = clean_bool(row["Is_Active"])

        # ----------------------------------------------------
        # Required fields
        # ----------------------------------------------------

        if not department_id:
            invalid_rows += 1
            continue

        if not department_name:
            invalid_rows += 1
            continue

        if not department_code:
            invalid_rows += 1
            continue

        if not department_type:
            invalid_rows += 1
            continue

        # ----------------------------------------------------
        # Existing ID
        # ----------------------------------------------------

        if department_id in existing_ids:
            skipped_existing += 1
            continue

        # ----------------------------------------------------
        # Duplicate CSV records
        # ----------------------------------------------------

        normalized_name = department_name.lower()
        normalized_code = department_code.lower()

        normalized_email = (
            email.lower()
            if email
            else None
        )

        duplicate = False

        if department_id in seen_ids:
            duplicate = True

        if normalized_name in seen_names:
            duplicate = True

        if normalized_code in seen_codes:
            duplicate = True

        if normalized_email and normalized_email in seen_emails:
            duplicate = True

        if normalized_name in existing_names:
            duplicate = True

        if normalized_code in existing_codes:
            duplicate = True

        if normalized_email and normalized_email in existing_emails:
            duplicate = True

        if duplicate:
            skipped_duplicates += 1
            continue

        # ----------------------------------------------------
        # Enum validation
        # ----------------------------------------------------

        if department_type not in valid_department_types:
            invalid_rows += 1
            continue

        if status and status not in valid_statuses:
            invalid_rows += 1
            continue

        # ----------------------------------------------------
        # Numeric validation
        # ----------------------------------------------------

        if floor_number is not None and floor_number < 0:
            invalid_rows += 1
            continue

        if total_doctors is not None and total_doctors < 0:
            invalid_rows += 1
            continue

        if total_staff is not None and total_staff < 0:
            invalid_rows += 1
            continue

        if capacity is not None and capacity < 0:
            invalid_rows += 1
            continue

        # ----------------------------------------------------
        # Track values
        # ----------------------------------------------------

        seen_ids.add(department_id)
        seen_names.add(normalized_name)
        seen_codes.add(normalized_code)

        if normalized_email:
            seen_emails.add(normalized_email)

        # ----------------------------------------------------
        # Prepare row
        # ----------------------------------------------------

        prepared_rows.append((
            department_id,
            department_name,
            department_code,
            description,
            department_type,
            contact_number,
            email,
            location,
            floor_number,
            extension_number,

            # Head_Doctor_ID stays NULL because
            # doctors have not been loaded yet.
            head_doctor_id,

            total_doctors if total_doctors is not None else 0,
            total_staff if total_staff is not None else 0,
            capacity if capacity is not None else 0,

            opening_time,
            closing_time,

            is_24x7 if is_24x7 is not None else 0,

            status if status else "Active",

            is_active if is_active is not None else 1,

            "Synthetic_ETL"
        ))

    # --------------------------------------------------------
    # 8. Pre-insert summary
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("PRE-INSERT SUMMARY")
    print("=" * 70)

    print(f"CSV rows               : {len(df):,}")
    print(f"Existing skipped       : {skipped_existing:,}")
    print(f"Duplicate rows skipped : {skipped_duplicates:,}")
    print(f"Invalid rows            : {invalid_rows:,}")
    print(f"Prepared for insertion : {len(prepared_rows):,}")

    # --------------------------------------------------------
    # 9. Insert in batches
    # --------------------------------------------------------

    inserted = 0

    try:

        for start in range(
            0,
            len(prepared_rows),
            BATCH_SIZE
        ):

            batch = prepared_rows[
                start:start + BATCH_SIZE
            ]

            cursor.executemany(
                insert_sql,
                batch
            )

            connection.commit()

            inserted += len(batch)

            print(
                f"   Inserted "
                f"{inserted:,}/"
                f"{len(prepared_rows):,}"
            )

    except Error as e:

        connection.rollback()

        print()
        print("âŒ INSERT FAILED")
        print(e)

        cursor.close()
        connection.close()

        sys.exit(1)

    # --------------------------------------------------------
    # 10. Final database count
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM departments
    """)

    total_departments = cursor.fetchone()[0]

    # --------------------------------------------------------
    # 11. Additional validation
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM departments
        WHERE Department_ID IS NULL
    """)

    null_ids = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM departments
        WHERE Department_Name IS NULL
           OR Department_Code IS NULL
           OR Department_Type IS NULL
    """)

    missing_required = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    # --------------------------------------------------------
    # 12. Final result
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("STEP 07 - DEPARTMENTS ETL COMPLETED")
    print("=" * 70)

    print(f"Inserted departments : {inserted:,}")
    print(f"Total departments    : {total_departments:,}")
    print(f"NULL Department IDs  : {null_ids:,}")
    print(f"Missing required     : {missing_required:,}")

    if (
        total_departments > 0
        and null_ids == 0
        and missing_required == 0
    ):
        print()
        print("âœ… DEPARTMENTS ETL PASSED")
    else:
        print()
        print("âš ï¸ DEPARTMENTS ETL NEEDS REVIEW")

    print("=" * 70)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()