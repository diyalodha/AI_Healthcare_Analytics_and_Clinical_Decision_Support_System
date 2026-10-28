
"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File    : generate_prescriptions.py
Purpose : Generate referentially consistent prescriptions.

Output  : prescriptions_corrected.csv
Records : config.NUM_PRESCRIPTIONS (800000)

Author  : Diya Lodha & Team
===========================================================
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


# ==========================================================
# Input files
# ==========================================================

DIAGNOSIS_FILE = os.path.join(
    config.SYNTHETIC_DIR, "diagnoses.csv"
)

ADMISSION_FILE = os.path.join(
    config.SYNTHETIC_DIR, "admissions.csv"
)

MEDICATION_FILE = os.path.join(
    config.SYNTHETIC_DIR, "medications.csv"
)

OUTPUT_FILE = os.path.join(
    config.SYNTHETIC_DIR, "prescriptions_corrected.csv"
)


# ==========================================================
# Prescription values
# ==========================================================

DOSAGE = ["5 mg", "10 mg", "20 mg", "50 mg", "100 mg"]

FREQUENCY = [
    "Once Daily",
    "Twice Daily",
    "Three Times Daily",
    "Before Meals",
    "After Meals",
]

DURATION = ["5 Days", "7 Days", "14 Days", "30 Days", "90 Days"]

ROUTES = ["Oral", "Injection", "IV", "Topical"]

STATUSES = ["Active", "Completed", "Discontinued"]


# ==========================================================
# Generate prescriptions
# ==========================================================

