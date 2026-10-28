import csv
import os
import sys
import uuid
import re
from datetime import datetime
from decimal import Decimal, InvalidOperation

import mysql.connector
from mysql.connector import Error


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)

CSV_FILE = os.path.join(
    BASE_DIR,
    "datasets",
    "synthetic",
    "lab_results.csv"
)

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "database": "healthcare_ai_db",
}

# IMPORTANT:
# Load ONLY into the new replacement table.
TARGET_TABLE = "lab_results_new"

INSERT_BATCH_SIZE = 5000


# ============================================================
# PASSWORD
# ============================================================

def get_password():
    password = os.environ.get("MYSQL_PASSWORD")

    if password:
        return password

    import getpass
    return getpass.getpass("MySQL password: ")


# ============================================================
# PARSING HELPERS
# ============================================================

def parse_datetime(value):

    if not value:
        return None

    value = str(value).strip()

    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
        "%d-%m-%Y %H:%M:%S",
        "%d-%m-%Y",
    ]

    for fmt in formats:

        try:
            return datetime.strptime(value, fmt)

        except ValueError:
            continue

    return None


def parse_numeric(value):

    if value is None:
        return None

    value = str(value).strip()

    if not value:
        return None

    try:
        return Decimal(value)

    except (InvalidOperation, ValueError):
        return None


def parse_reference_range(reference_range):

    if not reference_range:
        return None, None

    text = str(reference_range).strip()

    match = re.search(
        r"(-?\d+(?:\.\d+)?)\s*[-–]\s*(-?\d+(?:\.\d+)?)",
        text
    )

    if not match:
        return None, None

    try:

        minimum = Decimal(match.group(1))
        maximum = Decimal(match.group(2))

        return minimum, maximum

    except InvalidOperation:

        return None, None


def clean_uuid(value):

    if not value:
        return None

    value = str(value).strip()

    try:

        return str(uuid.UUID(value))

    except ValueError:

        return None


# ============================================================
# RESULT CATEGORY
# ============================================================

def determine_result_category(test_name):

    name = str(test_name).lower()

    hematology = [
        "cbc",
        "hemoglobin",
        "haemoglobin",
        "hematocrit",
        "haematocrit",
        "platelet",
        "rbc",
        "wbc",
        "white blood",
        "red blood",
        "neutrophil",
        "lymphocyte",
        "monocyte",
        "eosinophil",
        "basophil",
        "esr",
    ]

    biochemistry = [
        "glucose",
        "sugar",
        "creatinine",
        "urea",
        "bun",
        "bilirubin",
        "albumin",
        "protein",
        "cholesterol",
        "triglyceride",
        "hdl",
        "ldl",
        "sodium",
        "potassium",
        "calcium",
        "chloride",
        "ast",
        "alt",
        "sgot",
        "sgpt",
        "alp",
        "uric acid",
    ]

    microbiology = [
        "culture",
        "microbiology",
        "bacteria",
        "fungal",
        "fungus",
        "urine culture",
        "blood culture",
    ]

    pathology = [
        "biopsy",
        "histopathology",
        "cytology",
        "pathology",
    ]

    imaging = [
        "x-ray",
        "xray",
        "mri",
        "ct scan",
        "computed tomography",
        "ultrasound",
        "sonography",
        "echocardiogram",
        "ecg",
        "ekg",
        "imaging",
    ]

    for item in hematology:

        if item in name:
            return "Hematology"

    for item in biochemistry:

        if item in name:
            return "Biochemistry"

    for item in microbiology:

        if item in name:
            return "Microbiology"

    for item in pathology:

        if item in name:
            return "Pathology"

    for item in imaging:

        if item in name:
            return "Imaging"

    return "Other"


# ============================================================
# RESULT STATUS
# ============================================================

def calculate_abnormal_flag(status):

    return (
        1
        if str(status).strip().lower() == "abnormal"
        else 0
    )


def calculate_severity(status):

    status = str(status).strip().lower()

    if status == "critical":
        return 100

    if status == "abnormal":
        return 50

    return 0


# ============================================================
# DATABASE CONNECTION
# ============================================================

def connect_database():

    password = get_password()

    config = DB_CONFIG.copy()
    config["password"] = password

    connection = mysql.connector.connect(**config)

    if not connection.is_connected():

        raise RuntimeError(
            "Could not connect to MySQL."
        )

    return connection


# ============================================================
# LOAD REFERENCE DATA
# ============================================================

