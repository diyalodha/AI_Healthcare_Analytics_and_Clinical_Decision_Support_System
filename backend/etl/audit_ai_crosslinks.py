
import os
import sys
from pathlib import Path

import pandas as pd
import mysql.connector

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "datasets" / "synthetic"
CHUNK_SIZE = 50_000
DB_BATCH_SIZE = 1_000

FILES = {
    "predictions": DATA / "ai_predictions.csv",
    "recommendations": DATA / "ai_recommendations.csv",
    "explainability": DATA / "explainable_ai.csv",
}


def read_csv(path, **kwargs):
    return pd.read_csv(
        path, dtype=str, keep_default_na=False, **kwargs
    )


def main():
    password = os.environ.get("MYSQL_PASSWORD")
    if not password:
        sys.exit("ERROR: MYSQL_PASSWORD is missing in this PowerShell session.")

    for path in FILES.values():
        if not path.is_file():
            sys.exit(f"ERROR: File not found: {path}")

    print("=" * 70)
    print("FULL PATIENT AND AI CROSS-LINK AUDIT")
    print("READ-ONLY: no database records will be modified")
    print("=" * 70)

    # Build a complete prediction ID -> patient ID mapping.
    prediction_map = {}
    prediction_rows = 0

    for chunk in read_csv(
        FILES["predictions"], chunksize=CHUNK_SIZE
    ):
        prediction_rows += len(chunk)

        for prediction_id, patient_id in zip(
            chunk["AI_Prediction_ID"].str.strip(),
            chunk["Patient_ID"].str.strip(),
        ):
            if prediction_id:
                prediction_map[prediction_id] = patient_id

    print(f"\nPrediction rows: {prediction_rows:,}")
    print(f"Unique prediction IDs: {len(prediction_map):,}")

    source_patients = {
        patient_id
        for patient_id in prediction_map.values()
        if patient_id
    }
    print(f"Unique prediction patient IDs: {len(source_patients):,}")

    # Check linked patient IDs in recommendations and explainability.
    for label, path in [
        ("RECOMMENDATIONS", FILES["recommendations"]),
        ("EXPLAINABILITY", FILES["explainability"]),
    ]:
        total = linked = patient_matches = patient_mismatches = 0
        missing_prediction = blank_patient = 0

        for chunk in read_csv(path, chunksize=CHUNK_SIZE):
            total += len(chunk)

            for prediction_id, patient_id in zip(
                chunk["AI_Prediction_ID"].str.strip(),
                chunk["Patient_ID"].str.strip(),
            ):
                expected_patient = prediction_map.get(prediction_id)

                if not prediction_id or prediction_id not in prediction_map:
                    missing_prediction += 1
                    continue

                linked += 1

                if not patient_id:
                    blank_patient += 1
                elif patient_id == expected_patient:
                    patient_matches += 1
                else:
                    patient_mismatches += 1

        print(f"\n{label}")
        print(f"Rows: {total:,}")
        print(f"Linked to an existing prediction: {linked:,}")
        print(f"Missing prediction reference: {missing_prediction:,}")
        print(f"Patient IDs matching linked prediction: {patient_matches:,}")
        print(f"Patient ID mismatches: {patient_mismatches:,}")
        print(f"Blank patient IDs among linked rows: {blank_patient:,}")

    # Verify every unique prediction patient ID exists in MySQL.
    print("\n" + "-" * 70)
    print("DATABASE PATIENT EXISTENCE CHECK")
    print("-" * 70)

    conn = None
    cur = None

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=password,
            database="healthcare_ai_db",
        )
        cur = conn.cursor()

        existing_patients = set()
        patient_list = list(source_patients)

        for start in range(0, len(patient_list), DB_BATCH_SIZE):
            batch = patient_list[start:start + DB_BATCH_SIZE]
            placeholders = ",".join(["%s"] * len(batch))

            cur.execute(
                "SELECT Patient_ID FROM patients "
                f"WHERE Patient_ID IN ({placeholders})",
                batch,
            )
            existing_patients.update(row[0] for row in cur.fetchall())

            checked = min(start + len(batch), len(patient_list))
            print(
                f"\rPatient IDs checked: {checked:,}/{len(patient_list):,}",
                end="",
                flush=True,
            )

        missing = source_patients - existing_patients

        print("\n")
        print(f"Unique source patients: {len(source_patients):,}")
        print(f"Patients found in database: {len(existing_patients):,}")
        print(f"Patients missing from database: {len(missing):,}")

        if missing:
            print("Sample missing Patient_ID values (maximum 10):")
            for patient_id in list(missing)[:10]:
                print(f"  {patient_id}")

    except mysql.connector.Error as exc:
        print(f"\nMySQL audit failed: {exc}")
        sys.exit(1)

    finally:
        if cur is not None:
            cur.close()
        if conn is not None and conn.is_connected():
            conn.close()

    print("\n" + "=" * 70)
    print("AUDIT COMPLETE — NO INSERT, UPDATE, OR DELETE EXECUTED")
    print("=" * 70)


if __name__ == "__main__":
    main()
