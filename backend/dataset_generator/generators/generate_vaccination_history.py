"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File : generate_vaccination_history.py

Purpose :
Generate ground-truth based vaccination history dataset.

Input:
patients.csv

Output:
vaccination_history.csv

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
# Patient File
# ==========================================================

PATIENT_FILE = os.path.join(
    config.SYNTHETIC_DIR,
    "patients.csv"
)



# ==========================================================
# Ground Truth Vaccines
# ==========================================================

VACCINES = [

    {
        "Vaccine_Name":"BCG",
        "Disease_Prevented":"Tuberculosis",
        "Dose_Number":1
    },

    {
        "Vaccine_Name":"Polio Vaccine",
        "Disease_Prevented":"Polio",
        "Dose_Number":1
    },

    {
        "Vaccine_Name":"DPT",
        "Disease_Prevented":"Diphtheria Tetanus Pertussis",
        "Dose_Number":1
    },

    {
        "Vaccine_Name":"Hepatitis B",
        "Disease_Prevented":"Hepatitis B",
        "Dose_Number":1
    },

    {
        "Vaccine_Name":"MMR",
        "Disease_Prevented":"Measles Mumps Rubella",
        "Dose_Number":1
    },

    {
        "Vaccine_Name":"Influenza Vaccine",
        "Disease_Prevented":"Influenza",
        "Dose_Number":1
    },

    {
        "Vaccine_Name":"COVID-19 Vaccine",
        "Disease_Prevented":"COVID-19",
        "Dose_Number":2
    },

    {
        "Vaccine_Name":"Pneumococcal Vaccine",
        "Disease_Prevented":"Pneumonia",
        "Dose_Number":1
    }

]



# ==========================================================
# Generate Vaccination History
# ==========================================================


def generate_vaccination_history():


    show_progress(
        "Generating Vaccination History Dataset"
    )


    patients = pd.read_csv(
        PATIENT_FILE
    )


    records = []



    for _, patient in patients.iterrows():


        # Probability based on healthcare behaviour

        if random.random() < 0.75:


            vaccine_count = random.randint(
                2,
                5
            )


            selected_vaccines = random.sample(
                VACCINES,
                vaccine_count
            )



            for vaccine in selected_vaccines:


                vaccination_date = datetime.now() - timedelta(
                    days=random.randint(
                        30,
                        6000
                    )
                )


                record = {


                    "Vaccination_ID":
                        generate_uuid(),


                    "Patient_ID":
                        patient["Patient_ID"],


                    "Vaccine_Name":
                        vaccine["Vaccine_Name"],


                    "Disease_Prevented":
                        vaccine["Disease_Prevented"],


                    "Dose_Number":
                        vaccine["Dose_Number"],


                    "Vaccination_Date":
                        vaccination_date.date(),


                    "Vaccination_Status":
                        random.choice(
                            [
                            "Completed",
                            "Completed",
                            "Pending"
                            ]
                        ),


                    "Administered_By":
                        "Hospital Vaccination Center"


                }


                records.append(
                    record
                )



    dataframe = pd.DataFrame(
        records
    )


    save_dataframe(
        dataframe,
        "vaccination_history.csv"
    )


    print(
        f"Generated {len(dataframe)} vaccination records"
    )



# ==========================================================
# Run
# ==========================================================

if __name__ == "__main__":

    generate_vaccination_history()