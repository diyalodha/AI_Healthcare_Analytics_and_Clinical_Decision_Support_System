import os
import sys
import mysql.connector
from mysql.connector import Error

# ============================================================
# STEP 60 — PATIENT DIAGNOSES MAPPING
# ============================================================

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": "healthcare_ai_db",
    "autocommit": False
}

BATCH_SIZE = 5000
SCRIPT_NAME = "60_patient_diagnoses_mapping"


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
    print("STEP 60 — PATIENT DIAGNOSES MAPPING")
    print("=" * 70)

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:

        # --------------------------------------------------------
        # 1. Read diagnoses from database
        # --------------------------------------------------------
        print("\nReading diagnoses from database...")

        cursor.execute("""
            SELECT
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
                Ground_Truth_Verified
            FROM diagnoses
            WHERE Is_Deleted = 0
            ORDER BY Diagnosis_ID
        """)

        diagnoses = cursor.fetchall()

        print(f"Diagnoses read: {len(diagnoses):,}")

        if not diagnoses:
            print("\nERROR: No diagnoses found.")
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
        # 3. Load valid doctor IDs
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
        # 4. Load valid disease IDs
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
        # 5. Load valid admission IDs
        # --------------------------------------------------------
        cursor.execute("""
            SELECT Admission_ID
            FROM admissions
        """)

        valid_admissions = {
            row["Admission_ID"]
            for row in cursor.fetchall()
        }

        print(f"DB admissions: {len(valid_admissions):,}")

        # --------------------------------------------------------
        # 6. Load valid appointment IDs
        # --------------------------------------------------------
        cursor.execute("""
            SELECT Appointment_ID
            FROM appointments
        """)

        valid_appointments = {
            row["Appointment_ID"]
            for row in cursor.fetchall()
        }

        print(f"DB appointments: {len(valid_appointments):,}")

        # --------------------------------------------------------
        # 7. Validate diagnosis records
        # --------------------------------------------------------
        valid_records = []

        invalid_patient = 0
        invalid_doctor = 0
        invalid_disease = 0
        invalid_admission = 0
        invalid_appointment = 0

        for row in diagnoses:

            patient_id = row["Patient_ID"]
            doctor_id = row["Doctor_ID"]
            disease_id = row["Disease_ID"]
            admission_id = row["Admission_ID"]
            appointment_id = row["Appointment_ID"]

            # Mandatory patient
            if patient_id not in valid_patients:
                invalid_patient += 1
                continue

            # Mandatory doctor
            if doctor_id not in valid_doctors:
                invalid_doctor += 1
                continue

            # Mandatory disease
            if disease_id not in valid_diseases:
                invalid_disease += 1
                continue

            # Optional admission
            if admission_id is not None:
                if admission_id not in valid_admissions:
                    invalid_admission += 1
                    admission_id = None

            # Optional appointment
            if appointment_id is not None:
                if appointment_id not in valid_appointments:
                    invalid_appointment += 1
                    appointment_id = None

            valid_records.append({
                "Diagnosis_ID": row["Diagnosis_ID"],
                "Patient_ID": patient_id,
                "Doctor_ID": doctor_id,
                "Disease_ID": disease_id,
                "Appointment_ID": appointment_id,
                "Admission_ID": admission_id,
                "Diagnosis_Number": row["Diagnosis_Number"],
                "Diagnosis_Date": row["Diagnosis_Date"],
                "Chief_Complaint": row["Chief_Complaint"],
                "Symptoms": row["Symptoms"],
                "Clinical_Notes": row["Clinical_Notes"],
                "Severity": row["Severity"],
                "Diagnosis_Status": row["Diagnosis_Status"],
                "Diagnosis_Method": row["Diagnosis_Method"],
                "Stage": row["Stage"],
                "Is_Primary_Diagnosis": row["Is_Primary_Diagnosis"] or 0,
                "Follow_Up_Required": row["Follow_Up_Required"] or 0,
                "Follow_Up_Date": row["Follow_Up_Date"],
                "AI_Prediction_Used": row["AI_Prediction_Used"] or 0,
                "AI_Confidence": row["AI_Confidence"],
                "AI_Model_Name": row["AI_Model_Name"],
                "Ground_Truth_Verified": row["Ground_Truth_Verified"] or 0
            })

        print("\nSOURCE VALIDATION")
        print("-" * 70)
        print(f"Invalid Patient_ID:       {invalid_patient:,}")
        print(f"Invalid Doctor_ID:        {invalid_doctor:,}")
        print(f"Invalid Disease_ID:       {invalid_disease:,}")
        print(f"Invalid Admission_ID:     {invalid_admission:,}")
        print(f"Invalid Appointment_ID:   {invalid_appointment:,}")
        print(f"Valid records prepared:   {len(valid_records):,}")

        # --------------------------------------------------------
        # 8. Clear existing mappings
        # --------------------------------------------------------
        print("\nClearing existing Step 60 mappings...")

        cursor.execute("""
            DELETE FROM patient_diagnoses_map
        """)

        print(f"Existing mappings removed: {cursor.rowcount:,}")

        # --------------------------------------------------------
        # 9. Insert mappings in batches
        # --------------------------------------------------------
        insert_sql = """
            INSERT INTO patient_diagnoses_map (
                Diagnosis_Map_ID,
                Patient_ID,
                Diagnosis_ID,
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
                Data_Source,
                Created_By,
                Updated_By
            )
            VALUES (
                UUID(),
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s,
                1, 0, 1, 'Synthetic', %s, %s
            )
        """

        inserted = 0

        for start in range(0, len(valid_records), BATCH_SIZE):

            batch = valid_records[start:start + BATCH_SIZE]

            values = [
                (
                    row["Patient_ID"],
                    row["Diagnosis_ID"],
                    row["Doctor_ID"],
                    row["Disease_ID"],
                    row["Appointment_ID"],
                    row["Admission_ID"],
                    row["Diagnosis_Number"],
                    row["Diagnosis_Date"],
                    row["Chief_Complaint"],
                    row["Symptoms"],
                    row["Clinical_Notes"],
                    row["Severity"],
                    row["Diagnosis_Status"],
                    row["Diagnosis_Method"],
                    row["Stage"],
                    row["Is_Primary_Diagnosis"],
                    row["Follow_Up_Required"],
                    row["Follow_Up_Date"],
                    row["AI_Prediction_Used"],
                    row["AI_Confidence"],
                    row["AI_Model_Name"],
                    row["Ground_Truth_Verified"],
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
        print("STEP 60 VALIDATION")
        print("=" * 70)

        # --------------------------------------------------------
        # Total mappings
        # --------------------------------------------------------
        cursor.execute("""
            SELECT COUNT(*) AS Total
            FROM patient_diagnoses_map
        """)

        total = cursor.fetchone()["Total"]

        print(f"\nExpected mappings: {len(valid_records):,}")
        print(f"Actual mappings:   {total:,}")

        # --------------------------------------------------------
        # Unique patients
        # --------------------------------------------------------
        cursor.execute("""
            SELECT COUNT(DISTINCT Patient_ID) AS Total
            FROM patient_diagnoses_map
        """)

        unique_patients = cursor.fetchone()["Total"]

        print(f"Unique patients:   {unique_patients:,}")

        # --------------------------------------------------------
        # Unique diagnoses
        # --------------------------------------------------------
        cursor.execute("""
            SELECT COUNT(DISTINCT Diagnosis_ID) AS Total
            FROM patient_diagnoses_map
        """)

        unique_diagnoses = cursor.fetchone()["Total"]

        print(f"Unique diagnoses:  {unique_diagnoses:,}")

        # --------------------------------------------------------
        # Unique diseases
        # --------------------------------------------------------
        cursor.execute("""
            SELECT COUNT(DISTINCT Disease_ID) AS Total
            FROM patient_diagnoses_map
        """)

        unique_diseases = cursor.fetchone()["Total"]

        print(f"Unique diseases:   {unique_diseases:,}")

        # --------------------------------------------------------
        # NULL checks
        # --------------------------------------------------------
        cursor.execute("""
            SELECT
                SUM(Patient_ID IS NULL) AS Null_Patient,
                SUM(Diagnosis_ID IS NULL) AS Null_Diagnosis,
                SUM(Doctor_ID IS NULL) AS Null_Doctor,
                SUM(Disease_ID IS NULL) AS Null_Disease,
                SUM(Diagnosis_Number IS NULL) AS Null_Diagnosis_Number,
                SUM(Diagnosis_Date IS NULL) AS Null_Diagnosis_Date
            FROM patient_diagnoses_map
        """)

        nulls = cursor.fetchone()

        print("\nNULL CHECKS")
        print("-" * 70)
        print(f"Null Patient_ID:       {nulls['Null_Patient']}")
        print(f"Null Diagnosis_ID:     {nulls['Null_Diagnosis']}")
        print(f"Null Doctor_ID:        {nulls['Null_Doctor']}")
        print(f"Null Disease_ID:       {nulls['Null_Disease']}")
        print(f"Null Diagnosis_Number: {nulls['Null_Diagnosis_Number']}")
        print(f"Null Diagnosis_Date:   {nulls['Null_Diagnosis_Date']}")

        # --------------------------------------------------------
        # Orphan patient links
        # --------------------------------------------------------
        cursor.execute("""
            SELECT COUNT(*) AS Total
            FROM patient_diagnoses_map pdm
            LEFT JOIN patients p
                ON pdm.Patient_ID = p.Patient_ID
            WHERE p.Patient_ID IS NULL
        """)

        orphan_patients = cursor.fetchone()["Total"]

        print(f"\nOrphan patients:   {orphan_patients:,}")

        # --------------------------------------------------------
        # Orphan diagnosis links
        # --------------------------------------------------------
        cursor.execute("""
            SELECT COUNT(*) AS Total
            FROM patient_diagnoses_map pdm
            LEFT JOIN diagnoses d
                ON pdm.Diagnosis_ID = d.Diagnosis_ID
            WHERE d.Diagnosis_ID IS NULL
        """)

        orphan_diagnoses = cursor.fetchone()["Total"]

        print(f"Orphan diagnoses:  {orphan_diagnoses:,}")

        # --------------------------------------------------------
        # Orphan doctors
        # --------------------------------------------------------
        cursor.execute("""
            SELECT COUNT(*) AS Total
            FROM patient_diagnoses_map pdm
            LEFT JOIN doctors d
                ON pdm.Doctor_ID = d.Doctor_ID
            WHERE d.Doctor_ID IS NULL
        """)

        orphan_doctors = cursor.fetchone()["Total"]

        print(f"Orphan doctors:    {orphan_doctors:,}")

        # --------------------------------------------------------
        # Orphan diseases
        # --------------------------------------------------------
        cursor.execute("""
            SELECT COUNT(*) AS Total
            FROM patient_diagnoses_map pdm
            LEFT JOIN diseases d
                ON pdm.Disease_ID = d.Disease_ID
            WHERE d.Disease_ID IS NULL
        """)

        orphan_diseases = cursor.fetchone()["Total"]

        print(f"Orphan diseases:   {orphan_diseases:,}")

        # --------------------------------------------------------
        # Orphan admission links
        # --------------------------------------------------------
        cursor.execute("""
            SELECT COUNT(*) AS Total
            FROM patient_diagnoses_map pdm
            LEFT JOIN admissions a
                ON pdm.Admission_ID = a.Admission_ID
            WHERE pdm.Admission_ID IS NOT NULL
              AND a.Admission_ID IS NULL
        """)

        orphan_admissions = cursor.fetchone()["Total"]

        print(f"Orphan admissions: {orphan_admissions:,}")

        # --------------------------------------------------------
        # Diagnosis status
        # --------------------------------------------------------
        print("\nDIAGNOSIS STATUS")

        cursor.execute("""
            SELECT
                Diagnosis_Status,
                COUNT(*) AS Total
            FROM patient_diagnoses_map
            GROUP BY Diagnosis_Status
            ORDER BY Total DESC
        """)

        for row in cursor.fetchall():
            print(
                f"{row['Diagnosis_Status']}: "
                f"{row['Total']:,}"
            )

        # --------------------------------------------------------
        # Diagnosis severity
        # --------------------------------------------------------
        print("\nDIAGNOSIS SEVERITY")

        cursor.execute("""
            SELECT
                Severity,
                COUNT(*) AS Total
            FROM patient_diagnoses_map
            GROUP BY Severity
            ORDER BY Total DESC
        """)

        for row in cursor.fetchall():
            print(
                f"{row['Severity']}: "
                f"{row['Total']:,}"
            )

        # --------------------------------------------------------
        # Diagnosis method
        # --------------------------------------------------------
        print("\nDIAGNOSIS METHOD")

        cursor.execute("""
            SELECT
                Diagnosis_Method,
                COUNT(*) AS Total
            FROM patient_diagnoses_map
            GROUP BY Diagnosis_Method
            ORDER BY Total DESC
        """)

        for row in cursor.fetchall():
            print(
                f"{row['Diagnosis_Method']}: "
                f"{row['Total']:,}"
            )

        # --------------------------------------------------------
        # Admission linkage
        # --------------------------------------------------------
        cursor.execute("""
            SELECT
                SUM(Admission_ID IS NOT NULL) AS Linked,
                SUM(Admission_ID IS NULL) AS Not_Linked
            FROM patient_diagnoses_map
        """)

        admission_linkage = cursor.fetchone()

        print("\nADMISSION LINKAGE")
        print("-" * 70)
        print(
            f"Linked to admission:     "
            f"{admission_linkage['Linked']:,}"
        )
        print(
            f"Without admission link:  "
            f"{admission_linkage['Not_Linked']:,}"
        )

        # --------------------------------------------------------
        # Data source
        # --------------------------------------------------------
        print("\nDATA SOURCE")

        cursor.execute("""
            SELECT
                Data_Source,
                COUNT(*) AS Total
            FROM patient_diagnoses_map
            GROUP BY Data_Source
        """)

        for row in cursor.fetchall():
            print(
                f"{row['Data_Source']}: "
                f"{row['Total']:,}"
            )

        # --------------------------------------------------------
        # Final status
        # --------------------------------------------------------
        expected = len(valid_records)

        if (
            total == expected
            and unique_diagnoses == expected
            and nulls["Null_Patient"] == 0
            and nulls["Null_Diagnosis"] == 0
            and nulls["Null_Doctor"] == 0
            and nulls["Null_Disease"] == 0
            and nulls["Null_Diagnosis_Number"] == 0
            and nulls["Null_Diagnosis_Date"] == 0
            and orphan_patients == 0
            and orphan_diagnoses == 0
            and orphan_doctors == 0
            and orphan_diseases == 0
            and orphan_admissions == 0
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