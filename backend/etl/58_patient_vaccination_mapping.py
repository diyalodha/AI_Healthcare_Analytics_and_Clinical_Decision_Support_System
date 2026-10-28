import os
import sys
import uuid
import pandas as pd
import mysql.connector


# ============================================================
# CONFIGURATION
# ============================================================

DB_HOST = "localhost"
DB_USER = "root"
DB_NAME = "healthcare_ai_db"

PROJECT_ROOT = r"E:\College Final Year\Major Project\Healthcare_AI_Project"

SOURCE_FILE = os.path.join(
    PROJECT_ROOT,
    "datasets",
    "synthetic",
    "vaccination_history.csv"
)

TARGET_TABLE = "patient_vaccination_map"

SCRIPT_NAME = "58_patient_vaccination_mapping.py"

BATCH_SIZE = 5000


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    password = os.environ.get("MYSQL_PASSWORD")

    if password is None:
        print("ERROR: MYSQL_PASSWORD environment variable is not set.")
        print()
        print("Run in PowerShell:")
        print('$env:MYSQL_PASSWORD = Read-Host "Enter MySQL root password"')
        sys.exit(1)

    try:

        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=password,
            database=DB_NAME
        )

        print("Connected to MySQL successfully.")

        return conn

    except mysql.connector.Error as e:

        print(f"ERROR connecting to MySQL: {e}")
        sys.exit(1)


# ============================================================
# HELPERS
# ============================================================

def clean_string(value):

    if pd.isna(value):
        return None

    value = str(value).strip()

    if value == "":
        return None

    return value


def clean_date(value):

    if pd.isna(value):
        return None

    try:
        return pd.to_datetime(value).date()

    except Exception:
        return None


def normalize_status(value):

    value = clean_string(value)

    if value is None:
        return "Completed"

    value = value.lower()

    if value == "completed":
        return "Completed"

    if value == "pending":
        return "Partially Vaccinated"

    if value == "booster due":
        return "Overdue"

    return "Completed"


# ============================================================
# LOAD SOURCE DATA
# ============================================================

