import os
import sys
import uuid
from decimal import Decimal

import mysql.connector
from mysql.connector import Error


# ============================================================
# CONFIGURATION
# ============================================================

DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_NAME = "healthcare_ai_db"

BATCH_SIZE = 5000

SCRIPT_NAME = "61_patient_vital_signs_mapping.py"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_db_connection():
    password = os.environ.get("MYSQL_PASSWORD")

    if not password:
        print("ERROR: MYSQL_PASSWORD environment variable is not set.")
        print()
        print("In PowerShell, run:")
        print('$env:MYSQL_PASSWORD = Read-Host "Enter MySQL root password"')
        sys.exit(1)

    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=password,
            database=DB_NAME,
            autocommit=False
        )

        return connection

    except Error as e:
        print(f"ERROR: Could not connect to MySQL: {e}")
        sys.exit(1)


# ============================================================
# SAFE VALUE HELPERS
# ============================================================

def clean_value(value):
    """
    Convert pandas/DB values to values accepted by MySQL.
    """
    if value is None:
        return None

    return value


def normalize_enum(value, allowed_values, default_value):
    """
    Keep enum values valid for the target table.
    """
    if value is None:
        return default_value

    value = str(value).strip()

    if value in allowed_values:
        return value

    return default_value


# ============================================================
# MAIN MAPPING
# ============================================================