def load_reference_data(connection):

    cursor = connection.cursor()

    print("\nLoading reference data...")

    # --------------------------------------------------------
    # PATIENTS
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT Patient_ID
        FROM patients
        """
    )

    valid_patients = {
        str(row[0])
        for row in cursor.fetchall()
    }

    print(
        f"  Patients loaded: "
        f"{len(valid_patients):,}"
    )

    # --------------------------------------------------------
    # ADMISSIONS
    #
    # IMPORTANT:
    # admissions uses Admitting_Doctor_ID,
    # NOT Doctor_ID.
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT
            Admission_ID,
            Patient_ID,
            Admitting_Doctor_ID
        FROM admissions
        """
    )

    admission_map = {}

    for (
        admission_id,
        patient_id,
        admitting_doctor_id
    ) in cursor.fetchall():

        admission_map[str(admission_id)] = {
            "Patient_ID": (
                str(patient_id)
                if patient_id
                else None
            ),
            "Doctor_ID": (
                str(admitting_doctor_id)
                if admitting_doctor_id
                else None
            ),
        }

    print(
        f"  Admissions loaded: "
        f"{len(admission_map):,}"
    )

    # --------------------------------------------------------
    # DOCTORS
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT Doctor_ID
        FROM doctors
        """
    )

    valid_doctors = {
        str(row[0])
        for row in cursor.fetchall()
    }

    print(
        f"  Doctors loaded: "
        f"{len(valid_doctors):,}"
    )

    # --------------------------------------------------------
    # LAB TESTS
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT
            Lab_Test_ID,
            Test_Name
        FROM lab_tests
        """
    )

    lab_test_map = {}

    for lab_test_id, test_name in cursor.fetchall():

        if test_name is None:
            continue

        key = str(test_name).strip().lower()

        if key not in lab_test_map:

            lab_test_map[key] = str(
                lab_test_id
            )

    print(
        f"  Lab tests loaded: "
        f"{len(lab_test_map):,}"
    )

    cursor.close()

    return (
        valid_patients,
        admission_map,
        valid_doctors,
        lab_test_map,
    )


# ============================================================
# INSERT BATCH
# ============================================================

