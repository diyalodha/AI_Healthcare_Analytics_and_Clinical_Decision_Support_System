import os
import re
import hashlib
import mysql.connector
import pandas as pd
import numpy as np


# ============================================================
# STEP 55 - PATIENT INSURANCE MAPPING
# ============================================================

PROJECT_ROOT = r"E:\College Final Year\Major Project\Healthcare_AI_Project"

PATIENTS_FILE = os.path.join(
    PROJECT_ROOT,
    "datasets",
    "synthetic",
    "patients.csv"
)

INSURANCE_FILE = os.path.join(
    PROJECT_ROOT,
    "datasets",
    "synthetic",
    "insurance_providers.csv"
)

BATCH_SIZE = 5000

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "database": "healthcare_ai_db"
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clean_text(value):
    if pd.isna(value):
        return None

    value = str(value).strip()

    if value == "" or value.lower() in {"nan", "none", "null"}:
        return None

    return value


def deterministic_hash(text):
    return int(
        hashlib.sha256(str(text).encode("utf-8")).hexdigest(),
        16
    )


def normalize_provider_type(provider_type):
    """
    CSV:
        Private
        Government

    DB:
        Government
        Private
        Employer
        TPA
    """

    provider_type = clean_text(provider_type)

    if provider_type == "Government":
        return "Government"

    if provider_type == "Private":
        return "Private"

    return "Private"


def normalize_policy_type(provider_type, index):
    """
    Maps provider type to target patient policy type.
    """

    if provider_type == "Government":
        return "Government Scheme"

    options = [
        "Individual",
        "Family Floater",
        "Group",
        "Corporate"
    ]

    # Deterministic distribution
    return options[index % len(options)]


def normalize_plan_name(provider_name, provider_type, policy_type):
    """
    Creates a synthetic plan name.
    """

    provider_name = clean_text(provider_name)

    if provider_name is None:
        provider_name = "Insurance Provider"

    provider_name = provider_name.strip()

    if provider_type == "Government":
        return f"{provider_name} Government Health Plan"

    return f"{provider_name} {policy_type} Health Plan"


def generate_policy_number(patient_id, provider_id, index):
    """
    Deterministic unique policy number.
    """

    raw = f"{patient_id}|{provider_id}|{index}"

    digest = hashlib.sha256(
        raw.encode("utf-8")
    ).hexdigest()[:16].upper()

    return f"POL-{digest}"


