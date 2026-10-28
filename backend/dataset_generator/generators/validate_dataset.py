"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File : validate_dataset.py

Purpose :
Validate synthetic dataset integrity.

Checks:
1. Duplicate Rows
2. Primary Key Duplicates
3. Missing Values
4. Foreign Key Integrity

Author : Diya Lodha & Team
===========================================================
"""

import os
import sys
import pandas as pd

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)

if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

import config

# ==========================================================
# Dataset Folder
# ==========================================================

DATASET_DIR = config.SYNTHETIC_DIR


# ==========================================================
# Load CSV
# ==========================================================

def load(filename):
    return pd.read_csv(
        os.path.join(DATASET_DIR, filename)
    )


# ==========================================================
# Load Datasets
# ==========================================================

patients = load("patients.csv")
departments = load("departments.csv")
doctors = load("doctors.csv")
diseases = load("diseases.csv")
admissions = load("admissions.csv")
diagnoses = load("diagnoses.csv")
vitals = load("vital_signs.csv")
labs = load("lab_results.csv")
procedures = load("medical_procedures.csv")
prescriptions = load("prescriptions.csv")
clinical_notes = load("clinical_notes.csv")
icu = load("icu_stays.csv")
discharge = load("discharge_summary.csv")
imaging = load("imaging_reports.csv")
images = load("medical_images_metadata.csv")
predictions = load("ai_predictions.csv")
recommendations = load("ai_recommendations.csv")
health = load("health_scores.csv")
xai = load("explainable_ai.csv")
allergies = load("patient_allergies.csv")
vaccinations = load("vaccination_history.csv")
rooms = load("hospital_rooms.csv")
beds = load("beds.csv")
insurance = load("insurance_providers.csv")
medications = load("medications.csv")


# ==========================================================
# Helper Functions
# ==========================================================

def check_pk(df, name):
    pk = df.columns[0]
    dup = df[pk].duplicated().sum()

    print(
        f"{name:<30} PK Duplicates : {dup}"
    )


def check_duplicates(df, name):
    dup = df.duplicated().sum()

    print(
        f"{name:<30} Duplicate Rows : {dup}"
    )


def check_nulls(df, name):
    nulls = df.isnull().sum().sum()

    print(
        f"{name:<30} Missing Values : {nulls}"
    )


def check_fk(child,
             child_col,
             parent,
             parent_col,
             relation):

    invalid = (
        ~child[child_col].isin(
            parent[parent_col]
        )
    ).sum()

    if invalid == 0:

        print(
            f"{relation:<45} PASS"
        )

    else:

        print(
            f"{relation:<45} FAIL ({invalid})"
        )


print("=" * 80)
print("PRIMARY KEY CHECK")
print("=" * 80)

datasets = [
    ("Patients", patients),
    ("Departments", departments),
    ("Doctors", doctors),
    ("Diseases", diseases),
    ("Admissions", admissions),
    ("Diagnoses", diagnoses),
    ("Vital Signs", vitals),
    ("Lab Results", labs),
    ("Medical Procedures", procedures),
    ("Prescriptions", prescriptions),
    ("Clinical Notes", clinical_notes),
    ("ICU Stays", icu),
    ("Discharge Summary", discharge),
    ("Imaging Reports", imaging),
    ("Medical Images", images),
    ("AI Predictions", predictions),
    ("AI Recommendations", recommendations),
    ("Health Scores", health),
    ("Explainable AI", xai),
    ("Patient Allergies", allergies),
    ("Vaccinations", vaccinations),
    ("Hospital Rooms", rooms),
    ("Beds", beds),
    ("Insurance", insurance),
    ("Medications", medications)
]

for name, df in datasets:
    check_pk(df, name)


print("\n" + "=" * 80)
print("DUPLICATE ROW CHECK")
print("=" * 80)

for name, df in datasets:
    check_duplicates(df, name)


print("\n" + "=" * 80)
print("MISSING VALUE CHECK")
print("=" * 80)

for name, df in datasets:
    check_nulls(df, name)


print("\n" + "=" * 80)
print("FOREIGN KEY CHECK")
print("=" * 80)

check_fk(
    admissions,
    "Patient_ID",
    patients,
    "Patient_ID",
    "Admissions -> Patients"
)

check_fk(
    doctors,
    "Department_ID",
    departments,
    "Department_ID",
    "Doctors -> Departments"
)

check_fk(
    diagnoses,
    "Patient_ID",
    patients,
    "Patient_ID",
    "Diagnoses -> Patients"
)

check_fk(
    diagnoses,
    "Admission_ID",
    admissions,
    "Admission_ID",
    "Diagnoses -> Admissions"
)

check_fk(
    diagnoses,
    "Disease_ID",
    diseases,
    "Disease_ID",
    "Diagnoses -> Diseases"
)

check_fk(
    diagnoses,
    "Doctor_ID",
    doctors,
    "Doctor_ID",
    "Diagnoses -> Doctors"
)

check_fk(
    vitals,
    "Patient_ID",
    patients,
    "Patient_ID",
    "Vital Signs -> Patients"
)

check_fk(
    vitals,
    "Admission_ID",
    admissions,
    "Admission_ID",
    "Vital Signs -> Admissions"
)

check_fk(
    labs,
    "Patient_ID",
    patients,
    "Patient_ID",
    "Lab Results -> Patients"
)

check_fk(
    labs,
    "Admission_ID",
    admissions,
    "Admission_ID",
    "Lab Results -> Admissions"
)

check_fk(
    discharge,
    "Admission_ID",
    admissions,
    "Admission_ID",
    "Discharge Summary -> Admissions"
)

check_fk(
    imaging,
    "Admission_ID",
    admissions,
    "Admission_ID",
    "Imaging Reports -> Admissions"
)

check_fk(
    predictions,
    "Patient_ID",
    patients,
    "Patient_ID",
    "AI Predictions -> Patients"
)

check_fk(
    recommendations,
    "AI_Prediction_ID",
    predictions,
    "AI_Prediction_ID",
    "AI Recommendations -> AI Predictions"
)

check_fk(
    xai,
    "AI_Prediction_ID",
    predictions,
    "AI_Prediction_ID",
    "Explainable AI -> AI Predictions"
)

print("\n" + "=" * 80)
print("VALIDATION COMPLETED")
print("=" * 80)