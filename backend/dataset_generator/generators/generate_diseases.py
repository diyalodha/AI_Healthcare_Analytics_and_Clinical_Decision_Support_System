"""
===========================================================
Project : AI Healthcare Analytics & Clinical Decision
          Support System

File : generate_diseases.py

Purpose :
Generate ground-truth based disease dataset.

Input:
reference/diseases_master.csv

Output:
datasets/synthetic/diseases.csv

Author : Diya Lodha & Team
===========================================================
"""


import os
import sys
import pandas as pd


# ==========================================================
# Add Parent Directory Path
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
# Reference File Path
# ==========================================================

REFERENCE_FILE = os.path.join(
    PARENT_DIR,
    "reference",
    "diseases_master.csv"
)



# ==========================================================
# Generate Diseases
# ==========================================================

def generate_diseases():

    show_progress(
        "Generating Disease Dataset"
    )


    # ------------------------------------------------------
    # Load Master Disease Data
    # ------------------------------------------------------

    diseases_df = pd.read_csv(
        REFERENCE_FILE
    )


    # ------------------------------------------------------
    # Limit According to Config
    # ------------------------------------------------------

    diseases_df = diseases_df.head(
        config.NUM_DISEASES
    )



    records = []


    for _, disease in diseases_df.iterrows():


        record = {


            "Disease_ID":
                generate_uuid(),


            "Disease_Name":
                disease["Disease_Name"],


            "Disease_Category":
                disease["Disease_Category"],


            "ICD_Code":
                disease["ICD_Code"],


            "Description":
                disease["Description"],


            "Risk_Level":
                disease["Risk_Level"],


            "Chronic_Status":
                disease["Chronic_Status"],


            "Common_Age_Group":
                disease["Common_Age_Group"],


            "Gender_Affected":
                disease["Gender_Affected"],


            "Treatable":
                disease["Treatable"]

        }


        records.append(record)



    dataframe = pd.DataFrame(
        records
    )


    save_dataframe(
        dataframe,
        "diseases.csv"
    )


    print(
        f"Generated {len(dataframe)} diseases"
    )



# ==========================================================
# Run
# ==========================================================


if __name__ == "__main__":

    generate_diseases()