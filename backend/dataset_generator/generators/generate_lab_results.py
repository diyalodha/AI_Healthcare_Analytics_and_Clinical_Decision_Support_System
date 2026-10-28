
import os
import sys
import random
import numpy as np
import pandas as pd
import mysql.connector

# ============================================================
# PATH SETUP
# ============================================================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)

if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

import config
from utils import generate_uuid, save_dataframe, show_progress


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")

MYSQL_DATABASE = "healthcare_ai_db"


# ============================================================
# LAB TEST DEFINITIONS
# ============================================================

LAB_TESTS = [
    {
        "name": "Blood Glucose",
        "unit": "mg/dL",
        "normal": (70, 120),
        "critical": 250
    },
    {
        "name": "Hemoglobin",
        "unit": "g/dL",
        "normal": (12, 17),
        "critical": 8
    },
    {
        "name": "Creatinine",
        "unit": "mg/dL",
        "normal": (0.6, 1.3),
        "critical": 3
    },
    {
        "name": "Urea",
        "unit": "mg/dL",
        "normal": (15, 45),
        "critical": 100
    },
    {
        "name": "WBC Count",
        "unit": "cells/uL",
        "normal": (4000, 11000),
        "critical": 30000
    },
    {
        "name": "Platelet Count",
        "unit": "cells/uL",
        "normal": (150000, 450000),
        "critical": 50000
    },
    {
        "name": "Cholesterol",
        "unit": "mg/dL",
        "normal": (120, 200),
        "critical": 300
    },
    {
        "name": "ALT",
        "unit": "U/L",
        "normal": (7, 56),
        "critical": 200
    }
]


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_mysql_connection():

    if not MYSQL_PASSWORD:
        raise RuntimeError(
            "MYSQL_PASSWORD environment variable is not set."
        )

    return mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )


# ============================================================
# LOAD DATABASE ADMISSIONS
# ============================================================