def insert_batch(connection, rows):

    if not rows:
        return

    sql = f"""
        INSERT INTO {TARGET_TABLE} (
            Lab_Result_ID,
            Patient_ID,
            Lab_Test_ID,
            Doctor_ID,
            Admission_ID,
            Test_Date,
            Sample_Type,
            Result_Category,
            Result_Value,
            Numeric_Result_Value,
            Unit,
            Reference_Min_Value,
            Reference_Max_Value,
            Result_Status,
            Abnormal_Flag,
            Severity_Score,
            Verification_Status,
            AI_Analyzed,
            AI_Risk_Category,
            Used_For_Model_Training,
            Data_Source,
            Is_Active,
            Is_Deleted,
            Record_Version
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s
        )
    """

    cursor = connection.cursor()

    cursor.executemany(
        sql,
        rows
    )

    connection.commit()

    cursor.close()


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("63B - LOAD CORRECTED LAB RESULTS")
    print("=" * 70)

    print("\nCSV file:")
    print(CSV_FILE)

    print("\nTarget table:")
    print(TARGET_TABLE)

    # --------------------------------------------------------
    # CHECK CSV
    # --------------------------------------------------------

    if not os.path.exists(CSV_FILE):

        print("\nERROR: CSV file does not exist.")

        sys.exit(1)

    # --------------------------------------------------------
    # CONNECT
    # --------------------------------------------------------

    print("\nConnecting to MySQL...")

    connection = None

    try:

        connection = connect_database()

        print("MySQL connection successful.")

        # ----------------------------------------------------
        # TARGET TABLE CHECK
        # ----------------------------------------------------

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_schema = %s
              AND table_name = %s
            """,
            (
                DB_CONFIG["database"],
                TARGET_TABLE,
            )
        )

        table_exists = cursor.fetchone()[0]

        cursor.close()

        if table_exists != 1:

            raise RuntimeError(
                f"Target table '{TARGET_TABLE}' "
                f"does not exist."
            )

        # ----------------------------------------------------
        # TARGET MUST BE EMPTY
        # ----------------------------------------------------

        cursor = connection.cursor()

        cursor.execute(
            f"""
            SELECT COUNT(*)
            FROM {TARGET_TABLE}
            """
        )

        existing_rows = cursor.fetchone()[0]

        cursor.close()

        print(
            f"\nExisting rows in "
            f"{TARGET_TABLE}: "
            f"{existing_rows:,}"
        )

        if existing_rows != 0:

            raise RuntimeError(
                f"{TARGET_TABLE} is not empty. "
                f"Loader stopped for safety."
            )

        # ----------------------------------------------------
        # REFERENCE DATA
        # ----------------------------------------------------

        (
            valid_patients,
            admission_map,
            valid_doctors,
            lab_test_map,
        ) = load_reference_data(
            connection
        )

        # ----------------------------------------------------
        # STATISTICS
        # ----------------------------------------------------

        total_rows = 0
        inserted_rows = 0

        invalid_patient_rows = 0
        invalid_admission_rows = 0
        invalid_doctor_rows = 0
        invalid_lab_test_rows = 0
        invalid_date_rows = 0
        invalid_status_rows = 0

        normal_rows = 0
        abnormal_rows = 0
        critical_rows = 0
        pending_rows = 0

        batch = []

        # ----------------------------------------------------
        # OPEN CSV
        # ----------------------------------------------------

        print("\nOpening corrected CSV...")

        with open(
            CSV_FILE,
            "r",
            encoding="utf-8-sig",
            newline=""
        ) as csv_file:

            reader = csv.DictReader(csv_file)

            expected_columns = [
                "Lab_Result_ID",
                "Patient_ID",
                "Admission_ID",
                "Doctor_ID",
                "Test_Name",
                "Result_Value",
                "Unit",
                "Reference_Range",
                "Result_Status",
                "Test_Date",
                "Performed_By",
            ]

            missing_columns = [
                column
                for column in expected_columns
                if column not in reader.fieldnames
            ]

            if missing_columns:

                raise RuntimeError(
                    "CSV is missing columns: "
                    + ", ".join(missing_columns)
                )

            print("\nCSV columns verified.")

            # ------------------------------------------------
            # PROCESS ROWS
            # ------------------------------------------------

            for csv_row in reader:

                total_rows += 1

                lab_result_id = clean_uuid(
                    csv_row.get("Lab_Result_ID")
                )

                patient_id = clean_uuid(
                    csv_row.get("Patient_ID")
                )

                admission_id = clean_uuid(
                    csv_row.get("Admission_ID")
                )

                doctor_id = clean_uuid(
                    csv_row.get("Doctor_ID")
                )

                test_name = (
                    csv_row.get("Test_Name")
                    or ""
                ).strip()

                result_value = (
                    csv_row.get("Result_Value")
                    or ""
                ).strip()

                unit = (
                    csv_row.get("Unit")
                    or ""
                ).strip()

                reference_range = (
                    csv_row.get("Reference_Range")
                    or ""
                ).strip()

                result_status = (
                    csv_row.get("Result_Status")
                    or "Pending"
                ).strip()

                test_date = parse_datetime(
                    csv_row.get("Test_Date")
                )

                # ------------------------------------------------
                # PATIENT
                # ------------------------------------------------

                if (
                    not patient_id
                    or patient_id not in valid_patients
                ):

                    invalid_patient_rows += 1
                    continue

                # ------------------------------------------------
                # ADMISSION
                # ------------------------------------------------

                if (
                    not admission_id
                    or admission_id not in admission_map
                ):

                    invalid_admission_rows += 1
                    continue

                admission_record = admission_map[
                    admission_id
                ]

                # ------------------------------------------------
                # PATIENT ↔ ADMISSION
                # ------------------------------------------------

                if (
                    admission_record["Patient_ID"]
                    != patient_id
                ):

                    invalid_patient_rows += 1
                    continue

                # ------------------------------------------------
                # DOCTOR
                # ------------------------------------------------

                if (
                    not doctor_id
                    or doctor_id not in valid_doctors
                ):

                    invalid_doctor_rows += 1
                    continue

                # ------------------------------------------------
                # DOCTOR ↔ ADMISSION
                #
                # CSV Doctor_ID must equal
                # admissions.Admitting_Doctor_ID
                # ------------------------------------------------

                if (
                    admission_record["Doctor_ID"]
                    != doctor_id
                ):

                    invalid_doctor_rows += 1
                    continue

                # ------------------------------------------------
                # LAB TEST
                # ------------------------------------------------

                lab_test_id = lab_test_map.get(
                    test_name.lower()
                )

                if not lab_test_id:

                    invalid_lab_test_rows += 1
                    continue

                # ------------------------------------------------
                # DATE
                # ------------------------------------------------

                if not test_date:

                    invalid_date_rows += 1
                    continue

                # ------------------------------------------------
                # STATUS
                # ------------------------------------------------

                allowed_statuses = {
                    "Normal",
                    "Abnormal",
                    "Critical",
                    "Pending",
                }

                if result_status not in allowed_statuses:

                    invalid_status_rows += 1
                    continue

                # ------------------------------------------------
                # VALUES
                # ------------------------------------------------

                reference_min, reference_max = (
                    parse_reference_range(
                        reference_range
                    )
                )

                numeric_result = parse_numeric(
                    result_value
                )

                result_category = (
                    determine_result_category(
                        test_name
                    )
                )

                abnormal_flag = (
                    calculate_abnormal_flag(
                        result_status
                    )
                )

                severity_score = (
                    calculate_severity(
                        result_status
                    )
                )

                # ------------------------------------------------
                # STATUS STATISTICS
                # ------------------------------------------------

                if result_status == "Normal":

                    normal_rows += 1

                elif result_status == "Abnormal":

                    abnormal_rows += 1

                elif result_status == "Critical":

                    critical_rows += 1

                elif result_status == "Pending":

                    pending_rows += 1

                # ------------------------------------------------
                # DATABASE ROW
                # ------------------------------------------------

                row = (
                    lab_result_id,
                    patient_id,
                    lab_test_id,
                    doctor_id,
                    admission_id,
                    test_date,
                    None,
                    result_category,
                    result_value or None,
                    numeric_result,
                    unit or None,
                    reference_min,
                    reference_max,
                    result_status,
                    abnormal_flag,
                    severity_score,
                    "Pending",
                    0,
                    "Low",
                    0,
                    "Synthetic",
                    1,
                    0,
                    1,
                )

                batch.append(row)

                # ------------------------------------------------
                # INSERT BATCH
                # ------------------------------------------------

                if len(batch) >= INSERT_BATCH_SIZE:

                    insert_batch(
                        connection,
                        batch
                    )

                    inserted_rows += len(batch)

                    batch.clear()

                    if inserted_rows % 50000 == 0:

                        print(
                            f"Inserted: "
                            f"{inserted_rows:,}"
                        )

        # --------------------------------------------------------
        # FINAL BATCH
        # --------------------------------------------------------

        if batch:

            insert_batch(
                connection,
                batch
            )

            inserted_rows += len(batch)

            batch.clear()

        # --------------------------------------------------------
        # FINAL COUNT
        # --------------------------------------------------------

        cursor = connection.cursor()

        cursor.execute(
            f"""
            SELECT COUNT(*)
            FROM {TARGET_TABLE}
            """
        )

        final_count = cursor.fetchone()[0]

        cursor.close()

        # --------------------------------------------------------
        # SUMMARY
        # --------------------------------------------------------

        print("\n" + "=" * 70)
        print("LOAD COMPLETED")
        print("=" * 70)

        print(
            f"\nCSV rows processed       : "
            f"{total_rows:,}"
        )

        print(
            f"Rows inserted            : "
            f"{inserted_rows:,}"
        )

        print(
            f"Rows in database         : "
            f"{final_count:,}"
        )

        print("\nValidation statistics:")

        print(
            f"Invalid Patient rows     : "
            f"{invalid_patient_rows:,}"
        )

        print(
            f"Invalid Admission rows   : "
            f"{invalid_admission_rows:,}"
        )

        print(
            f"Invalid Doctor rows      : "
            f"{invalid_doctor_rows:,}"
        )

        print(
            f"Invalid Lab Test rows    : "
            f"{invalid_lab_test_rows:,}"
        )

        print(
            f"Invalid Date rows        : "
            f"{invalid_date_rows:,}"
        )

        print(
            f"Invalid Status rows      : "
            f"{invalid_status_rows:,}"
        )

        print("\nResult status:")

        print(
            f"Normal                   : "
            f"{normal_rows:,}"
        )

        print(
            f"Abnormal                 : "
            f"{abnormal_rows:,}"
        )

        print(
            f"Critical                 : "
            f"{critical_rows:,}"
        )

        print(
            f"Pending                  : "
            f"{pending_rows:,}"
        )

        if (
            total_rows == 3_000_000
            and inserted_rows == 3_000_000
            and final_count == 3_000_000
            and invalid_patient_rows == 0
            and invalid_admission_rows == 0
            and invalid_doctor_rows == 0
            and invalid_lab_test_rows == 0
            and invalid_date_rows == 0
            and invalid_status_rows == 0
        ):

            print(
                "\nSUCCESS: "
                "All 3,000,000 corrected rows loaded."
            )

        else:

            print(
                "\nWARNING: "
                "Validation did not produce "
                "the expected perfect result."
            )

    except Error as e:

        print("\nMYSQL ERROR:")
        print(e)

        sys.exit(1)

    except Exception as e:

        print("\nERROR:")
        print(e)

        sys.exit(1)

    finally:

        if connection is not None:

            try:

                if connection.is_connected():

                    connection.close()

                    print(
                        "\nMySQL connection closed."
                    )

            except Exception:
                pass


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()