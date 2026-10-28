"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File : generate_discharge_summary.py

Purpose :
Generate discharge summary records.

Input:
admissions.csv
diagnoses.csv
doctors.csv

Output:
discharge_summary.csv

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

ADMISSION_FILE = os.path.join(
    config.SYNTHETIC_DIR,
    "admissions.csv"
)

DIAGNOSIS_FILE = os.path.join(
    config.SYNTHETIC_DIR,
    "diagnoses.csv"
)

DOCTOR_FILE = os.path.join(
    config.SYNTHETIC_DIR,
    "doctors.csv"
)

DISEASE_FILE = os.path.join(
    config.SYNTHETIC_DIR,
    "diseases.csv"
)

# ==========================================================
# Static Values
# ==========================================================

DISCHARGE_CONDITIONS = [
    "Stable",
    "Improved",
    "Critical",
    "Referred"
]

READMISSION_RISK = [
    "Low",
    "Medium",
    "High"
]

HOSPITAL_COURSE = (
    "Patient admitted for treatment. "
    "Investigations completed. "
    "Treatment provided and patient "
    "discharged after clinical improvement."
)

FOLLOW_UP = (
    "Follow up with treating physician "
    "and continue prescribed medications."
)



# ==========================================================
# Generate Discharge Summary
# ==========================================================

def generate_discharge_summary():

    show_progress(
        "Generating Discharge Summary Dataset"
    )

    admissions = pd.read_csv(
        ADMISSION_FILE
    )

    diagnoses = pd.read_csv(
        DIAGNOSIS_FILE
    )

    doctors = pd.read_csv(
        DOCTOR_FILE
    )

    diseases = pd.read_csv(
    DISEASE_FILE
    )

    disease_lookup = dict(
    zip(
        diseases["Disease_ID"],
        diseases["Disease_Name"]
    )
)


    records = []



    total_records = config.NUM_DISCHARGE_SUMMARY



    for start in range(
        0,
        total_records,
        config.DISCHARGE_CHUNK_SIZE
    ):

        chunk_size = min(
            config.DISCHARGE_CHUNK_SIZE,
            total_records - start
        )



        admission_index = np.random.randint(
            0,
            len(admissions),
            chunk_size
        )

        diagnosis_index = np.random.randint(
            0,
            len(diagnoses),
            chunk_size
        )

        doctor_index = np.random.randint(
            0,
            len(doctors),
            chunk_size
        )



        for i in range(chunk_size):

            admission = admissions.iloc[
                admission_index[i]
            ]

            diagnosis = diagnoses.iloc[
                diagnosis_index[i]
            ]

            doctor = doctors.iloc[
                doctor_index[i]
            ]

            record = {

                "Discharge_Summary_ID":
                    generate_uuid(),

                "Patient_ID":
                    admission["Patient_ID"],

                "Admission_ID":
                    admission["Admission_ID"],

                "Diagnosis_ID":
                    diagnosis["Diagnosis_ID"],

                "Doctor_ID":
                    doctor["Doctor_ID"],

                "Discharge_Date":
                    admission["Discharge_Date"],

                "Final_Diagnosis":
                    disease_lookup[
                        diagnosis["Disease_ID"]
                    ],

                "Hospital_Course":
                    HOSPITAL_COURSE,

                "Discharge_Condition":
                    random.choice(
                        DISCHARGE_CONDITIONS
                    ),

                "Follow_Up_Instructions":
                    FOLLOW_UP,

                "Readmission_Risk":
                    random.choice(
                        READMISSION_RISK
                    )

            }

            records.append(
                record
            )

        print(
            f"{min(start + chunk_size, total_records)} discharge summaries generated"
        )



    # ==========================================================
    # Convert to DataFrame
    # ==========================================================

    dataframe = pd.DataFrame(
        records
    )



    # ==========================================================
    # Save CSV
    # ==========================================================

    save_dataframe(
        dataframe,
        "discharge_summary.csv"
    )



    print(
        f"Generated {len(dataframe)} discharge summaries"
    )



# ==========================================================
# Run
# ==========================================================

if __name__ == "__main__":

    generate_discharge_summary()