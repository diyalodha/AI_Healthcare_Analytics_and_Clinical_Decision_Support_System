"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File : generate_vital_signs.py

Purpose :
Generate patient vital sign records.

Optimized version for large-scale generation.

Output:
vital_signs.csv

Records:
2,000,000

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



# ==========================================================
# Generate Vital Signs
# ==========================================================


def generate_vital_signs():


    show_progress(
        "Generating Vital Signs Dataset"
    )



    patients = pd.read_csv(
        PATIENT_FILE
    )


    admissions = pd.read_csv(
        ADMISSION_FILE
    )



    patient_ids = patients[
        "Patient_ID"
    ].values


    admission_ids = admissions[
        "Admission_ID"
    ].values



    records = []



    total = config.NUM_VITAL_SIGNS



    for start in range(
        0,
        total,
        config.VITAL_CHUNK_SIZE
    ):


        size = min(
            config.VITAL_CHUNK_SIZE,
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



        heart_rates = np.random.randint(
            60,
            120,
            size
        )


        systolic_bp = np.random.randint(
            90,
            180,
            size
        )


        diastolic_bp = np.random.randint(
            50,
            110,
            size
        )


        temperatures = np.round(
            np.random.uniform(
                36,
                39.5,
                size
            ),
            1
        )


        oxygen_levels = np.round(
            np.random.uniform(
                85,
                100,
                size
            ),
            1
        )


        respiratory_rates = np.random.randint(
            12,
            35,
            size
        )


        weights = np.round(
            np.random.uniform(
                40,
                120,
                size
            ),
            1
        )



        for i in range(size):


            oxygen_status = (

                "Critical"

                if oxygen_levels[i] < 90

                else

                "Normal"

            )



            records.append(

                {


                "Vital_Sign_ID":
                    generate_uuid(),


                "Patient_ID":
                    patient_sample[i],


                "Admission_ID":
                    admission_sample[i],


                "Heart_Rate":

                    int(
                        heart_rates[i]
                    ),


                "Systolic_BP":

                    int(
                        systolic_bp[i]
                    ),


                "Diastolic_BP":

                    int(
                        diastolic_bp[i]
                    ),


                "Temperature":

                    temperatures[i],


                "Oxygen_Saturation":

                    oxygen_levels[i],


                "Respiratory_Rate":

                    int(
                        respiratory_rates[i]
                    ),


                "Weight":

                    weights[i],


                "Blood_Sugar":

                    round(
                        random.uniform(
                            70,
                            250
                        ),
                        2
                    ),


                "Oxygen_Status":

                    oxygen_status,


                "Recorded_Time":

                    str(
                        pd.Timestamp.now()
                    )



                }

            )



        print(
            f"{len(records)} vital signs generated"
        )



    dataframe = pd.DataFrame(
        records
    )



    save_dataframe(
        dataframe,
        "vital_signs.csv"
    )



    print(
        f"Generated {len(dataframe)} vital sign records"
    )



# ==========================================================
# Run
# ==========================================================


if __name__ == "__main__":

    generate_vital_signs()