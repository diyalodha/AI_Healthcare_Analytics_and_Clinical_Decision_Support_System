"""
AI Healthcare Analytics & Clinical Decision Support System
Generate prescriptions with explicit, validated Diagnosis_ID links.

Input files remain unchanged.
Output: datasets/synthetic/prescriptions_with_diagnosis.csv
"""

import os
import sys
import random
import numpy as np
import pandas as pd

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)

if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

import config
from utils import generate_uuid, show_progress


DIAGNOSIS_FILE = os.path.join(config.SYNTHETIC_DIR, "diagnoses.csv")
ADMISSION_FILE = os.path.join(config.SYNTHETIC_DIR, "admissions.csv")
MEDICATION_FILE = os.path.join(config.SYNTHETIC_DIR, "medications.csv")

OUTPUT_FILE = os.path.join(
    config.SYNTHETIC_DIR,
    "prescriptions_with_diagnosis.csv",
)

DOSAGE = ["5 mg", "10 mg", "20 mg", "50 mg", "100 mg"]
FREQUENCY = [
    "Once Daily",
    "Twice Daily",
    "Three Times Daily",
    "Before Meals",
    "After Meals",
]
DURATION = ["5 Days", "7 Days", "14 Days", "30 Days", "90 Days"]
STATUSES = ["Active", "Completed", "Discontinued"]


def normalize_ids(df, columns):
    for column in columns:
        df[column] = df[column].fillna("").astype(str).str.strip()
    return df