def load_database_admissions():

    print()
    print("=" * 60)
    print("LOADING ADMISSIONS FROM MYSQL DATABASE")
    print("=" * 60)

    connection = get_mysql_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                Admission_ID,
                Patient_ID,
                Admitting_Doctor_ID
            FROM admissions
            WHERE Admission_ID IS NOT NULL
              AND Patient_ID IS NOT NULL
              AND Admitting_Doctor_ID IS NOT NULL
            """
        )

        rows = cursor.fetchall()
        cursor.close()

    finally:
        connection.close()

    if not rows:
        raise ValueError(
            "No valid admissions found in healthcare_ai_db."
        )

    print(f"Admissions loaded from MySQL: {len(rows):,}")

    # Validate duplicate Admission_ID values.
    admission_ids = [
        row["Admission_ID"] for row in rows
    ]

    if len(admission_ids) != len(set(admission_ids)):
        raise ValueError(
            "Duplicate Admission_ID values found in "
            "MySQL admissions table."
        )

    # Convert database field names to generator field names.
    admission_records = []

    for row in rows:
        admission_records.append({
            "Admission_ID": row["Admission_ID"],
            "Patient_ID": row["Patient_ID"],
            "Doctor_ID": row["Admitting_Doctor_ID"]
        })

    return admission_records


# ============================================================
# GENERATE LABORATORY RESULT VALUE AND STATUS
# ============================================================

def generate_lab_value(lab):

    low, high = lab["normal"]
    critical = lab["critical"]

    # Validate the configured critical value.
    if not (critical < low or critical > high):
        raise ValueError(
            f"Invalid critical value for {lab['name']}: "
            f"critical={critical}, normal_range=({low}, {high})"
        )

    abnormal_probability = random.random()

    if abnormal_probability < 0.10:

        # -----------------------------------------------
        # LOW ABNORMAL RESULT
        # Example: Hemoglobin and Platelet Count
        # -----------------------------------------------

        if critical < low:
            value = round(
                random.uniform(critical, low - 0.01),
                2
            )

        # -----------------------------------------------
        # HIGH ABNORMAL RESULT
        # Example: Glucose, Creatinine, Urea, WBC,
        # Cholesterol and ALT
        # -----------------------------------------------

        else:
            value = round(
                random.uniform(high + 0.01, critical),
                2
            )

    else:

        # Generate a result inside the normal range.
        value = round(
            random.uniform(low, high),
            2
        )

    # Determine status using the actual generated value.
    if value < low or value > high:
        status = "Abnormal"
    else:
        status = "Normal"

    return value, status


# ============================================================
# MAIN GENERATOR
# ============================================================

def generate_lab_results():

    show_progress("Generating Laboratory Results Dataset")

    print()
    print("IMPORTANT:")
    print(
        "Laboratory results will use admissions directly "
        "from the current MySQL database."
    )
    print(
        "Admission_ID, Patient_ID and Doctor_ID relationships "
        "will be validated before saving."
    )

    # --------------------------------------------------------
    # Load admissions from MySQL
    # --------------------------------------------------------

    admission_records = load_database_admissions()

    # --------------------------------------------------------
    # Total records
    # --------------------------------------------------------

    total_records = config.NUM_LAB_RESULTS
    chunk_size_config = config.LAB_CHUNK_SIZE

    if total_records <= 0:
        raise ValueError(
            "config.NUM_LAB_RESULTS must be greater than zero."
        )

    if chunk_size_config <= 0:
        raise ValueError(
            "config.LAB_CHUNK_SIZE must be greater than zero."
        )

    print()
    print(f"Target lab-result records: {total_records:,}")
    print(
        f"Available valid admissions: {len(admission_records):,}"
    )

    # --------------------------------------------------------
    # Generate records
    # --------------------------------------------------------

    records = []

    for start in range(
        0,
        total_records,
        chunk_size_config
    ):

        current_chunk_size = min(
            chunk_size_config,
            total_records - start
        )

        chunk = []

        for _ in range(current_chunk_size):

            # Select a complete admission record so that
            # the patient and doctor belong to that admission.
            admission = random.choice(admission_records)

            admission_id = admission["Admission_ID"]
            patient_id = admission["Patient_ID"]
            doctor_id = admission["Doctor_ID"]

            # Select a laboratory test.
            lab = random.choice(LAB_TESTS)

            # Generate the corrected value and status.
            value, status = generate_lab_value(lab)

            low, high = lab["normal"]

            # Generate test date.
            test_date = str(
                pd.Timestamp(
                    random.randint(
                        1420070400,
                        1767139200
                    ),
                    unit="s"
                ).date()
            )

            # Create record.
            record = {
                "Lab_Result_ID": generate_uuid(),
                "Patient_ID": patient_id,
                "Admission_ID": admission_id,
                "Doctor_ID": doctor_id,
                "Test_Name": lab["name"],
                "Result_Value": value,
                "Unit": lab["unit"],
                "Reference_Range": f"{low}-{high}",
                "Result_Status": status,
                "Test_Date": test_date,
                "Performed_By": "Central Laboratory"
            }

            chunk.append(record)

        records.extend(chunk)

        print(
            f"{len(records):,} / {total_records:,} "
            "lab results generated"
        )

    # ========================================================
    # CREATE DATAFRAME
    # ========================================================

    dataframe = pd.DataFrame(records)

    # ========================================================
    # FINAL VALIDATION
    # ========================================================

    print()
    print("=" * 60)
    print("RUNNING FINAL VALIDATION")
    print("=" * 60)

    # --------------------------------------------------------
    # Row count
    # --------------------------------------------------------

    if len(dataframe) != total_records:
        raise ValueError(
            f"Expected {total_records:,} rows but generated "
            f"{len(dataframe):,} rows."
        )

    print(f"Row count: {len(dataframe):,} - VALID")

    # --------------------------------------------------------
    # Duplicate Lab_Result_ID
    # --------------------------------------------------------

    duplicate_lab_ids = (
        dataframe["Lab_Result_ID"].duplicated().sum()
    )

    if duplicate_lab_ids > 0:
        raise ValueError(
            f"Duplicate Lab_Result_ID values found: "
            f"{duplicate_lab_ids:,}"
        )

    print(
        f"Unique Lab_Result_IDs: "
        f"{dataframe['Lab_Result_ID'].nunique():,} - VALID"
    )

    # --------------------------------------------------------
    # Missing values
    # --------------------------------------------------------

    required_columns = [
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
        "Performed_By"
    ]

    for column in required_columns:

        missing_count = dataframe[column].isna().sum()

        if missing_count > 0:
            raise ValueError(
                f"Missing {column} values: {missing_count:,}"
            )

    print("Required columns: no missing values - VALID")

    # --------------------------------------------------------
    # Validate result status against reference range
    # --------------------------------------------------------

    reference_lookup = {
        lab["name"]: lab["normal"]
        for lab in LAB_TESTS
    }

    expected_low = dataframe["Test_Name"].map(
        lambda name: reference_lookup[name][0]
    )

    expected_high = dataframe["Test_Name"].map(
        lambda name: reference_lookup[name][1]
    )

    expected_status = np.where(
        (dataframe["Result_Value"] < expected_low)
        | (dataframe["Result_Value"] > expected_high),
        "Abnormal",
        "Normal"
    )

    status_mismatches = (
        dataframe["Result_Status"].to_numpy()
        != expected_status
    ).sum()

    if status_mismatches > 0:
        raise ValueError(
            "Result_Status validation failed. "
            f"Mismatched records: {status_mismatches:,}"
        )

    print(
        "Result_Status vs reference range: VALID "
        "(0 mismatches)"
    )

    # --------------------------------------------------------
    # Build admission validation lookup
    # --------------------------------------------------------

    admission_lookup = pd.DataFrame(admission_records)

    # Validate admission IDs and their patient/doctor links.
    validation_df = dataframe.merge(
        admission_lookup,
        on="Admission_ID",
        how="left",
        suffixes=("_generated", "_database"),
        validate="many_to_one",
        indicator=True
    )

    missing_database_admissions = (
        validation_df["_merge"] != "both"
    ).sum()

    if missing_database_admissions > 0:
        raise ValueError(
            "Generated CSV contains Admission_ID values "
            "not present in the MySQL admissions table: "
            f"{missing_database_admissions:,}"
        )

    print("All Admission_ID values exist in MySQL: VALID")

    # --------------------------------------------------------
    # Patient relationship
    # --------------------------------------------------------

    patient_mismatches = (
        validation_df["Patient_ID_generated"]
        != validation_df["Patient_ID_database"]
    ).sum()

    if patient_mismatches > 0:
        raise ValueError(
            f"Patient/Admission mismatches found: "
            f"{patient_mismatches:,}"
        )

    print("Patient/Admission relationship: VALID")

    # --------------------------------------------------------
    # Doctor relationship
    # --------------------------------------------------------

    doctor_mismatches = (
        validation_df["Doctor_ID_generated"]
        != validation_df["Doctor_ID_database"]
    ).sum()

    if doctor_mismatches > 0:
        raise ValueError(
            f"Doctor/Admission mismatches found: "
            f"{doctor_mismatches:,}"
        )

    print("Doctor/Admission/Doctor relationship: VALID")

    # ========================================================
    # SUMMARY BEFORE SAVING
    # ========================================================

    normal_count = (
        dataframe["Result_Status"] == "Normal"
    ).sum()

    abnormal_count = (
        dataframe["Result_Status"] == "Abnormal"
    ).sum()

    print()
    print("=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)

    print(f"Generated records       : {len(dataframe):,}")
    print(
        f"Unique Lab_Result_IDs   : "
        f"{dataframe['Lab_Result_ID'].nunique():,}"
    )
    print(
        f"Unique Patients         : "
        f"{dataframe['Patient_ID'].nunique():,}"
    )
    print(
        f"Unique Admissions       : "
        f"{dataframe['Admission_ID'].nunique():,}"
    )
    print(
        f"Unique Doctors          : "
        f"{dataframe['Doctor_ID'].nunique():,}"
    )
    print(f"Normal Results          : {normal_count:,}")
    print(f"Abnormal Results        : {abnormal_count:,}")

    # Per-test status summary.
    print()
    print("Status counts by test:")

    print(
        pd.crosstab(
            dataframe["Test_Name"],
            dataframe["Result_Status"]
        ).to_string()
    )

    # ========================================================
    # SAVE DATASET
    # ========================================================

    print()
    print("=" * 60)
    print("SAVING LAB RESULTS DATASET")
    print("=" * 60)

    save_dataframe(
        dataframe,
        "lab_results.csv"
    )

    # ========================================================
    # COMPLETION
    # ========================================================

    print()
    print("=" * 60)
    print("LAB RESULTS DATASET GENERATION COMPLETED")
    print("=" * 60)

    print(f"Generated records       : {len(dataframe):,}")
    print(f"Normal Results          : {normal_count:,}")
    print(f"Abnormal Results        : {abnormal_count:,}")
    print("Reference-range status  : VALID")
    print("Admission relationships : VALID")
    print("Dataset saved           : SUCCESS")
    print("=" * 60)


# ============================================================
# SCRIPT ENTRY POINT
# ============================================================

if __name__ == "__main__":
    generate_lab_results()