def main():

    print("=" * 75)
    print("STEP 61 - PATIENT VITAL SIGNS MAPPING")
    print("=" * 75)

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:

        # --------------------------------------------------------
        # 1. Read source count
        # --------------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM vital_signs
        """)

        source_count = cursor.fetchone()["total"]

        print(f"Source vital sign records: {source_count:,}")

        if source_count == 0:
            print()
            print("ERROR: vital_signs table is empty.")
            print("Load/validate vital signs before running Step 61.")
            return

        # --------------------------------------------------------
        # 2. Check source duplicate Vital_Record_ID
        # --------------------------------------------------------

        cursor.execute("""
            SELECT
                Vital_Record_ID,
                COUNT(*) AS Duplicate_Count
            FROM vital_signs
            GROUP BY Vital_Record_ID
            HAVING COUNT(*) > 1
            LIMIT 10
        """)

        source_duplicates = cursor.fetchall()

        print(
            f"Source duplicate Vital_Record_ID groups: "
            f"{len(source_duplicates):,}"
        )

        if source_duplicates:
            print()
            print("ERROR: Duplicate Vital_Record_ID values exist in source.")
            print("Mapping cannot safely continue because target requires")
            print("Vital_Record_ID to be UNIQUE.")
            return

        # --------------------------------------------------------
        # 3. Load valid patient IDs
        # --------------------------------------------------------

        cursor.execute("""
            SELECT Patient_ID
            FROM patients
        """)

        valid_patient_ids = {
            row["Patient_ID"]
            for row in cursor.fetchall()
        }

        print(f"DB patients: {len(valid_patient_ids):,}")

        # --------------------------------------------------------
        # 4. Load valid doctor IDs
        # --------------------------------------------------------

        cursor.execute("""
            SELECT Doctor_ID
            FROM doctors
        """)

        valid_doctor_ids = {
            row["Doctor_ID"]
            for row in cursor.fetchall()
        }

        print(f"DB doctors: {len(valid_doctor_ids):,}")

        # --------------------------------------------------------
        # 5. Load valid ICU stay IDs
        # --------------------------------------------------------

        cursor.execute("""
            SELECT ICU_Stay_ID
            FROM icu_stay_details
        """)

        valid_icu_stay_ids = {
            row["ICU_Stay_ID"]
            for row in cursor.fetchall()
        }

        print(f"DB ICU stays: {len(valid_icu_stay_ids):,}")

        # --------------------------------------------------------
        # 6. Validate source records
        # --------------------------------------------------------

        print()
        print("Validating source records...")

        cursor.execute("""
            SELECT
                Vital_Record_ID,
                Patient_ID,
                Doctor_ID,
                ICU_Stay_ID,
                Recorded_DateTime,
                Recorded_By,
                Device_ID,
                Device_Type,
                Measurement_Source,
                Temperature_C,
                Heart_Rate_BPM,
                Respiratory_Rate,
                Oxygen_Saturation,
                Blood_Pressure_Systolic,
                Blood_Pressure_Diastolic,
                Mean_Arterial_Pressure,
                Pulse_Rate,
                Height_cm,
                Weight_kg,
                BMI,
                Blood_Glucose,
                Pain_Score,
                Glasgow_Coma_Scale,
                Body_Surface_Area,
                Abnormal_Flag,
                AI_Risk_Level,
                Early_Warning_Score,
                Clinical_Remarks,
                Notes,
                Data_Source,
                Is_Active,
                Is_Deleted,
                Record_Version,
                Created_By,
                Updated_By
            FROM vital_signs
            ORDER BY Vital_Record_ID
        """)

        valid_records = []

        invalid_patient = 0
        invalid_doctor = 0
        invalid_icu_stay = 0
        invalid_datetime = 0
        invalid_measurement_source = 0
        invalid_ai_risk = 0

        total_rows = 0

        allowed_measurement_sources = {
            "Manual",
            "Monitor",
            "Wearable Device",
            "ICU Monitor"
        }

        allowed_ai_risk_levels = {
            "Low",
            "Medium",
            "High",
            "Critical"
        }

        while True:

            rows = cursor.fetchmany(BATCH_SIZE)

            if not rows:
                break

            for row in rows:

                total_rows += 1

                vital_id = row["Vital_Record_ID"]
                patient_id = row["Patient_ID"]
                doctor_id = row["Doctor_ID"]
                icu_stay_id = row["ICU_Stay_ID"]
                recorded_datetime = row["Recorded_DateTime"]

                # Required source fields
                if not vital_id or not patient_id:
                    continue

                # Patient validation
                if patient_id not in valid_patient_ids:
                    invalid_patient += 1
                    continue

                # Doctor is nullable in target
                if doctor_id is not None:
                    if doctor_id not in valid_doctor_ids:
                        invalid_doctor += 1
                        doctor_id = None

                # ICU stay is nullable in target
                if icu_stay_id is not None:
                    if icu_stay_id not in valid_icu_stay_ids:
                        invalid_icu_stay += 1
                        icu_stay_id = None

                # Recorded_DateTime is required
                if recorded_datetime is None:
                    invalid_datetime += 1
                    continue

                # Measurement source
                measurement_source = normalize_enum(
                    row["Measurement_Source"],
                    allowed_measurement_sources,
                    "Manual"
                )

                if (
                    row["Measurement_Source"] is not None
                    and str(row["Measurement_Source"]).strip()
                    not in allowed_measurement_sources
                ):
                    invalid_measurement_source += 1

                # AI risk
                ai_risk_level = normalize_enum(
                    row["AI_Risk_Level"],
                    allowed_ai_risk_levels,
                    "Low"
                )

                if (
                    row["AI_Risk_Level"] is not None
                    and str(row["AI_Risk_Level"]).strip()
                    not in allowed_ai_risk_levels
                ):
                    invalid_ai_risk += 1

                valid_records.append(
                    (
                        patient_id,
                        vital_id,
                        doctor_id,
                        icu_stay_id,
                        recorded_datetime,
                        row["Recorded_By"],
                        row["Device_ID"],
                        row["Device_Type"],
                        measurement_source,
                        row["Temperature_C"],
                        row["Heart_Rate_BPM"],
                        row["Respiratory_Rate"],
                        row["Oxygen_Saturation"],
                        row["Blood_Pressure_Systolic"],
                        row["Blood_Pressure_Diastolic"],
                        row["Mean_Arterial_Pressure"],
                        row["Pulse_Rate"],
                        row["Height_cm"],
                        row["Weight_kg"],
                        row["BMI"],
                        row["Blood_Glucose"],
                        row["Pain_Score"],
                        row["Glasgow_Coma_Scale"],
                        row["Body_Surface_Area"],
                        row["Abnormal_Flag"]
                        if row["Abnormal_Flag"] is not None
                        else 0,
                        ai_risk_level,
                        row["Early_Warning_Score"],
                        row["Clinical_Remarks"],
                        row["Notes"],
                        "Synthetic",
                        row["Is_Active"]
                        if row["Is_Active"] is not None
                        else 1,
                        row["Is_Deleted"]
                        if row["Is_Deleted"] is not None
                        else 0,
                        row["Record_Version"]
                        if row["Record_Version"] is not None
                        else 1,
                        SCRIPT_NAME,
                        SCRIPT_NAME
                    )
                )

        print()
        print("SOURCE VALIDATION")
        print("-" * 75)
        print(f"Source rows processed:        {total_rows:,}")
        print(f"Valid records prepared:       {len(valid_records):,}")
        print(f"Invalid Patient_ID:           {invalid_patient:,}")
        print(f"Invalid Doctor_ID:            {invalid_doctor:,}")
        print(f"Invalid ICU_Stay_ID:          {invalid_icu_stay:,}")
        print(f"Invalid Recorded_DateTime:    {invalid_datetime:,}")
        print(f"Invalid Measurement_Source:   {invalid_measurement_source:,}")
        print(f"Invalid AI_Risk_Level:        {invalid_ai_risk:,}")

        # --------------------------------------------------------
        # 7. Clear existing mappings
        # --------------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM patient_vital_signs_map
        """)

        existing_count = cursor.fetchone()["total"]

        print()
        print(f"Existing Step 61 mappings: {existing_count:,}")

        if existing_count > 0:
            print("Removing existing Step 61 mappings...")

            cursor.execute("""
                DELETE FROM patient_vital_signs_map
            """)

            print(
                f"Existing mappings removed: "
                f"{cursor.rowcount:,}"
            )

        # --------------------------------------------------------
        # 8. Insert mappings
        # --------------------------------------------------------

        insert_sql = """
            INSERT INTO patient_vital_signs_map
            (
                Patient_ID,
                Vital_Record_ID,
                Doctor_ID,
                ICU_Stay_ID,
                Recorded_DateTime,
                Recorded_By,
                Device_ID,
                Device_Type,
                Measurement_Source,
                Temperature_C,
                Heart_Rate_BPM,
                Respiratory_Rate,
                Oxygen_Saturation,
                Blood_Pressure_Systolic,
                Blood_Pressure_Diastolic,
                Mean_Arterial_Pressure,
                Pulse_Rate,
                Height_cm,
                Weight_kg,
                BMI,
                Blood_Glucose,
                Pain_Score,
                Glasgow_Coma_Scale,
                Body_Surface_Area,
                Abnormal_Flag,
                AI_Risk_Level,
                Early_Warning_Score,
                Clinical_Remarks,
                Notes,
                Data_Source,
                Is_Active,
                Is_Deleted,
                Record_Version,
                Created_By,
                Updated_By
            )
            VALUES
            (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s
            )
        """

        inserted = 0

        print()
        print("Inserting mappings...")

        for start in range(0, len(valid_records), BATCH_SIZE):

            batch = valid_records[
                start:start + BATCH_SIZE
            ]

            cursor.executemany(insert_sql, batch)

            inserted += cursor.rowcount

            if inserted % 100000 == 0 or inserted == len(valid_records):
                print(
                    f"Inserted: {inserted:,} / "
                    f"{len(valid_records):,}"
                )

        connection.commit()

        print()
        print("=" * 75)
        print("INSERTION COMPLETE")
        print("=" * 75)

        # --------------------------------------------------------
        # 9. Validation - total
        # --------------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM patient_vital_signs_map
        """)

        actual_count = cursor.fetchone()["total"]

        print()
        print("STEP 61 VALIDATION")
        print("-" * 75)
        print(f"Expected records: {len(valid_records):,}")
        print(f"Actual records:   {actual_count:,}")

        # --------------------------------------------------------
        # 10. Unique patients
        # --------------------------------------------------------

        cursor.execute("""
            SELECT COUNT(DISTINCT Patient_ID) AS total
            FROM patient_vital_signs_map
        """)

        unique_patients = cursor.fetchone()["total"]

        print(f"Unique patients:  {unique_patients:,}")

        # --------------------------------------------------------
        # 11. Unique vital records
        # --------------------------------------------------------

        cursor.execute("""
            SELECT COUNT(DISTINCT Vital_Record_ID) AS total
            FROM patient_vital_signs_map
        """)

        unique_vital_records = cursor.fetchone()["total"]

        print(
            f"Unique vital records: "
            f"{unique_vital_records:,}"
        )

        # --------------------------------------------------------
        # 12. NULL checks
        # --------------------------------------------------------

        cursor.execute("""
            SELECT
                SUM(Patient_ID IS NULL) AS Null_Patient,
                SUM(Vital_Record_ID IS NULL) AS Null_Vital_Record,
                SUM(Recorded_DateTime IS NULL) AS Null_DateTime,
                SUM(Measurement_Source IS NULL) AS Null_Source,
                SUM(AI_Risk_Level IS NULL) AS Null_Risk,
                SUM(Data_Source IS NULL) AS Null_Data_Source
            FROM patient_vital_signs_map
        """)

        nulls = cursor.fetchone()

        print()
        print("NULL CHECKS")
        print("-" * 75)
        print(f"Patient_ID NULL:          {nulls['Null_Patient']:,}")
        print(f"Vital_Record_ID NULL:     {nulls['Null_Vital_Record']:,}")
        print(f"Recorded_DateTime NULL:   {nulls['Null_DateTime']:,}")
        print(f"Measurement_Source NULL:  {nulls['Null_Source']:,}")
        print(f"AI_Risk_Level NULL:       {nulls['Null_Risk']:,}")
        print(f"Data_Source NULL:         {nulls['Null_Data_Source']:,}")

        # --------------------------------------------------------
        # 13. Orphan patient validation
        # --------------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM patient_vital_signs_map pvm
            LEFT JOIN patients p
                ON pvm.Patient_ID = p.Patient_ID
            WHERE p.Patient_ID IS NULL
        """)

        orphan_patients = cursor.fetchone()["total"]

        # --------------------------------------------------------
        # 14. Orphan doctor validation
        # --------------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM patient_vital_signs_map pvm
            LEFT JOIN doctors d
                ON pvm.Doctor_ID = d.Doctor_ID
            WHERE pvm.Doctor_ID IS NOT NULL
              AND d.Doctor_ID IS NULL
        """)

        orphan_doctors = cursor.fetchone()["total"]

        # --------------------------------------------------------
        # 15. Orphan ICU stay validation
        # --------------------------------------------------------

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM patient_vital_signs_map pvm
            LEFT JOIN icu_stay_details i
                ON pvm.ICU_Stay_ID = i.ICU_Stay_ID
            WHERE pvm.ICU_Stay_ID IS NOT NULL
              AND i.ICU_Stay_ID IS NULL
        """)

        orphan_icu_stays = cursor.fetchone()["total"]

        print()
        print("ORPHAN CHECKS")
        print("-" * 75)
        print(f"Orphan patients:    {orphan_patients:,}")
        print(f"Orphan doctors:     {orphan_doctors:,}")
        print(f"Orphan ICU stays:   {orphan_icu_stays:,}")

        # --------------------------------------------------------
        # 16. Vital measurement validation
        # --------------------------------------------------------

        cursor.execute("""
            SELECT
                SUM(
                    Temperature_C IS NOT NULL
                    AND (
                        Temperature_C < 25
                        OR Temperature_C > 45
                    )
                ) AS Invalid_Temperature,

                SUM(
                    Heart_Rate_BPM IS NOT NULL
                    AND (
                        Heart_Rate_BPM < 20
                        OR Heart_Rate_BPM > 250
                    )
                ) AS Invalid_Heart_Rate,

                SUM(
                    Respiratory_Rate IS NOT NULL
                    AND (
                        Respiratory_Rate < 5
                        OR Respiratory_Rate > 80
                    )
                ) AS Invalid_Respiratory_Rate,

                SUM(
                    Oxygen_Saturation IS NOT NULL
                    AND (
                        Oxygen_Saturation < 50
                        OR Oxygen_Saturation > 100
                    )
                ) AS Invalid_Oxygen_Saturation,

                SUM(
                    Blood_Pressure_Systolic IS NOT NULL
                    AND (
                        Blood_Pressure_Systolic < 40
                        OR Blood_Pressure_Systolic > 300
                    )
                ) AS Invalid_Systolic,

                SUM(
                    Blood_Pressure_Diastolic IS NOT NULL
                    AND (
                        Blood_Pressure_Diastolic < 20
                        OR Blood_Pressure_Diastolic > 200
                    )
                ) AS Invalid_Diastolic,

                SUM(
                    Pulse_Rate IS NOT NULL
                    AND (
                        Pulse_Rate < 20
                        OR Pulse_Rate > 250
                    )
                ) AS Invalid_Pulse,

                SUM(
                    BMI IS NOT NULL
                    AND (
                        BMI < 5
                        OR BMI > 100
                    )
                ) AS Invalid_BMI

            FROM patient_vital_signs_map
        """)

        measurement_validation = cursor.fetchone()

        print()
        print("PHYSIOLOGICAL RANGE CHECKS")
        print("-" * 75)
        print(
            f"Invalid Temperature:       "
            f"{measurement_validation['Invalid_Temperature']:,}"
        )
        print(
            f"Invalid Heart Rate:        "
            f"{measurement_validation['Invalid_Heart_Rate']:,}"
        )
        print(
            f"Invalid Respiratory Rate:  "
            f"{measurement_validation['Invalid_Respiratory_Rate']:,}"
        )
        print(
            f"Invalid Oxygen Saturation:  "
            f"{measurement_validation['Invalid_Oxygen_Saturation']:,}"
        )
        print(
            f"Invalid Systolic BP:        "
            f"{measurement_validation['Invalid_Systolic']:,}"
        )
        print(
            f"Invalid Diastolic BP:       "
            f"{measurement_validation['Invalid_Diastolic']:,}"
        )
        print(
            f"Invalid Pulse Rate:         "
            f"{measurement_validation['Invalid_Pulse']:,}"
        )
        print(
            f"Invalid BMI:                "
            f"{measurement_validation['Invalid_BMI']:,}"
        )

        # --------------------------------------------------------
        # 17. Measurement source distribution
        # --------------------------------------------------------

        cursor.execute("""
            SELECT
                Measurement_Source,
                COUNT(*) AS Record_Count
            FROM patient_vital_signs_map
            GROUP BY Measurement_Source
            ORDER BY Record_Count DESC
        """)

        source_distribution = cursor.fetchall()

        print()
        print("MEASUREMENT SOURCE")
        print("-" * 75)

        for row in source_distribution:
            print(
                f"{row['Measurement_Source']}: "
                f"{row['Record_Count']:,}"
            )

        # --------------------------------------------------------
        # 18. AI Risk distribution
        # --------------------------------------------------------

        cursor.execute("""
            SELECT
                AI_Risk_Level,
                COUNT(*) AS Record_Count
            FROM patient_vital_signs_map
            GROUP BY AI_Risk_Level
            ORDER BY Record_Count DESC
        """)

        risk_distribution = cursor.fetchall()

        print()
        print("AI RISK LEVEL")
        print("-" * 75)

        for row in risk_distribution:
            print(
                f"{row['AI_Risk_Level']}: "
                f"{row['Record_Count']:,}"
            )

        # --------------------------------------------------------
        # 19. Data source validation
        # --------------------------------------------------------

        cursor.execute("""
            SELECT
                Data_Source,
                COUNT(*) AS Record_Count
            FROM patient_vital_signs_map
            GROUP BY Data_Source
        """)

        data_sources = cursor.fetchall()

        print()
        print("DATA SOURCE")
        print("-" * 75)

        for row in data_sources:
            print(
                f"{row['Data_Source']}: "
                f"{row['Record_Count']:,}"
            )

        # --------------------------------------------------------
        # 20. Doctor linkage
        # --------------------------------------------------------

        cursor.execute("""
            SELECT
                SUM(Doctor_ID IS NOT NULL) AS Doctor_Assigned,
                SUM(Doctor_ID IS NULL) AS Doctor_NULL
            FROM patient_vital_signs_map
        """)

        doctor_linkage = cursor.fetchone()

        print()
        print("DOCTOR LINKAGE")
        print("-" * 75)
        print(
            f"Doctor ID assigned: "
            f"{doctor_linkage['Doctor_Assigned']:,}"
        )
        print(
            f"Doctor ID NULL:     "
            f"{doctor_linkage['Doctor_NULL']:,}"
        )

        # --------------------------------------------------------
        # 21. ICU linkage
        # --------------------------------------------------------

        cursor.execute("""
            SELECT
                SUM(ICU_Stay_ID IS NOT NULL) AS ICU_Linked,
                SUM(ICU_Stay_ID IS NULL) AS ICU_NULL
            FROM patient_vital_signs_map
        """)

        icu_linkage = cursor.fetchone()

        print()
        print("ICU STAY LINKAGE")
        print("-" * 75)
        print(
            f"ICU Stay linked: "
            f"{icu_linkage['ICU_Linked']:,}"
        )
        print(
            f"ICU Stay NULL:   "
            f"{icu_linkage['ICU_NULL']:,}"
        )

        # --------------------------------------------------------
        # 22. Final status
        # --------------------------------------------------------

        range_errors = sum(
            int(value or 0)
            for value in measurement_validation.values()
        )

        null_errors = sum(
            int(value or 0)
            for value in nulls.values()
        )

        passed = (
            actual_count == len(valid_records)
            and unique_vital_records == actual_count
            and null_errors == 0
            and orphan_patients == 0
            and orphan_doctors == 0
            and orphan_icu_stays == 0
            and range_errors == 0
        )

        print()
        print("=" * 75)

        if passed:
            print("FINAL STATUS: PASSED")
        else:
            print("FINAL STATUS: FAILED")

        print("=" * 75)

    except Exception as e:

        connection.rollback()

        print()
        print("=" * 75)
        print("ERROR - TRANSACTION ROLLED BACK")
        print("=" * 75)
        print(str(e))

        raise

    finally:

        cursor.close()
        connection.close()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()