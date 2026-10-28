"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File : generate_diagnoses.py

Purpose :
Generate ground-truth based diagnosis records.

Input:
patients.csv
admissions.csv
diseases.csv
doctors.csv

Output:
diagnoses.csv

Author : Diya Lodha & Team
===========================================================
"""


import os
import sys
import random
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


DISEASE_FILE = os.path.join(
    config.SYNTHETIC_DIR,
    "diseases.csv"
)


DOCTOR_FILE = os.path.join(
    config.SYNTHETIC_DIR,
    "doctors.csv"
)



# ==========================================================
# Generate Diagnoses
# ==========================================================


def generate_diagnoses():


    show_progress(
        "Generating Diagnosis Dataset"
    )


    admissions = pd.read_csv(
        ADMISSION_FILE
    )


    diseases = pd.read_csv(
        DISEASE_FILE
    )


    doctors = pd.read_csv(
        DOCTOR_FILE
    )



    records = []



    for i in range(
        config.NUM_DIAGNOSES
    ):


        admission = admissions.sample(
            1
        ).iloc[0]


        disease = diseases.sample(
            1
        ).iloc[0]


        doctor = doctors.sample(
            1
        ).iloc[0]



        record = {


            "Diagnosis_ID":
                generate_uuid(),


            "Patient_ID":
                admission["Patient_ID"],


            "Admission_ID":
                admission["Admission_ID"],


            "Disease_ID":
                disease["Disease_ID"],


            "Diagnosis_Date":
                admission["Admission_Date"],


            "Diagnosis_Type":
                random.choice(
                    [
                    "Primary",
                    "Secondary",
                    "Chronic Condition",
                    "Suspected"
                    ]
                ),


            "Diagnosis_Status":
                random.choice(
                    [
                    "Confirmed",
                    "Under Evaluation",
                    "Resolved"
                    ]
                ),


            "Doctor_ID":
                doctor["Doctor_ID"],


            "Severity":
                random.choice(
                    [
                    "Mild",
                    "Moderate",
                    "Severe"
                    ]
                ),


            "Notes":
                "Diagnosis recorded during clinical evaluation"


        }


        records.append(
            record
        )


        if (i+1) % 50000 == 0:

            print(
                f"{i+1} diagnoses generated"
            )



    dataframe = pd.DataFrame(
        records
    )



    save_dataframe(
        dataframe,
        "diagnoses.csv"
    )


    print(
        f"Generated {len(dataframe)} diagnoses"
    )



# ==========================================================
# Run
# ==========================================================

if __name__ == "__main__":

    generate_diagnoses()