def generate_policy_dates(patient_id, index):
    """
    Generate deterministic synthetic policy dates.

    Dates are kept in a historical/reasonable range rather than
    depending on today's date.
    """

    seed = deterministic_hash(patient_id)

    start_year = 2018 + (seed % 7)       # 2018-2024
    start_month = 1 + ((seed // 10) % 12)
    start_day = 1 + ((seed // 100) % 25)

    start_date = pd.Timestamp(
        year=int(start_year),
        month=int(start_month),
        day=int(start_day)
    )

    # Mostly one-year policies
    duration_days = 365

    # Some policies are two-year policies
    if (seed % 10) >= 8:
        duration_days = 730

    end_date = start_date + pd.Timedelta(
        days=duration_days - 1
    )

    return start_date.date(), end_date.date()


def determine_policy_status(end_date, seed):
    """
    Deterministically distribute Active / Expired policies.
    """

    if seed % 10 < 6:
        return "Active"

    return "Expired"


def generate_coverage(provider_type, policy_type, seed):
    """
    Synthetic coverage amount.
    """

    if provider_type == "Government":
        amounts = [
            100000,
            150000,
            200000,
            300000
        ]
    elif policy_type == "Corporate":
        amounts = [
            300000,
            500000,
            750000,
            1000000
        ]
    elif policy_type == "Family Floater":
        amounts = [
            300000,
            500000,
            750000
        ]
    else:
        amounts = [
            200000,
            300000,
            500000
        ]

    return float(
        amounts[seed % len(amounts)]
    )


def generate_copayment(provider_type, policy_type, seed):

    if provider_type == "Government":
        return 0.0

    values = [0.0, 5.0, 10.0, 15.0, 20.0]

    return float(
        values[seed % len(values)]
    )


def generate_deductible(total_coverage, seed):

    options = [
        0,
        5000,
        10000,
        15000,
        20000
    ]

    value = float(
        options[seed % len(options)]
    )

    # Never allow deductible greater than coverage
    return min(value, total_coverage)


def generate_claim_information(
    policy_status,
    total_coverage,
    seed
):
    """
    Synthetic claim information.

    This does NOT represent real claims.
    """

    # Most synthetic policies have no claim.
    if seed % 10 < 7:
        return (
            0,                  # Claim_Required
            None,               # Claim_Number
            "Not Required",     # Claim_Status
            None,               # Claim_Submission_Date
            None,               # Claim_Settlement_Date
            None,               # Claim_Amount
            None,               # Approved_Claim_Amount
            None                # Rejection_Reason
        )

    claim_amount = round(
        total_coverage * (0.05 + ((seed % 20) / 100)),
        2
    )

    if policy_status == "Expired":
        claim_status = "Settled"
    else:
        claim_status = "Approved"

    claim_number = f"CLM-{seed % 100000000:08d}"

    claim_submission_date = None
    claim_settlement_date = None

    # Dates are intentionally left NULL because
    # the source dataset contains no claim dates.
    approved_amount = claim_amount

    return (
        1,
        claim_number,
        claim_status,
        claim_submission_date,
        claim_settlement_date,
        claim_amount,
        approved_amount,
        None
    )


# ============================================================
# MAIN
# ============================================================

print("=" * 70)
print("STEP 55 - PATIENT INSURANCE MAPPING")
print("=" * 70)


# ============================================================
# LOAD SOURCE DATA
# ============================================================

print("\nLoading patients.csv...")

patients_df = pd.read_csv(
    PATIENTS_FILE,
    dtype=str
)

print(
    f"Patient rows loaded: {len(patients_df):,}"
)


print("\nLoading insurance_providers.csv...")

insurance_df = pd.read_csv(
    INSURANCE_FILE,
    dtype=str
)

print(
    f"Insurance provider rows loaded: {len(insurance_df):,}"
)


# ============================================================
# SOURCE VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("SOURCE VALIDATION")
print("=" * 70)


patients_df["Patient_ID"] = (
    patients_df["Patient_ID"]
    .map(clean_text)
)

insurance_df["Insurance_Provider_ID"] = (
    insurance_df["Insurance_Provider_ID"]
    .map(clean_text)
)

insurance_df["Provider_Name"] = (
    insurance_df["Provider_Name"]
    .map(clean_text)
)

insurance_df["Provider_Type"] = (
    insurance_df["Provider_Type"]
    .map(clean_text)
)

insurance_df["Coverage_Type"] = (
    insurance_df["Coverage_Type"]
    .map(clean_text)
)


print(
    "Unique Patient_IDs:",
    patients_df["Patient_ID"].nunique()
)

print(
    "Unique Insurance_Provider_IDs:",
    insurance_df["Insurance_Provider_ID"].nunique()
)

print(
    "Duplicate Patient_ID rows:",
    patients_df["Patient_ID"].duplicated().sum()
)

print(
    "Duplicate Insurance_Provider_ID rows:",
    insurance_df["Insurance_Provider_ID"].duplicated().sum()
)


# ============================================================
# DATABASE CONNECTION
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
# CHECK TARGET TABLE
# ============================================================

cursor.execute(
    "SELECT COUNT(*) FROM patient_insurance_map"
)

existing_count = cursor.fetchone()[0]

print(
    f"\nExisting patient_insurance_map records: "
    f"{existing_count:,}"
)

if existing_count > 0:
    print(
        "\nERROR: patient_insurance_map already contains records."
    )
    print(
        "To avoid duplicate mappings, the script will stop."
    )

    cursor.close()
    connection.close()
    raise SystemExit(1)


# ============================================================
# LOAD ACTUAL DATABASE PATIENT IDs
# ============================================================

print("\nLoading valid database Patient_IDs...")

cursor.execute(
    "SELECT Patient_ID FROM patients"
)

valid_patient_ids = {
    row[0]
    for row in cursor.fetchall()
}

print(
    f"Valid patients in database: "
    f"{len(valid_patient_ids):,}"
)


# ============================================================
# LOAD ACTUAL DATABASE INSURANCE IDs
# ============================================================

print("\nLoading actual database Insurance_IDs...")

cursor.execute(
    """
    SELECT
        Insurance_ID,
        Provider_Code,
        Provider_Name,
        Insurance_Type,
        Coverage_Type,
        Status
    FROM insurance_providers
    WHERE Is_Deleted = 0
    """
)

db_insurance_rows = cursor.fetchall()

print(
    f"Insurance providers available in database: "
    f"{len(db_insurance_rows):,}"
)


if len(db_insurance_rows) == 0:
    print(
        "\nERROR: No insurance providers found in database."
    )

    cursor.close()
    connection.close()
    raise SystemExit(1)


# ============================================================
# BUILD PROVIDER LOOKUP
# ============================================================

provider_lookup = {}

for row in db_insurance_rows:

    (
        insurance_id,
        provider_code,
        provider_name,
        insurance_type,
        coverage_type,
        status
    ) = row

    provider_lookup[
        clean_text(provider_name)
    ] = {
        "Insurance_ID": insurance_id,
        "Provider_Code": provider_code,
        "Provider_Name": provider_name,
        "Insurance_Type": insurance_type,
        "Coverage_Type": coverage_type,
        "Status": status
    }


# ============================================================
# MATCH CSV PROVIDERS TO DATABASE PROVIDERS
# ============================================================

print("\nMatching source providers with database providers...")

matched_providers = []

for _, row in insurance_df.iterrows():

    provider_name = clean_text(
        row["Provider_Name"]
    )

    if provider_name in provider_lookup:

        db_provider = provider_lookup[
            provider_name
        ]

        matched_providers.append(
            {
                "Source_ID": row["Insurance_Provider_ID"],
                "Provider_Name": provider_name,
                "Insurance_ID": db_provider["Insurance_ID"],
                "Insurance_Type": db_provider["Insurance_Type"],
                "Status": db_provider["Status"]
            }
        )


print(
    f"Matched providers: "
    f"{len(matched_providers):,}"
)


if len(matched_providers) == 0:

    print(
        "\nERROR: No source providers matched database providers."
    )

    cursor.close()
    connection.close()
    raise SystemExit(1)


# ============================================================
# PREPARE PATIENTS
# ============================================================

valid_patients_df = patients_df[
    patients_df["Patient_ID"].isin(valid_patient_ids)
].copy()

print(
    f"Valid patient rows for mapping: "
    f"{len(valid_patients_df):,}"
)

invalid_patient_count = (
    len(patients_df) -
    len(valid_patients_df)
)

print(
    f"Invalid Patient_ID rows: "
    f"{invalid_patient_count:,}"
)


# ============================================================
# INSERT QUERY
# ============================================================

insert_query = """
INSERT INTO patient_insurance_map (
    Patient_ID,
    Insurance_ID,
    Policy_Number,
    Policy_Type,
    Policy_Holder_Name,
    Relationship_To_Policy_Holder,
    Plan_Name,
    Policy_Start_Date,
    Policy_End_Date,
    Policy_Status,
    Total_Coverage_Amount,
    Used_Coverage_Amount,
    Remaining_Coverage_Amount,
    Co_Payment_Percentage,
    Deductible_Amount,
    Claim_Required,
    Claim_Number,
    Claim_Status,
    Claim_Submission_Date,
    Claim_Settlement_Date,
    Claim_Amount,
    Approved_Claim_Amount,
    Rejection_Reason,
    Nominee_Name,
    Nominee_Relationship,
    TPA_Name,
    TPA_Contact_Number,
    Data_Source,
    Created_By,
    Updated_By
)
VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
)
"""


# ============================================================
# GENERATE MAPPINGS
# ============================================================

print("\nGenerating synthetic patient-insurance mappings...")

batch = []

inserted = 0
skipped = 0

provider_count = len(matched_providers)

for index, (_, patient) in enumerate(
    valid_patients_df.iterrows()
):

    patient_id = patient["Patient_ID"]

    # Deterministic provider assignment
    provider = matched_providers[
        index % provider_count
    ]

    insurance_id = provider["Insurance_ID"]

    provider_type = normalize_provider_type(
        provider["Insurance_Type"]
    )

    policy_type = normalize_policy_type(
        provider_type,
        index
    )

    policy_number = generate_policy_number(
        patient_id,
        insurance_id,
        index
    )

    policy_holder_name = (
        clean_text(patient.get("First_Name"))
        + " "
        + clean_text(patient.get("Last_Name"))
    )

    if policy_type in {
        "Individual",
        "Government Scheme"
    }:
        relationship = "Self"
    elif policy_type == "Family Floater":
        relationship = "Family"
    elif policy_type == "Corporate":
        relationship = "Employee"
    else:
        relationship = "Self"

    plan_name = normalize_plan_name(
        provider["Provider_Name"],
        provider_type,
        policy_type
    )

    start_date, end_date = generate_policy_dates(
        patient_id,
        index
    )

    seed = deterministic_hash(
        f"{patient_id}|{insurance_id}"
    )

    policy_status = determine_policy_status(
        end_date,
        seed
    )

    total_coverage = generate_coverage(
        provider_type,
        policy_type,
        seed
    )

    # Synthetic utilization
    used_percentage = (
        (seed % 31) / 100
    )

    used_coverage = round(
        total_coverage * used_percentage,
        2
    )

    remaining_coverage = round(
        max(
            total_coverage -
            used_coverage,
            0
        ),
        2
    )

    copayment = generate_copayment(
        provider_type,
        policy_type,
        seed
    )

    deductible = generate_deductible(
        total_coverage,
        seed
    )

    (
        claim_required,
        claim_number,
        claim_status,
        claim_submission_date,
        claim_settlement_date,
        claim_amount,
        approved_claim_amount,
        rejection_reason
    ) = generate_claim_information(
        policy_status,
        total_coverage,
        seed
    )

    # --------------------------------------------------------
    # Important:
    # No nominee / TPA information exists in source data.
    # Therefore these remain NULL.
    # --------------------------------------------------------

    values = (
        patient_id,
        insurance_id,
        policy_number,
        policy_type,
        policy_holder_name,
        relationship,
        plan_name,
        start_date,
        end_date,
        policy_status,
        total_coverage,
        used_coverage,
        remaining_coverage,
        copayment,
        deductible,
        claim_required,
        claim_number,
        claim_status,
        claim_submission_date,
        claim_settlement_date,
        claim_amount,
        approved_claim_amount,
        rejection_reason,
        None,       # Nominee_Name
        None,       # Nominee_Relationship
        None,       # TPA_Name
        None,       # TPA_Contact_Number
        "Synthetic",
        "ETL_55",
        "ETL_55"
    )

    batch.append(values)

    if len(batch) >= BATCH_SIZE:

        cursor.executemany(
            insert_query,
            batch
        )

        connection.commit()

        inserted += len(batch)

        print(
            f"Inserted: {inserted:,}"
        )

        batch = []


# ============================================================
# FINAL BATCH
# ============================================================

if batch:

    cursor.executemany(
        insert_query,
        batch
    )

    connection.commit()

    inserted += len(batch)


# ============================================================
# FINAL VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("STEP 55 INSERT SUMMARY")
print("=" * 70)

print(
    f"Patients in source:        {len(patients_df):,}"
)

print(
    f"Valid patients:            {len(valid_patients_df):,}"
)

print(
    f"Matched insurance providers:{len(matched_providers):,}"
)

print(
    f"Inserted mappings:          {inserted:,}"
)


# ============================================================
# DATABASE COUNT
# ============================================================

cursor.execute(
    """
    SELECT COUNT(*)
    FROM patient_insurance_map
    """
)

db_count = cursor.fetchone()[0]

print(
    f"Database mappings:          {db_count:,}"
)


# ============================================================
# BASIC VALIDATION
# ============================================================

cursor.execute(
    """
    SELECT
        COUNT(*) AS Total_Mappings,
        COUNT(DISTINCT Patient_ID) AS Unique_Patients,
        COUNT(DISTINCT Insurance_ID) AS Unique_Insurance_Providers,
        COUNT(DISTINCT Policy_Number) AS Unique_Policies,
        SUM(Patient_ID IS NULL) AS Null_Patient_ID,
        SUM(Insurance_ID IS NULL) AS Null_Insurance_ID
    FROM patient_insurance_map
    """
)

result = cursor.fetchone()

(
    total_mappings,
    unique_patients,
    unique_providers,
    unique_policies,
    null_patients,
    null_providers
) = result

print("\nBASIC VALIDATION")
print(
    f"Total mappings:            {total_mappings:,}"
)

print(
    f"Unique patients:            {unique_patients:,}"
)

print(
    f"Unique insurance providers: {unique_providers:,}"
)

print(
    f"Unique policies:            {unique_policies:,}"
)

print(
    f"NULL Patient_ID:            {null_patients}"
)

print(
    f"NULL Insurance_ID:          {null_providers}"
)


# ============================================================
# FOREIGN KEY VALIDATION
# ============================================================

cursor.execute(
    """
    SELECT COUNT(*)
    FROM patient_insurance_map p
    LEFT JOIN patients pt
        ON p.Patient_ID = pt.Patient_ID
    WHERE pt.Patient_ID IS NULL
    """
)

orphan_patients = cursor.fetchone()[0]


cursor.execute(
    """
    SELECT COUNT(*)
    FROM patient_insurance_map p
    LEFT JOIN insurance_providers i
        ON p.Insurance_ID = i.Insurance_ID
    WHERE i.Insurance_ID IS NULL
    """
)

orphan_insurance = cursor.fetchone()[0]


print("\nFOREIGN KEY VALIDATION")

print(
    f"Orphaned Patient_ID links:   {orphan_patients}"
)

print(
    f"Orphaned Insurance_ID links: {orphan_insurance}"
)


# ============================================================
# POLICY STATUS DISTRIBUTION
# ============================================================

cursor.execute(
    """
    SELECT
        Policy_Status,
        COUNT(*)
    FROM patient_insurance_map
    GROUP BY Policy_Status
    ORDER BY Policy_Status
    """
)

print("\nPOLICY STATUS")

for status, count in cursor.fetchall():

    print(
        f"{status}: {count:,}"
    )


# ============================================================
# POLICY TYPE DISTRIBUTION
# ============================================================

cursor.execute(
    """
    SELECT
        Policy_Type,
        COUNT(*)
    FROM patient_insurance_map
    GROUP BY Policy_Type
    ORDER BY Policy_Type
    """
)

print("\nPOLICY TYPE")

for policy_type, count in cursor.fetchall():

    print(
        f"{policy_type}: {count:,}"
    )


# ============================================================
# DATA SOURCE VALIDATION
# ============================================================

cursor.execute(
    """
    SELECT
        Data_Source,
        COUNT(*)
    FROM patient_insurance_map
    GROUP BY Data_Source
    """
)

print("\nDATA SOURCE")

for source, count in cursor.fetchall():

    print(
        f"{source}: {count:,}"
    )


# ============================================================
# FINAL STATUS
# ============================================================

passed = (
    inserted == len(valid_patients_df)
    and db_count == inserted
    and unique_policies == total_mappings
    and null_patients == 0
    and null_providers == 0
    and orphan_patients == 0
    and orphan_insurance == 0
)


print("\n" + "=" * 70)

if passed:
    print("STEP 55 - PATIENT INSURANCE MAPPING: PASSED")
else:
    print("STEP 55 - PATIENT INSURANCE MAPPING: FAILED")

print("=" * 70)


cursor.close()
connection.close()