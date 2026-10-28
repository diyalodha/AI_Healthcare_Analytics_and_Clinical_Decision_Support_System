import csv
import os
import mysql.connector
from decimal import Decimal
from datetime import datetime

CSV_FILE = r"datasets\synthetic\vital_signs.csv"

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": os.environ.get("MYSQL_PASSWORD"),
    "database": "healthcare_ai_db"
}

BATCH_SIZE = 5000


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def main():

    print("=" * 70)
    print("STEP 61A - LOAD VITAL SIGNS")
    print("=" * 70)

    if not DB_CONFIG["password"]:
        print("ERROR: MYSQL_PASSWORD environment variable is not set.")
        print("Run:")
        print('$env:MYSQL_PASSWORD = Read-Host "Enter MySQL root password"')
        return

    if not os.path.exists(CSV_FILE):
        print(f"ERROR: CSV file not found: {CSV_FILE}")
        return

    file_size_mb = os.path.getsize(CSV_FILE) / (1024 * 1024)

    print(f"CSV file: {CSV_FILE}")
    print(f"CSV size: {file_size_mb:.2f} MB")

    conn = get_connection()
    cursor = conn.cursor()

    # ------------------------------------------------------------
    # LOAD VALID PATIENT IDs
    # ------------------------------------------------------------

    cursor.execute("SELECT Patient_ID FROM patients")
    valid_patients = {row[0] for row in cursor.fetchall()}

    print(f"DB patients: {len(valid_patients):,}")

    # ------------------------------------------------------------
    # CHECK EXISTING RECORDS
    # ------------------------------------------------------------

    cursor.execute("SELECT COUNT(*) FROM vital_signs")
    existing_count = cursor.fetchone()[0]

    print(f"Existing vital_signs records: {existing_count:,}")

    # ------------------------------------------------------------
    # REMOVE PREVIOUS TEST LOAD
    # ------------------------------------------------------------

    if existing_count > 0:

        print("\nClearing existing vital_signs records...")

        cursor.execute("DELETE FROM vital_signs")
        conn.commit()

        print("Existing vital_signs records cleared.")

    # ------------------------------------------------------------
    # SOURCE VALIDATION
    # ------------------------------------------------------------

    print("\nReading and validating CSV...")
    print("NOTE: Admission_ID is intentionally NOT used.")
    print("The source Admission_ID relationships do not match")
    print("the currently loaded admissions dataset.")
    print("Doctor_ID and ICU_Stay_ID will therefore remain NULL.")

    total_rows = 0
    valid_rows = 0

    invalid_vital_id = 0
    invalid_patient = 0
    invalid_datetime = 0
    invalid_numeric = 0
    duplicate_vital_id = 0

    normal_count = 0
    critical_count = 0

    seen_vital_ids = set()

    insert_sql = """
        INSERT INTO vital_signs (
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
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s
        )
    """

    batch = []

    with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:

            total_rows += 1

            # ----------------------------------------------------
            # Vital Record ID
            # ----------------------------------------------------

            vital_id = row["Vital_Sign_ID"].strip()

            if not vital_id:
                invalid_vital_id += 1
                continue

            if vital_id in seen_vital_ids:
                duplicate_vital_id += 1
                continue

            seen_vital_ids.add(vital_id)

            # ----------------------------------------------------
            # Patient ID
            # ----------------------------------------------------

            patient_id = row["Patient_ID"].strip()

            if patient_id not in valid_patients:
                invalid_patient += 1
                continue

            # ----------------------------------------------------
            # Recorded DateTime
            # ----------------------------------------------------

            try:
                recorded_datetime = datetime.strptime(
                    row["Recorded_Time"].strip(),
                    "%Y-%m-%d %H:%M:%S.%f"
                )
            except ValueError:

                try:
                    recorded_datetime = datetime.strptime(
                        row["Recorded_Time"].strip(),
                        "%Y-%m-%d %H:%M:%S"
                    )
                except ValueError:
                    invalid_datetime += 1
                    continue

            # ----------------------------------------------------
            # Numeric fields
            # ----------------------------------------------------

            try:
                heart_rate = int(row["Heart_Rate"])
                systolic_bp = int(row["Systolic_BP"])
                diastolic_bp = int(row["Diastolic_BP"])
                temperature = Decimal(row["Temperature"])
                oxygen_saturation = Decimal(row["Oxygen_Saturation"])
                respiratory_rate = int(row["Respiratory_Rate"])
                weight = Decimal(row["Weight"])
                blood_sugar = Decimal(row["Blood_Sugar"])

            except (ValueError, TypeError):
                invalid_numeric += 1
                continue

            # ----------------------------------------------------
            # Basic physiological validation
            # ----------------------------------------------------

            if not (20 <= heart_rate <= 250):
                invalid_numeric += 1
                continue

            if not (50 <= systolic_bp <= 300):
                invalid_numeric += 1
                continue

            if not (20 <= diastolic_bp <= 200):
                invalid_numeric += 1
                continue

            if not (25 <= float(temperature) <= 45):
                invalid_numeric += 1
                continue

            if not (50 <= float(oxygen_saturation) <= 100):
                invalid_numeric += 1
                continue

            if not (5 <= respiratory_rate <= 100):
                invalid_numeric += 1
                continue

            if not (20 <= float(weight) <= 300):
                invalid_numeric += 1
                continue

            if not (20 <= float(blood_sugar) <= 600):
                invalid_numeric += 1
                continue

            # ----------------------------------------------------
            # Oxygen status → AI Risk Level
            # ----------------------------------------------------

            oxygen_status = row["Oxygen_Status"].strip()

            if oxygen_status == "Critical":
                ai_risk_level = "Critical"
                critical_count += 1

            else:
                ai_risk_level = "Low"
                normal_count += 1

            # ----------------------------------------------------
            # Prepare record
            # ----------------------------------------------------
            #
            # IMPORTANT:
            # Doctor_ID = NULL
            # ICU_Stay_ID = NULL
            #
            # We do NOT derive doctor from Admission_ID because
            # the CSV admission relationships are inconsistent.
            #
            # ----------------------------------------------------

            values = (
                vital_id,
                patient_id,
                None,                       # Doctor_ID
                None,                       # ICU_Stay_ID
                recorded_datetime,
                None,                       # Recorded_By
                None,                       # Device_ID
                None,                       # Device_Type
                "Manual",                  # Measurement_Source

                temperature,
                heart_rate,
                respiratory_rate,
                oxygen_saturation,
                systolic_bp,
                diastolic_bp,

                None,                       # MAP
                heart_rate,                # Pulse_Rate

                None,                       # Height
                weight,
                None,                       # BMI
                blood_sugar,

                None,                       # Pain_Score
                None,                       # GCS
                None,                       # BSA

                0,                          # Abnormal_Flag
                ai_risk_level,
                None,                       # Early_Warning_Score
                None,                       # Clinical_Remarks
                None,                       # Notes

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
            # Batch INSERT
            # ----------------------------------------------------

            if len(batch) >= BATCH_SIZE:

                cursor.executemany(insert_sql, batch)
                conn.commit()

                batch.clear()

                if total_rows % 100000 == 0:
                    print(
                        f"Processed: {total_rows:,} | "
                        f"Valid: {valid_rows:,}"
                    )

    # ------------------------------------------------------------
    # INSERT REMAINING BATCH
    # ------------------------------------------------------------

    if batch:
        cursor.executemany(insert_sql, batch)
        conn.commit()
        batch.clear()

    # ------------------------------------------------------------
    # SOURCE VALIDATION RESULTS
    # ------------------------------------------------------------

    print("\n" + "=" * 70)
    print("SOURCE VALIDATION")
    print("=" * 70)

    print(f"Source rows processed:          {total_rows:,}")
    print(f"Valid records prepared:         {valid_rows:,}")
    print(f"Invalid Vital_Record_ID:        {invalid_vital_id:,}")
    print(f"Duplicate Vital_Record_ID:      {duplicate_vital_id:,}")
    print(f"Invalid Patient_ID:              {invalid_patient:,}")
    print(f"Invalid Recorded_DateTime:       {invalid_datetime:,}")
    print(f"Invalid numeric values:          {invalid_numeric:,}")

    print("\nOXYGEN STATUS")
    print(f"Normal:                          {normal_count:,}")
    print(f"Critical:                        {critical_count:,}")

    # ------------------------------------------------------------
    # DATABASE VALIDATION
    # ------------------------------------------------------------

    cursor.execute("SELECT COUNT(*) FROM vital_signs")
    actual_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(DISTINCT Vital_Record_ID)
        FROM vital_signs
    """)
    unique_vital_ids = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(DISTINCT Patient_ID)
        FROM vital_signs
    """)
    unique_patients = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM vital_signs
        WHERE Patient_ID IS NULL
    """)
    null_patients = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM vital_signs
        WHERE Doctor_ID IS NOT NULL
    """)
    doctor_assigned = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM vital_signs
        WHERE ICU_Stay_ID IS NOT NULL
    """)
    icu_assigned = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM vital_signs
        WHERE Temperature_C < 25
           OR Temperature_C > 45
           OR Heart_Rate_BPM < 20
           OR Heart_Rate_BPM > 250
           OR Respiratory_Rate < 5
           OR Respiratory_Rate > 100
           OR Oxygen_Saturation < 50
           OR Oxygen_Saturation > 100
           OR Blood_Pressure_Systolic < 50
           OR Blood_Pressure_Systolic > 300
           OR Blood_Pressure_Diastolic < 20
           OR Blood_Pressure_Diastolic > 200
           OR Weight_kg < 20
           OR Weight_kg > 300
           OR Blood_Glucose < 20
           OR Blood_Glucose > 600
    """)
    invalid_db_ranges = cursor.fetchone()[0]

    cursor.execute("""
        SELECT AI_Risk_Level, COUNT(*)
        FROM vital_signs
        GROUP BY AI_Risk_Level
    """)
    risk_distribution = cursor.fetchall()

    cursor.execute("""
        SELECT Measurement_Source, COUNT(*)
        FROM vital_signs
        GROUP BY Measurement_Source
    """)
    measurement_distribution = cursor.fetchall()

    cursor.execute("""
        SELECT MIN(Recorded_DateTime), MAX(Recorded_DateTime)
        FROM vital_signs
    """)
    date_range = cursor.fetchone()

    # ------------------------------------------------------------
    # DISPLAY DATABASE VALIDATION
    # ------------------------------------------------------------

    print("\n" + "=" * 70)
    print("DATABASE VALIDATION")
    print("=" * 70)

    print(f"Expected records:                {valid_rows:,}")
    print(f"Actual records:                  {actual_count:,}")
    print(f"Unique Vital_Record_ID:          {unique_vital_ids:,}")
    print(f"Unique patients:                 {unique_patients:,}")

    print("\nNULL CHECKS")
    print(f"Patient_ID NULL:                 {null_patients:,}")
    print(f"Doctor_ID assigned:              {doctor_assigned:,}")
    print(f"ICU_Stay_ID assigned:            {icu_assigned:,}")

    print("\nPHYSIOLOGICAL RANGE CHECK")
    print(f"Invalid ranges:                  {invalid_db_ranges:,}")

    print("\nAI RISK LEVEL")
    for risk, count in risk_distribution:
        print(f"{risk}: {count:,}")

    print("\nMEASUREMENT SOURCE")
    for source, count in measurement_distribution:
        print(f"{source}: {count:,}")

    print("\nDATE RANGE")
    print(f"Earliest: {date_range[0]}")
    print(f"Latest:   {date_range[1]}")

    # ------------------------------------------------------------
    # FINAL STATUS
    # ------------------------------------------------------------

    passed = (
        total_rows == 2_000_000
        and valid_rows == 2_000_000
        and invalid_vital_id == 0
        and duplicate_vital_id == 0
        and invalid_patient == 0
        and invalid_datetime == 0
        and invalid_numeric == 0
        and actual_count == 2_000_000
        and unique_vital_ids == 2_000_000
        and null_patients == 0
        and doctor_assigned == 0
        and icu_assigned == 0
        and invalid_db_ranges == 0
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