
import os
import sys
import hashlib
from pathlib import Path

import pandas as pd
import mysql.connector


# =========================================================
# CONFIGURATION
# =========================================================
PROJECT_ROOT = Path(__file__).resolve().parents[2]

CSV_PATH = PROJECT_ROOT / "datasets" / "synthetic" / "health_scores_repaired.csv"
REJECT_PATH = PROJECT_ROOT / "backend" / "etl" / "71_health_scores_rejected.csv"

CHUNK_SIZE = 5000
INSERT_BATCH_SIZE = 1000
LOOKUP_BATCH_SIZE = 500
DATASET_VERSION = "synthetic-v1"

REQUIRED_COLUMNS = [
    "Health_Score_ID",
    "Patient_ID",
    "Vital_Sign_ID",
    "Lab_Result_ID",
    "Overall_Health_Score",
    "Risk_Level",
    "Blood_Pressure_Status",
    "BMI_Category",
    "Chronic_Disease_Status",
    "Monitoring_Required",
    "Generated_Date",
]

VALID_RISK_LEVELS = {"Low", "Medium", "High", "Critical"}


# =========================================================
# DATABASE
# =========================================================
def connect_db():
    password = os.environ.get("MYSQL_PASSWORD")

    if not password:
        raise RuntimeError(
            "MYSQL_PASSWORD is missing. Set it in PowerShell."
        )

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=password,
        database="healthcare_ai_db",
        autocommit=False,
    )


# =========================================================
# HELPERS
# =========================================================
def clean_text(value):
    if pd.isna(value):
        return None

    value = str(value).strip()
    return value if value else None


def make_score_number(source_id):
    digest = hashlib.sha256(
        source_id.encode("utf-8")
    ).hexdigest()[:24]

    return f"HS-{digest}"


def lookup_existing_ids(cursor, table, column, ids):
    found = set()

    ids = [
        str(value)
        for value in ids
        if value is not None and not pd.isna(value)
    ]

    for start in range(0, len(ids), LOOKUP_BATCH_SIZE):
        batch = ids[start:start + LOOKUP_BATCH_SIZE]
        if not batch:
            continue

        placeholders = ",".join(["%s"] * len(batch))

        cursor.execute(
            f"SELECT `{column}` FROM `{table}` "
            f"WHERE `{column}` IN ({placeholders})",
            tuple(batch),
        )

        found.update(str(row[0]) for row in cursor.fetchall())

    return found


def lookup_patient_map(cursor, table, id_column, ids):
    """
    Return clinical_record_id -> Patient_ID.

    vital_signs uses Vital_Record_ID as its actual primary key.
    """
    result = {}

    ids = [
        str(value)
        for value in ids
        if value is not None and not pd.isna(value)
    ]

    for start in range(0, len(ids), LOOKUP_BATCH_SIZE):
        batch = ids[start:start + LOOKUP_BATCH_SIZE]
        if not batch:
            continue

        placeholders = ",".join(["%s"] * len(batch))

        cursor.execute(
            f"SELECT `{id_column}`, `Patient_ID` "
            f"FROM `{table}` "
            f"WHERE `{id_column}` IN ({placeholders})",
            tuple(batch),
        )

        for record_id, patient_id in cursor.fetchall():
            result[str(record_id)] = str(patient_id)

    return result


def write_rejection_report(rejected):
    if rejected:
        pd.DataFrame(rejected).to_csv(REJECT_PATH, index=False)
        print(f"Rejection report: {REJECT_PATH}")
    else:
        if REJECT_PATH.exists():
            REJECT_PATH.unlink()
        print("Rejected source rows: 0")


