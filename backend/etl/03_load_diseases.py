import os
import pandas as pd
import mysql.connector
from mysql.connector import Error

# ==============================================================
# CONFIGURATION
# ==============================================================

DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = os.environ.get("MYSQL_PASSWORD")
DB_NAME = "healthcare_ai_db"

CSV_FILE = os.path.join(
    "datasets",
    "synthetic",
    "diseases.csv"
)

BATCH_SIZE = 1000


# ==============================================================
# DATABASE CONNECTION
# ==============================================================

def get_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        if connection.is_connected():
            return connection

    except Error as e:
        print(f"âŒ Database connection failed: {e}")

    return None


# ==============================================================
# VALUE HELPERS
# ==============================================================

def clean_value(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    if value == "":
        return None

    return value


def convert_boolean(value):
    if pd.isna(value):
        return 0

    value = str(value).strip().lower()

    if value in ("true", "yes", "1"):
        return 1

    return 0


def map_disease_type(value):
    if pd.isna(value):
        return "Other"

    value = str(value).strip().lower()

    mapping = {
        "acute": "Acute",
        "chronic": "Chronic",
        "genetic": "Genetic",
        "infectious": "Infectious",
        "lifestyle": "Lifestyle",
        "autoimmune": "Autoimmune",
        "cancer": "Cancer",
        "mental health": "Mental Health",
        "other": "Other",
        "yes": "Chronic",
        "true": "Chronic",
        "1": "Chronic",
        "no": "Acute",
        "false": "Acute",
        "0": "Acute"
    }

    return mapping.get(value, "Other")


def map_severity(value):
    if pd.isna(value):
        return "Low"

    value = str(value).strip().lower()

    mapping = {
        "low": "Low",
        "mild": "Low",
        "moderate": "Moderate",
        "medium": "Moderate",
        "high": "High",
        "severe": "High",
        "critical": "Critical"
    }

    return mapping.get(value, "Low")


# ==============================================================
# MAIN ETL
# ==============================================================

def main():

    print("=" * 70)
    print("        AI HEALTHCARE PROJECT - DISEASE ETL")
    print("=" * 70)

    print(f"CSV File     : {os.path.abspath(CSV_FILE)}")
    print(f"Batch Size   : {BATCH_SIZE}")
    print(f"Database     : {DB_NAME}")

    print("=" * 70)
    print()

    # ----------------------------------------------------------
    # CHECK CSV
    # ----------------------------------------------------------

    if not os.path.exists(CSV_FILE):
        print(f"âŒ CSV file not found: {CSV_FILE}")
        return

    print("CSV file found successfully.")

    # ----------------------------------------------------------
    # CONNECT DATABASE
    # ----------------------------------------------------------

    connection = get_connection()

    if connection is None:
        return

    print("MySQL connection successful.")
    print()

    cursor = connection.cursor()

    # ----------------------------------------------------------
    # REQUIRED CSV COLUMNS
    # ----------------------------------------------------------

    required_columns = [
        "Disease_ID",
        "Disease_Name",
        "ICD_Code",
        "Disease_Category",
        "Description",
        "Risk_Level",
        "Chronic_Status",
        "Common_Age_Group",
        "Gender_Affected",
        "Treatable"
    ]

    # ----------------------------------------------------------
    # READ CSV
    # ----------------------------------------------------------

    print("Reading diseases.csv...")

    try:
        df = pd.read_csv(CSV_FILE)
    except Exception as e:
        print(f"âŒ Failed to read CSV: {e}")
        cursor.close()
        connection.close()
        return

    print(f"Rows loaded from CSV: {len(df):,}")

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        print("âŒ Missing CSV columns:")
        for column in missing_columns:
            print(f"   - {column}")

        cursor.close()
        connection.close()
        return

    print("CSV columns verified successfully.")
    print()

    # ----------------------------------------------------------
    # LOAD EXISTING DATABASE IDS
    # ----------------------------------------------------------

    cursor.execute("SELECT Disease_ID FROM diseases")
    existing_ids = {
        row[0]
        for row in cursor.fetchall()
    }

    print(f"Existing diseases : {len(existing_ids):,}")
    print()

    # ----------------------------------------------------------
    # PREPARE RECORDS
    # ----------------------------------------------------------

    print("Preparing disease records...")
    print("-" * 70)

    records = []

    existing_skipped = 0
    duplicate_csv_ids = 0
    invalid_rows = 0

    seen_ids = set()

    for _, row in df.iterrows():

        disease_id = clean_value(row["Disease_ID"])
        disease_name = clean_value(row["Disease_Name"])

        # ------------------------------------------------------
        # REQUIRED VALUES
        # ------------------------------------------------------

        if disease_id is None or disease_name is None:
            invalid_rows += 1
            continue

        # ------------------------------------------------------
        # IMPORTANT:
        # Disease_ID is the UNIQUE identifier.
        #
        # Disease_Name is NOT used for deduplication because
        # the dataset intentionally contains multiple records
        # with the same disease name.
        # ------------------------------------------------------

        if disease_id in seen_ids:
            duplicate_csv_ids += 1
            continue

        seen_ids.add(disease_id)

        if disease_id in existing_ids:
            existing_skipped += 1
            continue

        # ------------------------------------------------------
        # MAP CSV VALUES
        # ------------------------------------------------------

        icd10_code = clean_value(row["ICD_Code"])

        disease_category = clean_value(
            row["Disease_Category"]
        )

        description = clean_value(
            row["Description"]
        )

        disease_type = map_disease_type(
            row["Chronic_Status"]
        )

        severity = map_severity(
            row["Risk_Level"]
        )

        # ------------------------------------------------------
        # DATABASE-ONLY FIELDS
        # ------------------------------------------------------

        symptoms = None
        causes = None
        risk_factors = None
        prevention = None
        treatment_protocol = None
        recovery_period_days = None

        mortality_risk = "Low"

        requires_hospitalization = 0
        is_contagious = 0

        status = "Active"
        is_active = 1
        is_deleted = 0

        created_by = "Synthetic_ETL"
        updated_by = "Synthetic_ETL"

        record_version = 1

        # ------------------------------------------------------
        # BUILD RECORD
        # ------------------------------------------------------

        record = (
            disease_id,
            disease_name,
            icd10_code,
            None,                       # SNOMED_Code
            disease_category,
            None,                       # Department_Name
            disease_type,
            description,
            symptoms,
            causes,
            risk_factors,
            prevention,
            treatment_protocol,
            recovery_period_days,
            severity,
            mortality_risk,
            requires_hospitalization,
            is_contagious,
            status,
            is_active,
            is_deleted,
            created_by,
            updated_by,
            record_version
        )

        records.append(record)

    # ----------------------------------------------------------
    # PREPARATION SUMMARY
    # ----------------------------------------------------------

    print(f"Prepared records        : {len(records):,}")
    print(f"Existing records skipped: {existing_skipped:,}")
    print(f"CSV duplicate IDs       : {duplicate_csv_ids:,}")
    print(f"Invalid rows             : {invalid_rows:,}")

    print()

    # ----------------------------------------------------------
    # INSERT QUERY
    # ----------------------------------------------------------

    insert_query = """
        INSERT INTO diseases (
            Disease_ID,
            Disease_Name,
            ICD10_Code,
            SNOMED_Code,
            Disease_Category,
            Department_Name,
            Disease_Type,
            Description,
            Symptoms,
            Causes,
            Risk_Factors,
            Prevention,
            Treatment_Protocol,
            Recovery_Period_Days,
            Severity,
            Mortality_Risk,
            Requires_Hospitalization,
            Is_Contagious,
            Status,
            Is_Active,
            Is_Deleted,
            Created_By,
            Updated_By,
            Record_Version
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s
        )
    """

    # ----------------------------------------------------------
    # INSERT IN BATCHES
    # ----------------------------------------------------------

    inserted = 0

    if records:

        print("Starting database insertion...")
        print("-" * 70)

        try:

            for start in range(0, len(records), BATCH_SIZE):

                batch = records[
                    start:start + BATCH_SIZE
                ]

                cursor.executemany(
                    insert_query,
                    batch
                )

                connection.commit()

                inserted += len(batch)

                print(
                    f"Inserted {inserted:,} / "
                    f"{len(records):,} diseases"
                )

        except Error as e:

            connection.rollback()

            print()
            print(f"âŒ Database insertion failed: {e}")

            cursor.close()
            connection.close()
            return

    # ----------------------------------------------------------
    # FINAL COUNT
    # ----------------------------------------------------------

    cursor.execute(
        "SELECT COUNT(*) FROM diseases"
    )

    total_diseases = cursor.fetchone()[0]

    # ----------------------------------------------------------
    # FINAL OUTPUT
    # ----------------------------------------------------------

    print()
    print("=" * 70)
    print("DISEASE ETL COMPLETED SUCCESSFULLY")
    print("=" * 70)

    print(f"CSV rows processed       : {len(df):,}")
    print(f"Existing records skipped : {existing_skipped:,}")
    print(f"CSV duplicate IDs        : {duplicate_csv_ids:,}")
    print(f"Invalid rows             : {invalid_rows:,}")
    print(f"Inserted this run        : {inserted:,}")
    print(f"Total diseases           : {total_diseases:,}")

    print("=" * 70)

    # ----------------------------------------------------------
    # SAMPLE RECORDS
    # ----------------------------------------------------------

    print()
    print("Sample disease records:")
    print("-" * 70)

    cursor.execute("""
        SELECT
            Disease_ID,
            Disease_Name,
            ICD10_Code,
            Disease_Type,
            Severity,
            Status
        FROM diseases
        ORDER BY Disease_Name, Disease_ID
        LIMIT 10
    """)

    for record in cursor.fetchall():
        print(record)

    print()

    cursor.close()
    connection.close()

    print("Database connection closed.")
    print("Disease ETL finished.")


# ==============================================================
# RUN
# ==============================================================

if __name__ == "__main__":
    main()