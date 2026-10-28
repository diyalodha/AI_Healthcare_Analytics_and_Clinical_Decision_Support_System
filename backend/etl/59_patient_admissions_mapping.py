import os
import sys
import mysql.connector
from mysql.connector import Error

# ============================================================
# STEP 59 — PATIENT ADMISSIONS MAPPING
# ============================================================

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": "healthcare_ai_db",
    "autocommit": False
}

BATCH_SIZE = 5000
SCRIPT_NAME = "59_patient_admissions_mapping"


def get_connection():
    if not DB_CONFIG["password"]:
        print("ERROR: MYSQL_PASSWORD environment variable is not set.")
        print("Set it in PowerShell before running this script.")
        sys.exit(1)

    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print(f"ERROR connecting to MySQL: {e}")
        sys.exit(1)


def main():

    print("=" * 70)
    print("STEP 59 — PATIENT ADMISSIONS MAPPING")
    print("=" * 70)

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:

        # --------------------------------------------------------
        # 1. Read admissions from the validated admissions table
        # --------------------------------------------------------
        print("\nReading admissions from database...")

        cursor.execute("""
            SELECT
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
                AI_Risk_Level,
                Notes,
                Predicted_Disease_ID
            FROM admissions
            WHERE Is_Deleted = 0
            ORDER BY Admission_ID
        """)

        admissions = cursor.fetchall()

        print(f"Admissions read: {len(admissions):,}")

        if not admissions:
            print("\nERROR: No admissions found.")
            conn.rollback()
            return

        # --------------------------------------------------------
        # 2. Load valid patient IDs
        # --------------------------------------------------------
        cursor.execute("""
            SELECT Patient_ID
            FROM patients
        """)

        valid_patients = {
            row["Patient_ID"]
            for row in cursor.fetchall()
        }

        print(f"DB patients: {len(valid_patients):,}")

        # --------------------------------------------------------
        # 3. Load valid departments
        # --------------------------------------------------------
        cursor.execute("""
            SELECT Department_ID
            FROM departments
        """)

        valid_departments = {
            row["Department_ID"]
            for row in cursor.fetchall()
        }

        print(f"DB departments: {len(valid_departments):,}")

        # --------------------------------------------------------
        # 4. Load valid doctors
        # --------------------------------------------------------
        cursor.execute("""
            SELECT Doctor_ID
            FROM doctors
        """)

        valid_doctors = {
            row["Doctor_ID"]
            for row in cursor.fetchall()
        }

        print(f"DB doctors: {len(valid_doctors):,}")

        # --------------------------------------------------------
        # 5. Load valid diseases
        # --------------------------------------------------------
        cursor.execute("""
            SELECT Disease_ID
            FROM diseases
        """)

        valid_diseases = {
            row["Disease_ID"]
            for row in cursor.fetchall()
        }

        print(f"DB diseases: {len(valid_diseases):,}")

        # --------------------------------------------------------
        # 6. Validate source admissions
        # --------------------------------------------------------
        valid_records = []

        invalid_patient = 0
        invalid_department = 0
        invalid_doctor = 0
        invalid_disease = 0

        for row in admissions:

            patient_id = row["Patient_ID"]
            department_id = row["Department_ID"]
            doctor_id = row["Admitting_Doctor_ID"]
            disease_id = row["Predicted_Disease_ID"]

            # Patient is mandatory
            if patient_id not in valid_patients:
                invalid_patient += 1
                continue

            # Department is mandatory
            if department_id not in valid_departments:
                invalid_department += 1
                continue

            # Doctor is mandatory
            if doctor_id not in valid_doctors:
                invalid_doctor += 1
                continue

            # Predicted disease is optional
            if disease_id is not None and disease_id not in valid_diseases:
                invalid_disease += 1
                disease_id = None

            valid_records.append({
                "Admission_ID": row["Admission_ID"],
                "Patient_ID": patient_id,
                "Department_ID": department_id,
                "Admitting_Doctor_ID": doctor_id,
                "Predicted_Disease_ID": disease_id,
                "Room_ID": row["Room_ID"],
                "Bed_ID": row["Bed_ID"],
                "Admission_Number": row["Admission_Number"],
                "Admission_Date": row["Admission_Date"],
                "Expected_Discharge_Date": row["Expected_Discharge_Date"],
                "Actual_Discharge_Date": row["Actual_Discharge_Date"],
                "Admission_Type": row["Admission_Type"],
                "Admission_Reason": row["Admission_Reason"],
                "Initial_Diagnosis": row["Initial_Diagnosis"],
                "Ward": row["Ward"],
                "Room_Number": row["Room_Number"],
                "Bed_Number": row["Bed_Number"],
                "Current_Status": row["Current_Status"],
                "Length_of_Stay": row["Length_of_Stay"],
                "Is_ICU_Admission": row["Is_ICU_Admission"] or 0,
                "Requires_Surgery": row["Requires_Surgery"] or 0,
                "Is_Emergency": row["Is_Emergency"] or 0,
                "AI_Risk_Level": row["AI_Risk_Level"],
                "Notes": row["Notes"],
            })

        print("\nSOURCE VALIDATION")
        print("-" * 70)
        print(f"Invalid Patient_ID:      {invalid_patient:,}")
        print(f"Invalid Department_ID:   {invalid_department:,}")
        print(f"Invalid Doctor_ID:       {invalid_doctor:,}")
        print(f"Invalid Disease_ID:      {invalid_disease:,}")
        print(f"Valid records prepared:  {len(valid_records):,}")

        # --------------------------------------------------------
        # 7. Clear existing mappings
        # --------------------------------------------------------
        print("\nClearing existing Step 59 mappings...")

        cursor.execute("""
            DELETE FROM patient_admissions_map
        """)

        print(f"Existing mappings removed: {cursor.rowcount:,}")

        # --------------------------------------------------------
        # 8. Insert mappings in batches
        # --------------------------------------------------------
        insert_sql = """
            INSERT INTO patient_admissions_map (
                Admission_Map_ID,
                Patient_ID,
                Admission_ID,
                Department_ID,
                Admitting_Doctor_ID,
                Predicted_Disease_ID,
                Room_ID,
                Bed_ID,
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
                AI_Risk_Level,
                Notes,
                Data_Source,
                Created_By,
                Updated_By
            )
            VALUES (
                UUID(),
                %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s
            )
        """

        inserted = 0

        for start in range(0, len(valid_records), BATCH_SIZE):

            batch = valid_records[start:start + BATCH_SIZE]

            values = [
                (
                    row["Patient_ID"],
                    row["Admission_ID"],
                    row["Department_ID"],
                    row["Admitting_Doctor_ID"],
                    row["Predicted_Disease_ID"],
                    row["Room_ID"],
                    row["Bed_ID"],
                    row["Admission_Number"],
                    row["Admission_Date"],
                    row["Expected_Discharge_Date"],
                    row["Actual_Discharge_Date"],
                    row["Admission_Type"],
                    row["Admission_Reason"],
                    row["Initial_Diagnosis"],
                    row["Ward"],
                    row["Room_Number"],
                    row["Bed_Number"],
                    row["Current_Status"],
                    row["Length_of_Stay"],
                    row["Is_ICU_Admission"],
                    row["Requires_Surgery"],
                    row["Is_Emergency"],
                    row["AI_Risk_Level"],
                    row["Notes"],
                    "Synthetic",
                    SCRIPT_NAME,
                    SCRIPT_NAME
                )
                for row in batch
            ]

            cursor.executemany(insert_sql, values)
            inserted += len(batch)

            print(
                f"Inserted: {inserted:,} / {len(valid_records):,}",
                end="\r"
            )

        conn.commit()

        print()
        print(f"\nInserted mappings: {inserted:,}")

        # ========================================================
        # VALIDATION
        # ========================================================

        print("\n" + "=" * 70)
        print("STEP 59 VALIDATION")
        print("=" * 70)

        # --------------------------------------------------------
        # Total mappings
        # --------------------------------------------------------
        cursor.execute("""
            SELECT COUNT(*) AS Total
            FROM patient_admissions_map
        """)

        total = cursor.fetchone()["Total"]

        print(f"\nExpected mappings: {len(valid_records):,}")
        print(f"Actual mappings:   {total:,}")

        # --------------------------------------------------------
        # Unique patients
        # --------------------------------------------------------
        cursor.execute("""
            SELECT COUNT(DISTINCT Patient_ID) AS Total
            FROM patient_admissions_map
        """)

        unique_patients = cursor.fetchone()["Total"]

        print(f"Unique patients:   {unique_patients:,}")

        # --------------------------------------------------------
        # Unique admissions
        # --------------------------------------------------------
        cursor.execute("""
            SELECT COUNT(DISTINCT Admission_ID) AS Total
            FROM patient_admissions_map
        """)

        unique_admissions = cursor.fetchone()["Total"]

        print(f"Unique admissions:  {unique_admissions:,}")

        # --------------------------------------------------------
        # Unique departments
        # --------------------------------------------------------
        cursor.execute("""
            SELECT COUNT(DISTINCT Department_ID) AS Total
            FROM patient_admissions_map
        """)

        unique_departments = cursor.fetchone()["Total"]

        print(f"Unique departments: {unique_departments:,}")

        # --------------------------------------------------------
        # NULL checks
        # --------------------------------------------------------
        cursor.execute("""
            SELECT
                SUM(Patient_ID IS NULL) AS Null_Patient,
                SUM(Admission_ID IS NULL) AS Null_Admission,
                SUM(Department_ID IS NULL) AS Null_Department,
                SUM(Admitting_Doctor_ID IS NULL) AS Null_Doctor,
                SUM(Admission_Number IS NULL) AS Null_Admission_Number,
                SUM(Admission_Date IS NULL) AS Null_Admission_Date
            FROM patient_admissions_map
        """)

        nulls = cursor.fetchone()

        print("\nNULL CHECKS")
        print("-" * 70)
        print(f"Null Patient_ID:          {nulls['Null_Patient']}")
        print(f"Null Admission_ID:        {nulls['Null_Admission']}")
        print(f"Null Department_ID:       {nulls['Null_Department']}")
        print(f"Null Admitting_Doctor_ID: {nulls['Null_Doctor']}")
        print(f"Null Admission_Number:    {nulls['Null_Admission_Number']}")
        print(f"Null Admission_Date:      {nulls['Null_Admission_Date']}")

        # --------------------------------------------------------
        # Orphan patient links
        # --------------------------------------------------------
        cursor.execute("""
            SELECT COUNT(*) AS Total
            FROM patient_admissions_map pam
            LEFT JOIN patients p
                ON pam.Patient_ID = p.Patient_ID
            WHERE p.Patient_ID IS NULL
        """)

        orphan_patients = cursor.fetchone()["Total"]

        print(f"\nOrphan patients:    {orphan_patients:,}")

        # --------------------------------------------------------
        # Orphan admission links
        # --------------------------------------------------------
        cursor.execute("""
            SELECT COUNT(*) AS Total
            FROM patient_admissions_map pam
            LEFT JOIN admissions a
                ON pam.Admission_ID = a.Admission_ID
            WHERE a.Admission_ID IS NULL
        """)

        orphan_admissions = cursor.fetchone()["Total"]

        print(f"Orphan admissions:  {orphan_admissions:,}")

        # --------------------------------------------------------
        # Orphan departments
        # --------------------------------------------------------
        cursor.execute("""
            SELECT COUNT(*) AS Total
            FROM patient_admissions_map pam
            LEFT JOIN departments d
                ON pam.Department_ID = d.Department_ID
            WHERE d.Department_ID IS NULL
        """)

        orphan_departments = cursor.fetchone()["Total"]

        print(f"Orphan departments: {orphan_departments:,}")

        # --------------------------------------------------------
        # Orphan doctors
        # --------------------------------------------------------
        cursor.execute("""
            SELECT COUNT(*) AS Total
            FROM patient_admissions_map pam
            LEFT JOIN doctors d
                ON pam.Admitting_Doctor_ID = d.Doctor_ID
            WHERE d.Doctor_ID IS NULL
        """)

        orphan_doctors = cursor.fetchone()["Total"]

        print(f"Orphan doctors:     {orphan_doctors:,}")

        # --------------------------------------------------------
        # Admission status distribution
        # --------------------------------------------------------
        print("\nADMISSION STATUS")

        cursor.execute("""
            SELECT
                Current_Status,
                COUNT(*) AS Total
            FROM patient_admissions_map
            GROUP BY Current_Status
            ORDER BY Total DESC
        """)

        for row in cursor.fetchall():
            print(f"{row['Current_Status']}: {row['Total']:,}")

        # --------------------------------------------------------
        # Admission type distribution
        # --------------------------------------------------------
        print("\nADMISSION TYPE")

        cursor.execute("""
            SELECT
                Admission_Type,
                COUNT(*) AS Total
            FROM patient_admissions_map
            GROUP BY Admission_Type
            ORDER BY Total DESC
        """)

        for row in cursor.fetchall():
            print(f"{row['Admission_Type']}: {row['Total']:,}")

        # --------------------------------------------------------
        # Data source
        # --------------------------------------------------------
        print("\nDATA SOURCE")

        cursor.execute("""
            SELECT
                Data_Source,
                COUNT(*) AS Total
            FROM patient_admissions_map
            GROUP BY Data_Source
        """)

        for row in cursor.fetchall():
            print(f"{row['Data_Source']}: {row['Total']:,}")

        # --------------------------------------------------------
        # Final status
        # --------------------------------------------------------
        expected = len(valid_records)

        if (
            total == expected
            and unique_admissions == expected
            and nulls["Null_Patient"] == 0
            and nulls["Null_Admission"] == 0
            and nulls["Null_Department"] == 0
            and nulls["Null_Doctor"] == 0
            and nulls["Null_Admission_Number"] == 0
            and nulls["Null_Admission_Date"] == 0
            and orphan_patients == 0
            and orphan_admissions == 0
            and orphan_departments == 0
            and orphan_doctors == 0
        ):
            print("\n" + "=" * 70)
            print("FINAL STATUS: PASSED")
            print("=" * 70)

        else:
            print("\n" + "=" * 70)
            print("FINAL STATUS: FAILED")
            print("=" * 70)

    except Exception as e:

        conn.rollback()

        print("\nERROR:")
        print(e)

        print("\nTransaction rolled back.")

    finally:

        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()