# =========================================================
# MAIN
# =========================================================
def main():
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"CSV not found: {CSV_PATH}")

    if not os.environ.get("MYSQL_PASSWORD"):
        raise RuntimeError(
            "MYSQL_PASSWORD is missing. Set it in PowerShell."
        )

    print("Reading health-score CSV...")

    df = pd.read_csv(
        CSV_PATH,
        dtype={
            "Health_Score_ID": str,
            "Patient_ID": str,
            "Vital_Sign_ID": str,
            "Lab_Result_ID": str,
        },
        keep_default_na=False,
    )

    missing_columns = sorted(set(REQUIRED_COLUMNS) - set(df.columns))
    if missing_columns:
        raise ValueError(f"Missing CSV columns: {missing_columns}")

    df["Health_Score_ID"] = df["Health_Score_ID"].map(clean_text)

    if df["Health_Score_ID"].isna().any():
        raise ValueError("Missing Health_Score_ID values in source CSV.")

    if df["Health_Score_ID"].duplicated().any():
        raise ValueError("Duplicate Health_Score_ID values in source CSV.")

    df = df[REQUIRED_COLUMNS].copy()

    for column in [
        "Patient_ID",
        "Vital_Sign_ID",
        "Lab_Result_ID",
        "Risk_Level",
        "Blood_Pressure_Status",
        "BMI_Category",
        "Chronic_Disease_Status",
        "Monitoring_Required",
    ]:
        df[column] = df[column].map(clean_text)

    df["Overall_Health_Score"] = pd.to_numeric(
        df["Overall_Health_Score"], errors="coerce"
    )

    df["Generated_Date"] = pd.to_datetime(
        df["Generated_Date"], errors="coerce"
    )

    print(f"Source rows: {len(df):,}")
    print("Connecting to MySQL...")

    conn = connect_db()
    cursor = conn.cursor()

    inserted = 0
    skipped = 0
    rejected = []
    processed = 0

    insert_sql = """
        INSERT INTO patient_health_score (
            Health_Score_ID,
            Patient_ID,
            Health_Score_Number,
            Score_Date,
            Overall_Health_Score,
            AI_Risk_Level,
            Major_Risk_Factors,
            Improvement_Suggestions,
            Reviewed_By_Doctor,
            Data_Source,
            Dataset_Version,
            Is_Active,
            Is_Deleted,
            Record_Version,
            Created_By
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s,
            0, 'Synthetic', %s, 1, 0, 1, %s
        )
    """

    try:
        cursor.execute("SELECT COUNT(*) FROM patient_health_score")
        initial_count = int(cursor.fetchone()[0])

        print(f"Existing destination rows: {initial_count:,}")

        for start in range(0, len(df), CHUNK_SIZE):
            chunk = df.iloc[start:start + CHUNK_SIZE].copy()

            patient_ids = chunk["Patient_ID"].dropna().unique().tolist()
            vital_ids = chunk["Vital_Sign_ID"].dropna().unique().tolist()
            lab_ids = chunk["Lab_Result_ID"].dropna().unique().tolist()
            source_ids = chunk["Health_Score_ID"].dropna().unique().tolist()

            valid_patients = lookup_existing_ids(
                cursor, "patients", "Patient_ID", patient_ids
            )

            # Correct schema column: Vital_Record_ID
            vital_patient_map = lookup_patient_map(
                cursor, "vital_signs", "Vital_Record_ID", vital_ids
            )

            lab_patient_map = lookup_patient_map(
                cursor, "lab_results", "Lab_Result_ID", lab_ids
            )

            existing_scores = lookup_existing_ids(
                cursor,
                "patient_health_score",
                "Health_Score_ID",
                source_ids,
            )

            generated_numbers = [
                make_score_number(source_id) for source_id in source_ids
            ]

            existing_numbers = lookup_existing_ids(
                cursor,
                "patient_health_score",
                "Health_Score_Number",
                generated_numbers,
            )

            pending = []

            for _, row in chunk.iterrows():
                processed += 1

                source_id = row["Health_Score_ID"]
                patient_id = row["Patient_ID"]
                vital_id = row["Vital_Sign_ID"]
                lab_id = row["Lab_Result_ID"]

                reason = None

                if not patient_id or not vital_id:
                    reason = "Missing required patient/vital ID"

                elif source_id in existing_scores:
                    skipped += 1
                    continue

                elif patient_id not in valid_patients:
                    reason = "Patient_ID not found in patients"

                elif vital_id not in vital_patient_map:
                    reason = (
                        "Vital_Sign_ID not found using Vital_Record_ID"
                    )

                elif vital_patient_map[vital_id] != patient_id:
                    reason = "Vital record belongs to a different patient"

                elif (
                    pd.notna(lab_id)
                    and str(lab_id).strip() != ""
                    and str(lab_id).strip().lower() != "nan"
                    and lab_id not in lab_patient_map
                ):
                    reason = "Lab_Result_ID not found in lab_results"

                elif (
                    pd.notna(lab_id)
                    and str(lab_id).strip() != ""
                    and str(lab_id).strip().lower() != "nan"
                    and lab_patient_map[lab_id] != patient_id
                ):
                    reason = "Lab result belongs to a different patient"

                score = row["Overall_Health_Score"]

                if reason is None and (
                    pd.isna(score) or not 0 <= float(score) <= 100
                ):
                    reason = "Overall_Health_Score outside 0-100 range"

                risk = row["Risk_Level"]

                if reason is None and risk not in VALID_RISK_LEVELS:
                    reason = f"Unsupported Risk_Level: {risk}"

                score_date = row["Generated_Date"]

                if reason is None and pd.isna(score_date):
                    reason = "Invalid Generated_Date"

                score_number = (
                    make_score_number(source_id) if source_id else None
                )

                if reason is None and score_number in existing_numbers:
                    reason = "Health_Score_Number already exists"

                monitoring = row["Monitoring_Required"]
                monitoring_normalized = (
                    monitoring.lower() if monitoring is not None else ""
                )

                if reason is None and monitoring_normalized not in {
                    "true", "false", "1", "0", "yes", "no"
                }:
                    reason = "Unrecognized Monitoring_Required value"

                if reason is not None:
                    rejected.append({
                        **row.to_dict(),
                        "Rejection_Reason": reason,
                    })
                    continue

                bp_status = (
                    row["Blood_Pressure_Status"] or "Not supplied"
                )
                bmi_category = row["BMI_Category"] or "Not supplied"
                chronic_status = (
                    row["Chronic_Disease_Status"] or "Not supplied"
                )

                risk_factors = (
                    f"Source blood-pressure status: {bp_status}; "
                    f"source BMI category: {bmi_category}; "
                    f"source chronic-disease status: {chronic_status}"
                )

                if monitoring_normalized in {"true", "1", "yes"}:
                    suggestions = (
                        "Monitoring is indicated by the source dataset."
                    )
                else:
                    suggestions = None

                pending.append((
                    source_id,
                    patient_id,
                    score_number,
                    score_date.to_pydatetime(),
                    round(float(score), 2),
                    risk,
                    risk_factors,
                    suggestions,
                    DATASET_VERSION,
                    f"SRC:{source_id}",
                ))

                existing_scores.add(source_id)
                existing_numbers.add(score_number)

                if len(pending) >= INSERT_BATCH_SIZE:
                    cursor.executemany(insert_sql, pending)
                    conn.commit()
                    inserted += len(pending)
                    pending.clear()

            if pending:
                cursor.executemany(insert_sql, pending)
                conn.commit()
                inserted += len(pending)

            print(
                f"Processed {min(start + CHUNK_SIZE, len(df)):,}/"
                f"{len(df):,} | inserted: {inserted:,} | "
                f"skipped: {skipped:,} | rejected: {len(rejected):,}"
            )

        write_rejection_report(rejected)

        cursor.execute("SELECT COUNT(*) FROM patient_health_score")
        final_count = int(cursor.fetchone()[0])

        print("\n========== HEALTH SCORE LOAD FINISHED ==========")
        print(f"Source rows: {len(df):,}")
        print(f"Processed rows: {processed:,}")
        print(f"Inserted this run: {inserted:,}")
        print(f"Already imported/skipped: {skipped:,}")
        print(f"Rejected source rows: {len(rejected):,}")
        print(f"Initial destination rows: {initial_count:,}")
        print(f"Final destination rows: {final_count:,}")
        print("No disease, doctor, or prediction-session links were invented.")
        print("Doctor review remains unconfirmed.")
        print("Vital/lab references were checked for patient consistency.")

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"\nERROR: {exc}")
        sys.exit(1)
