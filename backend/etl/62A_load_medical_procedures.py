import csv
import os
import mysql.connector
from datetime import datetime
from decimal import Decimal, InvalidOperation

CSV_FILE = r"datasets\synthetic\medical_procedures.csv"

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": os.environ.get("MYSQL_PASSWORD"),
    "database": "healthcare_ai_db"
}

BATCH_SIZE = 5000


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def parse_date(value):
    value = value.strip()

    formats = [
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S.%f"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass

    return None


def main():

    print("=" * 70)
    print("STEP 62A - LOAD MEDICAL PROCEDURES")
    print("=" * 70)

    if not DB_CONFIG["password"]:
        print("ERROR: MYSQL_PASSWORD is not set.")
        print('Run: $env:MYSQL_PASSWORD = Read-Host "Enter MySQL root password"')
        return

    if not os.path.exists(CSV_FILE):
        print(f"ERROR: CSV not found: {CSV_FILE}")
        return

    conn = get_connection()
    cursor = conn.cursor()

    file_size_mb = os.path.getsize(CSV_FILE) / (1024 * 1024)

    print(f"CSV file: {CSV_FILE}")
    print(f"CSV size: {file_size_mb:.2f} MB")

    # ------------------------------------------------------------
    # LOAD VALID REFERENCE IDS
    # ------------------------------------------------------------

    cursor.execute("SELECT Patient_ID FROM patients")
    valid_patients = {row[0] for row in cursor.fetchall()}

    cursor.execute("SELECT Doctor_ID FROM doctors")
    valid_doctors = {row[0] for row in cursor.fetchall()}

    cursor.execute("SELECT Department_ID FROM departments")
    valid_departments = {row[0] for row in cursor.fetchall()}

    cursor.execute("""
        SELECT Admission_ID, Patient_ID
        FROM admissions
    """)

    admissions = {
        row[0]: row[1]
        for row in cursor.fetchall()
    }

    # ------------------------------------------------------------
    # CREATE DEPARTMENT → DOCTOR LOOKUP
    # ------------------------------------------------------------

    cursor.execute("""
        SELECT Doctor_ID, Department_ID
        FROM doctors
        ORDER BY Doctor_ID
    """)

    department_doctors = {}

    for doctor_id, department_id in cursor.fetchall():

        if department_id not in department_doctors:
            department_doctors[department_id] = []

        department_doctors[department_id].append(doctor_id)

    print(f"DB patients:                    {len(valid_patients):,}")
    print(f"DB doctors:                     {len(valid_doctors):,}")
    print(f"DB departments:                 {len(valid_departments):,}")
    print(f"DB admissions:                   {len(admissions):,}")

    # ------------------------------------------------------------
    # EXISTING RECORDS
    # ------------------------------------------------------------

    cursor.execute("SELECT COUNT(*) FROM medical_procedures")
    existing_count = cursor.fetchone()[0]

    print(f"Existing medical_procedures:     {existing_count:,}")

    if existing_count > 0:

        print("\nClearing existing medical_procedures records...")

        cursor.execute("DELETE FROM medical_procedures")
        conn.commit()

        print("Existing records cleared.")

    # ------------------------------------------------------------
    # INSERT SQL
    # ------------------------------------------------------------

    insert_sql = """
        INSERT INTO medical_procedures (
            Procedure_ID,
            Patient_ID,
            Doctor_ID,
            Admission_ID,
            Diagnosis_ID,
            Department_ID,
            Procedure_Number,
            Procedure_Code,
            Procedure_Name,
            Procedure_Category,
            Procedure_Date,
            Duration_Minutes,
            Procedure_Status,
            Priority,
            Operation_Theater,
            Anaesthetist,
            Assistant_Surgeon,
            Anaesthesia_Type,
            Procedure_Cost,
            Complications,
            Procedure_Outcome,
            Follow_Up_Required,
            Notes,
            AI_Risk_Level,
            AI_Recommendation,
            AI_Confidence,
            Data_Source,
            Is_Active,
            Is_Deleted,
            Record_Version,
            Created_By,
            Updated_By
        )
        VALUES (
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s,
            %s, %s
        )
    """

    # ------------------------------------------------------------
    # COUNTERS
    # ------------------------------------------------------------

    total_rows = 0
    valid_rows = 0

    invalid_patient = 0
    invalid_doctor = 0
    invalid_department = 0
    invalid_date = 0
    invalid_cost = 0

    admission_valid = 0
    admission_patient_match = 0
    admission_nullified = 0

    source_doctor_used = 0
    fallback_doctor_used = 0

    status_counts = {}
    category_counts = {}
    anesthesia_counts = {}

    batch = []

    print("\nReading and validating CSV...")

    # ------------------------------------------------------------
    # READ CSV
    # ------------------------------------------------------------

    with open(
        CSV_FILE,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            total_rows += 1

            source_procedure_id = row["Procedure_ID"].strip()
            patient_id = row["Patient_ID"].strip()
            admission_id = row["Admission_ID"].strip()
            source_doctor_id = row["Doctor_ID"].strip()
            department_id = row["Department_ID"].strip()

            # ----------------------------------------------------
            # PATIENT
            # ----------------------------------------------------

            if patient_id not in valid_patients:
                invalid_patient += 1
                continue

            # ----------------------------------------------------
            # DEPARTMENT
            # ----------------------------------------------------

            if department_id not in valid_departments:
                invalid_department += 1
                continue

            # ----------------------------------------------------
            # DOCTOR
            # ----------------------------------------------------

            if source_doctor_id in valid_doctors:

                doctor_id = source_doctor_id
                source_doctor_used += 1

            else:

                invalid_doctor += 1

                # Fallback to a real doctor from the procedure's
                # department rather than creating a fake ID.

                doctors_in_department = department_doctors.get(
                    department_id,
                    []
                )

                if not doctors_in_department:

                    print(
                        f"ERROR: No doctor found for Department_ID "
                        f"{department_id}"
                    )
                    cursor.close()
                    conn.close()
                    return

                doctor_id = doctors_in_department[
                    total_rows % len(doctors_in_department)
                ]

                fallback_doctor_used += 1

            # ----------------------------------------------------
            # ADMISSION
            # ----------------------------------------------------

            final_admission_id = None

            if admission_id in admissions:

                admission_valid += 1

                if admissions[admission_id] == patient_id:

                    final_admission_id = admission_id
                    admission_patient_match += 1

                else:

                    # Do not preserve an incorrect relationship.
                    admission_nullified += 1

            # ----------------------------------------------------
            # PROCEDURE DATE
            # ----------------------------------------------------

            procedure_date = parse_date(
                row["Procedure_Date"]
            )

            if procedure_date is None:
                invalid_date += 1
                continue

            # ----------------------------------------------------
            # COST
            # ----------------------------------------------------

            try:
                cost = Decimal(row["Cost"].strip())

                if cost < 0:
                    invalid_cost += 1
                    continue

            except (InvalidOperation, ValueError):
                invalid_cost += 1
                continue

            # ----------------------------------------------------
            # PROCEDURE TYPE
            # ----------------------------------------------------

            procedure_type = row["Procedure_Type"].strip()

            allowed_categories = {
                "Surgical",
                "Diagnostic",
                "Therapeutic",
                "Emergency",
                "Minimally Invasive",
                "Other"
            }

            if procedure_type not in allowed_categories:
                procedure_type = "Other"

            category_counts[procedure_type] = (
                category_counts.get(procedure_type, 0) + 1
            )

            # ----------------------------------------------------
            # STATUS
            # ----------------------------------------------------

            procedure_status = row["Procedure_Status"].strip()

            allowed_statuses = {
                "Scheduled",
                "In Progress",
                "Completed",
                "Cancelled"
            }

            if procedure_status not in allowed_statuses:
                procedure_status = "Scheduled"

            status_counts[procedure_status] = (
                status_counts.get(procedure_status, 0) + 1
            )

            # ----------------------------------------------------
            # ANAESTHESIA
            # ----------------------------------------------------

            anesthesia_used = row["Anesthesia_Used"].strip()

            if anesthesia_used.lower() == "yes":
                anesthesia_type = "General"
            else:
                anesthesia_type = "None"

            anesthesia_counts[anesthesia_type] = (
                anesthesia_counts.get(anesthesia_type, 0) + 1
            )

            # ----------------------------------------------------
            # PROCEDURE NUMBER
            # ----------------------------------------------------

            procedure_number = f"PROC-{total_rows:06d}"

            # ----------------------------------------------------
            # DURATION
            # ----------------------------------------------------

            duration_minutes = 30

            # ----------------------------------------------------
            # PRIORITY
            # ----------------------------------------------------

            if procedure_type == "Emergency":
                priority = "Emergency"
            elif procedure_status == "Completed":
                priority = "Medium"
            else:
                priority = "Medium"

            # ----------------------------------------------------
            # OUTCOME
            # ----------------------------------------------------

            if procedure_status == "Completed":
                outcome = "Procedure completed successfully."
            elif procedure_status == "Cancelled":
                outcome = "Procedure cancelled."
            else:
                outcome = None

            # ----------------------------------------------------
            # INSERT VALUES
            # ----------------------------------------------------

            values = (
                source_procedure_id,
                patient_id,
                doctor_id,
                final_admission_id,
                None,                       # Diagnosis_ID
                department_id,

                procedure_number,
                None,                       # Procedure_Code

                row["Procedure_Name"].strip(),
                procedure_type,
                procedure_date,
                duration_minutes,

                procedure_status,
                priority,

                None,                       # Operation_Theater
                None,                       # Anaesthetist
                None,                       # Assistant_Surgeon

                anesthesia_type,
                cost,

                None,                       # Complications
                outcome,

                0,                          # Follow_Up_Required

                row["Notes"].strip() or None,

                "Low",                      # AI_Risk_Level
                None,                       # AI_Recommendation
                None,                       # AI_Confidence

                "Synthetic",

                1,                          # Is_Active
                0,                          # Is_Deleted
                1,                          # Record_Version

                None,                       # Created_By
                None                        # Updated_By
            )

            batch.append(values)
            valid_rows += 1

            # ----------------------------------------------------
            # BATCH INSERT
            # ----------------------------------------------------

            if len(batch) >= BATCH_SIZE:

                cursor.executemany(insert_sql, batch)
                conn.commit()

                batch.clear()

                if total_rows % 25000 == 0:
                    print(
                        f"Processed: {total_rows:,} | "
                        f"Valid: {valid_rows:,}"
                    )

    # ------------------------------------------------------------
    # REMAINING BATCH
    # ------------------------------------------------------------

    if batch:
        cursor.executemany(insert_sql, batch)
        conn.commit()
        batch.clear()

    # ------------------------------------------------------------
    # SOURCE VALIDATION
    # ------------------------------------------------------------

    print("\n" + "=" * 70)
    print("SOURCE VALIDATION")
    print("=" * 70)

    print(f"Source rows processed:             {total_rows:,}")
    print(f"Valid records prepared:            {valid_rows:,}")
    print(f"Invalid Patient_ID:                {invalid_patient:,}")
    print(f"Invalid Doctor_ID:                 {invalid_doctor:,}")
    print(f"Invalid Department_ID:             {invalid_department:,}")
    print(f"Invalid Procedure_Date:            {invalid_date:,}")
    print(f"Invalid Cost:                      {invalid_cost:,}")

    print("\nDOCTOR HANDLING")
    print("-" * 70)
    print(f"Valid source doctors used:         {source_doctor_used:,}")
    print(f"Fallback doctors used:             {fallback_doctor_used:,}")

    print("\nADMISSION HANDLING")
    print("-" * 70)
    print(f"Admission IDs existing in DB:      {admission_valid:,}")
    print(f"Admission -> Patient matches:      {admission_patient_match:,}")
    print(f"Incorrect admissions set NULL:      {admission_nullified:,}")

    print("\nPROCEDURE CATEGORY")
    print("-" * 70)

    for key, value in category_counts.items():
        print(f"{key}: {value:,}")

    print("\nPROCEDURE STATUS")
    print("-" * 70)

    for key, value in status_counts.items():
        print(f"{key}: {value:,}")

    print("\nANAESTHESIA")
    print("-" * 70)

    for key, value in anesthesia_counts.items():
        print(f"{key}: {value:,}")

    # ------------------------------------------------------------
    # DATABASE VALIDATION
    # ------------------------------------------------------------

    cursor.execute("SELECT COUNT(*) FROM medical_procedures")
    actual_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(DISTINCT Procedure_ID)
        FROM medical_procedures
    """)
    unique_procedure_ids = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(DISTINCT Procedure_Number)
        FROM medical_procedures
    """)
    unique_procedure_numbers = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(DISTINCT Patient_ID)
        FROM medical_procedures
    """)
    unique_patients = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(DISTINCT Doctor_ID)
        FROM medical_procedures
    """)
    unique_doctors = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(DISTINCT Department_ID)
        FROM medical_procedures
    """)
    unique_departments = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM medical_procedures
        WHERE Patient_ID IS NULL
           OR Doctor_ID IS NULL
           OR Department_ID IS NULL
           OR Procedure_Number IS NULL
           OR Procedure_Name IS NULL
           OR Procedure_Date IS NULL
    """)
    required_nulls = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM medical_procedures mp
        LEFT JOIN patients p
            ON mp.Patient_ID = p.Patient_ID
        WHERE p.Patient_ID IS NULL
    """)
    orphan_patients = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM medical_procedures mp
        LEFT JOIN doctors d
            ON mp.Doctor_ID = d.Doctor_ID
        WHERE d.Doctor_ID IS NULL
    """)
    orphan_doctors = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM medical_procedures mp
        LEFT JOIN departments d
            ON mp.Department_ID = d.Department_ID
        WHERE d.Department_ID IS NULL
    """)
    orphan_departments = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM medical_procedures
        WHERE Procedure_Cost < 0
           OR Duration_Minutes <= 0
    """)
    invalid_ranges = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM medical_procedures
        WHERE Admission_ID IS NOT NULL
    """)
    admission_links = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM medical_procedures mp
        LEFT JOIN admissions a
            ON mp.Admission_ID = a.Admission_ID
        WHERE mp.Admission_ID IS NOT NULL
          AND (
              a.Admission_ID IS NULL
              OR a.Patient_ID <> mp.Patient_ID
          )
    """)
    bad_admission_links = cursor.fetchone()[0]

    # ------------------------------------------------------------
    # DISPLAY DATABASE VALIDATION
    # ------------------------------------------------------------

    print("\n" + "=" * 70)
    print("DATABASE VALIDATION")
    print("=" * 70)

    print(f"Expected records:                  {valid_rows:,}")
    print(f"Actual records:                    {actual_count:,}")
    print(f"Unique Procedure_ID:               {unique_procedure_ids:,}")
    print(f"Unique Procedure_Number:           {unique_procedure_numbers:,}")
    print(f"Unique patients:                   {unique_patients:,}")
    print(f"Unique doctors:                    {unique_doctors:,}")
    print(f"Unique departments:                {unique_departments:,}")

    print("\nNULL CHECKS")
    print("-" * 70)
    print(f"Required fields NULL:              {required_nulls:,}")

    print("\nORPHAN CHECKS")
    print("-" * 70)
    print(f"Orphan patients:                   {orphan_patients:,}")
    print(f"Orphan doctors:                    {orphan_doctors:,}")
    print(f"Orphan departments:                {orphan_departments:,}")

    print("\nRANGE CHECKS")
    print("-" * 70)
    print(f"Invalid cost/duration:             {invalid_ranges:,}")

    print("\nADMISSION LINKAGE")
    print("-" * 70)
    print(f"Valid Admission links retained:    {admission_links:,}")
    print(f"Incorrect Admission links:         {bad_admission_links:,}")

    # ------------------------------------------------------------
    # FINAL STATUS
    # ------------------------------------------------------------

    passed = (
        total_rows == 250000
        and valid_rows == 250000
        and invalid_patient == 0
        and invalid_department == 0
        and invalid_date == 0
        and invalid_cost == 0
        and actual_count == 250000
        and unique_procedure_ids == 250000
        and unique_procedure_numbers == 250000
        and required_nulls == 0
        and orphan_patients == 0
        and orphan_doctors == 0
        and orphan_departments == 0
        and invalid_ranges == 0
        and bad_admission_links == 0
    )

    print("\n" + "=" * 70)

    if passed:
        print("FINAL STATUS: PASSED")
    else:
        print("FINAL STATUS: FAILED")

    print("=" * 70)

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()