"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File : generate_icu_stays.py

Purpose :
Generate ICU stay records based on hospital workflow.

Input:
admissions.csv
doctors.csv
departments.csv

Output:
icu_stays.csv

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


DOCTOR_FILE = os.path.join(
    config.SYNTHETIC_DIR,
    "doctors.csv"
)


DEPARTMENT_FILE = os.path.join(
    config.SYNTHETIC_DIR,
    "departments.csv"
)



# ==========================================================
# Generate ICU Stay
# ==========================================================


def generate_icu_stays():


    show_progress(
        "Generating ICU Stay Dataset"
    )



    admissions = pd.read_csv(
        ADMISSION_FILE
    )


    doctors = pd.read_csv(
        DOCTOR_FILE
    )


    departments = pd.read_csv(
        DEPARTMENT_FILE
    )



    records = []



    for i in range(
        config.NUM_ICU_STAYS
    ):



        admission = admissions.sample(
            1
        ).iloc[0]


        doctor = doctors.sample(
            1
        ).iloc[0]


        icu_department = departments[
            departments["Department_Code"] == "ICU"
        ]



        if len(icu_department) > 0:

            department_id = (
                icu_department.iloc[0]
                ["Department_ID"]
            )

        else:

            department_id = None



        record = {



            "ICU_Stay_ID":
                generate_uuid(),


            "Patient_ID":
                admission["Patient_ID"],


            "Admission_ID":
                admission["Admission_ID"],


            "ICU_Department_ID":
                department_id,


            "Doctor_ID":
                doctor["Doctor_ID"],


            "ICU_Admission_Date":
                admission["Admission_Date"],


            "ICU_Discharge_Date":
                admission["Discharge_Date"],


            "ICU_Type":
                random.choice(
                    [
                    "Medical ICU",
                    "Surgical ICU",
                    "Cardiac ICU",
                    "Neonatal ICU"
                    ]
                ),


            "Ventilator_Required":
                random.choice(
                    [
                    True,
                    False
                    ]
                ),


            "Severity_Level":
                random.choice(
                    [
                    "Moderate",
                    "Severe",
                    "Critical"
                    ]
                ),


            "Length_of_Stay_Days":
                random.randint(
                    1,
                    30
                ),


            "Outcome":
                random.choice(
                    [
                    "Recovered",
                    "Transferred",
                    "Expired"
                    ]
                )


        }


        records.append(
            record
        )



        if (i + 1) % 10000 == 0:

            print(
                f"{i+1} ICU stays generated"
            )



    dataframe = pd.DataFrame(
        records
    )



    save_dataframe(
        dataframe,
        "icu_stays.csv"
    )



    print(
        f"Generated {len(dataframe)} ICU stays"
    )



# ==========================================================
# Run
# ==========================================================


if __name__ == "__main__":

    generate_icu_stays()