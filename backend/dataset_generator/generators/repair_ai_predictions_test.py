from pathlib import Path
import random
import uuid

import numpy as np
import pandas as pd

BASE = Path("datasets/synthetic")
OUTPUT = BASE / "test_output" / "ai_predictions_test.csv"
TARGET_ROWS = 500_000
SEED = 42

PREDICTION_COLUMNS = [
    "AI_Prediction_ID",
    "Patient_ID",
    "Diagnosis_ID",
    "Prediction_Type",
    "Model_Name",
    "Risk_Score",
    "Prediction_Result",
    "Confidence_Score",
    "Input_Vital_ID",
    "Input_Lab_Result_ID",
    "Prediction_Date",
    "Clinical_Recommendation",
]

def require_columns(df, columns, filename):
    missing = sorted(set(columns) - set(df.columns))
    if missing:
        raise ValueError(f"{filename} is missing columns: {missing}")

def main():
    rng = np.random.default_rng(SEED)
    random.seed(SEED)

    print("Reading required source columns...")

    diagnoses = pd.read_csv(
        BASE / "diagnoses.csv",
        dtype={
            "Diagnosis_ID": "string",
            "Patient_ID": "string",
            "Disease_ID": "string",
        },
        usecols=[
            "Diagnosis_ID", "Patient_ID", "Disease_ID",
            "Diagnosis_Date", "Diagnosis_Status", "Severity",
        ],
    )

    diseases = pd.read_csv(
        BASE / "diseases.csv",
        dtype={"Disease_ID": "string"},
        usecols=["Disease_ID", "Disease_Category"],
    )

    vitals = pd.read_csv(
        BASE / "vital_signs.csv",
        dtype={"Vital_Sign_ID": "string", "Patient_ID": "string"},
        usecols=["Vital_Sign_ID", "Patient_ID", "Recorded_Time"],
    )

    labs = pd.read_csv(
        BASE / "lab_results.csv",
        dtype={"Lab_Result_ID": "string", "Patient_ID": "string"},
        usecols=["Lab_Result_ID", "Patient_ID"],
    )

    for df, cols, name in [
        (diagnoses, ["Diagnosis_ID", "Patient_ID", "Disease_ID",
                     "Diagnosis_Status", "Severity"], "diagnoses.csv"),
        (diseases, ["Disease_ID", "Disease_Category"], "diseases.csv"),
        (vitals, ["Vital_Sign_ID", "Patient_ID", "Recorded_Time"],
         "vital_signs.csv"),
        (labs, ["Lab_Result_ID", "Patient_ID"], "lab_results.csv"),
    ]:
        require_columns(df, cols, name)

    # Use only diagnoses whose disease category can be resolved.
    diagnoses = diagnoses.merge(
        diseases.drop_duplicates("Disease_ID"),
        on="Disease_ID",
        how="left",
        validate="many_to_one",
    )

    diagnoses = diagnoses.dropna(
        subset=["Diagnosis_ID", "Patient_ID", "Disease_Category"]
    )
    diagnoses = diagnoses[
        diagnoses["Diagnosis_Status"].isin(
            ["Confirmed", "Under Evaluation"]
        )
    ].copy()

    # Build per-patient row-index lookups; IDs are never selected
    # independently of their patient.
    print("Building patient-specific lookups...")

    diagnosis_groups = {
        patient_id: group.index.to_numpy()
        for patient_id, group in diagnoses.groupby("Patient_ID", sort=False)
    }

    vital_groups = {
        patient_id: group.index.to_numpy()
        for patient_id, group in vitals.groupby("Patient_ID", sort=False)
    }

    lab_groups = {
        patient_id: group.index.to_numpy()
        for patient_id, group in labs.groupby("Patient_ID", sort=False)
    }

    eligible = sorted(
        set(diagnosis_groups)
        & set(vital_groups)
        & set(lab_groups)
    )

    if not eligible:
        raise RuntimeError(
            "No patients have an eligible diagnosis, vital sign, and lab result."
        )

    if not len(diagnoses) or not len(vitals) or not len(labs):
        raise RuntimeError("One or more required source datasets are empty.")

    print(f"Eligible patients: {len(eligible):,}")
    print(f"Generating {TARGET_ROWS:,} test rows...")

    patient_choices = rng.choice(eligible, size=TARGET_ROWS, replace=True)
    records = []

    for i, patient_id in enumerate(patient_choices):
        d_idx = int(rng.choice(diagnosis_groups[patient_id]))
        v_idx = int(rng.choice(vital_groups[patient_id]))
        l_idx = int(rng.choice(lab_groups[patient_id]))

        diagnosis = diagnoses.loc[d_idx]
        vital = vitals.loc[v_idx]
        lab = labs.loc[l_idx]

        category = str(diagnosis["Disease_Category"]).strip().lower()

        if category == "endocrine":
            prediction_type = "Diabetes Risk Prediction"
        elif category == "cardiovascular":
            prediction_type = "Cardiac Disease Risk Prediction"
        elif category == "renal":
            prediction_type = "Kidney Disease Risk Prediction"
        elif category == "respiratory":
            prediction_type = "Respiratory Disease Risk Prediction"
        else:
            prediction_type = random.choice([
                "Hospital Readmission Risk",
                "ICU Admission Risk",
                "Mortality Risk Prediction",
            ])

        # Explicitly synthetic demo values, not model predictions.
        risk_score = round(float(rng.uniform(0.05, 0.95)), 3)
        prediction_result = (
            "High Risk" if risk_score > 0.70
            else "Medium Risk" if risk_score > 0.40
            else "Low Risk"
        )

        records.append({
            "AI_Prediction_ID": str(uuid.uuid4()),
            "Patient_ID": patient_id,
            "Diagnosis_ID": diagnosis["Diagnosis_ID"],
            "Prediction_Type": prediction_type,
            "Model_Name": "Synthetic Demo Generator",
            "Risk_Score": risk_score,
            "Prediction_Result": prediction_result,
            "Confidence_Score": round(float(rng.uniform(0.70, 0.99)), 3),
            "Input_Vital_ID": vital["Vital_Sign_ID"],
            "Input_Lab_Result_ID": lab["Lab_Result_ID"],
            "Prediction_Date": vital["Recorded_Time"],
            "Clinical_Recommendation": (
                "Synthetic demonstration record only. "
                "Requires review by an authorized clinician."
            ),
        })

        if (i + 1) % 50000 == 0:
            print(f"Generated {i + 1:,} / {TARGET_ROWS:,}")

    result = pd.DataFrame(records, columns=PREDICTION_COLUMNS)

    # Source-level relationship checks before writing.
    diagnosis_patient = diagnoses.set_index("Diagnosis_ID")["Patient_ID"]
    vital_patient = vitals.set_index("Vital_Sign_ID")["Patient_ID"]
    lab_patient = labs.set_index("Lab_Result_ID")["Patient_ID"]

    if result["AI_Prediction_ID"].duplicated().any():
        raise RuntimeError("Duplicate prediction IDs detected.")

    linked_diagnosis_patient = result["Diagnosis_ID"].map(diagnosis_patient)
    linked_vital_patient = result["Input_Vital_ID"].map(vital_patient)
    linked_lab_patient = result["Input_Lab_Result_ID"].map(lab_patient)

    checks = {
        "Diagnosis belongs to prediction patient":
            linked_diagnosis_patient.eq(result["Patient_ID"]).all(),
        "Vital belongs to prediction patient":
            linked_vital_patient.eq(result["Patient_ID"]).all(),
        "Lab result belongs to prediction patient":
            linked_lab_patient.eq(result["Patient_ID"]).all(),
        "All output columns preserved":
            list(result.columns) == PREDICTION_COLUMNS,
        "Prediction IDs unique":
            result["AI_Prediction_ID"].is_unique,
    }

    print("\nVALIDATION")
    for name, passed in checks.items():
        print(f"{'PASS' if passed else 'FAIL'}: {name}")

    if not all(checks.values()):
        raise RuntimeError("Validation failed; output was not written.")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT, index=False)

    print(f"\nTEST FILE CREATED: {OUTPUT}")
    print(f"Rows: {len(result):,}")
    print("Original ai_predictions.csv was not changed.")
    print(
        "Reminder: scores are synthetic placeholders, "
        "not clinically validated predictions."
    )

if __name__ == "__main__":
    main()