def generate_prescriptions():
    show_progress("Generating Prescriptions with Diagnosis_ID")

    if os.path.exists(OUTPUT_FILE):
        raise FileExistsError(
            f"Output already exists: {OUTPUT_FILE}\n"
            "No file was overwritten. Rename or back up it before retrying."
        )

    print("Loading diagnoses...")
    diagnoses = pd.read_csv(
        DIAGNOSIS_FILE,
        dtype=str,
        usecols=[
            "Diagnosis_ID",
            "Patient_ID",
            "Admission_ID",
            "Doctor_ID",
            "Diagnosis_Date",
        ],
    )

    print("Loading admissions...")
    admissions = pd.read_csv(
        ADMISSION_FILE,
        dtype=str,
        usecols=[
            "Admission_ID",
            "Patient_ID",
            "Admission_Date",
            "Discharge_Date",
        ],
    )

    print("Loading medications...")
    medications = pd.read_csv(
        MEDICATION_FILE,
        dtype=str,
        usecols=["Medication_ID", "Medication_Name", "Route"],
    )

    diagnoses = normalize_ids(
        diagnoses,
        ["Diagnosis_ID", "Patient_ID", "Admission_ID", "Doctor_ID"],
    )
    admissions = normalize_ids(
        admissions, ["Admission_ID", "Patient_ID"]
    )
    medications = normalize_ids(medications, ["Medication_ID"])

    diagnoses["Diagnosis_Date"] = pd.to_datetime(
        diagnoses["Diagnosis_Date"], errors="coerce"
    )
    admissions["Admission_Date"] = pd.to_datetime(
        admissions["Admission_Date"], errors="coerce"
    )
    admissions["Discharge_Date"] = pd.to_datetime(
        admissions["Discharge_Date"], errors="coerce"
    )

    # Reject missing IDs and dates instead of creating synthetic links.
    diagnoses = diagnoses[
        (diagnoses["Diagnosis_ID"] != "")
        & (diagnoses["Patient_ID"] != "")
        & (diagnoses["Admission_ID"] != "")
        & (diagnoses["Doctor_ID"] != "")
    ].dropna(subset=["Diagnosis_Date"])

    admissions = admissions[
        (admissions["Admission_ID"] != "")
        & (admissions["Patient_ID"] != "")
    ].dropna(subset=["Admission_Date", "Discharge_Date"])

    medications = medications[
        (medications["Medication_ID"] != "")
    ].drop_duplicates(subset=["Medication_ID"])

    if diagnoses.empty or admissions.empty or medications.empty:
        raise ValueError("A required input file has no usable records.")

    if diagnoses["Diagnosis_ID"].duplicated().any():
        raise ValueError("Duplicate Diagnosis_ID values in diagnoses.csv.")

    if admissions["Admission_ID"].duplicated().any():
        raise ValueError("Duplicate Admission_ID values in admissions.csv.")

    if medications["Medication_ID"].duplicated().any():
        raise ValueError("Duplicate Medication_ID values in medications.csv.")

    # Link using BOTH Admission_ID and Patient_ID.
    linked = diagnoses.merge(
        admissions,
        on=["Admission_ID", "Patient_ID"],
        how="inner",
        validate="many_to_one",
    )

    # Ensure diagnosis date is inside the corresponding admission window.
    linked = linked[
        (linked["Diagnosis_Date"] >= linked["Admission_Date"])
        & (linked["Diagnosis_Date"] <= linked["Discharge_Date"])
    ].copy()

    linked = linked[
        (linked["Diagnosis_ID"] != "")
        & (linked["Doctor_ID"] != "")
    ].reset_index(drop=True)

    if linked.empty:
        raise ValueError(
            "No valid diagnosis rows match their patient's admission dates."
        )

    # Confirm every linked diagnosis points to a unique diagnosis ID.
    if linked["Diagnosis_ID"].duplicated().any():
        raise ValueError(
            "A Diagnosis_ID appears more than once after linking."
        )

    print(f"Validated diagnosis-admission links: {len(linked):,}")

    valid_routes = {"Oral", "Injection", "Inhalation", "IV", "Topical"}
    medications["Route"] = medications["Route"].fillna("").str.strip()
    medications["Prescription_Route"] = medications["Route"].where(
        medications["Route"].isin(valid_routes), "Oral"
    )

    medication_ids = medications["Medication_ID"].to_numpy()
    route_lookup = dict(
        zip(medications["Medication_ID"], medications["Prescription_Route"])
    )

    total = int(config.NUM_PRESCRIPTIONS)
    chunk_size = int(config.PRESCRIPTION_CHUNK_SIZE)

    if total <= 0 or chunk_size <= 0:
        raise ValueError("Configured row count and chunk size must be positive.")

    rng = np.random.default_rng(42)
    random.seed(42)

    written = 0
    first_chunk = True

    for start in range(0, total, chunk_size):
        size = min(chunk_size, total - start)

        selected_indices = rng.integers(0, len(linked), size=size)
        selected = linked.iloc[selected_indices].reset_index(drop=True)

        medication_sample = rng.choice(
            medication_ids, size=size, replace=True
        )

        records = []

        for i in range(size):
            diagnosis_date = selected.at[i, "Diagnosis_Date"]
            discharge_date = selected.at[i, "Discharge_Date"]

            available_days = max(
                0, (discharge_date - diagnosis_date).days
            )
            offset_days = random.randint(0, available_days)
            prescription_date = (
                diagnosis_date + pd.Timedelta(days=offset_days)
            ).date()

            medication_id = medication_sample[i]

            records.append({
                "Prescription_ID": generate_uuid(),
                "Diagnosis_ID": selected.at[i, "Diagnosis_ID"],
                "Patient_ID": selected.at[i, "Patient_ID"],
                "Admission_ID": selected.at[i, "Admission_ID"],
                "Doctor_ID": selected.at[i, "Doctor_ID"],
                "Medication_ID": medication_id,
                "Dosage": random.choice(DOSAGE),
                "Frequency": random.choice(FREQUENCY),
                "Duration": random.choice(DURATION),
                "Route": route_lookup[medication_id],
                "Prescription_Status": random.choice(STATUSES),
                "Prescription_Date": str(prescription_date),
                "Notes": (
                    "Synthetic prescription linked to an explicit diagnosis "
                    "and matching patient admission. Clinical appropriateness "
                    "requires validation."
                ),
            })

        chunk_df = pd.DataFrame(records)

        chunk_df.to_csv(
            OUTPUT_FILE,
            mode="w" if first_chunk else "a",
            header=first_chunk,
            index=False,
        )

        first_chunk = False
        written += len(chunk_df)
        print(f"Written {written:,} / {total:,} prescriptions")

    if written != total:
        raise RuntimeError(f"Expected {total:,} records; wrote {written:,}.")

    print("\nGeneration completed.")
    print(f"Total records: {written:,}")
    print(f"Output file: {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_prescriptions()
