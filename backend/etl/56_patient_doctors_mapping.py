import os
import sys
import uuid
import pandas as pd
import mysql.connector
from mysql.connector import Error

# ============================================================
# STEP 56 - PATIENT DOCTORS MAPPING
# ============================================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

DIAGNOSES_FILE = os.path.join(
    BASE_DIR,
    "datasets",
    "synthetic",
    "diagnoses.csv"
)

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "database": "healthcare_ai_db"
}

BATCH_SIZE = 5000


def print_header(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def get_connection():
    password = input("Enter MySQL root password: ")

    return mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=password,
        database=DB_CONFIG["database"]
    )


def main():

    print_header("STEP 56 - PATIENT DOCTORS MAPPING")

    # --------------------------------------------------------
    # 1. LOAD DIAGNOSES
    # --------------------------------------------------------

    print("\nLoading diagnoses.csv...")

    if not os.path.exists(DIAGNOSES_FILE):
        print(f"ERROR: File not found:\n{DIAGNOSES_FILE}")
        sys.exit(1)

    diagnoses = pd.read_csv(DIAGNOSES_FILE)

    print(f"Diagnosis rows loaded: {len(diagnoses):,}")

    required_columns = [
        "Patient_ID",
        "Doctor_ID",
        "Diagnosis_Date"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in diagnoses.columns
    ]

    if missing_columns:
        print("ERROR: Missing required columns:")
        for col in missing_columns:
            print(f"  - {col}")
        sys.exit(1)

    # --------------------------------------------------------
    # 2. SOURCE VALIDATION
    # --------------------------------------------------------

    print_header("SOURCE VALIDATION")

    diagnoses["Diagnosis_Date"] = pd.to_datetime(
        diagnoses["Diagnosis_Date"],
        errors="coerce"
    )

    null_patient = diagnoses["Patient_ID"].isna().sum()
    null_doctor = diagnoses["Doctor_ID"].isna().sum()
    null_date = diagnoses["Diagnosis_Date"].isna().sum()

    print(f"NULL Patient_ID:      {null_patient:,}")
    print(f"NULL Doctor_ID:       {null_doctor:,}")
    print(f"NULL Diagnosis_Date:  {null_date:,}")

    # Keep only rows required to form a doctor relationship
    valid_source = diagnoses[
        diagnoses["Patient_ID"].notna()
        & diagnoses["Doctor_ID"].notna()
        & diagnoses["Diagnosis_Date"].notna()
    ].copy()

    print(f"Valid source rows:     {len(valid_source):,}")

    # --------------------------------------------------------
    # 3. CREATE DATABASE CONNECTION
    # --------------------------------------------------------

    print("\nConnecting to MySQL...")

    try:
        conn = get_connection()

        if not conn.is_connected():
            print("ERROR: MySQL connection failed.")
            sys.exit(1)

        cursor = conn.cursor(dictionary=True)

        print("MySQL connection successful.")

    except Error as e:
        print(f"ERROR connecting to MySQL: {e}")
        sys.exit(1)

    # --------------------------------------------------------
    # 4. CHECK EXISTING MAPPINGS
    # --------------------------------------------------------

    cursor.execute(
        "SELECT COUNT(*) AS total "
        "FROM patient_doctors_map"
    )

    existing_count = cursor.fetchone()["total"]

    print(
        f"\nExisting patient_doctors_map records: "
        f"{existing_count:,}"
    )

    if existing_count > 0:
        print(
            "\nERROR: patient_doctors_map already contains "
            "records."
        )
        print(
            "No records were modified to avoid duplicate mappings."
        )

        cursor.close()
        conn.close()
        sys.exit(1)

    # --------------------------------------------------------
    # 5. LOAD VALID PATIENT IDS
    # --------------------------------------------------------

    print("\nLoading valid database Patient_IDs...")

    cursor.execute(
        "SELECT Patient_ID FROM patients"
    )

    patient_rows = cursor.fetchall()

    valid_patient_ids = {
        row["Patient_ID"]
        for row in patient_rows
    }

    print(
        f"Valid patients in database: "
        f"{len(valid_patient_ids):,}"
    )

    # --------------------------------------------------------
    # 6. LOAD DOCTOR + DEPARTMENT RELATIONSHIPS
    # --------------------------------------------------------

    print("\nLoading actual database Doctor_IDs...")

    cursor.execute(
        """
        SELECT
            Doctor_ID,
            Department_ID
        FROM doctors
        """
    )

    doctor_rows = cursor.fetchall()

    doctor_department = {
        row["Doctor_ID"]: row["Department_ID"]
        for row in doctor_rows
    }

    print(
        f"Valid doctors in database: "
        f"{len(doctor_department):,}"
    )

    # --------------------------------------------------------
    # 7. FILTER VALID RELATIONSHIPS
    # --------------------------------------------------------

    print_header("RELATIONSHIP VALIDATION")

    valid_source["Patient_ID"] = (
        valid_source["Patient_ID"].astype(str)
    )

    valid_source["Doctor_ID"] = (
        valid_source["Doctor_ID"].astype(str)
    )

    valid_source["patient_valid"] = (
        valid_source["Patient_ID"].isin(valid_patient_ids)
    )

    valid_source["doctor_valid"] = (
        valid_source["Doctor_ID"].isin(doctor_department)
    )

    invalid_patients = (
        (~valid_source["patient_valid"]).sum()
    )

    invalid_doctors = (
        (~valid_source["doctor_valid"]).sum()
    )

    print(
        f"Invalid Patient_ID rows: "
        f"{invalid_patients:,}"
    )

    print(
        f"Invalid Doctor_ID rows:  "
        f"{invalid_doctors:,}"
    )

    valid_relationships = valid_source[
        valid_source["patient_valid"]
        & valid_source["doctor_valid"]
    ].copy()

    print(
        f"Valid diagnosis relationships: "
        f"{len(valid_relationships):,}"
    )

    if valid_relationships.empty:
        print("\nERROR: No valid patient-doctor relationships found.")
        cursor.close()
        conn.close()
        sys.exit(1)

    # --------------------------------------------------------
    # 8. NORMALIZE DATES
    # --------------------------------------------------------

    valid_relationships["Diagnosis_Date"] = (
        valid_relationships["Diagnosis_Date"].dt.date
    )

    # --------------------------------------------------------
    # 9. BUILD PATIENT-DOCTOR RELATIONSHIPS
    # --------------------------------------------------------

    print("\nGenerating patient-doctor relationships...")

    relationship_summary = (
        valid_relationships
        .groupby(
            ["Patient_ID", "Doctor_ID"],
            as_index=False
        )
        .agg(
            Start_Date=("Diagnosis_Date", "min"),
            Last_Consultation_Date=("Diagnosis_Date", "max"),
            Total_Visits_Completed=("Diagnosis_Date", "count")
        )
    )

    print(
        f"Unique Patient-Doctor relationships: "
        f"{len(relationship_summary):,}"
    )

    # --------------------------------------------------------
    # 10. DETERMINE PRIMARY DOCTOR
    # --------------------------------------------------------

    relationship_summary = relationship_summary.sort_values(
        [
            "Patient_ID",
            "Start_Date",
            "Doctor_ID"
        ]
    )

    relationship_summary["Is_Primary_Doctor"] = (
        relationship_summary
        .groupby("Patient_ID")
        .cumcount()
        .eq(0)
        .astype(int)
    )

    # --------------------------------------------------------
    # 11. ADD DEPARTMENT
    # --------------------------------------------------------

    relationship_summary["Department_ID"] = (
        relationship_summary["Doctor_ID"]
        .map(doctor_department)
    )

    # --------------------------------------------------------
    # 12. INSERT DATA
    # --------------------------------------------------------

    print_header("INSERTING PATIENT-DOCTOR MAPPINGS")

    insert_sql = """
        INSERT INTO patient_doctors_map
        (
            Patient_Doctor_Map_ID,
            Patient_ID,
            Doctor_ID,
            Department_ID,
            Doctor_Role,
            Is_Primary_Doctor,
            Assignment_Reason,
            Start_Date,
            End_Date,
            Relationship_Status,
            Total_Visits_Completed,
            Last_Consultation_Date,
            Next_Scheduled_Visit,
            Clinical_Notes,
            Data_Source,
            Created_By,
            Updated_By
        )
        VALUES
        (
            %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s
        )
    """

    inserted = 0

    try:

        batch = []

        for _, row in relationship_summary.iterrows():

            patient_id = row["Patient_ID"]
            doctor_id = row["Doctor_ID"]
            department_id = row["Department_ID"]

            start_date = row["Start_Date"]
            last_date = row["Last_Consultation_Date"]

            total_visits = int(
                row["Total_Visits_Completed"]
            )

            is_primary = int(
                row["Is_Primary_Doctor"]
            )

            values = (
                str(uuid.uuid4()),
                patient_id,
                doctor_id,
                department_id,
                "Attending Physician",
                is_primary,
                "Derived from diagnosis records",
                start_date,
                None,
                "Active",
                total_visits,
                last_date,
                None,
                "Synthetic patient-doctor relationship derived from diagnosis history.",
                "Synthetic",
                "ETL_56",
                "ETL_56"
            )

            batch.append(values)

            if len(batch) >= BATCH_SIZE:

                cursor.executemany(
                    insert_sql,
                    batch
                )

                conn.commit()

                inserted += len(batch)

                print(
                    f"Inserted: {inserted:,}"
                )

                batch = []

        if batch:

            cursor.executemany(
                insert_sql,
                batch
            )

            conn.commit()

            inserted += len(batch)

            print(
                f"Inserted: {inserted:,}"
            )

    except Error as e:

        conn.rollback()

        print(
            f"\nERROR during insertion: {e}"
        )

        cursor.close()
        conn.close()
        sys.exit(1)

    # --------------------------------------------------------
    # 13. DATABASE VALIDATION
    # --------------------------------------------------------

    print_header("STEP 56 DATABASE VALIDATION")

    cursor.execute(
        "SELECT COUNT(*) AS total "
        "FROM patient_doctors_map"
    )

    total_mappings = cursor.fetchone()["total"]

    cursor.execute(
        """
        SELECT COUNT(DISTINCT Patient_ID) AS total
        FROM patient_doctors_map
        """
    )

    unique_patients = cursor.fetchone()["total"]

    cursor.execute(
        """
        SELECT COUNT(DISTINCT Doctor_ID) AS total
        FROM patient_doctors_map
        """
    )

    unique_doctors = cursor.fetchone()["total"]

    cursor.execute(
        """
        SELECT COUNT(DISTINCT Department_ID) AS total
        FROM patient_doctors_map
        """
    )

    unique_departments = cursor.fetchone()["total"]

    cursor.execute(
        """
        SELECT COUNT(*) AS total
        FROM patient_doctors_map
        WHERE Patient_ID IS NULL
        """
    )

    null_patients = cursor.fetchone()["total"]

    cursor.execute(
        """
        SELECT COUNT(*) AS total
        FROM patient_doctors_map
        WHERE Doctor_ID IS NULL
        """
    )

    null_doctors = cursor.fetchone()["total"]

    cursor.execute(
        """
        SELECT COUNT(*) AS total
        FROM patient_doctors_map p
        LEFT JOIN patients pt
            ON p.Patient_ID = pt.Patient_ID
        WHERE pt.Patient_ID IS NULL
        """
    )

    orphan_patients = cursor.fetchone()["total"]

    cursor.execute(
        """
        SELECT COUNT(*) AS total
        FROM patient_doctors_map p
        LEFT JOIN doctors d
            ON p.Doctor_ID = d.Doctor_ID
        WHERE d.Doctor_ID IS NULL
        """
    )

    orphan_doctors = cursor.fetchone()["total"]

    cursor.execute(
        """
        SELECT COUNT(*) AS total
        FROM patient_doctors_map
        WHERE Data_Source = 'Synthetic'
        """
    )

    synthetic_count = cursor.fetchone()["total"]

    cursor.execute(
        """
        SELECT COUNT(*) AS total
        FROM patient_doctors_map
        WHERE Is_Primary_Doctor = 1
        """
    )

    primary_count = cursor.fetchone()["total"]

    print(f"Total mappings:             {total_mappings:,}")
    print(f"Unique patients:             {unique_patients:,}")
    print(f"Unique doctors:              {unique_doctors:,}")
    print(f"Unique departments:          {unique_departments:,}")
    print(f"NULL Patient_ID:             {null_patients:,}")
    print(f"NULL Doctor_ID:              {null_doctors:,}")
    print(f"Orphan Patient_ID links:     {orphan_patients:,}")
    print(f"Orphan Doctor_ID links:      {orphan_doctors:,}")
    print(f"Synthetic mappings:          {synthetic_count:,}")
    print(f"Primary doctor mappings:     {primary_count:,}")

    # --------------------------------------------------------
    # 14. RELATIONSHIP STATUS
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT
            Relationship_Status,
            COUNT(*) AS total
        FROM patient_doctors_map
        GROUP BY Relationship_Status
        ORDER BY Relationship_Status
        """
    )

    print("\nRELATIONSHIP STATUS")

    for row in cursor.fetchall():

        print(
            f"{row['Relationship_Status']}: "
            f"{row['total']:,}"
        )

    # --------------------------------------------------------
    # 15. DOCTOR ROLE
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT
            Doctor_Role,
            COUNT(*) AS total
        FROM patient_doctors_map
        GROUP BY Doctor_Role
        ORDER BY Doctor_Role
        """
    )

    print("\nDOCTOR ROLE")

    for row in cursor.fetchall():

        print(
            f"{row['Doctor_Role']}: "
            f"{row['total']:,}"
        )

    # --------------------------------------------------------
    # 16. FINAL VALIDATION
    # --------------------------------------------------------

    passed = True

    if total_mappings != inserted:
        passed = False

    if total_mappings == 0:
        passed = False

    if null_patients != 0:
        passed = False

    if null_doctors != 0:
        passed = False

    if orphan_patients != 0:
        passed = False

    if orphan_doctors != 0:
        passed = False

    if synthetic_count != total_mappings:
        passed = False

    if primary_count == 0:
        passed = False

    if passed:

        print_header(
            "STEP 56 - PATIENT DOCTORS MAPPING: PASSED"
        )

    else:

        print_header(
            "STEP 56 - PATIENT DOCTORS MAPPING: FAILED"
        )

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()