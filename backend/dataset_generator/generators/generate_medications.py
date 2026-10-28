"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File : generate_medications.py

Purpose :
Generate ground-truth based medication dataset.

Input:
reference/medications_master.csv

Output:
datasets/synthetic/medications.csv

Author : Diya Lodha & Team
===========================================================
"""


import os
import sys
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
# Reference File
# ==========================================================

REFERENCE_FILE = os.path.join(
    PARENT_DIR,
    "reference",
    "medications_master.csv"
)



# ==========================================================
# Generate Medications
# ==========================================================

def generate_medications():

    show_progress(
        "Generating Medication Dataset"
    )


    # Load Master Medication Data

    medications_df = pd.read_csv(
        REFERENCE_FILE
    )


    # Limit according to config

    medications_df = medications_df.head(
        config.NUM_MEDICATIONS
    )



    records = []



    for _, medication in medications_df.iterrows():


        record = {


            "Medication_ID":
                generate_uuid(),


            "Medication_Name":
                medication["Medication_Name"],


            "Generic_Name":
                medication["Generic_Name"],


            "Drug_Class":
                medication["Drug_Class"],


            "Used_For":
                medication["Used_For"],


            "Route":
                medication["Route"],


            "Dosage_Form":
                medication["Dosage_Form"],


            "Strength":
                medication["Strength"],


            "Risk_Level":
                medication["Risk_Level"]


        }


        records.append(
            record
        )



    dataframe = pd.DataFrame(
        records
    )



    save_dataframe(
        dataframe,
        "medications.csv"
    )



    print(
        f"Generated {len(dataframe)} medications"
    )



# ==========================================================
# Run
# ==========================================================


if __name__ == "__main__":

    generate_medications()