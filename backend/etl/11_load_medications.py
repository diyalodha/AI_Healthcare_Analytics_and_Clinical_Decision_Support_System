import os
import sys
import pandas as pd
import mysql.connector
from mysql.connector import Error

# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ROOT = r"E:\College Final Year\Major Project\Healthcare_AI_Project"

CSV_PATH = os.path.join(
    PROJECT_ROOT,
    "datasets",
    "synthetic",
    "medications.csv"
)

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": input("Enter MySQL root password: "),
    "database": "healthcare_ai_db"
}

BATCH_SIZE = 5000


# ============================================================
# ROUTE MAPPING
# ============================================================

ROUTE_MAPPING = {
    "oral": "Oral",
    "iv": "IV",
    "intravenous": "IV",
    "im": "IM",
    "intramuscular": "IM",
    "subcutaneous": "Subcutaneous",
    "topical": "Topical",
    "inhalation": "Inhalation",
    "rectal": "Rectal",
    "ophthalmic": "Ophthalmic",
    "nasal": "Nasal",
    "injection": "Other"
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clean_string(value):

    if pd.isna(value):
        return None

    value = str(value).strip()

    if value == "":
        return None

    if value.lower() in {"nan", "none", "null"}:
        return None

    return value


def map_route(value):

    value = clean_string(value)

    if value is None:
        return "Other"

    return ROUTE_MAPPING.get(
        value.lower(),
        "Other"
    )


# ============================================================
# START
# ============================================================

print("=" * 70)
print("STEP 11 - LOAD MEDICATIONS")
print("=" * 70)


# ============================================================
# LOAD CSV
# ============================================================

print("\nLoading medications.csv...")

try:

    df = pd.read_csv(
        CSV_PATH,
        dtype=str
    )

except Exception as e:

    print("\nERROR reading medications.csv:")
    print(e)

    sys.exit(1)

print(
    f"CSV rows loaded: {len(df):,}"
)


# ============================================================
# REQUIRED COLUMNS
# ============================================================

required_columns = [
    "Medication_ID",
    "Medication_Name",
    "Generic_Name",
    "Drug_Class",
    "Used_For",
    "Route",
    "Dosage_Form",
    "Strength",
    "Risk_Level"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:

    print("\nERROR: Missing columns:")

    for column in missing_columns:
        print(f"  - {column}")

    sys.exit(1)


# ============================================================
# CLEAN DATA
# ============================================================

for column in required_columns:

    df[column] = df[column].apply(
        clean_string
    )


before_count = len(df)

df = df[
    df["Medication_ID"].notna()
    & df["Medication_Name"].notna()
    & df["Generic_Name"].notna()
    & df["Drug_Class"].notna()
    & df["Used_For"].notna()
    & df["Dosage_Form"].notna()
    & df["Strength"].notna()
    & df["Risk_Level"].notna()
].copy()

invalid_required = (
    before_count - len(df)
)

print(
    f"Valid rows: {len(df):,}"
)

print(
    f"Invalid required rows: "
    f"{invalid_required:,}"
)


# ============================================================
# DUPLICATE CHECK
# ============================================================

duplicate_count = df[
    "Medication_ID"
].duplicated().sum()

print(
    f"Duplicate Medication_ID rows: "
    f"{duplicate_count:,}"
)

if duplicate_count > 0:

    df = df.drop_duplicates(
        subset=["Medication_ID"],
        keep="first"
    ).copy()


# ============================================================
# ROUTE MAPPING
# ============================================================

print("\nSource Route values:")

print(
    df["Route"]
    .value_counts(dropna=False)
    .to_string()
)

df["Mapped_Route"] = df["Route"].apply(
    map_route
)

print("\nMapped database Route values:")

print(
    df["Mapped_Route"]
    .value_counts(dropna=False)
    .to_string()
)

print("\nRoute mapping used:")

for route in sorted(
    df["Route"].dropna().unique()
):

    print(
        f"  {route:<15} -> "
        f"{map_route(route)}"
    )


# ============================================================
# CONNECT TO MYSQL
# ============================================================

print("\nConnecting to MySQL...")

try:

    connection = mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"]
    )

    cursor = connection.cursor()

    print(
        "MySQL connection successful."
    )

except Error as e:

    print(
        "\nERROR connecting to MySQL:"
    )

    print(e)

    sys.exit(1)


# ============================================================
# EXISTING RECORD CHECK
# ============================================================

try:

    cursor.execute(
        "SELECT COUNT(*) FROM medications"
    )

    existing_count = cursor.fetchone()[0]

    print(
        f"\nExisting medications in database: "
        f"{existing_count:,}"
    )

    if existing_count > 0:

        print(
            "\nWARNING: medications table already "
            "contains records."
        )

        print(
            "Loader stopped to prevent duplicates."
        )

        cursor.close()
        connection.close()

        sys.exit(0)

except Error as e:

    print(
        "\nERROR checking medications:"
    )

    print(e)

    cursor.close()
    connection.close()

    sys.exit(1)


# ============================================================
# INSERT SQL
# ============================================================
#
# Only columns for which we have reliable source data
# are explicitly inserted.
#
# Other columns use their database defaults or NULL.

insert_sql = """
INSERT INTO medications (
    Medication_ID,
    Medication_Code,
    Medication_Name,
    Generic_Name,
    Drug_Class,
    Used_For,
    Dosage_Form,
    Strength,
    Route,
    Prescription_Required,
    Risk_Level,
    Status,
    Is_Active,
    Is_Deleted,
    Created_By,
    Updated_By,
    Record_Version
)
VALUES (
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s,
    %s
)
"""


# ============================================================
# INSERT
# ============================================================

print("\nBeginning insertion...")

inserted = 0

try:

    batch = []

    for position, (_, row) in enumerate(
        df.iterrows(),
        start=1
    ):

        medication_code = (
            f"MED-{position:06d}"
        )

        values = (
            row["Medication_ID"],
            medication_code,
            row["Medication_Name"],
            row["Generic_Name"],
            row["Drug_Class"],
            row["Used_For"],
            row["Dosage_Form"],
            row["Strength"],
            row["Mapped_Route"],
            1,
            row["Risk_Level"],
            "Available",
            1,
            0,
            "ETL_11",
            "ETL_11",
            1
        )

        batch.append(values)

        if len(batch) >= BATCH_SIZE:

            cursor.executemany(
                insert_sql,
                batch
            )

            connection.commit()

            inserted += len(batch)

            print(
                f"Inserted: "
                f"{inserted:,} / "
                f"{len(df):,}"
            )

            batch = []


    # Remaining records

    if batch:

        cursor.executemany(
            insert_sql,
            batch
        )

        connection.commit()

        inserted += len(batch)


    print("\n" + "=" * 70)
    print("MEDICATION LOAD COMPLETED")
    print("=" * 70)

    print(
        f"CSV rows:  {len(df):,}"
    )

    print(
        f"Inserted:  {inserted:,}"
    )


except Error as e:

    connection.rollback()

    print(
        "\nERROR during insertion:"
    )

    print(e)

    print(
        "\nTransaction rolled back."
    )

    cursor.close()
    connection.close()

    sys.exit(1)


# ============================================================
# FINAL VERIFICATION
# ============================================================

try:

    cursor.execute(
        "SELECT COUNT(*) FROM medications"
    )

    total_medications = (
        cursor.fetchone()[0]
    )


    cursor.execute(
        """
        SELECT COUNT(DISTINCT Medication_ID)
        FROM medications
        """
    )

    unique_ids = (
        cursor.fetchone()[0]
    )


    cursor.execute(
        """
        SELECT COUNT(DISTINCT Medication_Code)
        FROM medications
        """
    )

    unique_codes = (
        cursor.fetchone()[0]
    )


    cursor.execute(
        """
        SELECT Route, COUNT(*)
        FROM medications
        GROUP BY Route
        ORDER BY Route
        """
    )

    route_counts = cursor.fetchall()


    print("\nFinal database verification:")

    print(
        f"Total medications:       "
        f"{total_medications:,}"
    )

    print(
        f"Unique Medication_IDs:   "
        f"{unique_ids:,}"
    )

    print(
        f"Unique Medication_Codes: "
        f"{unique_codes:,}"
    )


    print(
        "\nDatabase Route distribution:"
    )

    for route, count in route_counts:

        print(
            f"  {route:<15} "
            f"{count:,}"
        )


    if (
        total_medications == 500
        and unique_ids == 500
        and unique_codes == 500
    ):

        print(
            "\nSTATUS: PASSED"
        )

        print(
            "All 500 medication master records "
            "are loaded successfully."
        )

    else:

        print(
            "\nSTATUS: CHECK REQUIRED"
        )


except Error as e:

    print(
        "\nERROR during final verification:"
    )

    print(e)


finally:

    cursor.close()
    connection.close()

    print(
        "\nMySQL connection closed."
    )