def generate_prescriptions():

    show_progress("Generating Corrected Prescription Dataset")

    # Never overwrite the original or a previous corrected file.
    if os.path.exists(OUTPUT_FILE):
        raise FileExistsError(
            f"Output already exists: {OUTPUT_FILE}\n"
            "Rename or back up that file before generating again."
        )

    print("Loading diagnoses...")
    diagnoses = pd.read_csv(
        DIAGNOSIS_FILE,
        dtype=str,
        usecols=[
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

    # Normalize identifiers before joining.
    for column in ["Patient_ID", "Admission_ID", "Doctor_ID"]:
        diagnoses[column] = diagnoses[column].str.strip()

    for column in ["Patient_ID", "Admission_ID"]:
        admissions[column] = admissions[column].str.strip()

    medications["Medication_ID"] = (
        medications["Medication_ID"].str.strip()
    )

    # Parse dates and reject invalid source records.
    diagnoses["Diagnosis_Date"] = pd.to_datetime(
        diagnoses["Diagnosis_Date"], errors="coerce"
    )

    admissions["Admission_Date"] = pd.to_datetime(
        admissions["Admission_Date"], errors="coerce"
    )

    admissions["Discharge_Date"] = pd.to_datetime(
        admissions["Discharge_Date"], errors="coerce"
    )

    diagnoses.dropna(
        subset=[
            "Patient_ID",
            "Admission_ID",
            "Doctor_ID",
            "Diagnosis_Date",
        ],
        inplace=True,
    )

    admissions.dropna(
        subset=[
            "Patient_ID",
            "Admission_ID",
            "Admission_Date",
            "Discharge_Date",
        ],
        inplace=True,
    )

    medications.dropna(
        subset=["Medication_ID"],
        inplace=True,
    )

    if diagnoses.empty or admissions.empty or medications.empty:
        raise ValueError(
            "A required input file has no usable records."
        )

    # One admission ID should identify one patient/admission pair.
    duplicate_admissions = admissions["Admission_ID"].duplicated()
    if duplicate_admissions.any():
        raise ValueError(
            "Duplicate Admission_ID values found in admissions.csv. "
            "Resolve these before generating prescriptions."
        )

    # Match both IDs to ensure the admission belongs to the patient.
    linked = diagnoses.merge(
        admissions,
        on=["Admission_ID", "Patient_ID"],
        how="inner",
        validate="many_to_one",
    )

    # Only diagnoses within the admission window are eligible.
    linked = linked[
        (linked["Diagnosis_Date"] >= linked["Admission_Date"])
        & (linked["Diagnosis_Date"] <= linked["Discharge_Date"])
    ].copy()

    linked.dropna(
        subset=["Patient_ID", "Admission_ID", "Doctor_ID"],
        inplace=True,
    )

    linked.reset_index(drop=True, inplace=True)

    if linked.empty:
        raise ValueError(
            "No diagnoses matched valid patient-admission records."
        )

    if medications["Medication_ID"].nunique() == 0:
        raise ValueError("No valid medication IDs found.")

    print(f"Valid linked diagnosis rows: {len(linked):,}")

    # Use each medication's master-data route when available.
    valid_routes = {"Oral", "Injection", "Inhalation", "IV", "Topical"}
    medication_routes = medications["Route"].fillna("").str.strip()

    medications["Prescription_Route"] = medication_routes.where(
        medication_routes.isin(valid_routes),
        "Oral",
    )

    medication_ids = medications["Medication_ID"].to_numpy()
    medication_route_by_id = dict(
        zip(
            medications["Medication_ID"],
            medications["Prescription_Route"],
        )
    )

    total = int(config.NUM_PRESCRIPTIONS)
    chunk_size = int(config.PRESCRIPTION_CHUNK_SIZE)

    if total <= 0 or chunk_size <= 0:
        raise ValueError(
            "NUM_PRESCRIPTIONS and PRESCRIPTION_CHUNK_SIZE must be positive."
        )

    rng = np.random.default_rng(42)
    random.seed(42)

    written = 0
    first_chunk = True

    try:
        for start in range(0, total, chunk_size):

            size = min(chunk_size, total - start)

            # Reuse valid diagnosis/admission links when needed to reach
            # the configured target of 800,000 prescriptions.
            selected_indices = rng.integers(
                0, len(linked), size=size
            )
            selected = linked.iloc[selected_indices].reset_index(drop=True)

            medication_sample = rng.choice(
                medication_ids, size=size, replace=True
            )

            records = []

            for i in range(size):

                diagnosis_date = selected.at[i, "Diagnosis_Date"]
                discharge_date = selected.at[i, "Discharge_Date"]

                # Choose a prescription date from diagnosis date through
                # discharge date, inclusive.
                available_days = (
                    discharge_date - diagnosis_date
                ).days

                offset_days = random.randint(
                    0, max(0, available_days)
                )

                prescription_date = (
                    diagnosis_date + pd.Timedelta(days=offset_days)
                ).date()

                medication_id = medication_sample[i]

                records.append({
                    "Prescription_ID": generate_uuid(),
                    "Patient_ID": selected.at[i, "Patient_ID"],
                    "Admission_ID": selected.at[i, "Admission_ID"],
                    "Doctor_ID": selected.at[i, "Doctor_ID"],
                    "Medication_ID": medication_id,
                    "Dosage": random.choice(DOSAGE),
                    "Frequency": random.choice(FREQUENCY),
                    "Duration": random.choice(DURATION),
                    "Route": medication_route_by_id[medication_id],
                    "Prescription_Status": random.choice(STATUSES),
                    "Prescription_Date": str(prescription_date),
                    "Notes": (
                        "Synthetic prescription linked to a valid "
                        "patient diagnosis and admission; clinical "
                        "appropriateness requires validation."
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
            raise RuntimeError(
                f"Expected {total:,} rows but wrote {written:,}."
            )

    except Exception:
        # Keep any partial output for inspection rather than silently
        # deleting potentially useful diagnostic data.
        print(
            f"Generation failed. Inspect partial output: {OUTPUT_FILE}"
        )
        raise

    print("\nPrescription generation completed.")
    print(f"Total records: {written:,}")
    print(f"Output file: {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_prescriptions()
