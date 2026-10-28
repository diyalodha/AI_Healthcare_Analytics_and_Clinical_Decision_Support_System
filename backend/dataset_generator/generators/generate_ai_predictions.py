"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File : generate_ai_predictions.py

Purpose :
Generate AI clinical prediction dataset.

Input:
patients.csv
diagnoses.csv
vital_signs.csv
lab_results.csv

Output:
ai_predictions.csv

Author : Diya Lodha & Team
===========================================================
"""


import os
import sys
import random
import numpy as np
import pandas as pd


# ==========================================================
# Add Parent Directory
# ==========================================================

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PARENT_DIR = os.path.dirname(
    CURRENT_DIR
)


if PARENT_DIR not in sys.path:
    sys.path.insert(
        0,
        PARENT_DIR
    )


import config


from utils import (
    generate_uuid,
    save_dataframe,
    show_progress
)



# ==========================================================
# Files
# ==========================================================


PATIENT_FILE = os.path.join(
    config.SYNTHETIC_DIR,
    "patients.csv"
)


DIAGNOSIS_FILE = os.path.join(
    config.SYNTHETIC_DIR,
    "diagnoses.csv"
)


VITAL_FILE = os.path.join(
    config.SYNTHETIC_DIR,
    "vital_signs.csv"
)


LAB_FILE = os.path.join(
    config.SYNTHETIC_DIR,
    "lab_results.csv"
)



# ==========================================================
# Prediction Categories
# ==========================================================


PREDICTIONS = [

    "Diabetes Risk Prediction",
    "Cardiac Disease Risk Prediction",
    "Kidney Disease Risk Prediction",
    "Respiratory Disease Risk Prediction",
    "Hospital Readmission Risk",
    "ICU Admission Risk",
    "Mortality Risk Prediction"

]



# ==========================================================
# Generate AI Predictions
# ==========================================================


def generate_ai_predictions(output_filename="ai_predictions.csv", num_predictions=None):


    show_progress(
        "Generating AI Predictions Dataset"
    )



    patients = pd.read_csv(
        PATIENT_FILE
    )


    diagnoses = pd.read_csv(
        DIAGNOSIS_FILE
    )


    vitals = pd.read_csv(
        VITAL_FILE
    )


    labs = pd.read_csv(
        LAB_FILE
    )



    records = []

    target_count = (
        config.NUM_AI_PREDICTIONS
        if num_predictions is None
        else int(num_predictions)
    )

    if target_count < 1:
        raise ValueError("num_predictions must be at least 1")

    # Group source rows by patient so every reference belongs
    # to the patient selected for that prediction.
    diagnosis_indices = diagnoses.groupby("Patient_ID").indices
    vital_indices = vitals.groupby("Patient_ID").indices
    lab_indices = labs.groupby("Patient_ID").indices

    eligible_patient_ids = [
        patient_id
        for patient_id in patients["Patient_ID"].tolist()
        if patient_id in diagnosis_indices
        and patient_id in vital_indices
        and patient_id in lab_indices
    ]

    if not eligible_patient_ids:
        raise ValueError(
            "No patients have diagnoses, vital signs, and lab results."
        )

    patients_by_id = patients.set_index("Patient_ID", drop=False)

    selected_patient_ids = np.random.choice(
        eligible_patient_ids,
        size=target_count,
        replace=True
    )

    for i in range(target_count):

        patient_id = selected_patient_ids[i]
        patient = patients_by_id.loc[patient_id]

        diagnosis = diagnoses.iloc[
            np.random.choice(diagnosis_indices[patient_id])
        ]

        vital = vitals.iloc[
            np.random.choice(vital_indices[patient_id])
        ]

        lab = labs.iloc[
            np.random.choice(lab_indices[patient_id])
        ]

        risk_score = round(
            random.uniform(
                0.05,
                0.95
            ),
            3
        )



        prediction = (

            "High Risk"
            if risk_score > 0.70

            else

            "Medium Risk"
            if risk_score > 0.40

            else

            "Low Risk"

        )



        record = {



            "AI_Prediction_ID":
                generate_uuid(),


            "Patient_ID":
                patient["Patient_ID"],


            "Diagnosis_ID":
                diagnosis["Diagnosis_ID"],


            "Prediction_Type":
                random.choice(
                    PREDICTIONS
                ),


            "Model_Name":
                random.choice(
                    [
                    "Random Forest",
                    "XGBoost",
                    "Neural Network",
                    "Logistic Regression"
                    ]
                ),


            "Risk_Score":
                risk_score,


            "Prediction_Result":
                prediction,


            "Confidence_Score":
                round(
                    random.uniform(
                        0.70,
                        0.99
                    ),
                    3
                ),


            "Input_Vital_ID":
                vital["Vital_Sign_ID"],


            "Input_Lab_Result_ID":
                lab["Lab_Result_ID"],


            "Prediction_Date":
                vital["Recorded_Time"],


            "Clinical_Recommendation":

                (
                "Review patient history, "
                "monitor clinical parameters "
                "and follow physician guidance."
                )



        }



        records.append(
            record
        )



        if (i + 1) % 50000 == 0:

            print(
                f"{i+1} AI predictions generated"
            )



    dataframe = pd.DataFrame(
        records
    )



    save_dataframe(
        dataframe,
        output_filename
    )



    print(
        f"Generated {len(dataframe)} AI predictions"
    )



# ==========================================================
# Run
# ==========================================================


if __name__ == "__main__":

    generate_ai_predictions()