def load_source_data():

    print()
    print("=" * 70)
    print("LOADING VACCINATION SOURCE DATA")
    print("=" * 70)

    if not os.path.exists(SOURCE_FILE):

        print()
        print("ERROR: Source file not found:")
        print(SOURCE_FILE)

        sys.exit(1)

    df = pd.read_csv(SOURCE_FILE)

    print()
    print(f"Source file: {SOURCE_FILE}")
    print(f"Source rows: {len(df):,}")

    # --------------------------------------------------------
    # ACTUAL SOURCE COLUMNS
    # --------------------------------------------------------

    required_columns = [
        "Vaccination_ID",
        "Patient_ID",
        "Vaccine_Name",
        "Disease_Prevented",
        "Dose_Number",
        "Vaccination_Date",
        "Vaccination_Status",
        "Administered_By"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:

        print()
        print("ERROR: Missing source columns:")

        for column in missing_columns:
            print(f"  - {column}")

        print()
        print("Actual columns:")

        for column in df.columns:
            print(f"  - {column}")

        sys.exit(1)

    print()
    print("Source columns verified successfully.")

    return df


# ============================================================
# LOAD VALID PATIENT IDs
# ============================================================

def load_valid_patients(conn):

    print()
    print("=" * 70)
    print("LOADING VALID PATIENT IDs")
    print("=" * 70)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT Patient_ID
        FROM patients
    """)

    valid_patients = {
        str(row[0])
        for row in cursor.fetchall()
    }

    cursor.close()

    print(f"DB patients: {len(valid_patients):,}")

    return valid_patients


# ============================================================
# PREPARE MAPPING RECORDS
# ============================================================

def prepare_records(df, valid_patients):

    print()
    print("=" * 70)
    print("PREPARING PATIENT VACCINATION MAPPINGS")
    print("=" * 70)

    records = []

    invalid_patient = 0
    invalid_date = 0
    invalid_vaccine = 0
    invalid_dose = 0

    status_counts = {}
    vaccine_counts = {}
    administered_by_counts = {}

    for _, row in df.iterrows():

        # ----------------------------------------------------
        # PATIENT
        # ----------------------------------------------------

        patient_id = clean_string(
            row["Patient_ID"]
        )

        if patient_id not in valid_patients:

            invalid_patient += 1
            continue

        # ----------------------------------------------------
        # VACCINE
        # ----------------------------------------------------

        vaccine_name = clean_string(
            row["Vaccine_Name"]
        )

        if vaccine_name is None:

            invalid_vaccine += 1
            continue

        # ----------------------------------------------------
        # TARGET DISEASE
        # ----------------------------------------------------

        target_disease = clean_string(
            row["Disease_Prevented"]
        )

        if target_disease is None:

            target_disease = "Unspecified"

        # ----------------------------------------------------
        # DATE
        # ----------------------------------------------------

        administration_date = clean_date(
            row["Vaccination_Date"]
        )

        if administration_date is None:

            invalid_date += 1
            continue

        # ----------------------------------------------------
        # DOSE
        # ----------------------------------------------------

        dose_number = row["Dose_Number"]

        if pd.isna(dose_number):

            dose_number = 1

        else:

            try:
                dose_number = int(dose_number)

            except Exception:

                invalid_dose += 1
                continue

        if dose_number < 1:

            invalid_dose += 1
            continue

        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        vaccination_status = normalize_status(
            row["Vaccination_Status"]
        )

        # ----------------------------------------------------
        # ADMINISTERED BY
        #
        # Source value is:
        # "Hospital Vaccination Center"
        #
        # It is NOT a Doctor_ID.
        # Therefore Administered_By_Doctor_ID = NULL.
        # ----------------------------------------------------

        administered_by = clean_string(
            row["Administered_By"]
        )

        # ----------------------------------------------------
        # TARGET DEFAULTS
        #
        # These fields do not exist in source data.
        # We use NULL/default values rather than inventing
        # clinical information.
        # ----------------------------------------------------

        vaccine_code = None
        manufacturer = None
        batch_number = None
        lot_number = None
        expiration_date = None

        total_doses_required = dose_number

        route = "Other"
        administration_site = "Other"

        dosage_administered = None

        next_due_date = None

        exemption_reason = None

        adverse_reaction_observed = 0
        adverse_reaction_severity = "None"
        adverse_reaction_description = None

        # ----------------------------------------------------
        # SOURCE
        # ----------------------------------------------------

        data_source = "Synthetic"

        # ----------------------------------------------------
        # CREATE TARGET RECORD
        # ----------------------------------------------------

        record = (
            str(uuid.uuid4()),          # Vaccination_Map_ID
            patient_id,                 # Patient_ID
            None,                       # Administered_By_Doctor_ID
            vaccine_name,               # Vaccine_Name
            vaccine_code,               # Vaccine_Code
            target_disease,             # Target_Disease
            manufacturer,               # Manufacturer
            batch_number,               # Batch_Number
            lot_number,                 # Lot_Number
            expiration_date,            # Expiration_Date
            dose_number,                # Dose_Number
            total_doses_required,       # Total_Doses_Required
            administration_date,        # Administration_Date
            route,                      # Route_Of_Administration
            administration_site,        # Administration_Site
            dosage_administered,        # Dosage_Administered
            vaccination_status,         # Vaccination_Status
            next_due_date,              # Next_Due_Date
            exemption_reason,           # Exemption_Reason
            adverse_reaction_observed,  # Adverse_Reaction_Observed
            adverse_reaction_severity,  # Adverse_Reaction_Severity
            adverse_reaction_description,  # Adverse_Reaction_Description
            1,                          # Is_Active
            0,                          # Is_Deleted
            1,                          # Record_Version
            data_source,                # Data_Source
            administered_by,            # Created_By
            administered_by             # Updated_By
        )

        records.append(record)

        # ----------------------------------------------------
        # STATISTICS
        # ----------------------------------------------------

        status_counts[vaccination_status] = (
            status_counts.get(vaccination_status, 0) + 1
        )

        vaccine_counts[vaccine_name] = (
            vaccine_counts.get(vaccine_name, 0) + 1
        )

        if administered_by:

            administered_by_counts[administered_by] = (
                administered_by_counts.get(
                    administered_by,
                    0
                ) + 1
            )

    # ========================================================
    # SUMMARY
    # ========================================================

    print()
    print(f"Valid records prepared : {len(records):,}")
    print(f"Invalid Patient_ID     : {invalid_patient:,}")
    print(f"Invalid Vaccine_Name   : {invalid_vaccine:,}")
    print(f"Invalid Date           : {invalid_date:,}")
    print(f"Invalid Dose_Number    : {invalid_dose:,}")

    print()
    print("VACCINATION STATUS")

    for status in sorted(status_counts):

        print(
            f"{status:<25}: "
            f"{status_counts[status]:,}"
        )

    print()
    print("UNIQUE VACCINES")

    print(
        f"Unique vaccine names   : "
        f"{len(vaccine_counts):,}"
    )

    print()
    print("ADMINISTERED BY")

    for source, count in sorted(
        administered_by_counts.items(),
        key=lambda x: x[1],
        reverse=True
    ):

        print(
            f"{source:<35}: "
            f"{count:,}"
        )

    return records


# ============================================================
# INSERT RECORDS
# ============================================================

def insert_records(conn, records):

    print()
    print("=" * 70)
    print("INSERTING PATIENT VACCINATION MAPPINGS")
    print("=" * 70)

    if not records:

        print("No records to insert.")
        return 0

    cursor = conn.cursor()

    insert_sql = """
        INSERT INTO patient_vaccination_map (
            Vaccination_Map_ID,
            Patient_ID,
            Administered_By_Doctor_ID,
            Vaccine_Name,
            Vaccine_Code,
            Target_Disease,
            Manufacturer,
            Batch_Number,
            Lot_Number,
            Expiration_Date,
            Dose_Number,
            Total_Doses_Required,
            Administration_Date,
            Route_Of_Administration,
            Administration_Site,
            Dosage_Administered,
            Vaccination_Status,
            Next_Due_Date,
            Exemption_Reason,
            Adverse_Reaction_Observed,
            Adverse_Reaction_Severity,
            Adverse_Reaction_Description,
            Is_Active,
            Is_Deleted,
            Record_Version,
            Data_Source,
            Created_By,
            Updated_By
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s
        )
    """

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

            inserted += len(batch)

            print(
                f"   Inserted: "
                f"{inserted:,}/{len(records):,}"
            )

        conn.commit()

        print()
        print(f"Inserted records: {inserted:,}")

        cursor.close()

        return inserted

    except Exception as e:

        conn.rollback()

        print()
        print("ERROR during insertion:")
        print(e)

        print()
        print("Transaction rolled back.")

        cursor.close()

        raise


# ============================================================
# VALIDATION
# ============================================================

def validate(conn, expected_records):

    print()
    print("=" * 70)
    print("STEP 58 VALIDATION")
    print("=" * 70)

    cursor = conn.cursor()

    # --------------------------------------------------------
    # TOTAL RECORDS
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM patient_vaccination_map
    """)

    actual_records = cursor.fetchone()[0]

    print(
        f"Expected records : "
        f"{expected_records:,}"
    )

    print(
        f"Actual records   : "
        f"{actual_records:,}"
    )

    # --------------------------------------------------------
    # UNIQUE PATIENTS
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(DISTINCT Patient_ID)
        FROM patient_vaccination_map
    """)

    unique_patients = cursor.fetchone()[0]

    print(
        f"Unique patients  : "
        f"{unique_patients:,}"
    )

    # --------------------------------------------------------
    # UNIQUE VACCINES
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(DISTINCT Vaccine_Name)
        FROM patient_vaccination_map
    """)

    unique_vaccines = cursor.fetchone()[0]

    print(
        f"Unique vaccines  : "
        f"{unique_vaccines:,}"
    )

    # --------------------------------------------------------
    # NULL CHECKS
    # --------------------------------------------------------

    print()
    print("NULL CHECKS")

    required_columns = [
        "Patient_ID",
        "Vaccine_Name",
        "Target_Disease",
        "Dose_Number",
        "Total_Doses_Required",
        "Administration_Date",
        "Route_Of_Administration",
        "Administration_Site",
        "Vaccination_Status",
        "Data_Source"
    ]

    null_counts = {}

    for column in required_columns:

        cursor.execute(
            f"""
            SELECT COUNT(*)
            FROM patient_vaccination_map
            WHERE {column} IS NULL
            """
        )

        count = cursor.fetchone()[0]

        null_counts[column] = count

        print(
            f"{column:<30}: "
            f"{count:,}"
        )

    # --------------------------------------------------------
    # ORPHAN PATIENTS
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM patient_vaccination_map pvm
        LEFT JOIN patients p
            ON pvm.Patient_ID = p.Patient_ID
        WHERE p.Patient_ID IS NULL
    """)

    orphan_patients = cursor.fetchone()[0]

    # --------------------------------------------------------
    # ORPHAN DOCTORS
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM patient_vaccination_map pvm
        LEFT JOIN doctors d
            ON pvm.Administered_By_Doctor_ID = d.Doctor_ID
        WHERE pvm.Administered_By_Doctor_ID IS NOT NULL
          AND d.Doctor_ID IS NULL
    """)

    orphan_doctors = cursor.fetchone()[0]

    print()
    print("ORPHAN CHECKS")

    print(
        f"Orphan patients : "
        f"{orphan_patients:,}"
    )

    print(
        f"Orphan doctors   : "
        f"{orphan_doctors:,}"
    )

    # --------------------------------------------------------
    # INVALID DOSES
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM patient_vaccination_map
        WHERE Dose_Number < 1
           OR Total_Doses_Required < 1
           OR Dose_Number > Total_Doses_Required
    """)

    invalid_doses = cursor.fetchone()[0]

    # --------------------------------------------------------
    # INVALID DATES
    # --------------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM patient_vaccination_map
        WHERE Next_Due_Date IS NOT NULL
          AND Next_Due_Date < Administration_Date
    """)

    invalid_dates = cursor.fetchone()[0]

    print()
    print("VALUE VALIDATION")

    print(
        f"Invalid dates : "
        f"{invalid_dates:,}"
    )

    print(
        f"Invalid doses : "
        f"{invalid_doses:,}"
    )

    # --------------------------------------------------------
    # VACCINATION STATUS
    # --------------------------------------------------------

    print()
    print("VACCINATION STATUS")

    cursor.execute("""
        SELECT
            Vaccination_Status,
            COUNT(*)
        FROM patient_vaccination_map
        GROUP BY Vaccination_Status
        ORDER BY Vaccination_Status
    """)

    for status, count in cursor.fetchall():

        print(
            f"{status:<25}: "
            f"{count:,}"
        )

    # --------------------------------------------------------
    # DATA SOURCE
    # --------------------------------------------------------

    print()
    print("DATA SOURCE")

    cursor.execute("""
        SELECT
            Data_Source,
            COUNT(*)
        FROM patient_vaccination_map
        GROUP BY Data_Source
        ORDER BY Data_Source
    """)

    for source, count in cursor.fetchall():

        print(
            f"{source:<25}: "
            f"{count:,}"
        )

    # --------------------------------------------------------
    # ADMINISTERED BY DOCTOR
    # --------------------------------------------------------

    print()
    print("ADMINISTERED BY DOCTOR")

    cursor.execute("""
        SELECT
            COUNT(*)
        FROM patient_vaccination_map
        WHERE Administered_By_Doctor_ID IS NOT NULL
    """)

    doctor_assigned = cursor.fetchone()[0]

    cursor.execute("""
        SELECT
            COUNT(*)
        FROM patient_vaccination_map
        WHERE Administered_By_Doctor_ID IS NULL
    """)

    doctor_not_assigned = cursor.fetchone()[0]

    print(
        f"Doctor ID assigned : "
        f"{doctor_assigned:,}"
    )

    print(
        f"Doctor ID NULL     : "
        f"{doctor_not_assigned:,}"
    )

    # --------------------------------------------------------
    # FINAL STATUS
    # --------------------------------------------------------

    passed = True

    if actual_records != expected_records:
        passed = False

    if orphan_patients != 0:
        passed = False

    if orphan_doctors != 0:
        passed = False

    if invalid_dates != 0:
        passed = False

    if invalid_doses != 0:
        passed = False

    for count in null_counts.values():

        if count != 0:
            passed = False

    print()
    print("=" * 70)

    if passed:

        print("FINAL STATUS: PASSED")

    else:

        print("FINAL STATUS: FAILED")

    print("=" * 70)

    cursor.close()

    if not passed:
        sys.exit(1)


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("STEP 58 - PATIENT VACCINATION MAPPING")
    print("=" * 70)

    conn = get_connection()

    try:

        # ----------------------------------------------------
        # CHECK EXISTING DATA
        # ----------------------------------------------------

        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM patient_vaccination_map
        """)

        existing_records = cursor.fetchone()[0]

        cursor.close()

        print()
        print(
            f"Existing mapping records: "
            f"{existing_records:,}"
        )

        if existing_records > 0:

            print()
            print(
                "ERROR: patient_vaccination_map "
                "already contains records."
            )

            print(
                "No records were inserted."
            )

            return

        # ----------------------------------------------------
        # LOAD SOURCE
        # ----------------------------------------------------

        df = load_source_data()

        # ----------------------------------------------------
        # VALID PATIENTS
        # ----------------------------------------------------

        valid_patients = load_valid_patients(
            conn
        )

        # ----------------------------------------------------
        # PREPARE
        # ----------------------------------------------------

        records = prepare_records(
            df,
            valid_patients
        )

        if not records:

            print()
            print(
                "ERROR: No valid records prepared."
            )

            return

        # ----------------------------------------------------
        # INSERT
        # ----------------------------------------------------

        inserted = insert_records(
            conn,
            records
        )

        # ----------------------------------------------------
        # VALIDATE
        # ----------------------------------------------------

        validate(
            conn,
            inserted
        )

    except Exception as e:

        print()
        print("=" * 70)
        print("STEP 58 FAILED")
        print("=" * 70)

        print(e)

        try:
            conn.rollback()
        except Exception:
            pass

    finally:

        conn.close()

        print()
        print("Database connection closed.")


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()