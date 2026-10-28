import os
import hashlib
import mysql.connector
import pandas as pd


# ============================================================
# STEP 12 - LOAD INSURANCE PROVIDERS
# ============================================================

PROJECT_ROOT = r"E:\College Final Year\Major Project\Healthcare_AI_Project"

SOURCE_FILE = os.path.join(
    PROJECT_ROOT,
    "backend",
    "dataset_generator",
    "reference",
    "insurance_master.csv"
)

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "database": "healthcare_ai_db"
}


# ============================================================
# HELPERS
# ============================================================

def clean_text(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    if value == "" or value.lower() in {"nan", "none", "null"}:
        return None

    return value


def generate_provider_code(index):
    """
    Deterministic provider code.
    Example:
        INS-0001
        INS-0002
    """
    return f"INS-{index:04d}"


def map_insurance_type(provider_type):
    """
    Reference CSV:
        Private
        Government

    Database enum:
        Government
        Private
        Employer
        TPA
    """

    provider_type = clean_text(provider_type)

    mapping = {
        "Private": "Private",
        "Government": "Government"
    }

    return mapping.get(provider_type)


def map_coverage_type(provider_type, coverage_type):
    """
    Reference CSV:
        Health Insurance
        Public Healthcare
        Employee Healthcare

    Database enum:
        Individual
        Family
        Corporate
        Senior Citizen
    """

    provider_type = clean_text(provider_type)
    coverage_type = clean_text(coverage_type)

    # Private health insurance
    if provider_type == "Private" and coverage_type == "Health Insurance":
        return "Individual"

    # Government/public healthcare
    if provider_type == "Government" and coverage_type == "Public Healthcare":
        return "Senior Citizen"

    # Government employee healthcare
    if provider_type == "Government" and coverage_type == "Employee Healthcare":
        return "Corporate"

    # Safe fallback
    if provider_type == "Private":
        return "Individual"

    if provider_type == "Government":
        return "Corporate"

    return "Individual"


def generate_email(provider_name):
    """
    Generates deterministic synthetic email.
    """

    clean_name = "".join(
        char.lower()
        for char in provider_name
        if char.isalnum() or char == " "
    )

    clean_name = clean_name.replace(" ", ".")[:40]

    return f"contact.{clean_name}@example-healthcare.in"


def generate_claim_email(provider_name):
    """
    Generates deterministic synthetic claims email.
    """

    clean_name = "".join(
        char.lower()
        for char in provider_name
        if char.isalnum() or char == " "
    )

    clean_name = clean_name.replace(" ", ".")[:40]

    return f"claims.{clean_name}@example-healthcare.in"


def generate_website(index):
    return f"https://insurance-provider-{index:04d}.example"


def generate_claim_website(index):
    return f"https://insurance-provider-{index:04d}.example/claims"


def generate_support_hours(provider_type):
    if provider_type == "Government":
        return "24x7"

    return "24x7"


# ============================================================
# START
# ============================================================

print("=" * 70)
print("STEP 12 - LOAD INSURANCE PROVIDERS")
print("=" * 70)


# ============================================================
# LOAD SOURCE
# ============================================================

print("\nLoading insurance_master.csv...")

df = pd.read_csv(
    SOURCE_FILE,
    dtype={
        "Provider_Name": str,
        "Provider_Type": str,
        "Coverage_Type": str
    }
)

print(
    f"Source rows loaded: {len(df):,}"
)


# ============================================================
# SOURCE VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("SOURCE VALIDATION")
print("=" * 70)

required_columns = [
    "Provider_Name",
    "Provider_Type",
    "Coverage_Type",
    "Network_Size",
    "Claim_Ratio"
]

missing_columns = [
    col
    for col in required_columns
    if col not in df.columns
]

if missing_columns:
    print(
        "ERROR: Missing required columns:",
        missing_columns
    )
    raise SystemExit(1)


df["Provider_Name"] = (
    df["Provider_Name"].map(clean_text)
)

df["Provider_Type"] = (
    df["Provider_Type"].map(clean_text)
)

df["Coverage_Type"] = (
    df["Coverage_Type"].map(clean_text)
)


print(
    f"Unique Provider_Name: "
    f"{df['Provider_Name'].nunique():,}"
)

print(
    f"Duplicate Provider_Name rows: "
    f"{df['Provider_Name'].duplicated().sum():,}"
)

print("\nProvider Type distribution:")

print(
    df["Provider_Type"]
    .value_counts(dropna=False)
    .to_string()
)

print("\nCoverage Type distribution:")

print(
    df["Coverage_Type"]
    .value_counts(dropna=False)
    .to_string()
)


# ============================================================
# CONNECT TO MYSQL
# ============================================================

print("\nConnecting to MySQL...")

connection = mysql.connector.connect(
    host=DB_CONFIG["host"],
    user=DB_CONFIG["user"],
    database=DB_CONFIG["database"],
    password=input("Enter MySQL root password: ")
)

cursor = connection.cursor()

print("MySQL connection successful.")


# ============================================================
# CHECK EXISTING RECORDS
# ============================================================

cursor.execute(
    "SELECT COUNT(*) FROM insurance_providers"
)

existing_count = cursor.fetchone()[0]

print(
    f"\nExisting insurance providers: "
    f"{existing_count:,}"
)

if existing_count > 0:

    print(
        "\nERROR: insurance_providers already contains data."
    )

    print(
        "Loader stopped to prevent duplicate master data."
    )

    cursor.close()
    connection.close()

    raise SystemExit(1)


# ============================================================
# INSERT QUERY
# ============================================================

insert_query = """
INSERT INTO insurance_providers (
    Provider_Code,
    Provider_Name,
    Insurance_Type,
    Coverage_Type,
    Contact_Number,
    Helpline_Number,
    Email,
    Claim_Email,
    Website,
    Claim_Website,
    GST_Number,
    IRDAI_Registration_No,
    Address,
    City,
    State,
    Country,
    Postal_Code,
    Cashless_Available,
    Support_Hours,
    Status,
    Is_Active,
    Is_Deleted,
    Created_By,
    Updated_By,
    Record_Version
)
VALUES (
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s
)
"""


# ============================================================
# PREPARE DATA
# ============================================================

print("\nPreparing insurance provider records...")

records = []

invalid_rows = 0

for index, (_, row) in enumerate(
    df.iterrows(),
    start=1
):

    provider_name = clean_text(
        row["Provider_Name"]
    )

    provider_type = clean_text(
        row["Provider_Type"]
    )

    coverage_type = clean_text(
        row["Coverage_Type"]
    )

    if (
        provider_name is None
        or provider_type is None
        or coverage_type is None
    ):
        invalid_rows += 1
        continue

    insurance_type = map_insurance_type(
        provider_type
    )

    db_coverage_type = map_coverage_type(
        provider_type,
        coverage_type
    )

    if insurance_type is None:
        invalid_rows += 1
        continue

    provider_code = generate_provider_code(
        index
    )

    email = generate_email(
        provider_name
    )

    claim_email = generate_claim_email(
        provider_name
    )

    website = generate_website(
        index
    )

    claim_website = generate_claim_website(
        index
    )

    values = (
        provider_code,
        provider_name,
        insurance_type,
        db_coverage_type,

        None,                  # Contact_Number
        None,                  # Helpline_Number
        email,
        claim_email,
        website,
        claim_website,

        None,                  # GST_Number
        None,                  # IRDAI_Registration_No
        None,                  # Address
        None,                  # City
        None,                  # State

        "India",
        None,                  # Postal_Code

        1,                     # Cashless_Available
        generate_support_hours(provider_type),

        "Active",
        1,                     # Is_Active
        0,                     # Is_Deleted

        "ETL_12",
        "ETL_12",
        1
    )

    records.append(values)


print(
    f"Valid records prepared: {len(records):,}"
)

print(
    f"Invalid records skipped: {invalid_rows:,}"
)


# ============================================================
# INSERT
# ============================================================

if not records:

    print(
        "\nERROR: No valid insurance provider records."
    )

    cursor.close()
    connection.close()

    raise SystemExit(1)


print("\nInserting insurance providers...")

cursor.executemany(
    insert_query,
    records
)

connection.commit()

print(
    f"Inserted records: {cursor.rowcount:,}"
)


# ============================================================
# DATABASE VALIDATION
# ============================================================

cursor.execute(
    """
    SELECT
        COUNT(*) AS Total_Providers,
        COUNT(DISTINCT Insurance_ID) AS Unique_Insurance_IDs,
        COUNT(DISTINCT Provider_Code) AS Unique_Provider_Codes,
        COUNT(DISTINCT Provider_Name) AS Unique_Provider_Names,
        SUM(Status = 'Active') AS Active_Providers,
        SUM(Is_Active = 1) AS Active_Flag,
        SUM(Is_Deleted = 0) AS Not_Deleted
    FROM insurance_providers
    """
)

result = cursor.fetchone()

(
    total_providers,
    unique_ids,
    unique_codes,
    unique_names,
    active_providers,
    active_flag,
    not_deleted
) = result


print("\n" + "=" * 70)
print("DATABASE VALIDATION")
print("=" * 70)

print(
    f"Total providers:           {total_providers:,}"
)

print(
    f"Unique Insurance_IDs:      {unique_ids:,}"
)

print(
    f"Unique Provider_Codes:     {unique_codes:,}"
)

print(
    f"Unique Provider_Names:     {unique_names:,}"
)

print(
    f"Active Status providers:   {active_providers:,}"
)

print(
    f"Is_Active = 1:             {active_flag:,}"
)

print(
    f"Is_Deleted = 0:             {not_deleted:,}"
)


# ============================================================
# TYPE VALIDATION
# ============================================================

cursor.execute(
    """
    SELECT
        Insurance_Type,
        COUNT(*)
    FROM insurance_providers
    GROUP BY Insurance_Type
    ORDER BY Insurance_Type
    """
)

print("\nINSURANCE TYPE")

for insurance_type, count in cursor.fetchall():

    print(
        f"{insurance_type}: {count:,}"
    )


cursor.execute(
    """
    SELECT
        Coverage_Type,
        COUNT(*)
    FROM insurance_providers
    GROUP BY Coverage_Type
    ORDER BY Coverage_Type
    """
)

print("\nCOVERAGE TYPE")

for coverage_type, count in cursor.fetchall():

    print(
        f"{coverage_type}: {count:,}"
    )


# ============================================================
# FINAL STATUS
# ============================================================

passed = (
    total_providers == len(records)
    and unique_ids == total_providers
    and unique_codes == total_providers
    and unique_names == total_providers
    and active_providers == total_providers
    and active_flag == total_providers
    and not_deleted == total_providers
    and invalid_rows == 0
)


print("\n" + "=" * 70)

if passed:
    print("STEP 12 - LOAD INSURANCE PROVIDERS: PASSED")
else:
    print("STEP 12 - LOAD INSURANCE PROVIDERS: FAILED")

print("=" * 70)


cursor.close()
connection.close()