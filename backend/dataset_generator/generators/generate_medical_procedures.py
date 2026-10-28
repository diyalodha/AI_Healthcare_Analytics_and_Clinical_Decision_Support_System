"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File : generate_medical_procedures.py

Purpose :
Generate medical procedure records.

Optimized version for faster generation.

Output:
medical_procedures.csv

Records:
250000

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
# Procedure Master Data
# ==========================================================


PROCEDURES = [

    "Appendectomy",
    "Cardiac Catheterization",
    "MRI Scan",
    "CT Scan",
    "Ultrasound",
    "Endoscopy",
    "Colonoscopy",
    "Dialysis",
    "Chemotherapy",
    "Physiotherapy",
    "Blood Transfusion",
    "Fracture Surgery",
    "Cataract Surgery",
    "Angioplasty",
    "Biopsy"

]



# ==========================================================
# Generate Medical Procedures
# ==========================================================


def generate_medical_procedures():


    show_progress(
        "Generating Medical Procedures Dataset"
    )



    patients = pd.read_csv(
        PATIENT_FILE
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



    patient_ids = patients[
        "Patient_ID"
    ].values


    admission_ids = admissions[
        "Admission_ID"
    ].values


    doctor_ids = doctors[
        "Doctor_ID"
    ].values


    department_ids = departments[
        "Department_ID"
    ].values



    records = []



    total = config.NUM_MEDICAL_PROCEDURES



    for start in range(
        0,
        total,
        config.GENERATION_CHUNK_SIZE
    ):


        size = min(
            config.GENERATION_CHUNK_SIZE,
            total-start
        )



        patient_sample = np.random.choice(
            patient_ids,
            size=size
        )


        admission_sample = np.random.choice(
            admission_ids,
            size=size
        )


        doctor_sample = np.random.choice(
            doctor_ids,
            size=size
        )


        department_sample = np.random.choice(
            department_ids,
            size=size
        )



        for i in range(size):


            procedure = random.choice(
                PROCEDURES
            )



            records.append(

                {


                "Procedure_ID":
                    generate_uuid(),


                "Patient_ID":
                    patient_sample[i],


                "Admission_ID":
                    admission_sample[i],


                "Doctor_ID":
                    doctor_sample[i],


                "Department_ID":
                    department_sample[i],


                "Procedure_Name":
                    procedure,


                "Procedure_Type":
                    random.choice(
                        [
                        "Diagnostic",
                        "Surgical",
                        "Therapeutic"
                        ]
                    ),


                "Procedure_Date":
                    str(
                        pd.Timestamp(
                            random.randint(
                                1420070400,
                                1767139200
                            ),
                            unit="s"
                        ).date()
                    ),


                "Anesthesia_Used":
                    random.choice(
                        [
                        "Yes",
                        "No"
                        ]
                    ),


                "Procedure_Status":
                    random.choice(
                        [
                        "Completed",
                        "Scheduled",
                        "Cancelled"
                        ]
                    ),


                "Cost":
                    round(
                        random.uniform(
                            1000,
                            200000
                        ),
                        2
                    ),


                "Notes":
                    "Procedure performed successfully"



                }

            )



        print(
            f"{len(records)} procedures generated"
        )



    dataframe = pd.DataFrame(
        records
    )



    save_dataframe(
        dataframe,
        "medical_procedures.csv"
    )



    print(
        f"Generated {len(dataframe)} medical procedures"
    )



# ==========================================================
# Run
# ==========================================================


if __name__ == "__main__":

    generate_medical_procedures()