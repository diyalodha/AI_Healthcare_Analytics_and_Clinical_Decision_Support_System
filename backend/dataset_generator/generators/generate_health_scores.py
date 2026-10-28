"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File : generate_health_scores.py

Purpose :
Generate AI-based patient health score dataset.

Input:
patients.csv
vital_signs.csv
lab_results.csv

Output:
health_scores.csv

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


VITAL_FILE = os.path.join(
    config.SYNTHETIC_DIR,
    "vital_signs.csv"
)


LAB_FILE = os.path.join(
    config.SYNTHETIC_DIR,
    "lab_results.csv"
)



# ==========================================================
# Generate Health Scores
# ==========================================================


def generate_health_scores():


    show_progress(
        "Generating Patient Health Scores Dataset"
    )



    patients = pd.read_csv(
        PATIENT_FILE
    )


    vitals = pd.read_csv(
        VITAL_FILE
    )


    labs = pd.read_csv(
        LAB_FILE
    )



    records = []

    patient_index = np.random.randint(
        0,
        len(patients),
        config.NUM_HEALTH_SCORE
    )

    vital_index = np.random.randint(
        0,
        len(vitals),
        config.NUM_HEALTH_SCORE
    )

    lab_index = np.random.randint(
        0,
        len(labs),
        config.NUM_HEALTH_SCORE
    )


    lab_index = np.random.randint(
        0,
        len(labs),
        config.NUM_HEALTH_SCORE
    )



    for i in range(
        config.NUM_HEALTH_SCORE
    ):



        patient = patients.iloc[
            patient_index[i]
      ]


        vital = vitals.iloc[
            vital_index[i]
        ]


        lab = labs.iloc[
            lab_index[i]
        ]



        health_score = random.randint(
            1,
            100
        )



        risk_level = (

            "High"

            if health_score < 40

            else

            "Medium"

            if health_score < 70

            else

            "Low"

        )



        record = {



            "Health_Score_ID":
                generate_uuid(),


            "Patient_ID":
                patient["Patient_ID"],


            "Vital_Sign_ID":
                vital["Vital_Sign_ID"],


            "Lab_Result_ID":
                lab["Lab_Result_ID"],


            "Overall_Health_Score":
                health_score,


            "Risk_Level":
                risk_level,


            "Blood_Pressure_Status":
                random.choice(
                    [
                    "Normal",
                    "Elevated",
                    "High"
                    ]
                ),


            "BMI_Category":
                random.choice(
                    [
                    "Underweight",
                    "Normal",
                    "Overweight",
                    "Obese"
                    ]
                ),


            "Chronic_Disease_Status":
                random.choice(
                    [
                    "No Chronic Disease",
                    "Single Condition",
                    "Multiple Conditions"
                    ]
                ),


            "Monitoring_Required":
                True
                if health_score < 50
                else False,


            "Generated_Date":
                vital["Recorded_Time"]



        }



        records.append(
            record
        )



        if (i + 1) % 20000 == 0:

            print(
                f"{i+1} health scores generated"
            )



    dataframe = pd.DataFrame(
        records
    )



    save_dataframe(
        dataframe,
        "health_scores.csv"
    )



    print(
        f"Generated {len(dataframe)} health scores"
    )



# ==========================================================
# Run
# ==========================================================


if __name__ == "__main__":

    generate_health_scores()