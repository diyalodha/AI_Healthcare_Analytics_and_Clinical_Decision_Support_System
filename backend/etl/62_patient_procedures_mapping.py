import os
import sys
import uuid
import mysql.connector
from mysql.connector import Error


# ============================================================
# CONFIGURATION
# ============================================================

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": "healthcare_ai_db",
    "charset": "utf8mb4",
}

BATCH_SIZE = 5000


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    if not DB_CONFIG["password"]:
        print("\nERROR: MYSQL_PASSWORD environment variable is not set.")
        print("\nRun this first in PowerShell:")
        print('$env:MYSQL_PASSWORD = Read-Host "Enter MySQL root password"')
        sys.exit(1)

    return mysql.connector.connect(**DB_CONFIG)


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("STEP 62 - PATIENT PROCEDURES MAPPING")
    print("=" * 70)

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        # ====================================================
        # LOAD VALID DATABASE IDS
        # ====================================================

        cursor.execute("""
            SELECT Patient_ID
            FROM patients
        """)
        valid_patients = {
            str(row[0])
            for row in cursor.fetchall()
        }

        cursor.execute("""
            SELECT Doctor_ID
            FROM doctors
        """)
        valid_doctors = {
            str(row[0])
            for row in cursor.fetchall()
        }

        cursor.execute("""
            SELECT Department_ID
            FROM departments
        """)
        valid_departments = {
            str(row[0])
            for row in cursor.fetchall()
        }

        cursor.execute("""
            SELECT Procedure_ID
            FROM medical_procedures
        """)
        valid_procedures = {
            str(row[0])
            for row in cursor.fetchall()
        }

        cursor.execute("""
            SELECT Admission_ID
            FROM admissions
        """)
        valid_admissions = {
            str(row[0])
            for row in cursor.fetchall()
        }

        print(
            f"\nDB patients:                    "
            f"{len(valid_patients):,}"
        )

        print(
            f"DB doctors:                     "
            f"{len(valid_doctors):,}"
        )

        print(
            f"DB departments:                 "
            f"{len(valid_departments):,}"
        )

        print(
            f"DB medical procedures:          "
            f"{len(valid_procedures):,}"
        )

        print(
            f"DB admissions:                   "
            f"{len(valid_admissions):,}"
        )

        # ====================================================
        # EXISTING MAPPINGS
        # ====================================================

        cursor.execute("""
            SELECT COUNT(*)
            FROM patient_procedures_map
        """)

        existing_count = cursor.fetchone()[0]

        print(
            f"Existing patient_procedures_map: "
            f"{existing_count:,}"
        )

        # ====================================================
        # CLEAR EXISTING MAPPINGS
        # ====================================================

        if existing_count > 0:

            print("\nClearing existing mappings...")

            cursor.execute("""
                DELETE FROM patient_procedures_map
            """)

            connection.commit()

            print("Existing mappings cleared.")

        # ====================================================
        # READ VALIDATED MEDICAL PROCEDURES
        # ====================================================

        print("\nReading validated medical_procedures table...")

        cursor.execute("""
            SELECT
                Procedure_ID,
                Patient_ID,
                Doctor_ID,
                Admission_ID,
                Department_ID,
                Procedure_Number,
                Procedure_Name,
                Procedure_Category,
                Procedure_Date,
                Duration_Minutes,
                Procedure_Status,
                Priority,
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
            FROM medical_procedures
        """)

        rows = cursor.fetchall()

        total_source_rows = len(rows)

        print(
            f"Medical procedure rows:         "
            f"{total_source_rows:,}"
        )

        # ====================================================
        # VALIDATION COUNTERS
        # ====================================================

        valid_rows = 0

        invalid_patient = 0
        invalid_doctor = 0
        invalid_department = 0
        invalid_procedure = 0
        invalid_admission = 0

        admission_retained = 0
        admission_null = 0

        inserted_rows = 0

        unique_patients = set()
        unique_procedures = set()
        unique_doctors = set()
        unique_departments = set()

        category_counts = {}
        status_counts = {}
        anesthesia_counts = {}
        priority_counts = {}

        records_to_insert = []

        # ====================================================
        # PROCESS PROCEDURES
        # ====================================================

        for index, row in enumerate(rows, start=1):

            (
                procedure_id,
                patient_id,
                doctor_id,
                admission_id,
                department_id,
                procedure_number,
                procedure_name,
                procedure_category,
                procedure_date,
                duration_minutes,
                procedure_status,
                priority,
                anaesthesia_type,
                procedure_cost,
                complications,
                procedure_outcome,
                follow_up_required,
                notes,
                ai_risk_level,
                ai_recommendation,
                ai_confidence,
                data_source,
                is_active,
                is_deleted,
                record_version,
                created_by,
                updated_by
            ) = row

            procedure_id = str(procedure_id)
            patient_id = str(patient_id)
            doctor_id = str(doctor_id)
            department_id = str(department_id)

            # ------------------------------------------------
            # PATIENT
            # ------------------------------------------------

            if patient_id not in valid_patients:
                invalid_patient += 1
                continue

            # ------------------------------------------------
            # PROCEDURE
            # ------------------------------------------------

            if procedure_id not in valid_procedures:
                invalid_procedure += 1
                continue

            # ------------------------------------------------
            # DOCTOR
            # ------------------------------------------------

            if doctor_id not in valid_doctors:
                invalid_doctor += 1
                continue

            # ------------------------------------------------
            # DEPARTMENT
            # ------------------------------------------------

            if department_id not in valid_departments:
                invalid_department += 1
                continue

            # ------------------------------------------------
            # ADMISSION
            #
            # IMPORTANT:
            # We only retain an Admission_ID if it exists in
            # the actual admissions table AND belongs to the
            # same patient.
            # ------------------------------------------------

            if admission_id is not None:

                admission_id = str(admission_id)

                if admission_id in valid_admissions:

                    cursor.execute("""
                        SELECT Patient_ID
                        FROM admissions
                        WHERE Admission_ID = %s
                    """, (admission_id,))

                    admission_row = cursor.fetchone()

                    if admission_row is not None:

                        admission_patient = str(
                            admission_row[0]
                        )

                        if admission_patient == patient_id:

                            admission_retained += 1

                        else:

                            admission_id = None
                            admission_null += 1

                    else:

                        admission_id = None
                        admission_null += 1

                else:

                    invalid_admission += 1
                    admission_id = None
                    admission_null += 1

            else:

                admission_null += 1

            # ------------------------------------------------
            # MAP ID
            # ------------------------------------------------

            map_id = str(uuid.uuid4())

            # ------------------------------------------------
            # INSERT RECORD
            # ------------------------------------------------

            records_to_insert.append(
                (
                    map_id,
                    patient_id,
                    procedure_id,
                    doctor_id,
                    admission_id,
                    department_id,
                    procedure_number,
                    procedure_name,
                    procedure_category,
                    procedure_date,
                    duration_minutes,
                    procedure_status,
                    priority,
                    anaesthesia_type,
                    procedure_cost,
                    complications,
                    procedure_outcome,
                    follow_up_required,
                    notes,
                    ai_risk_level,
                    ai_recommendation,
                    ai_confidence,
                    data_source,
                    is_active,
                    is_deleted,
                    record_version,
                    created_by,
                    updated_by
                )
            )

            valid_rows += 1

            unique_patients.add(patient_id)
            unique_procedures.add(procedure_id)
            unique_doctors.add(doctor_id)
            unique_departments.add(department_id)

            category_counts[procedure_category] = (
                category_counts.get(
                    procedure_category,
                    0
                ) + 1
            )

            status_counts[procedure_status] = (
                status_counts.get(
                    procedure_status,
                    0
                ) + 1
            )

            anesthesia_counts[anaesthesia_type] = (
                anesthesia_counts.get(
                    anaesthesia_type,
                    0
                ) + 1
            )

            priority_counts[priority] = (
                priority_counts.get(
                    priority,
                    0
                ) + 1
            )

            # ------------------------------------------------
            # BATCH INSERT
            # ------------------------------------------------

            if len(records_to_insert) >= BATCH_SIZE:

                insert_sql = """
                    INSERT INTO patient_procedures_map
                    (
                        Procedure_Map_ID,
                        Patient_ID,
                        Procedure_ID,
                        Doctor_ID,
                        Admission_ID,
                        Department_ID,
                        Procedure_Number,
                        Procedure_Name,
                        Procedure_Category,
                        Procedure_Date,
                        Duration_Minutes,
                        Procedure_Status,
                        Priority,
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
                    VALUES
                    (
                        %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s
                    )
                """

                cursor.executemany(
                    insert_sql,
                    records_to_insert
                )

                connection.commit()

                inserted_rows += len(records_to_insert)

                records_to_insert = []

            if index % 25000 == 0:

                print(
                    f"Processed: {index:,} | "
                    f"Valid: {valid_rows:,}"
                )

        # ====================================================
        # INSERT REMAINING RECORDS
        # ====================================================

        if records_to_insert:

            insert_sql = """
                INSERT INTO patient_procedures_map
                (
                    Procedure_Map_ID,
                    Patient_ID,
                    Procedure_ID,
                    Doctor_ID,
                    Admission_ID,
                    Department_ID,
                    Procedure_Number,
                    Procedure_Name,
                    Procedure_Category,
                    Procedure_Date,
                    Duration_Minutes,
                    Procedure_Status,
                    Priority,
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
                VALUES
                (
                    %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s
                )
            """

            cursor.executemany(
                insert_sql,
                records_to_insert
            )

            connection.commit()

            inserted_rows += len(records_to_insert)

        # ====================================================
        # SOURCE VALIDATION
        # ====================================================

        print("\n" + "=" * 70)
        print("SOURCE VALIDATION")
        print("=" * 70)

        print(
            f"Source medical procedures:       "
            f"{total_source_rows:,}"
        )

        print(
            f"Valid records prepared:           "
            f"{valid_rows:,}"
        )

        print(
            f"Invalid Patient_ID:               "
            f"{invalid_patient:,}"
        )

        print(
            f"Invalid Procedure_ID:             "
            f"{invalid_procedure:,}"
        )

        print(
            f"Invalid Doctor_ID:                "
            f"{invalid_doctor:,}"
        )

        print(
            f"Invalid Department_ID:            "
            f"{invalid_department:,}"
        )

        print(
            f"Invalid Admission_ID:              "
            f"{invalid_admission:,}"
        )

        # ====================================================
        # ADMISSION HANDLING
        # ====================================================

        print("\n" + "=" * 70)
        print("ADMISSION HANDLING")
        print("=" * 70)

        print(
            f"Admission links retained:         "
            f"{admission_retained:,}"
        )

        print(
            f"Admission links set NULL:         "
            f"{admission_null:,}"
        )

        # ====================================================
        # PROCEDURE CATEGORY
        # ====================================================

        print("\n" + "=" * 70)
        print("PROCEDURE CATEGORY")
        print("=" * 70)

        for key in sorted(category_counts):

            print(
                f"{key}:".ljust(35),
                f"{category_counts[key]:,}"
            )

        # ====================================================
        # STATUS
        # ====================================================

        print("\n" + "=" * 70)
        print("PROCEDURE STATUS")
        print("=" * 70)

        for key in sorted(status_counts):

            print(
                f"{key}:".ljust(35),
                f"{status_counts[key]:,}"
            )

        # ====================================================
        # ANAESTHESIA
        # ====================================================

        print("\n" + "=" * 70)
        print("ANAESTHESIA")
        print("=" * 70)

        for key in sorted(anesthesia_counts):

            print(
                f"{key}:".ljust(35),
                f"{anesthesia_counts[key]:,}"
            )

        # ====================================================
        # PRIORITY
        # ====================================================

        print("\n" + "=" * 70)
        print("PRIORITY")
        print("=" * 70)

        for key in sorted(priority_counts):

            print(
                f"{key}:".ljust(35),
                f"{priority_counts[key]:,}"
            )

        # ====================================================
        # DATABASE VALIDATION
        # ====================================================

        cursor.execute("""
            SELECT COUNT(*)
            FROM patient_procedures_map
        """)

        actual_count = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(DISTINCT Procedure_Map_ID)
            FROM patient_procedures_map
        """)

        unique_map_ids = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(DISTINCT Procedure_ID)
            FROM patient_procedures_map
        """)

        unique_target_procedures = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(DISTINCT Patient_ID)
            FROM patient_procedures_map
        """)

        unique_target_patients = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(DISTINCT Doctor_ID)
            FROM patient_procedures_map
        """)

        unique_target_doctors = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(DISTINCT Department_ID)
            FROM patient_procedures_map
        """)

        unique_target_departments = cursor.fetchone()[0]

        # ====================================================
        # REQUIRED NULL CHECK
        # ====================================================

        cursor.execute("""
            SELECT COUNT(*)
            FROM patient_procedures_map
            WHERE Patient_ID IS NULL
               OR Procedure_ID IS NULL
               OR Doctor_ID IS NULL
               OR Department_ID IS NULL
               OR Procedure_Number IS NULL
               OR Procedure_Name IS NULL
               OR Procedure_Category IS NULL
               OR Procedure_Date IS NULL
               OR Procedure_Status IS NULL
        """)

        required_nulls = cursor.fetchone()[0]

        # ====================================================
        # ORPHAN PATIENTS
        # ====================================================

        cursor.execute("""
            SELECT COUNT(*)
            FROM patient_procedures_map ppm
            LEFT JOIN patients p
                ON ppm.Patient_ID = p.Patient_ID
            WHERE p.Patient_ID IS NULL
        """)

        orphan_patients = cursor.fetchone()[0]

        # ====================================================
        # ORPHAN PROCEDURES
        # ====================================================

        cursor.execute("""
            SELECT COUNT(*)
            FROM patient_procedures_map ppm
            LEFT JOIN medical_procedures mp
                ON ppm.Procedure_ID = mp.Procedure_ID
            WHERE mp.Procedure_ID IS NULL
        """)

        orphan_procedures = cursor.fetchone()[0]

        # ====================================================
        # ORPHAN DOCTORS
        # ====================================================

        cursor.execute("""
            SELECT COUNT(*)
            FROM patient_procedures_map ppm
            LEFT JOIN doctors d
                ON ppm.Doctor_ID = d.Doctor_ID
            WHERE d.Doctor_ID IS NULL
        """)

        orphan_doctors = cursor.fetchone()[0]

        # ====================================================
        # ORPHAN DEPARTMENTS
        # ====================================================

        cursor.execute("""
            SELECT COUNT(*)
            FROM patient_procedures_map ppm
            LEFT JOIN departments d
                ON ppm.Department_ID = d.Department_ID
            WHERE d.Department_ID IS NULL
        """)

        orphan_departments = cursor.fetchone()[0]

        # ====================================================
        # ADMISSION FK VALIDATION
        # ====================================================

        cursor.execute("""
            SELECT COUNT(*)
            FROM patient_procedures_map ppm
            LEFT JOIN admissions a
                ON ppm.Admission_ID = a.Admission_ID
            WHERE ppm.Admission_ID IS NOT NULL
              AND a.Admission_ID IS NULL
        """)

        orphan_admissions = cursor.fetchone()[0]

        # ====================================================
        # ADMISSION-PATIENT CONSISTENCY
        # ====================================================

        cursor.execute("""
            SELECT COUNT(*)
            FROM patient_procedures_map ppm
            JOIN admissions a
                ON ppm.Admission_ID = a.Admission_ID
            WHERE ppm.Patient_ID <> a.Patient_ID
        """)

        incorrect_admission_links = cursor.fetchone()[0]

        # ====================================================
        # PROCEDURE CONSISTENCY
        # ====================================================

        cursor.execute("""
            SELECT COUNT(*)
            FROM patient_procedures_map ppm
            JOIN medical_procedures mp
                ON ppm.Procedure_ID = mp.Procedure_ID
            WHERE ppm.Patient_ID <> mp.Patient_ID
               OR ppm.Doctor_ID <> mp.Doctor_ID
               OR ppm.Department_ID <> mp.Department_ID
               OR ppm.Procedure_Name <> mp.Procedure_Name
               OR ppm.Procedure_Date <> mp.Procedure_Date
        """)

        procedure_mismatches = cursor.fetchone()[0]

        # ====================================================
        # DATA SOURCE
        # ====================================================

        cursor.execute("""
            SELECT Data_Source, COUNT(*)
            FROM patient_procedures_map
            GROUP BY Data_Source
        """)

        data_sources = cursor.fetchall()

        # ====================================================
        # ACTIVE
        # ====================================================

        cursor.execute("""
            SELECT Is_Active, COUNT(*)
            FROM patient_procedures_map
            GROUP BY Is_Active
        """)

        active_counts = cursor.fetchall()

        # ====================================================
        # DELETED
        # ====================================================

        cursor.execute("""
            SELECT Is_Deleted, COUNT(*)
            FROM patient_procedures_map
            GROUP BY Is_Deleted
        """)

        deleted_counts = cursor.fetchall()

        # ====================================================
        # FINAL DATABASE REPORT
        # ====================================================

        print("\n" + "=" * 70)
        print("DATABASE VALIDATION")
        print("=" * 70)

        print(
            f"Expected records:                 "
            f"{valid_rows:,}"
        )

        print(
            f"Inserted records:                 "
            f"{inserted_rows:,}"
        )

        print(
            f"Actual records:                   "
            f"{actual_count:,}"
        )

        print(
            f"Unique Procedure_Map_ID:          "
            f"{unique_map_ids:,}"
        )

        print(
            f"Unique Procedure_ID:              "
            f"{unique_target_procedures:,}"
        )

        print(
            f"Unique patients:                  "
            f"{unique_target_patients:,}"
        )

        print(
            f"Unique doctors:                   "
            f"{unique_target_doctors:,}"
        )

        print(
            f"Unique departments:               "
            f"{unique_target_departments:,}"
        )

        # ====================================================
        # NULL CHECKS
        # ====================================================

        print("\n" + "=" * 70)
        print("NULL CHECKS")
        print("=" * 70)

        print(
            f"Required fields NULL:             "
            f"{required_nulls:,}"
        )

        # ====================================================
        # ORPHAN CHECKS
        # ====================================================

        print("\n" + "=" * 70)
        print("ORPHAN CHECKS")
        print("=" * 70)

        print(
            f"Orphan patients:                  "
            f"{orphan_patients:,}"
        )

        print(
            f"Orphan procedures:                "
            f"{orphan_procedures:,}"
        )

        print(
            f"Orphan doctors:                   "
            f"{orphan_doctors:,}"
        )

        print(
            f"Orphan departments:               "
            f"{orphan_departments:,}"
        )

        print(
            f"Orphan admissions:                "
            f"{orphan_admissions:,}"
        )

        # ====================================================
        # CONSISTENCY
        # ====================================================

        print("\n" + "=" * 70)
        print("CONSISTENCY CHECKS")
        print("=" * 70)

        print(
            f"Procedure relationship mismatches:"
            f" {procedure_mismatches:,}"
        )

        print(
            f"Incorrect Admission -> Patient:   "
            f"{incorrect_admission_links:,}"
        )

        # ====================================================
        # DATA SOURCE
        # ====================================================

        print("\n" + "=" * 70)
        print("DATA SOURCE")
        print("=" * 70)

        for source, count in data_sources:

            print(
                f"{source}:".ljust(35),
                f"{count:,}"
            )

        # ====================================================
        # ACTIVE STATUS
        # ====================================================

        print("\n" + "=" * 70)
        print("ACTIVE STATUS")
        print("=" * 70)

        for status, count in active_counts:

            print(
                f"Is_Active = {status}:".ljust(35),
                f"{count:,}"
            )

        # ====================================================
        # DELETED STATUS
        # ====================================================

        print("\n" + "=" * 70)
        print("DELETED STATUS")
        print("=" * 70)

        for status, count in deleted_counts:

            print(
                f"Is_Deleted = {status}:".ljust(35),
                f"{count:,}"
            )

        # ====================================================
        # FINAL PASS / FAIL
        # ====================================================

        passed = True

        if actual_count != valid_rows:
            passed = False

        if inserted_rows != valid_rows:
            passed = False

        if unique_map_ids != actual_count:
            passed = False

        if unique_target_procedures != actual_count:
            passed = False

        if required_nulls != 0:
            passed = False

        if orphan_patients != 0:
            passed = False

        if orphan_procedures != 0:
            passed = False

        if orphan_doctors != 0:
            passed = False

        if orphan_departments != 0:
            passed = False

        if orphan_admissions != 0:
            passed = False

        if incorrect_admission_links != 0:
            passed = False

        if procedure_mismatches != 0:
            passed = False

        print("\n" + "=" * 70)

        if passed:
            print("FINAL STATUS: PASSED")
        else:
            print("FINAL STATUS: FAILED")

        print("=" * 70)

    except Error as e:

        if connection:
            connection.rollback()

        print("\nDATABASE ERROR:")
        print(e)

        sys.exit(1)

    except Exception as e:

        if connection:
            connection.rollback()

        print("\nERROR:")
        print(e)

        sys.exit(1)

    finally:

        if cursor:
            cursor.close()

        if connection and connection.is_connected():
            connection.close()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()