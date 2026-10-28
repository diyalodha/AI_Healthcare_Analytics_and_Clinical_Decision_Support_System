"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File : generate_admissions.py

Purpose :
Generate ground-truth hospital admission records.

Input:
patients.csv
departments.csv
doctors.csv

Output:
admissions.csv

Author : Diya Lodha & Team
===========================================================
"""


import os
import sys
import random
import pandas as pd

from datetime import datetime, timedelta



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
# File Paths
# ==========================================================

PATIENT_FILE = os.path.join(
    config.SYNTHETIC_DIR,
    "patients.csv"
)


DEPARTMENT_FILE = os.path.join(
    config.SYNTHETIC_DIR,
    "departments.csv"
)


DOCTOR_FILE = os.path.join(
    config.SYNTHETIC_DIR,
    "doctors.csv"
)



# ==========================================================
# Generate Admissions
# ==========================================================

def generate_admissions():


    show_progress(
        "Generating Admissions Dataset"
    )


    patients = pd.read_csv(
        PATIENT_FILE
    )


    departments = pd.read_csv(
        DEPARTMENT_FILE
    )


    doctors = pd.read_csv(
        DOCTOR_FILE
    )



    records = []



    # Number of admissions from config

    for i in range(
        config.NUM_ADMISSIONS
    ):


        patient = patients.sample(
            1
        ).iloc[0]


        department = departments.sample(
            1
        ).iloc[0]


        doctor = doctors.sample(
            1
        ).iloc[0]



        admission_date = datetime.now() - timedelta(
            days=random.randint(
                1,
                4000
            )
        )


        length_of_stay = random.randint(
            1,
            15
        )


        discharge_date = (
            admission_date
            +
            timedelta(
                days=length_of_stay
            )
        )



        record = {


            "Admission_ID":
                generate_uuid(),


            "Patient_ID":
                patient["Patient_ID"],


            "Department_ID":
                department["Department_ID"],


            "Doctor_ID":
                doctor["Doctor_ID"],


            "Admission_Date":
                admission_date.date(),


            "Discharge_Date":
                discharge_date.date(),


            "Admission_Type":
                random.choice(
                    [
                    "Emergency",
                    "Routine",
                    "Referral"
                    ]
                ),


            "Admission_Status":
                random.choice(
                    [
                    "Admitted",
                    "Discharged"
                    ]
                ),


            "Length_of_Stay":
                length_of_stay,


            "Room_Number":
                random.randint(
                    101,
                    999
                ),


            "Payment_Status":
                random.choice(
                    [
                    "Paid",
                    "Pending",
                    "Insurance Covered"
                    ]
                )


        }


        records.append(
            record
        )


        if (i+1) % 50000 == 0:

            print(
                f"{i+1} admissions generated"
            )



    dataframe = pd.DataFrame(
        records
    )



    save_dataframe(
        dataframe,
        "admissions.csv"
    )


    print(
        f"Generated {len(dataframe)} admissions"
    )



# ==========================================================
# Run
# ==========================================================

if __name__ == "__main__":

    generate_admissions()